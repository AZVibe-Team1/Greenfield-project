# JobPortal - Implementation Plan

## Brief Description / Context

The JobPortal is a comprehensive platform connecting job seekers with employers, leveraging AI for intelligent matching, resume parsing, and personalized recommendations. This implementation plan breaks down the development into six logical phases, each with specific deliverables, dependencies, and technical requirements.

The phased approach ensures that foundational components (authentication, database, core models) are built first, followed by user-facing features, and finally AI-powered enhancements.

---

## Implementation Phases Overview

| Phase | Focus Area | Duration Estimate | Dependencies |
|-------|-----------|------------------|--------------|
| 0 | Project Foundation & Setup | 1-2 weeks | None |
| 1 | Core Authentication & User Management | 2-3 weeks | Phase 0 |
| 2 | Job Management & Search | 3-4 weeks | Phase 1 |
| 3 | Application & Interview Management | 2-3 weeks | Phase 2 |
| 4 | AI Features & Recommendations | 3-4 weeks | Phase 2, 3 |
| 5 | Notifications & Polish | 2 weeks | Phase 3, 4 |

---

## Phase 0: Project Foundation & Setup

### Purpose
Establish the development environment, project structure, core dependencies, and infrastructure foundation.

### Deliverables
- ✅ Fully configured development environment
- ✅ Database connection and ODM setup
- ✅ Project structure following layered architecture
- ✅ Docker configuration
- ✅ Basic CI/CD pipeline
- ✅ Logging and error handling framework

### Technical Tasks

#### Backend Setup
- **Files to Create/Modify:**
  - `backend/main.py` - FastAPI application entry point with CORS, middleware
  - `backend/core/config.py` - Environment configuration, settings management
  - `backend/core/database.py` - MongoDB connection with Beanie initialization
  - `backend/core/security.py` - Security utilities (password hashing, JWT)
  - `backend/core/exceptions.py` - Custom exception classes
  - `backend/core/logging.py` - Structured logging configuration
  - `backend/utils/validators.py` - Common validation utilities
  - `pyproject.toml` - Update with all required dependencies

- **Dependencies to Install (via uv):**
  ```bash
  fastapi
  uvicorn[standard]
  beanie
  motor
  pydantic
  pydantic-settings
  python-jose[cryptography]
  passlib[bcrypt]
  python-multipart
  email-validator
  ```

#### Frontend Setup
- **Files to Create/Modify:**
  - `frontend/package.json` - Next.js 14 dependencies
  - `frontend/tsconfig.json` - TypeScript configuration
  - `frontend/tailwind.config.ts` - Tailwind CSS setup
  - `frontend/next.config.js` - Next.js configuration
  - `frontend/lib/api-client.ts` - API client with axios/fetch
  - `frontend/lib/auth-context.tsx` - Authentication context provider
  - `frontend/middleware.ts` - Route protection middleware
  - `frontend/types/index.ts` - Common TypeScript types

#### Infrastructure
- **Files to Create:**
  - `docker-compose.yml` - Multi-service orchestration
  - `backend/Dockerfile` - Backend container
  - `frontend/Dockerfile` - Frontend container
  - `.env.example` - Environment variables template
  - `.gitignore` - Ignore sensitive files

#### Database Setup
- **Tasks:**
  - Create MongoDB Atlas cluster or local MongoDB
  - Configure database connection strings
  - Set up database indexes for performance
  - Create initial collections structure

### Dependencies
- None (foundation phase)

### Acceptance Criteria
- ✓ Backend server runs on http://localhost:8000
- ✓ Frontend dev server runs on http://localhost:3000
- ✓ MongoDB connection successful
- ✓ Docker containers build and run successfully
- ✓ Health check endpoints respond correctly
- ✓ Logging outputs structured JSON logs

---

## Phase 1: Core Authentication & User Management

### Purpose
Implement secure user registration, login, and profile management for both job seekers and employers with role-based access control.

### Deliverables
- ✅ User registration (job seekers and employers)
- ✅ Secure login with JWT authentication
- ✅ Password reset functionality
- ✅ Profile management (view, edit)
- ✅ Role-based access control (RBAC)
- ✅ Frontend authentication UI

### Technical Tasks

#### Backend - Models
- **Files to Create:**
  - `backend/model/user.py` - User base model (email, password_hash, role, created_at)
  - `backend/model/job_seeker.py` - JobSeeker model (extends user, profile fields)
  - `backend/model/employer.py` - Employer model (company info, extends user)
  - `backend/model/token.py` - Token blacklist model for logout

