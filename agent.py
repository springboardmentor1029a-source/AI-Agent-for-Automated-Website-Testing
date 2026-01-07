"""Baseline LangGraph agent configuration for handling user inputs."""
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AgentState(TypedDict):
    """State for the LangGraph agent."""
    user_input: str
    response: str
    status: str


class BaselineAgent:
    """
    Baseline LangGraph agent configuration.
    This is a simple implementation that will be enhanced in later milestones.
    """
    
    def __init__(self):
        """Initialize the baseline agent."""
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """
        Build the LangGraph workflow.
        This is a baseline configuration with simple input handling.
        """
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("process_input", self._process_input)
        workflow.add_node("generate_response", self._generate_response)
        
        # Define flow
        workflow.set_entry_point("process_input")
        workflow.add_edge("process_input", "generate_response")
        workflow.add_edge("generate_response", END)
        
        return workflow.compile()
    
    def _process_input(self, state: AgentState) -> AgentState:
        """
        Process the user input.
        Baseline implementation - just validates and stores the input.
        """
        user_input = state.get("user_input", "")
        
        if not user_input:
            state["status"] = "error"
            state["response"] = "No input provided"
        else:
            state["status"] = "processing"
            # In baseline, we just acknowledge the input
            # This will be enhanced with actual LLM processing in later milestones
        
        return state
    
    def _generate_response(self, state: AgentState) -> AgentState:
        """
        Generate a response to the user input.
        Baseline implementation - returns a simple acknowledgment.
        """
        user_input = state.get("user_input", "")
        
        if state.get("status") == "error":
            state["response"] = "Error: " + state.get("response", "Unknown error")
        else:
            # Baseline response - will be enhanced with LLM in later milestones
            state["response"] = f"Baseline agent received: '{user_input}'. Ready for enhancement with LLM processing."
            state["status"] = "success"
        
        return state
    
    def process(self, user_input: str) -> dict:
        """
        Process user input through the agent workflow.
        
        Args:
            user_input: The user's input string
            
        Returns:
            Dictionary with status and response
        """
        initial_state: AgentState = {
            "user_input": user_input,
            "response": "",
            "status": "pending"
        }
        
        # Execute the workflow
        final_state = self.workflow.invoke(initial_state)
        
        return {
            "status": final_state.get("status", "unknown"),
            "message": final_state.get("response", ""),
            "input": final_state.get("user_input", "")
        }


# Global agent instance
_agent_instance = None


def get_agent() -> BaselineAgent:
    """Get or create the global agent instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = BaselineAgent()
    return _agent_instance

