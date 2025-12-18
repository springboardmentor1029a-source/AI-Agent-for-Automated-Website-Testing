"""Generate test scripts"""
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from agent.state import TestStep

class TestGenerator:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Generate Playwright Python test from steps. Return only code."),
            ("user", "Target: {target_url}\nSteps:\n{steps}\n\nGenerate script:")
        ])
    
    def generate(self, steps: List[TestStep], target_url: str = "") -> str:
        steps_text = "\n".join([f"{i+1}. {s.action.upper()}: {s.description}" for i, s in enumerate(steps)])
        chain = self.prompt | self.llm
        result = chain.invoke({"target_url": target_url, "steps": steps_text})
        code = result.content
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()
        return code
