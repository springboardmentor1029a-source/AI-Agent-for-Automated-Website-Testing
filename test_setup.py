"""Quick test script to verify Milestone 1 setup."""
import sys

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import playwright
        print("✅ Playwright imported successfully")
    except ImportError as e:
        print(f"❌ Playwright import failed: {e}")
        return False
    
    try:
        import langgraph
        print("✅ LangGraph imported successfully")
    except ImportError as e:
        print(f"❌ LangGraph import failed: {e}")
        return False
    
    try:
        from agent import BaselineAgent
        print("✅ Agent module imported successfully")
    except ImportError as e:
        print(f"❌ Agent module import failed: {e}")
        return False
    
    try:
        from app import app
        print("✅ Flask app imported successfully")
    except ImportError as e:
        print(f"❌ Flask app import failed: {e}")
        return False
    
    return True


def test_agent():
    """Test the baseline agent."""
    print("\nTesting baseline agent...")
    
    try:
        from agent import get_agent
        
        agent = get_agent()
        result = agent.process("Test input")
        
        if result["status"] == "success":
            print("✅ Agent processed input successfully")
            print(f"   Response: {result['message']}")
            return True
        else:
            print(f"❌ Agent returned error status: {result['status']}")
            return False
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Milestone 1 Setup Verification")
    print("=" * 60)
    print()
    
    imports_ok = test_imports()
    agent_ok = test_agent()
    
    print()
    print("=" * 60)
    if imports_ok and agent_ok:
        print("✅ All tests passed! Milestone 1 setup is correct.")
        print("\nYou can now run: python app.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)
    print("=" * 60)


if __name__ == '__main__':
    main()

