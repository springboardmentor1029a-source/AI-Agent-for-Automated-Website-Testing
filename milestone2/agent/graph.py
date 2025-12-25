from langgraph.graph import StateGraph, END
from agent.ai_parser import ai_parse_instruction
from agent.test_generator import generate_test
from agent.executor import run_pytest
from agent.stats import update_stats, get_stats

def agent_node(state):
    steps = ai_parse_instruction(state["instruction"], state["website_url"])

    if not steps or steps[0].get("action") != "goto":
        steps.insert(0, {"action": "goto", "url": state["website_url"]})

    for s in steps:
        if s.get("action") == "search" and "query" not in s:
            s["query"] = state["instruction"].split()[-1]

    code = generate_test(steps, state["config"])
    with open("tests/test_generated.py", "w", encoding="utf-8") as f:
        f.write(code)

    result = run_pytest(state["config"])
    update_stats(result["passed"])

    return {
        "steps": steps,
        "result": result,
        "stats": get_stats()
    }

workflow = StateGraph(dict)
workflow.add_node("agent", agent_node)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)

app = workflow.compile()
