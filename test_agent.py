from agent.base_agent import create_agent
import json

def main():
    agent = create_agent()
    # initial state must at least include instruction (and optionally target)
    state = {"instruction": 'Open the page, type "Harshitha Somu" in name field and click Submit', "target": "/test"}

    # compiled graph object supports invoke()
    result = agent.invoke(state)
    print("Result (graph invoke):")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
