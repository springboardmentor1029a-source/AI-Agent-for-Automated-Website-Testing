from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel
from typing import List, Optional
import json
import re

class TestAction(BaseModel):
    """Structured action extracted from user instruction"""
    action_type: str  # e.g., "navigate", "fill", "click", "assert"
    target: Optional[str]  # CSS selector or element description
    value: Optional[str]  # Value to enter (for fill actions)
    description: str  # Human-readable description

class TestStep(BaseModel):
    """Single test step with action and expected outcome"""
    step_number: int
    action: TestAction
    expected_outcome: Optional[str] = None

class ParsedInstruction(BaseModel):
    """Complete parsed instruction"""
    test_name: str
    url: str
    steps: List[TestStep]
    assertions: List[str]

class InstructionParser:
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-flash-latest",
            google_api_key=api_key,
            temperature=0.3
        )

    def parse_instruction(self, user_instruction: str, url: str) -> ParsedInstruction:
        """
        Parse natural language instruction into structured test steps
        
        Example:
        Input: "Test the login with invalid email and check for error message"
        Output: ParsedInstruction with steps like navigate, fill, click, assert
        """
        
        prompt = f"""
You are a test automation expert. Convert the following natural language test instruction 
into a structured test workflow.

URL to test: {url}
User Instruction: {user_instruction}

Return a JSON with this structure:
{{
    "test_name": "descriptive test name",
    "steps": [
        {{
            "step_number": 1,
            "action": {{
                "action_type": "navigate|fill|click|assert|wait|screenshot",
                "target": "CSS selector or element description",
                "value": "value to enter (if applicable)",
                "description": "What this step does"
            }},
            "expected_outcome": "What should happen after this step"
        }}
    ],
    "assertions": ["list of things to verify"]
}}

Common action types:
- navigate: Go to URL
- fill: Enter text in input field
- click: Click on button/element
- assert: Verify text or condition
- wait: Wait for element to appear
- screenshot: Capture page

Be specific with CSS selectors and element descriptions.
"""
        
        messages = [
            SystemMessage(content="You are a test automation parser. Return ONLY valid JSON."),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # Handle response content - it might be a string, list, or dict
        response_text = ""
        if isinstance(response.content, list):
            # If it's a list, extract text from each content block
            for content in response.content:
                if isinstance(content, dict):
                    # Handle dict with 'text' key
                    response_text += content.get('text', str(content))
                else:
                    response_text += str(content)
        elif isinstance(response.content, dict):
            # Handle dict response (e.g., {'type': 'text', 'text': '...'})
            response_text = response.content.get('text', str(response.content))
        else:
            # If it's already a string, use it directly
            response_text = str(response.content)
        
        # Remove markdown code blocks if present (```json ... ```)
        # Remove ```json and ``` markers
        response_text = re.sub(r'```json\s*', '', response_text)
        response_text = re.sub(r'```\s*$', '', response_text, flags=re.MULTILINE)
        response_text = response_text.strip()
        
        # Extract JSON from response
        try:
            # Find JSON object boundaries
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}')
            
            if start_idx == -1 or end_idx == -1:
                raise ValueError("No JSON object found in response")
            
            json_str = response_text[start_idx:end_idx+1]
            parsed_data = json.loads(json_str)
            
            # Build ParsedInstruction object
            steps = []
            for i, step_data in enumerate(parsed_data.get('steps', []), 1):
                action_data = step_data['action']
                action = TestAction(
                    action_type=action_data['action_type'],
                    target=action_data.get('target'),
                    value=action_data.get('value'),
                    description=action_data['description']
                )
                step = TestStep(
                    step_number=i,
                    action=action,
                    expected_outcome=step_data.get('expected_outcome')
                )
                steps.append(step)
            
            parsed_instruction = ParsedInstruction(
                test_name=parsed_data['test_name'],
                url=url,
                steps=steps,
                assertions=parsed_data.get('assertions', [])
            )
            
            return parsed_instruction
        
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing response: {e}")
            print(f"Response type: {type(response.content)}")
            print(f"Response content: {response_text[:500]}...")  # Print first 500 chars
            raise ValueError(f"Failed to parse instruction: {e}. Response: {response_text[:200]}")

# Test the parser
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    parser = InstructionParser(api_key)
    
    instruction = "Navigate to login page, enter invalid email 'test@123', password 'wrong', click login button, and verify error message appears"
    url = "https://example.com/login"
    
    result = parser.parse_instruction(instruction, url)
    print("Parsed Instruction:")
    print(result.model_dump_json(indent=2))
