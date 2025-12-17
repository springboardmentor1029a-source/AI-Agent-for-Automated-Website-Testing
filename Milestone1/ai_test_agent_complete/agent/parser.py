import re
from typing import List, Dict
# This parser is a practical hybrid: rule-based extraction + placeholders for NLP (spaCy)
def parse_instruction(text: str):
    text_low = text.lower()
    steps = []
    # simple rules for common actions
    if "open" in text_low or "go to" in text_low:
        m = re.search(r'open\s+([^,]+)', text_low)
        if m:
            steps.append({"action":"goto", "target": m.group(1).strip()})
        else:
            steps.append({"action":"goto", "target": "http://127.0.0.1:5000/static/testpage.html"})
    if "username" in text_low or "user name" in text_low:
        # value after username keywords
        m = re.search(r'(?:username|user name)\s+(?:is|=)?\s*([\w@.-]+)', text_low)
        val = m.group(1) if m else "admin"
        steps.append({"action":"fill", "target":"#username", "value": val})
    if "password" in text_low:
        m = re.search(r'password\s+(?:is|=)?\s*([\w@.-]+)', text_low)
        val = m.group(1) if m else "pass"
        steps.append({"action":"fill", "target":"#password", "value": val})
    if "click" in text_low or "press" in text_low:
        if "login" in text_low:
            steps.append({"action":"click", "target":"#loginBtn"})
    # expected outcome extraction (very simple)
    expect = None
    m = re.search(r'expect\s+([^,]+)', text_low)
    if m:
        expect = m.group(1).strip()
        steps.append({"action":"expect_text", "target":"#result", "value": expect})
    return steps
