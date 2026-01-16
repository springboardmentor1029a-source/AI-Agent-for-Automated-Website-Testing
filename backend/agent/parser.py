import re

def parse_instruction(text):
    steps = []
    lines = text.lower().split("\n")

    for line in lines:
        line = line.strip()
        if not line: continue
        
        if "open" in line:
            # support "open website.com" and "goto website.com"
            value = re.sub(r'^(open|goto)\s+', '', line).strip()
            steps.append({"action": "open", "value": value})
            
        elif "search" in line:
            # remove 'search for' or 'search' from the start
            value = re.sub(r'^search\s+(for\s+)?', '', line).strip()
            steps.append({"action": "search", "value": value})
            
        elif any(x in line for x in ["verify", "check", "analyze", "validate"]):
            steps.append({"action": "verify", "value": line})
    return steps
