"""
Instruction Parser Module
Converts natural language test instructions into structured actions
"""

import re
from typing import List, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import os

class InstructionParser:
    """Parses natural language instructions into structured test actions"""
    
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0,
            google_api_key=api_key
        ) if api_key and api_key != 'your_gemini_api_key_here' else None
        
    def parse(self, instruction: str) -> List[Dict]:
        """
        Parse natural language instruction into structured actions
        
        Args:
            instruction: Natural language test description
            
        Returns:
            List of action dictionaries with type, target, value, and assertion info
        """
        if self.llm:
            return self._parse_with_llm(instruction)
        else:
            return self._parse_with_rules(instruction)
    
    def _parse_with_llm(self, instruction: str) -> List[Dict]:
        """Parse using LLM for better accuracy"""
        prompt = PromptTemplate(
            input_variables=["instruction"],
            template="""You are an expert at converting natural language test instructions into structured test actions.

Given this test instruction:
{instruction}

Convert it into a JSON array of action objects. Each action should have:
- "type": One of "navigate", "click", "fill", "select", "check", "assert_text", "assert_visible", "assert_url", "wait"
- "target": CSS selector, URL, or text to find (can be approximate for LLM to figure out)
- "value": Value to fill/select (for fill, select actions) or expected value (for assertions)
- "description": Human readable description of this step

Example output format:
[
  {{"type": "navigate", "target": "https://example.com", "value": "", "description": "Navigate to example.com"}},
  {{"type": "fill", "target": "input[name='email']", "value": "test@example.com", "description": "Fill email field"}},
  {{"type": "click", "target": "button[type='submit']", "value": "", "description": "Click submit button"}},
  {{"type": "assert_text", "target": "body", "value": "Success", "description": "Check for success message"}}
]

Provide ONLY the JSON array, no other text.
"""
        )
        
        try:
            result = self.llm.invoke(prompt.format(instruction=instruction))
            content = result.content.strip()
            
            # Extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            import json
            actions = json.loads(content)
            return actions
        except Exception as e:
            print(f"LLM parsing failed: {e}, falling back to rule-based parsing")
            return self._parse_with_rules(instruction)
    
    def _parse_with_rules(self, instruction: str) -> List[Dict]:
        """Fallback rule-based parsing"""
        actions = []
        lines = instruction.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            line_lower = line.lower()
            
            # Navigate patterns - support URLs without http/https
            if 'navigate' in line_lower or 'go to' in line_lower or 'open' in line_lower or 'visit' in line_lower:
                # Extract URL
                url_match = re.search(r'(https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9-]+\.[a-zA-Z]{2,})', line)
                if url_match:
                    url = url_match.group(1)
                    # Add https:// if not present
                    if not url.startswith('http'):
                        url = 'https://' + url
                    actions.append({
                        'type': 'navigate',
                        'target': url,
                        'value': '',
                        'description': f'Navigate to {url}'
                    })
            
            # Search patterns (for search boxes)
            elif 'search for' in line_lower or 'search' in line_lower and 'for' in line_lower:
                # Extract search query
                if 'search for' in line_lower:
                    query = line_lower.split('search for')[1].strip()
                else:
                    query = line_lower.split('for')[1].strip() if 'for' in line_lower else ''
                
                query = self._extract_quoted_text(line) or query.strip()
                
                actions.append({
                    'type': 'search',
                    'target': 'search',
                    'value': query,
                    'description': f'Search for "{query}"'
                })
            
            # Type patterns (for input fields)
            elif 'type' in line_lower and ('in' in line_lower or 'into' in line_lower):
                parts = re.split(r'\s+in\s+|\s+into\s+', line_lower, maxsplit=1)
                if len(parts) == 2:
                    value = parts[0].replace('type', '').strip()
                    value = self._extract_quoted_text(line) or value
                    target = parts[1].strip()
                    actions.append({
                        'type': 'fill',
                        'target': target,
                        'value': value,
                        'description': f'Type "{value}" in {target}'
                    })
            
            # Click patterns
            elif 'click' in line_lower or 'press' in line_lower:
                target = self._extract_target(line, ['click', 'press', 'button', 'link', 'on', 'the'])
                target = self._extract_quoted_text(line) or target
                actions.append({
                    'type': 'click',
                    'target': target,
                    'value': '',
                    'description': f'Click on "{target}"'
                })
            
            # Fill/Enter patterns
            elif 'fill' in line_lower or 'enter' in line_lower:
                if ' with ' in line_lower:
                    parts = line_lower.split(' with ')
                    target = self._extract_target(parts[0], ['fill', 'enter', 'in', 'into', 'the'])
                    value = parts[1].strip()
                    value = self._extract_quoted_text(line.split(' with ')[1]) or value
                    actions.append({
                        'type': 'fill',
                        'target': target,
                        'value': value,
                        'description': f'Fill {target} with "{value}"'
                    })
            
            # Wait patterns
            elif 'wait' in line_lower:
                seconds_match = re.search(r'(\d+)\s*(?:second|sec)', line_lower)
                seconds = seconds_match.group(1) if seconds_match else '2'
                actions.append({
                    'type': 'wait',
                    'target': '',
                    'value': seconds,
                    'description': f'Wait {seconds} seconds'
                })
            
            # Assert/Check patterns
            elif 'check' in line_lower or 'verify' in line_lower or 'assert' in line_lower or 'should see' in line_lower or 'contains' in line_lower:
                if 'url' in line_lower:
                    value = self._extract_quoted_text(line)
                    actions.append({
                        'type': 'assert_url',
                        'target': '',
                        'value': value,
                        'description': f'Verify URL contains "{value}"'
                    })
                else:
                    value = self._extract_quoted_text(line)
                    if not value:
                        # Extract text after check/verify/contains
                        for keyword in ['check', 'verify', 'contains', 'should see']:
                            if keyword in line_lower:
                                value = line_lower.split(keyword)[1].strip()
                                break
                    actions.append({
                        'type': 'assert_text',
                        'target': 'body',
                        'value': value,
                        'description': f'Verify page contains "{value}"'
                    })
        
        return actions
    
    def _extract_target(self, text: str, keywords: List[str]) -> str:
        """Extract target element from text"""
        for keyword in keywords:
            text = text.replace(keyword, '')
        
        # Extract quoted text
        quoted = self._extract_quoted_text(text)
        if quoted:
            return quoted
        
        return text.strip()
    
    def _extract_quoted_text(self, text: str) -> str:
        """Extract text within quotes"""
        matches = re.findall(r'["\']([^"\']+)["\']', text)
        if matches:
            return matches[0]
        return ''
