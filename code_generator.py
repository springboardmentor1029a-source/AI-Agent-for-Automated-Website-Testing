# agent/code_generator.py

import os
import json
import re

USE_GEMINI = False  # 🔴 turn OFF unstable Gemini

# -----------------------------
# RULE-BASED FALLBACK (STABLE)
# -----------------------------
def rule_based_generator(text: str) -> dict:
    text = text.lower()
    steps = []

    if "login" in text:
        steps.append({
            "action": "goto",
            "url": "http://127.0.0.1:5000/login"
        })

    if "invalid" in text or "wrong" in text:
        steps.extend([
            {
                "action": "type",
                "selector": "#email",
                "value": "wrong@test.com"
            },
            {
                "action": "type",
                "selector": "#password",
                "value": "12345"
            },
            {
                "action": "click",
                "selector": "button[type=submit]"
            },
            {
                "action": "assert_text",
                "value": "Invalid credentials"
            }
        ])

    if not steps:
        steps.append({
            "action": "goto",
            "url": "http://127.0.0.1:5000"
        })

    return {"steps": steps}


# -----------------------------
# MAIN ENTRY
# -----------------------------
def generate_test_plan(parsed_input: str) -> dict:
    """
    Generates test steps using AI or fallback logic.
    """

    if USE_GEMINI:
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

            prompt = f"""
Convert this instruction into JSON test steps:
\"\"\"{parsed_input}\"\"\"
Return only JSON.
"""
            response = model.generate_content(prompt)
            text = response.text

            text = re.sub(r"```json|```", "", text).strip()
            return json.loads(text)

        except Exception as e:
            # 🔥 auto-fallback
            return rule_based_generator(parsed_input)

    # Default path (SAFE)
    return rule_based_generator(parsed_input)