- **Model Fields:**
  ```python
  # User (base)
  - email: EmailStr
  - password_hash: str
  - role: Literal["job_seeker", "employer"]
  - is_active: bool
  - is_verified: bool
  - created_at: datetime
  - updated_at: datetime
  
  # JobSeeker
  - full_name: str
  - phone: Optional[str]
  - location: str
  - skills: List[str]
  - experience_years: int
  - resume_url: Optional[str]
  - preferences: Dict (job_type, salary_range, etc.)
  
  # Employer
  - company_name: str
  - company_size: str
  - industry: str
  - website: Optional[str]
  - description: str
  - logo_url: Optional[str]
  ```

#### Backend - Schemas
- **Files to Create:**
  - `backend/schemas/auth_schema.py` - LoginRequest, RegisterRequest, TokenResponse
  - `backend/schemas/user_schema.py` - UserResponse, UserUpdate
  - `backend/schemas/job_seeker_schema.py` - JobSeekerCreate, JobSeekerResponse, JobSeekerUpdate
  - `backend/schemas/employer_schema.py` - EmployerCreate, EmployerResponse, EmployerUpdate

#### Backend - Database Layer
- **Files to Create:**
  - `backend/db/user_db.py` - CRUD operations for user
  - `backend/db/job_seeker_db.py` - CRUD for job seeker profiles
  - `backend/db/employer_db.py` - CRUD for employer profiles

- **Key Functions:**
  - `create_user()`, `get_user_by_email()`, `get_user_by_id()`
  - `update_user()`, `delete_user()`
  - `create_job_seeker_profile()`, `update_job_seeker_profile()`
  - `create_employer_profile()`, `update_employer_profile()`

#### Backend - Services
- **Files to Create:**
  - `backend/services/auth_service.py` - Authentication logic
  - `backend/services/user_service.py` - User management logic
  - `backend/services/job_seeker_service.py` - Job seeker profile logic
  - `backend/services/employer_service.py` - Employer profile logic

- **Key Functions:**
  - `register_user()`, `authenticate_user()`, `create_access_token()`
  - `verify_password()`, `reset_password()`, `refresh_token()`
  - `get_current_user()` (dependency injection)

#### Backend - Routers
- **Files to Create:**
  - `backend/api/v1/routes/auth_router.py` - /auth/register, /auth/login, /auth/logout
  - `backend/api/v1/routes/user_router.py` - /users/me, /users/me (PUT)
  - `backend/api/v1/routes/job_seeker_router.py` - /job-seekers/profile endpoints
  - `backend/api/v1/routes/employer_router.py` - /employers/profile endpoints

- **Endpoints:**
  ```
  POST   /api/v1/auth/register
  POST   /api/v1/auth/login
  POST   /api/v1/auth/logout
  POST   /api/v1/auth/refresh
  POST   /api/v1/auth/password-reset-request
  POST   /api/v1/auth/password-reset
  
  GET    /api/v1/users/me
  PUT    /api/v1/users/me
  DELETE /api/v1/users/me
  
  GET    /api/v1/job-seekers/profile
  PUT    /api/v1/job-seekers/profile
  
  GET    /api/v1/employers/profile
  PUT    /api/v1/employers/profile
  ```

#### Frontend - Authentication
- **Files to Create:**
  - `frontend/app/(auth)/login/page.tsx` - Login page
  - `frontend/app/(auth)/register/page.tsx` - Registration page (role selection)
  - `frontend/app/(auth)/register/job-seeker/page.tsx` - Job seeker registration
  - `frontend/app/(auth)/register/employer/page.tsx` - Employer registration
  - `frontend/app/(auth)/forgot-password/page.tsx` - Password reset request
  - `frontend/app/(auth)/reset-password/page.tsx` - Password reset form
  - `frontend/components/auth/LoginForm.tsx` - Login form component
  - `frontend/components/auth/RegisterForm.tsx` - Registration form component
  - `frontend/lib/auth.ts` - Auth helper functions
  - `frontend/services/auth-service.ts` - Auth API calls
  - `frontend/store/auth-store.ts` - Auth state management (Zustand/Redux)

#### Frontend - Profile Management
- **Files to Create:**
  - `frontend/app/dashboard/profile/page.tsx` - Profile view/edit page
  - `frontend/components/profile/JobSeekerProfile.tsx` - Job seeker profile component
  - `frontend/components/profile/EmployerProfile.tsx` - Employer profile component
  - `frontend/components/profile/ProfileEdit.tsx` - Profile editing form
  - `frontend/services/user-service.ts` - User API calls

### Dependencies
- Phase 0 (Project Foundation)

### Acceptance Criteria
- ✓ Users can register as job seeker or employer
- ✓ Users can login with email/password
- ✓ JWT tokens are generated and validated
- ✓ Protected routes require authentication
- ✓ Users can view and edit their profiles
- ✓ Password reset flow works via email
- ✓ RBAC prevents unauthorized access
- ✓ All passwords are hashed with bcrypt
- ✓ Input validation works on all forms

---

## Phase 2: Job Management & Search

