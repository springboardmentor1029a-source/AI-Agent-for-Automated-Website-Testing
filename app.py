from flask import Flask, render_template, request, jsonify
import os
import json
import asyncio
from dotenv import load_dotenv

from src.parser.instruction_parser import InstructionParser
from src.generator.code_generator import PlaywrightCodeGenerator
from src.executor.code_executor import CodeExecutor
from src.reporter.report_generator import ReportGenerator

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Initialize components
api_key = os.getenv("OPENAI_API_KEY")
parser = InstructionParser(api_key)
generator = PlaywrightCodeGenerator()
executor = CodeExecutor()
reporter = ReportGenerator()

@app.route("/")
def index():
    """Home page"""
    return render_template("index.html")

@app.route("/api/parse-instruction", methods=["POST"])
def parse_instruction():
    """Parse natural language instruction"""
    try:
        data = request.json
        instruction = data.get("instruction")
        url = data.get("url")
        
        if not instruction or not url:
            return jsonify({"error": "Missing instruction or URL"}), 400
        
        # Parse instruction
        parsed = parser.parse_instruction(instruction, url)
        
        return jsonify({
            "status": "success",
            "parsed_instruction": parsed.model_dump()
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/generate-code", methods=["POST"])
def generate_code():
    """Generate Playwright code from parsed instruction"""
    try:
        data = request.json
        parsed_data = data.get("parsed_instruction")
        
        if not parsed_data:
            return jsonify({"error": "Missing parsed instruction"}), 400
        
        # Reconstruct ParsedInstruction object
        from src.parser.instruction_parser import ParsedInstruction
        parsed_instruction = ParsedInstruction(**parsed_data)
        
        # Generate code
        code = generator.generate_code(parsed_instruction)
        
        return jsonify({
            "status": "success",
            "code": code
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/execute-test", methods=["POST"])
def execute_test():
    """Execute generated test code"""
    try:
        data = request.json
        code = data.get("code")
        test_name = data.get("test_name", "test")
        
        if not code:
            return jsonify({"error": "Missing code"}), 400
        
        # Execute code (async)
        result = asyncio.run(executor.execute_code(code, test_name))
        
        return jsonify({
            "status": "success",
            "result": result
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/generate-report", methods=["POST"])
def generate_report():
    """Generate HTML report from results"""
    try:
        data = request.json
        results = data.get("results", [])
        
        if not results:
            return jsonify({"error": "No results to report"}), 400
        
        # Generate reports
        html_path = reporter.generate_html_report(results)
        json_path = reporter.generate_json_report(results)
        
        return jsonify({
            "status": "success",
            "html_report": html_path,
            "json_report": json_path
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/test-flow", methods=["POST"])
def complete_test_flow():
    """Execute complete flow: parse → generate → execute → report"""
    try:
        data = request.json
        instruction = data.get("instruction")
        url = data.get("url")
        
        if not instruction or not url:
            return jsonify({"error": "Missing instruction or URL"}), 400
        
        # Step 1: Parse
        print(f"[1/4] Parsing instruction: {instruction}")
        parsed = parser.parse_instruction(instruction, url)
        
        # Step 2: Generate
        print(f"[2/4] Generating code for test: {parsed.test_name}")
        code = generator.generate_code(parsed)
        
        # Step 3: Execute
        print(f"[3/4] Executing test...")
        result = asyncio.run(executor.execute_code(code, parsed.test_name))
        
        # Step 4: Report
        print(f"[4/4] Generating report...")
        html_path = reporter.generate_html_report([result])
        json_path = reporter.generate_json_report([result])
        
        return jsonify({
            "status": "success",
            "test_name": parsed.test_name,
            "execution_result": result,
            "html_report": html_path,
            "json_report": json_path
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
