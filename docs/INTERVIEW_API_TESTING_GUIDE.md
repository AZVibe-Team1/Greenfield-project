# Interview Scheduling API - Testing Guide

Quick reference for testing the interview scheduling endpoints.

---

## 🔧 Setup

### 1. Add Environment Variable

Add to `.env`:
```bash
N8N_WEBHOOK_URL=http://localhost:5678/webhook/interview-schedule
```

### 2. Start Services

```bash
docker compose up --build
```

---

## 📍 API Base URL

```
http://localhost:8000/api/v1/interviews
```

---

## 🔑 Authentication

All endpoints require authentication. Include JWT token in headers:

```
Authorization: Bearer <your_token>
```

Get token from:
- POST `/api/v1/auth/login`

---

## 📝 Test Scenarios

### Scenario 1: Schedule Interview (Employer)

**Endpoint:** `POST /api/v1/interviews/`

**Request:**
```json
{
  "job_id": "674c1234567890abcdef1234",
  "seeker_id": "674c9876543210fedcba5678",
  "interview_type": "Video",
  "scheduled_date": "2025-11-20T10:00:00-07:00",
  "scheduled_time": "10:00 AM",
  "duration_minutes": 60,
  "location_or_link": "https://zoom.us/j/123456789",
  "interviewer_name": "Jane Smith",
  "interviewer_email": "jane@techcorp.com",
  "notes": "Please prepare a portfolio of your recent work"
}
```

**Expected Response (201):**
```json
{
  "interview_id": "674cabc1234567890abcdef1",
  "job_id": "674c1234567890abcdef1234",
  "job_title": "Senior Software Engineer",
  "employer_id": "674c1234567890abcdef5678",
  "company_name": "Tech Corp",
  "seeker_id": "674c9876543210fedcba5678",
  "seeker_name": "John Doe",
  "seeker_email": "john@example.com",
  "interview_type": "Video",
  "scheduled_date": "2025-11-20T10:00:00-07:00",
  "scheduled_time": "10:00 AM",
  "duration_minutes": 60,
  "location_or_link": "https://zoom.us/j/123456789",
  "interviewer_name": "Jane Smith",
  "status": "Scheduled",
  "created_at": "2025-11-16T15:30:00-07:00",
  "n8n_notification_sent": true
}
```

**Notes:**
- `n8n_notification_sent` will be `false` if n8n is down
- Interview is still created successfully even if email fails

---

### Scenario 2: Get My Interviews (Employer)

**Endpoint:** `GET /api/v1/interviews/employer/me`

**Expected Response (200):**
```json
[
  {
    "interview_id": "674cabc1234567890abcdef1",
    "job_id": "674c1234567890abcdef1234",
    "job_title": "Senior Software Engineer",
    "company_name": "Tech Corp",
    "seeker_id": "674c9876543210fedcba5678",
    "seeker_name": "John Doe",
    "seeker_email": "john@example.com",
    "interview_type": "Video",
    "scheduled_date": "2025-11-20T10:00:00-07:00",
    "scheduled_time": "10:00 AM",
    "status": "Scheduled",
    "n8n_notification_sent": true
  }
]
```

---

### Scenario 3: Get My Interviews (Seeker)

**Endpoint:** `GET /api/v1/interviews/seeker/me`

**Expected Response (200):**
```json
[
  {
    "interview_id": "674cabc1234567890abcdef1",
    "job_id": "674c1234567890abcdef1234",
    "job_title": "Senior Software Engineer",
    "employer_id": "674c1234567890abcdef5678",
    "company_name": "Tech Corp",
    "interview_type": "Video",
    "scheduled_date": "2025-11-20T10:00:00-07:00",
    "scheduled_time": "10:00 AM",
    "location_or_link": "https://zoom.us/j/123456789",
    "interviewer_name": "Jane Smith",
    "status": "Scheduled"
  }
]
```

---

### Scenario 4: Get Interviews for Specific Job (Employer)

**Endpoint:** `GET /api/v1/interviews/job/{job_id}`

**Example:** `GET /api/v1/interviews/job/674c1234567890abcdef1234`

**Expected Response (200):**
```json
[
  {
    "interview_id": "674cabc1234567890abcdef1",
    "seeker_name": "John Doe",
    "seeker_email": "john@example.com",
    "interview_type": "Video",
    "scheduled_date": "2025-11-20T10:00:00-07:00",
    "scheduled_time": "10:00 AM",
    "status": "Scheduled"
  },
  {
    "interview_id": "674cabc1234567890abcdef2",
    "seeker_name": "Jane Wilson",
    "seeker_email": "jane@example.com",
    "interview_type": "In-person",
    "scheduled_date": "2025-11-22T14:00:00-07:00",
    "scheduled_time": "2:00 PM",
    "status": "Confirmed"
  }
]
```

---

### Scenario 5: Update Interview Status

**Endpoint:** `PATCH /api/v1/interviews/{interview_id}/status`

**Example:** `PATCH /api/v1/interviews/674cabc1234567890abcdef1/status`

**Request:**
```json
{
  "status": "Confirmed"
}
```

**Valid Status Values:**
- `"Scheduled"`
- `"Confirmed"`
- `"Rescheduled"`
- `"Completed"`
- `"Cancelled"`
- `"No-Show"`

