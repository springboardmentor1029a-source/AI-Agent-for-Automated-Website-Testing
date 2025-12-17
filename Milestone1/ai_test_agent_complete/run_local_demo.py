from agent.workflow import run_agent_test
if __name__ == '__main__':
    instr = "Open demo page, enter username admin and password pass, click login and expect Login successful"
    print(run_agent_test(instr))
