from langgraph.graph import StateGraph

class AgentState(dict):
    pass

def process(state):
    text = state["input"]
    return {"output": f"Agent processed input: {text}"}

def run_agent_sync(message):
    graph = StateGraph(AgentState)
    graph.add_node("process", process)
    graph.set_entry_point("process")
    app = graph.compile()
    result = app.invoke({"input": message})
    return result["output"]
