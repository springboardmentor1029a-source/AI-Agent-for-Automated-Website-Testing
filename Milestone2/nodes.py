# agent/nodes.py
import os
import json
import time
from datetime import datetime
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from .state import AgentState, TestStep


def get_llm(temperature: float = 0):
    """Get configured LLM instance"""
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=temperature,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )


def parse_instruction_node(state: AgentState) -> Dict[str, Any]:
    """Parse natural language instruction into test steps"""
    print(f"\n🔍 PARSING: {state['instruction']}")
    
    try:
        llm = get_llm()
        
        prompt = f"""Parse this E2E test instruction into specific steps.

URL: {state['target_url']}
Instruction: {state['instruction']}

Return ONLY a JSON array of steps. Each step must have:
- action: "navigate"|"click"|"type"|"wait"|"verify"|"select"
- target: CSS selector or "url" for navigate
- value: text to type (only for type action)
- description: what this step does

Example output:
[
  {{"action": "navigate", "target": "url", "value": null, "description": "Navigate to website"}},
  {{"action": "click", "target": "button.login", "value": null, "description": "Click login button"}},
  {{"action": "type", "target": "input[name='email']", "value": "test@example.com", "description": "Enter email"}},
  {{"action": "verify", "target": ".success-message", "value": null, "description": "Verify success message appears"}}
]

IMPORTANT: Return ONLY the JSON array, no markdown, no explanation."""

        response = llm.invoke([HumanMessage(content=prompt)])
        response_text = response.content.strip()
        
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
            response_text = response_text.strip()
        
        steps_data = json.loads(response_text)
        
        parsed_steps = []
        for step_dict in steps_data:
            step = TestStep(
                action=step_dict.get("action", ""),
                target=step_dict.get("target", ""),
                value=step_dict.get("value"),
                description=step_dict.get("description", "")
            )
            parsed_steps.append(step)
            print(f"  ✓ Step: {step.action} - {step.description}")
        
        return {
            "parsed_steps": parsed_steps,
            "messages": state.get("messages", []) + [response]
        }
        
    except Exception as e:
        print(f"❌ Parse error: {e}")
        return {
            "error": f"Failed to parse instruction: {str(e)}",
            "parsed_steps": []
        }


def generate_test_script_node(state: AgentState) -> Dict[str, Any]:
    """Generate Playwright test script"""
    print("\n📝 Generating test script...")
    
    try:
        steps = state.get("parsed_steps", [])
        if not steps:
            return {"test_script": ""}
        
        script_lines = [
            "from playwright.sync_api import sync_playwright",
            "",
            "def run_test():",
            "    with sync_playwright() as p:",
            "        browser = p.chromium.launch(headless=True)",
            "        page = browser.new_page()",
            ""
        ]
        
        for step in steps:
            if step.action == "navigate":
                script_lines.append(f"        page.goto('{state['target_url']}')")
            elif step.action == "click":
                script_lines.append(f"        page.click('{step.target}')")
            elif step.action == "type":
                script_lines.append(f"        page.fill('{step.target}', '{step.value}')")
        
        script_lines.extend([
            "",
            "        browser.close()",
            ""
        ])
        
        script = "\n".join(script_lines)
        print("  ✓ Script generated")
        
        return {"test_script": script}
        
    except Exception as e:
        print(f"❌ Script generation error: {e}")
        return {"test_script": ""}