**Request (with cancellation):**
```json
{
  "status": "Cancelled",
  "cancellation_reason": "Candidate accepted another offer"
}
```

**Expected Response (200):**
```json
{
  "interview_id": "674cabc1234567890abcdef1",
  "status": "Confirmed",
  "job_title": "Senior Software Engineer",
  "seeker_name": "John Doe",
  "scheduled_date": "2025-11-20T10:00:00-07:00"
}
```

---

### Scenario 6: Check n8n Connection Status

**Endpoint:** `GET /api/v1/interviews/n8n/status`

**Expected Response (200) - Connected:**
```json
{
  "status": "connected",
  "message": "n8n service is reachable"
}
```

**Expected Response (200) - Disconnected:**
```json
{
  "status": "disconnected",
  "message": "Cannot connect to n8n service"
}
```

---

### Scenario 7: Retry Failed Notification

**Endpoint:** `POST /api/v1/interviews/{interview_id}/retry-notification`

**Example:** `POST /api/v1/interviews/674cabc1234567890abcdef1/retry-notification`

**Expected Response (200) - Success:**
```json
{
  "success": true,
  "message": "Notification sent successfully"
}
```

**Expected Response (200) - Failure:**
```json
{
  "success": false,
  "message": "Cannot connect to n8n service"
}
```

---

## ⚠️ Error Responses

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden (Wrong Role)
```json
{
  "detail": "Only employers can schedule interviews"
}
```

### 404 Not Found
```json
{
  "detail": "Interview 674cabc1234567890abcdef1 not found"
}
```

### 404 Not Found (Invalid References)
```json
{
  "detail": "Employer 674c1234567890abcdef5678 not found"
}
```
or
```json
{
  "detail": "Job 674c1234567890abcdef1234 not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Failed to schedule interview"
}
```

---

## 🧪 Postman/Thunder Client Collection

### Create Collection Variables

```
base_url: http://localhost:8000/api/v1
employer_token: <get_from_login>
seeker_token: <get_from_login>
```

### Test Flow

1. **Login as Employer**
   - POST `{{base_url}}/auth/login`
   - Save token as `employer_token`

2. **Login as Seeker**
   - POST `{{base_url}}/auth/login`
   - Save token as `seeker_token`

3. **Get Job IDs**
   - GET `{{base_url}}/employers/jobs` (with employer token)
   - Save a job_id

4. **Get Seeker IDs**
   - GET `{{base_url}}/employers/applications` (with employer token)
   - Save a seeker_id from applications

5. **Schedule Interview**
   - POST `{{base_url}}/interviews/` (with employer token)
   - Use job_id and seeker_id from above

6. **Verify as Employer**
   - GET `{{base_url}}/interviews/employer/me` (with employer token)

7. **Verify as Seeker**
   - GET `{{base_url}}/interviews/seeker/me` (with seeker token)

8. **Update Status**
   - PATCH `{{base_url}}/interviews/{interview_id}/status` (with employer token)

---

## 🔍 MongoDB Queries (for debugging)

### View All Interviews
```javascript
db.interviews.find().pretty()
```

### View Interviews by Status
```javascript
db.interviews.find({ status: "Scheduled" }).pretty()
```

### View Interviews by Seeker
```javascript
db.interviews.find({ seeker_id: "674c9876543210fedcba5678" }).pretty()
```

### Check n8n Notification Status
```javascript
db.interviews.find({ n8n_notification_sent: false }).pretty()
```

---

## 📊 Sample Data for Testing

### Sample Interview Types
- `"Video"` - For Zoom/Google Meet/Teams
- `"In-person"` - For office interviews
- `"Phone"` - For phone screenings

### Sample Locations/Links
- Video: `https://zoom.us/j/123456789`
- In-person: `123 Main St, Phoenix, AZ 85001`
- Phone: `+1-555-123-4567`

### Sample Interviewer Names
- `"Jane Smith"` (Technical Lead)
- `"John Doe"` (HR Manager)
- `"Sarah Wilson"` (CTO)

---

## 🐛 Debugging Tips

### Check Logs
```bash
docker logs greenfield-project-backend-1 -f
```

### Look for:
- `✅ n8n notification sent successfully`
- `⚠️ n8n returned status 404`
- `❌ Connection error to n8n`
- `Created interview {interview_id} for job {job_id}`

### Common Issues

**Interview not showing up:**
- Check if interview was created (check logs)
- Verify MongoDB connection
- Ensure using correct authentication token

**n8n notifications not sending:**
- Check `N8N_WEBHOOK_URL` in `.env`
- Verify n8n service is running: `GET /api/v1/interviews/n8n/status`
- Check n8n logs for webhook errors

**403 Forbidden errors:**
- Verify you're using the correct role token
- Employers schedule, both can view/update

---

## ✅ Success Indicators

- Interview created with 201 status
- `n8n_notification_sent: true` in response
- Seeker receives email (if n8n configured)
- Interview appears in both employer and seeker lists
- Status can be updated successfully

---

**Last Updated:** November 16, 2025  
**API Version:** v1  
**Branch:** `schedule-interview`

