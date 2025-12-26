import os
from agent.base_agent import run_agent

# 1. SET YOUR API KEY
# Replace the text below with the actual key you got from Google AI Studio
os.environ["GEMINI_API_KEY"] = "YOUR API KEY HERE"

if __name__ == "__main__":
    print("--- Gemini Web Agent Loaded ---")
    
    # 2. ASK THE USER FOR A TASK
    user_task = input("What should I do? (e.g. 'Search for shoes on Myntra'): ")
    
    # 3. RUN THE AGENT
    if user_task:
        run_agent(user_task)
    else:
        print("No task entered. Exiting.")
