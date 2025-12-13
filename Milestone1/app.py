# app.py
from flask import Flask, send_from_directory, request, jsonify
import agent  # our agent module (next)

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/agent', methods=['POST'])
def call_agent():
    data = request.get_json() or {}
    user_input = data.get('input', '')
    # call our baseline agent (sync)
    response = agent.handle_input(user_input)
    return jsonify({"input": user_input, "response": response})

if __name__ == "__main__":
    # For development only. Use `flask run` or a production server for production.
    app.run(host='0.0.0.0', port=5000, debug=True)

