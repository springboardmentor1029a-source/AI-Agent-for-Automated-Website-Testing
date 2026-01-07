# AI-Agent-for-Automated-Website-Testing

An AI-powered web testing agent designed to automate and validate website interactions.
The project uses a Flask-based backend, Playwright for browser automation, and a
LangGraph-based agent workflow to process and respond to testing instructions.

---

## Overview

This project provides a foundation for building intelligent website testing systems.
It exposes a web interface and API that allow users to send testing instructions
to an agent, which can interact with web pages and return structured responses.

The current implementation focuses on establishing a stable architecture that can
be extended with advanced reasoning, LLM integration, and automated test execution.

---

## Key Features

- Flask web server for serving test pages and APIs
- Interactive HTML test interface
- Browser automation using Playwright
- Baseline LangGraph agent workflow
- REST API for agent interaction
- Health check endpoint for service monitoring

---

## Tech Stack

- Python
- Flask
- Playwright
- LangGraph / LangChain

---

## Quick Start

```bash
# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium

# Run the application
python app.py



#Project Structure
.
├── app.py              # Flask application entry point
├── agent.py            # LangGraph agent logic
├── run.py              # Optional runner script
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
├── static/             # Static assets
├── logs/               # Application logs
├── .env.example        # Environment variable template
└── README.md           # Project documentation

#Open your browser and navigate to:

http://localhost:5000