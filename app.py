from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from ai_agent import AIWebsiteTester

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Initialize AI agent
try:
    ai_tester = AIWebsiteTester()
    print("✅ AI Agent initialized successfully with LangGraph + OpenAI + Playwright")
except Exception as e:
    print(f"❌ Error initializing AI Agent: {e}")
    ai_tester = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/run-test', methods=['POST'])
def run_test():
    try:
        if not ai_tester:
            return jsonify({
                'error': 'AI Agent not initialized. Please check OpenAI API key and dependencies.'
            }), 500
        
        data = request.json
        website_url = data.get('websiteUrl', '').strip()
        test_instruction = data.get('testInstruction', '').strip()
        browser = data.get('browser', 'chrome')

        # Input validation
        if not website_url:
            return jsonify({
                'error': 'Website URL is required',
                'field': 'websiteUrl'
            }), 400
        
        if not test_instruction:
            return jsonify({
                'error': 'Test instruction is required',
                'field': 'testInstruction'
            }), 400
        
        # Validate URL format
        if not website_url.startswith(('http://', 'https://')):
            website_url = 'https://' + website_url
        
        # Validate instruction length
        if len(test_instruction) < 5:
            return jsonify({
                'error': 'Test instruction must be at least 5 characters',
                'field': 'testInstruction'
            }), 400
        
        if len(test_instruction) > 500:
            return jsonify({
                'error': 'Test instruction must be less than 500 characters',
                'field': 'testInstruction'
            }), 400

        # Run the test using AI agent (LangGraph workflow)
        result = ai_tester.run_test(website_url, test_instruction, browser)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'details': str(e.__traceback__) if hasattr(e, '__traceback__') else None
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/screenshots/<filename>', methods=['GET'])
def get_screenshot(filename):
    """Serve screenshot files"""
    screenshots_dir = Path("screenshots")
    screenshot_path = screenshots_dir / filename
    if screenshot_path.exists() and screenshot_path.is_file():
        return send_from_directory(str(screenshots_dir), filename)
    return jsonify({'error': 'Screenshot not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

