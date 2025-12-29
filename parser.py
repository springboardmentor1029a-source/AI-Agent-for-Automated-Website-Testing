# parser.py
import re
from urllib.parse import urlparse
from typing import List

from schemas import (
    TestCase, VisitAction, SearchAction, LoginAction,
    AssertCountAction, AssertTextAction, Action
)

def normalize_url(url: str) -> str:
    url = url.strip().rstrip(".,!?")
    if not url.startswith("http"):
        url = "https://" + url
    return url

def extract_url(text: str) -> str | None:
    match = re.search(r'(https?://[^\s<>"{}|\\^`\[\]]+|[a-zA-Z0-9.-]+\.(com|in|org|net|co\.in|co\.uk|de|fr)[^\s]*)', text)
    if match:
        return normalize_url(match.group(0))
    return None

def extract_email(text: str) -> str | None:
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else None

def extract_password(text: str) -> str | None:
    match = re.search(r'(?:password|pass|pwd)[\s:=]*["\']?(\w+)', text, re.IGNORECASE)
    return match.group(1) if match else None

def parse_instruction(instruction: str) -> TestCase:
    instruction = instruction.strip()
    actions: List[Action] = []
    name = instruction[:50] + "..." if len(instruction) > 50 else instruction

    lower = instruction.lower()

    # 1. Visit
    url = extract_url(instruction)
    if url:
        actions.append(VisitAction(url=url))
    else:
        actions.append(VisitAction(url="https://www.google.com"))

    # 2. Search
    if any(word in lower for word in ["search", "find", "look for"]):
        query = "iphone"  # default
        # Try known products
        products = ["macbook", "iphone", "laptop", "shoes", "watch", "tv", "samsung", "oneplus", "airpods"]
        for p in products:
            if p in lower:
                query = p
                break
        else:
            # Extract noun after "search"
            after = lower.split("search", 1)[-1] if "search" in lower else lower
            match = re.search(r'\b([a-zA-Z]{4,15})\b', after)
            if match:
                query = match.group(1)
        actions.append(SearchAction(query=query))

        # Optional: Assert result count
        count_match = re.search(r'should have (\d+|\w+) results?', lower)
        if count_match:
            text = count_match.group(1)
            try:
                exact = int(text)
                actions.append(AssertCountAction(selector="search_results", exact_count=exact))
            except:
                pass

    # 3. Login (expect failure by default)
    if any(word in lower for word in ["login", "log in", "signin", "sign in"]):
        email = extract_email(instruction) or "test@example.com"
        password = extract_password(instruction) or "wrongpass"
        actions.append(LoginAction(email=email, password=password, expect_failure=True))
        actions.append(AssertTextAction(selector=None, text="incorrect|invalid|wrong|not found", negated=False))

    return TestCase(name=name, actions=actions)