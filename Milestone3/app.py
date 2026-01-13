from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-test', methods=['POST'])
def run_test():
    data = request.json
    user_input = data.get("instruction", "")

    response = {
        "execution_status": "Test executed successfully",
        "generated_steps": [
            "Open the login page"
        ],
        "parsed_actions": [
            {
                "action": "goto",
                "target": "https://www.google.com"
            }
        ]
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
