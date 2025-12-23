import asyncio
import subprocess
import json
import sys
from typing import Dict, Any
from pathlib import Path

class CodeExecutor:
    """Executes generated test code"""
    
    def __init__(self, output_dir: str = "generated_tests"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    async def execute_code(self, code: str, test_name: str) -> Dict[str, Any]:
        """
        Execute generated code and return results
        """
        # Save code to temporary file
        test_file = self.output_dir / f"{test_name}.py"
        
        with open(test_file, "w") as f:
            f.write(code)
        
        print(f"✓ Test code saved to {test_file}")
        
        try:
            # Run the code using subprocess with increased timeout for web tests
            result = subprocess.run(
                [sys.executable, str(test_file)],
                capture_output=True,
                text=True,
                timeout=120  # Increased to 2 minutes for web automation
            )
            
            # Parse output
            if result.returncode != 0:
                # Test failed
                error_msg = result.stderr if result.stderr else "Test execution failed"
                return {
                    "execution_status": "failed",
                    "error": error_msg,
                    "test_name": test_name,
                    "stdout": result.stdout[:500] if result.stdout else None,
                    "stderr": result.stderr[:500] if result.stderr else None
                }
            
            if result.stdout:
                try:
                    # Try to find JSON in output (might have other text)
                    stdout_lines = result.stdout.strip().split('\n')
                    json_output = None
                    
                    # Look for JSON object in output
                    for line in stdout_lines:
                        if line.strip().startswith('{'):
                            # Found start of JSON, try to parse from here
                            json_start = result.stdout.find('{')
                            json_str = result.stdout[json_start:]
                            # Find the matching closing brace
                            brace_count = 0
                            json_end = -1
                            for i, char in enumerate(json_str):
                                if char == '{':
                                    brace_count += 1
                                elif char == '}':
                                    brace_count -= 1
                                    if brace_count == 0:
                                        json_end = i + 1
                                        break
                            
                            if json_end > 0:
                                json_output = json.loads(json_str[:json_end])
                                break
                    
                    if json_output:
                        json_output["execution_status"] = "success"
                        return json_output
                    else:
                        # Try parsing entire stdout as JSON
                        output = json.loads(result.stdout)
                        output["execution_status"] = "success"
                        return output
                        
                except json.JSONDecodeError as e:
                    return {
                        "execution_status": "failed",
                        "error": f"Could not parse test output as JSON: {str(e)}",
                        "raw_output": result.stdout[:1000],  # Limit output size
                        "test_name": test_name
                    }
            else:
                return {
                    "execution_status": "failed",
                    "error": result.stderr if result.stderr else "No output from test",
                    "test_name": test_name
                }
        
        except subprocess.TimeoutExpired as e:
            return {
                "execution_status": "failed",
                "error": f"Test execution timeout (120s). The test took too long to complete.",
                "test_name": test_name,
                "steps": [{"step": "timeout", "status": "failed", "error": "Execution timeout"}]
            }
        except Exception as e:
            return {
                "execution_status": "failed",
                "error": str(e),
                "test_name": test_name
            }

# Test the executor
if __name__ == "__main__":
    # Sample test code
    sample_code = """
import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime

async def run_test():
    results = {"test_name": "Sample Test", "steps": []}
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto("https://example.com", timeout=10000)
            results["steps"].append({"step": "navigate", "status": "passed"})
        except Exception as e:
            results["steps"].append({"step": "navigate", "status": "failed", "error": str(e)})
        
        await browser.close()
        results["status"] = "completed"
        results["timestamp"] = datetime.now().isoformat()
        return results

if __name__ == '__main__':
    result = asyncio.run(run_test())
    print(json.dumps(result, indent=2))
"""
    
    executor = CodeExecutor()
    result = asyncio.run(executor.execute_code(sample_code, "sample_test"))
    print("Execution Result:")
    print(json.dumps(result, indent=2))

