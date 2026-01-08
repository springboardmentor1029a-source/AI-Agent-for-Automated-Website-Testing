from dotenv import load_dotenv
load_dotenv()

import argparse
import gradio as gr
from src.webui.interface import theme_map, create_ui

# ================= LOGIN LOGIC =================
def check_login(username, password):
    if username == "admin" and password == "1234":
        return gr.update(visible=False), gr.update(visible=True), "Login successful"
    else:
        return gr.update(visible=True), gr.update(visible=False), "Invalid username or password"

# ================= CUSTOM CSS =================

CUSTOM_CSS = """
/* ===== PAGE BACKGROUND ===== */
html, body {
    min-height: 100vh;
    background: #e6f4ff !important;   /* Light blue background */
    color: #0a2540 !important;
    overflow-y: auto;
}

.gradio-container {
    min-height: 100vh;
    background: #e6f4ff !important;
    overflow-y: auto;
}

/* Remove default gradio background */
.gradio-container * {
    background-color: transparent;
}

/* ===== LOGIN / INSTRUCTIONS BOX ===== */
.white-box, .instructions-box {
    width: 720px;
    padding: 30px;
    background: #cce9ff !important;  /* light blue box */
    color: #0a2540 !important;
    border-radius: 14px;
    box-shadow: 0 12px 25px rgba(0,0,0,0.15);
    text-align: center;
    margin: auto;
    margin-top: 8%;
}

/* Headings */
.center-heading {
    text-align: center;
    margin-bottom: 20px;
}

/* Inputs */
input, textarea {
    background: #b3ddff !important;
    color: #0a2540 !important;
    border: 1px solid #4db8ff !important;
    border-radius: 6px;
}

/* Button */
button {
    background: #4db8ff !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: bold;
}

/* ===== FEATURE CARDS ===== */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 40px;
}

.feature-card {
    background: #b3ddff !important;
    color: #0a2540 !important;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.12);
    text-align: left;
}

.feature-card h4, .feature-card p {
    color: #0a2540 !important;
}

/* ===== WORKFLOW ===== */
.workflow-wrapper {
    background: #cce9ff !important;
    padding: 30px;
    border-radius: 14px;
    box-shadow: 0 12px 25px rgba(0,0,0,0.15);
    width: 600px;
    margin: auto;
}

.workflow-title, .workflow-text h4, .workflow-text p {
    color: #0a2540 !important;
}

/* ===== AI Browser Agent Box ===== */
.ai-agent-box {
    background: #d9f0ff !important;   /* light blue only */
    color: #0a2540 !important;
    padding: 20px;
    border-radius: 14px;
    min-height: 80vh;
    text-align: center;
}



"""

# ================= INSTRUCTIONS =================
INSTRUCTIONS_MD = """
<div class="feature-grid">

  <div class="feature-card">
    <h4>✨ Natural Language Input</h4>
    <p>Describe tests in plain English — no coding required</p>
  </div>

  <div class="feature-card">
    <h4>💻 Auto Code Generation</h4>
    <p>AI generates Playwright test scripts automatically</p>
  </div>

  <div class="feature-card">
    <h4>⚡ Headless Execution</h4>
    <p>Tests run in a fast headless browser environment</p>
  </div>

  <div class="feature-card">
    <h4>📊 Detailed Reports</h4>
    <p>Get comprehensive pass/fail reports with insights</p>
  </div>

</div>

<div class="workflow-wrapper">
  <div class="workflow-title">● Agent Workflow</div>

  <div class="workflow-step">
    <div class="workflow-dot"></div>
    <div class="workflow-text">
      <h4>Parse Instructions</h4>
      <p>Interpreting natural language input</p>
    </div>
  </div>

  <div class="workflow-step">
    <div class="workflow-dot"></div>
    <div class="workflow-text">
      <h4>Extract Actions</h4>
      <p>Converting instructions to browser actions</p>
    </div>
  </div>

  <div class="workflow-step">
    <div class="workflow-dot"></div>
    <div class="workflow-text">
      <h4>Generate Code</h4>
      <p>Creating Playwright test scripts</p>
    </div>
  </div>

  <div class="workflow-step">
    <div class="workflow-dot"></div>
    <div class="workflow-text">
      <h4>Execute Test</h4>
      <p>Running tests in headless browser</p>
    </div>
  </div>

  <div class="workflow-step">
    <div class="workflow-dot"></div>
    <div class="workflow-text">
      <h4>Generate Report</h4>
      <p>Compiling test results</p>
    </div>
  </div>

</div>
"""

# ================= MAIN APP =================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7788)
    parser.add_argument("--theme", default="Ocean", choices=theme_map.keys())
    args = parser.parse_args()

    browser_ui = create_ui(theme_name=args.theme)

    with gr.Blocks(css=CUSTOM_CSS) as app:

        # 🔐 LOGIN PAGE
        login_section = gr.Column(visible=True)
        with login_section:
            with gr.Column(elem_classes=["white-box", "center-heading"]):
                gr.Markdown("## 🌐 Bindu WebQA Agent")
                gr.Markdown("### Control your browser with AI assistance")
                username = gr.Textbox(label="Username")
                password = gr.Textbox(label="Password", type="password")
                login_btn = gr.Button("Login")
                login_msg = gr.Markdown()

        # 🌐 MAIN PAGE
        main_section = gr.Column(visible=False)
        with main_section:
            with gr.Tabs():
                with gr.Tab("📘 Instructions"):
                    with gr.Column(elem_classes=["white-box", "instructions-box", "center-heading"]):
                        gr.Markdown("## 🌐 Bindu WebQA Agent")
                        gr.Markdown("### Control your browser with AI assistance")
                        gr.Markdown(INSTRUCTIONS_MD)

                with gr.Tab("🤖 AI Browser Agent"):
                    with gr.Column(elem_classes=["ai-agent-box"]):
                        browser_ui.render()

        # 🔄 LOGIN ACTION
        login_btn.click(
            check_login,
            inputs=[username, password],
            outputs=[login_section, main_section, login_msg]
        )

    app.queue().launch(server_name=args.ip, server_port=args.port)

if __name__ == "__main__":
    main()
