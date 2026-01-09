import json
import os
import time
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright, TimeoutError
from groq import Groq

# =================================================
# CONFIG
# =================================================

BASE_DIR = os.path.dirname(__file__)
MEMORY_FILE = os.path.join(BASE_DIR, "site_memory.json")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "..", "static", "screenshots")

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
VISION_MODEL = "llama-3.2-vision-preview"

# =================================================
# MEMORY
# =================================================

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {}

def save_memory(mem):
    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=2)

SITE_MEMORY = load_memory()

def invalidate_search_memory(host):
    if host in SITE_MEMORY and "search" in SITE_MEMORY[host]:
        del SITE_MEMORY[host]["search"]
        if not SITE_MEMORY[host]:
            del SITE_MEMORY[host]
        save_memory(SITE_MEMORY)

# =================================================
# HELPERS
# =================================================

def get_host(page):
    try:
        return urlparse(page.url).netloc
    except:
        return "unknown"

def wait_for_page_stable(page, timeout=15000):
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except:
        pass

def detect_captcha(page):
    selectors = [
        "iframe[src*='captcha']",
        "iframe[src*='challenge']",
        "text=/captcha/i",
        "text=/verify/i",
    ]
    for sel in selectors:
        try:
            if page.query_selector(sel):
                return True
        except:
            pass
    return False

def capture_final_screenshot(page):
    filename = f"final_{int(time.time())}.png"
    path = os.path.join(SCREENSHOT_DIR, filename)
    page.screenshot(path=path, full_page=True)
    return f"static/screenshots/{filename}"


def needs_obstacle_resolution(err):
    keywords = [
        "Unable to locate search input",
        "not visible",
        "Timeout",
        "detached",
        "obscured",
    ]
    return any(k.lower() in str(err).lower() for k in keywords)

def json_safe(obj):
    if isinstance(obj, bytes):
        return "<binary>"
    if isinstance(obj, dict):
        return {k: json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [json_safe(v) for v in obj]
    return obj

# =================================================
# SEARCH LOGIC
# =================================================

def try_memory_search(page):
    host = get_host(page)
    entry = SITE_MEMORY.get(host, {}).get("search")
    if not entry:
        return None
    try:
        page.mouse.click(entry["bbox"]["x"], entry["bbox"]["y"])
        time.sleep(0.3)
        handle = page.evaluate_handle("""
            () => {
                const el = document.activeElement;
                if (!el) return null;
                const t = el.tagName.toLowerCase();
                if (t === 'input' || t === 'textarea') return el;
                return null;
            }
        """)
        return handle.as_element()
    except:
        return None

def learn_search_target(el, page):
    try:
        box = el.bounding_box()
        if not box:
            return
        host = get_host(page)
        SITE_MEMORY.setdefault(host, {})["search"] = {
            "bbox": {
                "x": int(box["x"] + box["width"] / 2),
                "y": int(box["y"] + box["height"] / 2),
            }
        }
        save_memory(SITE_MEMORY)
    except:
        pass

def find_visible_input(page):
    try:
        inputs = page.query_selector_all("input, textarea")
    except:
        return None

    best, area = None, 0
    for el in inputs:
        try:
            if not el.is_visible():
                continue
            box = el.bounding_box()
            if not box:
                continue
            a = box["width"] * box["height"]
            if a > area:
                best, area = el, a
        except:
            continue

    if best:
        box = best.bounding_box()
        page.mouse.click(
            int(box["x"] + box["width"] / 2),
            int(box["y"] + box["height"] / 2)
        )
        time.sleep(0.3)

    return best

def find_search_target(page, timeout=8):
    wait_for_page_stable(page)

    host = get_host(page)
    el = try_memory_search(page)
    if el:
        return el

    invalidate_search_memory(host)
    start = time.time()

    while time.time() - start < timeout:
        el = find_visible_input(page)
        if el:
            learn_search_target(el, page)
            return el
        time.sleep(0.4)

    raise TimeoutError("Unable to locate search input")

# =================================================
# EXECUTOR
# =================================================

def execute_test(instruction_json):
    steps = []
    verbal_result = None
    final_screenshot = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for i, step in enumerate(instruction_json.get("actions", []), start=1):
            res = {
                "step": i,
                "action": step["action"],
                "status": "PASS",
                "duration_ms": 0,
                "error": None,
            }
            start = time.time()
            action_success = False

            try:
                if step["action"] == "open":
                    page.goto(step["target"], wait_until="load", timeout=30000)
                    wait_for_page_stable(page)
                    if detect_captcha(page):
                        raise RuntimeError("CAPTCHA_DETECTED")
                    action_success = True

                elif step["action"] == "search":
                    wait_for_page_stable(page)
                    el = find_search_target(page)
                    el.fill(step["value"])
                    page.keyboard.press("Enter")
                    page.wait_for_load_state("networkidle", timeout=20000)
                    verbal_result = f"Searched for '{step['value']}' successfully"
                    action_success = True

            except Exception as err:
                res["status"] = "FAIL"
                res["error"] = str(err)
                steps.append(res)
                break

            if action_success:
                res["status"] = "PASS"

            res["duration_ms"] = int((time.time() - start) * 1000)
            steps.append(res)

        if verbal_result:
            final_screenshot = capture_final_screenshot(page)

        browser.close()

    overall_status = (
        "FAIL" if any(s["status"] == "FAIL" for s in steps) else "PASS"
    )

    return json_safe({
        "overall_status": overall_status,
        "verbal_result": verbal_result,
        "final_screenshot": final_screenshot,
        "steps": steps,
    })
