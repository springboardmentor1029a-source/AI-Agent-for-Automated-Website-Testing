import subprocess, json, os
def execute_test(file_path):
    # Run the generated test script as a subprocess and capture JSON-like output
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)
    result = subprocess.run(["python", file_path], capture_output=True, text=True, timeout=60)
    stdout = result.stdout.strip()
    stderr = result.stderr.strip()
    return {"stdout": stdout, "stderr": stderr, "returncode": result.returncode}
