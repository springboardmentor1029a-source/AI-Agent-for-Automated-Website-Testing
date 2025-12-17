# agent_graph.py

from typing import Dict, Any
from langgraph.graph import StateGraph, END

# ✅ IMPORT EVERYTHING EXPLICITLY
from agent.state import AgentState
from agent.parser_module import parse_user_input
from agent.code_generator import generate_test_plan
from agent.executor import execute_test


# --------- LANGGRAPH NODE ---------

def planning_node(state: AgentState) -> AgentState:
    user_text = state.get("user_input", "")

    parsed_text = parse_user_input(user_text)
    test_plan = generate_test_plan(parsed_text)
    execution_result = execute_test(test_plan)

    return {
        "user_input": user_text,
        "parsed_input": parsed_text,
        "test_plan": test_plan,
        "execution": execution_result
    }


# --------- BUILD GRAPH ---------

graph_builder = StateGraph(AgentState)

graph_builder.add_node("planner", planning_node)
graph_builder.set_entry_point("planner")
graph_builder.add_edge("planner", END)

graph = graph_builder.compile()


# --------- HELPER FOR FLASK ---------

def run_agent(user_input: str) -> Dict[str, Any]:
    initial_state: AgentState = {
        "user_input": user_input,
        "parsed_input": "",
        "test_plan": {},
        "execution": {}
    }

    final_state = graph.invoke(initial_state)
    return final_state
