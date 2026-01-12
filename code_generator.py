# code_generator.py
from parser import TestCase

def generate_playwright_code(test_case: TestCase) -> str:
    lines = [
        "from playwright.sync_api import sync_playwright",
        "import json, os",
        "",
        "def run_test():",
        "    results = []",
        "    with sync_playwright() as p:",
        "        browser = p.chromium.launch(headless=True)",
        "        page = browser.new_page()",
        "        page.set_viewport_size({\"width\": 1920, \"height\": 1080})",
        ""
    ]

    for i, action in enumerate(test_case.actions):
        lines.append(f"        # Step {i+1}: {action.type.upper()}")

        if action.type == "visit":
            lines += [
                f"        page.goto(\"{action.url}\", wait_until=\"domcontentloaded\")",
                f"        results.append({{\"step\": {i+1}, \"action\": \"visit\", \"status\": \"passed\", \"details\": \"Visited {action.url}\"}})"
            ]

        elif action.type == "search":
            query = action.query.replace('"', '\\"')
            lines += [
                f"        page.fill(\"input[placeholder*='search' i], input[name='q'], input#twotabsearchtextbox\", \"{query}\")",
                f"        page.keyboard.press(\"Enter\")",
                f"        page.wait_for_load_state(\"networkidle\")",
                f"        count = page.locator(\"[data-component-type='s-search-result'], .s-result-item, ._2kHMtA\").count()",
                f"        status = \"passed\" if count > 0 else \"failed\"",
                f"        results.append({{\"step\": {i+1}, \"action\": \"search\", \"query\": \"{query}\", \"status\": status, \"details\": f\"Found {{count}} results\"}})"
            ]

        elif action.type == "login":
            email = action.email.replace('"', '\\"')
            pwd = action.password.replace('"', '\\"')
            lines += [
                f"        page.fill(\"input[type='email'], input#email, input[name='email']\", \"{email}\")",
                f"        page.fill(\"input[type='password'], input#pass, input[name='password']\", \"{pwd}\")",
                f"        page.click(\"button:has-text('Log in'), button:has-text('Sign in')\")",
                f"        page.wait_for_timeout(4000)",
                f"        error = page.locator(\"text=incorrect, text=wrong, text=invalid\").count() > 0",
                f"        still_login = page.locator(\"input[type='password']\").count() > 0",
                f"        status = \"passed\" if (error or still_login) else \"failed\"",
                f"        results.append({{\"step\": {i+1}, \"action\": \"login\", \"status\": status, \"details\": \"Login failed as expected\"}})"
            ]

    lines += [
        "",
        "        browser.close()",
        "        return results",
        "",
        "if __name__ == \"__main__\":",
        "    os.makedirs('reports', exist_ok=True)",
        "    results = run_test()",
        "    with open('reports/result.json', 'w') as f:",
        "        json.dump(results, f, indent=2)",
        "    print(json.dumps(results, indent=2))"
    ]

    return "\n".join(lines)