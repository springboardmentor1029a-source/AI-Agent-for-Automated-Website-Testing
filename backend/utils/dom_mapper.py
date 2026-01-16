from playwright.sync_api import Page, Locator

def find_element(page: Page, selector: str, timeout: int = 5000) -> Locator:
    """
    Tries to find an element using multiple strategies to handle dynamic IDs or changes.
    """
    # Create variations of casing (Original, Lowercase, Titlecase)
    variations = {selector, selector.lower(), selector.title()}
    
    strategies = []
    for s in variations:
        strategies.extend([
            f"[aria-label='{s}']",                  # Aria Label
            f"[placeholder='{s}']",                 # Placeholder
            f"button:has-text('{s}')",              # Button text
            f"a:has-text('{s}')",                   # Link text
            f"text={s}",                            # Text content
            f"[title='{s}']",                       # Title attribute
            f"[data-testid='{s}']",                 # Test ID
             # Basic IDs if valid CSS 
            f"#{s}" if " " not in s else None, 
        ])
    
    # Filter out None and duplicate strategies while preserving order
    seen = set()
    cleaned_strategies = []
    for s in strategies:
        if s and s not in seen:
            cleaned_strategies.append(s)
            seen.add(s)
    
    # Add generic fallbacks at the end
    cleaned_strategies.append(selector)

    for strategy in cleaned_strategies:
        try:
            element = page.locator(strategy).first
            if element.count() > 0:  
                # If we found something, try to ensure it's actionable
                try:
                    element.wait_for(state="attached", timeout=500)
                    if element.is_visible():
                        return element
                except:
                    pass
                # Even if not visible, we return it as best guess if it's attached
                return element
        except Exception:
            continue
            
    # Fallback: If no strategy works, return None so the caller can use a generic fallback
    return None
