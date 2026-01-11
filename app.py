"""
AI Browser Test Runner
Simple natural language → Playwright automation demo
January 2026 version
"""

from flask import Flask, request, render_template_string, send_file, abort
import subprocess
import tempfile
import os
import uuid
import json
import time
import traceback
from pathlib import Path
from typing import List, Dict, Any

app = Flask(__name__)

RUNS_DIR = Path("runs")
RUNS_DIR.mkdir(exist_ok=True)

# ──────────────────────────────────────────────
#               SHARED NAVIGATION + STYLE
# ──────────────────────────────────────────────

NAVBAR = '''
<nav style="
    background: white;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    position: sticky;
    top: 0;
    z-index: 1000;
    padding: 1rem 2rem;
">
    <div style="max-width:1200px; margin:auto; display:flex; justify-content:space-between; align-items:center;">
        <div style="font-size:1.6rem; font-weight:bold; color:#4f46e5;">AI Test Runner</div>
        <div style="display:flex; gap:2.2rem; align-items:center;">
            <a href="/" style="color:#64748b; text-decoration:none; font-weight:500; {{ 'color:#4f46e5;' if request.path == '/' else '' }}">Home</a>
            <a href="/about" style="color:#64748b; text-decoration:none; font-weight:500; {{ 'color:#4f46e5;' if request.path == '/about' else '' }}">About</a>
            <a href="/features" style="color:#64748b; text-decoration:none; font-weight:500; {{ 'color:#4f46e5;' if request.path == '/features' else '' }}">Features</a>
            <a href="/" style="background:#4f46e5; color:white; padding:0.6rem 1.4rem; border-radius:8px; text-decoration:none;">Try Now →</a>
        </div>
    </div>
</nav>
'''

BASE_STYLE = '''
<style>
    body {
        margin:0;
        font-family: system-ui, -apple-system, sans-serif;
        background: #f8fafc;
        color: #1e293b;
        line-height: 1.6;
    }
    .container {
        max-width: 1000px;
        margin: 2.5rem auto;
        padding: 0 1.5rem;
    }
    .card {
        background: white;
        border-radius: 12px;
        padding: 2.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.06);
    }
    h1 { color: #4f46e5; margin-bottom: 1.2rem; }
    textarea {
        width: 100%;
        min-height: 140px;
        padding: 1rem;
        font-size: 1.1rem;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        resize: vertical;
        margin: 1.5rem 0;
    }
    button {
        background: #4f46e5;
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        border-radius: 10px;
        cursor: pointer;
        width: 100%;
        transition: background 0.2s;
    }
    button:hover { background: #4338ca; }
    .message {
        margin: 1.5rem 0;
        padding: 1rem;
        border-radius: 8px;
    }
    .success { background: #ecfdf5; color: #065f46; }
    .error { background: #fee2e2; color: #991b1b; }
    footer {
        text-align: center;
        padding: 3rem 1rem;
        color: #64748b;
        border-top: 1px solid #e2e8f0;
        margin-top: 4rem;
    }
</style>
'''

# ──────────────────────────────────────────────
#           BASIC PARSER (very naive – improve later)
# ──────────────────────────────────────────────

def parse_instruction(text: str) -> List[Dict[str, Any]]:
    text = text.lower().strip()
    actions = []

    # Visit detection
    if any(x in text for x in ["visit", "go to", "open"]):
        url = "https://www.google.com"  # fallback
        for domain in ["amazon.in", "amazon.com", "flipkart.com", "google.com"]:
            if domain in text:
                url = f"https://www.{domain}"
                break
        actions.append({"type": "visit", "url": url})

    # Search detection
    if "search" in text:
        parts = text.split("search")
        if len(parts) > 1:
            query_part = parts[1].strip()
            if query_part.startswith("for"):
                query_part = query_part[3:].strip()
            query = query_part.split("and")[0].split("then")[0].strip()
            if query:
                actions.append({"type": "search", "query": query})

    if not actions:
        raise ValueError("Couldn't understand instruction.\nTry e.g.: 'Visit amazon.in and search for laptop'")

    return actions

# ──────────────────────────────────────────────
#               HOME / MAIN PAGE
# ──────────────────────────────────────────────