### Purpose
Enable employers to post jobs and job seekers to search, filter, and view job listings.

### Deliverables
- ✅ Job posting creation and management (employers)
- ✅ Job search with filters (job seekers)
- ✅ Job detail view
- ✅ Job listing page with pagination
- ✅ Advanced search (by title, skills, location, company)
- ✅ Save/bookmark jobs (job seekers)

### Technical Tasks

#### Backend - Models
- **Files to Create:**
  - `backend/model/job.py` - Job posting model
  - `backend/model/saved_job.py` - Saved jobs (bookmarks)

- **Job Model Fields:**
  ```python
  - title: str
  - description: str
  - requirements: List[str]
  - skills_required: List[str]
  - location: str
  - job_type: Literal["full_time", "part_time", "contract", "remote"]
  - experience_level: Literal["entry", "mid", "senior"]
  - salary_range: Dict (min, max, currency)
  - employer_id: PydanticObjectId
  - company_name: str (denormalized for search)
  - status: Literal["active", "closed", "draft"]
  - posted_date: datetime
  - deadline: Optional[datetime]
  - views_count: int
  - applications_count: int
  ```

#### Backend - Schemas
- **Files to Create:**
  - `backend/schemas/job_schema.py` - JobCreate, JobUpdate, JobResponse, JobListResponse
  - `backend/schemas/search_schema.py` - SearchFilters, SearchResponse

#### Backend - Database Layer
- **Files to Create:**
  - `backend/db/job_db.py` - CRUD for jobs
  - `backend/db/saved_job_db.py` - CRUD for saved jobs

- **Key Functions:**
  - `create_job()`, `get_job_by_id()`, `update_job()`, `delete_job()`
  - `search_jobs(filters)` - Complex search with multiple filters
  - `get_jobs_by_employer()`, `get_active_jobs()`
  - `save_job()`, `unsave_job()`, `get_saved_jobs()`

#### Backend - Services
- **Files to Create:**
  - `backend/services/job_service.py` - Job management logic
  - `backend/services/search_service.py` - Search logic with filters

- **Key Functions:**
  - `create_job_posting()`, `update_job_posting()`, `close_job()`
  - `search_jobs_with_filters()` - Handle complex queries
  - `increment_job_views()`, `get_job_statistics()`

#### Backend - Routers
- **Files to Create:**
  - `backend/api/v1/routes/job_router.py` - Job CRUD endpoints
  - `backend/api/v1/routes/search_router.py` - Search endpoints

- **Endpoints:**
  ```
  POST   /api/v1/jobs              (employer only)
  GET    /api/v1/jobs              (list with pagination)
  GET    /api/v1/jobs/:id
  PUT    /api/v1/jobs/:id          (employer only, own jobs)
  DELETE /api/v1/jobs/:id          (employer only, own jobs)
  PATCH  /api/v1/jobs/:id/close    (employer only)
  
  GET    /api/v1/jobs/employer/my-jobs  (employer's jobs)
  GET    /api/v1/search/jobs       (with query params)
  
  POST   /api/v1/jobs/:id/save     (job seeker only)
  DELETE /api/v1/jobs/:id/save     (job seeker only)
  GET    /api/v1/jobs/saved        (job seeker only)
  ```

#### Frontend - Job Posting (Employers)
- **Files to Create:**
  - `frontend/app/employer/jobs/page.tsx` - My jobs list
  - `frontend/app/employer/jobs/new/page.tsx` - Create job posting
  - `frontend/app/employer/jobs/[id]/edit/page.tsx` - Edit job
  - `frontend/components/jobs/JobForm.tsx` - Job creation/edit form
  - `frontend/components/jobs/JobCard.tsx` - Job card component
  - `frontend/components/jobs/JobList.tsx` - Job list component
  - `frontend/services/job-service.ts` - Job API calls

#### Frontend - Job Search (Job Seekers)
- **Files to Create:**
  - `frontend/app/jobs/page.tsx` - Job search/listing page
  - `frontend/app/jobs/[id]/page.tsx` - Job detail page
  - `frontend/app/jobs/saved/page.tsx` - Saved jobs page
  - `frontend/components/search/SearchBar.tsx` - Search input
  - `frontend/components/search/SearchFilters.tsx` - Filter sidebar
  - `frontend/components/search/JobResults.tsx` - Search results
  - `frontend/components/jobs/JobDetails.tsx` - Job detail view
  - `frontend/services/search-service.ts` - Search API calls
  - `frontend/hooks/useJobSearch.ts` - Search hook with filters

#### Database Indexes
- **Create Indexes:**
  ```python
  # jobs collection
  - text index on: title, description, skills_required
  - compound index on: location, job_type, status
  - index on: employer_id, posted_date, status
  ```

### Dependencies
- Phase 1 (need authentication and user roles)

