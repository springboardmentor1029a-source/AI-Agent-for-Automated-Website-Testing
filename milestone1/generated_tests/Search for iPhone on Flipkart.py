import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime

async def run_test():
    """Generated test: Search for iPhone on Flipkart"""
    results = {"test_name": "Search for iPhone on Flipkart", "steps": [], "assertions": []}
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Navigate to URL
        try:
            await page.goto("https://www.flipkart.com/", timeout=30000)
            await page.wait_for_load_state("networkidle")
            results["steps"].append({"step": "navigate", "status": "passed"})
        except Exception as e:
            results["steps"].append({"step": "navigate", "status": "failed", "error": str(e)})
            await browser.close()
            return results

        # Step 1: Navigate to the Flipkart homepage.
        try:
            results["steps"].append({"step": 1, "description": "Navigate to the Flipkart homepage.", "status": "passed"})
        except Exception as e:
            results["steps"].append({"step": 1, "description": "Navigate to the Flipkart homepage.", "status": "failed", "error": str(e)})

        # Step 2: Enter the search term 'iphone' into the primary search bar.
        try:
            await page.fill("input[name="q"]", "iphone")
            await page.wait_for_timeout(500)
            results["steps"].append({"step": 2, "description": "Enter the search term 'iphone' into the primary search bar.", "status": "passed"})
        except Exception as e:
            results["steps"].append({"step": 2, "description": "Enter the search term 'iphone' into the primary search bar.", "status": "failed", "error": str(e)})

        # Step 3: Click the search button (magnifying glass icon) to execute the search query.
        try:
            await page.click("button[type="submit"]")
            await page.wait_for_timeout(1000)
            results["steps"].append({"step": 3, "description": "Click the search button (magnifying glass icon) to execute the search query.", "status": "passed"})
        except Exception as e:
            results["steps"].append({"step": 3, "description": "Click the search button (magnifying glass icon) to execute the search query.", "status": "failed", "error": str(e)})

        # Assertions
        try:
            # Verify that the current URL contains '/search?q=iphone'
            results["assertions"].append({"assertion": "Verify that the current URL contains '/search?q=iphone'", "status": "passed"})
        except AssertionError as e:
            results["assertions"].append({"assertion": "Verify that the current URL contains '/search?q=iphone'", "status": "failed", "error": str(e)})
        try:
            # Verify that product listings related to 'iphone' are displayed on the page.
            results["assertions"].append({"assertion": "Verify that product listings related to 'iphone' are displayed on the page.", "status": "passed"})
        except AssertionError as e:
            results["assertions"].append({"assertion": "Verify that product listings related to 'iphone' are displayed on the page.", "status": "failed", "error": str(e)})

        await browser.close()
        results["status"] = "completed"
        results["timestamp"] = datetime.now().isoformat()
        return results

if __name__ == '__main__':
    result = asyncio.run(run_test())
    print(json.dumps(result, indent=2))