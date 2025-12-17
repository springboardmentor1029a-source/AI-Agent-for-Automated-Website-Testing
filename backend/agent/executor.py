from playwright.sync_api import sync_playwright, TimeoutError
import time

def run_test(steps):
    results = []

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
                try:
                    # ---------------- OPEN ----------------
                    if step["type"] == "goto":
                        page.goto(step["value"], timeout=30000)
                        page.wait_for_load_state("domcontentloaded")

                        # Handle Google consent if present
                        try:
                            page.click("button:has-text('Accept all')", timeout=3000)
                        except TimeoutError:
                            pass

                        results.append({
                            "step_no": idx + 1,
                            "action": "OPEN",
                            "target": step["value"],
                            "status": "PASS"
                        })

                    # ---------------- SEARCH ----------------
                    elif step["type"] == "search":
                        page.wait_for_selector("input", timeout=15000)
                        page.click("input")
                        page.keyboard.type(step["value"], delay=120)
                        page.keyboard.press("Enter")
                        page.wait_for_load_state("networkidle")

                        results.append({
                            "step_no": idx + 1,
                            "action": "SEARCH",
                            "target": step["value"],
                            "status": "PASS"
                        })

                    # ---------------- VERIFY ----------------
                    elif step["type"] == "verify":
                        current_url = page.url
                        if "google" in current_url or "search" in current_url:
                            results.append({
                                "step_no": idx + 1,
                                "action": "VERIFY",
                                "target": current_url,
                                "status": "PASS"
                            })
                        else:
                            results.append({
                                "step_no": idx + 1,
                                "action": "VERIFY",
                                "target": current_url,
                                "status": "FAIL",
                                "error": "Unexpected URL"
                            })

                except Exception as step_error:
                    results.append({
                        "step_no": idx + 1,
                        "action": step["type"].upper(),
                        "target": step.get("value", ""),
                        "status": "FAIL",
                        "error": str(step_error)
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
        }]

    return results