### Acceptance Criteria
- ✓ Employers can create, edit, and delete job postings
- ✓ Job seekers can search jobs by keywords, skills, location
- ✓ Search results are paginated and sortable
- ✓ Job detail page shows complete information
- ✓ Job seekers can save/bookmark jobs
- ✓ Employers can view their posted jobs
- ✓ Job statistics (views, applications) are tracked
- ✓ Only active jobs appear in search results
- ✓ Search performance is acceptable (<500ms)

---

## Phase 3: Application & Interview Management

### Purpose
Enable job seekers to apply for jobs and employers to review applications, shortlist candidates, and schedule interviews.

### Deliverables
- ✅ Job application submission
- ✅ Application tracking (status, history)
- ✅ Resume upload and management
- ✅ Application review (employer side)
- ✅ Candidate shortlisting
- ✅ Interview scheduling
- ✅ Application status updates

### Technical Tasks

#### Backend - Models
- **Files to Create:**
  - `backend/model/application.py` - Job application model
  - `backend/model/resume.py` - Resume metadata model
  - `backend/model/interview.py` - Interview scheduling model

- **Application Model Fields:**
  ```python
  - job_id: PydanticObjectId
  - job_seeker_id: PydanticObjectId
  - resume_url: str
  - cover_letter: Optional[str]
  - status: Literal["submitted", "reviewing", "shortlisted", "interview", "rejected", "accepted"]
  - applied_date: datetime
  - updated_date: datetime
  - employer_notes: Optional[str]
  - screening_answers: Optional[Dict]
  ```

- **Interview Model Fields:**
  ```python
  - application_id: PydanticObjectId
  - job_id: PydanticObjectId
  - job_seeker_id: PydanticObjectId
  - employer_id: PydanticObjectId
  - scheduled_time: datetime
  - duration_minutes: int
  - location_type: Literal["in_person", "video", "phone"]
  - location_details: str
  - status: Literal["scheduled", "completed", "cancelled", "rescheduled"]
  - notes: Optional[str]
  ```

#### Backend - Schemas
- **Files to Create:**
  - `backend/schemas/application_schema.py` - ApplicationCreate, ApplicationResponse, ApplicationUpdate
  - `backend/schemas/resume_schema.py` - ResumeUpload, ResumeResponse
  - `backend/schemas/interview_schema.py` - InterviewCreate, InterviewResponse, InterviewUpdate

#### Backend - Database Layer
- **Files to Create:**
  - `backend/db/application_db.py` - CRUD for applications
  - `backend/db/resume_db.py` - Resume storage operations
  - `backend/db/interview_db.py` - Interview CRUD

- **Key Functions:**
  - `create_application()`, `get_application_by_id()`, `update_application_status()`
  - `get_applications_by_job()`, `get_applications_by_job_seeker()`
  - `check_duplicate_application()`, `get_application_statistics()`
  - `create_interview()`, `update_interview()`, `get_interviews()`

#### Backend - Services
- **Files to Create:**
  - `backend/services/application_service.py` - Application logic
  - `backend/services/resume_service.py` - Resume handling and validation
  - `backend/services/interview_service.py` - Interview scheduling logic
  - `backend/services/file_service.py` - File upload/storage (S3 or local)

- **Key Functions:**
  - `submit_application()`, `withdraw_application()`
  - `review_application()`, `shortlist_candidate()`
  - `upload_resume()`, `validate_resume_file()`
  - `schedule_interview()`, `reschedule_interview()`, `cancel_interview()`

#### Backend - Routers
- **Files to Create:**
  - `backend/api/v1/routes/application_router.py` - Application endpoints
  - `backend/api/v1/routes/resume_router.py` - Resume upload endpoints
  - `backend/api/v1/routes/interview_router.py` - Interview endpoints

- **Endpoints:**
  ```
  POST   /api/v1/applications              (job seeker, apply to job)
  GET    /api/v1/applications              (job seeker, my applications)
  GET    /api/v1/applications/:id
  DELETE /api/v1/applications/:id          (withdraw)
  
  GET    /api/v1/jobs/:id/applications     (employer, job's applications)
  PATCH  /api/v1/applications/:id/status   (employer, update status)
  POST   /api/v1/applications/:id/shortlist (employer)
  
  POST   /api/v1/resumes/upload            (job seeker)
  GET    /api/v1/resumes/my-resumes
  DELETE /api/v1/resumes/:id
  
  POST   /api/v1/interviews                (employer)
  GET    /api/v1/interviews                (both roles)
  PUT    /api/v1/interviews/:id
  PATCH  /api/v1/interviews/:id/cancel
  ```

