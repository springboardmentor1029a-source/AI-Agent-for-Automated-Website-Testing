# agent/executor.py
import os
from datetime import datetime

import os
import time
from playwright.sync_api import sync_playwright
from agent.summarizer import summarize_text


# 🔍 Detect page type
def detect_page_type(page):
    if page.locator("input[type='password']").count() > 0:
        return "login"
    if page.locator("#mw-content-text").count() > 0:
        return "article"
    return "generic"


def execute_test(test_plan: dict) -> dict:
    steps = test_plan.get("steps", [])
    logs = []
    extracted_data = ""

    # 📸 Screenshot folder
    screenshot_dir = "static/screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = ""

    try:
        with sync_playwright() as p:
            # ✅ Chromium = most stable
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            for i, step in enumerate(steps, start=1):
                action = step.get("action")
                logs.append(f"Step {i}: {action}")

                # ---------- GOTO ----------
                if action == "goto":
                    page.goto(step["url"], timeout=60000)
                    page.wait_for_load_state("domcontentloaded")

                # ---------- EXTRACT TEXT ----------
                elif action == "extract_text":

                    # 🔽 Auto-scroll (safe + fast)
                    page.evaluate("""
    async () => {
        const delay = ms => new Promise(r => setTimeout(r, ms));
        const totalHeight = document.body.scrollHeight;
        let current = 0;

        while (current < totalHeight) {
            window.scrollTo(0, current);
            current += 500;
            await delay(300);
        }
        

        window.scrollTo(0, 0); // scroll back to top
    }
""")


                    page_type = detect_page_type(page)
                    logs.append(f"Detected page type: {page_type}")

                    # 📘 ARTICLE (Wikipedia / blogs)
                    if page_type == "article":
                        extracted_data = page.evaluate("""
                            () => {
                                const paras = Array.from(
                                    document.querySelectorAll("#mw-content-text p")
                                )
                                .map(p => p.innerText.trim())
                                .filter(t => t.length > 50);

                                if (paras.length > 0) {
                                    return paras.slice(0, 5).join("\\n\\n");
                                }
                                return document.body.innerText.slice(0, 1200);
                            }
                        """)

                    # 🔐 LOGIN PAGE
                    elif page_type == "login":
                        extracted_data = (
                            "Login page detected. "
                            "Credentials are not tested for ethical reasons."
                        )

                    # 🌐 GENERIC PUBLIC SITE
                    else:
                        extracted_data = page.evaluate("""
                            () => {
                                const headings = Array.from(
                                    document.querySelectorAll("h1, h2")
                                ).map(h => h.innerText.trim());

                                if (headings.length > 0) {
                                    return headings.slice(0, 6).join("\\n");
                                }
                                return document.body.innerText.slice(0, 1000);
                            }
                        """)

            # ---------- SCREENSHOT (SAFE FIX) ----------
            timestamp = int(time.time())
            screenshot_path = f"{screenshot_dir}/page_{timestamp}.png"

            page.screenshot(
                path=screenshot_path,
                full_page=False,     # ❗ avoids timeout
                timeout=10000
            )

            logs.append(f"Screenshot saved: {screenshot_path}")

            # ⏳ Keep browser visible
            page.wait_for_timeout(3000)
            browser.close()

            summary = summarize_text(extracted_data)

            return {
                "status": "PASSED",
                "logs": logs,
                "extracted_data": extracted_data,
                "summary": summary,
                "screenshot": screenshot_path
            }

    except Exception as e:
        return {
            "status": "ERROR",
            "logs": logs,
            "extracted_data": "No data extracted",
            "summary": str(e),
            "screenshot": screenshot_path
        }
