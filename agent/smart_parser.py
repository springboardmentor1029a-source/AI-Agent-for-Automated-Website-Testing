"""
Smart Instruction Parser
Uses Gemini AI with Rule-Based Fallback (No OpenAI needed!)
"""

import os
import re
import json
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class SmartParser:
    """
    Intelligent parser with two strategies:
    1. Gemini AI (primary - fast, free, smart)
    2. Rule-based (fallback - works offline)
    """
    
    def __init__(self):
        self.gemini_available = False
        self.gemini_model = None
        
        # Try to initialize Gemini
        try:
            import google.generativeai as genai
            
            gemini_key = os.getenv('GEMINI_API_KEY')
            if gemini_key:
                genai.configure(api_key=gemini_key)
                # Try different model names - Google keeps changing them
                try:
                    self.gemini_model = genai.GenerativeModel('gemini-pro')
                    print("AI Parser loaded successfully (Gemini Pro)")
                except:
                    try:
                        self.gemini_model = genai.GenerativeModel('models/gemini-pro')
                        print("AI Parser loaded successfully (Gemini Pro v2)")
                    except:
                        # Just skip Gemini and use rules
                        print("Gemini model unavailable, using rule-based parser")
                        self.gemini_available = False
                        return
            else:
                print("Gemini API key not found, using rule-based parser")
        except Exception as e:
            print(f"Gemini initialization failed: {str(e)}")
            print("Falling back to rule-based parser")
    
    def parse(self, instruction: str) -> List[Dict]:
        """Main parsing method with smart fallback"""
        
        # TEMPORARILY DISABLED: Gemini API models keep changing
        # Try Gemini first
        # if self.gemini_available:
        #     result = self._parse_with_gemini(instruction)
        #     if result:
        #         return result
        
        # Use rule-based parser (100% reliable)
        return self._parse_with_rules(instruction)
    
    def _parse_with_gemini(self, instruction: str) -> List[Dict]:
        """Parse using Gemini AI"""
        try:
            prompt = f"""Convert this test instruction into structured actions.

Instruction: "{instruction}"

Return ONLY valid JSON array (no markdown, no explanation):
[
    {{"type": "navigate", "target": "URL", "value": "", "description": "Navigate to URL"}},
    {{"type": "fill", "target": "CSS selector", "value": "text to type", "description": "Fill input"}},
    {{"type": "click", "target": "CSS selector", "value": "", "description": "Click element"}},
    {{"type": "assert_text", "target": "selector", "value": "expected text", "description": "Verify text"}}
]

Types: navigate, click, fill, search, assert_text, assert_url, wait

For URLs: Add https:// if missing
For search: Use type "search" with search query as value
For Google search: type="navigate" to google.com, then type="search" with query

Example 1:
Input: "go to google.com and search for AI tools"
Output: [
  {{"type": "navigate", "target": "https://google.com", "value": "", "description": "Navigate to Google"}},
  {{"type": "search", "target": "input[name='q']", "value": "AI tools", "description": "Search for AI tools"}}
]

Example 2:
Input: "go to amazon.com and search for laptop"
Output: [
  {{"type": "navigate", "target": "https://amazon.com", "value": "", "description": "Navigate to Amazon"}},
  {{"type": "search", "target": "input#twotabsearchtextbox", "value": "laptop", "description": "Search for laptop"}}
]

Now parse: "{instruction}"
"""
            
            response = self.gemini_model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean response
            response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            # Parse JSON
            actions = json.loads(response_text)
            
            if isinstance(actions, list) and len(actions) > 0:
                return actions
                
        except Exception as e:
            print(f"Gemini parsing error: {str(e)}")
        
        return None
    
    def _parse_with_rules(self, instruction: str) -> List[Dict]:
        """Rule-based parser (works without API)"""
        
        actions = []
        inst_lower = instruction.lower()
        
        # Extract URL
        url_patterns = [
            r'(?:go to|navigate to|open|visit)\s+(?:https?://)?([a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,})',
            r'(https?://[^\s]+)',
            r'(www\.[^\s]+)',
            r'([a-zA-Z0-9\-]+\.(?:com|org|net|io|ai))'
        ]
        
        url = None
        for pattern in url_patterns:
            match = re.search(pattern, inst_lower)
            if match:
                url = match.group(1) if '://' not in match.group(0) else match.group(0)
                if not url.startswith('http'):
                    url = 'https://' + url
                actions.append({
                    'type': 'navigate',
                    'target': url,
                    'value': '',
                    'description': f'Navigate to {url}'
                })
                break
        
        # Extract search query
        search_patterns = [
            r'search (?:for |)[\"\']([^\"\']+)[\"\']',
            r'search (?:for |)(\w+(?:\s+\w+)*)',
            r'type [\"\']([^\"\']+)[\"\']',
        ]
        
        for pattern in search_patterns:
            match = re.search(pattern, inst_lower)
            if match:
                query = match.group(1)
                actions.append({
                    'type': 'search',
                    'target': 'input[name="q"], input[type="search"], input#twotabsearchtextbox',
                    'value': query,
                    'description': f'Search for {query}'
                })
                break
        
        # Click actions
        if 'click' in inst_lower:
            click_match = re.search(r'click\s+(?:on\s+)?(?:the\s+)?(\w+)', inst_lower)
            if click_match:
                target = click_match.group(1)
                actions.append({
                    'type': 'click',
                    'target': f'button:has-text("{target}"), #{target}, .{target}',
                    'value': '',
                    'description': f'Click {target}'
                })
        
        if not actions:
            actions.append({
                'type': 'navigate',
                'target': url or 'https://google.com',
                'value': '',
                'description': 'Default navigation'
            })
        
        return actions
