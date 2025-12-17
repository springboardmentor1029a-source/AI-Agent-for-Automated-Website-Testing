# app.py
from flask import Flask, request, render_template_string
from playwright.sync_api import sync_playwright
import re
import threading

app = Flask(__name__)

# Fixed & simple URL + action extractor
def extract_action(instruction: str):
    instruction = instruction.lower().strip()

    # Default values
    url = "https://www.google.com"
    action = "visit"
    product = "iphone"
    email = "wrong@test.com"
    password = "wrong123"

    # Extract URL (supports amazon.in, flipkart.com, facebook.com, etc.)
    url_match = re.search(r'(https?://)?([a-zA-Z0-9.-]+\.(com|in|org|net|co\.in|co\.uk|de|fr))', instruction)
    if url_match:
        raw_url = url_match.group(0)
        if not raw_url.startswith("http"):
            raw_url = "https://" + raw_url
        url = raw_url.split()[0].rstrip(".,!?")  # clean trailing punctuation

    # Detect search action
    if any(word in instruction for word in ["search", "find", "look for"]):
        action = "search"
        # Look for known products
        for p in ["macbook", "iphone", "laptop", "shoes", "watch", "tv", "samsung", "oneplus"]:
            if p in instruction:
                product = p
                break
        else:
            # Get first word after "search"
            after = instruction.split("search", 1)[1] if "search" in instruction else ""
            match = re.search(r'\b([a-zA-Z]+)\b', after)
            if match:
                product = match.group(1)

    # Detect login action
    if any(word in instruction for word in ["login", "log in", "signin"]):
        action = "invalid_login"
        email_match = re.search(r'[\w\.-]+@[\w\.-]+', instruction)
        if email_match:
            email = email_match.group(0)
        pass_match = re.search(r'(?:pass|pwd)[\s:]?(\w+)', instruction)
        if pass_match:
            password = pass_match.group(1)

    return {"url": url, "action": action, "product": product, "email": email, "password": password}

# Main test runner
def run_playwright_test(instruction: str) -> str:
    config = extract_action(instruction)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            page = context.new_page()
            page.set_default_timeout(25000)

            print(f"Opening: {config['url']}")
            page.goto(config["url"], wait_until="domcontentloaded")

            # Close popups (Amazon, Flipkart, etc.)
            try:
                page.click("text=Close", timeout=5000)
                page.click("#nav-main >> text=Skip", timeout=3000)
                page.click("button:has-text('Not now')", timeout=3000)
            except:
                pass

            if config["action"] == "search":
                # Best search box selector (works on Amazon, Flipkart, etc.)
                search_box = page.locator("input[placeholder*='search' i], input[name='q'], input#twotabsearchtextbox, input[name='field-keywords'], input[title='Search'], input._3704LK").first

                if search_box.is_visible(timeout=10000):
                    search_box.fill(config["product"])
                    search_box.press("Enter")
                    page.wait_for_load_state("networkidle", timeout=20000)

                    # Count results - works on Amazon.in, Flipkart, etc.
                    result_count = 0
                    selectors = [
                        "div[data-component-type='s-search-result']",     # Amazon
                        "._1AtVbE, ._2kHMtA",                             # Flipkart
                        "div.srp-river-results div[data-asin]",           # Amazon fallback
                        "div._4ddWXP, div._2kHMtA"                        # Flipkart fallback
                    ]
                    for sel in selectors:
                        result_count = page.locator(sel).count()
                        if result_count > 0:
                            break

                    if result_count == 0:
                        # Last fallback: look for any product title containing the word
                        result_count = page.locator(f"text={config['product']}").count()

                    return f"Found {result_count} results for '{config['product']}' on {config['url']}"

                else:
                    return "Could not find search box."

            elif config["action"] == "invalid_login":
                page.fill("input[name='email'], input#email", config["email"])
                page.fill("input[name='pass'], input#pass", config["password"])
                page.click("button[name='login'], button:has-text('Log In')")
                error = page.locator("text=incorrect, text=wrong, text=not found, text=invalid").first
                if error.is_visible(timeout=8000):
                    msg = error.text_content().strip()
                    return f"Login failed (as expected): {msg[:100]}"
                return "No error shown — login may have worked!"

            return f"Successfully opened {config['url']}"

    except Exception as e:
        return f"Error: {str(e)}"

# Thread runner
def background_test(instruction, result_holder):
    result_holder["result"] = run_playwright_test(instruction)

# HTML
HTML = '''
<!DOCTYPE html>
<html><head><title> AI agent </title>
<style>
    body {font-family: system-ui; background: #667eea; color: white; padding: 40px; min-height: 100vh;}
    .box {max-width: 700px; margin: auto; background: rgba(255,255,255,0.95); color: #333; padding: 40px; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.3);}
    h1 {text-align: center; color: #667eea;}
    textarea {width: 100%; height: 100px; padding: 15px; font-size: 16px; border: 2px solid #ddd; border-radius: 12px;}
    button {background: #667eea; color: white; padding: 15px; font-size: 18px; border: none; border-radius: 12px; width: 100%; cursor: pointer;}
    button:hover {background: #5a67d8;}
    .result {margin-top: 20px; padding: 20px; border-radius: 12px; font-weight: bold; font-size: 18px;}
    .success {background: #d4edda; color: #155724;}
    .error {background: #f8d7da; color: #721c24;}
</style></head>
<body>
<div class="box">
    <h1>AI agent test runner</h1>
    <form method="post">
        <textarea name="instruction" placeholder="Try: visit amazon.in search macbook and count results" required>{{ instruction }}</textarea>
        <button type="submit">Run Test</button>
    </form>
    {% if result %}
    <div class="result {{ 'success' if 'Found' in result or 'failed' in result else 'error' }}">{{ result }}</div>
    {% endif %}
</div>
</body></html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    instruction = ""

    if request.method == 'POST':
        instruction = request.form['instruction']
        holder = {}
        t = threading.Thread(target=background_test, args=(instruction, holder))
        t.start()
        t.join(timeout=40)
        result = holder.get("result", "Timeout or error")

    return render_template_string(HTML, result=result, instruction=instruction)

if __name__ == '__main__':
    print("Starting Playwright AI Tester...")
    print("Make sure you ran: playwright install chromium")
    app.run(debug=True, port=5000)