# 🤖 AI Agent for Automated Website Testing

An intelligent web-based application that automates website testing using natural language instructions. Users can describe what they want to test in plain English, and the AI agent automatically generates and executes Playwright test scripts.

This project is developed as part of the Infosys Springboard Virtual Internship and demonstrates the use of AI agents, LLMs, and browser automation.

---

## 🚀 Features

- Natural language based website testing  
- AI agent workflow using LangGraph  
- Automatic Playwright script generation  
- Headless browser execution  
- Fallback mode (works without OpenAI API key)  
- Tests search, navigation, forms, images, and links  
- Real-time test execution results and performance metrics  

---

## 🧰 Technology Stack

### Backend
- Python 3.8+
- Flask
- LangGraph
- LangChain
- OpenAI GPT-3.5-turbo
- Playwright

### Frontend
- HTML5
- CSS3
- JavaScript
- Font Awesome

---

## 📋 Prerequisites

- Python 3.8 or higher  
- Playwright browsers (Chromium)  
- OpenAI API key (optional – fallback mode supported)

---

## ⚙️ Installation

### Clone the Repository
```bash
git clone <your-github-repository-url>
cd infosys-springboard
Create Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt
playwright install chromium
(Optional) Set OpenAI API Key

Create a .env file:

OPENAI_API_KEY=your_api_key_here

Note: The application works even without an OpenAI API key using fallback mode.

▶️ Running the Application
Flask Web Application
python app.py
Open in browser:

http://localhost:5001
Streamlit Application
streamlit run streamlit_app.py
Open in browser:

http://localhost:8501
🧪 Usage Examples
Search Test

Website URL:

https://amazon.com
Test Instruction:

go to website and search for iphone 15
Navigation Test
navigate to the contact page and verify the form loads
Comprehensive Test
check all images, links, and forms on the homepage
⚙️ How It Works

User Instruction
↓
LangGraph AI Agent
↓
Instruction Parsing (GPT / Fallback)
↓
Playwright Script Generation
↓
Headless Browser Execution
↓
Test Results and Performance Metrics
