from flask import Flask,render_template, request, jsonify
from agent_graph import graph

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/run_agent', methods=['POST'])
def run_agent():
    try:
        data = request.get_json(silent=True) or {}
        instruction = data.get('instruction') or "Go to google.com"
        
        print(f"DEBUG: Starting Agent with: {instruction}")

        initial_state = {
            "instruction": instruction,
            "parsed_actions": [],
            "current_step_index": 0,
            "execution_history": [],
            "logs": [],
            "retry_count": 0,
            "page_source": None
        }

        # Invoke the graph
        final_state = graph.invoke(initial_state)

        # Return the actual result to the frontend
        return jsonify({
            "status": "success",
            "report": final_state.get("final_report", "Task sequence finished."),
            "logs": final_state.get("logs", [])
        })
    except Exception as e:
        print(f"SERVER ERROR: {e}")
        return jsonify({"status": "error", "message":str(e)}),500

if __name__ == '__main__':
    app.run(port=5000,debug=True)