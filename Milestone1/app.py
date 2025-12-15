from flask import Flask, render_template, request, jsonify
from langgraph_agent import run_agent_sync
from browser_tester import test_website

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["query"]
    return jsonify({"response": run_agent_sync(user_input)})

@app.route("/test-site", methods=["POST"])
def test_site():
    url = request.form["url"]
    return jsonify(test_website(url))

if __name__ == "__main__":
    app.run(debug=True)
