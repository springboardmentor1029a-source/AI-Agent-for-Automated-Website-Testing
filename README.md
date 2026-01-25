🤖 AI Agent for Automated Website Testing

An intelligent web-based application that automates website testing using natural language instructions. Users simply describe what they want to test in plain English, and the AI agent automatically generates and executes Playwright test scripts.

This project was developed as part of the Infosys Springboard Virtual Internship and demonstrates practical usage of AI agents, Large Language Models, and browser automation.

🚀 Features

Natural language based website testing

AI agent workflow using LangGraph

Automatic Playwright script generation

Headless browser execution

Fallback mode (works without OpenAI API key)

Supports testing of search, navigation, forms, images, and links

Real-time execution results with basic performance metrics

🧰 Technology Stack

Backend

Python 3.8+

Flask

LangGraph

LangChain

OpenAI GPT-3.5-turbo

Playwright

Frontend

HTML5

CSS3

JavaScript

Font Awesome

📋 Prerequisites

Python 3.8 or higher

Playwright browsers (Chromium)

OpenAI API key (optional – fallback mode supported)

⚙️ Installation and Setup

Clone the repository and navigate into the project directory. Create a virtual environment (recommended), activate it, and install the required dependencies. After installing dependencies, install Playwright browsers.

If you want AI-powered instruction parsing, create a .env file and add your OpenAI API key. The application will still work without an API key using fallback mode.

▶️ Running the Application

You can run the application in two ways.

Flask Web Application
Start the Flask server and open the application in your browser at http://localhost:5001.

Streamlit Application
Run the Streamlit app and access it at http://localhost:8501.

🧪 Usage Examples

Search Test
Website URL: https://amazon.com

Instruction: go to website and search for iphone 15

Navigation Test
Instruction: navigate to the contact page and verify the form loads

Comprehensive Website Test
Instruction: check all images, links, and forms on the homepage

🗂️ Project Structure

The project follows a clean and modular structure with separate files for the Flask backend, Streamlit interface, AI agent logic, frontend templates, static assets, and configuration files.

⚙️ How It Works

The user provides a website URL and a natural language instruction.
The LangGraph-based AI agent processes the instruction.
The instruction is parsed using OpenAI GPT or a fallback keyword-based parser.
Playwright test scripts are generated dynamically.
Tests are executed in a headless browser.
Execution results and performance metrics are returned to the user.

🔄 Fallback Mode

If the OpenAI API key is missing or quota is exceeded, the system automatically switches to fallback mode. In this mode, keyword-based parsing is used to generate Playwright scripts without making any API calls.

📡 API Endpoints

POST /api/run-test
Runs a test on the provided website using the given instruction.

GET /api/health
Checks the health status of the application.

🐞 Troubleshooting

If Playwright is not installed, install the Chromium browser.
If the port is already in use, change the port number in the Flask application.
If OpenAI quota is exceeded, continue using fallback mode.

📜 License

This project is created for educational purposes only.

🙌 Acknowledgements

Built using LangGraph, OpenAI GPT, Playwright, Flask, and Streamlit.

