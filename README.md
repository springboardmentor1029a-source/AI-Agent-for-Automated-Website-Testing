🌐 Bindu WebQA Agent 
AI Agent for Automated Website Testing

🚀 Project Overview

Web UI for AI-Powered Browser Automation is an interactive, user-friendly interface built on top of the browser-use framework.
The project enables AI agents to interact with real websites through a graphical Web UI, making browser automation accessible, observable, and easy to control.

This WebUI is designed using Gradio and supports multiple Large Language Models (LLMs), persistent browser sessions, custom browser integration, and automated web interaction workflows.

🎯 Objectives Achieved

✅ Integrated browser-use with a Gradio WebUI

✅ Enabled natural language instructions for website testing

✅ Connected LLMs to browser automation workflows

✅ Implemented persistent browser sessions

✅ Supported custom browser usage with user profiles

✅ Displayed real-time browser interaction results

🧠 System Architecture Flow
User Input (WebUI – Natural Language)
        ↓
LLM Processing (OpenAI / Azure / Ollama / DeepSeek)
        ↓
Browser-Use Agent
        ↓
Playwright Browser Actions
        ↓
Live Browser Execution
        ↓
Test Output & Observations (UI)

🧩 Project Description (Milestone 2)

Bindu WebQA Agent is an AI-powered web testing application that allows users to test websites by simply describing actions in plain English.

The system leverages:

browser-use for AI browser control

Playwright for browser automation

Gradio for WebUI interaction

LLMs for instruction understanding and action planning

🚀 Key Features Implemented in Milestone 2

🖥️ WebUI Interface
Gradio-based user interface for entering test instructions

🤖 LLM-Powered Instruction Handling
Converts natural language into browser actions

🌐 Automated Website Interaction
Navigation, clicks, form interactions, and UI validation

♻️ Persistent Browser Sessions
Browser state is preserved across tasks

🌍 Custom Browser Support
Uses existing browser profiles to avoid re-login

🛠️ Technology Stack
🔹 Backend & AI

Python 3.11

browser-use

Playwright

LLMs (OpenAI, Azure OpenAI, Ollama, DeepSeek)

🔹 Frontend

Gradio WebUI
HTML5 / CSS / JavaScript
```
web-ui/
│
├── .github/                # GitHub workflows and issue templates
├── .venv/                  # Python virtual environment
├── .vscode/                # VS Code editor settings
│
├── assets/                 # Images and static assets used in UI
│
├── src/                    # Core source code of the Web UI Agent
├── tests/                  # Test cases for validating functionality
├── tmp/                    # Temporary files and runtime data
│
├── .dockerignore           # Files ignored during Docker build
├── .env                    # Environment variables (local use)
├── .env.example            # Sample environment configuration
├── .gitignore              # Git ignored files and folders
│
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker image build instructions
│
├── LICENSE                 # Project license
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── SECURITY.md             # Security policies
├── supervisord.conf        # Process manager configuration
└── webui.py                # Main application entry point

```
⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/springboardmentor1029a-source/AI-Agent-for-Automated-Website-Testing.git
cd AI-Agent-for-Automated-Website-Testing

2️⃣ Create Virtual Environment
uv venv --python 3.11
Activate:

Windows

.\.venv\Scripts\Activate.ps1

macOS / Linux

source .venv/bin/activate

3️⃣ Install Dependencies
uv pip install -r requirements.txt

Install Playwright browsers:

playwright install --with-deps

4️⃣ Configure Environment
cp .env.example .env

(Add API keys if required)

🚀 Running the Application
python webui.py --ip 127.0.0.1 --port 7788

Open in browser:

http://127.0.0.1:7788

💡 Usage Examples

“Open Amazon and search for iPhone 15”

“Navigate to the contact page and verify the form is visible”

“Check all links and images on the homepage”

📊 Project Outcome

Successfully demonstrated AI-controlled browser testing

Verified WebUI → Agent → Browser execution flow

Built a strong foundation for advanced testing features in future milestones

📝 License

This project is developed for educational and internship purposes.
