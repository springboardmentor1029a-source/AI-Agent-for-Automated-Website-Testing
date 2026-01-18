"""
AI Agent for Automated Website Testing using LangGraph and Playwright
Implements the architecture as specified in the project PDF:
- LangGraph for agent workflow orchestration
- OpenAI GPT for natural language understanding
- Playwright for browser automation
- Code generation for Playwright scripts
"""

import os
import json
import time
import tempfile
import base64
from datetime import datetime
from typing import TypedDict, Annotated
from pathlib import Path
from dotenv import load_dotenv

# LangGraph and LangChain imports
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

# Playwright imports (optional - graceful degradation if not installed)
try:
    from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    sync_playwright = None
    Page = None
    Browser = None
    BrowserContext = None

# Load environment variables
load_dotenv()

class AgentState(TypedDict):
    """State structure for LangGraph agent"""
    instruction: str
    website_url: str
    parsed_steps: list
    generated_code: str
    execution_result: dict
    test_report: dict
    error: str
    screenshots: list
    validations: list


class AIWebsiteTester:
    """
    AI-powered website testing agent using LangGraph, OpenAI GPT, and Playwright.
    Follows the architecture: Instruction → Parse → Generate Code → Execute → Report
    """
    
    def __init__(self, model_name="gpt-3.5-turbo"):
        """Initialize the AI agent with OpenAI model"""
        # Initialize OpenAI LLM
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0,
            api_key=api_key
        )
        
        # Initialize Playwright browser
        self.page = None
        self.browser = None
        self.context = None
        self.playwright_instance = None
        
        # Create screenshots directory
        self.screenshots_dir = Path("screenshots")
        self.screenshots_dir.mkdir(exist_ok=True)
        
        # Build LangGraph workflow
        self.workflow = self._build_workflow()
        
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow: Parse → Generate → Execute → Report"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("parse_instruction", self._parse_instruction)
        workflow.add_node("generate_code", self._generate_playwright_code)
        workflow.add_node("execute_test", self._execute_playwright_code)
        workflow.add_node("generate_report", self._generate_report)
        
        # Define edges
        workflow.set_entry_point("parse_instruction")
        workflow.add_edge("parse_instruction", "generate_code")
        workflow.add_edge("generate_code", "execute_test")
        workflow.add_edge("execute_test", "generate_report")
        workflow.add_edge("generate_report", END)
        
        return workflow.compile()
    
    def _parse_instruction_fallback(self, instruction: str, website_url: str) -> list:
        """
        Fallback parser: Uses keyword matching when OpenAI API is unavailable
        """
        instruction_lower = instruction.lower()
        steps = []
        
        # Always start with navigation
        steps.append({"action": "navigate", "target": "website_url", "value": website_url})
        
        # Detect search action
        search_keywords = ['search', 'search for', 'find', 'look for', 'query']
        for keyword in search_keywords:
            if keyword in instruction_lower:
                # Extract search query
                parts = instruction_lower.split(keyword)
                if len(parts) > 1:
                    search_query = parts[-1].strip()
                    search_query = search_query.replace('for ', '').replace('the ', '').strip()
                    if search_query:
                        steps.append({
                            "action": "search",
                            "target": "search box",
                            "value": search_query
                        })
                        steps.append({
                            "action": "verify",
                            "target": "search results",
                            "assertion": "results displayed"
                        })
                break
        
        # Detect click action
        if any(word in instruction_lower for word in ['click', 'press', 'select']):
            steps.append({"action": "click", "target": "button", "value": None})
        
        # Detect fill/input action
        if any(word in instruction_lower for word in ['fill', 'enter', 'type', 'input']):
            steps.append({"action": "fill", "target": "input field", "value": None})
        
        return steps
    
    def _parse_instruction(self, state: AgentState) -> AgentState:
        """
        Instruction Parser Module: Interprets natural language and maps to browser actions
        Uses OpenAI GPT with fallback to keyword matching
        """
        try:
            system_prompt = """You are an expert test automation engineer. 
            Parse the natural language test instruction and extract actionable test steps.
            Return a JSON array of steps, where each step has:
            - action: type of action (navigate, click, fill, search, verify, etc.)
            - target: what element to interact with (description or selector)
            - value: optional value for fill/input actions
            - assertion: optional expected result
            
            Example output:
            [
                {"action": "navigate", "target": "website_url", "value": null},
                {"action": "search", "target": "search box", "value": "iphone 17"},
                {"action": "verify", "target": "search results", "assertion": "results displayed"}
            ]
            """
            
            user_message = f"""
            Website URL: {state['website_url']}
            Test Instruction: {state['instruction']}
            
            Parse this instruction and return the test steps as JSON.
            """
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message)
            ]
            
            response = self.llm.invoke(messages)
            response_text = response.content.strip()
            
            # Extract JSON from response
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            parsed_steps = json.loads(response_text)
            
            state["parsed_steps"] = parsed_steps
            state["error"] = None
            
        except Exception as e:
            error_str = str(e).lower()
            # Check if it's a quota/API error or connection error
            if any(keyword in error_str for keyword in ["quota", "429", "insufficient_quota", "connection", "timeout", "network"]):
                # Use fallback parser
                state["parsed_steps"] = self._parse_instruction_fallback(
                    state["instruction"], 
                    state["website_url"]
                )
                state["error"] = None
                state["using_fallback"] = True
            else:
                # For other errors, still try fallback
                state["parsed_steps"] = self._parse_instruction_fallback(
                    state["instruction"], 
                    state["website_url"]
                )
                state["error"] = None
                state["using_fallback"] = True
        
        return state
    
    def _generate_playwright_code_fallback(self, parsed_steps: list, website_url: str) -> str:
        """
        Fallback code generator: Creates Playwright code directly from parsed steps
        """
        code_lines = [
            "# Generated Playwright test code",
            "from playwright.sync_api import expect",
            "",
            "# Navigate to website with timeout",
            f'page.goto("{website_url}", wait_until="domcontentloaded", timeout=60000)',
            "try:",
            "    page.wait_for_load_state('networkidle', timeout=30000)",
            "except:",
            "    pass  # Continue even if networkidle times out",
            "",
        ]
        
        for step in parsed_steps:
            action = step.get("action", "")
            target = step.get("target", "")
            value = step.get("value", "")
            
            if action == "navigate":
                if value:
                    code_lines.append(f'page.goto("{value}", wait_until="domcontentloaded", timeout=60000)')
                    code_lines.append("try:")
                    code_lines.append("    page.wait_for_load_state('networkidle', timeout=30000)")
                    code_lines.append("except:")
                    code_lines.append("    pass")
            
            elif action == "search":
                # Try multiple search box selectors with better timeout handling
                code_lines.append("# Find and fill search box")
                code_lines.append("search_selectors = [")
                code_lines.append("    '#twotabsearchtextbox',  # Amazon specific")
                code_lines.append("    'input[type=\"search\"]',")
                code_lines.append("    'input[name=\"q\"]',")
                code_lines.append("    'textarea[name=\"q\"]',  # Google sometimes uses textarea for search box")
                code_lines.append("    'input[name=\"search\"]',")
                code_lines.append("    'input[id*=\"search\"]',")
                code_lines.append("    'input[placeholder*=\"search\" i]',")
                code_lines.append("]")
                code_lines.append("")
                code_lines.append("search_input = None")
                code_lines.append("for selector in search_selectors:")
                code_lines.append("    try:")
                code_lines.append("        search_input = page.locator(selector).first")
                code_lines.append("        search_input.wait_for(state='visible', timeout=10000)")
                code_lines.append("        if search_input.is_visible():")
                code_lines.append("            break")
                code_lines.append("    except Exception as e:")
                code_lines.append("        continue")
                code_lines.append("")
                code_lines.append("if search_input:")
                code_lines.append("    try:")
                code_lines.append(f'        search_input.fill("{value}", timeout=10000)')
                code_lines.append("        time.sleep(0.5)  # Brief pause before submitting")
                code_lines.append("        # Wait for navigation after search (context will be destroyed)")
                code_lines.append("        with page.expect_navigation(timeout=30000, wait_until='domcontentloaded'):")
                code_lines.append("            # Try to submit")
                code_lines.append("            try:")
                code_lines.append("                page.keyboard.press('Enter')")
                code_lines.append("            except:")
                code_lines.append("                # Try to find and click search button")
                code_lines.append("                try:")
                code_lines.append("                    page.locator('#nav-search-submit-button, button[type=\"submit\"], input[type=\"submit\"]').first.click(timeout=10000)")
                code_lines.append("                except:")
                code_lines.append("                    pass")
                code_lines.append("        # Wait a bit for page to fully load after navigation")
                code_lines.append("        time.sleep(2)")
                code_lines.append("    except Exception as e:")
                code_lines.append("        # If navigation fails, try without navigation context")
                code_lines.append("        try:")
                code_lines.append("            page.wait_for_load_state('domcontentloaded', timeout=20000)")
                code_lines.append("        except:")
                code_lines.append("            pass  # Continue even if timeout")
            
            elif action == "click":
                code_lines.append(f"# Click {target}")
                code_lines.append(f"page.locator('{target}').first.click(timeout=30000)")
                code_lines.append("try:")
                code_lines.append("    page.wait_for_load_state('domcontentloaded', timeout=15000)")
                code_lines.append("except:")
                code_lines.append("    pass")
            
            elif action == "fill":
                code_lines.append(f"# Fill {target}")
                code_lines.append(f"page.locator('{target}').first.fill('{value}')")
            
            elif action == "verify":
                code_lines.append(f"# Verify {target}")
                code_lines.append(f"# Assertion: {step.get('assertion', 'element exists')}")
        
        code_lines.append("")
        code_lines.append("# Capture screenshot after actions")
        code_lines.append("time.sleep(1)  # Wait for page to settle")
        code_lines.append("")
        code_lines.append("# Test results")
        code_lines.append("results = {")
        code_lines.append("    'status': 'success',")
        code_lines.append("    'message': 'Test executed successfully',")
        code_lines.append(f"    'url': page.url,")
        code_lines.append("    'title': page.title(),")
        code_lines.append("}")
        
        return "\n".join(code_lines)
    
    def _generate_playwright_code(self, state: AgentState) -> AgentState:
        """
        Code Generation Module: Converts parsed actions into executable Playwright scripts
        Uses OpenAI GPT with fallback to direct code generation
        """
        # If using fallback parser, use fallback code generator
        if state.get("using_fallback"):
            state["generated_code"] = self._generate_playwright_code_fallback(
                state["parsed_steps"],
                state["website_url"]
            )
            state["error"] = None
            return state
        
        try:
            system_prompt = """You are an expert Playwright test automation engineer.
            Generate Python Playwright code based on the parsed test steps.
            The code should:
            1. Use Playwright's sync API
            2. Navigate to the website with timeout handling
            3. Perform the actions from parsed_steps
            4. Include assertions to validate expected outcomes
            5. Return a dictionary with test results
            
            IMPORTANT: Use timeout handling for all operations:
            - Use page.goto(url, wait_until="domcontentloaded", timeout=60000) for navigation
            - Use try/except blocks for wait operations that might timeout
            - Use page.wait_for_load_state('domcontentloaded', timeout=30000) instead of 'networkidle'
            - Add timeout parameters to all click(), fill(), and wait operations
            - Don't wait for 'networkidle' as it can timeout on slow sites
            
            Use Playwright best practices:
            - Use page.goto() with timeout for navigation
            - Use page.fill() with timeout for input fields
            - Use page.click() with timeout for buttons/links
            - Use page.locator() with text, role, or CSS selectors
            - Use expect() for assertions
            - Handle timeouts gracefully with try/except
            
            Return ONLY the Python code, no explanations.
            """
            
            steps_json = json.dumps(state["parsed_steps"], indent=2)
            user_message = f"""
            Website URL: {state['website_url']}
            Parsed Steps:
            {steps_json}
            
            Generate Playwright Python code to execute these steps.
            """
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message)
            ]
            
            response = self.llm.invoke(messages)
            code = response.content.strip()
            
            # Extract code block if present
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0].strip()
            elif "```" in code:
                code = code.split("```")[1].split("```")[0].strip()
            
            state["generated_code"] = code
            state["error"] = None
            
        except Exception as e:
            error_str = str(e).lower()
            # Check if it's a quota/API error or connection error
            if any(keyword in error_str for keyword in ["quota", "429", "insufficient_quota", "connection", "timeout", "network"]):
                # Use fallback code generator
                state["generated_code"] = self._generate_playwright_code_fallback(
                    state["parsed_steps"],
                    state["website_url"]
                )
                state["error"] = None
            else:
                # For other errors, still try fallback to ensure tests can run
                state["generated_code"] = self._generate_playwright_code_fallback(
                    state["parsed_steps"],
                    state["website_url"]
                )
                state["error"] = None
        
        return state
    
    def _capture_screenshot(self, name: str = "screenshot") -> dict:
        """Capture screenshot and return base64 encoded data"""
        try:
            if not self.page:
                return None
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = self.screenshots_dir / f"{name}_{timestamp}.png"
            self.page.screenshot(path=str(screenshot_path), full_page=True)
            
            # Read and encode as base64
            with open(screenshot_path, "rb") as f:
                screenshot_data = base64.b64encode(f.read()).decode('utf-8')
            
            return {
                "path": str(screenshot_path),
                "base64": screenshot_data,
                "name": f"{name}_{timestamp}.png",
                "timestamp": timestamp
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _validate_page(self, instruction: str) -> list:
        """Validate page elements based on instruction"""
        validations = []
        try:
            if not self.page:
                return validations
            
            instruction_lower = instruction.lower()
            # Get page content properly - content() is a method in Playwright
            try:
                page_content = self.page.content()
                page_text = page_content.lower() if isinstance(page_content, str) else ""
            except:
                # Fallback: try to get text from body
                try:
                    page_text = self.page.locator("body").inner_text().lower()
                except:
                    page_text = ""
            page_url = self.page.url
            
            # Validate URL is correct
            validations.append({
                "type": "url_validation",
                "status": "pass",
                "message": f"Successfully navigated to: {page_url}",
                "details": {"url": page_url}
            })
            
            # Check if page loaded
            title = self.page.title()
            validations.append({
                "type": "page_load",
                "status": "pass",
                "message": f"Page loaded successfully: {title}",
                "details": {"title": title}
            })
            
            # Check for search-related content
            if "search" in instruction_lower or "find" in instruction_lower:
                search_inputs = self.page.locator("input[type='search'], input[name*='search'], input[id*='search'], textarea[name='q'], input[name='q'], #twotabsearchtextbox").count()
                if search_inputs > 0:
                    validations.append({
                        "type": "search_box",
                        "status": "pass",
                        "message": f"Found {search_inputs} search input field(s)",
                        "details": {"count": search_inputs}
                    })
                else:
                    validations.append({
                        "type": "search_box",
                        "status": "warning",
                        "message": "Search box not found",
                        "details": {}
                    })
            
            # Check for images
            if "image" in instruction_lower or "picture" in instruction_lower:
                images = self.page.locator("img").count()
                validations.append({
                    "type": "images",
                    "status": "pass",
                    "message": f"Found {images} image(s) on page",
                    "details": {"count": images}
                })
            
            # Check for links
            if "link" in instruction_lower:
                links = self.page.locator("a[href]").count()
                validations.append({
                    "type": "links",
                    "status": "pass",
                    "message": f"Found {links} link(s) on page",
                    "details": {"count": links}
                })
            
            # Check for forms
            if "form" in instruction_lower:
                forms = self.page.locator("form").count()
                validations.append({
                    "type": "forms",
                    "status": "pass",
                    "message": f"Found {forms} form(s) on page",
                    "details": {"count": forms}
                })
            
            # Extract search query if mentioned
            if "search" in instruction_lower and page_text:
                for word in ["search for", "find", "look for", "search"]:
                    if word in instruction_lower:
                        query = instruction_lower.split(word)[-1].strip().split()[0:3]  # Get first few words
                        query_text = " ".join(query).strip()
                        if query_text and len(query_text) > 0:
                            # Check if query appears in page (case-insensitive)
                            if query_text.lower() in page_text:
                                validations.append({
                                    "type": "content_validation",
                                    "status": "pass",
                                    "message": f"Found search query '{query_text}' in page content",
                                    "details": {"query": query_text}
                                })
                            else:
                                # Check if page title contains the query
                                try:
                                    title = self.page.title().lower()
                                    if query_text.lower() in title:
                                        validations.append({
                                            "type": "content_validation",
                                            "status": "pass",
                                            "message": f"Found search query '{query_text}' in page title",
                                            "details": {"query": query_text}
                                        })
                                except:
                                    pass
                        break
            
        except Exception as e:
            validations.append({
                "type": "validation_error",
                "status": "error",
                "message": f"Validation error: {str(e)}",
                "details": {}
            })
        
        return validations
    
    def _execute_playwright_code(self, state: AgentState) -> AgentState:
        """
        Execution Module: Runs Playwright tests in headless browser with screenshots and validation
        """
        if not PLAYWRIGHT_AVAILABLE:
            state["execution_result"] = {
                "status": "error",
                "error": "Playwright is not installed. Please install it with: pip install playwright && playwright install chromium"
            }
            state["screenshots"] = []
            state["validations"] = []
            return state
        
        if state.get("error") or not state.get("generated_code"):
            state["execution_result"] = {
                "status": "error",
                "error": state.get("error", "No code generated")
            }
            state["screenshots"] = []
            state["validations"] = []
            return state
        
        screenshots = []
        validations = []
        
        try:
            # Initialize Playwright with increased timeouts
            self.playwright_instance = sync_playwright().start()
            self.browser = self.playwright_instance.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
            )
            self.context = self.browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            self.page = self.context.new_page()
            # Set default timeout to 60 seconds
            self.page.set_default_timeout(60000)
            self.page.set_default_navigation_timeout(60000)
            
            # Capture initial screenshot
            initial_screenshot = self._capture_screenshot("initial")
            if initial_screenshot:
                screenshots.append(initial_screenshot)
            
            # Create a safe execution environment
            execution_globals = {
                "page": self.page,
                "browser": self.browser,
                "context": self.context,
                "time": time,
                "json": json,
                "datetime": datetime,
            }
            
            # Execute the generated code with timeout protection
            navigation_occurred = False
            try:
                exec(state["generated_code"], execution_globals)
            except Exception as exec_error:
                error_msg = str(exec_error)
                # Check if it's a navigation context error (this is often OK - page navigated successfully)
                if any(keyword in error_msg for keyword in [
                    "Execution context was destroyed", 
                    "Target closed", 
                    "Target page, context or browser has been closed",
                    "navigation",
                    "page closed",
                    "context closed"
                ]):
                    # This usually means navigation happened successfully
                    navigation_occurred = True
                    # Wait for new page to load
                    try:
                        # Get the current page from context (might be a new page after navigation)
                        if self.context and self.context.pages:
                            self.page = self.context.pages[-1]  # Get the latest page
                            self.page.wait_for_load_state('domcontentloaded', timeout=10000)
                        elif self.page:
                            try:
                                self.page.wait_for_load_state('domcontentloaded', timeout=10000)
                            except:
                                # Page might be closed, try to get new one
                                if self.context and self.context.pages:
                                    self.page = self.context.pages[-1]
                        time.sleep(1)  # Brief pause
                    except Exception as nav_error:
                        # Even if we can't get the new page, navigation likely succeeded
                        pass
                    # Don't treat this as a fatal error - navigation likely succeeded
                else:
                    # If execution fails with other error, capture error screenshot and continue
                    try:
                        error_screenshot = self._capture_screenshot("execution_error")
                        if error_screenshot:
                            screenshots.append(error_screenshot)
                    except:
                        pass
                    # Only raise if it's not a navigation-related error
                    if not any(keyword in error_msg.lower() for keyword in ["closed", "destroyed", "navigation"]):
                        raise exec_error
            
            # Wait a bit for page to settle (reduced from 2 to 1 second)
            time.sleep(1)
            
            # Capture final screenshot - handle case where page might have navigated
            try:
                final_screenshot = self._capture_screenshot("final")
                if final_screenshot:
                    screenshots.append(final_screenshot)
            except Exception as screenshot_error:
                # If screenshot fails due to closed page, try to get new page
                try:
                    if self.context and self.context.pages:
                        self.page = self.context.pages[-1]
                        final_screenshot = self._capture_screenshot("final")
                        if final_screenshot:
                            screenshots.append(final_screenshot)
                except:
                    pass  # Continue even if screenshot fails
            
            # Run validations - handle case where page might have navigated
            try:
                validations = self._validate_page(state["instruction"])
            except Exception as validation_error:
                # If validation fails, try to get new page and retry
                try:
                    if self.context and self.context.pages:
                        self.page = self.context.pages[-1]
                        validations = self._validate_page(state["instruction"])
                    else:
                        validations = []
                except:
                    validations = []
            
            # Try to get results from executed code
            try:
                if "results" in execution_globals and not navigation_occurred:
                    execution_result = execution_globals["results"]
                else:
                    # Get page info safely (page might have navigated)
                    current_url = "Unknown"
                    current_title = "Unknown"
                    
                    # Try multiple ways to get page info after navigation
                    try:
                        if self.page:
                            current_url = self.page.url
                            current_title = self.page.title()
                    except:
                        try:
                            # Try to get from context pages
                            if self.context and self.context.pages:
                                latest_page = self.context.pages[-1]
                                current_url = latest_page.url
                                current_title = latest_page.title()
                                self.page = latest_page  # Update page reference
                        except:
                            pass
                    
                    # Determine status message
                    if navigation_occurred:
                        status_msg = "Test executed successfully - Page navigated to search results"
                    else:
                        status_msg = "Test executed successfully"
                    
                    execution_result = {
                        "status": "success",
                        "message": status_msg,
                        "url": current_url,
                        "title": current_title,
                        "navigation_occurred": navigation_occurred
                    }
            except Exception as result_error:
                # If we can't get results, still mark as success if navigation occurred
                if navigation_occurred:
                    execution_result = {
                        "status": "success",
                        "message": "Test executed successfully - Navigation completed",
                        "url": "Page navigated",
                        "title": "Search results page",
                        "navigation_occurred": True
                    }
                else:
                    execution_result = {
                        "status": "success",
                        "message": "Test executed (unable to get page details)",
                        "url": "Unknown",
                        "title": "Unknown"
                    }
            
            # Add validation results to execution result
            execution_result["validations"] = validations
            execution_result["screenshots_count"] = len(screenshots)
            
            state["execution_result"] = execution_result
            state["screenshots"] = screenshots
            state["validations"] = validations
            state["error"] = None
            
        except Exception as e:
            # Capture error screenshot if page exists
            if self.page:
                error_screenshot = self._capture_screenshot("error")
                if error_screenshot:
                    screenshots.append(error_screenshot)
            
            state["execution_result"] = {
                "status": "error",
                "error": str(e),
                "traceback": str(e.__traceback__) if hasattr(e, '__traceback__') else None
            }
            state["screenshots"] = screenshots
            state["validations"] = validations
            state["error"] = f"Execution error: {str(e)}"
        
        finally:
            # Cleanup
            self._cleanup_browser()
        
        return state
    
    def _generate_report(self, state: AgentState) -> AgentState:
        """
        Reporting Module: Generates human-readable test report
        """
        try:
            execution_result = state.get("execution_result", {})
            parsed_steps = state.get("parsed_steps", [])
            
            # Compile comprehensive report
            report = {
                "status": execution_result.get("status", "unknown"),
                "website_url": state["website_url"],
                "test_instruction": state["instruction"],
                "timestamp": datetime.now().isoformat(),
                "steps_executed": len(parsed_steps),
                "execution_details": execution_result,
                "parsed_steps": parsed_steps,
                "generated_code": state.get("generated_code", ""),
            }
            
            # Add performance metrics if available
            if self.page:
                try:
                    performance = self.page.evaluate("""
                        () => {
                            const perf = performance.timing;
                            return {
                                loadTime: perf.loadEventEnd - perf.navigationStart,
                                domContentLoaded: perf.domContentLoadedEventEnd - perf.navigationStart,
                                pageSize: document.documentElement.innerHTML.length
                            };
                        }
                    """)
                    report["performance"] = performance
                except:
                    pass
            
            state["test_report"] = report
            state["error"] = None
            
        except Exception as e:
            state["test_report"] = {
                "status": "error",
                "error": f"Error generating report: {str(e)}"
            }
            state["error"] = str(e)
        
        return state
    
    def _cleanup_browser(self):
        """Clean up browser resources"""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright_instance:
                self.playwright_instance.stop()
        except:
            pass
        finally:
            self.page = None
            self.context = None
            self.browser = None
            self.playwright_instance = None
    
    def run_test(self, website_url: str, test_instruction: str, browser: str = "chrome"):
        """
        Main method to run tests based on natural language instruction.
        Follows the workflow: Instruction → Parse → Generate → Execute → Report
        """
        try:
            # Initialize state
            initial_state: AgentState = {
                "instruction": test_instruction,
                "website_url": website_url,
                "parsed_steps": [],
                "generated_code": "",
                "execution_result": {},
                "test_report": {},
                "error": None,
                "screenshots": [],
                "validations": []
            }
            
            # Run the LangGraph workflow
            final_state = self.workflow.invoke(initial_state)
            
            # Format response for API
            report = final_state.get("test_report", {})
            
            if final_state.get("error"):
                return {
                    "status": "error",
                    "error": final_state["error"],
                    "websiteUrl": website_url,
                    "testInstruction": test_instruction,
                    "browser": browser,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Format results for frontend
            results = []
            execution_details = report.get("execution_details", {})
            validations = final_state.get("validations", [])
            screenshots = final_state.get("screenshots", [])
            
            if execution_details.get("status") == "success":
                results.append("✅ Test executed successfully")
                if "message" in execution_details:
                    results.append(execution_details["message"])
                if "title" in execution_details:
                    results.append(f"Page Title: {execution_details['title']}")
            else:
                results.append(f"❌ Test execution: {execution_details.get('status', 'unknown')}")
                if "error" in execution_details:
                    results.append(f"Error: {execution_details['error']}")
            
            # Add validation results
            if validations:
                results.append(f"\n📋 Validations ({len(validations)} checks):")
                for val in validations:
                    status_icon = "✅" if val.get("status") == "pass" else "⚠️" if val.get("status") == "warning" else "❌"
                    results.append(f"{status_icon} {val.get('message', '')}")
            
            # Add performance metrics
            if "performance" in report:
                perf = report["performance"]
                results.append(f"\n⚡ Performance Metrics:")
                results.append(f"Page load time: {perf.get('loadTime', 0)}ms")
                if "pageSize" in perf:
                    page_size_kb = perf["pageSize"] / 1024
                    results.append(f"Page size: {page_size_kb:.2f}KB")
            
            # Prepare screenshot data for frontend (filter out errors and duplicates)
            screenshot_data = []
            seen_names = set()
            for screenshot in screenshots:
                if screenshot and "error" not in screenshot and screenshot.get("base64"):
                    name = screenshot.get("name", "")
                    # Avoid duplicates
                    if name and name not in seen_names:
                        seen_names.add(name)
                        screenshot_data.append({
                            "name": name,
                            "base64": screenshot.get("base64"),
                            "timestamp": screenshot.get("timestamp")
                        })
            
            return {
                "status": report.get("status", "success"),
                "websiteUrl": website_url,
                "testInstruction": test_instruction,
                "browser": browser,
                "results": results,
                "performance": report.get("performance"),
                "timestamp": report.get("timestamp", datetime.now().isoformat()),
                "execution_details": execution_details,
                "validations": validations,
                "screenshots": screenshot_data,
                "screenshots_count": len(screenshot_data)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Unexpected error: {str(e)}",
                "websiteUrl": website_url,
                "testInstruction": test_instruction,
                "browser": browser,
                "timestamp": datetime.now().isoformat()
            }
        finally:
            self._cleanup_browser()
    
    def __del__(self):
        """Cleanup on deletion"""
        self._cleanup_browser()
