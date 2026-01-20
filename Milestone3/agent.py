from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# ✅ Correct absolute import
from Parser.instruction_parser import parse_instruction


class AgentState(TypedDict):
    instruction: str
    parsed_steps: list


def parse_step(state: AgentState):
    instruction = state["instruction"]
    steps = parse_instruction(instruction)
    print("Parsed steps:", steps)
    return {"parsed_steps": steps}


graph = StateGraph(AgentState)
graph.add_node("parse_instruction", parse_step)
graph.add_edge(START, "parse_instruction")
graph.add_edge("parse_instruction", END)

agent = graph.compile()


if __name__ == "__main__":
    user_instruction = "Open website and click link"
    result = agent.invoke({"instruction": user_instruction})
    print("\nFinal Result:", result)
