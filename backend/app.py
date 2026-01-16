import os, json, time
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "..", "screenshots")
VIDEOS_DIR = os.path.join(BASE_DIR, "..", "videos")
REPORTS_DIR = os.path.join(BASE_DIR, "..", "reports")

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(VIDEOS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

stats = {"total": 0, "passed": 0, "failed": 0}
history = []

# ---------------- STATIC FILE ROUTES ----------------

@app.route("/screenshots/<path:f>")
def screenshots(f):
    return send_from_directory(SCREENSHOTS_DIR, f,as_attachment=True)

@app.route("/videos/<path:f>")
def videos(f):
    return send_from_directory(VIDEOS_DIR, f,as_attachment=True)

@app.route("/reports/<path:f>")
def reports(f):
    return send_from_directory(REPORTS_DIR, f)

@app.route("/reports-list")
def reports_list():
    files = sorted(
        [f for f in os.listdir(REPORTS_DIR) if f.endswith(".html")],
        reverse=True
    )
    return jsonify(files)

@app.route("/history")
def get_history():
    return jsonify(history[::-1])

@app.route("/stats")
def get_stats():
    return jsonify(stats)

# ---------------- TEST EXECUTION ----------------

@app.route("/test", methods=["POST"])
def run_test():
    start_time = time.time()
    failure_reason = None

    instruction = request.json.get("instruction", "").lower().strip()
    words = instruction.split()

    url, query = None, None
    for w in words:
        if "." in w and not url:
            url = "https://" + w if not w.startswith("http") else w

    if "search" in words:
        query = " ".join(words[words.index("search") + 1:])

    if not url:
        return jsonify({"error": "No URL found"}), 400

    testcase_count = 1 + (1 if query else 0)
    stats["total"] += testcase_count

    open_ok, search_ok = False, False

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_name = f"screenshot_{ts}.png"
    video_file = None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)

            context = browser.new_context(
                record_video_dir=VIDEOS_DIR,
                record_video_size={"width": 1280, "height": 720}
            )

            page = context.new_page()

            # ---------- OPEN ----------
            page.goto(url, timeout=15000)
            page.wait_for_load_state("domcontentloaded")
            open_ok = True

            # ---------- SEARCH ----------
            if query:
                page.wait_for_timeout(2000)

                if "google" in url:
                    page.fill("input[name='q']", query)
                    page.keyboard.press("Enter")

                elif "amazon" in url:
                    page.fill("#twotabsearchtextbox", query)
                    page.click("#nav-search-submit-button")

                elif "wikipedia" in url:
                    page.fill("input[name='search']", query)
                    page.keyboard.press("Enter")

                elif "flipkart" in url:
                    page.locator("input[type='text']").first.fill(query)
                    page.keyboard.press("Enter")

                else:
                    # Generic fallback
                    page.locator("input").first.fill(query)
                    page.keyboard.press("Enter")

                page.wait_for_timeout(3000)
                status="passed"
                failure_resaon=None
                search_ok = True

            # ---------- SCREENSHOT ----------
            page.screenshot(
                path=os.path.join(SCREENSHOTS_DIR, screenshot_name),
                full_page=True
            )

            context.close()
            browser.close()

    except PlaywrightTimeout:
        failure_reason = "Page load or search timeout"
    except Exception as e:
        failure_reason = str(e)

    # ---------- VIDEO PICKUP ----------
    videos = sorted(
        [f for f in os.listdir(VIDEOS_DIR) if f.endswith(".webm")],
        key=lambda x: os.path.getmtime(os.path.join(VIDEOS_DIR, x)),
        reverse=True
    )
    video_file = videos[0] if videos else None

    # ---------- STATUS ----------
    status = "PASSED" if open_ok and (search_ok if query else True) else "FAILED"
    stats["passed" if status == "PASSED" else "failed"] += testcase_count

    execution_time = round(time.time() - start_time, 2)

    # ---------- REPORT ----------
    report_name = f"report_{ts}.html"
    report_path = os.path.join(REPORTS_DIR, report_name)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"""
        <html>
        <head><title>Test Report</title></head>
        <body style="font-family:Arial;padding:20px">
        <h2>AI Web Testing Agent – Report</h2>

        <b>Instruction:</b> {instruction}<br>
        <b>Status:</b> {status}<br>
        <b>Execution Time:</b> {execution_time}s<br>
        <b>Failure Reason:</b> {failure_reason or "N/A"}<br><br>

        <b>Screenshot:</b><br>
        {f'<a href="/screenshots/{screenshot_name}">View Screenshot</a>' if open_ok else 'Not Available'}<br><br>

        <b>Video:</b><br>
        {f'<a href="/videos/{video_file}">Download Video</a>' if video_file else 'Not Available'}

        </body>
        </html>
        """)

    history.append({
        "instruction": instruction,
        "status": status,
        "time": ts
    })

    return jsonify({
        "status": status,
        "execution_time": execution_time,
        "failure_reason": failure_reason,
        "screenshot": screenshot_name if open_ok else None,
        "video": video_file,
        "report": report_name,
        "stats": stats
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
