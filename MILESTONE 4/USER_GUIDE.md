# E2E Testing Agent - User Guide

## 📋 Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Creating Tests](#creating-tests)
4. [Viewing Results](#viewing-results)
5. [Dashboard Features](#dashboard-features)
6. [Best Practices](#best-practices)
7. [FAQ](#faq)

---

## 🎯 Introduction

The E2E Testing Agent is an AI-powered automated testing tool that allows you to create end-to-end tests using natural language instructions.

### Key Features
-  Write tests in plain English
-  Automatic Playwright code generation
-  Headless browser execution
-  Detailed reports with screenshots
-  Test history tracking
- Error recovery and retry logic

---

##  Getting Started

### Accessing the Application

1. Open browser and go to `http://localhost:5000`
2. You'll see the main dashboard

### Creating Your First Test

1. Click **"New Test"** button
2. Enter test instructions in plain English
3. Provide target website URL
4. Click **"Run Test"**

**Example:**
```
1. Navigate to https://example.com
2. Verify page title contains "Example"
3. Click "More information" link
```

---

## 📝 Creating Tests

### Writing Effective Test Instructions

#### Good Example:
```
1. Go to https://www.google.com
2. Wait for search box to appear
3. Type "Playwright testing" in the search box
4. Click the search button
5. Wait for results to load
6. Verify search results are displayed
```

#### Supported Actions:
- **Navigate**: "Go to URL", "Navigate to homepage"
- **Click**: "Click the button", "Click submit"
- **Type**: "Enter text", "Type in field"
- **Wait**: "Wait for element", "Wait 2 seconds"
- **Verify**: "Check that", "Verify message appears"

### Tips for Better Tests
- Be specific about element descriptions
- Include wait steps for dynamic content
- Add verification steps
- Break complex tests into smaller steps

---

## 📊 Viewing Results

### Test Report Structure

1. **Header**
   - Test ID
   - Status (Passed/Failed)
   - Execution time

2. **Summary**
   - Target URL
   - Timestamp
   - Screenshot count

3. **Screenshots**
   - Visual evidence of execution
   - Click to view full size

4. **Errors** (if failed)
   - Error type
   - Error message
   - Recovery suggestions

5. **Logs**
   - Step-by-step execution details

---

## 🎛️ Dashboard Features

### Statistics Cards
- **Total Tests**: All tests run
- **Passed/Failed**: Success metrics
- **Success Rate**: Pass percentage
- **Avg Execution**: Average time

### Test History Table
- View recent tests
- Filter by status
- Sort by date/duration
- Quick access to reports

### Charts
- Success rate visualization
- Test trend over time
- Execution time analysis

---

## 💡 Best Practices

### 1. Write Clear Instructions
```
"Click the blue submit button at the bottom"
"Click something"
```

### 2. Add Wait Conditions
```
 "Wait for success message to appear"
 Immediate verification without waiting
```

### 3. Use Specific Selectors
```
"Enter 'john@example.com' in the email field"
"Type in the box"
```

### 4. Include Verification Steps
```
 "Verify dashboard title is 'Welcome'"
 Just clicking without verification
```

### 5. Handle Dynamic Content
- Add waits for loading states
- Verify elements before interaction
- Use retry logic for flaky elements

---

## ❓ FAQ

**Q: How long do tests take to run?**
A: Most tests complete in 3-10 seconds depending on website speed.

**Q: Can I test websites that require login?**
A: Yes, include login steps in your test instructions.

**Q: What browsers are supported?**
A: Tests run in Chromium (headless) via Playwright.

**Q: How many tests can I run?**
A: Unlimited! History stores the last 100 tests.

**Q: Can I export test results?**
A: Yes, click "Export Data" on the dashboard.

**Q: What if my test fails?**
A: Check the error message and screenshots. The system provides recovery suggestions.

---

## 📞 Support

For issues or questions:
- Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
- Review the [API Reference](API_REFERENCE.md)
- Submit feedback through the dashboard

---

**Last Updated**: January 2026
**Version**: Milestone 4