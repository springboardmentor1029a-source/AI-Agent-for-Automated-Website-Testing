# parser.py
import re
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, validator

class Action(BaseModel):
    type: Literal["visit", "search", "login"]
    url: Optional[str] = None
    query: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

    @validator('url', always=True)
    def set_default_url(cls, v):
        return v or "https://www.google.com"

class TestCase(BaseModel):
    description: str
    actions: List[Action] = Field(default_factory=list)

def parse_instruction(instruction: str) -> TestCase:
    """
    Parses natural language browser instructions into structured TestCase.
    Supports multi-step: visit, search, login.
    """
    original = instruction.strip()
    instruction = original.lower()
    actions = []
    current_url = None

    # Extract URL
    url_match = re.search(r'(https?://[^\s]+|[a-zA-Z0-9.-]+\.(com|in|org|net|co\.in|co\.uk|de|fr))', instruction)
    if url_match:
        url = url_match.group(0)
        if not url.startswith("http"):
            url = "https://" + url
        current_url = url.rstrip(".,!?;")

    # Split by common separators
    parts = re.split(r'[,.]\s*| and | then ', instruction)

    for part in parts:
        part = part.strip()
        if not part:
            continue

        action = Action(type="visit", url=current_url)

        if any(k in part for k in ["visit", "go to", "open", "go", "navigate to"]):
            action.type = "visit"
            action.url = current_url

        elif any(k in part for k in ["search", "find", "look for", "buy", "shop for"]):
            action.type = "search"
            action.url = current_url or "https://www.amazon.in"
            # Extract query after trigger words
            query_part = part
            for trigger in ["search", "find", "look for", "buy", "shop for"]:
                if trigger in query_part:
                    query_part = query_part.split(trigger, 1)[-1].strip()
                    break
            query = re.sub(r'^(for|the)\s+', '', query_part).strip(' "\'.,')
            action.query = query or "test"

        elif any(k in part for k in ["login", "log in", "signin", "sign in"]):
            action.type = "login"
            action.url = current_url or "https://www.facebook.com"
            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', part)
            action.email = email_match.group(0) if email_match else "test@example.com"
            pass_match = re.search(r'(?:password|pass|pwd)[\s:]*([^\s,]+)', part, re.I)
            action.password = pass_match.group(1) if pass_match else "wrong123"

        if action.type != "visit" or action.url:
            actions.append(action)

    if not actions and current_url:
        actions.append(Action(type="visit", url=current_url))

    return TestCase(description=original, actions=actions)