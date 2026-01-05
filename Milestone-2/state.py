from typing import TypedDict, Dict, Any

class AgentState(TypedDict):
    user_input: str
    parsed_input: str
    test_plan: Dict[str, Any]
    execution: Dict[str, Any]
