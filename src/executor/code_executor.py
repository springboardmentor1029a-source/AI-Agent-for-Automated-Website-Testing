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
            # Run the code using subprocess
            result = subprocess.run(
                [sys.executable, str(test_file)],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Parse output
            if result.stdout:
                try:
                    output = json.loads(result.stdout)
                    output["execution_status"] = "success"
                    return output
                except json.JSONDecodeError:
                    return {
                        "execution_status": "failed",
                        "error": "Could not parse test output",
                        "raw_output": result.stdout
                    }
            else:
                return {
                    "execution_status": "failed",
                    "error": result.stderr if result.stderr else "No output",
                    "test_name": test_name
                }
        
        except subprocess.TimeoutExpired:
            return {
                "execution_status": "failed",
                "error": "Test execution timeout (60s)",
                "test_name": test_name
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

