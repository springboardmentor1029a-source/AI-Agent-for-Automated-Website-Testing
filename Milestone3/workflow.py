# workflow.py

def generate_test_steps(actions):
    """
    Converts parsed actions into Playwright executable steps
    """

    steps = []

    for action in actions:
        if action["action"] == "goto":
            steps.append({
                "action": "goto"
            })

        elif action["action"] == "fill":
            steps.append({
                "action": "fill",
                "selector": action["selector"],
                "value": action["value"]
            })

        elif action["action"] == "click":
            steps.append({
                "action": "click",
                "selector": action["selector"]
            })

    return steps
