
from typing import List, Dict, Any, Optional, Tuple
import re


class DOMMapper:
    """Maps elements using multiple selector strategies with fallbacks"""
    
    def __init__(self):
        self.selector_history = []
        self.successful_selectors = {}
    
    def find_element(self, page, description: str, primary_selector: str = None) -> Optional[Any]:
        """
        Find element using multiple strategies
        
        Args:
            page: Playwright page object
            description: Human-readable element description
            primary_selector: Primary CSS selector to try first
            
        Returns:
            Playwright locator object or None
        """
        strategies = self._generate_selector_strategies(description, primary_selector)
        
        for i, (strategy_name, selector) in enumerate(strategies, 1):
            try:
                print(f"  [{i}/{len(strategies)}] Trying {strategy_name}: {selector}")
                
                # Try to locate element
                locator = page.locator(selector)
                
                # Check if element exists
                if locator.count() > 0:
                    print(f"  ✓ Found element using {strategy_name}")
                    
                    # Log successful selector
                    self._log_successful_selector(description, selector, strategy_name)
                    
                    return locator.first
                    
            except Exception as e:
                print(f"  ✗ {strategy_name} failed: {str(e)}")
                continue
        
        print(f"  ❌ Could not find element: {description}")
        return None
    
    def _generate_selector_strategies(self, description: str, 
                                     primary_selector: str = None) -> List[Tuple[str, str]]:
        """
        Generate list of selector strategies to try
        
        Args:
            description: Element description
            primary_selector: Primary selector
            
        Returns:
            List of (strategy_name, selector) tuples
        """
        strategies = []
        
        # Strategy 1: Primary selector if provided
        if primary_selector:
            strategies.append(("Primary Selector", primary_selector))
        
        # Strategy 2: Check if description mentions common patterns
        description_lower = description.lower()
        
        # Extract potential selectors from description
        if "button" in description_lower:
            # Try button-specific selectors
            if "submit" in description_lower:
                strategies.extend([
                    ("Button by Type", "button[type='submit']"),
                    ("Input Submit", "input[type='submit']"),
                    ("Button Text", "button:has-text('submit')"),
                    ("Button Text (case-insensitive)", "button:text-is('Submit')"),
                ])
            
            if "login" in description_lower:
                strategies.extend([
                    ("Login Button ID", "#login, #loginButton, #btn-login"),
                    ("Login Button Class", ".login, .login-button, .btn-login"),
                    ("Login Button Text", "button:has-text('login')"),
                ])
            
            # Generic button selectors
            strategies.append(("Any Button", "button"))
        
        if "input" in description_lower or "field" in description_lower:
            if "email" in description_lower:
                strategies.extend([
                    ("Email Input Type", "input[type='email']"),
                    ("Email Input Name", "input[name*='email']"),
                    ("Email Input ID", "#email, #emailAddress"),
                    ("Email Input Placeholder", "input[placeholder*='email' i]"),
                ])
            
            if "password" in description_lower:
                strategies.extend([
                    ("Password Input Type", "input[type='password']"),
                    ("Password Input Name", "input[name*='password']"),
                    ("Password Input ID", "#password, #passwd"),
                ])
            
            if "name" in description_lower:
                strategies.extend([
                    ("Name Input", "input[name='name']"),
                    ("Name Input Type", "input[type='text'][name*='name']"),
                    ("Name Input ID", "#name, #fullname, #username"),
                ])
        
        if "link" in description_lower or "anchor" in description_lower:
            # Extract link text from description
            text_match = re.search(r'"([^"]+)"', description)
            if text_match:
                link_text = text_match.group(1)
                strategies.extend([
                    ("Link by Text", f"a:has-text('{link_text}')"),
                    ("Link by Exact Text", f"a:text-is('{link_text}')"),
                ])
            strategies.append(("Any Link", "a"))
        
        # Strategy 3: Common ID patterns
        keywords = self._extract_keywords(description)
        for keyword in keywords:
            strategies.append((f"ID with '{keyword}'", f"#{keyword}, [id*='{keyword}']"))
        
        # Strategy 4: Common class patterns
        for keyword in keywords:
            strategies.append((f"Class with '{keyword}'", f".{keyword}, [class*='{keyword}']"))
        
        # Strategy 5: Aria labels and roles
        for keyword in keywords:
            strategies.extend([
                (f"Aria Label '{keyword}'", f"[aria-label*='{keyword}' i]"),
                (f"Aria LabelledBy '{keyword}'", f"[aria-labelledby*='{keyword}' i]"),
            ])
        
        # Strategy 6: Data attributes
        for keyword in keywords:
            strategies.append((f"Data attribute '{keyword}'", f"[data-testid*='{keyword}'], [data-test*='{keyword}']"))
        
        # Strategy 7: Generic text content
        for keyword in keywords:
            strategies.append((f"Text contains '{keyword}'", f":text('{keyword}')"))
        
        return strategies
    
    def _extract_keywords(self, description: str) -> List[str]:
        """
        Extract keywords from description
        
        Args:
            description: Element description
            
        Returns:
            List of keywords
        """
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during'}
        
        # Extract words
        words = re.findall(r'\b\w+\b', description.lower())
        
        # Filter and return
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        return keywords[:5]  # Return top 5 keywords
    
    def _log_successful_selector(self, description: str, selector: str, strategy: str):
        """Log successful selector for future reference"""
        entry = {
            "description": description,
            "selector": selector,
            "strategy": strategy,
            "success_count": 1
        }
        
        # Update or add to successful selectors
        key = f"{description}:{selector}"
        if key in self.successful_selectors:
            self.successful_selectors[key]["success_count"] += 1
        else:
            self.successful_selectors[key] = entry
    
    def get_best_selector(self, description: str) -> Optional[str]:
        """
        Get most successful selector for a description
        
        Args:
            description: Element description
            
        Returns:
            Best selector or None
        """
        matching = [v for k, v in self.successful_selectors.items() 
                   if v["description"] == description]
        
        if not matching:
            return None
        
        # Return selector with highest success count
        best = max(matching, key=lambda x: x["success_count"])
        return best["selector"]
    
    def generate_smart_selector(self, element_type: str, attributes: Dict[str, str]) -> str:
        """
        Generate smart selector from element attributes
        
        Args:
            element_type: Type of element (button, input, etc.)
            attributes: Dictionary of element attributes
            
        Returns:
            Generated CSS selector
        """
        selectors = [element_type]
        
        # Prioritize attributes
        priority = ['id', 'data-testid', 'data-test', 'name', 'type', 'class']
        
        for attr in priority:
            if attr in attributes and attributes[attr]:
                value = attributes[attr]
                
                if attr == 'id':
                    return f"#{value}"  # ID is most specific, return immediately
                elif attr == 'class':
                    classes = value.split()
                    if classes:
                        return f"{element_type}.{classes[0]}"
                else:
                    selectors.append(f"[{attr}='{value}']")
        
        return "".join(selectors)
    
    def suggest_alternative_selectors(self, failed_selector: str) -> List[str]:
        """
        Suggest alternative selectors when one fails
        
        Args:
            failed_selector: The selector that failed
            
        Returns:
            List of alternative selectors
        """
        alternatives = []
        
        # If it's an ID selector
        if failed_selector.startswith('#'):
            element_id = failed_selector[1:]
            alternatives.extend([
                f"[id='{element_id}']",
                f"[id*='{element_id}']",
                f":text('{element_id}')",
            ])
        
        # If it's a class selector
        elif failed_selector.startswith('.'):
            class_name = failed_selector[1:]
            alternatives.extend([
                f"[class*='{class_name}']",
                f"[class~='{class_name}']",
            ])
        
        # If it contains attribute selector
        elif '[' in failed_selector:
            # Extract attribute name
            attr_match = re.search(r'\[(\w+)', failed_selector)
            if attr_match:
                attr = attr_match.group(1)
                alternatives.append(f"[{attr}]")  # Just check attribute exists
        
        return alternatives


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("DOM MAPPER - TESTING")
    print("=" * 60)
    
    mapper = DOMMapper()
    
    # Test 1: Generate strategies
    print("\n[Test 1] Generate Selector Strategies")
    print("-" * 60)
    
    strategies = mapper._generate_selector_strategies(
        "click the submit button",
        primary_selector="button#submit"
    )
    
    print(f"Generated {len(strategies)} strategies:")
    for i, (name, selector) in enumerate(strategies[:10], 1):  # Show first 10
        print(f"  {i}. {name}: {selector}")
    
    # Test 2: Extract keywords
    print("\n[Test 2] Extract Keywords")
    print("-" * 60)
    
    keywords = mapper._extract_keywords("Click the login button on the main page")
    print(f"Keywords: {keywords}")
    
    # Test 3: Generate smart selector
    print("\n[Test 3] Generate Smart Selector")
    print("-" * 60)
    
    selector = mapper.generate_smart_selector("button", {
        "type": "submit",
        "class": "btn btn-primary",
        "name": "submitBtn"
    })
    print(f"Generated selector: {selector}")
    
    # Test 4: Suggest alternatives
    print("\n[Test 4] Suggest Alternative Selectors")
    print("-" * 60)
    
    alternatives = mapper.suggest_alternative_selectors("#loginButton")
    print("Alternatives for '#loginButton':")
    for alt in alternatives:
        print(f"  • {alt}")
    
    print("\n" + "=" * 60)
    print("✅ DOM MAPPER TESTS COMPLETE")
    print("=" * 60)
    