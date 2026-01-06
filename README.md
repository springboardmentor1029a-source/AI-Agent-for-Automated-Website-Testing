# app.py
from flask import Flask, request, render_template_string, send_file
import subprocess
import tempfile
import os
import uuid

from parser import parse_instruction
from schemas import TestCase

app = Flask(__name__)

# Unique run ID to avoid screenshot conflicts when multiple users run tests
RUN_ID = str(uuid.uuid4())[:8]

def generate_playwright_code(test_case: TestCase) -> str:
    lines = [
        "from playwright.sync_api import sync_playwright",
        "import os",
        "",
        "def run_test():",
        "    with sync_playwright() as p:",
        "        browser = p.chromium.launch(headless=True)",
        "        page = browser.new_page()",
        "        page.set_viewport_size({'width': 1920, 'height': 1080})",
        "        has_search = False",
        ""
    ]

    for action in test_case.actions:
        if action.type == "visit":
            lines.append(f'        page.goto("{action.url}", wait_until="networkidle")')
            lines.append('        assert page.title() != "", "Page failed to load (empty title)"')
        elif action.type == "search":
            lines.append('        # Perform search')
            lines.append('        page.fill("input[placeholder*=\'search\' i], input[name=\'q\'], input#twotabsearchtextbox", "' + action.query.replace('"', '\\"') + '")')
            lines.append('        page.press("input[placeholder*=\'search\' i], input[name=\'q\'], input#twotabsearchtextbox", "Enter")')
            lines.append('        page.wait_for_load_state("networkidle")')
            lines.append(f'        print("Searched for: {action.query}")')
            lines.append('        has_search = True')
            # Take screenshot specifically for search results
            lines.append('        page.screenshot(path="search_results.png", full_page=False)')
            lines.append('        assert "' + action.query.lower() + '" in page.content().lower(), "Search query not found in results"')
        elif action.type == "login":
            lines.append('        # Login attempt')
            lines.append(f'        page.fill("input[type=\'email\'], input#email, input[name=\'email\']", "{action.email}")')
            lines.append(f'        page.fill("input[type=\'password\'], input#pass, input[name=\'password\']", "{action.password}")')
            lines.append('        page.click("button:has-text(\'Log in\'), button:has-text(\'Sign in\'), input[type=\'submit\']")')
            lines.append('        page.wait_for_timeout(3000)')
            lines.append('        if "invalid" in page.content().lower() or "error" in page.content().lower():')
            lines.append('            print("Login failed as expected")')
            lines.append('        else:')
            lines.append('            print("Login may have succeeded")')

    lines += [
        "",
        "        # Final screenshot always",
        "        page.screenshot(path='test_result.png', full_page=True)",
        "        print('Test completed successfully.')",
        "        browser.close()",
        "",
        "if __name__ == '__main__':",
        "    run_test()"
    ]
    return "\n".join(lines)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Agent Test Builder</title>
    <style>
        body {font-family: system-ui, sans-serif; background: #667eea; color: white; padding: 40px; min-height: 100vh; margin: 0;}
        .box {max-width: 1000px; margin: auto; background: rgba(255,255,255,0.95); color: #333; padding: 40px; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); position: relative;}
        h1 {text-align: center; color: #667eea; margin-top: 0;}
        textarea {width: 100%; height: 100px; padding: 15px; font-size: 16px; border: 2px solid #ddd; border-radius: 12px; margin-bottom: 15px; box-sizing: border-box;}
        button.main-btn {background: #667eea; color: white; padding: 15px; font-size: 18px; border: none; border-radius: 12px; width: 100%; cursor: pointer; margin-top: 10px;}
        button.main-btn:hover {background: #5a67d8;}
        pre {background: #f8f9fa; padding: 15px; border-radius: 10px; overflow-x: auto; margin-top: 20px; font-size: 14px;}
        .section {margin-top: 40px;}
        h2 {color: #667eea; border-bottom: 2px solid #ddd; padding-bottom: 8px;}
        img.result-img {max-width: 100%; border: 3px solid #667eea; border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.2); margin-top: 15px;}
        .help-btn {position: absolute; top: 20px; right: 20px; background: #5a67d8; color: white; padding: 12px 20px; border-radius: 30px; border: none; font-size: 16px; font-weight: 600; cursor: pointer;}
        .help-btn:hover {background: #4c54b2; transform: translateY(-2px);}
        .modal {display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.6); align-items: center; justify-content: center; z-index: 1000;}
        .modal-content {background: white; color: #333; padding: 30px; border-radius: 16px; max-width: 700px; width: 90%; max-height: 80vh; overflow-y: auto; box-shadow: 0 10px 30px rgba(0,0,0,0.3);}
        .close-btn {float: right; background: none; border: none; font-size: 28px; cursor: pointer; color: #aaa;}
        .close-btn:hover {color: #333;}
        .example {background: #f1f3f5; padding: 12px; border-radius: 8px; margin: 12px 0; font-family: monospace;}
        .footer-note {margin-top: 60px; text-align: center; color: #666; font-size: 14px;}
    </style>
</head>
<body>
<div class="box">
    <h1>AI Agent Test Builder </h1>

    <button class="help-btn" onclick="document.getElementById('helpModal').style.display='flex'">
        How to Use
    </button>

    <form method="post">
        <textarea name="instruction" placeholder="e.g. Visit amazon.in and search for macbook" required>{{ instruction }}</textarea>
        <button type="submit" class="main-btn">Parse & Generate Code</button>
    </form>

    {% if parsed %}
    <div class="section">
        <h2>Parsed Structured Test Case (JSON)</h2>
        <pre>{{ parsed }}</pre>
    </div>
    {% endif %}

    {% if code %}
    <div class="section">
        <h2>Generated Playwright Python Code</h2>
        <pre>{{ code }}</pre>
    </div>
    <form method="post">
        <input type="hidden" name="run" value="true">
        <input type="hidden" name="instruction" value="{{ instruction }}">
        <button type="submit" class="main-btn">Run Test in Browser</button>
    </form>
    {% endif %}

    {% if output %}
    <div class="section">
        <h2>Test Execution Output</h2>
        <pre>{{ output }}</pre>
    </div>

    {% if search_screenshot_exists %}
    <div class="section">
        <h2>🔍 Search Results Screenshot</h2>
        <p><strong>This shows the page right after performing the search.</strong></p>
        <img src="/search_results.png?t={{ cache_bust }}" class="result-img" alt="Search Results">
    </div>
    {% endif %}

    <div class="section">
        <h2>Final Page State</h2>
        <img src="/test_result.png?t={{ cache_bust }}" class="result-img" alt="Final Test Result">
    </div>
    {% endif %}

    <div class="footer-note">
        Next step: Connect to LangGraph → LLM Agent → Autonomous Browser Testing
    </div>
</div>

<!-- Help Modal -->
<div id="helpModal" class="modal">
    <div class="modal-content">
        <button class="close-btn" onclick="document.getElementById('helpModal').style.display='none'">&times;</button>
        <h2>how to use</h2>
        <p>Enter a natural language instruction. The AI parses it and generates + runs a Playwright test.</p>
        <strong>Now with automatic search results screenshot!</strong>

        <strong>Try these:</strong>
        <div class="example">Visit amazon.in and search for macbook</div>
        <div class="example">Go to google.com and search for springboard </div>
        <div class="example">Visit flipkart.com search iPhone 16</div>
        <div class="example">Visit http://localhost:5000/test-search.html and search for hello world</div>
    </div>
</div>

<script>
    window.onclick = function(event) {
        const modal = document.getElementById('helpModal');
        if (event.target === modal) modal.style.display = "none";
    }
</script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    parsed = None
    code = None
    instruction = ""
    output = None
    search_screenshot_exists = False
    cache_bust = str(uuid.uuid4())[:8]  # Prevent browser caching of images

    if request.method == 'POST':
        if 'run' in request.form:
            instruction = request.form['instruction']
            try:
                test_case: TestCase = parse_instruction(instruction)
                code = generate_playwright_code(test_case)
            except Exception as e:
                output = f"Parsing error: {str(e)}"
                return render_template_string(HTML, instruction=instruction, output=output, cache_bust=cache_bust)

            # Clean old screenshots
            for f in ['test_result.png', 'search_results.png']:
                if os.path.exists(f):
                    os.remove(f)

            # Write and execute code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                filename = f.name

            try:
                result = subprocess.run(["python", filename], capture_output=True, text=True, timeout=90)
                output = result.stdout + result.stderr
                if result.returncode != 0:
                    output += f"\n\n⚠️ Script exited with code: {result.returncode}"
            except subprocess.TimeoutExpired:
                output = "❌ Test timed out after 90 seconds"
            except Exception as e:
                output = f"Execution error: {str(e)}"
            finally:
                os.unlink(filename)

            # Check for search results screenshot
            if os.path.exists('search_results.png'):
                search_screenshot_exists = True

        else:
            instruction = request.form['instruction']
            try:
                test_case: TestCase = parse_instruction(instruction)
                parsed = test_case.model_dump_json(indent=2)
                code = generate_playwright_code(test_case)
            except Exception as e:
                parsed = f"Error parsing instruction: {str(e)}"

    return render_template_string(
        HTML,
        instruction=instruction,
        parsed=parsed,
        code=code,
        output=output,
        search_screenshot_exists=search_screenshot_exists,
        cache_bust=cache_bust
    )

@app.route('/test_result.png')
def serve_final():
    if os.path.exists('test_result.png'):
        return send_file('test_result.png', mimetype='image/png')
    return "Screenshot not found", 404

@app.route('/search_results.png')
def serve_search():
    if os.path.exists('search_results.png'):
        return send_file('search_results.png', mimetype='image/png')
    return "Search screenshot not available", 404

# Local test pages remain the same
@app.route('/test-search.html')
def test_search():
    return '''
    <!DOCTYPE html>
    <html><head><title>Test Search</title></head>
    <body>
        <h1>Local Test Search Page</h1>
        <form method="get" action="/search_results">
            <input type="text" name="q" placeholder="Search here..." style="padding:10px; font-size:16px;">
            <button type="submit">Search</button>
        </form>
    </body></html>
    '''

@app.route('/search_results')
def search_results():
    query = request.args.get('q', 'nothing')
    return f'<h1>Search Results for: "{query}"</h1><p>You searched for {query}. This is a local test page.</p>'

if __name__ == '__main__':
    print("🚀 AI Agent Test Builder with Search Results Screenshot!")
    print("📌 Open http://localhost:5000")
    app.run(debug=True, port=5000)
