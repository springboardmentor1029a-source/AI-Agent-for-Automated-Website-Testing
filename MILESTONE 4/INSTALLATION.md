# E2E Testing Agent - Installation Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)

---

## 💻 System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.14+, or Linux
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum
- **Disk Space**: 500MB free space
- **Internet**: Required for browser downloads

### Recommended
- **Python**: 3.10+
- **RAM**: 8GB
- **Disk Space**: 2GB

---

## Installation Steps

### Step 1: Clone or Download the Project
```bash
# Clone the repository
git clone https://github.com/yourusername/kushal-ai-agent.git

# Navigate to project directory
cd kushal-ai-agent
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

### Step 4: Install Playwright Browsers
```bash
# Install Playwright browsers
playwright install chromium

# Or install all browsers
playwright install
```

### Step 5: Set Up Environment Variables

Create a `.env` file in the project root:
```bash
# .env file
OPENAI_API_KEY=your-openai-api-key-here
FLASK_ENV=development
FLASK_DEBUG=True
```

### Step 6: Run the Application
```bash
# Start the Flask server
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for LLM | Yes | None |
| `FLASK_ENV` | Flask environment | No | production |
| `FLASK_DEBUG` | Enable debug mode | No | False |
| `PORT` | Server port | No | 5000 |

### Optional Configuration

Edit `config.py` for advanced settings:
```python
# config.py
class Config:
    # Maximum retries for failed tests
    MAX_RETRIES = 3
    
    # Screenshot quality
    SCREENSHOT_QUALITY = 80
    
    # Test timeout (seconds)
    TEST_TIMEOUT = 60
    
    # History limit
    HISTORY_LIMIT = 100
```

---

##  Verification

### Test Installation
```bash
# Run health check
curl http://localhost:5000/health

# Expected response:
# {"status": "healthy", "agent_ready": true}
```

### Run Sample Test

1. Open browser: `http://localhost:5000`
2. Click "New Test"
3. Try this example:
```
   1. Navigate to https://example.com
   2. Verify page loads
```
4. Check results

---

##  Requirements File

Your `requirements.txt` should include:
```txt
# Core Dependencies
flask==3.0.0
playwright==1.40.0

# LangChain & AI
langchain==0.1.0
langchain-openai==0.0.2
langchain-core==0.1.0

# Utilities
python-dotenv==1.0.0
pytest==7.4.3
```

---

## 🐳 Docker Installation (Optional)
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install Playwright
RUN playwright install chromium
RUN playwright install-deps

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t e2e-testing-agent .
docker run -p 5000:5000 e2e-testing-agent
```

---

## 🔧 Troubleshooting Installation

### Issue: "playwright: command not found"
**Solution:**
```bash
pip install playwright
playwright install
```

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Permission denied" on macOS/Linux
**Solution:**
```bash
chmod +x app.py
```

### Issue: Port 5000 already in use
**Solution:**
```bash
# Use different port
export PORT=8000
python app.py
```

---

## 🔄 Updating

To update to the latest version:
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Update Playwright
playwright install chromium
```

---

## 🗑️ Uninstallation
```bash
# Deactivate virtual environment
deactivate

# Remove project directory
cd ..
rm -rf kushal-ai-agent
```

---

**Installation Complete!** 🎉

Proceed to the [User Guide](USER_GUIDE.md) to start creating tests.