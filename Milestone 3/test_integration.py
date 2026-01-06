"""
Integration test for Milestone 3
Tests the complete workflow: Parse → Generate → Execute
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from generators.test_generator import TestGenerator
from executors.test_executor import TestExecutor
from parsers.instruction_parser import InstructionParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_separator(title=""):
    """Print a visual separator"""
    print("\n" + "="*70)
    if title:
        print(f"  {title}")
        print("="*70)
    print()

def print_step(step_num, total_steps, description):
    """Print step information"""
    print(f"\n[{step_num}/{total_steps}] {description}")
    print("-" * 70)

def test_milestone_3_basic():
    """Test basic workflow with simple test case"""
    
    print_separator("MILESTONE 3: PLAYWRIGHT CODE GENERATION & EXECUTION")
    print("Testing basic workflow...")
    
    try:
        # Initialize components
        print_step(1, 5, "Initializing Components")
        
        llm = ChatOpenAI(
            model="gpt-4",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        print("✓ LLM initialized")
        
        parser = InstructionParser(llm)
        print("✓ Instruction Parser initialized")
        
        generator = TestGenerator(llm)
        print("✓ Test Generator initialized")
        
        executor = TestExecutor()
        print("✓ Test Executor initialized")
        
        # Sample test case
        print_step(2, 5, "Parsing Test Instructions")
        
        test_instruction = """
        1. Navigate to http://localhost:5000/test_gui.html
        2. Enter "John Doe" in the name field
        3. Enter "john@example.com" in the email field
        4. Click the submit button
        5. Verify success message appears
        """
        
        print("Test Instructions:")
        print(test_instruction)
        
        steps = parser.parse(test_instruction)
        print(f"\n✓ Parsed {len(steps)} test steps:")
        for i, step in enumerate(steps, 1):
            print(f"   {i}. {step.action.upper()}: {step.description}")
        
        # Generate Playwright code
        print_step(3, 5, "Generating Playwright Test Code")
        
        test_code = generator.generate(
            steps=steps,
            target_url="http://localhost:5000/test_gui.html"
        )
        
        print("✓ Test code generated successfully")
        print("\n--- Generated Code Preview (first 500 chars) ---")
        print(test_code[:500] + "..." if len(test_code) > 500 else test_code)
        print("--- End Preview ---")
        
        # Validate generated code
        validation = generator.validate_generated_code(test_code)
        print(f"\nCode Validation: {'✓ VALID' if validation['valid'] else '✗ INVALID'}")
        if validation['warnings']:
            print("Warnings:")
            for warning in validation['warnings']:
                print(f"  ⚠ {warning}")
        if validation['errors']:
            print("Errors:")
            for error in validation['errors']:
                print(f"  ✗ {error}")
        
        # Execute test
        print_step(4, 5, "Executing Test with Playwright")
        print("⏳ Running test in headless browser...")
        
        result = executor.execute(
            script=test_code,
            target_url="http://localhost:5000/test_gui.html"
        )
        
        # Display results
        print_step(5, 5, "Test Execution Results")
        
        print(f"Status: {'✓ PASSED' if result['success'] else '✗ FAILED'}")
        print(f"Test ID: {result['test_id']}")
        print(f"Execution Time: {result['execution_time']:.2f}s")
        print(f"Screenshots Captured: {len(result['screenshots'])}")
        print(f"Errors Encountered: {len(result['errors'])}")
        
        if result['message']:
            print(f"\nMessage: {result['message']}")
        
        if result['errors']:
            print("\n❌ Errors:")
            for i, error in enumerate(result['errors'], 1):
                print(f"\n  Error {i}:")
                print(f"    Type: {error.get('type', 'Unknown')}")
                print(f"    Message: {error.get('message', 'No message')}")
        
        if result['screenshots']:
            print("\n📸 Screenshots Saved:")
            for screenshot in result['screenshots']:
                print(f"  - {screenshot}")
        
        if result.get('logs'):
            print("\n📝 Execution Logs:")
            for log in result['logs'][-10:]:  # Show last 10 logs
                print(f"  {log}")
        
        print(f"\n📄 Full Report: {result.get('report_path', 'Not saved')}")
        print(f"📜 Test Script: {result.get('script_path', 'Not saved')}")
        
        print_separator("MILESTONE 3 TEST COMPLETED")
        
        return result['success']
        
    except Exception as e:
        print(f"\n❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_milestone_3_advanced():
    """Test advanced workflow with complex test case"""
    
    print_separator("MILESTONE 3: ADVANCED TEST CASE")
    
    try:
        # Initialize components
        llm = ChatOpenAI(model="gpt-4", temperature=0)
        parser = InstructionParser(llm)
        generator = TestGenerator(llm)
        executor = TestExecutor()
        
        # Complex test case
        test_instruction = """
        1. Navigate to http://localhost:5000/test_gui.html
        2. Wait for page to load completely
        3. Enter "Jane Smith" in the name input field
        4. Enter "jane.smith@example.com" in the email field
        5. Select "Option 2" from the dropdown menu
        6. Check the agreement checkbox
        7. Click the submit button
        8. Wait for 2 seconds
        9. Verify that success message contains "Thank you"
        10. Verify that the form is reset
        """
        
        print("Complex Test Instructions:")
        print(test_instruction)
        
        # Parse
        steps = parser.parse(test_instruction)
        print(f"\n✓ Parsed {len(steps)} steps")
        
        # Generate
        test_code = generator.generate(steps=steps, target_url="http://localhost:5000/test_gui.html")
        print("✓ Generated advanced test code")
        
        # Execute
        result = executor.execute(script=test_code, target_url="http://localhost:5000/test_gui.html")
        
        print(f"\n{'✓ PASSED' if result['success'] else '✗ FAILED'}")
        print(f"Execution Time: {result['execution_time']:.2f}s")
        
        return result['success']
        
    except Exception as e:
        print(f"\n❌ Advanced test failed: {str(e)}")
        return False

def test_error_handling():
    """Test error handling with intentionally failing test"""
    
    print_separator("MILESTONE 3: ERROR HANDLING TEST")
    
    try:
        llm = ChatOpenAI(model="gpt-4", temperature=0)
        parser = InstructionParser(llm)
        generator = TestGenerator(llm)
        executor = TestExecutor()
        
        # Test case with intentional error
        test_instruction = """
        1. Navigate to http://localhost:5000/nonexistent-page.html
        2. Click on element that doesn't exist
        3. Verify something impossible
        """
        
        print("Error Test Instructions:")
        print(test_instruction)
        
        steps = parser.parse(test_instruction)
        test_code = generator.generate(steps=steps, target_url="http://localhost:5000/nonexistent-page.html")
        result = executor.execute(script=test_code, target_url="http://localhost:5000/nonexistent-page.html")
        
        print(f"\n✓ Error handling test completed")
        print(f"Status: {'FAILED (Expected)' if not result['success'] else 'PASSED (Unexpected)'}")
        print(f"Errors Captured: {len(result['errors'])}")
        print(f"Screenshots Captured: {len(result['screenshots'])}")
        
        # This test passes if it captures errors properly
        return len(result['errors']) > 0 and len(result['screenshots']) > 0
        
    except Exception as e:
        print(f"\n❌ Error handling test exception: {str(e)}")
        return False

def run_all_tests():
    """Run all integration tests"""
    
    print("\n" + "🚀" * 35)
    print("  MILESTONE 3 - INTEGRATION TEST SUITE")
    print("🚀" * 35 + "\n")
    
    results = {
        "Basic Test": False,
        "Advanced Test": False,
        "Error Handling": False
    }
    
    # Run tests
    print("\n" + "📋 Running Test Suite..." + "\n")
    
    # Test 1: Basic
    results["Basic Test"] = test_milestone_3_basic()
    
    # Test 2: Advanced (optional - comment out if Flask server not ready)
    # results["Advanced Test"] = test_milestone_3_advanced()
    
    # Test 3: Error Handling
    results["Error Handling"] = test_error_handling()
    
    # Summary
    print_separator("TEST SUITE SUMMARY")
    
    passed = sum(results.values())
    total = len(results)
    
    print("Results:")
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Milestone 3 requirements met!")
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Review the output above.")
    
    print_separator()
    
    return passed == total

if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key in .env file")
        sys.exit(1)
    
    # Run tests
    success = run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)