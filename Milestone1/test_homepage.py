from playwright.sync_api import sync_playwright

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://127.0.0.1:5000")
        # check page has expected title or heading
        heading = page.locator("h1").text_content()
        assert "AI Agent for Automated Website Testing" in heading
        print("Homepage check passed.")
        browser.close()

if __name__ == "__main__":
    run_test()
