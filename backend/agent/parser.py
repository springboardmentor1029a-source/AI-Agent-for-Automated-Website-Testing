import re

def parse_instruction(text):
    steps = []
    lines = text.lower().split("\n")

    for line in lines:
        if "open" in line:
            steps.append({"action": "open", "value": line.replace("open", "").strip()})
        elif "search" in line:
            steps.append({"action": "search", "value": line.replace("search for", "").strip()})
        elif "verify" in line or "check" in line:
            steps.append({"action": "verify", "value": line})
    return steps
