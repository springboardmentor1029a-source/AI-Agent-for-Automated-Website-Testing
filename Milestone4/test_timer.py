from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Open local HTML file
    page.goto("file:///C:/Users/HARSHIKA%20REDDY/OneDrive/Desktop/Documents/internship2/AI-Agent-for-Automated-Website-Testing/Milestone4/index.html")

    # Click the button
    page.click("text=Start 10 Seconds Timer")

    # Wait 11 seconds to observe message change
    time.sleep(11)

    # Get message text
    msg = page.text_content("#msg")
    print("Message after timer:", msg)

    # Keep browser open for 5 seconds
    time.sleep(5)

    browser.close()
