# Milestone 1 — Foundation Setup
**Author:** Kunal Bhamare

## Goal
Establish the project baseline: environment, dependencies, Flask test server, and a baseline LangGraph agent.

## Quick verification checklist
1. Create & activate venv, then `pip install -r requirements.txt`.
2. Run Flask: `python app.py` and visit `http://localhost:5000`.
3. Health check: `http://localhost:5000/health` → returns JSON.
4. Test agent: `curl -X POST http://localhost:5000/api/agent -H "Content-Type: application/json" -d '{"input":"Test"}'`.

If all pass → Milestone 1 is complete.

## Files referenced
- `app.py` — Flask server
- `agent.py` — baseline agent
- `requirements.txt` — dependencies
- `templates/test_page.html` — test UI

