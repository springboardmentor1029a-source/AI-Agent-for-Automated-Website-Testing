# agent.py
from langgraph.graph import StateGraph, START, END
from transformers import pipeline

# --- Load Local Model (NO API KEY REQUIRED) ---
# This loads distilgpt2 model inside the venv
model = pipeline("text-generation", model="distilgpt2")

def local_llm_node(state: dict):
    text = state.get("input", "")

    # Generate response locally
    out = model(
        text,
        max_length=50,
        num_return_sequences=1,
        pad_token_id=50256  # needed to avoid warnings
    )

    reply = out[0]['generated_text']
    return {"response": reply}

# --- Build Graph ---
def build_agent():
    g = StateGraph(dict)
    g.add_node("agent", local_llm_node)
    g.add_edge(START, "agent")
    g.add_conditional_edges("agent", lambda s: END, [END])
    return g.compile()

AGENT = build_agent()

# Main entry used by Flask
def handle_input(user_text: str):
    state = {"input": user_text}
    final_state = AGENT.invoke(state)
    return final_state.get("response", "")
