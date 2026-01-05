 # agent/code_generator.py

def generate_test_plan(parsed_input: str) -> dict:
    """
    Generates test steps for ANY public URL or topic.
    """
    text = parsed_input.strip()
    steps = []

    # 🔗 DIRECT PUBLIC URL
    if text.startswith("http://") or text.startswith("https://"):
        steps.append({
            "action": "goto",
            "url": text
        })
        steps.append({
            "action": "extract_text"
        })
        return {"steps": steps}

    # 🔍 TOPIC SEARCH (Wikipedia-style)
    if "give data about" in text or "search" in text:
        query = (
            text.lower()
            .replace("give data about", "")
            .replace("search", "")
            .strip()
        )

        if not query:
            query = "Artificial intelligence"

        wiki_url = "https://en.wikipedia.org/wiki/" + query.replace(" ", "_")

        steps.extend([
            {"action": "goto", "url": wiki_url},
            {"action": "extract_text"}
        ])
        return {"steps": steps}

    # 🌐 DEFAULT FALLBACK
    steps.append({
        "action": "goto",
        "url": "https://example.com"
    })
    steps.append({
        "action": "extract_text"
    })

    return {"steps": steps}
