from playwright.sync_api import sync_playwright
import json
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from state import AgentState
from typing import TypedDict, List, Dict
import time



# Initialize the LLM
llm = ChatGroq(model="llama-3.3-70b-versatile",groq_api_key="API_key")

class AgentState(TypedDict):
    instruction: str
    plan: str
    actions: List[str]
    parsed_actions: List[dict]
    observations: List[str]
    logs:List[str]
    current_step_index: int
    final_report: str

# ---  PARSER NODE ---
def parser_node(state: AgentState):
    
    prompt_text = """
    You are a web automation bot. Goal: {instruction}.
    Respond ONLY with JSON list of actions.  No extra text.
    Format: [{{"type": "navigate", "url": "https://www.google.com"}}]
    """

    prompt = ChatPromptTemplate.from_template(prompt_text)
    chain = prompt | llm
    
    # Invoke LLM with current state data
    response = chain.invoke({
        "instruction": state["instruction"],
    })

    # Clean the response (removing json tags if the LLM adds them)
    content = response.content
    clean_json = content.replace("```json", "").replace("```", "").strip()
    
    
    try:
    
        actions = json.loads(clean_json)
        return {
            **state,
            "parsed_actions":actions,
            "current_step_index": 0,  
            "logs": state.get("logs",[]) + [f"AI generated {len(actions)} actions."]
        }
    except Exception as e:
        print(f"CRITICAL PARSE ERROR: {e}")
        return {**state, "error_log": str(e)}




# ---  EXECUTOR NODE ---
def executor_node(state: AgentState):
    actions = state["parsed_actions"]
    idx = state.get("current_step_index", 0)
    new_observations = state.get("observations", [])
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,
        args=["--no-sandbox", "--disable-setuid-sandbox"])
        context = browser.new_context()
        page = context.new_page()

        print("DEBUG: Browser window is now open!")
        
       
     
        while idx < len(actions):
            action = actions[idx]
            log_msg = f"Executing {action['type']} on {action.get('selector', 'URL')}"
            state["logs"].append(log_msg)
            print(log_msg)

            
            try:
                if action["type"] == "navigate":
                    page.goto(action["url"], wait_until="networkidle")
                    new_observations.append(f"Successfully reached {action['url']}.Page title: {page.title()}")
                elif action["type"] == "click":
                    page.click(action["selector"])
                    new_observations.append(f"Clicked on element: {action['selector']}")
                elif action["type"] == "type":
                    page.fill(action["selector"], action["text"])
                    new_observations.append(f"Typed '{action['text']}' into {action['selector']}")
                
                
                idx += 1
                page.wait_for_timeout(2000)
            except Exception as e:
                browser.close()
                page.wait_for_timeout(20000)
                return {**state, "error_log": str(e), "current_step_index": idx}
    
    
    return {
        **state,
        "current_step_index": idx, 
        "observations": new_observations,
        "logs": state.get("logs", []) + [f"Successfully executed {idx} steps."]
    }

    
    

def reporter_node(state: AgentState):
    obs_list = state.get("observations", [])
    obs_html = "".join([f"<li style='margin-bottom: 8px;'>{obs}</li>" for obs in obs_list])
    

    
    report_text = f"""
    <div style="font-family: Arial, sans-serif;">
        <h2 style="color: #00d2ff; border-bottom: 1px solid #333; padding-bottom: 10px;">Testing Report</h2>
        <p><strong>Goal:</strong> {state.get('instruction', 'N/A')}</p>
        <p><strong>Steps Taken:</strong> {state.get('current_step_index', 0)}</p>
        <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
        <h4>Detailed Observations:</h4>
        <ul style="padding-left: 20px;">
            {obs_html if obs_list else "<li>No observations logged.</li>"}
        </ul>
    </div>
    """
    return {"final_report":report_text}
        

def should_continue(state: AgentState):
    if state.get("error") and state.get("retry_count",0) < 3:
        return "parser"

    if state.get("current_step_index") < len(state["parsed_actions"]):
        return "executor"
    return "reporter"

# --- GRAPH DEFINITION ---
workflow = StateGraph(AgentState)

workflow.add_node("parser", parser_node)
workflow.add_node("reporter",reporter_node)
workflow.add_node("executor",executor_node)

workflow.add_edge(START, "parser")
workflow.add_edge("parser", "executor")


workflow.add_conditional_edges(
    "executor",
    should_continue,
    {
        "executor":"executor",
        "parser": "parser",
        "reporter": "reporter"
    }
)
workflow.add_edge("reporter",END)
graph = workflow.compile()

