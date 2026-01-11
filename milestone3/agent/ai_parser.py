import json
import os
from dotenv import load_dotenv
from google import genai

# ✅ Load .env safely
load_dotenv()

MODEL = "gemini-2.0-flash"

SYSTEM_PROMPT = """
You are an AI web testing agent.

Given:
- A website URL
- A natural language instruction

Return ONLY valid JSON.
No explanation.
No markdown.

Allowed actions:
- goto (url)
- click (selector)
- fill (selector, value)
- search (query)
- assert_text (text)

Return format:
[
  {"action": "goto", "url": "..."},
  {"action": "search", "query": "..."}
]
"""

def ai_parse_instruction(instruction: str, website_url: str):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("❌ GEMINI_API_KEY not found. Check your .env file.")

    # ✅ Create client ONLY when needed
    client = genai.Client(api_key=api_key)

    prompt = f"""
Website URL:
{website_url}

Instruction:
{instruction}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=SYSTEM_PROMPT + prompt
    )

    text = response.text.strip()

    if not text.startswith("["):
        raise ValueError(f"❌ Invalid AI output:\n{text}")

    return json.loads(text)
