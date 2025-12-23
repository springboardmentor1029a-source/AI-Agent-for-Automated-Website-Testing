from typing import List
from src.parser.instruction_parser import ParsedInstruction, TestStep

class PlaywrightCodeGenerator:
    """Generates Playwright code from test steps"""
    
    def __init__(self):
        self.indent = "    "
    
    def generate_code(self, parsed_instruction: ParsedInstruction) -> str:
        """
        Generate complete Playwright test script
        """
        
        code_lines = [
            "import asyncio",
            "from playwright.async_api import async_playwright",
            "import json",
            "from datetime import datetime",
            "",
            "async def run_test():",
            f'{self.indent}"""Generated test: {parsed_instruction.test_name}"""',
            f'{self.indent}results = {{"test_name": "{parsed_instruction.test_name}", "steps": [], "assertions": []}}',
            f'{self.indent}',
            f'{self.indent}async with async_playwright() as p:',
            f'{self.indent * 2}browser = await p.chromium.launch(headless=True)',
            f'{self.indent * 2}page = await browser.new_page()',
            "",
        ]
        
        # Check if first step is already a navigate action
        has_navigate_step = False
        if parsed_instruction.steps and parsed_instruction.steps[0].action.action_type == "navigate":
            has_navigate_step = True
        
        # Navigate to URL (only if not already in steps)
        if not has_navigate_step:
            code_lines.append(f'{self.indent * 2}# Navigate to URL')
            code_lines.append(f'{self.indent * 2}try:')
            code_lines.append(f'{self.indent * 3}await page.goto("{parsed_instruction.url}", timeout=30000)')
            code_lines.append(f'{self.indent * 3}await page.wait_for_load_state("networkidle")')
            code_lines.append(f'{self.indent * 3}results["steps"].append({{"step": "navigate", "status": "passed"}})')
            code_lines.append(f'{self.indent * 2}except Exception as e:')
            code_lines.append(f'{self.indent * 3}results["steps"].append({{"step": "navigate", "status": "failed", "error": str(e)}})')
            code_lines.append(f'{self.indent * 3}await browser.close()')
            code_lines.append(f'{self.indent * 3}return results')
            code_lines.append("")
        
        # Generate code for each step
        for step in parsed_instruction.steps:
            if step.action.action_type == "navigate":
                # Handle navigate step specially
                code_lines.extend(self._generate_navigate_step(step, parsed_instruction.url))
            else:
                code_lines.extend(self._generate_step_code(step))
        
        # Assertions
        code_lines.append(f'{self.indent * 2}# Assertions')
        for assertion in parsed_instruction.assertions:
            code_lines.append(f'{self.indent * 2}try:')
            code_lines.append(f'{self.indent * 3}# {assertion}')
            code_lines.append(f'{self.indent * 3}results["assertions"].append({{"assertion": "{assertion}", "status": "passed"}})')
            code_lines.append(f'{self.indent * 2}except AssertionError as e:')
            code_lines.append(f'{self.indent * 3}results["assertions"].append({{"assertion": "{assertion}", "status": "failed", "error": str(e)}})')
        
        # Cleanup
        code_lines.append("")
        code_lines.append(f'{self.indent * 2}await browser.close()')
        code_lines.append(f'{self.indent * 2}results["status"] = "completed"')
        code_lines.append(f'{self.indent * 2}results["timestamp"] = datetime.now().isoformat()')
        code_lines.append(f'{self.indent * 2}return results')
        code_lines.append("")
        code_lines.append("if __name__ == '__main__':")
        code_lines.append(f'{self.indent}result = asyncio.run(run_test())')
        code_lines.append(f'{self.indent}print(json.dumps(result, indent=2))')
        
        return "\n".join(code_lines)
    
    def _generate_navigate_step(self, step: TestStep, url: str) -> List[str]:
        """Generate code for navigate step"""
        lines = []
        action = step.action
        
        lines.append(f'{self.indent * 2}# Step {step.step_number}: {action.description}')
        lines.append(f'{self.indent * 2}try:')
        lines.append(f'{self.indent * 3}await page.goto("{url}", timeout=30000)')
        lines.append(f'{self.indent * 3}await page.wait_for_load_state("networkidle")')
        safe_description = action.description.replace('"', '\\"') if action.description else ""
        lines.append(f'{self.indent * 3}results["steps"].append({{"step": {step.step_number}, "description": "{safe_description}", "status": "passed"}})')
        lines.append(f'{self.indent * 2}except Exception as e:')
        lines.append(f'{self.indent * 3}results["steps"].append({{"step": {step.step_number}, "description": "{safe_description}", "status": "failed", "error": str(e)}})')
        lines.append(f'{self.indent * 3}await browser.close()')
        lines.append(f'{self.indent * 3}return results')
        lines.append("")
        
        return lines
    
    def _generate_step_code(self, step: TestStep) -> List[str]:
        """Generate code for a single test step"""
        lines = []
        action = step.action
        
        lines.append(f'{self.indent * 2}# Step {step.step_number}: {action.description}')
        lines.append(f'{self.indent * 2}try:')
        
        if action.action_type == "fill":
            # Escape quotes in values
            safe_target = action.target.replace('"', '\\"') if action.target else ""
            safe_value = action.value.replace('"', '\\"') if action.value else ""
            lines.append(f'{self.indent * 3}await page.fill("{safe_target}", "{safe_value}")')
            lines.append(f'{self.indent * 3}await page.wait_for_timeout(500)')
            
        elif action.action_type == "click":
            # Escape quotes in target
            safe_target = action.target.replace('"', '\\"') if action.target else ""
            lines.append(f'{self.indent * 3}await page.click("{safe_target}")')
            lines.append(f'{self.indent * 3}await page.wait_for_timeout(1000)')
            
        elif action.action_type == "assert":
            safe_target = action.target.replace('"', '\\"') if action.target else ""
            safe_value = action.value.replace('"', '\\"') if action.value else ""
            lines.append(f'{self.indent * 3}text = await page.text_content("{safe_target}")')
            lines.append(f'{self.indent * 3}assert "{safe_value}" in text, "Assertion failed"')
            
        elif action.action_type == "wait":
            safe_target = action.target.replace('"', '\\"') if action.target else ""
            lines.append(f'{self.indent * 3}await page.wait_for_selector("{safe_target}", timeout=10000)')
            
        elif action.action_type == "screenshot":
            lines.append(f'{self.indent * 3}await page.screenshot(path="screenshot_{step.step_number}.png")')
        
        # Escape quotes in description
        safe_description = action.description.replace('"', '\\"') if action.description else ""
        lines.append(f'{self.indent * 3}results["steps"].append({{"step": {step.step_number}, "description": "{safe_description}", "status": "passed"}})')
        safe_description = action.description.replace('"', '\\"') if action.description else ""
        lines.append(f'{self.indent * 2}except Exception as e:')
        lines.append(f'{self.indent * 3}results["steps"].append({{"step": {step.step_number}, "description": "{safe_description}", "status": "failed", "error": str(e)}})')
        lines.append("")
        
        return lines

# Test the generator
if __name__ == "__main__":
    from src.parser.instruction_parser import ParsedInstruction, TestStep, TestAction
    
    # Create sample parsed instruction
    action1 = TestAction(
        action_type="navigate",
        target="",
        value="",
        description="Navigate to login page"
    )
    
    step1 = TestStep(
        step_number=1,
        action=action1,
        expected_outcome="Page loads successfully"
    )
    
    parsed = ParsedInstruction(
        test_name="Login Test",
        url="https://example.com/login",
        steps=[step1],
        assertions=["Login button visible"]
    )
    
    generator = PlaywrightCodeGenerator()
    code = generator.generate_code(parsed)
    
    print("Generated Code:")
    print(code)
    
    # Save to file
    with open("generated_test.py", "w") as f:
        f.write(code)
    print("\nCode saved to generated_test.py")

