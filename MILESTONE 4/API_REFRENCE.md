# E2E Testing Agent - API Reference

##  Table of Contents
1. [Overview](#overview)
2. [Base URL](#base-url)
3. [Authentication](#authentication)
4. [Endpoints](#endpoints)
5. [Data Models](#data-models)
6. [Error Codes](#error-codes)
7. [Examples](#examples)

---

## 🌐 Overview

The E2E Testing Agent provides a RESTful API for programmatic access to test execution and management.

### API Version
Current version: `v1.0`

### Content Type
All requests and responses use `application/json`

---

## 🔗 Base URL
```
http://localhost:5000/api
```

---

##  Authentication

Currently, no authentication is required for local deployment.

For production deployment, add API key authentication:
```http
Authorization: Bearer YOUR_API_KEY
```

---

## 📡 Endpoints

### 1. Health Check

Check if the server is running.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "agent_ready": true,
  "version": "1.0.0"
}
```

---

### 2. Run Test

Execute a new test.

**Endpoint:** `POST /api/test`

**Request Body:**
```json
{
  "instruction": "1. Go to https://example.com\n2. Verify page loads",
  "target_url": "https://example.com"
}
```

**Response:**
```json
{
  "success": true,
  "test_id": "20260106_145623",
  "message": "Test completed successfully",
  "execution_time": 3.45,
  "screenshots": [
    "/screenshots/success_20260106_145623.png"
  ],
  "report_path": "/reports/report_20260106_145623.json"
}
```

---

### 3. Parse Instructions

Parse test instructions without executing.

**Endpoint:** `POST /api/parse`

**Request Body:**
```json
{
  "instruction": "1. Click button\n2. Verify result",
  "target_url": "https://example.com"
}
```

**Response:**
```json
{
  "success": true,
  "steps": [
    {
      "action": "click",
      "description": "Click button"
    },
    {
      "action": "verify",
      "description": "Verify result"
    }
  ]
}
```

---

### 4. Get Test Report

Retrieve a specific test report.

**Endpoint:** `GET /api/report/:test_id`

**Parameters:**
- `test_id` (string): Test identifier

**Response:**
```json
{
  "success": true,
  "report": {
    "test_id": "20260106_145623",
    "success": true,
    "execution_time": 3.45,
    "target_url": "https://example.com",
    "timestamp": "2026-01-06T14:56:23",
    "screenshots": [...],
    "errors": [],
    "logs": [...]
  }
}
```

---

### 5. List Reports

Get list of all test reports.

**Endpoint:** `GET /api/reports`

**Query Parameters:**
- `limit` (integer, optional): Number of reports (default: 10)
- `status` (string, optional): Filter by status (passed/failed)

**Response:**
```json
{
  "success": true,
  "reports": [
    {
      "test_id": "20260106_145623",
      "success": true,
      "timestamp": "2026-01-06T14:56:23",
      "execution_time": 3.45
    }
  ],
  "total": 25
}
```

---

### 6. Get Statistics

Retrieve test statistics.

**Endpoint:** `GET /api/statistics`

**Response:**
```json
{
  "success": true,
  "statistics": {
    "total_tests": 50,
    "passed_tests": 45,
    "failed_tests": 5,
    "success_rate": 90.0,
    "average_execution_time": 4.23
  }
}
```

---

### 7. Get Success Rate Trend

Get success rate trend over time.

**Endpoint:** `GET /api/statistics/trend`

**Query Parameters:**
- `days` (integer, optional): Number of days (default: 7)

**Response:**
```json
{
  "success": true,
  "trend": [
    {
      "date": "2026-01-05",
      "total_tests": 10,
      "passed_tests": 9,
      "success_rate": 90.0
    }
  ]
}
```

---

### 8. Clear History

Clear all test history.

**Endpoint:** `POST /api/clear-history`

**Response:**
```json
{
  "success": true,
  "message": "History cleared successfully",
  "deleted_count": 50
}
```

---

## 📊 Data Models

### TestResult
```json
{
  "test_id": "string",
  "success": "boolean",
  "message": "string",
  "execution_time": "number",
  "target_url": "string",
  "timestamp": "string (ISO 8601)",
  "screenshots": ["string"],
  "errors": [
    {
      "type": "string",
      "message": "string",
      "traceback": "string"
    }
  ],
  "logs": ["string"]
}
```

### TestStep
```json
{
  "action": "string",
  "description": "string",
  "selector": "string (optional)",
  "value": "string (optional)"
}
```

### Statistics
```json
{
  "total_tests": "integer",
  "passed_tests": "integer",
  "failed_tests": "integer",
  "success_rate": "number",
  "average_execution_time": "number"
}
```

---

##  Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error |

### Error Response Format
```json
{
  "success": false,
  "error": "Error message here",
  "code": "ERROR_CODE"
}
```

---

##  Examples

### Python Example
```python
import requests

# Run a test
response = requests.post('http://localhost:5000/api/test', json={
    'instruction': '1. Go to https://example.com\n2. Verify page loads',
    'target_url': 'https://example.com'
})

result = response.json()
print(f"Test ID: {result['test_id']}")
print(f"Success: {result['success']}")
```

### JavaScript Example
```javascript
// Run a test
fetch('http://localhost:5000/api/test', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    instruction: '1. Go to https://example.com\n2. Verify page loads',
    target_url: 'https://example.com'
  })
})
.then(res => res.json())
.then(data => {
  console.log('Test ID:', data.test_id);
  console.log('Success:', data.success);
});
```

### cURL Example
```bash
# Run a test
curl -X POST http://localhost:5000/api/test \
  -H "Content-Type: application/json" \
  -d '{
    "instruction": "1. Go to https://example.com\n2. Verify page loads",
    "target_url": "https://example.com"
  }'
```

---

## Rate Limiting

Currently no rate limiting is enforced for local deployment.

For production:
- 100 requests per minute per IP
- 1000 requests per hour per API key

---

**API Version**: 1.0.0  
**Last Updated**: January 2026