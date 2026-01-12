# executor.py
import subprocess
import sys
import json
import os

def execute_test(code: str) -> dict:
    temp_file = "temp_test.py"
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(code)

        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=60
        )

        test_results = None
        if os.path.exists("reports/result.json"):
            with open("reports/result.json") as f:
                test_results = json.load(f)

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "results": test_results
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "stderr": "Test timed out", "results": None}
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)