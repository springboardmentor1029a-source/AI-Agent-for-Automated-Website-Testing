"""Parse instructions"""
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from agent.state import TestStep

class TestStepsList(BaseModel):
    steps: List[TestStep] = Field(description="List of test steps")

class InstructionParser:
    def __init__(self, llm):
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=TestStepsList)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Parse test instructions into steps.
Actions: navigate, click, fill, assert, wait
{format_instructions}
Target URL: {target_url}"""),
            ("user", "{instruction}")
        ])
    
    def parse(self, instruction: str, target_url: str = "") -> List[TestStep]:
        chain = self.prompt | self.llm | self.parser
        result = chain.invoke({
            "instruction": instruction,
            "target_url": target_url,
            "format_instructions": self.parser.get_format_instructions()
        })
        return result.steps
