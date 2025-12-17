import json, datetime, os
def generate_report(execution_result):
    # Try to parse the stdout as Python repr/str of dict; best-effort
    report = {"generated_at": datetime.datetime.utcnow().isoformat()+"Z", "execution": execution_result}
    # Save JSON report to reports/
    os.makedirs("reports", exist_ok=True)
    fname = os.path.join("reports", f"report_{int(datetime.datetime.utcnow().timestamp())}.json")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(json.dumps(report, indent=2))
    # Also return brief summary
    summary = {
        "report_file": fname,
        "returncode": execution_result.get("returncode"),
        "stdout_truncated": (execution_result.get("stdout") or "")[:500],
        "stderr_truncated": (execution_result.get("stderr") or "")[:500]
    }
    return summary
