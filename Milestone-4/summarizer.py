# agent/summarizer.py

import os
from google import genai

def summarize_text(text: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Summary unavailable (API key missing)."

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-1.0-pro",   # ✅ STABLE MODEL
            contents=f"Summarize the following text in 4–5 lines:\n\n{text[:4000]}"
        )

        return response.text.strip()

    except Exception as e:
        # 🔥 SAFE FALLBACK (never breaks UI)
        sentences = text.split(".")
        return ". ".join(sentences[:4]).strip() + "."
