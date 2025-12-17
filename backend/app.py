from flask import Flask, request, jsonify
from agent.graph import run_agent
from flask import send_file
import os

app = Flask(__name__)
@app.route("/")
def home():
    return {"status": "Backend running"}

@app.route("/run", methods=["POST"])
def run_test():
    user_input = request.json.get("instruction")
    report = run_agent(user_input)
    return jsonify(report)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.route("/download/pdf")
def download_pdf():
    pdf_path = os.path.join(BASE_DIR, "reports", "test_report.pdf")
    return send_file(pdf_path, as_attachment=True)
@app.route("/download/json")
def download_json():
    json_path = os.path.join(BASE_DIR, "reports", "test_report.json")
    return send_file(json_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)


