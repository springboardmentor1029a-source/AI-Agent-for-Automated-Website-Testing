import pytest

from playwright.sync_api import Page

def test_ai_generated(page: Page):
    page.goto("https://www.flipkart.com/")

    # Smart search
    search_inputs = page.locator("input[type='search'], input[name*='search'], input[placeholder*='Search'], input[aria-label*='Search']")
    if search_inputs.count() > 0:
        search_inputs.first.fill("iphones")
        search_inputs.first.press("Enter")
    