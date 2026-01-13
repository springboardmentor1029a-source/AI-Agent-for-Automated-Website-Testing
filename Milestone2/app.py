
from flask import Flask, request, jsonify
from agent import handle_input

app = Flask(__name__, static_folder="static")

# Serve UI
@app.route("/", methods=["GET"])
def home():
    return app.send_static_file("index.html")

# API endpoint for agent
@app.route("/api/agent", methods=["POST"])
def agent_api():
    data = request.get_json()
    user_input = data.get("input", "")
    response = handle_input(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)