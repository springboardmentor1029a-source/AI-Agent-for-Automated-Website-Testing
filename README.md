# AI Agent to Test Websites Automatically Using Natural Language
## Milestone 1: Project Setup and Agent Initialization
### Objective
The goal of Milestone 1 is to build the foundational setup for an AI-powered website testing system. This milestone focuses on environment setup, basic web application creation, and initializing an AI agent that can understand natural language test instructions.

---
## Milestone 1 Requirements
### 1. Setting Up the Python Environment
A Python virtual environment is created to isolate project dependencies. This ensures consistent execution across different systems and avoids version conflicts.


---
### 2. Installing Required Dependencies
The following libraries are installed:
- **Flask**: Used to create a lightweight web server to host a test website.
- **LangGraph**: Used to define and manage the AI agent workflow.
- **Playwright**: Installed for browser automation (to be used in future milestones).
All dependencies are listed in `requirements.txt` for easy installation.

---
### 3. Defining the Project Structure
The project is organized into separate folders for clarity and scalability:
- `agent/` contains AI agent logic.
- `static/` contains the test HTML website.
- `app.py` serves as the main Flask application.
This modular structure makes future development and maintenance easier.

---
### 4. Initializing a Flask Server with a Static Test Page
A Flask server is created to serve a basic static HTML login page. This page acts as a sample website that the AI agent will interact with and test in later milestones.

---
### 5. Implementing a Baseline LangGraph Agent
A basic LangGraph agent is implemented to process natural language inputs such as test instructions.
At this stage, the agent:
- Accepts user instructions in plain English
- Processes the input
- Returns a confirmation response
This demonstrates that the AI agent can understand and handle natural language commands.

---
## How to Run the Project
```bash
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install
python app.py