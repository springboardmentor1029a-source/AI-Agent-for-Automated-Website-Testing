from flask import Flask, request, jsonify, render_template
from agent.code_generator import generate_test_plan
from agent.executor import execute_test

app = Flask(__name__, static_folder="static")

@app.route("/")
def home():
    # Uses templates/index.html
    return render_template("index.html")

@app.route("/run_agent", methods=["POST"])
def run_agent_api():
    data = request.json
    user_input = data.get("user_input", "")

    test_plan = generate_test_plan(user_input)
    result = execute_test(test_plan)

    return jsonify({
        "user_input": user_input,
        "execution": result
    })

if __name__ == "__main__":
    app.run(debug=True)
