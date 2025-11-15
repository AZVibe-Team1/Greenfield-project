# AI Features Implementation Plan

## Overview

This plan implements three AI-powered features for the job portal:

1. **Seeker Job Recommendations** - AI-powered job matching with percentage scores
2. **Employer Candidate Recommendations** - AI-powered candidate matching with percentage scores  
3. **Email Notifications** - n8n integration for interview scheduling notifications

## Architecture Components

### Existing Infrastructure

- ChromaDB with embeddings (text-embedding-3-small) at `./chroma_db`
- Ingestion scripts: `ingest_seeker.py`, `ingest_employer.py`
- Vector store: `backend/ai/rag/vector_store.py`
- API routes: `seeker_router.py`, `employer_router.py`
- Frontend pages: `seeker/recommendations/page.tsx` (placeholder), `employer/jobs/[jobId]/page.tsx`

### New Components to Build

- LangChain matching/scoring service
- Recommendation API endpoints
- n8n service integration
- Frontend recommendation displays with scores
- Auto-apply functionality

---

## Feature 1: Seeker Job Recommendations

### Backend Implementation

#### 1.1 Create Matching Service (`backend/ai/chains/matching_service.py`)

- **Purpose**: Core matching logic using LangChain + ChromaDB
- **Functions**:
  - `match_seeker_to_jobs(seeker_id: str) -> list[dict]` - Main matching function
  - `calculate_match_score(seeker_data: dict, job_data: dict) -> float` - Score calculation (0-100%)
  - `get_seeker_embedding(seeker_id: str) -> list[float]` - Retrieve seeker embedding from ChromaDB
  - `search_similar_jobs(query_embedding: list[float], n_results: int) -> list[dict]` - Vector similarity search
- **Process**:

  1. Get seeker embedding from ChromaDB (`Seeker_Resume` collection)
  2. Query ChromaDB for similar jobs (`Employer_JobDescr` collection)
  3. For each job, fetch full details from MongoDB
  4. Use LangChain (gpt-4o-mini) to analyze match factors:

     - Skills overlap
     - Education compatibility
     - Pay range alignment
     - Experience relevance

  1. Calculate composite score (0-100%)
  2. Filter to only active jobs (`current_status == "Posted"`)
  3. Sort by match score (descending)

#### 1.2 Create LangChain Chain (`backend/ai/chains/scoring_chain.py`)

- **Purpose**: LLM-based scoring analysis
- **Components**:
  - Prompt template for match analysis
  - LangChain chain using `ChatOpenAI` (gpt-4o-mini)
  - Structured output parser for score (0-100)
- **Input**: Seeker profile + Job posting data
- **Output**: JSON with score breakdown and reasoning

#### 1.3 Add API Endpoint (`backend/api/v1/routes/seeker_router.py`)

- **Endpoint**: `GET /api/v1/seekers/recommendations`
- **Response Model**:
```python
class JobRecommendationResponse(BaseModel):
    job_id: str
    job_title: str
    company_name: str
    employer_id: str
    match_score: float  # 0-100
    score_breakdown: dict  # Skills, education, pay, etc.
    job_description: str
    # ... other job fields
```

- **Logic**: Call matching service, return sorted recommendations

#### 1.4 Auto-Apply Feature

- **New Endpoint**: `POST /api/v1/seekers/auto-apply/settings`
  - Store user-defined threshold (e.g., 80%)
- **Modify**: `POST /api/v1/seekers/recommendations/apply/{job_id}`
  - Check if match_score >= threshold
  - If yes, automatically call `apply_for_job()`
- **Background Task**: Periodic check for new jobs above threshold

### Frontend Implementation

#### 1.5 Update Recommendations Page (`frontend/app/seeker/recommendations/page.tsx`)

- **Display**:
  - List of recommended jobs sorted by match score
  - Show match score prominently (e.g., "95% Match")
  - Score breakdown visualization
  - "Apply" button (triggers auto-apply if threshold met)
  - Filter/sort options
- **API Integration**: Call `GET /api/v1/seekers/recommendations`

#### 1.6 Add Auto-Apply Settings (`frontend/app/seeker/profile/page.tsx`)

- **UI Component**: Toggle for auto-apply
- **Input**: Threshold percentage (default: 80%)
- **API**: `POST /api/v1/seekers/auto-apply/settings`

---

## Feature 2: Employer Candidate Recommendations

### Backend Implementation

