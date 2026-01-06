"""Execute tests with Playwright and capture results"""
import os
import tempfile
import subprocess
import json
import sys
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, expect, TimeoutError as PlaywrightTimeoutError
import traceback

class TestExecutor:
    def __init__(self, output_dir: str = "./outputs"):
        self.output_dir = Path(output_dir)
        self.screenshots_dir = self.output_dir / "screenshots"
        self.reports_dir = self.output_dir / "reports"
        self.test_scripts_dir = self.output_dir / "test_scripts"
        
        # Create all necessary directories
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.test_scripts_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_test_id = None
        self.execution_logs = []
    
    def execute(self, script: str, target_url: str) -> Dict[str, Any]:
        """Execute Playwright test script and return results"""
        
        # Generate unique test ID
        self.current_test_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        result = {
            "success": False,
            "test_id": self.current_test_id,
            "message": "",
            "execution_time": 0,
            "script_path": "",
            "screenshots": [],
            "errors": [],
            "logs": [],
            "target_url": target_url,
            "timestamp": datetime.now().isoformat()
        }
        
        start_time = datetime.now()
        
        try:
            # Save script to file
            script_path = self._save_script(script)
            result["script_path"] = str(script_path)
            
            # Execute script with Playwright
            execution_result = self._execute_with_playwright(script, target_url)
            
            # Update result with execution details
            result.update(execution_result)
            result["success"] = execution_result.get("success", False)
            
        except Exception as e:
            result["success"] = False
            result["message"] = f"Execution failed: {str(e)}"
            result["errors"].append({
                "type": type(e).__name__,
                "message": str(e),
                "traceback": traceback.format_exc()
            })
            self._log(f"ERROR: {str(e)}")
        
        finally:
            end_time = datetime.now()
            result["execution_time"] = (end_time - start_time).total_seconds()
            result["logs"] = self.execution_logs.copy()
            
            # Save execution report
            report_path = self._save_report(result)
            result["report_path"] = str(report_path)
            
            # Clear logs for next execution
            self.execution_logs.clear()
        
        return result
    
    def _execute_with_playwright(self, script: str, target_url: str) -> Dict[str, Any]:
        """Execute test using Playwright browser automation"""
        
        result = {
            "success": False,
            "message": "",
            "screenshots": [],
            "errors": [],
            "console_logs": []
        }
        
        self._log("Initializing Playwright...")
        
        try:
            with sync_playwright() as playwright:
                # Launch browser
                self._log("Launching Chromium browser...")
                browser = playwright.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )
                
                # Create context with realistic viewport
                context = browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
                
                # Create page
                page = context.new_page()
                
                # Set up console log capture
                page.on("console", lambda msg: result["console_logs"].append({
                    "type": msg.type,
                    "text": msg.text
                }))
                
                # Set up error capture
                page.on("pageerror", lambda exc: result["errors"].append({
                    "type": "PageError",
                    "message": str(exc)
                }))
                
                try:
                    self._log(f"Navigating to {target_url}...")
                    
                    # Execute the test script
                    exec_globals = {
                        "page": page,
                        "expect": expect,
                        "playwright": playwright,
                        "browser": browser,
                        "context": context,
                        "sync_playwright": sync_playwright,
                        "TimeoutError": PlaywrightTimeoutError
                    }
                    
                    # Execute the generated test code
                    exec(script, exec_globals)
                    
                    # Take success screenshot
                    screenshot_path = self._capture_screenshot(page, "success")
                    result["screenshots"].append(str(screenshot_path))
                    
                    result["success"] = True
                    result["message"] = "Test executed successfully"
                    self._log("✓ Test completed successfully")
                    
                except PlaywrightTimeoutError as e:
                    result["success"] = False
                    result["message"] = f"Timeout error: {str(e)}"
                    result["errors"].append({
                        "type": "TimeoutError",
                        "message": str(e),
                        "traceback": traceback.format_exc()
                    })
                    
                    # Capture error screenshot
                    screenshot_path = self._capture_screenshot(page, "timeout_error")
                    result["screenshots"].append(str(screenshot_path))
                    self._log(f"✗ Timeout error: {str(e)}")
                    
                except AssertionError as e:
                    result["success"] = False
                    result["message"] = f"Assertion failed: {str(e)}"
                    result["errors"].append({
                        "type": "AssertionError",
                        "message": str(e),
                        "traceback": traceback.format_exc()
                    })
                    
                    # Capture error screenshot
                    screenshot_path = self._capture_screenshot(page, "assertion_error")
                    result["screenshots"].append(str(screenshot_path))
                    self._log(f"✗ Assertion failed: {str(e)}")
                    
                except Exception as e:
                    result["success"] = False
                    result["message"] = f"Test execution error: {str(e)}"
                    result["errors"].append({
                        "type": type(e).__name__,
                        "message": str(e),
                        "traceback": traceback.format_exc()
                    })
                    
                    # Capture error screenshot
                    screenshot_path = self._capture_screenshot(page, "execution_error")
                    result["screenshots"].append(str(screenshot_path))
                    self._log(f"✗ Execution error: {str(e)}")
                
                finally:
                    # Cleanup
                    self._log("Closing browser...")
                    context.close()
                    browser.close()
        
        except Exception as e:
            result["success"] = False
            result["message"] = f"Playwright initialization error: {str(e)}"
            result["errors"].append({
                "type": "PlaywrightError",
                "message": str(e),
                "traceback": traceback.format_exc()
            })
            self._log(f"✗ Playwright error: {str(e)}")
        
        return result
    
    def _execute_with_subprocess(self, script_path: Path) -> Dict[str, Any]:
        """Alternative: Execute test script as subprocess using pytest"""
        
        result = {
            "success": False,
            "message": "",
            "screenshots": [],
            "errors": [],
            "stdout": "",
            "stderr": ""
        }
        
        try:
            self._log(f"Executing script via subprocess: {script_path}")
            
            # Run pytest on the script
            process = subprocess.run(
                [sys.executable, "-m", "pytest", str(script_path), "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            result["stdout"] = process.stdout
            result["stderr"] = process.stderr
            result["success"] = process.returncode == 0
            
            if result["success"]:
                result["message"] = "Test passed"
                self._log("✓ Test passed")
            else:
                result["message"] = "Test failed"
                result["errors"].append({
                    "type": "TestFailure",
                    "message": process.stderr
                })
                self._log(f"✗ Test failed: {process.stderr}")
            
            # Collect screenshots from directory
            result["screenshots"] = self._collect_screenshots()
            
        except subprocess.TimeoutExpired:
            result["success"] = False
            result["message"] = "Test execution timeout"
            result["errors"].append({
                "type": "TimeoutError",
                "message": "Test execution exceeded 60 seconds"
            })
            self._log("✗ Test execution timeout")
            
        except Exception as e:
            result["success"] = False
            result["message"] = f"Subprocess execution error: {str(e)}"
            result["errors"].append({
                "type": type(e).__name__,
                "message": str(e)
            })
            self._log(f"✗ Subprocess error: {str(e)}")
        
        return result
    
    def _save_script(self, script: str) -> Path:
        """Save test script to file"""
        filename = f"test_{self.current_test_id}.py"
        script_path = self.test_scripts_dir / filename
        
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script)
        
        self._log(f"Saved test script to {script_path}")
        return script_path
    
    def _capture_screenshot(self, page, name: str) -> Path:
        """Capture and save screenshot"""
        try:
            filename = f"{name}_{self.current_test_id}.png"
            screenshot_path = self.screenshots_dir / filename
            
            page.screenshot(path=str(screenshot_path), full_page=True)
            self._log(f"Screenshot saved: {screenshot_path}")
            
            return screenshot_path
        except Exception as e:
            self._log(f"Failed to capture screenshot: {str(e)}")
            return None
    
    def _collect_screenshots(self) -> List[str]:
        """Collect all screenshots from the screenshots directory for current test"""
        screenshots = []
        
        for file in self.screenshots_dir.glob(f"*{self.current_test_id}*.png"):
            screenshots.append(str(file))
        
        return screenshots
    
    def _save_report(self, result: Dict[str, Any]) -> Path:
        """Save execution report as JSON"""
        filename = f"report_{self.current_test_id}.json"
        report_path = self.reports_dir / filename
        
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, default=str)
        
        self._log(f"Report saved to {report_path}")
        return report_path
    
    def _log(self, message: str):
        """Add message to execution logs"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] {message}"
        self.execution_logs.append(log_entry)
        print(log_entry)  # Also print to console
    
    def get_report(self, test_id: str) -> Dict[str, Any]:
        """Retrieve execution report by test ID"""
        report_path = self.reports_dir / f"report_{test_id}.json"
        
        if report_path.exists():
            with open(report_path, "r", encoding="utf-8") as f:
                return json.load(f)
        
        return None
    
    def list_reports(self) -> List[Dict[str, Any]]:
        """List all execution reports"""
        reports = []
        
        for report_file in sorted(self.reports_dir.glob("report_*.json"), reverse=True):
            try:
                with open(report_file, "r", encoding="utf-8") as f:
                    report = json.load(f)
                    reports.append({
                        "test_id": report.get("test_id"),
                        "success": report.get("success"),
                        "timestamp": report.get("timestamp"),
                        "execution_time": report.get("execution_time"),
                        "message": report.get("message")
                    })
            except Exception as e:
                print(f"Error reading report {report_file}: {e}")
        
        return reports
    
    def cleanup_old_files(self, days: int = 7):
        """Clean up old test files and screenshots"""
        import time
        
        cutoff_time = time.time() - (days * 86400)
        
        for directory in [self.screenshots_dir, self.reports_dir, self.test_scripts_dir]:
            for file in directory.glob("*"):
                if file.stat().st_mtime < cutoff_time:
                    file.unlink()
                    self._log(f"Deleted old file: {file}")