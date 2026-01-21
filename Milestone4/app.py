# Milestone4/app.py

from Milestone4.agent import run_agent

if __name__ == "__main__":
    output = run_agent(
        "http://example.com",
        "Open website and click link"
    )
    print(output)
