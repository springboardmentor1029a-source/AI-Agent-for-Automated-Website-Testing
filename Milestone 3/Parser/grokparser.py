import os
import json
from typing import TypedDict
from langgraph.graph import StateGraph, END
from groq import Groq

# Initialize Groq Client0000
# Ensure you have GROQ_API_KEY in your environment variables
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.3-70b-versatile"

class ParserState(TypedDict):
    input: str
    cleaned_text: str
    result: str

def clean_text_node(state: ParserState) -> ParserState:
    prompt = f"""You are a text-cleaning assistant for browser automation.
TASK:
- Fix spelling mistakes
- Remove gibberish
- Normalize commands
- Do NOT add or remove actions

INPUT:
{state["input"]}

OUTPUT:
Return ONLY the cleaned instruction text."""

    # Groq uses the OpenAI-style chat completion API
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=MODEL_NAME,
    )

    return {
        **state,
        "cleaned_text": chat_completion.choices[0].message.content.strip()
    }

def parse_instruction_node(state: ParserState) -> ParserState:
    prompt = f"""You are an instruction parser for browser automation.

Convert the input into a JSON object with an "actions" array.

ALLOWED ACTIONS:
- open (target = full URL)
- click (target = element description)
- fill (target, value)
- search (value, on)
- assert (value)

RULES:
- Output ONLY valid JSON
- No markdown
- No explanation
- One action per step
- If the user says "search X on Y", set: on = Y
- If the user says "go to Y and search X", infer on = Y
- "on" MUST be one of: google, youtube, bing, amazon, generic

INPUT:
{state["cleaned_text"]}
"""

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=MODEL_NAME,
        response_format={"type": "json_object"}
    )

    instructions = json.loads(chat_completion.choices[0].message.content)

    return {
        **state,
        "result": json.dumps(instructions, indent=2)
    }

# --- Graph Construction (Remains the same) ---
graph = StateGraph(ParserState)

graph.add_node("clean_text", clean_text_node)
graph.add_node("parse_instruction", parse_instruction_node)

graph.set_entry_point("clean_text")
graph.add_edge("clean_text", "parse_instruction")


graph.add_edge("parse_instruction", END)

app = graph.compile()