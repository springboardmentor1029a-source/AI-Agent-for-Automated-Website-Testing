from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "models/gemini-flash-latest"

def find_selector(dom, target):
    prompt = f"""
You are a Playwright selector expert.

DOM:
{dom}

Target:
"{target}"

Return ONLY the best CSS selector.
No explanation.
"""
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text.strip()
