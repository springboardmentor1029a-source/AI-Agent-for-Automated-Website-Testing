
# workflow.py

def generate_test_steps(actions):
    steps = []

    for act in actions:
        if act["action"] == "open":
            steps.append("Open the webpage")
        elif act["action"] == "click":
            steps.append("Click on the button")
        elif act["action"] == "type":
            steps.append("Type into the input field")

    return steps