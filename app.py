from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, render_template, request, jsonify
from agent_graph import run_agent

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run_agent", methods=["POST"])
def run_agent_api():
    data = request.get_json()
    user_input = data.get("user_input", "")
    result = run_agent(user_input)
    return jsonify(result)

if __name__ == "__main__":
    print("BASE_DIR:", BASE_DIR)
    print("TEMPLATE_DIR:", TEMPLATE_DIR)
    print("Templates found:", os.listdir(TEMPLATE_DIR))
    app.run(debug=True)
@app.route("/login")
def login_page():
    return render_template("login.html")
