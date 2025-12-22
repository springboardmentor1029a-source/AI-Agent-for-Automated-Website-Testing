# AI Agent for Automated Website Testing

An intelligent web application that uses **LangGraph**, **OpenAI GPT**, and **Playwright** to automate website testing. Simply describe what you want to test in plain English, and the AI agent will automatically generate and execute Playwright test scripts.

## 🚀 Features

- **AI-Powered**: Uses OpenAI GPT-3.5-turbo for natural language understanding
- **LangGraph Workflow**: Agent-based architecture for intelligent test orchestration
- **Playwright Automation**: Modern browser automation with Playwright
- **Code Generation**: Automatically generates Playwright scripts from natural language
- **Fallback Mode**: Works even without OpenAI API (keyword-based parsing)
- **Comprehensive Testing**: Images, links, forms, performance, and more
- **Real-time Results**: Get detailed test reports instantly

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask**: Web framework
- **LangGraph**: Agent workflow orchestration
- **LangChain**: LLM integration framework
- **OpenAI GPT-3.5-turbo**: Natural language understanding and code generation
- **Playwright**: Browser automation (replaces Selenium)

### Frontend
- **HTML5/CSS3/JavaScript**: Modern web interface
- **Font Awesome**: Icons

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key (optional - fallback mode works without it)
- Playwright browsers

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

### Option 1: Using the run script
```bash
chmod +x run.sh
./run.sh
```

### Option 2: Manual start
```bash
python app.py
```

Then open your browser and navigate to: `http://localhost:5000`

## 💡 Usage Examples

### Example 1: Search Test
```
Website URL: https://amazon.com
Test Instruction: "go to website and search for iphone 15"
```

### Example 2: Navigation Test
```
Website URL: https://example.com
Test Instruction: "navigate to the contact page and verify the form loads"
```

### Example 3: Comprehensive Test
```
Website URL: https://example.com
Test Instruction: "check all images, links, and forms on the homepage"
```

## 🏗️ Project Structure

```
infosys springboard/
├── app.py                 # Flask application
├── ai_agent.py           # AI agent with LangGraph + Playwright
├── requirements.txt      # Python dependencies
├── run.sh                # Run script
├── .env                  # Environment variables (API key)
├── .gitignore           # Git ignore file
├── README.md            # This file
├── templates/
│   └── index.html       # Main HTML template
└── static/
    ├── css/
    │   └── style.css    # Stylesheet
    └── js/
        └── main.js      # JavaScript functionality
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

### GET `/api/health`
Check API health status

## 🐛 Troubleshooting

### OpenAI API Quota Error
If you see quota errors:
1. Add billing to OpenAI account: https://platform.openai.com
2. Or use fallback mode (automatic)

### Playwright Not Installed
```bash
playwright install chromium
```

### Port Already in Use
Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 📝 License

This project is for educational purposes.

## 📧 Support

For issues or questions, check the error messages in the application or review the code.

---

**Built with**: LangGraph + OpenAI GPT + Playwright + Flask
