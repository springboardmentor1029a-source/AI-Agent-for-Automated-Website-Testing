from playwright.sync_api import sync_playwright
import time

def run_playwright_test(url, actions):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        page.goto(url)

        for action in actions:
            if action["action"] == "goto":
                page.goto(url)

            elif action["action"] == "click":
                page.click(action["selector"])

            elif action["action"] == "fill":
                page.fill(action["selector"], action["value"])

        # ✅ KEEP BROWSER OPEN FOR 60 SECONDS
        time.sleep(60)

        browser.close()

    return results
