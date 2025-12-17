from flask import Flask, render_template, request, jsonify
from agent.workflow import run_agent_test

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/static_testpage")
def static_testpage():
    return app.send_static_file("testpage.html")

@app.route("/run_test", methods=["POST"])
def run_test():
    instruction = request.json.get("instruction")
    report = run_agent_test(instruction)
    return jsonify(report)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
