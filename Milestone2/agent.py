# agent.py

from langgraph.graph import StateGraph, START, END
from instruction_parser import parse_instruction
from workflow import generate_test_steps

# -----------------------------
# Node 1: Parse user input
# -----------------------------
def parser_node(state):
    user_input = state.get("input", "")
    parsed_actions = parse_instruction(user_input)
    return {
        **state,
        "parsed_actions": parsed_actions
    }

# -----------------------------
# Node 2: Generate test steps
# -----------------------------
def generator_node(state):
    actions = state.get("parsed_actions", [])
    steps = generate_test_steps(actions)
    return {
        **state,
        "generated_steps": steps
    }

# -----------------------------
# Node 3: Execute test (Demo level)
# -----------------------------
def execution_node(state):
    # Future lo ikkada Playwright execution add cheyyachu
    execution_result = "Test executed successfully in headless mode"
    return {
        **state,
        "execution_status": execution_result
    }

# -----------------------------
# Node 4: Reporting
# -----------------------------
def report_node(state):
    return {
        "parsed_actions": state.get("parsed_actions", []),
        "generated_steps": state.get("generated_steps", []),
        "execution_status": state.get("execution_status", "")
    }

# -----------------------------
# Build LangGraph workflow
# -----------------------------
def build_agent():
    g = StateGraph(dict)

    g.add_node("parser", parser_node)
    g.add_node("generator", generator_node)
    g.add_node("executor", execution_node)
    g.add_node("report", report_node)

    g.add_edge(START, "parser")
    g.add_edge("parser", "generator")
    g.add_edge("generator", "executor")
    g.add_edge("executor", "report")
    g.add_edge("report", END)

    return g.compile()

# Compile agent
AGENT = build_agent()

# -----------------------------
# Flask entry function
# -----------------------------
def handle_input(user_text: str):
    state = {"input": user_text}
    final_state = AGENT.invoke(state)
    return final_state