def execute_test_node(state: AgentState) -> Dict[str, Any]:
    """Execute the test steps using Playwright"""
    print("\n🚀 EXECUTING TEST...")
    
    start_time = time.time()
    steps = state.get("parsed_steps", [])
    target_url = state.get("target_url", "")
    
    if not steps:
        return {
            "execution_status": "failed",
            "error": "No steps to execute",
            "test_results": {"status": "failed"}
        }
    
    results = {
        "steps": [],
        "passed": 0,
        "failed": 0,
        "total": len(steps),
        "status": "running"
    }
    
    screenshots = []
    headless = os.getenv("HEADLESS", "True").lower() == "true"
    
    try:
        with sync_playwright() as p:
            print(f"  🌐 Launching browser (headless={headless})...")
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            page = context.new_page()
            
            for idx, step in enumerate(steps, 1):
                print(f"\n  Step {idx}/{len(steps)}: {step.action} - {step.description}")
                step_result = {
                    "step_number": idx,
                    "action": step.action,
                    "description": step.description,
                    "status": "pending"
                }
                
                try:
                    if step.action == "navigate":
                        print(f"    → Navigating to: {target_url}")
                        page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
                        page.wait_for_timeout(2000)
                        step_result["status"] = "passed"
                        results["passed"] += 1
                        print(f"    ✓ Navigation successful")
                        
                    elif step.action == "click":
                        print(f"    → Clicking: {step.target}")
                        page.wait_for_selector(step.target, timeout=10000)
                        page.click(step.target)
                        page.wait_for_timeout(1000)
                        step_result["status"] = "passed"
                        results["passed"] += 1
                        print(f"    ✓ Click successful")
                        
                    elif step.action == "type" or step.action == "fill":
                        print(f"    → Typing into: {step.target}")
                        page.wait_for_selector(step.target, timeout=10000)
                        page.fill(step.target, step.value or "")
                        page.wait_for_timeout(500)
                        step_result["status"] = "passed"
                        results["passed"] += 1
                        print(f"    ✓ Type successful")
                        
                    elif step.action == "wait":
                        print(f"    → Waiting for: {step.target}")
                        page.wait_for_selector(step.target, timeout=10000)
                        step_result["status"] = "passed"
                        results["passed"] += 1
                        print(f"    ✓ Element found")
                        
                    elif step.action == "verify" or step.action == "assert":
                        print(f"    → Verifying: {step.target}")
                        is_visible = page.is_visible(step.target)
                        if is_visible:
                            step_result["status"] = "passed"
                            results["passed"] += 1
                            print(f"    ✓ Verification passed")
                        else:
                            step_result["status"] = "failed"
                            step_result["error"] = "Element not visible"
                            results["failed"] += 1
                            print(f"    ✗ Verification failed")
                    
                    elif step.action == "select":
                        print(f"    → Selecting option: {step.value}")
                        page.select_option(step.target, step.value or "")
                        step_result["status"] = "passed"
                        results["passed"] += 1
                        print(f"    ✓ Selection successful")
                    
                    else:
                        print(f"    ⚠ Unknown action: {step.action}")
                        step_result["status"] = "skipped"
                    
                    screenshot_path = f"outputs/screenshots/step_{idx}_{int(time.time())}.png"
                    os.makedirs("outputs/screenshots", exist_ok=True)
                    page.screenshot(path=screenshot_path)
                    screenshots.append(screenshot_path)
                    step_result["screenshot"] = screenshot_path
                    
                except PlaywrightTimeout as e:
                    print(f"    ✗ Timeout: {str(e)}")
                    step_result["status"] = "failed"
                    step_result["error"] = f"Timeout: {str(e)}"
                    results["failed"] += 1
                    
                except Exception as e:
                    print(f"    ✗ Error: {str(e)}")
                    step_result["status"] = "failed"
                    step_result["error"] = str(e)
                    results["failed"] += 1
                
                results["steps"].append(step_result)
            
            browser.close()
            print("\n  ✓ Browser closed")
            
    except Exception as e:
        print(f"\n❌ Execution error: {e}")
        return {
            "execution_status": "failed",
            "error": f"Execution failed: {str(e)}",
            "test_results": results,
            "screenshots": screenshots
        }
    
    execution_time = time.time() - start_time
    
    if results["failed"] > 0:
        results["status"] = "failed"
        execution_status = "failed"
    else:
        results["status"] = "passed"
        execution_status = "completed"
    
    results["execution_time"] = round(execution_time, 2)
    
    print(f"\n📊 Results: {results['passed']} passed, {results['failed']} failed")
    print(f"⏱️  Execution time: {results['execution_time']}s")
    
    return {
        "execution_status": execution_status,
        "test_results": results,
        "screenshots": screenshots
    }


def generate_report_node(state: AgentState) -> Dict[str, Any]:
    """Generate final test report"""
    print("\n📋 Generating report...")
    
    test_results = state.get("test_results", {})
    
    report = {
        "instruction": state.get("instruction", ""),
        "target_url": state.get("target_url", ""),
        "timestamp": datetime.now().isoformat(),
        "status": test_results.get("status", "unknown"),
        "execution_time": test_results.get("execution_time", 0),
        "total_steps": test_results.get("total", 0),
        "passed_steps": test_results.get("passed", 0),
        "failed_steps": test_results.get("failed", 0),
        "steps": test_results.get("steps", []),
        "screenshots": state.get("screenshots", [])
    }
    
    if state.get("error"):
        report["error"] = state["error"]
    
    if report["status"] == "passed":
        summary = f"✅ Test PASSED: All {report['passed_steps']} steps completed successfully"
    else:
        summary = f"❌ Test FAILED: {report['failed_steps']} of {report['total_steps']} steps failed"
    
    report["summary"] = summary
    
    reports_dir = os.getenv("REPORTS_DIR", "./outputs/reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    report_filename = f"report_{int(time.time())}.json"
    report_path = os.path.join(reports_dir, report_filename)
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    report["report_path"] = report_path
    
    print(f"  ✓ Report saved: {report_path}")
    print(f"\n{summary}")
    
    return {"report": report}
