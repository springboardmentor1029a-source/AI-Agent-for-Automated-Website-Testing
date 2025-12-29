# app.py
from flask import Flask, request, render_template_string

from parser import parse_instruction
from schemas import TestCase

app = Flask(__name__)

def generate_playwright_code(test_case: TestCase) -> str:
    lines = [
        "from playwright.sync_api import sync_playwright",
        "",
        "def run_test():",
        "    with sync_playwright() as p:",
        "        browser = p.chromium.launch(headless=True)",
        "        page = browser.new_page()",
        "        page.set_viewport_size({'width': 1920, 'height': 1080})",
        ""
    ]

    for action in test_case.actions:
        if action.type == "visit":
            lines.append(f'        page.goto("{action.url}", wait_until="domcontentloaded")')
        elif action.type == "search":
            lines.append('        # Fill search box')
            lines.append('        page.fill("input[placeholder*=\'search\' i], input[name=\'q\'], input#twotabsearchtextbox", "' + action.query + '")')
            lines.append('        page.press("input[placeholder*=\'search\' i]", "Enter")')
            lines.append('        page.wait_for_load_state("networkidle")')
        elif action.type == "login":
            lines.append('        # Login attempt')
            lines.append(f'        page.fill("input[type=\'email\'], input#email, input[name=\'email\']", "{action.email}")')
            lines.append(f'        page.fill("input[type=\'password\'], input#pass, input[name=\'password\']", "{action.password}")')
            lines.append('        page.click("button:has-text(\'Log in\'), button:has-text(\'Sign in\'), input[type=\'submit\']")')
            lines.append('        page.wait_for_timeout(3000)')

    lines += [
        "",
        "        print('Test completed.')",
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
        .box {max-width: 900px; margin: auto; background: rgba(255,255,255,0.95); color: #333; padding: 40px; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); position: relative;}
        h1 {text-align: center; color: #667eea; margin-top: 0;}
        textarea {width: 100%; height: 100px; padding: 15px; font-size: 16px; border: 2px solid #ddd; border-radius: 12px; margin-bottom: 15px; box-sizing: border-box;}
        button.main-btn {background: #667eea; color: white; padding: 15px; font-size: 18px; border: none; border-radius: 12px; width: 100%; cursor: pointer;}
        button.main-btn:hover {background: #5a67d8;}
        pre {background: #f8f9fa; padding: 15px; border-radius: 10px; overflow-x: auto; margin-top: 20px; font-size: 14px;}
        .section {margin-top: 40px;}
        h2 {color: #667eea; border-bottom: 2px solid #ddd; padding-bottom: 8px;}

        /* How to Use Button - Top Right */
        .help-btn {
            position: absolute;
            top: 20px;
            right: 20px;
            background: #5a67d8;
            color: white;
            padding: 12px 20px;
            border-radius: 30px;
            border: none;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        .help-btn:hover {
            background: #4c54b2;
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.25);
        }

        /* Modal Overlay */
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.6);
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }
        .modal-content {
            background: white;
            color: #333;
            padding: 30px;
            border-radius: 16px;
            max-width: 700px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .modal-content h2 {color: #667eea; margin-top: 0;}
        .close-btn {
            float: right;
            background: none;
            border: none;
            font-size: 28px;
            cursor: pointer;
            color: #aaa;
        }
        .close-btn:hover {color: #333;}
        .example {
            background: #f1f3f5;
            padding: 12px;
            border-radius: 8px;
            margin: 12px 0;
            font-family: monospace;
            color: #2d3748;
            word-break: break-all;
        }
        ul {line-height: 1.8; padding-left: 20px;}

        .footer-note {
            margin-top: 60px;
            text-align: center;
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
<div class="box">
    <h1>AI Agent Test Builder (LangGraph Ready)</h1>

    <!-- How to Use Button (Top Right) -->
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
    {% endif %}

    <div class="footer-note">
        Next step: Connect to LangGraph → LLM Code Generator → Playwright Executor
    </div>
</div>

<!-- Help Modal -->
<div id="helpModal" class="modal">
    <div class="modal-content">
        <button class="close-btn" onclick="document.getElementById('helpModal').style.display='none'">&times;</button>
        <h2>How to Use</h2>
        <p>Write a natural language instruction describing what the browser agent should do. The system will automatically parse it into structured actions and generate executable Playwright Python code.</p>

        <strong>Supported commands:</strong>
        <ul>
            <li><strong>Visit a website:</strong> "Go to amazon.in", "Open flipkart.com", "Visit https://google.com"</li>
            <li><strong>Search for products:</strong> "search macbook", "find iPhone 16", "look for wireless earbuds"</li>
            <li><strong>Login (expects failure by default):</strong> "login with user@example.com password wrong123"</li>
            <li><strong>Combine actions:</strong> "Visit amazon.in and search for laptop"</li>
        </ul>

        <strong>Try these examples (copy and paste):</strong>
        <div class="example">Visit amazon.in and search for macbook</div>
        <div class="example">Go to flipkart.com, search for oneplus</div>
        <div class="example">Open https://facebook.com and login with test@user.com password secret</div>
        <div class="example">visit google.com search airpods</div>
        <div class="example">Go to www.amazon.in search shoes</div>
        <div class="example">Visit https://www.amazon.com and look for laptop deals</div>
    </div>
</div>

<script>
    // Close modal when clicking outside
    window.onclick = function(event) {
        const modal = document.getElementById('helpModal');
        if (event.target === modal) {
            modal.style.display = "none";
        }
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

    if request.method == 'POST':
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
        code=code
    )

if __name__ == '__main__':
    print("🚀 AI Agent Test Builder started!")
    print("📌 Open http://localhost:5000 in your browser")
    print("ℹ️  'How to Use' button is now clearly labeled in the top-right corner")
    app.run(debug=True, port=5000)