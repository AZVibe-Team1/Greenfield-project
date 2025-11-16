# Interview Scheduling Feature - Implementation Summary

## ✅ Implementation Complete

All backend components for the interview scheduling feature have been successfully implemented on the `schedule-interview` branch.

---

## 📁 Files Created

### 1. Interview Schema
**File:** `backend/schemas/interview.py`

- Complete Interview MongoDB model using Beanie ODM
- Separate collection approach (not embedded in employer schema)
- Denormalized fields for performance (job_title, company_name, seeker_name, seeker_email)
- Dual ID system (ObjectId + UUID) matching existing patterns
- Status tracking: Scheduled, Confirmed, Rescheduled, Completed, Cancelled, No-Show
- n8n integration fields (notification_sent, notification_sent_at)
- Proper indexes for efficient queries

### 2. n8n Integration Service
**File:** `backend/services/n8n_service.py`

- HTTP client using `httpx` for webhook calls
- Graceful failure handling (interview created even if email fails)
- Connection health check functionality
- Structured payload matching teammate's n8n workflow
- Comprehensive error logging

### 3. Interview Business Logic Service
**File:** `backend/services/interview_services.py`

- `create_interview()` - Creates interview with denormalized data
- `get_interviews_by_seeker()` - Seeker's interview list
- `get_interviews_by_employer()` - Employer's interview list
- `get_interviews_by_job()` - Job-specific interviews
- `update_interview_status()` - Status management
- `mark_notification_sent()` - Track email delivery

### 4. Interview API Router
**File:** `backend/api/v1/routes/interview_router.py`

Complete REST API with 7 endpoints (see API section below)

---

## 🔧 Files Modified

### 1. Database Settings
**File:** `backend/db/settings.py`

- Added `N8N_WEBHOOK_URL` configuration
- Registered `Interview` model in Beanie initialization
- Import statement updated

### 2. Main Application
**File:** `backend/main.py`

- Imported `interview_router`
- Registered router with `/api/v1` prefix

### 3. Dependencies
**File:** `pyproject.toml`

- Added `httpx` for HTTP requests to n8n

---

## 🔌 API Endpoints

All endpoints are prefixed with `/api/v1/interviews`

### Employer Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/` | Schedule new interview | Employer |
| GET | `/employer/me` | Get all my interviews | Employer |
| GET | `/job/{job_id}` | Get interviews for specific job | Employer |
| GET | `/n8n/status` | Check n8n connection status | Employer |
| POST | `/{interview_id}/retry-notification` | Retry failed email notification | Employer |

### Seeker Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/seeker/me` | Get all my interviews | Seeker |

### Shared Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| PATCH | `/{interview_id}/status` | Update interview status | Both |

---

## 📊 Data Model Overview

### Interview Collection Structure

```javascript
{
  // Identifiers
  interview_id: ObjectId,
  interview_identification: UUID,
  
  // Job Reference (denormalized)
  job_id: ObjectId,
  job_identification: UUID,
  job_title: "Senior Software Engineer",
  
  // Employer Reference (denormalized)
  employer_id: ObjectId,
  employer_identification: UUID,
  company_name: "Tech Corp",
  
  // Seeker Reference (denormalized)
  seeker_id: ObjectId,
  seeker_identification: UUID,
  seeker_name: "John Doe",
  seeker_email: "john@example.com",
  
  // Interview Details
  interview_details: {
    interview_type: "Video" | "In-person" | "Phone",
    scheduled_date: ISODate("2024-01-15T10:00:00Z"),
    scheduled_time: "10:00 AM",
    duration_minutes: 60,
    location_or_link: "https://zoom.us/j/123456",
    interviewer_name: "Jane Smith",
    interviewer_email: "jane@techcorp.com",
    notes: "Please prepare portfolio"
  },
  
  // Status & Tracking
  status: "Scheduled",
  scheduled_by: ObjectId,
  cancellation_reason: null,
  
  // n8n Integration
  n8n_notification_sent: true,
  n8n_notification_sent_at: ISODate("2024-01-10T15:30:00Z"),
  
  // Timestamps
  created_at: ISODate("2024-01-10T15:30:00Z"),
  updated_at: ISODate("2024-01-10T15:30:00Z")
}
```

### Indexes Created
- `seeker_id` - Seeker queries
- `employer_id` - Employer queries
- `job_id` - Job-specific queries
- `status` - Status filtering
- `interview_details.scheduled_date` - Date range queries
- `created_at` - Sorting by creation date

---

## 🔗 n8n Integration

### Webhook Payload Structure

```json
{
  "seeker_email": "candidate@example.com",
  "seeker_name": "John Doe",
  "job_title": "Senior Software Developer",
  "company_name": "Tech Corp",
  "interview_date": "2024-01-15",
  "interview_time": "10:00 AM",
  "interview_type": "Video Call",
  "location_or_link": "https://zoom.us/j/123456",
  "notes": "Please prepare portfolio examples"
}
```

### Error Handling Strategy

1. **Interview Creation First**: Interview is saved to MongoDB before n8n call
2. **Graceful Failure**: If n8n is down, interview is still created
3. **Status Tracking**: `n8n_notification_sent` flag tracks delivery
4. **Retry Mechanism**: Endpoint available to retry failed notifications
5. **Logging**: All webhook attempts logged for debugging