#### Frontend - Application (Job Seekers)
- **Files to Create:**
  - `frontend/app/jobs/[id]/apply/page.tsx` - Application form page
  - `frontend/app/applications/page.tsx` - My applications list
  - `frontend/app/applications/[id]/page.tsx` - Application details
  - `frontend/components/applications/ApplicationForm.tsx` - Apply form
  - `frontend/components/applications/ApplicationCard.tsx` - Application card
  - `frontend/components/applications/ApplicationStatus.tsx` - Status badge
  - `frontend/components/resume/ResumeUpload.tsx` - Resume upload component
  - `frontend/services/application-service.ts` - Application API calls

#### Frontend - Application Review (Employers)
- **Files to Create:**
  - `frontend/app/employer/applications/page.tsx` - All applications
  - `frontend/app/employer/jobs/[id]/applications/page.tsx` - Job's applications
  - `frontend/app/employer/applications/[id]/page.tsx` - Application review
  - `frontend/components/employer/ApplicationList.tsx` - Applications list
  - `frontend/components/employer/ApplicationReview.tsx` - Review component
  - `frontend/components/employer/CandidateCard.tsx` - Candidate card
  - `frontend/components/employer/StatusUpdate.tsx` - Status changer

#### Frontend - Interviews
- **Files to Create:**
  - `frontend/app/interviews/page.tsx` - Interviews list (both roles)
  - `frontend/app/employer/interviews/schedule/page.tsx` - Schedule interview
  - `frontend/components/interviews/InterviewCard.tsx` - Interview card
  - `frontend/components/interviews/InterviewForm.tsx` - Schedule form
  - `frontend/components/interviews/InterviewCalendar.tsx` - Calendar view
  - `frontend/services/interview-service.ts` - Interview API calls

#### File Storage Setup
- **Configure:**
  - AWS S3 bucket (or alternative: Cloudinary, local storage)
  - File validation (size, type: PDF, DOCX only)
  - Secure file URLs (signed URLs for S3)
  - Virus scanning (optional but recommended)

### Dependencies
- Phase 2 (need jobs to apply to)
- Phase 1 (need authentication)

### Acceptance Criteria
- ✓ Job seekers can apply to jobs with resume
- ✓ Job seekers can upload and manage multiple resumes
- ✓ Job seekers can track application status
- ✓ Employers can view all applications for their jobs
- ✓ Employers can update application status
- ✓ Employers can shortlist candidates
- ✓ Interview scheduling works with time slots
- ✓ Duplicate applications are prevented
- ✓ Resume files are stored securely
- ✓ File uploads are validated (type, size)

---

## Phase 4: AI Features & Recommendations

### Purpose
Implement AI-powered features including resume parsing, job recommendations, candidate matching, and semantic search.

### Deliverables
- ✅ Resume parsing (extract skills, experience)
- ✅ Job recommendations for job seekers
- ✅ Candidate recommendations for employers
- ✅ Semantic job search using embeddings
- ✅ Candidate ranking algorithm
- ✅ Skills extraction and matching

### Technical Tasks

#### Backend - AI Infrastructure Setup
- **Files to Create:**
  - `backend/ai/providers/openai_provider.py` - OpenAI client wrapper
  - `backend/ai/providers/anthropic_provider.py` - Anthropic client wrapper
  - `backend/ai/providers/embeddings_provider.py` - Embedding model wrapper
  - `backend/core/ai_config.py` - AI model configuration

- **Dependencies to Install:**
  ```bash
  uv add langchain langchain-openai langchain-anthropic
  uv add chromadb
  uv add pypdf python-docx  # for resume parsing
  uv add tiktoken  # token counting
  ```

#### Backend - Vector Store Setup
- **Files to Create:**
  - `backend/ai/rag/vector_store.py` - ChromaDB initialization
  - `backend/ai/rag/embeddings.py` - Generate and store embeddings
  - `backend/ai/rag/retrieval.py` - Vector search functions

- **Collections to Create:**
  - `job_embeddings` - Job description vectors
  - `resume_embeddings` - Resume content vectors
  - `skill_embeddings` - Skills taxonomy vectors

#### Backend - Resume Parsing
- **Files to Create:**
  - `backend/ai/chains/resume_parser_chain.py` - LangChain resume parsing
  - `backend/services/resume_parser_service.py` - Resume parsing service
  - `backend/model/parsed_resume.py` - Parsed resume data model

- **Parsing Functions:**
  - `extract_text_from_pdf()`, `extract_text_from_docx()`
  - `parse_resume_with_llm()` - Use LLM to extract structured data
  - `extract_skills()`, `extract_experience()`, `extract_education()`
  - `store_parsed_resume()` - Save to database

- **Parsed Resume Fields:**
  ```python
  - name: str
  - email: str
  - phone: Optional[str]
  - skills: List[str]
  - experience: List[Dict] (company, title, duration, description)
  - education: List[Dict] (institution, degree, field, year)
  - certifications: List[str]
  - summary: str
  ```

