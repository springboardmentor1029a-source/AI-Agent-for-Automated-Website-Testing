# AI Agent for Automated Website Testing

This project is developed as part of the **Infosys Springboard Mentorship Program**.  
It demonstrates an AI-powered approach to automate website testing using natural language instructions.

---

## 📌 Project Overview

The system accepts test steps written in plain English, parses them into structured actions, intelligently decides the target website, and executes automated browser tests while capturing screenshots and generating reports.

---

## 🧩 Milestone-wise Implementation

### 🔹 Milestone 1: Problem Understanding
- Studied AI-based website testing concepts
- Understood automation workflows and testing challenges

### 🔹 Milestone 2: Instruction Parsing & Mapping
- Natural language instruction parsing
- Conversion into structured commands such as open, search, and click

### 🔹 Milestone 3: Automated Test Execution
- Implemented browser automation using Selenium
- Intelligent routing logic:
  - Product-related searches → Amazon
  - General/company searches → Google
- Automatic screenshot capture during execution

### 🔹 Milestone 4: Reporting
- Generated test execution report in JSON format
- Included screenshots, timestamps, and execution status

---

## 🛠️ Technologies Used
- Python
- Streamlit (Frontend Web Interface)
- Selenium (Browser Automation)

---

## ⚙️ Key Features
- Natural language test input
- Rule-based fallback mode for instruction understanding
- Intelligent website selection
- Screenshot-based evidence
- Automated test report generation

---

## 🚀 How to Run the Project (Local)

Run the Streamlit application using the command:

```bash
streamlit run app.py
http://localhost:8501

