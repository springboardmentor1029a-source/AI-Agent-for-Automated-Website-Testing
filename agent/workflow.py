"""
LangGraph Workflow Module
Orchestrates the complete test automation workflow
"""

from typing import Dict, TypedDict, List
from langgraph.graph import StateGraph, END
from .smart_parser import SmartParser
from .code_generator import CodeGenerator
from .executor import TestExecutor
import time

class AgentState(TypedDict):
    """State shared across workflow nodes"""
    instruction: str
    target_url: str
    execution_mode: str
    parsed_actions: List[Dict]
    generated_code: str
    validation_result: Dict
    execution_result: Dict
    final_report: Dict
    error: str

class TestAgentWorkflow:
    """Main workflow orchestrator using LangGraph"""
    
    def __init__(self):
        self.parser = SmartParser()
        self.code_generator = CodeGenerator()
        self.executor = TestExecutor()
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("parse_instruction", self._parse_instruction_node)
        workflow.add_node("generate_code", self._generate_code_node)
        workflow.add_node("validate_code", self._validate_code_node)
        workflow.add_node("execute_test", self._execute_test_node)
        workflow.add_node("generate_report", self._generate_report_node)
        workflow.add_node("handle_error", self._handle_error_node)
        
        # Define edges
        workflow.set_entry_point("parse_instruction")
        workflow.add_edge("parse_instruction", "generate_code")
        workflow.add_edge("generate_code", "validate_code")
        workflow.add_conditional_edges(
            "validate_code",
            self._check_validation,
            {
                "valid": "execute_test",
                "invalid": "handle_error"
            }
        )
        workflow.add_edge("execute_test", "generate_report")
        workflow.add_edge("generate_report", END)
        workflow.add_edge("handle_error", END)
        
        return workflow.compile()
    
    def _parse_instruction_node(self, state: AgentState) -> AgentState:
        """Parse natural language instruction"""
        try:
            print("[*] Parsing instruction...")
            parsed_actions = self.parser.parse(state["instruction"])
            state["parsed_actions"] = parsed_actions
            print(f"[OK] Parsed {len(parsed_actions)} actions")
        except Exception as e:
            state["error"] = f"Parsing error: {str(e)}"
            state["parsed_actions"] = []
        return state
    
    def _generate_code_node(self, state: AgentState) -> AgentState:
        """Generate Playwright code"""
        try:
            print("[*] Generating test code...")
            browser_type = state.get("browser_type", "chromium")
            headless = state.get("headless", True)
            code = self.code_generator.generate(
                state["parsed_actions"],
                state["target_url"],
                browser_type=browser_type,
                headless=headless
            )
            state["generated_code"] = code
            print(f"[OK] Code generated for {browser_type} ({'headless' if headless else 'visible'} mode)")
        except Exception as e:
            state["error"] = f"Code generation error: {str(e)}"
            state["generated_code"] = ""
        return state
    
    def _validate_code_node(self, state: AgentState) -> AgentState:
        """Validate generated code"""
        try:
            print("[*] Validating code...")
            validation = self.executor.validate_script(state["generated_code"])
            state["validation_result"] = validation
            if validation["valid"]:
                print("[OK] Code validation passed")
            else:
                print("[ERROR] Code validation failed")
        except Exception as e:
            state["validation_result"] = {
                "valid": False,
                "errors": [str(e)]
            }
        return state
    
    def _execute_test_node(self, state: AgentState) -> AgentState:
        """Execute the test"""
        try:
            print("[*] Executing test...")
            execution = self.executor.execute(state["generated_code"])
            state["execution_result"] = execution
            
            print(f"[DEBUG] Execution status: {execution.get('status')}")
            
            if execution["status"] == "success":
                results = execution.get("results", {})
                passed = len(results.get("passed", []))
                failed = len(results.get("failed", []))
                print(f"[OK] Test execution completed - {passed} passed, {failed} failed")
            else:
                error_msg = execution.get('error', 'Unknown')
                stdout = execution.get('stdout', '')
                stderr = execution.get('stderr', '')
                print(f"[ERROR] Test execution failed: {error_msg}")
                if stdout:
                    print(f"[ERROR] stdout: {stdout[:500]}")
                if stderr:
                    print(f"[ERROR] stderr: {stderr[:500]}")
        except Exception as e:
            state["execution_result"] = {
                "status": "error",
                "error": str(e)
            }
        return state
    
    def _generate_report_node(self, state: AgentState) -> AgentState:
        """Generate final test report"""
        try:
            print("[*] Generating report...")
            
            execution = state.get("execution_result", {})
            results = execution.get("results", {})
            
            passed_tests = results.get("passed", [])
            failed_tests = results.get("failed", [])
            
            total = len(passed_tests) + len(failed_tests)
            success_rate = (len(passed_tests) / max(total, 1)) * 100 if total > 0 else 0
            
            report = {
                "success": True,
                "instruction": state["instruction"],
                "target_url": state["target_url"],
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_steps": len(state["parsed_actions"]),
                "passed": len(passed_tests),
                "failed": len(failed_tests),
                "success_rate": success_rate,
                "actions": state["parsed_actions"],
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "generated_code": state["generated_code"],
                "execution_status": execution.get("status", "unknown")
            }
            
            state["final_report"] = report
            
            print(f"[OK] Report generated - {len(passed_tests)}/{total} tests passed ({success_rate:.1f}%)")
            
        except Exception as e:
            state["error"] = f"Report generation error: {str(e)}"
            state["final_report"] = {"success": False, "error": str(e)}
        
        return state
    
    def _handle_error_node(self, state: AgentState) -> AgentState:
        """Handle errors in the workflow"""
        validation = state.get("validation_result", {})
        errors = validation.get("errors", [])
        
        state["final_report"] = {
            "success": False,
            "instruction": state["instruction"],
            "target_url": state["target_url"],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "error",
            "error": state.get("error", "Unknown error"),
            "validation_errors": errors,
            "generated_code": state.get("generated_code", ""),
            "total_steps": 0,
            "passed": 0,
            "failed": 0,
            "success_rate": 0
        }
        
        return state
    
    def _check_validation(self, state: AgentState) -> str:
        """Check if validation passed"""
        validation = state.get("validation_result", {})
        return "valid" if validation.get("valid", False) else "invalid"
    
    def run(self, instruction: str, target_url: str, browser_type: str = "chromium", headless: bool = True) -> Dict:
        """
        Run the complete test workflow
        
        Args:
            instruction: Natural language test instruction
            target_url: Target URL to test
            browser_type: Browser to use (chromium, firefox, webkit)
            headless: Whether to run in headless mode
            
        Returns:
            Final test report
        """
        initial_state = {
            "instruction": instruction,
            "target_url": target_url,
            "browser_type": browser_type,
            "headless": headless,
            "parsed_actions": [],
            "generated_code": "",
            "validation_result": {},
            "execution_result": {},
            "final_report": {},
            "error": ""
        }
        
        print("\n" + "="*60)
        print("[*] Yash AI Agent - Starting Test Workflow")
        print("="*60)
        
        final_state = self.workflow.invoke(initial_state)
        
        print("="*60)
        print("[*] Workflow Complete")
        print("="*60 + "\n")
        
        return final_state["final_report"]
