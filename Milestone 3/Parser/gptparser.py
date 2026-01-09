from typing import TypedDict
from langgraph.graph import StateGraph, END
import google.generativeai as genai
import os
import json



genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash-lite")



class ParserState(TypedDict):
    input: str
    cleaned_text: str
    result: str



def clean_text_node(state: ParserState) -> ParserState:
    prompt = f"""
You are a text-cleaning assistant for browser automation.

TASK:
- Fix spelling mistakes
- Remove gibberish
- Normalize commands
- Do NOT add or remove actions

INPUT:
{state["input"]}

OUTPUT:
Return ONLY the cleaned instruction text.
"""

    response = model.generate_content(prompt)

    return {
        **state,
        "cleaned_text": response.text.strip()
    }



def parse_instruction_node(state: ParserState) -> ParserState:
    prompt = f"""
You are an instruction parser for browser automation.

Convert the input into a JSON array of actions.

ALLOWED ACTIONS:
- open (target = full URL if possible)
- click (target = element description)
- search (value = search text)
- fill (target, value)
- assert (value)

RULES:
- Output ONLY valid JSON
- No markdown
- No explanation
- One action per step

INPUT:
{state["cleaned_text"]}
"""

    response = model.generate_content(prompt)

    # Validate + prettify JSON for frontend/logs
    instructions = json.loads(response.text)
    pretty_json = json.dumps(instructions, indent=2)

    return {
        **state,
        "result": pretty_json
    }



graph = StateGraph(ParserState)

graph.add_node("clean_text", clean_text_node)
graph.add_node("parse_instruction", parse_instruction_node)

graph.set_entry_point("clean_text")
graph.add_edge("clean_text", "parse_instruction")
graph.add_edge("parse_instruction", END)

app = graph.compile()