# instruction_parser.py

def parse_instruction(text: str):
    text = text.lower()
    actions = []

    # Open page
    if "open" in text or "goto" in text:
        actions.append({
            "action": "goto",
            "target": "login_page"
        })

    # Enter / type text
    if "enter" in text or "type" in text or "fill" in text:
        actions.append({
            "action": "fill",
            "target": "username_field",
            "value": "testuser"
        })

    # Click button
    if "click" in text or "press" in text:
        actions.append({
            "action": "click",
            "target": "login_button"
        })

    return actions
