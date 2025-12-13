from flask import Flask, send_from_directory, request, jsonify
from agent.base_agent import create_agent
import time
import traceback

# serve static files at root so /styles.css and /script.js work
app = Flask(__name__, static_folder="static", static_url_path="")

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/about")
def about_page():
    return send_from_directory("static", "about.html")

@app.route("/contact")
def contact_page():
    return send_from_directory("static", "contact.html")

@app.route("/test")
def test_page():
    return send_from_directory("static", "test.html")

@app.route("/api/run_test", methods=["POST"])
def api_run_test():
    """
    Expect JSON:
    {
      "instruction": "open amazon and search redmi",
      "target": "/test" or "https://example.com" (optional),
      "mode": "simulate" or "execute" (optional)
    }

    Returns:
    {
      "status": "ok",
      "instruction": "...",
      "target": "<resolved target OR echoed target>",
      "mode": "execute",
      "duration_sec": 0.123,
      "result": { ... agent output ... }
    }
    """
    try:
        payload = request.get_json(force=True)
    except Exception as e:
        return jsonify({"status": "error", "error": "Invalid JSON", "detail": str(e)}), 400

    instruction = (payload.get("instruction") or "").strip()
    target = (payload.get("target") or "/test").strip() or "/test"
    mode = payload.get("mode", "simulate")
    if mode not in ("simulate", "execute"):
        mode = "simulate"

    if not instruction:
        return jsonify({"status": "error", "error": "Missing instruction"}), 400

    # Build state for agent including the UI-provided mode
    state = {"instruction": instruction, "target": target, "mode": mode}

    agent = create_agent()

    start = time.time()
    try:
        result = agent.invoke(state)
    except Exception as e:
        # include traceback to help debug during development
        tb = traceback.format_exc()
        return jsonify({"status": "error", "error": str(e), "trace": tb}), 500
    duration = time.time() - start

    # Prefer the agent-resolved target if present in result (more accurate)
    resolved_target = None
    if isinstance(result, dict):
        # agent may include a top-level 'target' or within steps use a 'goto' target
        resolved_target = result.get("target")
        if not resolved_target:
            # try to find first goto step target
            steps = result.get("steps") or result.get("step_results") or []
            if isinstance(steps, list):
                for s in steps:
                    if isinstance(s, dict) and s.get("action") == "goto" and s.get("target"):
                        resolved_target = s.get("target")
                        break

    final_target = resolved_target if resolved_target else target

    response = {
        "status": "ok",
        "instruction": instruction,
        "target": final_target,
        "mode": mode,
        "duration_sec": round(duration, 3),
        "result": result
    }
    return jsonify(response)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
