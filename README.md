# AI Agent to Test Websites Automatically Using Natural Language

## 1. Introduction / Objective
This project implements an intelligent agent capable of performing automated end-to-end (E2E) testing on web applications. The agent accepts natural language instructions, interprets them, generates Playwright test scripts, executes those scripts in a headless browser, and produces detailed test reports.

## 2. Methodology / Workflow
### Instruction Interpretation Phase
- Accepts user-defined natural language test cases.
- Parses input and identifies actionable test steps.

### Code Generation Phase
- Converts interpreted steps into executable Playwright scripts.
- Dynamically generates assertions to validate expected outcomes.

### Execution Phase
- Runs Playwright tests in a headless browser environment.
- Monitors DOM and adapts dynamically to web structure changes.

### Reporting Phase
- Summarizes results including passed/failed assertions.
- Generates human-readable test reports for review.

## 3. Modules
- **Instruction Parser Module**: Interprets natural language test descriptions and maps them to browser actions.
- **Code Generation Module**: Converts parsed actions into executable Playwright Python scripts.
- **Execution Module**: Runs tests headlessly and captures runtime logs.
- **Assertion & Reporting Module**: Validates expected results and compiles test summaries.

## 4. System Design / Architecture
The architecture integrates LangGraph for agent workflow orchestration and Playwright for browser automation. Each test cycle follows a pipeline of instruction → code generation → execution → reporting.

## 5. Week-wise Module Implementation and High-Level Requirements

### Milestone 1: Week 1–2 (Environment & Core Setup)
**Goal**: Set up the foundation, dependencies, and basic server structure.

*   **Execution Detail**:
    *   Established the Python virtual environment and installed core libraries (`flask`, `playwright`, `langgraph`).
    *   Created the entry point for the backend server (`app.py`) to handle API requests.
*   **Files Added**:
    *   `backend/requirements.txt`: Lists all project dependencies.
    *   `backend/app.py`: The main Flask application server.
    *   `backend/agent/__init__.py`: Package initialization.

### Milestone 2: Week 3–4 (Instruction Parsing)
**Goal**: Build the brain that understands natural language.

*   **Execution Detail**:
    *   Implemented `parse_instruction` to take raw text (e.g., "Go to Google") and convert it into structured JSON objects (e.g., `{"type": "goto", "value": "google.com"}`).
    *   Defined the `run_agent` workflow to orchestrate the flow from input to parsing.
*   **Files Added**:
    *   `backend/agent/parser.py`: Contains logic to map text to command types (`goto`, `search`, `verify`).
    *   `backend/agent/graph.py`: Defines the main agent entry point and orchestration.

### Milestone 3: Week 5–6 (Code Generation & Execution)
**Goal**: Make the agent act on the web using Playwright.

*   **Execution Detail**:
    *   The **Generator** converts the structured JSON steps into Playwright-specific actions.
    *   The **Executor** uses `sync_playwright` to launch a browser (Chromium), open a context, and execute the steps.
    *   Implemented intelligent wait mechanisms (`wait_for_load_state`) and interaction logic (clicking, typing).
*   **Files Added**:
    *   `backend/agent/generator.py`: *Conceptually handles step pre-processing.*
    *   `backend/agent/executor.py`: The core engine that runs `page.goto()`, `page.click()`, and `page.fill()`.

### Milestone 4: Week 7–8 (Reporting & UI Finalization)
**Goal**: Polish the user experience and generate tangible results.

*   **Execution Detail**:
    *   **Reporting**: Integrated `reportlab` to draw PDF reports and standard `json` libraries to save execution data.
    *   **DOM Mapping**: Added `dom_mapper.py` to intelligently find elements when standard selectors fail (adaptive execution).
    *   **Frontend**: Built a vibrant Streamlit interface to input commands, view real-time logs, and download reports.
*   **Files Added**:
    *   `backend/agent/reporter.py`: Generates `test_report.pdf` and `test_report.json`.
    *   `backend/utils/dom_mapper.py`: Helper functions to locate DOM elements reliably.
    *   `frontend/app.py`: The Streamlit dashboard with Cyberpunk/Neon styling.
    *   `frontend/ui.css`: Custom CSS for the frontend application.

## 6. Technology Stack
**Programming Language**: Python 3.x
**Frameworks / Tools**:
- **LangGraph**: Workflow orchestration.
- **Playwright (Python)**: Browser automation engine.
- **Flask**: Backend API server.
- **Streamlit**: Interactive frontend UI.
- **ReportLab**: PDF report generation.

## 7. Additional Features & Enhancements
Beyond the core milestones, the following advanced features have been implemented to enhance usability and reliability:

- **Cyberpunk / Neon UI Theme**: A modern, vibrant frontend interface with glassmorphism effects, neon glows, and high-contrast styling for better visual feedback.
- **Real-Time Execution Logs**: The frontend displays live, detailed logs from the backend agent (e.g., "Executing GOTO", "Found search trigger"), providing transparency into the agent's decision-making process.
- **Smart Element Detection**: The agent uses adaptive strategies (fallback selectors, intelligent waits) to handle dynamic web elements that might not load immediately or have standard IDs.
- **Robust Auto-Retry Mechanism**: Test steps automatically retry up to 3 times upon failure to handle network flakiness or slow-loading resources.
- **Dynamic Report Generation**:
    - **Live JSON Reports**: Structured data summaries available immediately after test execution.
    - **PDF Export**: Professional-grade PDF reports with step-by-step pass/fail status and styling.

