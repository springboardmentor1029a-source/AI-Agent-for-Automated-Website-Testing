from playwright.sync_api import sync_playwright

def run_test(test_steps, url):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        page.goto(url)

        for step in test_steps:
            try:
                action = step.get("action")

                if action == "goto":
                    page.goto(step.get("url", url))
                    results.append("goto successful")

                elif action == "fill":
                    page.fill(step["selector"], step["value"])
                    results.append("fill successful")

                elif action == "click":
                    page.click(step["selector"])
                    results.append("click successful")

            except Exception as e:
                results.append(str(e))

        page.wait_for_timeout(60000)  # 60 seconds
        browser.close()

    return results