#### Backend - Job Recommendations
- **Files to Create:**
  - `backend/ai/chains/job_recommendation_chain.py` - Recommendation logic
  - `backend/services/recommendation_service.py` - Recommendation service
  - `backend/model/recommendation.py` - Recommendation model

- **Recommendation Functions:**
  - `generate_job_recommendations(job_seeker_id, limit)` - Get personalized jobs
  - `calculate_match_score(job, job_seeker)` - Similarity score
  - `get_similar_jobs(job_id)` - Find similar jobs
  - `update_recommendations_cache()` - Periodic refresh

- **Recommendation Algorithm:**
  - Vector similarity (resume vs job description)
  - Skills matching score
  - Location preference matching
  - Experience level matching
  - Weighted scoring system

#### Backend - Candidate Matching
- **Files to Create:**
  - `backend/ai/chains/candidate_matching_chain.py` - Matching logic
  - `backend/services/matching_service.py` - Candidate matching service

- **Matching Functions:**
  - `rank_candidates_for_job(job_id)` - Rank all applicants
  - `find_candidates_for_job(job_id, limit)` - Proactive candidate search
  - `calculate_candidate_fit_score(application_id)` - Fit percentage

- **Ranking Factors:**
  - Skills match percentage
  - Experience relevance
  - Location match
  - Vector similarity score
  - Application recency
  - Weighted composite score

#### Backend - Semantic Search
- **Files to Create:**
  - `backend/ai/rag/semantic_search.py` - Semantic search implementation
  - `backend/services/semantic_search_service.py` - Search service

- **Search Functions:**
  - `semantic_job_search(query, filters)` - Natural language job search
  - `hybrid_search(query, filters)` - Combine keyword + semantic
  - `get_job_embedding(job_id)`, `get_resume_embedding(resume_id)`

#### Backend - AI Prompts
- **Files to Create:**
  - `backend/ai/prompts/resume_parser_prompt.py` - Resume parsing prompt
  - `backend/ai/prompts/job_summary_prompt.py` - Job summarization
  - `backend/ai/prompts/skill_extraction_prompt.py` - Skills extraction
  - `backend/ai/prompts/match_explanation_prompt.py` - Explain match score

#### Backend - Routers
- **Files to Create:**
  - `backend/api/v1/routes/recommendation_router.py` - Recommendation endpoints
  - `backend/api/v1/routes/ai_router.py` - AI utilities endpoints

- **Endpoints:**
  ```
  GET    /api/v1/recommendations/jobs          (job seeker)
  GET    /api/v1/recommendations/candidates/:jobId (employer)
  
  POST   /api/v1/ai/parse-resume               (upload & parse)
  GET    /api/v1/ai/match-score/:applicationId (get fit score)
  POST   /api/v1/ai/semantic-search            (natural language search)
  
  GET    /api/v1/jobs/:id/similar              (similar jobs)
  GET    /api/v1/applications/:id/match-explanation
  ```

#### Backend - Workers/Tasks
- **Files to Create:**
  - `backend/workers/tasks/embedding_tasks.py` - Generate embeddings async
  - `backend/workers/tasks/recommendation_tasks.py` - Update recommendations

- **Background Tasks:**
  - Generate embeddings when job is created
  - Generate embeddings when resume is uploaded
  - Refresh recommendations daily
  - Update candidate rankings when new applications arrive

#### Frontend - AI Features
- **Files to Create:**
  - `frontend/app/recommendations/page.tsx` - Job recommendations page
  - `frontend/app/employer/candidates/[jobId]/page.tsx` - Candidate matches
  - `frontend/components/ai/RecommendationCard.tsx` - Recommended job card
  - `frontend/components/ai/MatchScore.tsx` - Match percentage display
  - `frontend/components/ai/SkillsMatch.tsx` - Skills comparison
  - `frontend/components/ai/ResumeParser.tsx` - Upload & parse UI
  - `frontend/components/search/SemanticSearch.tsx` - Natural language search
  - `frontend/services/ai-service.ts` - AI API calls
  - `frontend/services/recommendation-service.ts` - Recommendation APIs

#### Vector Database Setup
- **Tasks:**
  - Initialize ChromaDB collections
  - Create embedding pipelines
  - Set up similarity search indexes
  - Configure distance metrics (cosine similarity)

#### Model Configuration
- **Configure:**
  - Primary: OpenAI GPT-4o for parsing and generation
  - Embeddings: OpenAI text-embedding-3-small
  - Fallback: Open-source models (sentence-transformers)
  - Rate limiting and cost controls
  - Caching for repeated queries

### Dependencies
- Phase 2 (need jobs and search functionality)
- Phase 3 (need applications and resumes)