#### 2.1 Create Candidate Matching Service (`backend/ai/chains/candidate_matching_service.py`)

- **Purpose**: Match candidates to specific job postings
- **Functions**:
  - `match_job_to_candidates(job_id: str, employer_id: str) -> list[dict]` - Main matching function
  - `get_job_embedding(job_id: str) -> list[float]` - Retrieve job embedding from ChromaDB
  - `search_similar_seekers(query_embedding: list[float], n_results: int) -> list[dict]` - Vector similarity search
- **Process**:

  1. Get job embedding from ChromaDB (`Employer_JobDescr` collection)
  2. Query ChromaDB for similar seekers (`Seeker_Resume` collection)
  3. For each seeker, fetch full details from MongoDB
  4. Use LangChain (gpt-4o-mini) to analyze match factors
  5. Calculate composite score (0-100%)
  6. Check if seeker has applied (from `apps_received` array)
  7. Sort by match score (descending)

#### 2.2 Add API Endpoints (`backend/api/v1/routes/employer_router.py`)

- **Endpoint 1**: `GET /api/v1/employers/jobs` (enhance existing)
  - Add `recommendations_count` field to each job
- **Endpoint 2**: `GET /api/v1/employers/jobs/{job_id}/candidates`
  - **Response Model**:
```python
class CandidateRecommendationResponse(BaseModel):
    seeker_id: str
    first_name: str
    last_name: str
    email: str
    match_score: float  # 0-100
    score_breakdown: dict
    has_applied: bool  # Tag for applied status
    resume_preview: str
    # ... other seeker fields
```

- **Logic**: Call candidate matching service

### Frontend Implementation

#### 2.3 Update Employer Jobs Page (`frontend/app/employer/jobs/page.tsx`)

- **Display**:
  - List of active job postings
  - Each job shows "View Candidates" button
  - Click navigates to candidate recommendations

#### 2.4 Create Candidate Recommendations Page (`frontend/app/employer/jobs/[jobId]/candidates/page.tsx`)

- **Display**:
  - Job title and details at top
  - List of matching candidates sorted by score
  - Show match score prominently
  - "Applied" tag/badge for candidates who applied
  - Candidate cards with:
    - Name, email
    - Match score with breakdown
    - Resume preview
    - "Schedule Interview" button
- **API Integration**: Call `GET /api/v1/employers/jobs/{job_id}/candidates`

---

## Feature 3: Email Notifications via n8n

### Backend Implementation

#### 3.1 Create n8n Service (`backend/services/n8n_service.py`)

- **Purpose**: Interface with n8n API/webhooks
- **Functions**:
  - `check_n8n_connection() -> bool` - Health check
  - `trigger_interview_workflow(seeker_email: str, job_title: str, employer_name: str, interview_details: dict) -> bool` - Trigger n8n workflow
  - `get_n8n_status() -> dict` - Get n8n service status
- **Configuration**:
  - n8n API URL from environment variable
  - Webhook endpoint for interview scheduling
  - Error handling for n8n unavailability

#### 3.2 Add Interview Scheduling Endpoint (`backend/api/v1/routes/employer_router.py`)

- **Endpoint**: `POST /api/v1/employers/jobs/{job_id}/candidates/{seeker_id}/schedule-interview`
- **Request Model**:
```python
class ScheduleInterviewRequest(BaseModel):
    interview_date: datetime
    interview_time: str
    interview_type: str  # "In-person", "Video", "Phone"
    location_or_link: str
    notes: str | None = None
```

- **Logic**:

  1. Validate n8n connection
  2. Get seeker email from MongoDB
  3. Get job details
  4. Call n8n service to trigger workflow
  5. Update application status in MongoDB
  6. Return success/error

#### 3.3 Add n8n Health Check Endpoint (`backend/api/v1/routes/employer_router.py`)

- **Endpoint**: `GET /api/v1/employers/n8n/status`
- **Response**: `{"status": "connected" | "disconnected", "message": str}`

### Docker Configuration

#### 3.4 Add n8n to docker-compose.yml

- **Service**: `n8n`
- **Image**: `n8nio/n8n:latest`
- **Ports**: `5678:5678`
- **Volumes**: 
  - `./n8n_data:/home/node/.n8n` (persistent storage)
  - Environment variables for n8n config
- **Networks**: `jobportal-network`
- **Health Check**: HTTP endpoint check

### Frontend Implementation

#### 3.5 Update Candidate Recommendations Page

