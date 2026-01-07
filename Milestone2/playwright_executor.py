from playwright.sync_api import sync_playwright

def execute_commands(commands):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()

        for cmd in commands:
            if cmd["command"] == "OPEN_BROWSER":
                page.goto(cmd["target"])
                results.append(f"Opened {cmd['target']}")

            elif cmd["command"] == "ASSERT_TITLE":
                title = page.title()
                if cmd["value"].lower() in title.lower():
                    results.append("✅ Title validation passed")
                else:
                    results.append("❌ Title validation failed")

        input("Press ENTER to close the browser...")
        browser.close()

    return results
