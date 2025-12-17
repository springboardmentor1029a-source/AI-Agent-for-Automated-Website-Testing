from jinja2 import Template
import json
from pathlib import Path

TEMPLATE = '''from playwright.sync_api import sync_playwright, TimeoutError
def run_test():
    out = {"steps": []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("{{ goto }}")
{% for s in steps %}
{% if s.action == 'fill' %}
        page.fill("{{ s.target }}", "{{ s.value }}")
        out["steps"].append({"action":"fill","target":"{{ s.target }}","value":"{{ s.value }}"})
{% elif s.action == 'click' %}
        page.click("{{ s.target }}")
        out["steps"].append({"action":"click","target":"{{ s.target }}"})
{% elif s.action == 'expect_text' %}
        try:
            text = page.text_content("{{ s.target }}")
            assert text is not None, "No text found for {{ s.target }}"
            out["steps"].append({"action":"expect_text","target":"{{ s.target }}","value":text})
            if "{{ s.value }}" not in (text or ""):
                raise AssertionError(f'Expected "{{ s.value }}" in {{ s.target }}, got: '+str(text))
        except Exception as e:
            out["error"] = str(e)
            browser.close()
            return out
{% endif %}
{% endfor %}
        browser.close()
    return out

if __name__ == '__main__':
    print(run_test())
'''

def generate_code(steps, out_path="tests/generated_test.py"):
    # determine goto
    goto = "http://127.0.0.1:5000/static/testpage.html"
    for s in steps:
        if s.get("action") == "goto":
            goto = s.get("target")
            break
    template = Template(TEMPLATE)
    rendered = template.render(goto=goto, steps=steps)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(rendered, encoding='utf-8')
    return out_path
