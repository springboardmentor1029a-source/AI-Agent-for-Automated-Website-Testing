# agent/graph.py
from langgraph.graph import StateGraph, END
from typing import Literal
from .state import AgentState
from .nodes import (
    parse_instruction_node,
    generate_test_script_node,
    execute_test_node,
    generate_report_node
)


def should_continue_after_parse(state: AgentState) -> Literal["generate", "end"]:
    if state.get("error"):
        print("❌ Error detected, ending workflow")
        return "end"
    
    if not state.get("parsed_steps"):
        print("❌ No steps parsed, ending workflow")
        return "end"
    
    print("✓ Steps parsed successfully, continuing...")
    return "generate"


def should_continue_after_execute(state: AgentState) -> Literal["report", "end"]:
    return "report"


def create_agent_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("parse", parse_instruction_node)
    workflow.add_node("generate", generate_test_script_node)
    workflow.add_node("execute", execute_test_node)
    workflow.add_node("report", generate_report_node)
    
    workflow.set_entry_point("parse")
    
    workflow.add_conditional_edges(
        "parse",
        should_continue_after_parse,
        {
            "generate": "generate",
            "end": "report"
        }
    )
    
    workflow.add_edge("generate", "execute")
    
    workflow.add_conditional_edges(
        "execute",
        should_continue_after_execute,
        {
            "report": "report",
            "end": END
        }
    )
    
    workflow.add_edge("report", END)
    
    return workflow.compile()
