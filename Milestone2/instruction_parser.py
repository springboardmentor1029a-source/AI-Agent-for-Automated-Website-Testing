import re

def parse_instruction(text):
    text = text.lower()

    parsed = {
        "action": None,
        "url": None,
        "assert": None,
        "value": None
    }

    # Detect URL
    url_match = re.search(r"(https?://\S+)", text)
    if url_match:
        parsed["url"] = url_match.group(1)
        parsed["action"] = "open_url"

    # Detect title validation
    if "title" in text and "contains" in text:
        parsed["assert"] = "title_contains"
        parsed["value"] = text.split("contains")[-1].strip()

    return parsed
