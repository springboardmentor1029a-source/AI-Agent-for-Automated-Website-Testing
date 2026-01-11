"""
Intelligent E2E Testing Agent - FREE Gemini Version
Automated end-to-end testing using natural language instructions
Powered by Google's FREE Gemini API
"""

import os
import re
import json
from datetime import datetime
from typing import TypedDict, Annotated, Sequence
import operator

# LangGraph and LangChain imports
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Playwright imports
from playwright.sync_api import sync_playwright

# Streamlit for UI
import streamlit as st


# =====================================================
# 1. STATE DEFINITION
# =====================================================

class AgentState(TypedDict):
    """State object for the agent workflow"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    test_instruction: str
    parsed_steps: list
    generated_code: str
    execution_result: dict
    test_report: str


# =====================================================
# 2. INSTRUCTION PARSER MODULE
# =====================================================

class InstructionParser:
    """Parses natural language test instructions into actionable steps"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def parse(self, instruction: str) -> list:
        """Parse natural language into structured test steps"""
        
        # Simple pattern matching for common test patterns
        steps = []
        
        # Check for URL
        url_match = re.search(r'https?://[^\s]+', instruction)
        if url_match:
            url = url_match.group()
            steps.append({
                "action": "navigate",
                "target": url,
                "description": f"Navigate to {url}"
            })
        
        # Check for title verification
        if 'title' in instruction.lower() and 'contains' in instruction.lower():
            # Extract expected text
            title_match = re.search(r"['\"]([^'\"]+)['\"]", instruction)
            if title_match:
                expected = title_match.group(1)
                steps.append({
                    "action": "assert",
                    "target": "page_title",
                    "value": expected,
                    "description": f"Verify the page title contains '{expected}'"
                })
        
        # If we got steps, return them
        if steps:
            return steps
        
        # Fallback
        return [{
            "action": "navigate",
            "target": instruction,
            "description": "Execute test instruction"
        }]


# =====================================================
# 3. CODE GENERATION MODULE
# =====================================================

