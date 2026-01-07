from playwright.sync_api import sync_playwright

def test_website(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=10000)

            title = page.title()
            page.screenshot(path="static/screenshot.png")

            browser.close()

            return {
                "status": "SUCCESS",
                "title": title,
                "message": "Website loaded successfully",
                "screenshot": "static/screenshot.png"
            }

    except Exception as e:
        return {
            "status": "FAILED",
            "message": str(e)
        }
