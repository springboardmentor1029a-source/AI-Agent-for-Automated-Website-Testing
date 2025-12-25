from google import genai
from dotenv import load_dotenv
import os, json, re

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "models/gemini-flash-latest"

PROMPT = """
You are a test automation planner.

Website:
{url}

Allowed actions:
- goto (url)
- search (query)
- fill (target, value)
- click (target)
- assert_text (text)

Rules:
1. Output ONLY valid JSON array
2. No explanations
"""

def extract_json(text):
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found")
    return json.loads(match.group())

def ai_parse_instruction(instruction, url):
    response = client.models.generate_content(
        model=MODEL,
        contents=PROMPT.format(url=url) + "\n" + instruction
    )
    return extract_json(response.text)
