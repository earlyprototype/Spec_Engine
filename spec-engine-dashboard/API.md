# SPEC Engine Dashboard - API Documentation

**Version:** 1.0  
**Base URL:** `http://localhost:5000`  
**Last Updated:** 2 January 2026

---

## Table of Contents

1. [Authentication](#authentication)
2. [DNA Profile Endpoints](#dna-profile-endpoints)
3. [SPEC Endpoints](#spec-endpoints)
4. [Execution Endpoints](#execution-endpoints)
5. [File Endpoints](#file-endpoints)
6. [WebSocket Events](#websocket-events)
7. [Error Responses](#error-responses)

---

## Authentication

**Current Version:** No authentication (single-user local deployment)

For multi-user deployments, add JWT or session-based authentication to all endpoints.

---

## DNA Profile Endpoints

### List DNA Profiles

**GET** `/api/dna`

Returns all DNA profiles from file system and database.

**Response:**
```json
{
  "profiles": [
    {
      "id": "uuid",
      "dnaCode": "ATGCTCGA",
      "projectName": "My Project",
      "testing": "standard",
      "risk": "medium",
      "autonomy": "high",
      "customTools": "React, Node.js",
      "constraints": "Must support offline mode",
      "createdAt": "2026-01-02T10:00:00.000Z",
      "updatedAt": "2026-01-02T10:00:00.000Z",
      "specCount": 3
    }
  ]
}
```

### Get DNA Profile

**GET** `/api/dna/:dnaCode`

Returns specific DNA profile details.

**Parameters:**
- `dnaCode` (path) - 8-character DNA code (e.g., ATGCTCGA)

**Response:**
```json
{
  "id": "uuid",
  "dnaCode": "ATGCTCGA",
  "projectName": "My Project",
  "testing": "standard",
  "risk": "medium",
  "autonomy": "high",
  "customTools": "React, Node.js",
  "constraints": "Must support offline mode",
  "filePath": "/path/to/SPECs/ATGCTCGA/project_constitution.toml",
  "specs": [],
  "createdAt": "2026-01-02T10:00:00.000Z",
  "updatedAt": "2026-01-02T10:00:00.000Z"
}
```

### Create DNA Profile

**POST** `/api/dna`

Creates new DNA profile with auto-generated DNA code.

**Request Body:**
```json
{
  "projectName": "My Project",
  "testing": "standard",
  "risk": "medium",
  "autonomy": "high",
  "customTools": "React, Node.js",
  "constraints": "Must support offline mode"
}
```

**Required Fields:**
- `projectName` (string)
- `testing` (enum: "basic", "standard", "comprehensive")
- `risk` (enum: "low", "medium", "high")
- `autonomy` (enum: "low", "medium", "high")

**Response:**
```json
{
  "message": "DNA profile created successfully",
  "profile": {
    "id": "uuid",
    "dnaCode": "ATGCTCGA",
    "projectName": "My Project",
    ...
  }
}
```

### Update DNA Profile

**PUT** `/api/dna/:dnaCode`

Updates existing DNA profile.

**Parameters:**
- `dnaCode` (path) - DNA code to update

**Request Body:** Same as Create (all fields optional)

**Response:**
```json
{
  "message": "DNA profile updated successfully",
  "profile": { ... }
}
```

### Delete DNA Profile

**DELETE** `/api/dna/:dnaCode`

Deletes DNA profile (moves to .trash folder, cascade deletes from database).

**Parameters:**
- `dnaCode` (path) - DNA code to delete

**Response:**
```json
{
  "message": "DNA profile deleted successfully (moved to .trash)",
  "dnaCode": "ATGCTCGA"
}
```

---

## SPEC Endpoints

### List SPECs

**GET** `/api/specs`

Returns all SPECs across all DNA profiles.

**Query Parameters:**
- `dnaCode` (optional) - Filter by DNA code
- `status` (optional) - Filter by status (pending, running, completed)
- `search` (optional) - Search in descriptor and goal

**Response:**
```json
{
  "specs": [
    {
      "descriptor": "my_spec",
      "dnaCode": "ATGCTCGA",
      "goal": "Build a web application",
      "filePath": "/path/to/spec_my_spec.md",
      "parametersPath": "/path/to/parameters_my_spec.toml",
      "progressPath": "/path/to/progress_my_spec.json",
      "exists": true
    }
  ]
}
```

### Get SPEC Details

**GET** `/api/specs/:specId`

Returns detailed SPEC information.

**Parameters:**
- `specId` (path) - Format: `{dnaCode}/{descriptor}` (e.g., ATGCTCGA/my_spec)

**Response:**
```json
{
  "descriptor": "my_spec",
  "dnaCode": "ATGCTCGA",
  "goal": "Build a web application",
  "content": "# Full spec.md content...",
  "structure": {
    "tasks": [
      { "id": 1, "name": "Task 1 name" },
      { "id": 2, "name": "Task 2 name" }
    ]
  }
}
```

### Create SPEC

**POST** `/api/specs`

Creates new SPEC from template.

**Request Body:**
```json
{
  "dnaCode": "ATGCTCGA",
  "descriptor": "my_new_spec",
  "goal": "Build something awesome",
  "tasks": ["Task 1", "Task 2", "Task 3"]
}
```

**Required Fields:**
- `dnaCode` (string)
- `descriptor` (string, lowercase, underscores only)
- `goal` (string)

**Response:**
```json
{
  "message": "SPEC created successfully",
  "spec": { ... }
}
```

### Get Parameters

**GET** `/api/specs/:specId/parameters`

Returns parameters TOML file content.

**Parameters:**
- `specId` (path) - Format: `{dnaCode}/{descriptor}`

**Response:**
```json
{
  "content": "# Full parameters.toml content..."
}
```

### Update Parameters

**PUT** `/api/specs/:specId/parameters`

Updates parameters TOML file (validates and creates backup).

**Parameters:**
- `specId` (path) - Format: `{dnaCode}/{descriptor}`

**Request Body:**
```json
{
  "content": "# Updated TOML content..."
}
```

**Response:**
```json
{
  "message": "Parameters updated successfully",
  "backupPath": "/path/to/.backups/parameters_my_spec_2026-01-02.toml"
}
```

**Error Response (Invalid TOML):**
```json
{
  "error": "Invalid TOML syntax: Unexpected character..."
}
```

---

## Execution Endpoints

### List Executions

**GET** `/api/executions`

Returns all executions.

**Query Parameters:**
- `specId` (optional) - Filter by SPEC
- `status` (optional) - Filter by status

**Response:**
```json
{
  "executions": [
    {
      "id": "uuid",
      "specId": "uuid",
      "mode": "dynamic",
      "status": "completed",
      "goalStatus": "ACHIEVED",
      "startedAt": "2026-01-02T10:00:00.000Z",
      "completedAt": "2026-01-02T10:30:00.000Z",
      "duration": 1800000,
      "spec": {
        "descriptor": "my_spec",
        "dnaCode": "ATGCTCGA"
      }
    }
  ]
}
```

### Get Execution Details

**GET** `/api/executions/:executionId`

Returns detailed execution information.

**Parameters:**
- `executionId` (path) - Execution UUID

**Response:**
```json
{
  "execution": {
    "id": "uuid",
    "specId": "uuid",
    "mode": "dynamic",
    "status": "running",
    "goalStatus": null,
    "startedAt": "2026-01-02T10:00:00.000Z",
    "spec": { ... },
    "progressLogs": [ ... ]
  }
}
```

### Start Execution

**POST** `/api/executions`

Starts a new SPEC execution.

**Request Body:**
```json
{
  "specId": "ATGCTCGA/my_spec",
  "mode": "dynamic"
}
```

**Required Fields:**
- `specId` (string) - Format: `{dnaCode}/{descriptor}`
- `mode` (enum) - "silent", "dynamic", "collaborative"

**Response:**
```json
{
  "message": "Execution started",
  "executionId": "uuid",
  "specId": "ATGCTCGA/my_spec",
  "mode": "dynamic"
}
```

### Stop Execution

**POST** `/api/executions/:executionId/stop`

Stops a running execution.

**Parameters:**
- `executionId` (path) - Execution UUID

**Response:**
```json
{
  "message": "Execution stopped",
  "executionId": "uuid"
}
```

### Get Execution Results

**GET** `/api/executions/:executionId/results`

Returns execution results and completion verification.

**Parameters:**
- `executionId` (path) - Execution UUID

**Response:**
```json
{
  "execution": { ... },
  "progress": { ... },
  "goalStatus": "ACHIEVED",
  "completionVerification": {
    "primaryDeliverableExists": true,
    "qualityStandardsMet": true,
    "verificationMethodPassed": true
  },
  "postExecutionAnalysis": {
    "failureRate": 0.05,
    "backupsUsed": 2,
    "complianceScore": 95,
    "recommendations": [ ... ]
  }
}
```

### Get Execution Logs

**GET** `/api/executions/:executionId/logs`

Returns execution logs.

**Parameters:**
- `executionId` (path) - Execution UUID

**Response:**
```json
{
  "logs": [
    {
      "id": "uuid",
      "executionId": "uuid",
      "taskId": "1",
      "stepId": "1",
      "status": "completed",
      "method": "primary",
      "timestamp": "2026-01-02T10:00:00.000Z",
      "details": "Step completed successfully"
    }
  ]
}
```

---

## File Endpoints

### Validate TOML

**POST** `/api/files/validate/toml`

Validates TOML syntax.

**Request Body:**
```json
{
  "content": "[metadata]\nversion = \"1.0\""
}
```

**Response (Valid):**
```json
{
  "valid": true,
  "errors": []
}
```

**Response (Invalid):**
```json
{
  "valid": false,
  "errors": ["Expected newline but found ..."]
}
```

### Get Progress

**GET** `/api/files/progress/:specId`

Returns progress file content.

**Parameters:**
- `specId` (path) - Format: `{dnaCode}/{descriptor}`

**Response:**
```json
{
  "progress": {
    "run_id": "2026-01-02T10:00:00Z",
    "status": "completed",
    "goal_achievement_status": "ACHIEVED",
    "tasks": [ ... ],
    "completion_verification": { ... },
    "post_execution_analysis": { ... }
  }
}
```

---

## WebSocket Events

### Connection

**Client connects:**
```javascript
import { io } from 'socket.io-client';
const socket = io('http://localhost:5000');

socket.on('connect', () => {
  console.log('Connected:', socket.id);
});
```

### Subscribe to Progress

**Client subscribes:**
```javascript
socket.emit('subscribe-progress', 'ATGCTCGA/my_spec');
```

### Progress Updates

**Server broadcasts:**
```javascript
socket.on('progress-update', (progress) => {
  console.log('Progress:', progress);
  // progress contains full progress.json content
});
```

**Update Event Data:**
```json
{
  "status": "in_progress",
  "currentTask": 2,
  "currentStep": 3,
  "totalTasks": 5,
  "tasks": [ ... ]
}
```

### Unsubscribe

**Client unsubscribes:**
```javascript
socket.emit('unsubscribe-progress', 'ATGCTCGA/my_spec');
```

### Disconnect

```javascript
socket.disconnect();
```

---

## Error Responses

All error responses follow this format:

```json
{
  "error": "Human-readable error message",
  "message": "Technical details (development mode only)",
  "details": { ... }
}
```

### HTTP Status Codes

- **200** - Success
- **201** - Created
- **400** - Bad Request (invalid input)
- **404** - Not Found
- **500** - Internal Server Error

### Common Errors

**DNA Profile Not Found:**
```json
{
  "error": "DNA profile not found",
  "dnaCode": "INVALID1"
}
```

**Invalid TOML:**
```json
{
  "error": "Invalid TOML syntax: Expected newline but found ...",
  "line": 10
}
```

**Execution Already Running:**
```json
{
  "error": "SPEC is already executing",
  "specId": "ATGCTCGA/my_spec"
}
```

**Missing Required Fields:**
```json
{
  "error": "Missing required fields",
  "required": ["projectName", "testing", "risk", "autonomy"]
}
```

---

## Request Examples

### cURL Examples

**List DNA Profiles:**
```bash
curl http://localhost:5000/api/dna
```

**Create DNA Profile:**
```bash
curl -X POST http://localhost:5000/api/dna \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "Test Project",
    "testing": "standard",
    "risk": "medium",
    "autonomy": "high"
  }'
```

**Get SPEC Parameters:**
```bash
curl http://localhost:5000/api/specs/ATGCTCGA/my_spec/parameters
```

**Validate TOML:**
```bash
curl -X POST http://localhost:5000/api/files/validate/toml \
  -H "Content-Type: application/json" \
  -d '{"content": "[metadata]\nversion = \"1.0\""}'
```

**Start Execution:**
```bash
curl -X POST http://localhost:5000/api/executions \
  -H "Content-Type: application/json" \
  -d '{
    "specId": "ATGCTCGA/my_spec",
    "mode": "dynamic"
  }'
```

### JavaScript Examples

**Using Axios (Frontend):**

```javascript
import axios from 'axios';

// List SPECs
const response = await axios.get('/api/specs', {
  params: { dnaCode: 'ATGCTCGA' }
});

// Create DNA Profile
const profile = await axios.post('/api/dna', {
  projectName: 'Test Project',
  testing: 'standard',
  risk: 'medium',
  autonomy: 'high'
});

// Update Parameters
await axios.put('/api/specs/ATGCTCGA/my_spec/parameters', {
  content: tomlContent
});
```

---

## Rate Limiting

**Current Version:** No rate limiting

For production deployments, consider adding:
- 100 requests/minute per IP for general endpoints
- 10 requests/minute for execution start
- 1000 requests/minute for validation

---

## Versioning

API version is currently v1 (implicit).

Future versions will use URL versioning:
- `/api/v1/dna`
- `/api/v2/dna`

---

## CORS Configuration

**Allowed Origins:**
- Development: `http://localhost:3000`
- Production: Configure via `FRONTEND_URL` environment variable

**Allowed Methods:**
- GET, POST, PUT, DELETE

**Credentials:** Enabled for session support

---

## WebSocket Configuration

**Transport:** WebSocket with polling fallback  
**Path:** `/socket.io/`  
**Reconnection:** Automatic with exponential backoff

---

**API Documentation complete. All endpoints operational!**