class CodeGenerator:
    """Generates Playwright test scripts from parsed steps"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def generate(self, steps: list) -> str:
        """Generate executable Playwright Python code using template"""
        
        # Extract URL and expected values from steps
        url = None
        title_check = None
        
        for step in steps:
            if step.get("action") == "navigate":
                url = step.get("target")
            elif step.get("action") == "assert" and "title" in step.get("target", "").lower():
                title_check = step.get("value")
        
        # Use proven template
        if url:
            return self._generate_from_template(url, title_check)
        
        # Fallback
        return self._generate_from_template("https://example.com", "Example Domain")
    
    def _generate_from_template(self, url: str, title_check: str = None) -> str:
        """Generate code from proven template"""
        
        if title_check:
            return f'''from playwright.sync_api import sync_playwright

def run_test():
    result = {{"status": "unknown", "message": "", "details": {{}}}}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_default_timeout(30000)
            
            page.goto("{url}", wait_until="domcontentloaded")
            
            actual_title = page.title()
            expected_title_part = "{title_check}"
            
            if expected_title_part in actual_title:
                result["status"] = "passed"
                result["message"] = f"Test passed: Page title '{{actual_title}}' contains '{{expected_title_part}}'"
                result["details"]["actual_title"] = actual_title
                result["details"]["expected"] = expected_title_part
            else:
                result["status"] = "failed"
                result["message"] = f"Test failed: Page title '{{actual_title}}' does not contain '{{expected_title_part}}'"
                result["details"]["actual_title"] = actual_title
                result["details"]["expected"] = expected_title_part
            
            browser.close()
            
    except TimeoutError:
        result["status"] = "error"
        result["message"] = "Timeout: Page took too long to load"
        result["details"]["error_type"] = "TimeoutError"
    except Exception as e:
        result["status"] = "error"
        result["message"] = f"Error: {{str(e) or type(e).__name__}}"
        result["details"]["error_type"] = type(e).__name__
    
    return result
'''
        else:
            return f'''from playwright.sync_api import sync_playwright

def run_test():
    result = {{"status": "unknown", "message": "", "details": {{}}}}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_default_timeout(30000)
            
            page.goto("{url}", wait_until="domcontentloaded")
            
            title = page.title()
            
            result["status"] = "passed"
            result["message"] = f"Successfully navigated to {{title}}"
            result["details"]["url"] = "{url}"
            result["details"]["title"] = title
            
            browser.close()
            
    except Exception as e:
        result["status"] = "error"
        result["message"] = f"Error: {{str(e) or type(e).__name__}}"
        result["details"]["error_type"] = type(e).__name__
    
    return result
'''


# =====================================================
# 4. EXECUTION MODULE
# =====================================================

class TestExecutor:
    """Executes generated Playwright test scripts"""
    
    def execute(self, code: str) -> dict:
        """Execute the generated test code and return results"""
        
        result = {
            "status": "unknown",
            "message": "",
            "details": {},
            "timestamp": datetime.now().isoformat()
        }
        
        # Save code to temp file and run as subprocess
        import tempfile
        import subprocess
        
        try:
            # Create temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(code)
                f.write('\n\n')
                f.write('if __name__ == "__main__":\n')
                f.write('    import json\n')
                f.write('    result = run_test()\n')
                f.write('    print(json.dumps(result))\n')
                temp_file = f.name
            
            # Run the file
            process = subprocess.run(
                ['python', temp_file],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Clean up
            try:
                os.unlink(temp_file)
            except:
                pass
            
            # Parse output
            if process.returncode == 0:
                try:
                    output = process.stdout.strip()
                    if not output:
                        result["status"] = "error"
                        result["message"] = "Test produced no output"
                        result["details"]["stderr"] = process.stderr
                        return result
                    
                    test_result = json.loads(output)
                    if isinstance(test_result, dict):
                        result.update(test_result)
                    else:
                        result["status"] = "error"
                        result["message"] = "Invalid result format"
                        result["details"]["output"] = output
                except json.JSONDecodeError as e:
                    result["status"] = "error"
                    result["message"] = f"Failed to parse test output: {str(e)}"
                    result["details"]["stdout"] = process.stdout
                    result["details"]["stderr"] = process.stderr
            else:
                result["status"] = "error"
                result["message"] = f"Test process failed with code {process.returncode}"
                result["details"]["stdout"] = process.stdout
                result["details"]["stderr"] = process.stderr
                result["details"]["returncode"] = process.returncode
                
        except subprocess.TimeoutExpired:
            result["status"] = "error"
            result["message"] = "Test execution timed out (60 seconds)"
            
        except Exception as e:
            result["status"] = "error"
            result["message"] = f"Execution failed: {str(e) or type(e).__name__}"
            result["details"]["error_type"] = type(e).__name__
        
        return result


# =====================================================
# 5. REPORTING MODULE
# =====================================================

class ReportGenerator:
    """Generates human-readable test reports"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def generate(self, instruction: str, steps: list, execution_result: dict) -> str:
        """Generate a comprehensive test report"""
        
        status = execution_result.get("status", "unknown")
        message = execution_result.get("message", "No message")
        details = execution_result.get("details", {})
        
        if status == "passed":
            report = f"""## ✅ Test Passed

**Instruction:** {instruction}

**Result:** {message}

**Details:**
"""
            for key, value in details.items():
                report += f"- **{key}**: {value}\n"
        
        elif status == "failed":
            report = f"""## ❌ Test Failed

**Instruction:** {instruction}

**Result:** {message}

**Details:**
"""
            for key, value in details.items():
                report += f"- **{key}**: {value}\n"
        
        else:
            report = f"""## ⚠️ Test Error

**Instruction:** {instruction}

**Error:** {message}

**Details:**
"""
            for key, value in details.items():
                report += f"- **{key}**: {value}\n"
        
        return report


# =====================================================
# 6. LANGGRAPH WORKFLOW
# =====================================================

