# AI Agent for Automated Website Testing

A powerful, web-based dashboard for orchestrating AI agents. This project features a real-time terminal, live browser screenshots, and a clean PDF reporting engine that intelligently separates UI elements from the final document.

## 🚀 Key Features

-Live Command Console: Send natural language instructions to an autonomous agent.
-Real-time System Logs: Monitor the agent's thought process and execution steps via a neon-styled terminal.
-Visual Proof: View live screenshots of the browser actions directly in the dashboard summary.
-Smart PDF Export: Generate professional, high-contrast PDF reports. The system automatically strips out UI-only elements (like screenshots) to keep reports formal and concise.
-Dark Mode Interface: A sleek, developer-focused UI built with Bootstrap and custom CSS.

## 🛠️ Technology Stack
-Backend: Python, Flask, LangChain/LangGraph.
-Automation: Playwright (for browser orchestration).
-Frontend: HTML5, CSS3 (Custom Neon Theme), JavaScript (Async/Await).
-PDF Engine: html2pdf.js with DOM cloning logic.

### Backend
- **Python 3.8+**: Core programming language
- **Flask**: Web framework
- **LangGraph**: Agent workflow orchestration
- **LangChain**: LLM integration framework
- **OpenAI GPT-3.5-turbo**: Natural language understanding and code generation
- **Playwright**: Browser automation (replaces Selenium)

### Frontend
- **HTML5/CSS3/JavaScript**: Modern web interface

## 🚀 Getting Started
1. Prerequisites
Python 3.10+
Node.js (for Playwright browser binaries)

## 🔧 Installation

1. **Clone or download the project**
   ```bash
   cd "infosys springboard"
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

4. **Set up OpenAI API key (optional)**
   Create a `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   
   **Note**: The project works in fallback mode even without API key!

## 🚀 Running the Application
```bash
python app.py
```
Then open your browser and navigate to: `http://localhost:5000`


## 🏗️ Project Structure

```
infosys springboard/
├── app.py                 # Flask server and API endpoints
├── agent_graph.py         #The logic for the agent state machine(Execuotor and Reporter nodes).
├── requirements.txt       # Python dependencies
├── state.py               #Typed definitions for the Agent'state
├── .env                   # Environment variables (API key)
├── .gitignore             # Git ignore file
├── README.md              # This file
├── templates/
│   └── index.html         # Main HTML template
└── static/
    ├── css/
    │   └── style.css      # Stylesheet
    └── js/
        └── main.js        # JavaScript functionality
```

## 🔍 How It Works

1. **User Input**: User provides website URL and natural language instruction
2. **LangGraph Agent**: Orchestrates the testing workflow
3. **Instruction Parsing**: OpenAI GPT parses natural language (or fallback parser)
4. **Code Generation**: GPT generates Playwright test scripts
5. **Execution**: Playwright executes tests in headless browser
6. **Reporting**: Comprehensive test results with metrics

## 🎯 Architecture

```
Natural Language Instruction
    ↓
LangGraph Agent (Parse with GPT)
    ↓
Generate Playwright Scripts
    ↓
Execute in Headless Browser
    ↓
Generate Test Report
```

## 🔄 Fallback Mode

If OpenAI API is unavailable (quota exceeded, no API key, etc.), the system automatically switches to fallback mode:
- Uses keyword-based parsing
- Generates Playwright code directly
- Works without any API calls

## 📊 API Endpoints

### POST `/api/run-test`
Run a test on a website

**Request:**
```json
{
  "websiteUrl": "https://amazon.com",
  "testInstruction": "search for iphone 15",
  "browser": "chrome"
}
```

**Response:**
```json
{
  "status": "success",
  "websiteUrl": "https://amazon.com",
  "testInstruction": "search for iphone 15",
  "results": ["Test executed successfully"],
  "performance": {
    "loadTime": 2931,
    "pageSize": "885.04"
  }
}
```
💡 How the PDF Generation Works
-To maintain a "Dark Mode" website but generate "Light Mode" PDFs, the system uses a Cloning Technique:
-Clone: The JavaScript creates a hidden "stunt double" of the report.
-Filter: It identifies elements with the .screenshot-ui-only class and removes them.
-Transform: It forces all text to black and backgrounds to white.
-Render: html2pdf captures this cleaned version, leaving your live dashboard untouched.

## 📝 License

This project is for educational purposes.

## 📧 Support

For issues or questions, check the error messages in the application or review the code.

---

**Built with**: LangGraph + OpenAI GPT + Playwright + Flask
