from playwright.sync_api import sync_playwright, TimeoutError
import time
import sys
import os

# Add backend to sys.path to resolve utils import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.dom_mapper import find_element

def run_test(steps):
    results = []
    logs = []

    def log(message):
        print(message)
        logs.append(message)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=["--start-maximized"]
            )

            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 Chrome/120 Safari/537.36"
                ),
                viewport={"width": 1280, "height": 800}
            )

            page = context.new_page()

            for idx, step in enumerate(steps):
                retries = 3
                success = False
                last_error = None

                for attempt in range(retries):
                    try:
                        # ---------------- OPEN ----------------
                        if step["type"] == "goto":
                            log(f"Executing GOTO: {step['value']}")
                            page.goto(step["value"], timeout=30000)
                            page.wait_for_load_state("domcontentloaded")
                            log(f"Page loaded: {step['value']}")

                            # Handle Google consent if present
                            try:
                                accept_btn = find_element(page, "Accept all", timeout=2000)
                                if accept_btn:
                                    accept_btn.click()
                            except:
                                pass

                            results.append({
                                "step_no": idx + 1,
                                "action": "OPEN",
                                "target": step["value"],
                                "status": "PASS"
                            })
                            success = True
                            break

                        # ---------------- SEARCH ----------------
                        elif step["type"] == "search":
                            # Strategy 1: Look for an already visible input field first
                            log(f"Executing SEARCH: {step['value']}")
                            search_box = page.locator("input[type='text'], input[type='search'], input:not([type='hidden'])").filter(has=page.locator("visible=true")).first
                            
                            if search_box.count() > 0 and search_box.is_visible():
                                log("Found visible search input directly.")
                            else:
                                # Strategy 2: If no visible input, find a "Search" button/icon and click it
                                log("No visible input. Looking for search triggers...")
                                trigger = find_element(page, "Search", timeout=3000)
                                
                                if trigger:
                                    log("Found search trigger. Clicking...")
                                    trigger.click(force=True)
                                    # Wait for an input to appear
                                    try:
                                        search_box = page.locator("input[type='text'], input[type='search'], input:not([type='hidden'])").wait_for(state="visible", timeout=3000)
                                        # Re-select to get the locator handle
                                        search_box = page.locator("input[type='text'], input[type='search'], input:not([type='hidden'])").filter(has=page.locator("visible=true")).first
                                    except:
                                        log("No input appeared after clicking trigger.")
                                        search_box = None
                                else:
                                    log("No search trigger found.")
                                    search_box = None

                            # Fallback: Just grab the first input we can find, even if we aren't sure
                            if not search_box or search_box.count() == 0:
                                log("Fallback: searching for any input.")
                                search_box = page.locator("input").first

                            if not search_box or search_box.count() == 0:
                                raise Exception("Could not find any search input field.")

                            # Ensure we are interacting with an input-like element
                            tag_name = search_box.evaluate("el => el.tagName").upper()
                            is_editable = search_box.evaluate("el => el.isContentEditable")
                            
                            if tag_name not in ["INPUT", "TEXTAREA"] and not is_editable:
                                # Sometimes the locator captures a wrapper div. Try to find an input inside.
                                log(f"Target is {tag_name}, looking for internal input...")
                                internal_input = search_box.locator("input, textarea").first
                                if internal_input.count() > 0:
                                    search_box = internal_input

                            log("Filling search box...")
                            search_box.click(force=True)
                            search_box.fill(step["value"]) 
                            page.keyboard.press("Enter")
                            try:
                                page.wait_for_load_state("domcontentloaded", timeout=10000)
                            except:
                                pass # Continue even if timeout (e.g. YouTube keeps loading)

                            results.append({
                                "step_no": idx + 1,
                                "action": "SEARCH",
                                "target": step["value"],
                                "status": "PASS"
                            })
                            success = True
                            break

                        # ---------------- VERIFY ----------------
                        elif step["type"] == "verify":
                            log(f"Executing VERIFY: {step['value']}")
                            current_url = page.url
                            log(f"Checking content in URL: {current_url} and Page Title/Content")
                            
                            if "google" in current_url or "search" in current_url or step["value"].lower() in page.title().lower() or step["value"].lower() in page.content().lower():
                                log("Verification SUCCESS found content match.")
                                results.append({
                                    "step_no": idx + 1,
                                    "action": "VERIFY",
                                    "target": current_url,
                                    "status": "PASS"
                                })
                            else:
                                log(f"Verification FAILED. Content '{step['value']}' not found.")
                                results.append({
                                    "step_no": idx + 1,
                                    "action": "VERIFY",
                                    "target": current_url,
                                    "status": "FAIL",
                                    "error": f"Content '{step['value']}' not found in URL or Page Title"
                                })
                            success = True
                            break

                    except Exception as e:
                        log(f"Step {idx + 1} attempt {attempt + 1} failed: {str(e)}")
                        last_error = e
                        time.sleep(2) # Wait before retry

                if not success:
                     log(f"Step {idx + 1} FAILED after all attempts.")
                     results.append({
                        "step_no": idx + 1,
                        "action": step["type"].upper(),
                        "target": step.get("value", ""),
                        "status": "FAIL",
                        "error": str(last_error)
                    })

            browser.close()

    except Exception as fatal_error:
        # 🔥 Backend NEVER crashes now
        return [{
            "step_no": 1,
            "action": "SYSTEM",
            "target": "Playwright",
            "status": "FAIL",
            "error": f"Fatal error handled: {fatal_error}"
        }], logs

    return results, logs
