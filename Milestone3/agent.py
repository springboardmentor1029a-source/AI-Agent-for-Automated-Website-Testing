from langgraph.graph import StateGraph, START, END
from instruction_parser import parse_instruction
from workflow import generate_test_steps
from playwright_executor import run_test

def parser_node(state):
    parsed = parse_instruction(state["input"])
    state["parsed_actions"] = parsed
    return state

def generator_node(state):
    steps = generate_test_steps(state["parsed_actions"])
    state["generated_steps"] = steps
    return state

def execution_node(state):
    url = "http://127.0.0.1:5000"
    result = run_test(state["generated_steps"], url)
    state["execution_status"] = result
    return state

def report_node(state):
    return state

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

AGENT = build_agent()

def handle_input(text):
    return AGENT.invoke({"input": text})
