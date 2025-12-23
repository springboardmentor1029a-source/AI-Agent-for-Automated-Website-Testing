import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

class ReportGenerator:
    """Generates test reports in HTML and JSON formats"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_json_report(self, test_results: List[Dict[str, Any]], filename: str = None) -> str:
        """Generate JSON report"""
        if not filename:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report_path = self.output_dir / filename
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_tests": len(test_results),
            "passed": sum(1 for r in test_results if r.get("execution_status") == "success"),
            "failed": sum(1 for r in test_results if r.get("execution_status") == "failed"),
            "results": test_results
        }
        
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        
        return str(report_path)
    
    def generate_html_report(self, test_results: List[Dict[str, Any]], filename: str = None) -> str:
        """Generate HTML report"""
        if not filename:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        report_path = self.output_dir / filename
        
        total = len(test_results)
        passed = sum(1 for r in test_results if r.get("execution_status") == "success")
        failed = total - passed
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Web Testing Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
        }}
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        .header p {{
            opacity: 0.9;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            padding: 30px;
            background: #f9f9f9;
            border-bottom: 1px solid #e0e0e0;
        }}
        .summary-card {{
            text-align: center;
            padding: 20px;
            background: white;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        .summary-card.passed {{
            border-left-color: #4caf50;
        }}
        .summary-card.failed {{
            border-left-color: #f44336;
        }}
        .summary-card .number {{
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
        }}
        .summary-card.passed .number {{
            color: #4caf50;
        }}
        .summary-card.failed .number {{
            color: #f44336;
        }}
        .summary-card .label {{
            color: #666;
            margin-top: 10px;
            font-size: 14px;
        }}
        .results {{
            padding: 30px;
        }}
        .test-result {{
            margin-bottom: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
        }}
        .test-result.passed {{
            border-left: 4px solid #4caf50;
            background: #f1f8f4;
        }}
        .test-result.failed {{
            border-left: 4px solid #f44336;
            background: #fef1f0;
        }}
        .test-result-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .test-result-header h3 {{
            font-size: 18px;
        }}
        .status-badge {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }}
        .status-badge.passed {{
            background: #4caf50;
            color: white;
        }}
        .status-badge.failed {{
            background: #f44336;
            color: white;
        }}
        .test-details {{
            font-size: 14px;
            color: #666;
            margin-top: 10px;
        }}
        .step {{
            margin-left: 20px;
            padding: 10px;
            background: white;
            margin-top: 10px;
            border-radius: 4px;
            border-left: 2px solid #ddd;
        }}
        .error {{
            color: #d32f2f;
            font-family: monospace;
            margin-top: 10px;
            padding: 10px;
            background: #ffebee;
            border-radius: 4px;
        }}
        .footer {{
            background: #f9f9f9;
            padding: 20px;
            text-align: center;
            color: #999;
            font-size: 12px;
            border-top: 1px solid #e0e0e0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 AI Web Testing Report</h1>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <div class="number">{total}</div>
                <div class="label">Total Tests</div>
            </div>
            <div class="summary-card passed">
                <div class="number">{passed}</div>
                <div class="label">Passed</div>
            </div>
            <div class="summary-card failed">
                <div class="number">{failed}</div>
                <div class="label">Failed</div>
            </div>
        </div>
        
        <div class="results">
            <h2 style="margin-bottom: 20px;">Test Results</h2>
"""
        
        for result in test_results:
            status = result.get("execution_status", "unknown")
            status_class = "passed" if status == "success" else "failed"
            test_name = result.get("test_name", "Unknown Test")
            
            html += f"""
            <div class="test-result {status_class}">
                <div class="test-result-header">
                    <h3>{test_name}</h3>
                    <span class="status-badge {status_class}">{status.upper()}</span>
                </div>
                <div class="test-details">
                    <p><strong>Timestamp:</strong> {result.get('timestamp', 'N/A')}</p>
"""
            
            # Add steps if available
            if "steps" in result:
                html += "<p><strong>Steps:</strong></p>"
                for step in result["steps"]:
                    step_status = step.get("status", "unknown")
                    html += f'<div class="step">'
                    html += f'<strong>{step.get("description", step.get("step", "Step"))}</strong> - {step_status}'
                    if "error" in step:
                        html += f'<div class="error">Error: {step["error"]}</div>'
                    html += '</div>'
            
            # Add error if present
            if "error" in result:
                html += f'<div class="error">Error: {result["error"]}</div>'
            
            html += """
                </div>
            </div>
"""
        
        html += """
        </div>
        
        <div class="footer">
            <p>Generated by AI Web Testing Agent</p>
        </div>
    </div>
</body>
</html>
"""
        
        with open(report_path, "w") as f:
            f.write(html)
        
        return str(report_path)

# Test the generator
if __name__ == "__main__":
    sample_results = [
        {
            "test_name": "Login Test",
            "execution_status": "success",
            "timestamp": datetime.now().isoformat(),
            "steps": [
                {"step": 1, "description": "Navigate to login", "status": "passed"},
                {"step": 2, "description": "Fill email", "status": "passed"},
            ]
        },
        {
            "test_name": "Form Test",
            "execution_status": "failed",
            "timestamp": datetime.now().isoformat(),
            "error": "Form element not found",
            "steps": [
                {"step": 1, "description": "Navigate to form", "status": "passed"},
                {"step": 2, "description": "Fill form", "status": "failed", "error": "Element not found"},
            ]
        }
    ]
    
    generator = ReportGenerator()
    json_report = generator.generate_json_report(sample_results)
    html_report = generator.generate_html_report(sample_results)
    
    print(f"JSON Report: {json_report}")
    print(f"HTML Report: {html_report}")
