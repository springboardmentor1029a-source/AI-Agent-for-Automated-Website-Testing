# 🤖 AI-Powered E2E Testing Agent

An intelligent AI-based tool that converts **natural language instructions into Playwright E2E tests**, executes them in a headless browser, and generates detailed test reports using a clean Streamlit UI.

> 🔥 Perfect project for **QA Automation, SDET, Full Stack, AI + Testing** portfolios.

---

## ✨ Features

- 🗣️ Write tests in plain English
- 🤖 Auto-generates Playwright test scripts
- 🌐 Runs tests in headless Chromium
- 📊 Shows detailed pass/fail reports
- ⚡ Fast template-based execution
- 🎨 Clean Streamlit UI
- 🧠 Structured workflow using LangGraph

---

## 🛠 Tech Stack

- Python
- Playwright
- Streamlit
- LangGraph
- LangChain
- Google Gemini API

---

## 🚀 Setup & Run

```bash
git clone https://github.com/ShahanaKV/e2e-testing-agent.git
cd e2e-testing-agent

python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
playwright install

streamlit run app.py