HOME_HTML = NAVBAR + BASE_STYLE + '''
<div class="container">
    <div class="card">
        <h1>AI Browser Test Runner</h1>
        <p style="color:#475569; margin-bottom:1.8rem;">
            Describe what you want to test in natural language.<br>
            The system will generate and run Playwright automation.
        </p>

        <form method="post">
            <textarea name="instruction" placeholder="Examples:\n• Visit amazon.in and search for macbook pro\n• Go to flipkart.com search iphone 16\n• Visit google.com and search python tutorial" required>{{ instruction }}</textarea>
            <button type="submit">Run Test →</button>
        </form>

        {% if error %}
        <div class="message error">{{ error }}</div>
        {% endif %}

        {% if success %}
        <div class="message success" style="text-align:center;">
            Test finished!<br>
            <a href="{{ report_url }}" target="_blank" style="color:#065f46; font-weight:bold; text-decoration:underline;">
                → Open Detailed Report
            </a>
        </div>
        {% endif %}
    </div>
</div>

<footer>
    AI Browser Testing Prototype • Flask + Playwright • 2026
</footer>
'''

# ──────────────────────────────────────────────
#           ABOUT / FEATURES / etc. (minimal)
# ──────────────────────────────────────────────

ABOUT_HTML = NAVBAR + BASE_STYLE + '''
<div class="container">
    <div class="card">
        <h1>About</h1>
        <p>This is an experimental tool that turns natural language instructions into automated browser tests using Playwright.</p>
        <p>Goal: make quick regression/smoke testing faster and more accessible.</p>
    </div>
</div>
'''

FEATURES_HTML = NAVBAR + BASE_STYLE + '''
<div class="container">
    <div class="card">
        <h1>Features</h1>
        <ul style="margin-left:1.5rem; font-size:1.1rem;">
            <li>Natural language test description</li>
            <li>Automatic Playwright script generation</li>
            <li>Step-by-step report with screenshots</li>
            <li>Isolated test runs (no file conflicts)</li>
        </ul>
    </div>
</div>
'''

# ──────────────────────────────────────────────
#               TEST RUNNER (simplified)
# ──────────────────────────────────────────────

def generate_playwright_code(actions: List[Dict], run_id: str) -> str:
    lines = [
        "from playwright.sync_api import sync_playwright",
        "import time, json, os, traceback",
        f"RUN_DIR = 'runs/{run_id}'",
        "os.makedirs(RUN_DIR, exist_ok=True)",
        "results = []",
        "",
        "def log(snum, typ, tgt=None, stat='FAIL', msg='', dur=0):",
        "    results.append({'step':snum,'type':typ,'target':tgt,'status':stat,'msg':msg,'duration':dur})",
        "",
        "def shot(name):",
        "    p = f'{RUN_DIR}/{name}_{int(time.time()*1000)}.png'",
        "    page.screenshot(path=p, full_page=True)",
        "    return p",
        "",
        "try:",
        "    with sync_playwright() as p:",
        "        browser = p.chromium.launch(headless=True)",
        "        page = browser.new_page()",
        "        page.set_viewport_size({'width':1280,'height':800})",
    ]

    for i, action in enumerate(actions, 1):
        if action["type"] == "visit":
            lines += [
                f"        # Step {i} - VISIT",
                "        t0 = time.time()",
                f"        page.goto('{action['url']}', wait_until='domcontentloaded')",
                "        try: page.wait_for_load_state('networkidle', timeout=30000)",
                "        except: pass",
                f"        shot('step_{i}_visit')",
                f"        log({i}, 'visit', '{action['url']}', 'PASS', 'loaded', time.time()-t0)",
            ]

        elif action["type"] == "search":
            lines += [
                f"        # Step {i} - SEARCH",
                "        t0 = time.time()",
                "        try:",
                "            page.fill(\"input[placeholder*='search' i], input[name='q'], input#twotabsearchtextbox\", '''" + action["query"].replace("'", "\\'") + "''')",
                "            page.press(\"input[placeholder*='search' i], input[name='q'], input#twotabsearchtextbox\", 'Enter')",
                "            try: page.wait_for_load_state('networkidle', timeout=40000)",
                "            except: pass",
                f"            shot('step_{i}_search')",
                f"            log({i}, 'search', '{action['query']}', 'PASS', 'searched', time.time()-t0)",
                "        except Exception as ex:",
                f"            log({i}, 'search', '{action['query']}', 'FAIL', str(ex), time.time()-t0)",
            ]

    lines += [
        "        shot('final')",
        "        log(999, 'done', None, 'PASS', 'finished', 0)",
        "except Exception as e:",
        "    log(999, 'error', None, 'ERROR', traceback.format_exc(), 0)",
        "finally:",
        "    try: browser.close()",
        "    except: pass",
        "    try:",
        "        with open(f'{RUN_DIR}/results.json','w') as f:",
        "            json.dump(results, f, indent=2)",
        "    except: pass",
        "    print(json.dumps(results))",
    ]

    return "\n".join(lines)

