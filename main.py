import os
from dotenv import load_dotenv

load_dotenv()

from agent_graph import app

def test_parser():
    inputs = {
        "instruction": "Open the home page and click the login button",
        "parsed_actions": [],
        "current_step_index": 0,
        "execution_history": [],
        "retry_count": 0
    }
    
    print("--- Running Agent Parser ---")
    config = {"configurable": {"thread_id": "1"}}
    output = app.invoke(inputs, config)
    
    print("\nParsed Results:")
    for i, action in enumerate(output["parsed_actions"]):
        print(f"Step {i+1}: {action}")

if __name__ == "__main__":
    test_parser()