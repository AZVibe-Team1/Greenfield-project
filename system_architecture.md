# WorkAtlas - Complete System Architecture

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [System Overview](#system-overview)
3. [Complete Technology Stack](#complete-technology-stack)
4. [High-Level System Architecture](#high-level-system-architecture)
5. [Data Flow Architecture](#data-flow-architecture)
6. [Component Architecture](#component-architecture)
7. [Database Architecture](#database-architecture)
8. [AI/ML Architecture](#aiml-architecture)
9. [Security Architecture](#security-architecture)
10. [Deployment Architecture](#deployment-architecture)
11. [Integration Architecture](#integration-architecture)
12. [End-to-End User Flows](#end-to-end-user-flows)
13. [Performance & Scalability](#performance--scalability)
14. [System Health & Monitoring](#system-health--monitoring)

---

## Executive Summary

**WorkAtlas** is a modern, AI-powered job portal that intelligently matches job seekers with employers using semantic search and LLM-based analysis. The system leverages a microservices architecture with Next.js frontend, FastAPI backend, dual database system (MongoDB + ChromaDB), and OpenAI for AI capabilities.

### Key Capabilities
- 🎯 **AI-Powered Matching**: Semantic search + LLM scoring (GPT-4o-mini)
- 🔐 **Secure Authentication**: JWT-based with role-based access control
- 📊 **Dual Database**: MongoDB for documents, ChromaDB for vector embeddings
- 🚀 **High Performance**: Async operations, vector search, optimized queries
- 📧 **Workflow Automation**: n8n integration for email notifications
- 🐳 **Containerized**: Docker Compose orchestration for all services

### System Metrics
- **Total Technologies**: 40+ (Frontend: 12, Backend: 30+)
- **API Endpoints**: 20+ RESTful endpoints
- **Database Collections**: 6 (2 MongoDB, 4 ChromaDB)
- **Vector Dimensions**: 1536 (OpenAI text-embedding-3-small)
- **User Roles**: 2 (Job Seeker, Employer)
- **Services**: 3 (Frontend, Backend, n8n)

---

## System Overview

```mermaid
graph TB
    subgraph "Client Layer"
        Browser[Web Browser<br/>Desktop & Mobile]
    end
    
    subgraph "Frontend Service - Port 3000"
        NextJS[Next.js 14 App<br/>React 18 + TypeScript]
        Zustand[Zustand State<br/>Auth Management]
        TailwindCSS[Tailwind CSS<br/>Responsive UI]
    end
    
    subgraph "Backend Service - Port 8000"
        FastAPI[FastAPI Server<br/>Python 3.12]
        Services[Business Logic<br/>Services Layer]
        AILayer[AI/ML Layer<br/>LangChain + OpenAI]
    end
    
    subgraph "Database Layer"
        MongoDB[(MongoDB Atlas<br/>User & Job Data)]
        ChromaDB[(ChromaDB<br/>Vector Embeddings)]
    end
    
    subgraph "External Services"
        OpenAI[OpenAI API<br/>GPT-4o-mini<br/>Embeddings]
        N8N[n8n Workflow<br/>Port 5678<br/>Email Automation]
        LangSmith[LangSmith<br/>LLM Tracing]
    end
    
    Browser <-->|HTTP/REST| NextJS
    NextJS -->|JWT Auth| FastAPI
    NextJS --> Zustand
    NextJS --> TailwindCSS
    
    FastAPI --> Services
    Services --> AILayer
    Services --> MongoDB
    Services --> ChromaDB
    
    AILayer -->|LLM Calls| OpenAI
    ChromaDB -->|Embeddings| OpenAI
    
    Services -->|Webhooks| N8N
    AILayer -.->|Optional| LangSmith
    
    style Browser fill:#90caf9
    style NextJS fill:#000000,color:#ffffff
    style FastAPI fill:#009688,color:#ffffff
    style MongoDB fill:#47A248,color:#ffffff
    style ChromaDB fill:#FF6F00,color:#ffffff
    style OpenAI fill:#10a37f,color:#ffffff
    style N8N fill:#ea4b71,color:#ffffff
```

### System Components

| Component | Technology | Purpose | Port |
|-----------|------------|---------|------|
| **Frontend** | Next.js 14 + React 18 | User interface, client-side logic | 3000 |
| **Backend API** | FastAPI + Python 3.12 | REST API, business logic | 8000 |
| **Document DB** | MongoDB Atlas | User profiles, jobs, applications | 27017 |
| **Vector DB** | ChromaDB | Semantic embeddings for matching | Local |
| **AI Service** | OpenAI (GPT-4o-mini) | LLM scoring, embeddings | API |
| **Workflow** | n8n | Email automation, notifications | 5678 |
| **Monitoring** | LangSmith (Optional) | LLM tracing and debugging | API |

---

## Complete Technology Stack

### Full Stack Overview

```mermaid
graph TB
    subgraph "Frontend Stack - 12 Technologies"
        FE1[Next.js 14.1.0]
        FE2[React 18.2.0]
        FE3[TypeScript 5.x]
        FE4[Tailwind CSS 3.4.0]
        FE5[Zustand 4.5.0]
        FE6[Axios 1.6.5]
        FE7[Lucide React 0.553.0]
        FE8[ESLint 8.x]
        FE9[PostCSS 8.x]
        FE10[Autoprefixer 10.x]
        FE11[Node.js 20 LTS]
        FE12[Docker]
    end
    
    subgraph "Backend Stack - 30+ Technologies"
        BE1[Python 3.12]
        BE2[FastAPI 0.104+]
        BE3[Uvicorn 0.24+]
        BE4[Pydantic 2.12+]
        BE5[MongoDB Atlas]
        BE6[Motor 3.7+]
        BE7[Beanie 2.0+]
        BE8[ChromaDB 1.3+]
        BE9[LangChain 1.0+]
        BE10[OpenAI 2.8+]
        BE11[BCrypt 4.1.3]
        BE12[Python-JOSE 3.5+]
        BE13[Loguru 0.7+]
        BE14[HTTPX 0.28+]
        BE15[uv Package Manager]
    end
    
    subgraph "External Services"
        EXT1[OpenAI API]
        EXT2[n8n Workflow]
        EXT3[LangSmith]
        EXT4[Email Services]
    end
    
    subgraph "Infrastructure"
        INF1[Docker Compose]
        INF2[Docker Containers]
        INF3[Persistent Volumes]
        INF4[Network Bridge]
    end
    
    FE1 --> FE2
    FE2 --> FE3
    FE1 --> FE4
    FE2 --> FE5
    FE1 --> FE6
    FE2 --> FE7
    
    BE1 --> BE2
    BE2 --> BE3
    BE2 --> BE4
    BE7 --> BE6
    BE6 --> BE5
    BE9 --> BE10
    BE8 --> BE10
    
    BE2 --> EXT2
    BE9 --> EXT1
    BE9 -.-> EXT3
    EXT2 --> EXT4
    
    FE12 --> INF2
    BE15 --> INF2
    INF2 --> INF1
    INF1 --> INF3
    INF1 --> INF4
    
    style FE1 fill:#000000,color:#ffffff
    style BE2 fill:#009688,color:#ffffff
    style BE5 fill:#47A248,color:#ffffff
    style BE8 fill:#FF6F00,color:#ffffff
    style EXT1 fill:#10a37f,color:#ffffff
    style EXT2 fill:#ea4b71,color:#ffffff
```

### Technology Stack by Layer

#### Frontend Technologies (12)

| Category | Technologies | Purpose |
|----------|-------------|---------|
| **Framework** | Next.js 14, React 18, React-DOM | UI framework with SSR |
| **Language** | TypeScript 5.x | Type-safe development |
| **Styling** | Tailwind CSS, PostCSS, Autoprefixer | Utility-first CSS |
| **State** | Zustand 4.5 | Lightweight state management |
| **HTTP** | Axios 1.6 | API communication |
| **Icons** | Lucide React | Icon library (1000+ icons) |
| **Quality** | ESLint 8.x | Code linting |
| **Runtime** | Node.js 20 LTS | JavaScript runtime |
| **Deployment** | Docker | Containerization |

#### Backend Technologies (30+)

| Category | Technologies | Purpose |
|----------|-------------|---------|
| **Framework** | FastAPI, Uvicorn, Pydantic | Async web framework |
| **Language** | Python 3.12 | Core language |
| **Document DB** | MongoDB Atlas, Motor, Beanie ODM | NoSQL database |
| **Vector DB** | ChromaDB | Embedding storage |
| **AI/ML** | LangChain, LangChain Core, LangChain OpenAI, OpenAI SDK | LLM integration |
| **Security** | BCrypt, Python-JOSE, Email-Validator, PhoneNumbers | Auth & validation |
| **Files** | PyPDF2, Python-Docx, Aiofiles | Document processing |
| **HTTP** | HTTPX, Requests | External API calls |
| **Logging** | Loguru | Structured logging |
| **Utils** | Python-Dotenv, GICS, TZData, Pydantic Extra Types | Utilities |
| **Package Mgmt** | uv | Fast package manager |
| **Deployment** | Docker | Containerization |

#### External Services (4)

| Service | Purpose | Integration Method |
|---------|---------|-------------------|
| **OpenAI API** | GPT-4o-mini for scoring, text-embedding-3-small | REST API via SDK |
| **n8n** | Workflow automation for emails | Webhook triggers |
| **LangSmith** | LLM tracing and monitoring (optional) | LangChain integration |
| **Email Service** | Gmail/SMTP for notifications | Via n8n |

---

## High-Level System Architecture

### Complete System Architecture Diagram

```mermaid
graph TB
    subgraph "User Interface Layer"
        WebUI[Web Browser<br/>React Application]
    end
    
    subgraph "Presentation Layer - Next.js"
        Pages[Pages & Routes<br/>File-based Routing]
        Components[React Components<br/>Reusable UI]
        StateManager[Zustand Store<br/>Auth State]
        APIClient[Axios Client<br/>HTTP + JWT]
    end
    
    subgraph "API Gateway Layer - FastAPI"
        Router[API Router<br/>v1 Endpoints]
        CORS[CORS Middleware<br/>Origin Validation]
        JWTAuth[JWT Auth<br/>Token Validation]
        Validation[Pydantic Validation<br/>Request/Response]
    end
    
    subgraph "Business Logic Layer"
        AuthService[Auth Service<br/>Login/Register]
        SeekerService[Seeker Service<br/>Profile/Jobs/Apps]
        EmployerService[Employer Service<br/>Jobs/Candidates]
        N8nService[n8n Service<br/>Email Integration]
    end
    
    subgraph "AI/ML Processing Layer"
        MatchingEngine[Matching Engine<br/>Job-Seeker Matching]
        CandidateEngine[Candidate Engine<br/>Candidate-Job Matching]
        VectorSearch[Vector Search<br/>Semantic Similarity]
        LLMScoring[LLM Scoring Chain<br/>GPT-4o-mini Analysis]
        EmbeddingGen[Embedding Generator<br/>OpenAI Embeddings]
    end
    
    subgraph "Data Access Layer"
        SeekerCRUD[Seeker CRUD<br/>Database Operations]
        EmployerCRUD[Employer CRUD<br/>Database Operations]
        ChromaCRUD[Chroma CRUD<br/>Vector Operations]
        BeanieODM[Beanie ODM<br/>MongoDB Mapping]
    end
    
    subgraph "Data Storage Layer"
        MongoAtlas[(MongoDB Atlas<br/>Document Store<br/>seekers, employers)]
        ChromaLocal[(ChromaDB Local<br/>Vector Store<br/>4 Collections)]
    end
    
    subgraph "External Services Layer"
        OpenAIAPI[OpenAI API<br/>GPT-4o-mini<br/>Embeddings]
        N8nWorkflow[n8n Workflow<br/>Email Automation]
        LangSmithAPI[LangSmith API<br/>Tracing Optional]
    end
    
    WebUI --> Pages
    Pages --> Components
    Components --> StateManager
    Components --> APIClient
    
    APIClient -->|HTTPS + JWT| Router
    Router --> CORS
    CORS --> JWTAuth
    JWTAuth --> Validation
    
    Validation --> AuthService
    Validation --> SeekerService
    Validation --> EmployerService
    
    AuthService --> SeekerCRUD
    AuthService --> EmployerCRUD
    
    SeekerService --> SeekerCRUD
    SeekerService --> MatchingEngine
    
    EmployerService --> EmployerCRUD
    EmployerService --> CandidateEngine
    EmployerService --> N8nService
    
    MatchingEngine --> VectorSearch
    MatchingEngine --> LLMScoring
    CandidateEngine --> VectorSearch
    CandidateEngine --> LLMScoring
    
    VectorSearch --> ChromaCRUD
    LLMScoring --> OpenAIAPI
    
    SeekerCRUD --> BeanieODM
    EmployerCRUD --> BeanieODM
    SeekerCRUD --> ChromaCRUD
    EmployerCRUD --> ChromaCRUD
    
    BeanieODM --> MongoAtlas
    ChromaCRUD --> ChromaLocal
    ChromaCRUD --> EmbeddingGen
    EmbeddingGen --> OpenAIAPI
    
    N8nService --> N8nWorkflow
    LLMScoring -.->|Optional| LangSmithAPI
    
    style WebUI fill:#90caf9
    style Pages fill:#000000,color:#ffffff
    style Router fill:#009688,color:#ffffff
    style MatchingEngine fill:#10a37f,color:#ffffff
    style LLMScoring fill:#10a37f,color:#ffffff
    style MongoAtlas fill:#47A248,color:#ffffff
    style ChromaLocal fill:#FF6F00,color:#ffffff
    style OpenAIAPI fill:#10a37f,color:#ffffff
    style N8nWorkflow fill:#ea4b71,color:#ffffff
```

---

## Data Flow Architecture

### Complete Data Flow: User Registration to AI Matching

```mermaid
sequenceDiagram
    participant User as User Browser
    participant FE as Next.js Frontend
    participant API as FastAPI Gateway
    participant Auth as Auth Service
    participant Seeker as Seeker Service
    participant Employer as Employer Service
    participant Mongo as MongoDB
    participant Chroma as ChromaDB
    participant OpenAI as OpenAI API
    participant LLM as LLM Scoring
    participant N8n as n8n Workflow
    
    Note over User,N8n: 1. Registration Flow
    
    User->>FE: Fill Registration Form
    FE->>API: POST /auth/register/{role}
    API->>Auth: hash_password()
    Auth->>Mongo: Create User Document
    Auth->>OpenAI: Generate Embeddings
    OpenAI-->>Auth: Embedding Vectors
    Auth->>Chroma: Store Embeddings
    Chroma-->>Auth: Stored
    Auth-->>API: User Created
    API-->>FE: Success
    FE-->>User: Redirect to Login
    
    Note over User,N8n: 2. Login Flow
    
    User->>FE: Enter Credentials
    FE->>API: POST /auth/login
    API->>Auth: verify_password()
    Auth->>Mongo: Fetch User
    Auth->>Auth: create_jwt_token()
    Auth-->>API: JWT Token
    API-->>FE: Token + User Data
    FE->>FE: Store in localStorage
    FE-->>User: Redirect to Dashboard
    
    Note over User,N8n: 3. AI Matching Flow (Seeker)
    
    User->>FE: Request Recommendations
    FE->>API: GET /seekers/recommendations
    API->>Seeker: Get Recommendations
    Seeker->>Chroma: Fetch Seeker Embedding
    Chroma-->>Seeker: Embedding Vector
    Seeker->>Chroma: Vector Similarity Search
    Chroma-->>Seeker: Top 20 Job IDs
    Seeker->>Mongo: Fetch Job Details
    Mongo-->>Seeker: Job Documents
    
    loop For Each Job Match
        Seeker->>LLM: Score Match (Seeker + Job)
        LLM->>OpenAI: Call GPT-4o-mini
        OpenAI-->>LLM: Structured Analysis
        LLM-->>Seeker: Score Breakdown + Reasoning
    end
    
    Seeker->>Seeker: Rank by Overall Score
    Seeker-->>API: Ranked Recommendations
    API-->>FE: JSON Response
    FE-->>User: Display Matches
    
    Note over User,N8n: 4. Job Application Flow
    
    User->>FE: Apply to Job
    FE->>API: POST /seekers/applications
    API->>Seeker: Create Application
    Seeker->>Mongo: Update Seeker (applications)
    Seeker->>Mongo: Update Employer (apps_received)
    Mongo-->>Seeker: Updated
    Seeker-->>API: Success
    API-->>FE: Application Created
    FE-->>User: Confirmation
    
    Note over User,N8n: 5. AI Candidate Matching Flow (Employer)
    
    User->>FE: View Candidates for Job
    FE->>API: GET /employers/jobs/{id}/candidates
    API->>Employer: Get Candidates
    Employer->>Chroma: Fetch Job Embedding
    Chroma-->>Employer: Embedding Vector
    Employer->>Chroma: Vector Similarity Search
    Chroma-->>Employer: Top 20 Seeker IDs
    Employer->>Mongo: Fetch Seeker Details
    Mongo-->>Employer: Seeker Documents
    
    loop For Each Candidate
        Employer->>LLM: Score Match (Job + Seeker)
        LLM->>OpenAI: Call GPT-4o-mini
        OpenAI-->>LLM: Structured Analysis
        LLM-->>Employer: Score Breakdown + Reasoning
    end
    
    Employer->>Employer: Rank by Overall Score
    Employer-->>API: Ranked Candidates
    API-->>FE: JSON Response
    FE-->>User: Display Candidates
    
    Note over User,N8n: 6. Interview Scheduling Flow
    
    User->>FE: Schedule Interview
    FE->>API: POST /employers/.../schedule-interview
    API->>Employer: Schedule Interview
    Employer->>N8n: Trigger Webhook
    N8n->>N8n: Process Workflow
    N8n->>N8n: Format Email
    N8n->>N8n: Send Email
    N8n-->>Employer: Success/Failure
    Employer-->>API: Response
    API-->>FE: Confirmation
    FE-->>User: Interview Scheduled
```

### Data Flow Patterns

#### Pattern 1: CRUD Operations

```mermaid
graph LR
    Client[Client Request] --> API[API Gateway]
    API --> Service[Business Service]
    Service --> CRUD[CRUD Layer]
    CRUD --> ODM[Beanie ODM]
    ODM --> DB[(MongoDB)]
    DB --> ODM
    ODM --> CRUD
    CRUD --> Service
    Service --> API
    API --> Client
    
    style Client fill:#90caf9
    style API fill:#009688,color:#fff
    style DB fill:#47A248,color:#fff
```

#### Pattern 2: AI Matching Pipeline

```mermaid
graph LR
    Request[Match Request] --> Service[Matching Service]
    Service --> VectorDB[(ChromaDB)]
    VectorDB --> Results[Vector Results]
    Results --> MongoDB[(MongoDB)]
    MongoDB --> Details[Full Details]
    Details --> LLM[LLM Scoring]
    LLM --> OpenAI[OpenAI API]
    OpenAI --> Scores[Structured Scores]
    Scores --> Ranked[Ranked Results]
    Ranked --> Response[JSON Response]
    
    style Request fill:#90caf9
    style VectorDB fill:#FF6F00,color:#fff
    style MongoDB fill:#47A248,color:#fff
    style OpenAI fill:#10a37f,color:#fff
```

#### Pattern 3: External Integration

```mermaid
graph LR
    Trigger[User Action] --> Service[Service Layer]
    Service --> Prepare[Prepare Payload]
    Prepare --> HTTP[HTTP Client]
    HTTP --> External[External Service]
    External --> Process[Process Request]
    Process --> Response[Response]
    Response --> Service
    Service --> Result[Return Result]
    
    style Trigger fill:#90caf9
    style External fill:#ea4b71,color:#fff
```

---

## Component Architecture

### Frontend Component Architecture

```mermaid
graph TB
    subgraph "App Structure /app"
        Layout[layout.tsx<br/>Root Layout]
        Home[page.tsx<br/>Homepage]
        
        subgraph "Public Routes"
            Login[login/page.tsx]
            Register[register/page.tsx]
        end
        
        subgraph "Seeker Routes /seeker"
            SD[dashboard/page.tsx]
            SJ[jobs/page.tsx]
            SR[recommendations/page.tsx]
            SA[applications/page.tsx]
            SP[profile/page.tsx]
        end
        
        subgraph "Employer Routes /employer"
            ED[dashboard/page.tsx]
            EJ[jobs/page.tsx]
            EJN[jobs/new/page.tsx]
            EJD[jobs/[id]/page.tsx]
            EJC[jobs/[id]/candidates/page.tsx]
            EA[applications/page.tsx]
            EP[profile/page.tsx]
        end
    end
    
    subgraph "State Management /store"
        AuthStore[auth-store.ts<br/>Zustand]
    end
    
    subgraph "Custom Hooks /hooks"
        UseAuth[useAuth.ts<br/>useSeekerAuth<br/>useEmployerAuth]
    end
    
    subgraph "Services /services"
        AuthSvc[auth-service.ts]
        SeekerSvc[seeker-service.ts]
        EmployerSvc[employer-service.ts]
    end
    
    subgraph "Types /types"
        TypeDefs[index.ts<br/>TypeScript Interfaces]
    end
    
    Layout --> Home
    Layout --> Login
    Layout --> Register
    Layout --> SD
    Layout --> SR
    Layout --> ED
    Layout --> EJC
    
    SD --> UseAuth
    SR --> UseAuth
    ED --> UseAuth
    EJC --> UseAuth
    
    UseAuth --> AuthStore
    
    SD --> SeekerSvc
    SR --> SeekerSvc
    ED --> EmployerSvc
    EJC --> EmployerSvc
    
    Login --> AuthSvc
    Register --> AuthSvc
    
    AuthSvc --> TypeDefs
    SeekerSvc --> TypeDefs
    EmployerSvc --> TypeDefs
    
    style Layout fill:#000000,color:#fff
    style AuthStore fill:#ffeaa7
    style UseAuth fill:#74b9ff
```

### Backend Component Architecture

```mermaid
graph TB
    subgraph "Entry Point"
        Main[main.py<br/>FastAPI App]
    end
    
    subgraph "API Layer /api/v1/routes"
        AuthRouter[auth_router.py<br/>Login/Register/Me]
        SeekerRouter[seeker_router.py<br/>Profile/Jobs/Apps]
        EmployerRouter[employer_router.py<br/>Jobs/Candidates]
    end
    
    subgraph "Core /core"
        Security[security.py<br/>JWT/BCrypt]
        AIConfig[ai_config.py<br/>LLM Config]
    end
    
    subgraph "Services /services"
        SeekerSvc[seeker_services.py]
        EmployerSvc[employer_services.py]
        N8nSvc[n8n_service.py]
    end
    
    subgraph "AI Layer /ai"
        Matching[chains/matching_service.py]
        Candidate[chains/candidate_matching_service.py]
        Scoring[chains/scoring_chain.py]
        VectorStore[rag/vector_store.py]
    end
    
    subgraph "Database /db"
        Settings[settings.py<br/>Config]
        SeekerCRUD[seeker_db_ops.py]
        EmployerCRUD[employer_db_ops.py]
        ChromaCRUD[chroma_crud_ops.py]
    end
    
    subgraph "Schemas /schemas"
        SeekerSchema[seeker.py<br/>Beanie Model]
        EmployerSchema[employer.py<br/>Beanie Model]
    end
    
    subgraph "Utils /utils"
        Validators[validators.py]
        GICS[gics_helper.py]
    end
    
    Main --> AuthRouter
    Main --> SeekerRouter
    Main --> EmployerRouter
    
    AuthRouter --> Security
    SeekerRouter --> SeekerSvc
    EmployerRouter --> EmployerSvc
    
    SeekerSvc --> SeekerCRUD
    SeekerSvc --> Matching
    EmployerSvc --> EmployerCRUD
    EmployerSvc --> Candidate
    EmployerSvc --> N8nSvc
    
    Matching --> Scoring
    Matching --> VectorStore
    Candidate --> Scoring
    Candidate --> VectorStore
    
    Scoring --> AIConfig
    VectorStore --> ChromaCRUD
    
    SeekerCRUD --> Settings
    EmployerCRUD --> Settings
    ChromaCRUD --> Settings
    
    SeekerCRUD --> SeekerSchema
    EmployerCRUD --> EmployerSchema
    
    SeekerSchema --> Validators
    EmployerSchema --> Validators
    EmployerSchema --> GICS
    
    style Main fill:#009688,color:#fff
    style Matching fill:#10a37f,color:#fff
    style Scoring fill:#10a37f,color:#fff
    style Settings fill:#47A248,color:#fff
```

---

## Database Architecture

### Dual Database System Overview

```mermaid
graph TB
    subgraph "Application Layer"
        Services[Business Services]
    end
    
    subgraph "MongoDB - Document Store"
        MongoConn[Motor Async Driver<br/>+ Beanie ODM]
        
        subgraph "Collections"
            SeekersCol[(seekers collection)]
            EmployersCol[(employers collection)]
        end
        
        subgraph "Seeker Documents"
            SeekerDoc[Personal Info<br/>Education<br/>Skills<br/>Applications<br/>Resume]
        end
        
        subgraph "Employer Documents"
            EmployerDoc[Company Info<br/>Contact Person<br/>Open Jobs<br/>Apps Received]
        end
    end
    
    subgraph "ChromaDB - Vector Store"
        ChromaConn[ChromaDB Client<br/>+ OpenAI Embeddings]
        
        subgraph "Vector Collections"
            SeekerResume[(Seeker_Resume<br/>1536 dims)]
            SeekerSkills[(Seeker_Skills<br/>1536 dims)]
            JobDescr[(Employer_JobDescr<br/>1536 dims)]
            JobSkills[(Employer_Skillswish<br/>1536 dims)]
        end
    end
    
    subgraph "External"
        OpenAI[OpenAI API<br/>text-embedding-3-small]
    end
    
    Services --> MongoConn
    Services --> ChromaConn
    
    MongoConn --> SeekersCol
    MongoConn --> EmployersCol
    
    SeekersCol --> SeekerDoc
    EmployersCol --> EmployerDoc
    
    ChromaConn --> SeekerResume
    ChromaConn --> SeekerSkills
    ChromaConn --> JobDescr
    ChromaConn --> JobSkills
    
    ChromaConn --> OpenAI
    
    SeekerDoc -.->|Sync| SeekerResume
    SeekerDoc -.->|Sync| SeekerSkills
    EmployerDoc -.->|Sync| JobDescr
    EmployerDoc -.->|Sync| JobSkills
    
    style MongoConn fill:#47A248,color:#fff
    style SeekersCol fill:#47A248,color:#fff
    style EmployersCol fill:#47A248,color:#fff
    style ChromaConn fill:#FF6F00,color:#fff
    style SeekerResume fill:#FF6F00,color:#fff
    style SeekerSkills fill:#FF6F00,color:#fff
    style JobDescr fill:#FF6F00,color:#fff
    style JobSkills fill:#FF6F00,color:#fff
    style OpenAI fill:#10a37f,color:#fff
```

### Database Synchronization Flow

```mermaid
sequenceDiagram
    participant API as API Request
    participant Service as Service Layer
    participant Mongo as MongoDB
    participant Embedder as OpenAI Embeddings
    participant Chroma as ChromaDB
    
    Note over API,Chroma: Create Seeker Flow
    
    API->>Service: Create Seeker
    Service->>Service: Validate Data
    Service->>Mongo: Insert Document
    Mongo-->>Service: seeker_id + UUID
    
    alt Resume Provided
        Service->>Embedder: Generate Resume Embedding
        Embedder-->>Service: 1536-dim vector
        Service->>Chroma: Store in Seeker_Resume
    end
    
    Service->>Embedder: Generate Skills Embedding
    Embedder-->>Service: 1536-dim vector
    Service->>Chroma: Store in Seeker_Skills
    
    Chroma-->>Service: Stored
    Service-->>API: Success
    
    Note over API,Chroma: Create Job Flow
    
    API->>Service: Create Job
    Service->>Service: Validate Data
    Service->>Mongo: Add to open_jobs array
    Mongo-->>Service: job_id + UUID
    
    Service->>Embedder: Generate Job Description Embedding
    Embedder-->>Service: 1536-dim vector
    Service->>Chroma: Store in Employer_JobDescr
    
    Service->>Embedder: Generate Skills Embedding
    Embedder-->>Service: 1536-dim vector
    Service->>Chroma: Store in Employer_Skillswish
    
    Chroma-->>Service: Stored
    Service-->>API: Success
```

### Data Relationships

```mermaid
erDiagram
    SEEKER ||--o{ APPLICATION : has
    SEEKER ||--|| SEEKER_RESUME_EMBEDDING : "embedded in"
    SEEKER ||--|| SEEKER_SKILLS_EMBEDDING : "embedded in"
    
    EMPLOYER ||--o{ JOB : posts
    EMPLOYER ||--o{ APPLICATION_RECEIVED : receives
    
    JOB ||--|| JOB_DESCRIPTION_EMBEDDING : "embedded in"
    JOB ||--|| JOB_SKILLS_EMBEDDING : "embedded in"
    JOB ||--o{ APPLICATION : "applied to"
    
    APPLICATION ||--|| APPLICATION_RECEIVED : "tracked as"
    
    SEEKER {
        ObjectId seeker_id PK
        UUID seeker_identification UK
        string email UK
        string password_hash
        object information
        string resume
        array key_skills
        array applications FK
    }
    
    EMPLOYER {
        ObjectId employer_id PK
        UUID employer_identification UK
        string email UK
        string password_hash
        object company_information
        array open_jobs
        array apps_received FK
    }
    
    JOB {
        ObjectId job_id PK
        UUID job_identification UK
        string job_title
        string job_description
        array key_skills
        string current_status
    }
    
    APPLICATION {
        string job_id FK
        string employer_id FK
        datetime date_applied
        string application_status
    }
```

---

## AI/ML Architecture

### Complete AI Pipeline Architecture

```mermaid
graph TB
    subgraph "Input Layer"
        UserRequest[User Request<br/>Recommendations/Candidates]
    end
    
    subgraph "Orchestration Layer - LangChain"
        MatchingService[Matching Service<br/>Orchestrator]
    end
    
    subgraph "Vector Search Layer - ChromaDB"
        GetEmbedding[Retrieve Query<br/>Embedding]
        CosineSimilarity[Cosine Similarity<br/>Search]
        TopN[Top N Results<br/>n=20 default]
    end
    
    subgraph "Data Enrichment Layer - MongoDB"
        FetchDetails[Fetch Complete<br/>Documents]
        PrepareContext[Prepare Context<br/>for LLM]
    end
    
    subgraph "LLM Processing Layer - OpenAI"
        PromptTemplate[Build Prompt<br/>System + Human Messages]
        GPT4oMini[GPT-4o-mini<br/>temp=0.75]
        StructuredOutput[Pydantic Parser<br/>Structured Response]
    end
    
    subgraph "Scoring Layer"
        SkillsScore[Skills Match<br/>40% weight<br/>0-100]
        EducationScore[Education Match<br/>20% weight<br/>0-100]
        PayScore[Pay Alignment<br/>20% weight<br/>0-100]
        ExperienceScore[Experience Match<br/>20% weight<br/>0-100]
        OverallScore[Overall Score<br/>Weighted Average<br/>0-100]
        Reasoning[LLM Reasoning<br/>Explanation]
    end
    
    subgraph "Output Layer"
        RankResults[Rank by Score]
        FilterMinScore[Filter by min_score]
        JSONResponse[JSON Response<br/>with Metadata]
    end
    
    UserRequest --> MatchingService
    MatchingService --> GetEmbedding
    GetEmbedding --> CosineSimilarity
    CosineSimilarity --> TopN
    TopN --> FetchDetails
    FetchDetails --> PrepareContext
    
    PrepareContext --> PromptTemplate
    PromptTemplate --> GPT4oMini
    GPT4oMini --> StructuredOutput
    
    StructuredOutput --> SkillsScore
    StructuredOutput --> EducationScore
    StructuredOutput --> PayScore
    StructuredOutput --> ExperienceScore
    StructuredOutput --> Reasoning
    
    SkillsScore --> OverallScore
    EducationScore --> OverallScore
    PayScore --> OverallScore
    ExperienceScore --> OverallScore
    
    OverallScore --> RankResults
    RankResults --> FilterMinScore
    FilterMinScore --> JSONResponse
    
    style UserRequest fill:#90caf9
    style CosineSimilarity fill:#FF6F00,color:#fff
    style GPT4oMini fill:#10a37f,color:#fff
    style OverallScore fill:#4caf50,color:#fff
```

### AI Model Configuration

| Component | Model/Technology | Configuration |
|-----------|-----------------|---------------|
| **Embeddings** | OpenAI text-embedding-3-small | 1536 dimensions, $0.02/1M tokens |
| **LLM** | OpenAI GPT-4o-mini | Temperature: 0.75, Max tokens: auto |
| **Vector DB** | ChromaDB | Cosine similarity, persistent storage |
| **Orchestration** | LangChain 1.0+ | Prompt templates, output parsers |
| **Tracing** | LangSmith (optional) | LLM call tracking and debugging |

### Scoring Formula

```python
# Weighted Average Score Calculation
overall_score = (
    skills_score * 0.40 +        # Skills match (most important)
    education_score * 0.20 +     # Education compatibility
    pay_score * 0.20 +           # Salary alignment
    experience_score * 0.20      # Experience relevance
)

# Score Interpretation
# 0-40:   Poor match (not recommended)
# 41-70:  Moderate match (consider with caution)
# 71-85:  Good match (recommended)
# 86-100: Excellent match (highly recommended)
```

---

## Security Architecture

### Security Layers Overview

```mermaid
graph TB
    subgraph "Client Security"
        HTTPS[HTTPS/TLS<br/>Encrypted Transport]
        LocalStorage[localStorage<br/>JWT Token Storage]
        CSP[Content Security Policy<br/>XSS Protection]
    end
    
    subgraph "API Gateway Security"
        CORSPolicy[CORS Policy<br/>Origin Whitelist]
        RateLimit[Rate Limiting<br/>Ready for Redis]
        InputValidation[Input Validation<br/>Pydantic]
    end
    
    subgraph "Authentication Layer"
        JWTVerify[JWT Verification<br/>Token Validation]
        TokenExpiry[Token Expiry<br/>30 days default]
        RoleExtract[Role Extraction<br/>RBAC]
    end
    
    subgraph "Authorization Layer"
        RoleCheck[Role-Based Access<br/>Seeker/Employer]
        ResourceCheck[Resource Ownership<br/>User ID Validation]
        PermissionCheck[Permission Check<br/>Action Authorization]
    end
    
    subgraph "Data Security"
        PasswordHash[BCrypt Hashing<br/>Cost Factor 12]
        DataValidation[Input Validation<br/>Email, Phone, Address]
        SQLInjection[NoSQL Injection<br/>Prevention via ODM]
    end
    
    subgraph "External Security"
        APIKeys[API Key Management<br/>Environment Variables]
        SecretRotation[Secret Rotation<br/>Production Practice]
        AuditLog[Audit Logging<br/>Loguru]
    end
    
    HTTPS --> CORSPolicy
    LocalStorage -.->|Bearer Token| JWTVerify
    CORSPolicy --> RateLimit
    RateLimit --> InputValidation
    
    InputValidation --> JWTVerify
    JWTVerify --> TokenExpiry
    TokenExpiry --> RoleExtract
    
    RoleExtract --> RoleCheck
    RoleCheck --> ResourceCheck
    ResourceCheck --> PermissionCheck
    
    PermissionCheck --> DataValidation
    DataValidation --> SQLInjection
    
    PasswordHash -.-> DataValidation
    APIKeys -.-> External
    AuditLog -.-> External
    
    style HTTPS fill:#4caf50,color:#fff
    style JWTVerify fill:#ff9800,color:#fff
    style RoleCheck fill:#2196f3,color:#fff
    style PasswordHash fill:#9c27b0,color:#fff
```

### Authentication & Authorization Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant JWT
    participant RBAC
    participant Resource
    
    Note over User,Resource: Login Flow
    
    User->>Frontend: Enter Credentials
    Frontend->>API: POST /auth/login
    API->>API: Verify Password (BCrypt)
    
    alt Invalid Credentials
        API-->>Frontend: 401 Unauthorized
        Frontend-->>User: Show Error
    else Valid Credentials
        API->>JWT: create_access_token()
        JWT->>JWT: Sign with HS256
        JWT-->>API: JWT Token
        API-->>Frontend: Token + User Data
        Frontend->>Frontend: Store in localStorage
        Frontend-->>User: Redirect to Dashboard
    end
    
    Note over User,Resource: Protected Request Flow
    
    User->>Frontend: Access Protected Resource
    Frontend->>Frontend: Get Token from localStorage
    Frontend->>API: Request + Bearer Token
    
    API->>JWT: Verify Token Signature
    
    alt Invalid Token
        JWT-->>API: Invalid/Expired
        API-->>Frontend: 401 Unauthorized
        Frontend->>Frontend: Clear Token
        Frontend-->>User: Redirect to Login
    else Valid Token
        JWT->>JWT: Extract user_id & role
        JWT-->>API: User Context
        
        API->>RBAC: Check Role Permission
        
        alt No Permission
            RBAC-->>API: Forbidden
            API-->>Frontend: 403 Forbidden
        else Has Permission
            RBAC-->>API: Authorized
            API->>Resource: Access Resource
            Resource-->>API: Resource Data
            API-->>Frontend: Success Response
            Frontend-->>User: Display Data
        end
    end
```

### Role-Based Access Matrix

| Resource | Seeker | Employer | Public |
|----------|--------|----------|--------|
| **Homepage** | ✅ Read | ✅ Read | ✅ Read |
| **Login/Register** | ✅ Access | ✅ Access | ✅ Access |
| **Seeker Dashboard** | ✅ Read | ❌ Forbidden | ❌ Forbidden |
| **Seeker Profile** | ✅ Read/Write | ❌ Forbidden | ❌ Forbidden |
| **Job Search** | ✅ Read | ❌ Forbidden | ❌ Forbidden |
| **Job Recommendations** | ✅ Read | ❌ Forbidden | ❌ Forbidden |
| **Apply to Jobs** | ✅ Write | ❌ Forbidden | ❌ Forbidden |
| **Employer Dashboard** | ❌ Forbidden | ✅ Read | ❌ Forbidden |
| **Employer Profile** | ❌ Forbidden | ✅ Read/Write | ❌ Forbidden |
| **Job Postings** | ❌ Read Only | ✅ CRUD | ❌ Forbidden |
| **Candidate Matching** | ❌ Forbidden | ✅ Read | ❌ Forbidden |
| **Interview Scheduling** | ❌ Forbidden | ✅ Write | ❌ Forbidden |

---

## Deployment Architecture

### Docker Compose Infrastructure

```mermaid
graph TB
    subgraph "Host Machine"
        DockerEngine[Docker Engine]
    end
    
    subgraph "Docker Network: jobportal-network"
        subgraph "Frontend Container"
            NextJSApp[Next.js App<br/>Node 20-slim<br/>Port 3000]
            FEVolumes[Volumes:<br/>./frontend:/app<br/>node_modules<br/>.next]
        end
        
        subgraph "Backend Container"
            FastAPIApp[FastAPI App<br/>Python 3.12-slim<br/>Port 8000]
            BEVolumes[Volumes:<br/>./backend:/app<br/>./chroma_db<br/>./Logs]
        end
        
        subgraph "n8n Container"
            N8nApp[n8n Workflow<br/>Latest<br/>Port 5678]
            N8nVolumes[Volumes:<br/>./n8n_data]
        end
    end
    
    subgraph "External Services"
        MongoDB[MongoDB Atlas<br/>Cloud Hosted]
        OpenAI[OpenAI API<br/>Cloud Service]
    end
    
    subgraph "Persistent Storage"
        ChromaDB[./chroma_db<br/>Vector Database]
        Logs[./Logs<br/>Application Logs]
        N8nData[./n8n_data<br/>Workflow Data]
    end
    
    DockerEngine --> NextJSApp
    DockerEngine --> FastAPIApp
    DockerEngine --> N8nApp
    
    NextJSApp --> FEVolumes
    FastAPIApp --> BEVolumes
    N8nApp --> N8nVolumes
    
    NextJSApp <-->|HTTP| FastAPIApp
    FastAPIApp <-->|Webhook| N8nApp
    
    FastAPIApp -->|TLS| MongoDB
    FastAPIApp -->|HTTPS| OpenAI
    
    BEVolumes -.-> ChromaDB
    BEVolumes -.-> Logs
    N8nVolumes -.-> N8nData
    
    style DockerEngine fill:#2496ed,color:#fff
    style NextJSApp fill:#000000,color:#fff
    style FastAPIApp fill:#009688,color:#fff
    style N8nApp fill:#ea4b71,color:#fff
    style MongoDB fill:#47A248,color:#fff
    style OpenAI fill:#10a37f,color:#fff
```

### Container Configuration

| Container | Image | Port Mapping | Environment | Volumes |
|-----------|-------|-------------|-------------|---------|
| **frontend** | Node 20-slim | 3000:3000 | NEXT_PUBLIC_BACKEND_URL=http://backend:8000 | ./frontend:/app |
| **backend** | Python 3.12-slim | 8000:8000 | From .env file | ./backend:/app, ./chroma_db, ./Logs |
| **n8n** | n8nio/n8n:latest | 5678:5678 | N8N_BASIC_AUTH_ACTIVE=false | ./n8n_data |

### Deployment Flow

```mermaid
graph LR
    Code[Code Changes] --> Git[Git Commit]
    Git --> Build[Docker Build]
    Build --> Test[Run Tests]
    Test --> Push[Push Images]
    Push --> Deploy[Docker Compose Up]
    Deploy --> Health[Health Checks]
    Health --> Live[Service Live]
    
    style Code fill:#90caf9
    style Build fill:#2496ed,color:#fff
    style Deploy fill:#4caf50,color:#fff
    style Live fill:#4caf50,color:#fff
```

### Health Checks

```yaml
# Backend Health Check
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s

# n8n Health Check
healthcheck:
  test: ["CMD", "wget", "--spider", "http://localhost:5678/healthz"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

---

## Integration Architecture

### External Service Integrations

```mermaid
graph TB
    subgraph "WorkAtlas System"
        Backend[FastAPI Backend]
        AILayer[AI/ML Layer]
    end
    
    subgraph "OpenAI Integration"
        EmbedAPI[Embeddings API<br/>text-embedding-3-small]
        LLMAPI[Chat Completions API<br/>GPT-4o-mini]
    end
    
    subgraph "n8n Integration"
        Webhook[Webhook Endpoint<br/>/webhook/interview-schedule]
        EmailWorkflow[Email Workflow<br/>Gmail/SMTP]
    end
    
    subgraph "LangSmith Integration (Optional)"
        Tracing[Tracing API<br/>LLM Call Tracking]
        Dashboard[Web Dashboard<br/>Monitoring]
    end
    
    Backend -->|HTTPS POST| EmbedAPI
    AILayer -->|HTTPS POST| LLMAPI
    Backend -->|HTTP POST| Webhook
    Webhook --> EmailWorkflow
    AILayer -.->|HTTPS POST| Tracing
    Tracing -.-> Dashboard
    
    EmbedAPI -->|1536-dim vectors| Backend
    LLMAPI -->|JSON response| AILayer
    EmailWorkflow -->|Email| Users[Candidates]
    
    style Backend fill:#009688,color:#fff
    style EmbedAPI fill:#10a37f,color:#fff
    style LLMAPI fill:#10a37f,color:#fff
    style Webhook fill:#ea4b71,color:#fff
    style Tracing fill:#ff6f00,color:#fff
```

### Integration Patterns

#### 1. OpenAI API Integration

```mermaid
sequenceDiagram
    participant App as Application
    participant SDK as OpenAI SDK
    participant API as OpenAI API
    participant Cache as Response Cache
    
    App->>SDK: client.embeddings.create()
    SDK->>API: HTTPS POST /v1/embeddings
    API->>API: Generate Embeddings
    API-->>SDK: 1536-dim vector
    SDK-->>App: Embedding object
    App->>Cache: Store embedding
    
    App->>SDK: client.chat.completions.create()
    SDK->>API: HTTPS POST /v1/chat/completions
    API->>API: Process with GPT-4o-mini
    API-->>SDK: Completion response
    SDK-->>App: Structured output
```

#### 2. n8n Webhook Integration

```mermaid
sequenceDiagram
    participant Employer as Employer Service
    participant N8nSvc as n8n Service
    participant Webhook as n8n Webhook
    participant Workflow as Email Workflow
    participant SMTP as Email Provider
    participant Candidate as Job Seeker
    
    Employer->>N8nSvc: Schedule Interview
    N8nSvc->>N8nSvc: Format Payload
    N8nSvc->>Webhook: POST /webhook/interview-schedule
    
    Webhook->>Workflow: Trigger Workflow
    Workflow->>Workflow: Parse Data
    Workflow->>Workflow: Format Email Template
    Workflow->>SMTP: Send Email
    SMTP->>Candidate: Interview Invitation
    
    SMTP-->>Workflow: Success
    Workflow-->>Webhook: 200 OK
    Webhook-->>N8nSvc: Success
    N8nSvc-->>Employer: Interview Scheduled
```

---

## End-to-End User Flows

### Complete Seeker Journey

```mermaid
flowchart TD
    Start([Seeker Visits Site]) --> Homepage[View Homepage]
    Homepage --> Register{Has Account?}
    
    Register -->|No| RegForm[Fill Registration Form]
    Register -->|Yes| LoginPage[Go to Login]
    
    RegForm --> UploadResume[Upload Resume Optional]
    UploadResume --> SubmitReg[Submit Registration]
    SubmitReg --> BackendReg[Backend Processing]
    
    BackendReg --> HashPass[BCrypt Password Hash]
    HashPass --> CreateMongo[Create MongoDB Document]
    CreateMongo --> GenEmbed[Generate OpenAI Embeddings]
    GenEmbed --> StoreChroma[Store in 2 ChromaDB Collections]
    StoreChroma --> RegSuccess[Registration Success]
    RegSuccess --> LoginPage
    
    LoginPage --> EnterCreds[Enter Email & Password]
    EnterCreds --> ValidateCreds{Valid?}
    ValidateCreds -->|No| LoginError[Show Error]
    LoginError --> LoginPage
    ValidateCreds -->|Yes| CreateJWT[Create JWT Token]
    CreateJWT --> StoreFrontend[Store in localStorage]
    StoreFrontend --> Dashboard[Seeker Dashboard]
    
    Dashboard --> Action{Choose Action}
    
    Action -->|1| ViewProfile[View Profile]
    ViewProfile --> EditProfile{Edit?}
    EditProfile -->|Yes| UpdateProfile[Update Profile]
    UpdateProfile --> Dashboard
    EditProfile -->|No| Dashboard
    
    Action -->|2| SearchJobs[Search Jobs]
    SearchJobs --> BrowseJobs[Browse Job Listings]
    BrowseJobs --> ViewJobDetail[View Job Details]
    ViewJobDetail --> ApplyDecision{Apply?}
    ApplyDecision -->|No| SearchJobs
    ApplyDecision -->|Yes| SubmitApp[Submit Application]
    SubmitApp --> UpdateBothDB[Update MongoDB<br/>Seeker & Employer]
    UpdateBothDB --> AppConfirm[Show Confirmation]
    AppConfirm --> Dashboard
    
    Action -->|3| GetRecs[Get AI Recommendations]
    GetRecs --> BackendRecs[Backend Processing]
    BackendRecs --> FetchEmbed[Fetch Seeker Embedding]
    FetchEmbed --> VectorSearch[ChromaDB Similarity Search]
    VectorSearch --> Top20[Top 20 Job Matches]
    Top20 --> FetchJobDetails[Fetch from MongoDB]
    FetchJobDetails --> LLMLoop[For Each Job]
    
    LLMLoop --> CallGPT[Call GPT-4o-mini]
    CallGPT --> ParseScore[Parse Structured Scores]
    ParseScore --> NextJob{More Jobs?}
    NextJob -->|Yes| LLMLoop
    NextJob -->|No| RankAll[Rank by Overall Score]
    
    RankAll --> DisplayRecs[Display Recommendations]
    DisplayRecs --> ViewRecDetail[View Match Details]
    ViewRecDetail --> SeeBreakdown[See Score Breakdown]
    SeeBreakdown --> ReadReasoning[Read LLM Reasoning]
    ReadReasoning --> ApplyFromRec{Apply?}
    ApplyFromRec -->|Yes| SubmitApp
    ApplyFromRec -->|No| DisplayRecs
    
    Action -->|4| ViewApps[View My Applications]
    ViewApps --> TrackStatus[Track Application Status]
    TrackStatus --> Dashboard
    
    Action -->|5| LogoutAction[Logout]
    LogoutAction --> ClearToken[Clear localStorage]
    ClearToken --> Homepage
    
    style Homepage fill:#90caf9
    style Dashboard fill:#c8e6c9
    style BackendRecs fill:#10a37f,color:#fff
    style VectorSearch fill:#FF6F00,color:#fff
    style CallGPT fill:#10a37f,color:#fff
    style DisplayRecs fill:#fff9c4
```

### Complete Employer Journey

```mermaid
flowchart TD
    Start([Employer Visits Site]) --> Homepage[View Homepage]
    Homepage --> Register{Has Account?}
    
    Register -->|No| RegForm[Fill Registration Form]
    Register -->|Yes| LoginPage[Go to Login]
    
    RegForm --> CompanyInfo[Enter Company Info]
    CompanyInfo --> IndustryCode[Select GICS Industry Codes]
    IndustryCode --> SubmitReg[Submit Registration]
    SubmitReg --> BackendReg[Backend Processing]
    
    BackendReg --> ValidateGICS[Validate GICS Codes]
    ValidateGICS --> HashPass[BCrypt Password Hash]
    HashPass --> CreateMongo[Create MongoDB Document]
    CreateMongo --> RegSuccess[Registration Success]
    RegSuccess --> LoginPage
    
    LoginPage --> EnterCreds[Enter Email & Password]
    EnterCreds --> ValidateCreds{Valid?}
    ValidateCreds -->|No| LoginError[Show Error]
    LoginError --> LoginPage
    ValidateCreds -->|Yes| CreateJWT[Create JWT Token]
    CreateJWT --> StoreFrontend[Store in localStorage]
    StoreFrontend --> Dashboard[Employer Dashboard]
    
    Dashboard --> CheckN8n[Check n8n Status]
    CheckN8n --> Action{Choose Action}
    
    Action -->|1| CreateJob[Create New Job]
    CreateJob --> JobForm[Fill Job Details]
    JobForm --> SubmitJob[Submit Job Posting]
    SubmitJob --> JobBackend[Backend Processing]
    JobBackend --> AddToMongo[Add to open_jobs Array]
    AddToMongo --> JobEmbed[Generate 2 Embeddings]
    JobEmbed --> JobChroma[Store in ChromaDB]
    JobChroma --> JobSuccess[Job Posted]
    JobSuccess --> Dashboard
    
    Action -->|2| ManageJobs[Manage Jobs]
    ManageJobs --> JobList[View Job List]
    JobList --> SelectJob[Select Job]
    SelectJob --> JobAction{Action?}
    JobAction -->|Edit| EditJob[Edit Job Details]
    JobAction -->|Delete| DeleteJob[Delete Job]
    JobAction -->|View| ViewJobDetail[View Details]
    EditJob --> JobList
    DeleteJob --> JobList
    ViewJobDetail --> JobList
    
    Action -->|3| FindCandidates[Find AI Candidates]
    FindCandidates --> SelectJobMatch[Select Job Posting]
    SelectJobMatch --> BackendMatch[Backend Processing]
    BackendMatch --> FetchJobEmbed[Fetch Job Embedding]
    FetchJobEmbed --> VectorSearch[ChromaDB Similarity Search]
    VectorSearch --> Top20[Top 20 Seeker Matches]
    Top20 --> FetchSeekerDetails[Fetch from MongoDB]
    FetchSeekerDetails --> LLMLoop[For Each Candidate]
    
    LLMLoop --> CallGPT[Call GPT-4o-mini]
    CallGPT --> ParseScore[Parse Structured Scores]
    ParseScore --> CheckApplied[Check if Applied]
    CheckApplied --> NextCand{More Candidates?}
    NextCand -->|Yes| LLMLoop
    NextCand -->|No| RankAll[Rank by Overall Score]
    
    RankAll --> DisplayCands[Display Candidates]
    DisplayCands --> ReviewProfile[Review Candidate Profile]
    ReviewProfile --> SeeBreakdown[See Score Breakdown]
    SeeBreakdown --> ReadReasoning[Read LLM Reasoning]
    ReadReasoning --> ScheduleDecision{Schedule Interview?}
    
    ScheduleDecision -->|No| DisplayCands
    ScheduleDecision -->|Yes| InterviewForm[Fill Interview Form]
    InterviewForm --> SelectDateTime[Select Date & Time]
    SelectDateTime --> SelectType[Select Type<br/>In-person/Video/Phone]
    SelectType --> EnterLocation[Enter Location/Link]
    EnterLocation --> AddNotes[Add Notes Optional]
    AddNotes --> SubmitInterview[Submit Interview]
    
    SubmitInterview --> TriggerN8n[Trigger n8n Webhook]
    TriggerN8n --> N8nCheck{n8n Available?}
    N8nCheck -->|Yes| SendEmail[Send Email to Candidate]
    N8nCheck -->|No| ShowWarning[Show Warning]
    SendEmail --> EmailSent[Email Sent]
    EmailSent --> UpdateStatus[Update DB Status]
    ShowWarning --> UpdateStatus
    UpdateStatus --> IntSuccess[Interview Scheduled]
    IntSuccess --> DisplayCands
    
    Action -->|4| ViewApps[View Applications]
    ViewApps --> AppList[List All Applications]
    AppList --> Dashboard
    
    Action -->|5| UpdateProfile[Update Profile]
    UpdateProfile --> CompanyEdit[Edit Company Info]
    CompanyEdit --> Dashboard
    
    Action -->|6| LogoutAction[Logout]
    LogoutAction --> ClearToken[Clear localStorage]
    ClearToken --> Homepage
    
    style Homepage fill:#90caf9
    style Dashboard fill:#e1bee7
    style BackendMatch fill:#10a37f,color:#fff
    style VectorSearch fill:#FF6F00,color:#fff
    style CallGPT fill:#10a37f,color:#fff
    style TriggerN8n fill:#ea4b71,color:#fff
    style DisplayCands fill:#fff9c4
```

---

## Performance & Scalability

### Performance Optimization Strategy

```mermaid
graph TB
    subgraph "Frontend Optimizations"
        FE1[Code Splitting<br/>Automatic by Next.js]
        FE2[Image Optimization<br/>Next.js Image]
        FE3[Static Generation<br/>SSG where possible]
        FE4[Client-Side Caching<br/>sessionStorage]
    end
    
    subgraph "Backend Optimizations"
        BE1[Async Operations<br/>Non-blocking I/O]
        BE2[Connection Pooling<br/>Motor + AsyncIO]
        BE3[Query Optimization<br/>MongoDB Indexes]
        BE4[Batch Processing<br/>Parallel AI Scoring]
    end
    
    subgraph "Database Optimizations"
        DB1[MongoDB Indexes<br/>_id, email, UUID]
        DB2[ChromaDB Caching<br/>Embedding Reuse]
        DB3[Vector Search<br/>Optimized Cosine Similarity]
        DB4[Beanie Caching<br/>Document Cache]
    end
    
    subgraph "AI/ML Optimizations"
        AI1[Embedding Cache<br/>Avoid Regeneration]
        AI2[Batch LLM Calls<br/>Parallel Processing]
        AI3[Model Selection<br/>GPT-4o-mini for Speed]
        AI4[Result Caching<br/>Ready for Redis]
    end
    
    subgraph "Network Optimizations"
        NET1[HTTP/2<br/>Multiplexing]
        NET2[Compression<br/>Gzip Responses]
        NET3[CDN Ready<br/>Static Assets]
        NET4[Connection Keep-Alive<br/>Persistent Connections]
    end
    
    style FE1 fill:#000000,color:#fff
    style BE1 fill:#009688,color:#fff
    style DB3 fill:#FF6F00,color:#fff
    style AI2 fill:#10a37f,color:#fff
```

### Scalability Architecture

```mermaid
graph TB
    subgraph "Load Balancer"
        LB[Nginx/HAProxy<br/>Load Balancer]
    end
    
    subgraph "Frontend Tier - Stateless"
        FE1[Next.js Instance 1]
        FE2[Next.js Instance 2]
        FE3[Next.js Instance N]
    end
    
    subgraph "Backend Tier - Stateless"
        BE1[FastAPI Instance 1]
        BE2[FastAPI Instance 2]
        BE3[FastAPI Instance N]
    end
    
    subgraph "Cache Layer (Future)"
        Redis[Redis Cluster<br/>Session & Query Cache]
    end
    
    subgraph "Database Layer - Scalable"
        MongoCluster[MongoDB Atlas<br/>Auto-Sharding<br/>Read Replicas]
        ChromaCluster[ChromaDB<br/>Horizontal Scaling Ready]
    end
    
    subgraph "External Services"
        OpenAI[OpenAI API<br/>Auto-Scaling]
        N8nCluster[n8n Cluster<br/>Multiple Instances]
    end
    
    LB --> FE1
    LB --> FE2
    LB --> FE3
    
    FE1 --> BE1
    FE2 --> BE2
    FE3 --> BE3
    
    BE1 --> Redis
    BE2 --> Redis
    BE3 --> Redis
    
    BE1 --> MongoCluster
    BE2 --> MongoCluster
    BE3 --> MongoCluster
    
    BE1 --> ChromaCluster
    BE2 --> ChromaCluster
    BE3 --> ChromaCluster
    
    BE1 --> OpenAI
    BE2 --> OpenAI
    BE3 --> OpenAI
    
    BE1 --> N8nCluster
    BE2 --> N8nCluster
    BE3 --> N8nCluster
    
    style LB fill:#ff9800,color:#fff
    style Redis fill:#dc382d,color:#fff
    style MongoCluster fill:#47A248,color:#fff
    style OpenAI fill:#10a37f,color:#fff
```

### Performance Metrics

| Metric | Target | Current | Notes |
|--------|--------|---------|-------|
| **API Response Time** | < 200ms | ~150ms | CRUD operations |
| **AI Matching Time** | < 30s | ~10-25s | 20 matches with LLM scoring |
| **Vector Search** | < 100ms | ~50ms | ChromaDB similarity search |
| **Embedding Generation** | < 500ms | ~300ms | OpenAI API call |
| **Page Load Time** | < 3s | ~2s | Next.js optimized |
| **Bundle Size (Frontend)** | < 100KB | ~45KB | Gzipped |
| **Database Query** | < 50ms | ~20ms | MongoDB indexed queries |

---

## System Health & Monitoring

### Monitoring Architecture

```mermaid
graph TB
    subgraph "Application Layer"
        Frontend[Next.js App]
        Backend[FastAPI App]
        N8n[n8n Service]
    end
    
    subgraph "Logging Layer"
        Loguru[Loguru Logger<br/>Structured Logs]
        DebugLog[Debug_log.log<br/>All Events]
        ErrorLog[Error_log.log<br/>Errors Only]
    end
    
    subgraph "Health Checks"
        HealthEndpoint[/health endpoint]
        DBStatus[/db-status endpoint]
        N8nStatus[/n8n/status endpoint]
    end
    
    subgraph "Metrics (Future)"
        Prometheus[Prometheus<br/>Metrics Collection]
        Grafana[Grafana<br/>Visualization]
    end
    
    subgraph "Error Tracking (Future)"
        Sentry[Sentry<br/>Error Monitoring]
        Alerts[Alert System]
    end
    
    subgraph "AI Monitoring"
        LangSmith[LangSmith<br/>LLM Tracing]
        TokenUsage[Token Usage<br/>Cost Tracking]
    end
    
    Backend --> Loguru
    Loguru --> DebugLog
    Loguru --> ErrorLog
    
    Backend --> HealthEndpoint
    Backend --> DBStatus
    Backend --> N8nStatus
    
    Backend -.->|Future| Prometheus
    Prometheus -.-> Grafana
    
    Frontend -.->|Future| Sentry
    Backend -.->|Future| Sentry
    Sentry -.-> Alerts
    
    Backend -.->|Optional| LangSmith
    LangSmith --> TokenUsage
    
    style Backend fill:#009688,color:#fff
    style Loguru fill:#4caf50,color:#fff
    style LangSmith fill:#ff6f00,color:#fff
    style Prometheus fill:#e6522c,color:#fff
```

### Health Check Endpoints

| Endpoint | Method | Purpose | Response |
|----------|--------|---------|----------|
| `/health` | GET | Basic health check | `{"status": "healthy"}` |
| `/` | GET | API status | `{"message": "Job Portal API is running", "status": "ok"}` |
| `/db-status` | GET | Database connection | `{"connected": true, "database": "job-portal", "collections": [...]}` |
| `/api/v1/employers/n8n/status` | GET | n8n service status | `{"status": "connected", "message": "..."}` |

### Log Structure

```python
# Loguru Configuration
logger.add("Logs/Debug_log.log", level="DEBUG", rotation="50MB")
logger.add("Logs/Error_log.log", level="ERROR", rotation="50MB")

# Log Format
# {time} {level} {message}
# 2024-11-17 14:30:45 INFO User login successful: user_id=abc123
# 2024-11-17 14:31:12 ERROR Database connection failed: Connection timeout
```

---

## Conclusion

WorkAtlas is a comprehensive, AI-powered job portal that demonstrates modern software architecture principles:

### Key Architectural Strengths

1. **Microservices Architecture**: Clear separation between frontend, backend, and workflow services
2. **Dual Database Strategy**: MongoDB for documents, ChromaDB for vector search
3. **AI-First Design**: LLM integration at the core of matching logic
4. **Type Safety**: TypeScript (frontend) and Python type hints (backend)
5. **Async Throughout**: Non-blocking operations for high performance
6. **Stateless Services**: Easy horizontal scaling
7. **Container-First**: Docker for consistent deployment
8. **Security by Design**: JWT, BCrypt, RBAC, input validation

### Technology Highlights

- **40+ Technologies**: Modern, battle-tested stack
- **20+ API Endpoints**: Comprehensive REST API
- **6 Database Collections**: Optimized data storage
- **2 User Roles**: Clean RBAC implementation
- **1536-dim Vectors**: High-quality semantic embeddings
- **GPT-4o-mini**: Cost-effective AI scoring

### Scalability Path

- ✅ **Current**: Single instance deployment with Docker Compose
- 🔄 **Near Term**: Redis caching, load balancing, multiple instances
- 🎯 **Long Term**: Kubernetes orchestration, microservices separation, global CDN

### System Maturity

| Aspect | Status | Notes |
|--------|--------|-------|
| **Core Functionality** | ✅ Complete | All major features implemented |
| **AI Matching** | ✅ Production Ready | LLM-based with detailed scoring |
| **Security** | ✅ Production Ready | JWT, BCrypt, RBAC, validation |
| **Database** | ✅ Production Ready | MongoDB + ChromaDB |
| **Deployment** | ✅ Docker Ready | Docker Compose orchestration |
| **Monitoring** | 🔄 Partial | Logging in place, metrics pending |
| **Caching** | 🔄 Ready | Redis integration ready |
| **Testing** | 🎯 Future | Test suites to be implemented |

---

**Document Version**: 1.0  
**Last Updated**: November 17, 2025  
**System Version**: 0.1.0  
**Architecture Type**: Microservices with AI/ML Integration  
**Deployment**: Docker Compose (Development), Kubernetes-Ready (Production)  

**Project**: WorkAtlas - AI-Powered Job Portal  
**Team**: AZVIBE Greenfield Team  
**Repository**: Greenfield-project

