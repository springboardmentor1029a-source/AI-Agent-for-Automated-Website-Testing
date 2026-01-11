# E2E Testing Agent - Troubleshooting Guide

##  Table of Contents
1. [Common Issues](#common-issues)
2. [Installation Problems](#installation-problems)
3. [Test Execution Errors](#test-execution-errors)
4. [Browser Issues](#browser-issues)
5. [Performance Problems](#performance-problems)
6. [FAQ](#faq)

---

## 🔧 Common Issues

### Issue: Server Won't Start

**Symptoms:**
- `Address already in use` error
- Flask doesn't start

**Solutions:**
```bash
# Check if port 5000 is in use
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process or use different port
export PORT=8000
python app.py
```

---

### Issue: Tests Fail Immediately

**Symptoms:**
- All tests fail instantly
- "Browser not found" error

**Solutions:**
```bash
# Reinstall Playwright browsers
playwright install chromium

# Or install all browsers
playwright install

# Verify installation
playwright --version
```

---

### Issue: "ModuleNotFoundError"

**Symptoms:**
```
ModuleNotFoundError: No module named 'playwright'
```

**Solution:**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

---

### Issue: OpenAI API Key Not Found

**Symptoms:**
```
Error: OPENAI_API_KEY not found
```

**Solution:**
```bash
# Create .env file
echo "OPENAI_API_KEY=your-key-here" > .env

# Or export environment variable
export OPENAI_API_KEY="your-key-here"
```

---

## 🔨 Installation Problems

### Python Version Issues

**Problem:** "Python 3.8 or higher required"

**Solution:**
```bash
# Check Python version
python --version

# Install Python 3.10+
# Visit: https://www.python.org/downloads/

# Or use pyenv
pyenv install 3.11
pyenv local 3.11
```

---

### Pip Installation Fails

**Problem:** Package installation errors

**Solution:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Clear cache
pip cache purge

# Try installing again
pip install -r requirements.txt
```

---

### Virtual Environment Issues

**Problem:** Can't activate virtual environment

**Solution:**
```bash
# Delete and recreate
rm -rf .venv
python -m venv .venv

# Activate
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate  # Windows
```

---

## 🧪 Test Execution Errors

### Timeout Errors

**Problem:** Tests timeout frequently

**Solutions:**

1. **Increase timeout in config:**
```python
# config.py
TEST_TIMEOUT = 120  # Increase to 120 seconds
```

2. **Add explicit waits:**
```
1. Navigate to URL
2. Wait for page to load completely  ← Add this
3. Click button
```

3. **Check internet connection:**
```bash
ping google.com
```

---

### Element Not Found Errors

**Problem:** "Element not found" or "Selector failed"

**Solutions:**

1. **Add wait steps:**
```
1. Navigate to page
2. Wait for button to appear  ← Add explicit wait
3. Click the button
```

2. **Use more specific descriptions:**
```
 "Click the blue submit button with text 'Submit'"
 "Click button"
```

3. **Check if element is in iframe:**
```
The element might be inside an iframe.
Try: "Switch to iframe and click button"
```

---

### Screenshot Not Captured

**Problem:** Screenshots missing from reports

**Solutions:**
```bash
# Check outputs directory exists
ls -la outputs/screenshots/

# Create if missing
mkdir -p outputs/screenshots

# Check permissions
chmod 755 outputs/screenshots
```

---

##  Browser Issues

### Chromium Won't Launch

**Problem:** Browser launch fails

**Solutions:**
```bash
# Reinstall browsers
playwright install chromium --force

# Check system dependencies (Linux)
sudo playwright install-deps

# Try with different browser
playwright install firefox
```

---

### Headless Mode Issues

**Problem:** Tests fail in headless but work with UI

**Solution:**

Enable headed mode for debugging:
```python
# In test_executor.py
browser = playwright.chromium.launch(
    headless=False  # Change to False
)
```

---

### SSL Certificate Errors

**Problem:** SSL/HTTPS errors

**Solution:**
```python
# In test_executor.py
context = browser.new_context(
    ignore_https_errors=True  # Add this
)
```

---

## ⚡ Performance Problems

### Slow Test Execution

**Problem:** Tests take too long

**Solutions:**

1. **Reduce waits:**
```
 Wait 10 seconds
 Wait for element to appear
```

2. **Use faster selectors:**
```
 Use ID selectors: #submit-button
Complex CSS: div > ul > li:nth-child(3)
```

3. **Optimize network:**
```python
# Block unnecessary resources
context = browser.new_context(
    bypass_csp=True,
    block_resources=['image', 'stylesheet']
)
```

---

### Memory Issues

**Problem:** High memory usage

**Solutions:**
```bash
# Limit concurrent tests
export MAX_WORKERS=2

# Clear old reports
python -c "from executors.test_executor import TestExecutor; TestExecutor().cleanup_old_files(days=7)"

# Restart server periodically
```

---

### Dashboard Loading Slow

**Problem:** Dashboard takes long to load

**Solutions:**

1. **Limit history:**
```python
# config.py
HISTORY_LIMIT = 50  # Reduce from 100
```

2. **Clear browser cache:**
```
Clear browser cache and reload
```

3. **Optimize queries:**
```bash
# Clear old data
rm -rf outputs/reports/*_old.json
```

---

##  FAQ

### Q: Why do my tests fail intermittently?

**A:** This is usually due to:
- Network latency
- Dynamic content loading
- Timing issues

**Solutions:**
- Add explicit wait steps
- Use retry logic (already built-in)
- Increase timeouts

---

### Q: Can I run tests on mobile devices?

**A:** Yes, configure viewport:
```python
context = browser.new_context(
    viewport={'width': 375, 'height': 667},  # iPhone size
    user_agent='Mozilla/5.0 iPhone...'
)
```

---

### Q: How do I debug failing tests?

**A:** 
1. Enable headed mode (headless=False)
2. Add `page.pause()` in test code
3. Check screenshots in outputs folder
4. Review execution logs in report

---

### Q: Tests work locally but fail in CI/CD

**A:**
- Install system dependencies: `playwright install-deps`
- Use headless mode
- Increase timeouts
- Check network access

---

### Q: How do I test authentication flows?

**A:** Include login steps:
```
1. Navigate to login page
2. Enter username in email field
3. Enter password in password field
4. Click login button
5. Wait for dashboard to load
6. Verify user is logged in
```

---

## Debug Mode

Enable verbose logging:
```bash
# Set debug environment variables
export FLASK_DEBUG=1
export PLAYWRIGHT_DEBUG=1

# Run with verbose output
python app.py --debug
```

---

## 📞 Getting Help

If you can't resolve an issue:

1. Check execution logs in `outputs/reports/`
2. Review screenshots in `outputs/screenshots/`
3. Enable debug mode
4. Check [GitHub Issues](https://github.com/yourusername/repo/issues)
5. Contact support with:
   - Error message
   - Test instructions
   - Screenshots
   - System info

---

## 🔍 Diagnostic Commands
```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check Playwright installation
playwright --version

# Test Playwright
playwright codegen example.com

# Check system resources
top  # macOS/Linux
taskmgr  # Windows

# Check logs
tail -f outputs/test.log
```

---

**Still having issues?** 

Create an issue with:
- Full error message
- Steps to reproduce
- System information
- Screenshots

We're here to help! 