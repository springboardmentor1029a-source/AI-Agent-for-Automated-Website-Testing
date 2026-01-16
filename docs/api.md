# AI Agent Web Tester API Documentation

## Overview
This API allows external applications to trigger automated web tests using natural language instructions.

## Base URL
`http://127.0.0.1:5000`

## Endpoints

### 1. Health Check
Checks if the backend is running.

- **URL**: `/`
- **Method**: `GET`
- **Response**:
    ```json
    {
        "status": "Backend running"
    }
    ```

### 2. Run Test
Executes a test based on natural language instructions.

- **URL**: `/run`
- **Method**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**:
    ```json
    {
        "instruction": "Open google.com\nSearch for Playwright\nVerify results"
    }
    ```
- **Response**:
    ```json
    {
        "summary": {
            "total_steps": 3,
            "passed": 3,
            "failed": 0,
            "pass_percentage": 100.0
        },
        "steps": [
            {
                "step_no": 1,
                "action": "OPEN",
                "target": "google.com",
                "status": "PASS"
            },
            ...
        ]
    }
    ```

### 3. Download PDF Report
Downloads the last execution report in PDF format.

- **URL**: `/download/pdf`
- **Method**: `GET`
- **Response**: PDF File

### 4. Download JSON Report
Downloads the last execution report in JSON format.

- **URL**: `/download/json`
- **Method**: `GET`
- **Response**: JSON File
