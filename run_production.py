"""
Run the Flask app without debug mode auto-reload
"""

from app import app
import os

if __name__ == '__main__':
    os.makedirs('reports', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    
    print("\n" + "="*60)
    print("[*] Yash AI Agent Starting (Production Mode)...")
    print("[*] Access: http://localhost:5000")
    print("[*] Dashboard: http://localhost:5000/dashboard")
    print("="*60 + "\n")
    
    # Run without debug to avoid file watching issues
    app.run(host='0.0.0.0', port=5000, debug=False)
