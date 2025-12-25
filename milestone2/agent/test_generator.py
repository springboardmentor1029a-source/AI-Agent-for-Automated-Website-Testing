def py_safe(text):
    return str(text).replace('"', '\\"')

def generate_test(steps, config):
    code = [
        "import sys, os",
        "sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))",
        "from agent.dom_scanner import get_dom_snapshot",
        "from agent.selector_ai import find_selector",
        "",
        "def test_ai_generated(page):",
        "    dom = []",
        ""
    ]

    for step in steps:
        action = step.get("action")

        if action == "goto":
            url = step.get("url")
            if not url:
                continue
            code.append(f'    page.goto("{py_safe(url)}")')
            code.append("    dom = get_dom_snapshot(page)")

        elif action == "search":
            query = step.get("query")
            if not query:
                continue
            code.append('    sel = find_selector(dom, "search box")')
            code.append(f'    page.fill(sel, "{py_safe(query)}")')
            code.append('    page.keyboard.press("Enter")')

        elif action == "fill":
            code.append(f'    sel = find_selector(dom, "{py_safe(step.get("target",""))}")')
            code.append(f'    page.fill(sel, "{py_safe(step.get("value",""))}")')

        elif action == "click":
            code.append(f'    sel = find_selector(dom, "{py_safe(step.get("target",""))}")')
            code.append('    page.click(sel)')

        elif action == "assert_text":
            code.append(f'    assert "{py_safe(step.get("text",""))}" in page.content()')

    return "\n".join(code)
