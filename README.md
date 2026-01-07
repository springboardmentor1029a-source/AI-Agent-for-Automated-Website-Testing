<<<<<<< HEAD
# AI-Agent-for-Automated-Website-Testing
=======
# Milestone 1: Foundation Setup

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows: venv\Scripts\activate


# 3. Install dependencies (with venv activated)
pip install -r requirements.txt

# 4. Install Playwright browser
playwright install chromium

# 5. Run the application
python app.py
```

## Overview

This milestone establishes the foundation for the Web Test Agent project:

- Python environment setup with dependencies
- Flask server for serving test pages
- Baseline LangGraph agent configuration

## ✅ How to Know Milestone 1 is Complete

**Simple verification - check these 3 things:**

### 1. ✅ Python Environment & Dependencies
- **Check:** Run `pip list` (with venv activated)
- **You should see:** Flask, Playwright, LangGraph in the list
- **Test:** `python -c "import flask, playwright, langgraph; print('OK')"` should work

### 2. ✅ Flask Server & Test Page
- **Check:** Run `python app.py` and open `http://localhost:5000` in browser
- **You should see:** A beautiful test page with buttons, forms, and agent interface
- **Test:** Health check at `http://localhost:5000/health` should return JSON

### 3. ✅ LangGraph Agent
- **Check:** File `agent.py` exists and works
- **Test:** Type a message in the browser's agent input box and click "Send"
- **You should see:** Agent response appears below the input

**If all 3 work = Milestone 1 is COMPLETE! 🎉**

For detailed verification steps, see [VERIFICATION.md](VERIFICATION.md)

## Requirements

- Python 3.8 or higher
- pip (usually comes with Python)
- Virtual environment support (built into Python 3.3+)

**Check your Python version:**

```bash
python --version  # or python3 --version
```

**Check pip:**

```bash
pip --version  # or pip3 --version
```

## Installation

### Step 1: Create Virtual Environment

**On Windows:**

```bash
python -m venv venv
```

**On macOS/Linux:**

```bash
python3 -m venv venv
```

### Step 2: Activate Virtual Environment

**On Windows (Command Prompt):**

```bash
venv\Scripts\activate
```

**On Windows (PowerShell):**

```bash
venv\Scripts\Activate.ps1
```

**On macOS/Linux:**

```bash
source venv/bin/activate
```

**Verify activation:** You should see `(venv)` at the beginning of your command prompt.

### Step 3: Install Dependencies

**Make sure your virtual environment is activated first!** Then run:

```bash
pip install -r requirements.txt
```

This will install:

- Flask (web server)
- Playwright (browser automation)
- LangGraph (workflow orchestration)
- LangChain (LLM framework)
- Other required dependencies

### Step 4: Install Playwright Browsers

After installing dependencies, install the Playwright browser:

```bash
playwright install chromium
```

### Step 5: Set Up Environment Variables

```bash
# On Windows
copy .env.example .env

# On macOS/Linux
cp .env.example .env
```

Edit `.env` if needed (defaults are fine for milestone 1).

### Step 6: Verify Installation

Run the setup verification script:

```bash
python test_setup.py
```

This will check that all modules are installed correctly.

## Project Structure

```
milestone1/
├── app.py                 # Flask server
├── agent.py               # Baseline LangGraph agent
├── requirements.txt       # Python dependencies
├── templates/
│   └── test_page.html    # Static HTML test page
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Running the Application

**Important:** Make sure your virtual environment is activated before running!

1. **Activate virtual environment (if not already activated):**

   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
2. **Start the Flask server:**

```bash
python app.py
```

3. **Open your browser:**

```
http://localhost:5000
```

4. **Test the agent API:**

```bash
curl -X POST http://localhost:5000/api/agent \
  -H "Content-Type: application/json" \
  -d '{"input": "Test message"}'
```

**Alternative:** You can also use the simple runner:

```bash
python run.py
```

## Features

### ✅ Completed in Milestone 1

- [X] Python environment setup
- [X] Dependencies installed (Flask, Playwright, LangGraph)
- [X] Flask server running
- [X] Static HTML test page with interactive elements
- [X] Baseline LangGraph agent configuration
- [X] API endpoint for agent communication
- [X] Health check endpoint

### 🔄 Baseline Agent

The baseline agent in `agent.py` provides:

- Simple LangGraph workflow structure
- Input processing node
- Response generation node
- Basic state management

**Note:** The agent currently returns simple acknowledgments. LLM integration will be added in later milestones.

## API Endpoints

### GET `/`

Serves the main HTML test page.

### POST `/api/agent`

Processes user input through the LangGraph agent.

**Request:**

```json
{
  "input": "Your test instruction here"
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Agent response message",
  "input": "Original input"
}
```

### GET `/health`

Health check endpoint.

**Response:**

```json
{
  "status": "healthy",
  "service": "Web Test Agent - Milestone 1"
}
```

## Test Page Features

The HTML test page includes:

- Interactive buttons (primary, secondary, success, danger)
- Form elements (text input, email, textarea)
- Navigation links
- LangGraph agent interface
- Real-time agent communication

## Next Steps (Future Milestones)

- Milestone 2: Instruction parsing and action generation
- Milestone 3: Code generation with LLM
- Milestone 4: Test execution and reporting

## Troubleshooting

**Virtual environment not activated:**

- Make sure you see `(venv)` in your command prompt
- If not, activate it using the commands in Step 2 above
- Always activate the venv before running any Python commands

**Port already in use:**

- Change `PORT` in `.env` file
- Or kill the process using port 5000

**Playwright installation issues:**

- Make sure you've run `playwright install chromium` **after** activating venv
- Check that Python and pip are in your PATH
- Try: `python -m playwright install chromium`

**Import errors:**

- **First, ensure virtual environment is activated** (you should see `(venv)` in prompt)
- If venv is activated but still getting errors, reinstall dependencies:
  ```bash
  pip install -r requirements.txt --force-reinstall
  ```

**Module not found errors:**

- Make sure you installed dependencies **while the venv was activated**
- Deactivate and reactivate the venv, then reinstall:
  ```bash
  deactivate  # Exit venv
  # Delete venv folder if needed: rm -rf venv (Linux/Mac) or rmdir /s venv (Windows)
  python -m venv venv  # Recreate venv
  # Activate venv again
  pip install -r requirements.txt
  ```

**PowerShell execution policy error (Windows):**

- If you get an execution policy error in PowerShell, run:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
>>>>>>> e9efd0e (Add AI website testing agent implementation)
