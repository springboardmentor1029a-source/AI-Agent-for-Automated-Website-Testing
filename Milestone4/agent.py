from instruction_parser import parse_instruction
from playwright_executor import run_playwright_test
from report_generator import generate_report

def run_agent(url, instruction):
    actions = parse_instruction(instruction)
    result = run_playwright_test(url, actions)
    report = generate_report(result)

    return {
        "status": "success",
        "actions": actions,
        "report": report
    }
