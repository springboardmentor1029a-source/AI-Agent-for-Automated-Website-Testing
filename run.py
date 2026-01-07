"""Simple runner script for Milestone 1."""
import os
import sys

def main():
    """Run the Flask application."""
    print("=" * 60)
    print("Web Test Agent - Milestone 1")
    print("=" * 60)
    print("\nStarting Flask server...")
    print("Visit http://localhost:5000 to see the test page")
    print("Press Ctrl+C to stop the server\n")
    
    # Import and run the Flask app
    from app import app
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()

