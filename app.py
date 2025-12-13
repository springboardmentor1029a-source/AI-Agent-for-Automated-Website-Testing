# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from pathlib import Path

current_dir = Path(__file__).parent.absolute()

if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed")

try:
    from agent.graph import create_agent_graph
    from agent.state import AgentState

    print("✓ Successfully imported agent modules")
except ModuleNotFoundError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

app = Flask(__name__)
CORS(app)

agent_graph = None
try:
    agent_graph = create_agent_graph()
    print("✓ Agent graph initialized")
except Exception as e:
    print(f"✗ Could not initialize agent graph: {e}")


@app.route('/', methods=['GET'])
def home():
    """Home page"""
    return """
    <h1>🧪 E2E Testing Agent API</h1>
    <p>Server is running!</p>
    <h2>Available Endpoints:</h2>
    <ul>
        <li>GET /health - Health check</li>
        <li>POST /api/test - Run complete E2E test</li>
        <li>POST /api/parse - Parse instructions</li>
        <li>GET /api/reports - List reports</li>
    </ul>
    <p><strong>Agent Status:</strong> """ + ("✅ Ready" if agent_graph else "❌ Not Ready") + """</p>
    """


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "E2E Testing Agent API",
        "version": "1.0.0",
        "agent_ready": agent_graph is not None
    })


@app.route('/api/test', methods=['POST'])
def run_test():
    try:
        if agent_graph is None:
            return jsonify({"success": False, "error": "Agent not ready"}), 500

        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        instruction = data.get('instruction')
        target_url = data.get('target_url')

        if not instruction:
            return jsonify({"error": "instruction is required"}), 400
        if not target_url:
            return jsonify({"error": "target_url is required"}), 400

        browser = data.get('browser', 'chromium')
        headless = data.get('headless', True)

        os.environ["BROWSER_TYPE"] = browser
        os.environ["HEADLESS"] = str(headless)

        # Create state as a dictionary (TypedDict cannot be instantiated)
        initial_state = {
            "instruction": instruction,
            "target_url": target_url,
            "messages": [],
            "parsed_steps": [],
            "test_script": "",
            "execution_status": "pending",
            "test_results": {},
            "screenshots": [],
            "report": {},
            "error": None
        }

        print(f"\n{'=' * 60}")
        print(f"🚀 Running test: {instruction}")
        print(f"🌐 Target URL: {target_url}")
        print(f"{'=' * 60}")

        final_state = agent_graph.invoke(initial_state)

        if final_state.get("error"):
            return jsonify({
                "success": False,
                "error": final_state["error"],
                "report": final_state.get("report", {})
            }), 500

        return jsonify({
            "success": True,
            "report": final_state.get("report", {}),
            "screenshots": final_state.get("screenshots", [])
        })

    except Exception as e:
        print(f"❌ Error in /api/test: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/parse', methods=['POST'])
def parse_instruction():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        instruction = data.get('instruction')
        if not instruction:
            return jsonify({"error": "instruction is required"}), 400

        try:
            from parsers.instruction_parser import InstructionParser
            from agent.nodes import get_llm

            parser = InstructionParser(get_llm())
            steps = parser.parse(instruction, data.get('target_url', ''))

            return jsonify({
                "success": True,
                "steps": [
                    {"action": s.action, "target": s.target, "value": s.value, "description": s.description}
                    for s in steps
                ]
            })
        except ImportError as e:
            print(f"⚠️  Custom parser not available: {e}")
            return jsonify({
                "success": True,
                "message": "Using built-in parser",
                "steps": []
            })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/reports', methods=['GET'])
def list_reports():
    try:
        reports_dir = os.getenv("REPORTS_DIR", "./outputs/reports")

        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir, exist_ok=True)
            return jsonify({"success": True, "reports": []})

        reports = [
            {"filename": f, "path": os.path.join(reports_dir, f)}
            for f in os.listdir(reports_dir) if f.endswith('.json')
        ]

        return jsonify({
            "success": True,
            "reports": sorted(reports, key=lambda x: x['filename'], reverse=True)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    try:
        port = int(os.getenv('FLASK_PORT', 5000))
    except (ValueError, TypeError):
        port = 5000

    try:
        debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    except AttributeError:
        debug = True

    print(f"""
    ╔══════════════════════════════════════════════╗
    ║   E2E Testing Agent API Server               ║
    ║   Running on http://localhost:{port}         ║
    ╚══════════════════════════════════════════════╝

    Available endpoints:
    - GET  /                 - Home page
    - GET  /health           - Health check
    - POST /api/test         - Run complete E2E test  ⭐
    - POST /api/parse        - Parse instructions only
    - GET  /api/reports      - List all reports

    🌐 Open test_gui.html in your browser to test!
    """)

    app.run(host='0.0.0.0', port=port, debug=debug)