# ──────────────────────────────────────────────
#               ROUTES
# ──────────────────────────────────────────────

@app.route('/', methods=['GET', 'POST'])
def index():
    ctx = {
        'instruction': '',
        'success': False,
        'error': None,
        'report_url': None
    }

    if request.method == 'POST':
        instr = request.form.get('instruction', '').strip()
        ctx['instruction'] = instr

        if not instr:
            ctx['error'] = "Please enter an instruction"
        else:
            try:
                actions = parse_instruction(instr)
                run_id = str(uuid.uuid4())[:10]

                code = generate_playwright_code(actions, run_id)

                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp:
                    tmp.write(code)
                    tmp_path = tmp.name

                try:
                    result = subprocess.run(
                        ["python", tmp_path],
                        capture_output=True,
                        text=True,
                        timeout=120
                    )
                finally:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)

                ctx['success'] = True
                ctx['report_url'] = f"/report/{run_id}"

            except Exception as e:
                ctx['error'] = str(e)

    return render_template_string(HOME_HTML, **ctx, request=request)


@app.route('/about')
def about():
    return render_template_string(ABOUT_HTML, request=request)


@app.route('/features')
def features():
    return render_template_string(FEATURES_HTML, request=request)


@app.route('/report/<run_id>')
def report(run_id):
    folder = RUNS_DIR / run_id
    if not folder.exists():
        return "<h2>Run not found</h2>", 404

    results_file = folder / "results.json"
    steps = []
    overall = "UNKNOWN"
    passed = total = 0

    screenshots_map = {}
    for f in folder.glob("*.png"):
        name = f.stem
        url = f"/screenshot/{run_id}/{f.name}"
        if "step_" in name:
            try:
                num = int(name.split("step_")[1].split("_")[0])
                screenshots_map.setdefault(num, []).append({"url": url})
            except:
                pass
        elif "final" in name:
            screenshots_map.setdefault(999, []).append({"url": url})

    if results_file.exists():
        try:
            with open(results_file, encoding="utf-8") as f:
                data = json.load(f)

            for item in data:
                num = item.get("step", 0)
                status = item.get("status", "UNKNOWN").lower()
                step = {
                    "type": item.get("type", "unknown"),
                    "target": item.get("target"),
                    "status": status,
                    "msg": item.get("msg", ""),
                    "screenshots": screenshots_map.get(num, [])
                }
                steps.append(step)

                if num < 900:
                    total += 1
                    if status == "pass":
                        passed += 1

            overall = "PASS" if passed == total > 0 else "FAIL" if total > 0 else "ERROR"

        except Exception as e:
            steps.append({"type":"error", "status":"error", "msg":f"Cannot read results: {e}", "screenshots":[]})

    return f"""
    {NAVBAR}
    {BASE_STYLE}
    <div class="container">
        <div class="card">
            <h1>Report — {run_id}</h1>
            <p><strong>Status:</strong> {overall}</p>
            <p><strong>Steps passed:</strong> {passed}/{total}</p>

            <div style="margin-top:2rem;">
                {"".join(
                    f'<h3>{s["type"].upper()} {s.get("target","")}</h3>'
                    f'<p><strong>Status:</strong> {s["status"]}</p>'
                    f'<p>{s["msg"]}</p>'
                    f'{"".join(f"<img src=\'{sh["url"]}\' style=\'max-width:600px; margin:0.8rem 0; border-radius:8px;\'>" for sh in s["screenshots"])}'
                    '<hr style="margin:2rem 0; border-color:#e2e8f0;">'
                    for s in steps
                )}
            </div>
        </div>
    </div>
    """

@app.route('/screenshot/<run_id>/<filename>')
def serve_screenshot(run_id, filename):
    path = RUNS_DIR / run_id / filename
    if not path.is_file():
        abort(404)
    return send_file(path, mimetype='image/png')


if __name__ == '__main__':
    print("AI Browser Test Runner")
    print("http://localhost:5000")
    app.run(debug=True, port=5000)
