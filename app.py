"""Flask server for serving static HTML test page and handling agent requests."""
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from agent import get_agent

# Load environment variables
load_dotenv()

app = Flask(__name__)


@app.route('/')
def index():
    """Serve the home page."""
    return render_template('index.html')


@app.route('/test')
def test_page():
    """Serve the test console page."""
    return render_template('test.html')


@app.route('/docs')
def docs():
    """Serve the documentation page."""
    return render_template('docs.html')


@app.route('/about')
def about():
    """Serve the about page."""
    return render_template('about.html')


@app.route('/api/agent', methods=['POST'])
def agent_endpoint():
    """
    API endpoint for LangGraph agent to handle user inputs.
    This is a baseline implementation for Milestone 1.
    """
    try:
        data = request.get_json()
        user_input = data.get('input', '')
        
        if not user_input:
            return jsonify({
                'error': 'No input provided',
                'status': 'error'
            }), 400
        
        # Use the baseline LangGraph agent
        agent = get_agent()
        result = agent.process(user_input)
        
        response = {
            'status': result['status'],
            'message': result['message'],
            'input': result['input']
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Web Test Agent - Milestone 1'
    }), 200


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"Starting Flask server on port {port}")
    print(f"Visit http://localhost:{port} to see the test page")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

