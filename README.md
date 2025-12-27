# 🤖 AI-Powered Automated Website Testing Platform

**AI Agent for Intelligent Browser Automation - Natural Language to Test Scripts**

An enterprise-grade AI-powered browser automation platform that converts plain English instructions into robust automated web tests. Built for developers, QA engineers, and non-technical users alike.

---

## 🎯 Project Overview

This platform revolutionizes web testing by allowing anyone to perform sophisticated browser automation without writing code. Powered by advanced natural language parsing, intelligent error handling, and comprehensive reporting - perfect for modern web testing workflows.

### ✨ Key Features

#### Core Capabilities
- 🗣️ **Natural Language Processing** - Write test cases in plain English
- 🌐 **Multi-Browser Support** - Chrome, Firefox, Edge, Brave, Opera, WebKit, Chromium
- 👁️ **Flexible Execution Modes** - Visible mode for debugging, headless for CI/CD
- 🧠 **Smart Parser** - Rule-based system with 10+ action types, no API dependencies
- 💻 **Playwright Code Generation** - Creates reusable, production-ready Python scripts
- 🔄 **Retry Logic** - Automatic retry with exponential backoff for failed actions
- 🎯 **Adaptive DOM Mapping** - Intelligent element detection with multiple fallback strategies

#### Milestone 4 Enhancements
- ⏱️ **Execution Timing** - Precise start/end time tracking with duration metrics
- 📊 **Advanced Reporting** - Comprehensive test reports with success rates and metrics
- 🛡️ **Error Handling** - Enhanced error tracking with detailed context and recovery
- 📈 **Progress Visualization** - Animated progress bars and real-time status updates
- 🎨 **Polished UI** - Modern design with gradient effects and smooth animations
- 📸 **Screenshot Capture** - Full-page screenshots at every critical step
- 💾 **Test History** - Complete audit trail of all test executions

---

## 🏗️ Architecture & Technology Stack

### Technology Stack
| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend** | Python | 3.14 |
| **Web Framework** | Flask | 3.0 |
| **Automation** | Playwright | 1.40 |
| **Frontend** | HTML5, CSS3, JavaScript ES6+ | - |
| **Parser** | Custom SimpleParser (Rule-Based) | v1.0 |
| **Reporting** | JSON + fpdf2 | - |
| **Architecture** | REST API with Modular Design | - |

### System Architecture
```
┌─────────────────┐
│   Dashboard UI  │  (Natural Language Input)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Flask Backend  │  (API Endpoints)
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│Parser  │ │CodeGenerator │
└────┬───┘ └──────┬───────┘
     │            │
     └─────┬──────┘
           ▼
    ┌──────────────┐
    │  Executor    │  (Playwright)
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │   Reports    │  (JSON/Screenshots)
    └──────────────┘
```

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+ installed
- pip (Python package manager)
- Git
- 4GB RAM minimum
- Internet connection (for browser downloads)

### Quick Start

#### Step 1: Clone Repository
```bash
git clone https://github.com/Yashaswini-V21/AI-Automated-Testing.git
cd AI-Automated-Testing
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Install Playwright Browsers
```bash
python -m playwright install chromium firefox webkit
```

### Step 4: Run Application
```bash
python run_production.py
```

### Step 5: Access Dashboard
Navigate to: **http://localhost:5000**

---

## 🚀 Usage Guide

### Quick Start Example

1. **Launch Dashboard** - Click "Enter Dashboard" from landing page
2. **Write Test Instructions**:
   ```
   go to github.com and search for playwright python
   ```
3. **Configure Test**:
   - Browser: Google Chrome
   - Mode: Visible (for debugging) or Headless (for CI/CD)
4. **Execute** - Click "Run Test" button
5. **View Results** - Watch real-time execution with:
   - Live progress bar
   - Execution metrics
   - Step-by-step breakdown
   - Screenshot gallery

### Example Test Commands

#### Basic Navigation
```
go to github.com
```

#### E-commerce Testing
```
go to amazon.com and search for lenovo laptop and click the first product
```

#### Streaming Services
```
navigate to netflix.com and search for stranger things
```

#### Multi-Step Workflows
```
open youtube.com, search for AI tutorials, click first video, wait 3 seconds
```

### Supported Action Types (10+)
- **Navigate**: `go to`, `open`, `visit`, `navigate to`
- **Search**: `search for`, `type`, `enter`, `input`
- **Click**: `click`, `press`, `select` (with positions: first, second, third, last)
- **Fill**: `fill`, `enter text into`
- **Hover**: `hover over`, `mouse over`
- **Scroll**: `scroll`, `scroll down`, `scroll up`
- **Wait**: `wait`, `pause`, `delay`
- **Verify**: `verify`, `check`, `assert`
- **Screenshot**: `take screenshot`, `capture`
- **Refresh**: `refresh`, `reload`

---

## 📊 Milestone 4: Reporting Features

### Comprehensive Test Reports
Each test execution generates detailed reports with:

#### Metrics Tracked
- ⏱️ **Execution Time** - Precise start/end timestamps and duration
- 📈 **Success Rate** - Percentage of passed vs failed steps
- 🎯 **Step Breakdown** - Detailed pass/fail status for each action
- 🌐 **Browser Info** - Browser type and configuration
- 📸 **Visual Evidence** - Full-page screenshots at each step
- ❌ **Error Details** - Error type, message, and context

#### Report Export Formats
- **JSON** - Structured data for CI/CD integration
- **Visual Dashboard** - Real-time results with progress tracking
- **Screenshots** - Organized gallery view with timestamps

### Error Handling & Recovery
- **Retry Logic** - Automatic retry for transient failures (3 attempts)
- **Fallback Strategies** - Multiple selector patterns for element detection
- **Graceful Degradation** - Continues execution when possible
- **Detailed Logging** - Comprehensive error tracking with stack traces

---

## 📁 Project Structure

```
AI-Automated-Testing/
├── app.py                      # Flask REST API endpoints
├── run_production.py           # Production WSGI server
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

## 📁 Project Structure

```
AI AGENT/
├── app.py                  # Flask application
├── agent/                  # AI Agent modules
│   ├── __init__.py
│   ├── parser.py          # Instruction parser
│   ├── code_generator.py  # Playwright code generator
│   ├── executor.py        # Test executor
│   └── workflow.py        # LangGraph workflow
├── static/                # Frontend assets
│   ├── css/
│   ├── js/
│   └── images/
├── templates/             # HTML templates
├── test_site/             # Sample test website
└── reports/               # Generated test reports
```

## 🎨 Technology Stack

- **Backend**: Python, Flask, LangGraph
- **Browser Automation**: Playwright
- **AI**: OpenAI GPT-4, LangChain
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

