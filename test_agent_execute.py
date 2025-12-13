from agent.base_agent import create_agent
import json

agent = create_agent()

state = {
    "instruction": "open amazon and check redmi phones availability",
    "mode": "execute"
}

res = agent.invoke(state)
print(json.dumps(res, indent=2))
