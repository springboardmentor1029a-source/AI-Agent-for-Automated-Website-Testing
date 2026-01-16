from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
from datetime import datetime
from threading import Thread
import uuid

from Parser.grokparser import app as Langapp
from executer.playwriter import execute_test

app = Flask(__name__)


# In-memory job store

JOBS = {}


# Logs setup

LOG_DIR = os.path.join(app.root_path, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "logs.json")
PLAYWRIGHT_RESULT_FILE = os.path.join(LOG_DIR, "playlogs.json")


# Log helpers

def save_log(entry: str):
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "entry": entry
    })

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)


def save_playwright_result(result: dict):
    try:
        with open(PLAYWRIGHT_RESULT_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "result": result
    })

    with open(PLAYWRIGHT_RESULT_FILE, "w") as f:
        json.dump(data, f, indent=2)



# Pages

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/main")
def main_page():
    return render_template("main.html")


@app.route("/logs")
def logs_page():
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except:
        logs = []

    return render_template("logs.html", logs=logs)


@app.route("/logs/logs.json")
def serve_logs_json():
    return send_from_directory(LOG_DIR, "logs.json")


@app.route("/logs/playlogs.json")
def serve_playwright_logs():
    return send_from_directory(LOG_DIR, "playlogs.json")



# Test execution (async)

@app.route("/run", methods=["POST"])
def run():
    # Support BOTH form submit and fetch(JSON)
    if request.is_json:
        data = request.get_json(silent=True) or {}
        user_input = data.get("instruction")
    else:
        user_input = request.form.get("instruction")

    if not user_input:
        return jsonify({"error": "instruction missing"}), 400

    job_id = str(uuid.uuid4())
    JOBS[job_id] = {"status": "RUNNING"}

    def background_job():
        try:
            # LangGraph parsing
            result_state = Langapp.invoke({"input": user_input})
            output_text = result_state.get("result")

            save_log(output_text)

            instruction_json = json.loads(output_text)

            # Playwright execution
            playwright_result = execute_test(instruction_json)

            # ui logging for debugging
            if playwright_result.get("overall_status") == "BLOCKED":
                save_log(f"[BLOCKED] Reason: {playwright_result.get('reason')}")

            save_playwright_result(playwright_result)

            JOBS[job_id] = {
                "status": "DONE",
                "output": output_text,
                "playwright": playwright_result
            }

        except Exception as e:
            JOBS[job_id] = {
                "status": "ERROR",
                "error": str(e)
            }

    Thread(target=background_job, daemon=True).start()

    return jsonify({"job_id": job_id})


@app.route("/test-status/<job_id>")
def test_status(job_id):
    return jsonify(JOBS.get(job_id, {"status": "UNKNOWN"}))


# -----------------------------
# App start
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