---

## ⚙️ Configuration Required

### Environment Variables

Add to your `.env` file:

```bash
# n8n Configuration
N8N_WEBHOOK_URL=http://n8n:5678/webhook/interview-schedule
# For local testing: http://localhost:5678/webhook/interview-schedule
```

### Your Teammate's n8n Setup

Your teammate should have the webhook configured to receive POST requests with the payload structure above. The workflow should:
1. Receive webhook payload
2. Format email template
3. Send email to `seeker_email`
4. Log notification

---

## 🧪 Testing

### Manual Testing Steps

1. **Start Docker**:
   ```bash
   docker compose up --build
   ```

2. **Login as Employer** (via `/api/v1/auth/login`)

3. **Schedule Interview** (POST `/api/v1/interviews/`):
   ```json
   {
     "job_id": "your_job_id",
     "seeker_id": "your_seeker_id",
     "interview_type": "Video",
     "scheduled_date": "2024-01-20T10:00:00Z",
     "scheduled_time": "10:00 AM",
     "duration_minutes": 60,
     "location_or_link": "https://zoom.us/j/123456",
     "interviewer_name": "Jane Smith",
     "interviewer_email": "jane@techcorp.com",
     "notes": "Bring portfolio"
   }
   ```

4. **Check n8n Status** (GET `/api/v1/interviews/n8n/status`)

5. **View Interviews**:
   - Employer: GET `/api/v1/interviews/employer/me`
   - Seeker: GET `/api/v1/interviews/seeker/me`

6. **Update Status** (PATCH `/api/v1/interviews/{id}/status`):
   ```json
   {
     "status": "Confirmed"
   }
   ```

### Testing Without n8n

If n8n is not running:
- Interview will be created successfully
- `n8n_notification_sent` will be `false`
- Warning logged but no error thrown
- Use retry endpoint when n8n is available

---

## 📝 Next Steps (Frontend)

### Components to Build

1. **Scheduling Modal** - Form for employers to schedule interviews
2. **Interview List** - Display interviews for both seekers and employers
3. **Status Tracker** - Visual status indicators
4. **Calendar View** (optional) - Monthly view of scheduled interviews

### API Integration Examples

```typescript
// Schedule Interview
const scheduleInterview = async (data: ScheduleInterviewData) => {
  const response = await api.post('/api/v1/interviews/', data);
  return response.data;
};

// Get My Interviews (Employer)
const getMyInterviews = async () => {
  const response = await api.get('/api/v1/interviews/employer/me');
  return response.data;
};

// Update Status
const updateInterviewStatus = async (interviewId: string, status: string) => {
  const response = await api.patch(`/api/v1/interviews/${interviewId}/status`, {
    status
  });
  return response.data;
};
```

---

## 🎯 Design Decisions

### Why Separate Collection?

✅ **Scalability**: Interviews grow independently  
✅ **Query Performance**: Dedicated indexes  
✅ **Data Integrity**: Easier to manage lifecycle  
✅ **Future Features**: Room for feedback, ratings, recordings  

### Why Denormalization?

✅ **Performance**: No joins needed for display  
✅ **n8n Integration**: Complete data in one document  
✅ **Reliability**: Data preserved even if references change  

### Why Graceful n8n Failure?

✅ **User Experience**: Interview confirmed immediately  
✅ **Reliability**: System works without email  
✅ **Retry**: Can send email later when n8n is available  

---

## 🐛 Troubleshooting

### Common Issues

**1. n8n notifications not sending**
- Check `N8N_WEBHOOK_URL` in `.env`
- Verify n8n service is running
- Use `/api/v1/interviews/n8n/status` to check connection
- Check logs for webhook errors

**2. Interview creation fails**
- Verify employer_id, seeker_id, and job_id exist
- Check MongoDB connection
- Review logs for validation errors

**3. MongoDB collection not created**
- Ensure `Interview` model is registered in `settings.py`
- Restart backend container
- Check Beanie initialization logs

---

## 📚 Related Documentation

- [AI Features Implementation Plan](./AI_FEATURES_IMPLEMENTATION_PLAN.md)
- [Backend Guidelines](./backend_guidelines.txt)
- [Frontend README](./frontend_md/README_FRONTEND.md)

---

## 👥 Team Coordination

### Your Scope (Complete ✅)
- ✅ Interview schema and database
- ✅ CRUD endpoints
- ✅ Interview service logic
- ✅ n8n webhook integration
- ✅ Status tracking

### Teammate's Scope (n8n)
- n8n workflow setup
- Email template design
- Email service configuration
- Webhook endpoint testing

### Next: Frontend Integration
- Schedule interview modal
- Interview list views
- Status indicators
- Date/time pickers

---

## 🚀 Deployment Checklist

- [x] Backend code implemented
- [x] Dependencies added (`httpx`)
- [x] MongoDB model registered
- [x] API endpoints tested
- [ ] Add `N8N_WEBHOOK_URL` to `.env`
- [ ] Test with n8n workflow
- [ ] Frontend implementation
- [ ] End-to-end testing
- [ ] Documentation for users

---

**Implementation Date:** November 16, 2025  
**Branch:** `schedule-interview`  
**Status:** Backend Complete ✅  
**Next:** Frontend + n8n Integration

