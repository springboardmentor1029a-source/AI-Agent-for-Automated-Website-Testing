#!/bin/bash

# Navigate to project directory
cd "c:\AI AGENT"

# Initialize git repository
git init

# Configure git
git config user.name "Yashaswini"
git config user.email "yashaswini.v21@example.com"

# Stage all files
git add .

# First commit
git commit -m "Initial commit: AI Agent for Automated Website Testing

- Natural language test instruction parsing
- Multi-browser support (Chrome, Firefox, Edge)
- Automated Playwright code generation
- Visual test execution with screenshots
- Modern dashboard with real-time results
- PDF and JSON report export
- Covers Infosys Springboard Milestones 1, 2, and 3"

# Add your personal repository as remote
git remote add origin https://github.com/Yashaswini-V21/Ai-Agent-To-Test-Websites-Automatically-Using-Natural-Language.git

# Create and push to Yashaswini-branch (NOT main)
git checkout -b Yashaswini-branch
git push -u origin Yashaswini-branch

# Add mentor's repository as second remote
git remote add mentor https://github.com/springboardmentor1029a-source/AI-Agent-for-Automated-Website-Testing.git

# Push to mentor's Yashaswini-branch
git push mentor Yashaswini-branch

echo "✓ Successfully pushed to both repositories on Yashaswini-branch!"
