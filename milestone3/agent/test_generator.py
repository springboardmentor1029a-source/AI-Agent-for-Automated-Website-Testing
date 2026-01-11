def py_safe(text: str) -> str:
    return text.replace('"', '\\"')

def generate_test(steps, config):
    code = []

    code.append("def test_ai_generated(page):")

    for step in steps:
        action = step["action"]

        if action == "goto":
            code.append(f'    page.goto("{py_safe(step["url"])}")')

        elif action == "fill":
            code.append(
                f'    page.fill("{py_safe(step["selector"])}", "{py_safe(step["value"])}")'
            )

        elif action == "click":
            code.append(
                f'    page.click("{py_safe(step["selector"])}")'
            )

        elif action == "search":
            # generic smart search (works on most sites)
            code.append('    page.keyboard.press("Control+L")')
            code.append(f'    page.keyboard.type("{py_safe(step["query"])}")')
            code.append('    page.keyboard.press("Enter")')

        elif action == "assert_text":
            code.append(
                f'    assert "{py_safe(step["text"])}" in page.content()'
            )

    return "\n".join(code)
