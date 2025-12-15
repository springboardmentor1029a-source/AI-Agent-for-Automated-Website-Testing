# AI Powered Website Testing Agent

## Project Overview
This project is an AI-powered automated website testing agent developed as part of the Infosys Springboard Internship Program (Milestone 1).

The system allows a user to enter a website URL, which is then dynamically tested using Playwright automation. The backend is built using Flask, and a baseline LangGraph agent is implemented to process user inputs.

---

## Features
- Flask-based backend server
- Dynamic frontend using HTML, CSS, and JavaScript
- LangGraph baseline agent integration
- Automated website testing using Playwright
- Website load validation
- Page title extraction
- Screenshot capture
- Real-time test results displayed on UI

---

## Technologies Used
- Python
- Flask
- LangGraph
- Playwright
- HTML, CSS, JavaScript

---

## Project Structure
ai-webtest-agent/
│── app.py
│── langgraph_agent.py
│── browser_tester.py
│── requirements.txt
│
├── templates/
│ └── index.html
│
├── static/
│ └── screenshot.png
│
└── venv/

## Setup Instructions

### 1. Clone the repository

git clone <https://github.com/Jaksanishruthi/AI_Website_Testing_Agent>
cd ai-webtest-agent


### 2. Create virtual environment
python -m venv venv
venv\Scripts\activate


### 3. Install dependencies
pip install -r requirements.txt
playwright install


### 4. Run the application
python app.py


### 5. Access the application
Open browser and go to:
http://127.0.0.1:5000


---

## How It Works
1. User enters a website URL
2. Flask backend receives the request
3. Playwright opens the website and validates loading
4. Page title is extracted
5. Screenshot is captured
6. Results are returned dynamically to the UI

---

## Milestone Coverage
✔ Python environment setup  
✔ Dependency installation  
✔ Flask server initialization  
✔ Static HTML page  
✔ LangGraph agent configuration  
✔ Automated website testing (enhancement)  

---

## Future Enhancements
- Multiple test cases
- AI-based test generation
- Report generation
- Cloud deployment

---

## Author
Shruthi Jaksani  
Infosys Springboard Internship Program
