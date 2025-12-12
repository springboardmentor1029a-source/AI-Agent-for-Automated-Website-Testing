# 🚀 Quick Start Guide - Yash AI Agent

## Installation

Run the setup script to install all dependencies:

```powershell
.\setup.ps1
```

This will:
- Install Python dependencies
- Install Playwright browsers
- Create .env configuration file

## Manual Installation (Alternative)

If you prefer manual installation:

```powershell
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

## Running the Application

Start the Flask server:

```powershell
python app.py
```

The application will be available at:
- Main Application: http://localhost:5000
- Test Site: http://localhost:5000/test_site
- Dashboard: http://localhost:5000/dashboard

## Using the AI Agent

1. **Open the Dashboard** - Navigate to http://localhost:5000
2. **Wait for Landing Page** - Enjoy the 5-second animated intro with the Yash AI Agent logo
3. **Click "Start Testing Now"** to access the dashboard
4. **Enter Test Instructions** in natural language, for example:
   ```
   Navigate to http://localhost:5000/test_site
   Fill the email field with "test@example.com"
   Fill the password field with "password123"
   Click the "Login" button
   Verify that the page contains "Login successful"
   ```
5. **Click "Run Test"** and watch the AI agent work!
6. **View Results** - See detailed pass/fail status and generated Playwright code

## Example Test Instructions

### Login Test
```
Navigate to http://localhost:5000/test_site
Fill the email field with "test@example.com"
Fill the password field with "password123"
Click the Login button
Check that the page contains "Login successful"
```

### Form Submission Test
```
Navigate to http://localhost:5000/test_site
Fill the name field with "John Doe"
Fill the email field with "john@example.com"
Click the submit button
Verify success message appears
```

### Navigation Test
```
Navigate to http://localhost:5000/test_site
Click on the About link
Wait 2 seconds
Click on the Home link
```

## Features

✅ Natural Language Processing - Write tests in plain English
✅ AI-Powered Code Generation - Automatic Playwright script creation
✅ Real-time Execution - See results instantly
✅ Beautiful UI - Modern, animated interface
✅ Detailed Reports - Pass/fail status with error details
✅ Code Export - Copy generated Playwright code

## API Endpoints

- `POST /api/test` - Run a test
- `GET /api/reports` - List all reports
- `GET /api/reports/<id>` - Get specific report

## Troubleshooting

### Playwright Issues
If Playwright fails to run:
```powershell
playwright install chromium --force
```

### Port Already in Use
If port 5000 is busy, edit `app.py` and change the port:
```python
app.run(debug=True, port=5001, host='0.0.0.0')
```

### API Key Issues
The system works without a Gemini API key using rule-based parsing. For better accuracy with complex tests, ensure your `.env` file has:
```
GEMINI_API_KEY=your_actual_key_here
```

## Tech Stack

- **Backend**: Python, Flask, LangGraph
- **Browser Automation**: Playwright
- **AI**: Google Gemini, LangChain
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

## Project Structure

```
AI AGENT/
├── app.py                  # Flask application
├── agent/                  # AI Agent modules
│   ├── __init__.py
│   ├── parser.py          # Instruction parser
│   ├── code_generator.py  # Playwright code generator
│   ├── executor.py        # Test executor
│   └── workflow.py        # LangGraph workflow
├── static/                # Frontend assets
│   ├── css/
│   │   ├── landing.css
│   │   └── dashboard.css
│   └── js/
│       ├── landing.js
│       └── dashboard.js
├── templates/             # HTML templates
│   ├── index.html         # Landing page
│   ├── dashboard.html     # Main dashboard
│   └── test_site.html     # Sample test site
├── reports/               # Generated test reports
├── requirements.txt       # Python dependencies
├── setup.ps1             # Installation script
└── README.md             # Documentation
```

## Support

For issues or questions, check the console output for detailed error messages.

---

**Created by Yash** | Powered by AI 🤖
