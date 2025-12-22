#!/bin/bash

# AI Agent Website Testing - Run Script

echo "🚀 Starting AI Agent for Website Testing..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
if ! playwright install chromium 2>/dev/null; then
    echo "⚠️  Playwright browser installation had issues, but continuing..."
fi

# Check for OpenAI API key
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Please set OPENAI_API_KEY in .env file"
else
    echo "✅ Environment variables loaded from .env"
fi

# Run the application
echo "✅ Starting Flask application with LangGraph + OpenAI + Playwright..."
echo "📍 Server will be available at http://localhost:5000"
echo ""
python app.py

