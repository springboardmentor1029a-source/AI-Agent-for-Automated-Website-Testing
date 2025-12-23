from typing import TypedDict, List, Optional, Annotated
import operator

class AgentState(TypedDict):
    instruction: str
    parsed_actions: List[dict]
    current_step_index: int
    execution_history: Annotated[List[dict], operator.add]
    logs: Annotated[List[str], operator.add]  
    last_screenshot: Optional[str]            
    error_log: Optional[str]
    page_source: Optional[str]
    retry_count: int
    final_report:Optional[str]