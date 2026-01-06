"""Generate test scripts with assertions and proper structure"""
from typing import List, Dict
from langchain_core.prompts import ChatPromptTemplate
from agent.state import TestStep
import re

class TestGenerator:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Generate Playwright Python test from steps. 

Requirements:
1. Use pytest framework with proper fixtures
2. Include explicit assertions using expect() for validation
3. Add error handling with try-except blocks
4. Capture screenshots on failure
5. Use page.wait_for_selector() for element stability
6. Add page.wait_for_load_state('networkidle') after navigation
7. Include descriptive comments for each step

Structure:
- Import statements at top
- Test function with page fixture
- Proper assertions for verification steps
- Screenshot capture on failures

Return ONLY the complete Python code, no explanations or markdown."""),
            ("user", "Target: {target_url}\nSteps:\n{steps}\n\nGenerate complete test script:")
        ])
    
    def generate(self, steps: List[TestStep], target_url: str = "") -> str:
        """Generate complete Playwright test script with assertions"""
        
        # Format steps with detailed actions
        steps_text = self._format_steps(steps)
        
        # Generate code using LLM
        chain = self.prompt | self.llm
        result = chain.invoke({"target_url": target_url, "steps": steps_text})
        code = result.content
        
        # Extract clean code
        code = self._extract_code(code)
        
        # Ensure required imports
        code = self._ensure_imports(code)
        
        # Add error handling wrapper if missing
        code = self._ensure_error_handling(code)
        
        return code
    
    def _format_steps(self, steps: List[TestStep]) -> str:
        """Format test steps with detailed action descriptions"""
        formatted = []
        for i, step in enumerate(steps, 1):
            action = step.action.upper()
            description = step.description
            
            # Add context for different action types
            if action in ["CLICK", "TAP"]:
                formatted.append(f"{i}. {action}: Click on {description}")
            elif action in ["TYPE", "FILL", "INPUT"]:
                formatted.append(f"{i}. {action}: Enter text into {description}")
            elif action in ["NAVIGATE", "GOTO"]:
                formatted.append(f"{i}. {action}: Navigate to {description}")
            elif action in ["VERIFY", "CHECK", "ASSERT"]:
                formatted.append(f"{i}. {action}: Verify that {description}")
            elif action in ["WAIT"]:
                formatted.append(f"{i}. {action}: Wait for {description}")
            else:
                formatted.append(f"{i}. {action}: {description}")
        
        return "\n".join(formatted)
    
    def _extract_code(self, code: str) -> str:
        """Extract Python code from markdown blocks or raw text"""
        # Remove markdown code blocks
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()
        
        return code.strip()
    
    def _ensure_imports(self, code: str) -> str:
        """Ensure all required imports are present"""
        required_imports = {
            "playwright": "from playwright.sync_api import sync_playwright, expect, Page",
            "pytest": "import pytest",
            "time": "import time",
            "pathlib": "from pathlib import Path",
            "datetime": "from datetime import datetime"
        }
        
        # Check which imports are missing
        missing_imports = []
        for key, import_line in required_imports.items():
            if key not in code.lower():
                missing_imports.append(import_line)
        
        # Add missing imports at the beginning
        if missing_imports:
            imports_block = "\n".join(missing_imports)
            code = f"{imports_block}\n\n{code}"
        
        return code
    
    def _ensure_error_handling(self, code: str) -> str:
        """Ensure proper error handling is in place"""
        # Check if error handling exists
        has_try_except = "try:" in code and "except" in code
        
        if not has_try_except:
            # Wrap the test function in try-except if not present
            lines = code.split("\n")
            new_lines = []
            in_function = False
            indent_level = 0
            
            for line in lines:
                if line.strip().startswith("def test_"):
                    new_lines.append(line)
                    in_function = True
                    # Calculate indent level
                    indent_level = len(line) - len(line.lstrip()) + 4
                elif in_function and line.strip() and not line.strip().startswith("#"):
                    if "try:" not in "".join(new_lines):
                        new_lines.append(" " * indent_level + "try:")
                        indent_level += 4
                    new_lines.append(line)
                else:
                    new_lines.append(line)
            
            # Add except block before function ends
            if in_function and "except" not in "".join(new_lines):
                new_lines.append(" " * (indent_level - 4) + "except Exception as e:")
                new_lines.append(" " * indent_level + "print(f'Test failed: {str(e)}')")
                new_lines.append(" " * indent_level + "page.screenshot(path='error_screenshot.png')")
                new_lines.append(" " * indent_level + "raise")
            
            code = "\n".join(new_lines)
        
        return code
    
    def generate_assertions(self, step: TestStep) -> str:
        """Generate assertion code for validation steps"""
        action = step.action.lower()
        description = step.description
        
        if any(keyword in action for keyword in ["verify", "check", "assert", "validate"]):
            # Generate appropriate assertion based on description
            if "visible" in description.lower():
                return f"expect(page.locator('selector')).to_be_visible()"
            elif "text" in description.lower():
                return f"expect(page.locator('selector')).to_contain_text('expected_text')"
            elif "url" in description.lower():
                return f"expect(page).to_have_url(re.compile(r'.*expected.*'))"
            elif "title" in description.lower():
                return f"expect(page).to_have_title(re.compile(r'.*expected.*'))"
            else:
                return f"# Assertion: {description}"
        
        return ""
    
    def add_wait_strategies(self, code: str) -> str:
        """Add appropriate wait strategies to the generated code"""
        # Add waits after navigation
        code = re.sub(
            r"(page\.goto\([^)]+\))",
            r"\1\n    page.wait_for_load_state('networkidle')",
            code
        )
        
        # Add waits before interactions
        code = re.sub(
            r"(page\.(click|fill|type)\([^)]+\))",
            r"page.wait_for_selector('selector', state='visible')\n    \1",
            code
        )
        
        return code
    
    def optimize_selectors(self, code: str) -> str:
        """Optimize selectors for better reliability"""
        # This is a placeholder for selector optimization logic
        # In a real implementation, you might want to:
        # 1. Convert CSS selectors to more reliable ones
        # 2. Add data-testid attributes suggestions
        # 3. Use role-based selectors where possible
        
        return code
    
    def validate_generated_code(self, code: str) -> Dict[str, any]:
        """Validate the generated code for common issues"""
        validation_result = {
            "valid": True,
            "warnings": [],
            "errors": []
        }
        
        # Check for required components
        if "def test_" not in code:
            validation_result["errors"].append("No test function defined")
            validation_result["valid"] = False
        
        if "page" not in code:
            validation_result["errors"].append("No page object used")
            validation_result["valid"] = False
        
        # Check for best practices
        if "wait_for_selector" not in code:
            validation_result["warnings"].append("No explicit waits found - may cause flaky tests")
        
        if "screenshot" not in code:
            validation_result["warnings"].append("No screenshot capture on failure")
        
        if "expect" not in code and "assert" not in code:
            validation_result["warnings"].append("No assertions found - test may not validate results")
        
        return validation_result
    
    def get_template_code(self) -> str:
        """Get a basic template for Playwright tests"""
        return """from playwright.sync_api import sync_playwright, expect, Page
import pytest
import time
from pathlib import Path
from datetime import datetime

@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        yield page
        context.close()
        browser.close()

def test_example(page: Page):
    try:
        # Navigate to target URL
        page.goto('https://example.com')
        page.wait_for_load_state('networkidle')
        
        # Your test steps here
        
        # Assertions
        expect(page).to_have_url(re.compile(r'.*example.*'))
        
    except Exception as e:
        # Capture screenshot on failure
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        page.screenshot(path=f'error_{timestamp}.png')
        print(f'Test failed: {str(e)}')
        raise
"""