from flask import Flask, render_template, request, jsonify
from agent import run_agent

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_test():
    data = request.json
    url = data.get("url")
    instruction = data.get("instruction")

    result = run_agent(url, instruction)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
