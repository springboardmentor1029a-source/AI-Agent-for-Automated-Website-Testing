from langgraph.graph import StateGraph, END
from agent.ai_parser import ai_parse_instruction
from agent.test_generator import generate_test
import subprocess
import os
import sys


def agent_node(state: dict):
    """
    Main agent node:
    1. Convert instruction → steps (Gemini)
    2. Generate Playwright pytest test
    3. Run pytest with advanced Playwright options
    """

    instruction = state["instruction"]
    website_url = state["website_url"]
    config = state["config"]

    # 1️⃣ Parse instruction → steps
    steps = ai_parse_instruction(
        instruction=instruction,
        website_url=website_url
    )

    # 2️⃣ Generate pytest + playwright code
    test_code = generate_test(steps, config)

    os.makedirs("tests", exist_ok=True)

    test_file = os.path.join("tests", "test_generated.py")

    with open(test_file, "w", encoding="utf-8") as f:
        f.write("import pytest\n")
        f.write("from playwright.sync_api import Page\n\n")
        f.write(test_code)

    # 3️⃣ Build pytest command safely
    pytest_cmd = [
        sys.executable,
        "-m",
        "pytest",
        test_file,
        "-q"
    ]

    # 🎛 Playwright advanced options
    if config.get("headed"):
        pytest_cmd.append("--headed")

    pytest_cmd.append(f"--slowmo={config.get('slowmo', 0)}")
    pytest_cmd.append(f"--screenshot={config.get('screenshot', 'off')}")

    if config.get("video"):
        pytest_cmd.append("--video")

    # 4️⃣ Run pytest
    result = subprocess.run(
        pytest_cmd,
        capture_output=True,
        text=True
    )

    return {
        "steps": steps,
        "result": {
            "passed": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    }


# ---------------- LANGGRAPH SETUP ---------------- #

graph = StateGraph(dict)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.add_edge("agent", END)

app = graph.compile()
