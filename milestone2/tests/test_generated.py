import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.dom_scanner import get_dom_snapshot
from agent.selector_ai import find_selector

def test_ai_generated(page):
    dom = []

    page.goto("https://www.flipkart.com")
    dom = get_dom_snapshot(page)
    sel = find_selector(dom, "search box")
    page.fill(sel, "eggs")
    page.keyboard.press("Enter")