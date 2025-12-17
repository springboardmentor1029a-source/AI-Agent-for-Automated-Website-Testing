# AI Website Testing Agent — Complete Package 

This is an advanced starter implementation of an AI agent that generates and runs Playwright tests
from natural language instructions, using LangGraph for orchestration and a Streamlit dashboard for UI.

**What's included**
- Flask static test page (for demo)
- Streamlit UI to input test instructions and view results
- LangGraph-based workflow (parser -> generator -> executor -> reporter)
- NLP-oriented parser skeleton (using simple rule-based + spaCy hints)
- Playwright Python script generator (with placeholders for assertions)
- Executor that runs playwright scripts (invocation only — ensure playwright browsers are installed)
- Reporter that outputs JSON + HTML report
- Example testcases and generated script

**Notes**
- You must run `pip install -r requirements.txt` and `playwright install` before running Playwright tests.
- This repo aims to be a comprehensive starting point; adapt modules to your environment.

