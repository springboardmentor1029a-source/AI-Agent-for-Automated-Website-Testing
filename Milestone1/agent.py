# agent.py (Milestone 1)

def handle_input(text):
    """
    Basic agent for Milestone 1
    Just echoes or explains the input
    """

    if not text.strip():
        return "Please enter an instruction."

    # Simple logic
    if "automated testing" in text.lower():
        return (
            "Automated testing is the process of using tools or scripts "
            "to automatically execute test cases, verify results, and "
            "ensure software quality without manual effort."
        )

    # Default response
    return f"You entered: {text}"