### Acceptance Criteria
- ✓ Resume parsing extracts key information accurately (>80% accuracy)
- ✓ Job recommendations are relevant and personalized
- ✓ Candidate matching provides ranked lists
- ✓ Match scores are explainable and meaningful
- ✓ Semantic search understands natural language queries
- ✓ Embeddings are generated for all jobs and resumes
- ✓ AI responses are delivered within 2 seconds
- ✓ Fallback mechanisms work when primary AI is unavailable
- ✓ AI costs are monitored and controlled

---

## Phase 5: Notifications & Polish

### Purpose
Implement notification system, email alerts, and final polish for production readiness.

### Deliverables
- ✅ Email notification system
- ✅ Job alert subscriptions
- ✅ Application status notifications
- ✅ Interview reminders
- ✅ Dashboard improvements
- ✅ Error handling improvements
- ✅ Performance optimizations
- ✅ Documentation

### Technical Tasks

#### Backend - Notifications
- **Files to Create:**
  - `backend/model/notification.py` - Notification model
  - `backend/model/email_template.py` - Email template model
  - `backend/services/notification_service.py` - Notification logic
  - `backend/services/email_service.py` - Email sending service
  - `backend/workers/tasks/email_tasks.py` - Async email tasks
  - `backend/utils/email_templates.py` - HTML email templates

- **Dependencies to Install:**
  ```bash
  uv add fastapi-mail  # or use SendGrid/AWS SES SDK
  uv add jinja2  # for email templates
  ```

- **Notification Types:**
  - New job matches your profile
  - Application status update
  - New application received (employer)
  - Interview scheduled/reminder
  - Password reset
  - Account verification

#### Backend - Job Alerts
- **Files to Create:**
  - `backend/model/job_alert.py` - Alert subscription model
  - `backend/services/job_alert_service.py` - Alert logic
  - `backend/workers/tasks/alert_tasks.py` - Daily alert generation

- **Alert Fields:**
  ```python
  - user_id: PydanticObjectId
  - keywords: List[str]
  - location: Optional[str]
  - job_type: Optional[List[str]]
  - frequency: Literal["instant", "daily", "weekly"]
  - is_active: bool
  ```

#### Backend - Routers
- **Files to Create:**
  - `backend/api/v1/routes/notification_router.py` - Notification endpoints
  - `backend/api/v1/routes/alert_router.py` - Job alert endpoints

- **Endpoints:**
  ```
  GET    /api/v1/notifications
  PATCH  /api/v1/notifications/:id/read
  DELETE /api/v1/notifications/:id
  
  POST   /api/v1/alerts                (create job alert)
  GET    /api/v1/alerts
  PUT    /api/v1/alerts/:id
  DELETE /api/v1/alerts/:id
  PATCH  /api/v1/alerts/:id/toggle    (activate/deactivate)
  ```

#### Backend - Email Templates
- **Create Templates:**
  - Welcome email (with verification link)
  - Job alert email (list of matching jobs)
  - Application received (for employers)
  - Application status update (for job seekers)
  - Interview scheduled (both parties)
  - Interview reminder (24 hours before)
  - Password reset email

#### Backend - Dashboard APIs
- **Files to Create:**
  - `backend/api/v1/routes/dashboard_router.py` - Dashboard data endpoints
  - `backend/services/analytics_service.py` - Dashboard statistics

- **Dashboard Endpoints:**
  ```
  GET /api/v1/dashboard/job-seeker     (applications, saved, recommended)
  GET /api/v1/dashboard/employer       (jobs, applications, interviews)
  GET /api/v1/dashboard/stats          (counts, charts data)
  ```

#### Frontend - Notifications
- **Files to Create:**
  - `frontend/app/notifications/page.tsx` - Notifications page
  - `frontend/components/notifications/NotificationBell.tsx` - Header bell
  - `frontend/components/notifications/NotificationList.tsx` - List component
  - `frontend/components/notifications/NotificationItem.tsx` - Single notification
  - `frontend/services/notification-service.ts` - Notification APIs
  - `frontend/hooks/useNotifications.ts` - Notification hook with polling

#### Frontend - Job Alerts
- **Files to Create:**
  - `frontend/app/alerts/page.tsx` - Manage job alerts
  - `frontend/components/alerts/AlertForm.tsx` - Create/edit alert
  - `frontend/components/alerts/AlertCard.tsx` - Alert display
  - `frontend/services/alert-service.ts` - Alert APIs

#### Frontend - Dashboards
- **Files to Create:**
  - `frontend/app/dashboard/page.tsx` - Main dashboard (role-based)
  - `frontend/components/dashboard/JobSeekerDashboard.tsx` - Job seeker view
  - `frontend/components/dashboard/EmployerDashboard.tsx` - Employer view
  - `frontend/components/dashboard/StatsCard.tsx` - Statistics card
  - `frontend/components/dashboard/RecentActivity.tsx` - Activity feed
  - `frontend/components/dashboard/QuickActions.tsx` - Quick action buttons

