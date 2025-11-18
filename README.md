# Work Atlas

A secure, scalable, and user-friendly platform connecting job seekers and employers with AI-powered recommendations. Work Atlas leverages vector similarity search and large language models to provide intelligent job matching with detailed compatibility scores.

## Features

- **AI-Powered Job Matching**: Intelligent recommendations for job seekers based on skills, education, experience, and pay expectations
- **Candidate Recommendations**: Employers receive AI-scored candidate matches for their job postings
- **Vector Search**: ChromaDB-powered semantic search for efficient matching
- **Interview Scheduling**: Automated email notifications via n8n workflows
- **User Authentication**: Secure JWT-based authentication for seekers and employers
- **Real-time Status Monitoring**: Dashboard indicators for service health

---

## Project Setup

### Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose v2.0+

### Quick Start

1. **Copy environment variables:**
   ```bash
   cp env.template .env
   ```
   Edit `.env` and fill in your configuration values (MongoDB credentials, API keys, etc.).

2. **Start all services:**
   ```bash
   docker compose up
   ```
   This starts the backend API, frontend, and n8n services.

3. **Access the application:**
   - Backend API: `http://localhost:8000`
   - Frontend: `http://localhost:3000`
   - n8n UI: `http://localhost:5678`

### Docker Commands

```bash
# Rebuild containers
docker compose up --build

# Stop and remove containers
docker compose down
docker compose down -v --remove-orphans # Removes volumes and orphaned (old) containers

# View running containers
docker ps

# View logs
docker compose logs backend
docker compose logs frontend
docker compose logs n8n
```

Backend logs are also available at `./backend/Logs/` when running the application.

### Utility Scripts `./scripts`:
```Powershell
# (Windows) Ingest all chroma db data into local CHROMA_PC_PATH
./ingest_all.bat
```
```bash
# (Linux/macOS) Ingest all chroma db data into local CHROMA_PC_PATH
./ingest_all.sh
```
```Powershell
# (Windows) Sync all chroma and mongo data
./sync_all.bat
```
```bash
# (Linux/macOS) Sync all chroma and mongo data
./sync_all.sh
```
### Environment Variables

Key environment variables (see `env.template` for full list):
- `MONGO_DB_URL` - MongoDB connection string
- `OPENAI_API_KEY` - OpenAI API key for embeddings and LLM
- `N8N_API_URL` - n8n service URL (default: `http://n8n:5678`)
- `N8N_WEBHOOK_URL` - n8n webhook URL for interview scheduling
- `CORS_ORIGINS` - Allowed frontend origins

---

## Backend

### Tech Stack

- **Framework**: FastAPI (Python 3.12+)
- **Package Manager**: uv
- **Database**: MongoDB 6.x (Atlas) with Beanie ODM
- **Vector Store**: ChromaDB with OpenAI embeddings (text-embedding-3-small)
- **AI/LLM**: LangChain with OpenAI GPT-4o-mini
- **Authentication**: JWT (python-jose)
- **Logging**: Loguru
- **HTTP Client**: httpx (for n8n integration)

### Structure

```
backend/
├── api/v1/routes/          # API route handlers
│   ├── auth_router.py      # Authentication endpoints
│   ├── seeker_router.py    # Job seeker endpoints
│   └── employer_router.py  # Employer endpoints
├── ai/
│   ├── chains/             # LangChain matching services
│   │   ├── matching_service.py        # Seeker-to-job matching
│   │   ├── candidate_matching_service.py # Job-to-candidate matching
│   │   └── scoring_chain.py            # LLM-based scoring
│   └── rag/
│       └── vector_store.py # ChromaDB interface
├── core/
│   ├── ai_config.py        # AI/LLM configuration
│   └── security.py         # JWT and password hashing
├── db/
│   ├── settings.py         # MongoDB and ChromaDB setup
│   ├── seeker_db_ops.py    # Seeker CRUD operations
│   ├── employer_db_ops.py  # Employer CRUD operations
│   └── chroma_crud_ops.py  # ChromaDB operations
├── services/
│   ├── seeker_services.py  # Seeker business logic
│   ├── employer_services.py # Employer business logic
│   └── n8n_service.py     # n8n integration
├── schemas/
│   ├── seeker.py           # Pydantic models for seekers
│   └── employer.py         # Pydantic models for employers
└── main.py                 # FastAPI application entry point
```

### Key Components

- **Matching Services**: Use ChromaDB for vector similarity search, then LangChain for detailed scoring
- **RAG Pipeline**: Vector embeddings stored in ChromaDB collections (Seeker_Resume, Employer_JobDescr)
- **API Routes**: RESTful endpoints for authentication, job management, recommendations, and interview scheduling
- **Database Operations**: Async MongoDB operations using Beanie ODM with Motor

---

## Frontend

### Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **UI Library**: React 18
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Icons**: Lucide React

### Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── seeker/            # Job seeker pages
│   │   ├── dashboard/     # Seeker dashboard
│   │   ├── jobs/         # Browse jobs
│   │   ├── recommendations/ # AI job recommendations
│   │   ├── applications/ # Application history
│   │   └── profile/      # Profile management
│   ├── employer/         # Employer pages
│   │   ├── dashboard/    # Employer dashboard
│   │   ├── jobs/         # Job posting management
│   │   │   └── [jobId]/
│   │   │       └── candidates/ # AI candidate recommendations
│   │   ├── applications/ # Received applications
│   │   └── profile/      # Company profile
│   ├── login/            # Login page
│   └── register/        # Registration page
├── services/             # API service layer
│   ├── auth-service.ts   # Authentication API calls
│   ├── seeker-service.ts # Seeker API calls
│   └── employer-service.ts # Employer API calls
├── store/                # Zustand state management
│   └── auth-store.ts     # Authentication state
├── hooks/                # React hooks
│   └── useAuth.ts        # Authentication hook
├── lib/
│   └── api.ts            # Axios client configuration
└── types/
    └── index.ts          # TypeScript type definitions
```

### Key Features

- **Server-Side Rendering**: Next.js App Router with server components
- **Client-Side State**: Zustand for global authentication state
- **API Integration**: Centralized Axios client with interceptors for auth tokens
- **Responsive Design**: Tailwind CSS for mobile-first responsive layouts
- **Type Safety**: Full TypeScript coverage for API responses and components

---

## n8n and LangChain Integration

### LangChain Usage

LangChain powers the AI matching and scoring system:

1. **Scoring Chain** (`backend/ai/chains/scoring_chain.py`):
   - Uses GPT-4o-mini to analyze job-seeker compatibility
   - Calculates detailed match scores (0-100%) across multiple factors:
     - Skills overlap (40% weight)
     - Education compatibility (20% weight)
     - Pay range alignment (20% weight)
     - Experience relevance (20% weight)
   - Returns structured score breakdowns with reasoning

2. **Matching Services**:
   - **Seeker Matching** (`matching_service.py`): Matches job seekers to job postings
   - **Candidate Matching** (`candidate_matching_service.py`): Matches employers to candidates
   - Both services use a two-stage approach:
     1. Vector similarity search in ChromaDB for initial candidate filtering
     2. LangChain scoring chain for detailed analysis and ranking

3. **Vector Store Integration**:
   - ChromaDB stores embeddings for seekers (resumes) and jobs (descriptions)
   - OpenAI `text-embedding-3-small` model generates embeddings
   - Vector search provides fast semantic similarity matching

4. **LangSmith Tracing** (Optional):
   - Configure `LANGSMITH_API_KEY` and `LANGSMITH_TRACING=true` in `.env`
   - Automatically traces all LLM calls for debugging and optimization

### n8n Usage

n8n handles workflow automation for email notifications:

1. **Interview Scheduling Workflow**:
   - Webhook trigger receives interview details from backend
   - Email node sends formatted interview notifications to candidates
   - Configurable email templates with dynamic data (date, time, location, etc.)

2. **Integration Points**:
   - **Backend Service** (`backend/services/n8n_service.py`):
     - `check_n8n_connection()`: Health check for n8n availability
     - `trigger_interview_workflow()`: Sends interview details to n8n webhook
   - **API Endpoint**: `POST /api/v1/employers/jobs/{job_id}/candidates/{seeker_id}/schedule-interview`
   - **Status Monitoring**: `GET /api/v1/employers/n8n/status` for connection status

3. **Workflow Setup**:
   - Access n8n UI at `http://localhost:5678`
   - Create workflow with webhook trigger at `/webhook/interview-schedule`
   - Configure email node (SMTP, Gmail, SendGrid, etc.)
   - Activate workflow to receive requests

4. **Data Flow**:
   ```
   Employer schedules interview
   → Backend API receives request
   → n8n_service triggers webhook
   → n8n workflow processes request
   → Email sent to candidate
   → Status returned to frontend
   ```

### Configuration

**LangChain**:
- Set `OPENAI_API_KEY` in `.env`
- Optional: Set `LANGSMITH_API_KEY` for tracing
- Model: `gpt-4o-mini` (configurable via `OPENAI_MODEL`)

**n8n**:
- Set `N8N_API_URL=http://n8n:5678` (Docker) or `http://localhost:5678` (local)
- Set `N8N_WEBHOOK_URL` after creating workflow in n8n UI
- Workflows persist in `./n8n_data` directory

---

## Project Structure

- `backend/` - FastAPI backend application
- `frontend/` - Next.js frontend application
- `docker-compose.yml` - Docker Compose configuration
- `env.template` - Environment variables template
- `chroma_db/` - ChromaDB persistent storage
- `n8n_data/` - n8n workflow persistence
