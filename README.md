# 🌐 Bindu WebQA Agent - WebUI

Bindu WebQA Agent is a **Gradio-based UI** to control a browser using AI. Supports natural language instructions, automatic Playwright code generation, headless execution, and detailed reports.  

---

<details>
<summary>🌟 Features</summary>

- ✨ **Natural Language Input** – Describe browser tests in plain English.  
- 💻 **Auto Code Generation** – AI generates Playwright test scripts automatically.  
- ⚡ **Headless Execution** – Run tests in a fast headless environment.  
- 📊 **Detailed Reports** – Comprehensive pass/fail reports with insights.  
- 🖥️ **Custom Browser Support** – Use your own browser and maintain sessions.  
- 🔄 **Persistent Browser Sessions** – Keep browser open between tasks.  

</details>

<details>
<summary>💻 Installation (Local)</summary>

```bash
git clone https://github.com/browser-use/web-ui.git
cd web-ui

# Create Python environment
uv venv --python 3.11

# Activate
# Windows CMD
.venv\Scripts\activate
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
playwright install --with-deps

# Copy and edit environment file
copy .env.example .env       # Windows
cp .env.example .env         # macOS/Linux/PowerShell

# Run the WebUI
python webui.py --ip 127.0.0.1 --port 7788

Open browser at http://127.0.0.1:7788

Optional: Use your own browser by setting BROWSER_PATH and BROWSER_USER_DATA in .env.

Login:

Username: admin

Password: 1234

Tabs:

📘 Instructions – Features & workflow

🤖 AI Browser Agent – Control the browser, run tests, view reports

Workflow:

Parse Instructions (natural language)

Extract Actions (browser operations)

Generate Code (Playwright scripts)

Execute Test (headless/normal)

Generate Report (results & insights)

</details> <details> <summary>🎨 Customization</summary>

Modify CUSTOM_CSS in webui.py for colors and layout

Edit INSTRUCTIONS_MD for instructions/workflow

Change theme_name argument to switch themes

</details> <details> <summary>📜 Changelog</summary>

2025/01/26: Added DeepSeek-r1 integration for advanced reasoning

2025/01/10: Docker setup + persistent browser support

2025/01/06: New WebUI design & improved usability

</details> <details> <summary>💡 Credits & License</summary>

Built on browser-use

Thanks to WarmShao

License: MIT

</details> ```

✅ Features of this version:

Collapsible sections for a cleaner look

Badges for GitHub, Discord, Docs, Twitter

Video demo embedded

Instructions separate for Local vs Docker installation

Modern “GitHub-style” formatting
