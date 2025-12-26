# test_agent.py
from agent.base_agent import create_agent

# Initialize agent
agent = create_agent()

# Define the input instruction and target
input_state = {
    "instruction": 'type "Jane Doe" in name field and click Submit',
    "target": "/test",
    "mode": "simulate" # Run in simulation mode
}

print("Running test in SIMULATE mode...")
result = agent.invoke(input_state)

print("\n--- TEST REPORT ---")
print(f"Status: {result.get('status')}")
print(f"Duration: {result.get('duration_sec', 0)}s")
print(f"Total Steps: {result.get('total_steps')}")
print(f"Passed Assertions: {result.get('passed_steps')}")
print(f"Failed Assertions: {result.get('failed_steps')}")

for step in result.get("step_results", []):
    print(f"  Step {step['step']} ({step['status']}): {step['action']} - {step['detail']}")