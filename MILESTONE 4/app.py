

from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import modules
from generators.test_generator import TestGenerator
from executors.test_executor import TestExecutor
from parsers.instruction_parser import InstructionParser
from reporters.html_reporter import HTMLReporter
from reporters.json_reporter import JSONReporter
from langchain_openai import ChatOpenAI

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Initialize components
try:
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    parser = InstructionParser(llm)
    generator = TestGenerator(llm)
    executor = TestExecutor()
    html_reporter = HTMLReporter()
    json_reporter = JSONReporter()
    
    print("✓ Successfully imported agent modules")
    print("✓ Agent graph initialized")
    AGENT_READY = True
except Exception as e:
    print(f"✗ Error initializing agent: {e}")
    AGENT_READY = False

# Print startup banner
print("""
    ╔══════════════════════════════════════════════╗
    ║   E2E Testing Agent API Server               ║
    ║   Running on http://localhost:5000         ║
    ╚══════════════════════════════════════════════╝
    Available endpoints:
    - GET  /                 - Home page
    - GET  /health           - Health check
    - POST /api/test         - Run complete E2E test  ⭐
    - POST /api/parse        - Parse instructions only
    - GET  /api/reports      - List all reports
    - GET  /api/statistics   - Get test statistics
    - GET  /dashboard        - Dashboard UI
    - GET  /test-gui         - Test creation GUI
    - GET  /history          - Test history
    🌐 Open test_gui.html in your browser to test!
    """)


# ============================================================================
# WEB ROUTES
# ============================================================================

@app.route('/')
def home():
    """Home page - redirect to dashboard"""
    return render_template('dashboard.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')


@app.route('/test-gui')
def test_gui():
    """Enhanced test creation GUI"""
    return render_template('enhanced_gui.html')


@app.route('/history')
def history():
    """Test history page"""
    try:
        tests = json_reporter.get_recent_tests(100)
        return render_template('test_history.html', tests=tests)
    except Exception as e:
        return render_template('test_history.html', tests=[], error=str(e))


@app.route('/report/<test_id>')
def view_report(test_id):
    """View individual test report"""
    try:
        result = json_reporter.get_test_by_id(test_id)
        if result:
            return render_template('test_results.html', result=result, test_id=test_id)
        else:
            return "Report not found", 404
    except Exception as e:
        return f"Error loading report: {str(e)}", 500


@app.route('/screenshots/<filename>')
def serve_screenshot(filename):
    """Serve screenshot files"""
    screenshots_dir = Path("./outputs/screenshots")
    return send_from_directory(screenshots_dir, filename)


# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy" if AGENT_READY else "degraded",
        "agent_ready": AGENT_READY,
        "version": "1.0.0 (Milestone 4)"
    })


@app.route('/api/test', methods=['POST'])
def run_test():
    """Run complete E2E test"""
    if not AGENT_READY:
        return jsonify({
            "success": False,
            "error": "Agent not initialized. Check OpenAI API key."
        }), 500
    
    try:
        data = request.get_json()
        instruction = data.get('instruction', '')
        target_url = data.get('target_url', '')
        
        if not instruction or not target_url:
            return jsonify({
                "success": False,
                "error": "Missing instruction or target_url"
            }), 400
        
        # Parse instructions
        steps = parser.parse(instruction)
        
        # Generate test code
        test_code = generator.generate(steps=steps, target_url=target_url)
        
        # Execute test
        result = executor.execute(script=test_code, target_url=target_url)
        
        # Generate reports
        json_report_path = json_reporter.save_enhanced_report(result)
        html_report_path = html_reporter.generate_from_test_result(result)
        
        return jsonify({
            "success": result['success'],
            "test_id": result['test_id'],
            "message": result['message'],
            "execution_time": result['execution_time'],
            "screenshots": result['screenshots'],
            "errors": result['errors'],
            "json_report": json_report_path,
            "html_report": html_report_path
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/parse', methods=['POST'])
def parse_instructions():
    """Parse test instructions without executing"""
    if not AGENT_READY:
        return jsonify({
            "success": False,
            "error": "Agent not initialized"
        }), 500
    
    try:
        data = request.get_json()
        instruction = data.get('instruction', '')
        
        if not instruction:
            return jsonify({
                "success": False,
                "error": "Missing instruction"
            }), 400
        
        steps = parser.parse(instruction)
        
        return jsonify({
            "success": True,
            "steps": [{"action": s.action, "description": s.description} for s in steps]
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/reports')
def list_reports():
    """List all test reports"""
    try:
        limit = request.args.get('limit', 10, type=int)
        reports = json_reporter.get_recent_tests(limit)
        
        return jsonify({
            "success": True,
            "reports": reports,
            "total": len(json_reporter.history)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/statistics')
def get_statistics():
    """Get test statistics"""
    try:
        stats = json_reporter.get_test_statistics()
        
        return jsonify({
            "success": True,
            "statistics": stats
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/statistics/trend')
def get_trend():
    """Get success rate trend"""
    try:
        days = request.args.get('days', 7, type=int)
        trend = json_reporter.get_success_rate_trend(days)
        
        return jsonify({
            "success": True,
            "trend": trend
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear test history"""
    try:
        json_reporter.clear_log()
        
        return jsonify({
            "success": True,
            "message": "History cleared successfully"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/updates')
def check_updates():
    """Check for real-time updates (polling endpoint)"""
    # Placeholder for real-time updates
    return jsonify({
        "success": True,
        "has_updates": False,
        "updates": []
    })


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Create necessary directories
    Path("./outputs/screenshots").mkdir(parents=True, exist_ok=True)
    Path("./outputs/reports").mkdir(parents=True, exist_ok=True)
    Path("./outputs/html_reports").mkdir(parents=True, exist_ok=True)
    
    # Run Flask app
    port = int(os.getenv('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )