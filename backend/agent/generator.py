def generate_playwright_steps(parsed_steps):
    code_steps = []

    for step in parsed_steps:
        if step["action"] == "open":
            code_steps.append({"type": "goto", "value": f"https://{step['value']}.com"})
        elif step["action"] == "search":
            code_steps.append({"type": "search", "value": step["value"]})
        elif step["action"] == "verify":
            code_steps.append({"type": "verify", "value": step["value"]})

    return code_steps
