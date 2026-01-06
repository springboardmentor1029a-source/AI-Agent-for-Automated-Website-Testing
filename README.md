# AI Agent for Automated Website Testing – Milestone 2

## 📌 Milestone Overview
This milestone focuses on converting natural language test instructions into structured test actions using a LangGraph-based workflow.

---

## 🎯 Objectives Achieved
- Built an Instruction Parser to interpret natural language test cases.
- Converted parsed instructions into structured test actions.
- Connected Instruction Parser to a Code Generator using LangGraph.
- Demonstrated basic test case conversion output via a Flask API.

---

## 🧠 Architecture Flow

User Input (Natural Language)  
⬇  
Instruction Parser (`instruction_parser.py`)  
⬇  
Structured Actions  
⬇  
Workflow Generator (`workflow.py`)  
⬇  
LangGraph Agent (`agent.py`)  
⬇  
Output Response (JSON)

---

## 📂 Project Structure (Milestone 2)