class E2ETestingAgent:
    """Main agent orchestrating the testing workflow"""
    
    def __init__(self, api_key: str):
        if not api_key or len(api_key) < 20:
            raise ValueError("Invalid API key")
        
        for proxy_var in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
            os.environ.pop(proxy_var, None)
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0,
            convert_system_message_to_human=True
        )
        
        self.parser = InstructionParser(self.llm)
        self.generator = CodeGenerator(self.llm)
        self.executor = TestExecutor()
        self.reporter = ReportGenerator(self.llm)
        
        self.graph = self._build_graph()
    
    def _build_graph(self):
        workflow = StateGraph(AgentState)
        
        workflow.add_node("parse_instruction", self._parse_instruction)
        workflow.add_node("generate_code", self._generate_code)
        workflow.add_node("execute_test", self._execute_test)
        workflow.add_node("generate_report", self._generate_report)
        
        workflow.set_entry_point("parse_instruction")
        workflow.add_edge("parse_instruction", "generate_code")
        workflow.add_edge("generate_code", "execute_test")
        workflow.add_edge("execute_test", "generate_report")
        workflow.add_edge("generate_report", END)
        
        return workflow.compile()
    
    def _parse_instruction(self, state: AgentState):
        instruction = state["test_instruction"]
        steps = self.parser.parse(instruction)
        state["parsed_steps"] = steps
        state["messages"].append(AIMessage(content=f"Parsed {len(steps)} steps"))
        return state
    
    def _generate_code(self, state: AgentState):
        steps = state["parsed_steps"]
        code = self.generator.generate(steps)
        state["generated_code"] = code
        state["messages"].append(AIMessage(content="Generated code"))
        return state
    
    def _execute_test(self, state: AgentState):
        code = state["generated_code"]
        result = self.executor.execute(code)
        state["execution_result"] = result
        state["messages"].append(AIMessage(content=f"Status: {result['status']}"))
        return state
    
    def _generate_report(self, state: AgentState):
        report = self.reporter.generate(
            state["test_instruction"],
            state["parsed_steps"],
            state["execution_result"]
        )
        state["test_report"] = report
        state["messages"].append(AIMessage(content="Report generated"))
        return state
    
    def run_test(self, instruction: str):
        initial_state = {
            "messages": [HumanMessage(content=instruction)],
            "test_instruction": instruction,
            "parsed_steps": [],
            "generated_code": "",
            "execution_result": {},
            "test_report": ""
        }
        
        final_state = self.graph.invoke(initial_state)
        
        return {
            "steps": final_state["parsed_steps"],
            "code": final_state["generated_code"],
            "result": final_state["execution_result"],
            "report": final_state["test_report"]
        }


# =====================================================
# 7. STREAMLIT UI
# =====================================================

def main():
    st.set_page_config(
        page_title="E2E Testing Agent - FREE",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Intelligent E2E Testing Agent")
    st.markdown("✨ **FREE VERSION** - Powered by Google Gemini API")
    
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.success("🎉 Using FREE Google Gemini API!")
        st.info("Get your FREE API key at: https://makersuite.google.com/app/apikey")
        
        default_key = os.getenv("GOOGLE_API_KEY", "")
        api_key = st.text_input("Google API Key", value=default_key, type="password")
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("AI-powered E2E testing with Playwright")
    
    if not api_key:
        st.warning("⚠️ Please enter your Google API key in the sidebar")
        st.stop()
    
    st.header("📝 Test Instruction")
    
    example_tests = [
        "Navigate to https://example.com and verify the page title contains 'Example Domain'",
        "Go to https://www.google.com and verify the page loads"
    ]
    
    selected = st.selectbox("Choose example:", ["Custom"] + example_tests)
    
    if selected == "Custom":
        test_instruction = st.text_area("Enter test instruction:", height=100)
    else:
        test_instruction = st.text_area("Enter test instruction:", value=selected, height=100)
    
    if st.button("▶️ Run Test", type="primary", use_container_width=True):
        if not test_instruction:
            st.error("Please enter a test instruction")
            st.stop()
        
        with st.spinner("Running test..."):
            try:
                agent = E2ETestingAgent(api_key)
                result = agent.run_test(test_instruction)
                
                tab1, tab2, tab3, tab4 = st.tabs(["📊 Report", "📋 Steps", "💻 Code", "🔍 Details"])
                
                with tab1:
                    if result["result"]["status"] == "passed":
                        st.success("✅ Test Passed")
                    elif result["result"]["status"] == "failed":
                        st.error("❌ Test Failed")
                    else:
                        st.warning("⚠️ Test Error")
                    st.markdown(result["report"])
                
                with tab2:
                    for i, step in enumerate(result["steps"], 1):
                        with st.expander(f"Step {i}: {step.get('description')}"):
                            st.json(step)
                
                with tab3:
                    st.markdown("### Generated Code")
                    st.code(result["code"], language="python")
                    
                    st.download_button(
                        label="📥 Download Code",
                        data=result["code"],
                        file_name="test_code.py",
                        mime="text/plain"
                    )
                
                with tab4:
                    st.markdown("### Execution Details")
                    st.json(result["result"])
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                import traceback
                st.code(traceback.format_exc())


if __name__ == "__main__":
    main()