- **Add**: "Schedule Interview" button on each candidate card
- **Modal/Form**: Interview scheduling form
  - Date picker
  - Time picker
  - Interview type selector
  - Location/Link input
  - Notes field
- **API Integration**: Call `POST /api/v1/employers/jobs/{job_id}/candidates/{seeker_id}/schedule-interview`
- **Error Handling**: Show "Unable to schedule interview" if n8n is disconnected

#### 3.6 Add n8n Status Indicator (`frontend/app/employer/dashboard/page.tsx`)

- **Display**: Status badge showing n8n connection status
- **API**: Call `GET /api/v1/employers/n8n/status`

### n8n Workflow Setup

#### 3.7 Create n8n Workflow

- **Trigger**: Webhook (HTTP POST from backend)
- **Steps**:

  1. Receive webhook payload (seeker_email, job_title, employer_name, interview_details)
  2. Format email template
  3. Send email via SMTP/Email service
  4. Log notification

- **Export**: Save workflow JSON for documentation

---

## Implementation Order

### Phase 1: Core Matching Infrastructure

1. Create LangChain scoring chain (`backend/ai/chains/scoring_chain.py`)
2. Create seeker matching service (`backend/ai/chains/matching_service.py`)
3. Create candidate matching service (`backend/ai/chains/candidate_matching_service.py`)
4. Add unit tests for matching logic

### Phase 2: Seeker Recommendations

5. Add seeker recommendations API endpoint
6. Update frontend recommendations page
7. Implement auto-apply feature
8. Test end-to-end seeker flow

### Phase 3: Employer Recommendations

9. Add employer candidate recommendations API endpoint
10. Create candidate recommendations frontend page
11. Update employer jobs page with navigation
12. Test end-to-end employer flow

### Phase 4: n8n Integration

13. Add n8n service to backend
14. Add n8n to docker-compose.yml
15. Create interview scheduling endpoint
16. Set up n8n workflow
17. Update frontend with interview scheduling
18. Test email notifications

---

## Key Files to Modify/Create

### Backend

- `backend/ai/chains/scoring_chain.py` (NEW)
- `backend/ai/chains/matching_service.py` (NEW)
- `backend/ai/chains/candidate_matching_service.py` (NEW)
- `backend/services/n8n_service.py` (NEW)
- `backend/api/v1/routes/seeker_router.py` (MODIFY - add recommendations endpoint)
- `backend/api/v1/routes/employer_router.py` (MODIFY - add candidates endpoint, interview scheduling)
- `backend/schemas/seeker.py` (MODIFY - add auto-apply settings)
- `docker-compose.yml` (MODIFY - add n8n service)

### Frontend

- `frontend/app/seeker/recommendations/page.tsx` (MODIFY - implement recommendations display)
- `frontend/app/seeker/profile/page.tsx` (MODIFY - add auto-apply settings)
- `frontend/app/employer/jobs/page.tsx` (MODIFY - add candidate links)
- `frontend/app/employer/jobs/[jobId]/candidates/page.tsx` (NEW)
- `frontend/services/seeker-service.ts` (MODIFY - add recommendations API call)
- `frontend/services/employer-service.ts` (MODIFY - add candidates API call)

---

## Environment Variables

Add to `.env`:

```bash
# n8n Configuration
N8N_API_URL=http://n8n:5678
N8N_WEBHOOK_URL=http://n8n:5678/webhook/interview-schedule
N8N_API_KEY=  # Optional, if using n8n API authentication

# Auto-apply default threshold
DEFAULT_AUTO_APPLY_THRESHOLD=80
```

---

## Testing Strategy

1. **Unit Tests**: Matching algorithms, scoring functions
2. **Integration Tests**: API endpoints with mock ChromaDB/MongoDB
3. **E2E Tests**: Full recommendation flow (seeker + employer)
4. **n8n Tests**: Webhook triggering, email delivery

---

## Dependencies to Add

```bash
# Backend
uv add langchain langchain-openai httpx  # For n8n API calls

# Frontend (if needed)
# No new dependencies required
```

---

## Notes

- ChromaDB collections use different IDs:
  - Seekers: `seeker_identification` (UUID) in ChromaDB, but `seeker_id` (ObjectId) in MongoDB
  - Jobs: `job_identification` (UUID) in ChromaDB, but `job_id` (ObjectId) in MongoDB
- Matching scores should be cached to avoid repeated LLM calls
- Consider rate limiting for recommendation endpoints
- n8n workflow should handle email delivery failures gracefully