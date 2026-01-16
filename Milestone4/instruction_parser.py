def parse_instruction(instruction):
    steps = []
    parts = instruction.lower().split(",")

    for part in parts:
        part = part.strip()

        if "open" in part:
            steps.append({"action": "goto"})

        elif "click" in part:
            steps.append({
                "action": "click",
                "selector": "a"
            })

        elif "enter" in part or "type" in part:
            steps.append({
                "action": "fill",
                "selector": "input",
                "value": "test"
            })

    return steps
