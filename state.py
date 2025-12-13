# agent/state.py
from typing import TypedDict, List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class TestStep:
    """Represents a single test step"""
    action: str  # navigate, click, type, wait, verify, etc.
    target: str  # CSS selector or URL
    value: Optional[str] = None  # Value for type/input actions
    description: str = ""  # Human-readable description


class AgentState(TypedDict):
    """State that flows through the agent graph"""
    instruction: str  # User's natural language instruction
    target_url: str  # URL to test
    messages: List[Any]  # Conversation messages
    parsed_steps: List[TestStep]  # Parsed test steps
    test_script: str  # Generated Playwright script
    execution_status: str  # pending, running, completed, failed
    test_results: Dict[str, Any]  # Results from execution
    screenshots: List[str]  # Screenshot paths
    report: Dict[str, Any]  # Final test report
    error: Optional[str]  # Error message if any
