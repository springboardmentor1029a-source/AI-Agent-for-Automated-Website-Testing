import json
from langgraph.graph import StateGraph, END
from agent.parser import parse_instruction
from agent.generator import generate_code
from agent.executor import execute_test
from agent.reporter import generate_report

def run_agent_test(instruction: str):
    state = {"instruction": instruction}
    # Simple linear pipeline
    try:
        parsed = parse_instruction(instruction)
        code_path = generate_code(parsed)
        execution = execute_test(code_path)
        report = generate_report(execution)
        return {"status": "ok", "report": report}
    except Exception as e:
        return {"status": "error", "error": str(e)}
