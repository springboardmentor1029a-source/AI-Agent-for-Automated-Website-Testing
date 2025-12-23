from playwright.sync_api import sync_playwright
import json
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from state import AgentState
import time

# Initialize the LLM
llm = ChatGroq(model="llama-3.3-70b-versatile",groq_api_key="API_KEY")

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
                elif action["type"] == "click":
                    page.click(action["selector"])
                elif action["type"] == "type":
                    page.fill(action["selector"], action["text"])
                
                
                idx += 1
                page.wait_for_timeout(2000)
            except Exception as e:
                browser.close()
                page.wait_for_timeout(20000)
                return {**state, "error_log": str(e), "current_step_index": idx}

        browser.close()
    
    return {
        **state,
        "current_step_index": idx, 
        "logs": state.get("logs", []) + [f"Successfully executed {idx} steps."]
    }
def reporter_node(state: AgentState):
    print("\n" + "="*30)
    print("--- Final Testing Report ---")
    print(f"Goal: {state.get('instruction')}")
    print(f"Status: Testing Complete")
    print(f"Steps taken : {len(state.get('parsed_actions',[]))}")
    print("="*30 + "\n")
    return state
        

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

