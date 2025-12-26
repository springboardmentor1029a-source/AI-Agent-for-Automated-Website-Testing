import os
import json
import re
import time

try:
    from google import genai
except Exception:
    genai = None

from .playwright_executor import run_test_executor


def extract_search_text(instruction: str) -> str:
    """
    Extract ONLY the search query from natural language.
    Removes action phrases like 'open first product'.
    """
    instruction = instruction.lower()

    # Remove secondary actions
    instruction = re.sub(r"and open.*", "", instruction)
    instruction = re.sub(r"open first.*", "", instruction)
    instruction = re.sub(r"click first.*", "", instruction)

    patterns = [
        r"search for (.+)",
        r"type (.+)"
    ]

    for p in patterns:
        m = re.search(p, instruction)
        if m:
            return m.group(1).strip()

    return instruction.strip()


class GeminiAgent:
    def __init__(self):
        self.client = None
        api_key = os.getenv("GEMINI_API_KEY")

        if genai and api_key:
            try:
                self.client = genai.Client(api_key=api_key)
            except Exception:
                self.client = None

    def invoke(self, state):
        start_time = time.time()

        instruction = state.get("instruction", "")
        target = state.get("target", "")
        mode = state.get("mode", "execute")

        steps = []

        # ---------------------------------
        # TRY GEMINI (OPTIONAL)
        # ---------------------------------
        if self.client:
            try:
                prompt = f"""
Convert the instruction into Playwright steps.

Instruction:
"{instruction}"

Return ONLY JSON array.
Actions allowed: fill, press
"""

                res = self.client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt
                )

                text = re.sub(r"```.*?```", "", res.text, flags=re.S).strip()
                steps = json.loads(text)

            except Exception:
                steps = []

        # ---------------------------------
        # SAFE FALLBACK (CRITICAL)
        # ---------------------------------
        if not steps:
            search_text = extract_search_text(instruction)

            steps = [
                {
                    "action": "fill",
                    "selector": None,
                    "value": search_text
                },
                {
                    "action": "press",
                    "value": "Enter"
                }
            ]

        # ---------------------------------
        # SIMULATE MODE
        # ---------------------------------
        if mode == "simulate":
            return {
                "status": "completed_simulated",
                "duration": round(time.time() - start_time, 2),
                "total_steps": len(steps),
                "passed_steps": len(steps),
                "failed_steps": 0,
                "step_results": [
                    {
                        "step": i + 1,
                        "action": s["action"],
                        "status": "simulated",
                        "detail": f"Simulated with value '{s.get('value')}'"
                    }
                    for i, s in enumerate(steps)
                ]
            }

        # ---------------------------------
        # EXECUTE MODE
        # ---------------------------------
        report = run_test_executor(steps, target)

        total = len(report.get("step_results", []))
        passed = len([s for s in report["step_results"] if s["status"] == "ok"])

        report.update({
            "status": report.get("status", "executed"),
            "duration": round(time.time() - start_time, 2),
            "total_steps": total,
            "passed_steps": passed,
            "failed_steps": total - passed
        })

        return report


def create_agent():
    return GeminiAgent()
