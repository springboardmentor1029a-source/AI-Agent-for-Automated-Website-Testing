import subprocess

def run_pytest(config):
    cmd = ["pytest", "tests/test_generated.py"]

    if config.get("headed"):
        cmd.append("--headed")
    if config.get("slowmo", 0) > 0:
        cmd.extend(["--slowmo", str(config["slowmo"])])

    result = subprocess.run(cmd, capture_output=True, text=True)

    return {
        "passed": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr
    }
