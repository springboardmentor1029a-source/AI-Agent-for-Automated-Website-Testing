AI Agent to Test Websites Automatically Using Natural Language


This project eliminates the need for QA engineers to write complex test scripts. Simply describe what you want to test in plain English, and the AI agent automatically converts your instructions into executable Playwright tests, runs them, and generates comprehensive reports.


Features
•⁠  ⁠Natural Language Processing: Write test cases in plain English
•⁠  ⁠Automatic Script Generation: Converts instructions to Playwright Python code
•⁠  ⁠Headless Execution: Fast test runs in headless browsers
•⁠  ⁠Dynamic DOM Adaptation: Handles web structure changes automatically
•⁠  ⁠Comprehensive Reporting: Detailed test reports with pass/fail assertions
•⁠  ⁠Error Handling: Robust error detection and logging
•⁠  ⁠Real-time Monitoring: Captures runtime logs and screenshots on failure


System Architecture


The system uses LangGraph for orchestration and Playwright for browser automation, following a pipeline architecture:



User Input (Natural Language Test Case)

           ↓
Instruction Parser Module ( Interprets natural language, Maps to browser actions)

           ↓
Code Generation Module( Generates Playwright scripts and  Creates assertions)

           ↓
Execution Module (Playwright) (  Runs tests headlessly and Monitors DOM changes)

           ↓
Assertion & Reporting Module ( Validates results and Generates test reports)

           ↓
    Test Report (Success/Failure)


Core Workflow


1.⁠ ⁠Instruction Interpretation Phase
•⁠  ⁠Accepts user-defined natural language test cases
•⁠  ⁠Parses input and identifies actionable test steps
•⁠  ⁠Maps instructions to browser actions (click, type, navigate, verify)


2.⁠ ⁠Code Generation Phase
•⁠  ⁠Converts interpreted steps into executable Playwright scripts
•⁠  ⁠Dynamically generates assertions to validate expected outcomes
•⁠  ⁠Creates error handling and logging logic


3.⁠ ⁠Execution Phase
•⁠  ⁠Runs Playwright tests in a headless browser environment
•⁠  ⁠Monitors DOM and adapts dynamically to web structure changes
•⁠  ⁠Captures screenshots and logs during execution


4.⁠ ⁠Reporting Phase
•⁠  ⁠Summarises results including passed/failed assertions
•⁠  ⁠Generates human-readable test reports for review
•⁠  ⁠Provides actionable insights and error details

Technology Stack


Core Technologies


•⁠  ⁠Programming Language: Python 3.x
•⁠  ⁠Orchestration: LangGraph (workflow management)
•⁠  ⁠Browser Automation: Playwright (Python version)
•⁠  ⁠Backend: Flask (for static test pages and API)
•⁠  ⁠Frontend: Stream lit or Gradio (user interface)
•⁠  ⁠NLP Toolkit: LangChain Community Toolkit (PlaywrightBrowserToolkit


Development Tools
•⁠  ⁠VS Code / PyCharm
•⁠  ⁠Git for version control
•⁠  ⁠Virtual environment (venv)