#### Performance Optimizations
- **Backend:**
  - Add Redis caching for frequently accessed data
  - Optimize database queries (add missing indexes)
  - Implement rate limiting on endpoints
  - Add request/response compression
  - Implement pagination on all list endpoints

- **Frontend:**
  - Lazy load components
  - Implement infinite scroll for lists
  - Add skeleton loaders
  - Optimize images (Next.js Image component)
  - Add service worker for offline support

#### Documentation
- **Create:**
  - API documentation (Swagger/OpenAPI)
  - ERD diagram (database relationships)
  - Architecture diagram (system components)
  - README with setup instructions
  - Environment variables documentation
  - Deployment guide

#### Testing
- **Backend:**
  - Unit tests for services (pytest)
  - Integration tests for routers
  - Test coverage >70%

- **Frontend:**
  - Component tests (Jest + React Testing Library)
  - E2E tests for critical flows (Playwright)

### Dependencies
- Phase 3 (need applications and interviews)
- Phase 4 (need recommendations for alerts)

### Acceptance Criteria
- ✓ Users receive email notifications for important events
- ✓ Job alerts deliver matching jobs based on preferences
- ✓ Notifications appear in-app with real-time updates
- ✓ Dashboard shows personalized, relevant information
- ✓ Email templates are professional and branded
- ✓ System handles 10,000+ concurrent users
- ✓ API response times <200ms for standard queries
- ✓ Documentation is complete and accurate
- ✓ ERD and architecture diagrams are created
- ✓ Critical user flows are tested

---

## Post-Launch Considerations

### Phase 6: Future Enhancements (Post-MVP)
- Real-time chat/messaging between employers and candidates
- Video interview integration (Zoom/Google Meet)
- Advanced analytics dashboard for employers
- Mobile app (React Native)
- Social media integration (LinkedIn import)
- Applicant tracking system (ATS) integrations
- Payment system for premium features
- Admin panel for platform management
- Multi-language support
- Company reviews and ratings
- Salary insights and market data
- Skills assessment tests
- Referral system
- Job fairs/virtual events

---

## Risk Mitigation

### Technical Risks
| Risk | Mitigation Strategy |
|------|---------------------|
| AI API costs exceed budget | Implement caching, rate limiting, use fallback models |
| Vector search performance issues | Optimize indexes, use hybrid search, implement pagination |
| File storage costs | Set file size limits, implement cleanup policies |
| Database performance degradation | Add proper indexes, implement caching layer (Redis) |
| Third-party API downtime | Implement circuit breakers, fallback mechanisms |

### Development Risks
| Risk | Mitigation Strategy |
|------|---------------------|
| Timeline delays | Phased approach allows partial launches |
| Feature creep | Stick to MVP scope, defer enhancements |
| Team availability | Clear documentation, modular architecture |
| Integration complexity | Start with simple implementations, iterate |

---

## Success Metrics

### Phase 1-2 Success Metrics
- 100+ registered users (50 job seekers, 50 employers)
- 50+ job postings
- User registration flow completion rate >80%

### Phase 3 Success Metrics
- 200+ job applications submitted
- Application-to-interview conversion >10%
- Resume upload success rate >95%

### Phase 4 Success Metrics
- AI recommendation accuracy >70%
- Resume parsing accuracy >80%
- User engagement with recommendations >30%

### Phase 5 Success Metrics
- Email delivery rate >98%
- Notification open rate >40%
- Dashboard daily active users >60%

---

## Technical Stack Summary

### Backend
- Python 3.11+, FastAPI, Uvicorn
- MongoDB 6.x, Beanie ODM
- ChromaDB (vector store)
- LangChain, OpenAI/Anthropic
- Redis (caching)
- Celery (background tasks)
- Docker

### Frontend
- Next.js 14 (App Router)
- TypeScript, React 18
- Tailwind CSS
- Zustand/Redux (state)
- Axios (API client)
- Jest, Playwright (testing)

### Infrastructure
- Docker Compose (development)
- MongoDB Atlas (database)
- AWS S3 (file storage)
- SendGrid/AWS SES (email)
- Vercel/AWS (hosting)

---

## Conclusion

This phased implementation plan provides a structured approach to building the JobPortal platform. Each phase builds upon the previous one, ensuring a solid foundation before adding complex features. The AI capabilities in Phase 4 are built on top of a working job board, allowing for iteration and improvement based on real data.

Key priorities:
1. **Phase 0-1**: Get authentication and user management right
2. **Phase 2-3**: Build core job board functionality
3. **Phase 4**: Layer in AI features for differentiation
4. **Phase 5**: Polish and prepare for production

Estimated total timeline: **12-18 weeks** for MVP (Phases 0-5)

