"""
Quick test script to verify visible browser mode works
Run this directly: python test_visible_browser.py
"""

from playwright.sync_api import sync_playwright
import time

print("="*60)
print("TESTING VISIBLE BROWSER MODE")
print("="*60)

with sync_playwright() as p:
    print("\n[1/3] Launching Chrome browser in VISIBLE mode...")
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    
    print("[2/3] Creating page and navigating to Google...")
    page = browser.new_page()
    page.goto('https://www.google.com')
    
    print("[3/3] SUCCESS! Browser is open and showing Google.")
    print("\nBrowser will stay open for 30 seconds so you can see it...")
    print("You can close it manually anytime.\n")
    
    time.sleep(30)
    
    print("Closing browser...")
    browser.close()
    
print("\n" + "="*60)
print("TEST COMPLETE!")
print("="*60)
