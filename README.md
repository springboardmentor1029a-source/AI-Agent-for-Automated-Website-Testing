# 🤖 AI Agent To Test Websites Automatically Using Natural Language

**Yash AI Testing Agent - Intelligent Browser Automation Platform**

An AI-powered browser automation platform that converts plain English instructions into automated web tests. No coding required - just describe what you want to test in natural language!

---

## 🎯 Project Overview

This project enables anyone to perform automated browser testing without writing a single line of code. Simply type commands like "go to youtube.com and search for python tutorials" and watch the AI agent automatically control the browser, perform actions, and generate detailed test reports.

### ✨ Key Features

- 🗣️ **Natural Language Input** - Write test cases in plain English
- 🌐 **Multi-Browser Support** - Chrome, Firefox, Microsoft Edge
- 👁️ **Visible & Headless Modes** - Watch tests run or execute silently
- 🧠 **Smart Parser** - Rule-based system, no API dependencies, 100% reliable
- 💻 **Code Generation** - Generates reusable Playwright Python scripts
- 📸 **Screenshot Capture** - Full-page screenshots at every step
- 📊 **Professional Reports** - Export results as PDF or JSON
- 📜 **Test History** - Track all previous test executions
- 🎨 **Modern UI** - Beautiful animated dashboard with gradient effects

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.14, Flask 3.0 |
| **Automation** | Playwright 1.40 |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Parser** | Custom Rule-Based SimpleParser |
| **Export** | fpdf2 for PDF generation |
| **Architecture** | REST API with modular design |

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for browser downloads)

### Step 1: Clone Repository
```bash
git clone <your-repo-url>
cd "AI AGENT"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Install Browsers
```bash
python -m playwright install chromium firefox msedge
```

### Step 4: Run Application
```bash
python run_production.py
```

### Step 5: Open Browser
Navigate to: **http://localhost:5000**

---

## 🚀 Usage Guide

### Quick Start Example

1. **Open Dashboard** - Click "Enter Dashboard" on landing page
2. **Enter Test Description**:
   ```
   go to youtube.com and search for python tutorials
   ```
3. **Select Browser**: Google Chrome
4. **Select Mode**: Visible (to watch it work)
5. **Click "Run Agent"**
6. **Watch** - Browser opens and performs actions automatically!

### Example Test Commands

```
# Simple navigation
github.com

# Navigation with search
go to amazon.com and search for laptops

# YouTube search
www.youtube.com search AI tutorials

# Google search
google.com type artificial intelligence
```

---

## 📁 Project Structure

```
AI AGENT/
├── app.py                      # Main Flask application
├── run_production.py           # Production server runner
├── requirements.txt            # Python dependencies
├── agent/
│   ├── simple_parser.py        # Natural language parser
│   ├── code_generator.py       # Playwright code generator
│   └── executor.py             # Test executor
├── templates/
│   ├── index.html              # Landing page with robot animation
│   └── dashboard_modern.html   # Main testing dashboard
└── static/
    ├── css/
    │   └── landing.css         # Landing page styles
    ├── js/
    │   └── landing.js          # Landing page animations
    └── screenshots/            # Test screenshots (auto-generated)
```
