# WorkAtlas Backend - Systems Architecture Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Technology Stack](#technology-stack)
4. [Component Structure](#component-structure)
5. [Data Layer Architecture](#data-layer-architecture)
6. [API Architecture](#api-architecture)
7. [AI/ML Architecture](#aiml-architecture)
8. [Security Architecture](#security-architecture)
9. [Integration Architecture](#integration-architecture)
10. [User Flow Diagrams](#user-flow-diagrams)

---

## System Overview

**WorkAtlas Backend** is a high-performance Python backend built with FastAPI, providing REST APIs for an AI-powered job portal. It integrates MongoDB for document storage, ChromaDB for vector embeddings, and LangChain with OpenAI for intelligent job-seeker matching.

### Key Features
- **FastAPI Framework**: High-performance async API with automatic OpenAPI documentation
- **Dual Database System**: MongoDB for transactional data, ChromaDB for vector search
- **AI-Powered Matching**: LangChain + OpenAI for intelligent candidate-job matching
- **JWT Authentication**: Secure token-based authentication with role-based access
- **Beanie ODM**: MongoDB object-document mapping with Pydantic validation
- **n8n Integration**: Workflow automation for email notifications
- **Vector Embeddings**: OpenAI text-embedding-3-small for semantic search

---

## High-Level Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        Browser[Web Browser]
        Mobile[Mobile App Future]
    end
    
    subgraph "API Gateway"
        FastAPI[FastAPI Server<br/>Port 8000]
        CORS[CORS Middleware]
        Auth[JWT Auth Middleware]
    end
    
    subgraph "Business Logic Layer"
        SeekerService[Seeker Service]
        EmployerService[Employer Service]
        AIService[AI Matching Service]
        N8nService[n8n Integration Service]
    end
    
    subgraph "AI/ML Layer"
        LangChain[LangChain Orchestrator]
        OpenAI[OpenAI GPT-4o-mini]
        Embeddings[OpenAI Embeddings<br/>text-embedding-3-small]
        ScoringChain[Scoring Chain]
        VectorStore[Vector Store Interface]
    end
    
    subgraph "Data Access Layer"
        SeekerCRUD[Seeker CRUD]
        EmployerCRUD[Employer CRUD]
        ChromaCRUD[Chroma CRUD]
        Beanie[Beanie ODM]
    end
    
    subgraph "Database Layer"
        MongoDB[(MongoDB Atlas<br/>Document Store)]
        ChromaDB[(ChromaDB<br/>Vector Database)]
    end
    
    subgraph "External Services"
        n8n[n8n Workflow<br/>Email Automation]
        LangSmith[LangSmith<br/>Tracing Optional]
    end
    
    Browser --> FastAPI
    Mobile -.-> FastAPI
    
    FastAPI --> CORS
    CORS --> Auth
    Auth --> SeekerService
    Auth --> EmployerService
    Auth --> AIService
    
    SeekerService --> SeekerCRUD
    EmployerService --> EmployerCRUD
    AIService --> ScoringChain
    AIService --> VectorStore
    
    ScoringChain --> LangChain
    LangChain --> OpenAI
    VectorStore --> ChromaCRUD
    ChromaCRUD --> Embeddings
    
    SeekerCRUD --> Beanie
    EmployerCRUD --> Beanie
    Beanie --> MongoDB
    ChromaCRUD --> ChromaDB
    
    EmployerService --> N8nService
    N8nService --> n8n
    
    LangChain -.->|Optional| LangSmith
    
    style FastAPI fill:#009688,color:#ffffff
    style MongoDB fill:#47A248,color:#ffffff
    style ChromaDB fill:#FF6F00,color:#ffffff
    style OpenAI fill:#10a37f,color:#ffffff
    style n8n fill:#ea4b71,color:#ffffff
```

### Architecture Layers

1. **API Gateway Layer** (FastAPI)
   - Request routing and validation
   - CORS handling
   - JWT authentication
   - OpenAPI documentation

2. **Business Logic Layer** (Services)
   - Seeker operations (registration, profile, applications)
   - Employer operations (jobs, candidates, interviews)
   - AI matching orchestration
   - External service integration

3. **AI/ML Layer** (LangChain + OpenAI)
   - Vector embeddings generation
   - Semantic similarity search
   - LLM-based scoring and reasoning
   - Prompt engineering and chains

4. **Data Access Layer** (CRUD + ODM)
   - MongoDB operations via Beanie ODM
   - ChromaDB vector operations
   - Data validation and transformation

5. **Database Layer**
   - MongoDB: Users, jobs, applications
   - ChromaDB: Embeddings for resumes and job descriptions

---

## Technology Stack

### Complete Backend Tech Stack Overview

```mermaid
graph TB
    subgraph "Core Framework & Runtime"
        Python[Python 3.12<br/>Programming Language]
        FastAPI[FastAPI 0.104+<br/>Web Framework]
        Uvicorn[Uvicorn 0.24+<br/>ASGI Server]
        Pydantic[Pydantic 2.12+<br/>Data Validation]
    end
    
    subgraph "Database & ODM"
        MongoDB[MongoDB Atlas<br/>Document Database]
        Motor[Motor 3.7+<br/>Async MongoDB Driver]
        Beanie[Beanie 2.0+<br/>ODM Framework]
        ChromaDB[ChromaDB 1.3+<br/>Vector Database]
    end
    
    subgraph "AI & Machine Learning"
        LangChain[LangChain 1.0+<br/>LLM Framework]
        LangChainCore[LangChain Core<br/>Base Components]
        LangChainOpenAI[LangChain OpenAI<br/>OpenAI Integration]
        OpenAISDK[OpenAI 2.8+<br/>Python SDK]
    end
    
    subgraph "Security & Authentication"
        BCrypt[BCrypt 4.1<br/>Password Hashing]
        PyJOSE[Python JOSE 3.5+<br/>JWT Handling]
        EmailValidator[Email Validator 2.3+<br/>Email Validation]
        PhoneNumbers[PhoneNumbers 9.0+<br/>Phone Validation]
    end
    
    subgraph "File Processing"
        PyPDF2[PyPDF2 3.0+<br/>PDF Processing]
        PythonDocx[Python-Docx 1.2+<br/>DOCX Processing]
        Aiofiles[Aiofiles 24.1+<br/>Async File I/O]
    end
    
    subgraph "HTTP & Integration"
        HTTPX[HTTPX 0.28+<br/>Async HTTP Client]
        Requests[Requests 2.32+<br/>HTTP Client]
    end
    
    subgraph "Utilities & Tools"
        Loguru[Loguru 0.7+<br/>Logging]
        PythonDotenv[Python-Dotenv 1.2+<br/>Environment Config]
        GICS[GICS 0.2+<br/>Industry Codes]
        TZData[TZData 2024+<br/>Timezone Support]
    end
    
    subgraph "Development & Deployment"
        UV[uv<br/>Package Manager]
        Docker[Docker<br/>Containerization]
        DockerCompose[Docker Compose<br/>Orchestration]
    end
    
    Python --> FastAPI
    FastAPI --> Uvicorn
    FastAPI --> Pydantic
    
    Beanie --> Motor
    Motor --> MongoDB
    Beanie --> Pydantic
    
    LangChain --> LangChainCore
    LangChain --> LangChainOpenAI
    LangChainOpenAI --> OpenAISDK
    ChromaDB --> OpenAISDK
    
    FastAPI --> BCrypt
    FastAPI --> PyJOSE
    Pydantic --> EmailValidator
    Pydantic --> PhoneNumbers
    
    FastAPI --> HTTPX
    
    Python --> UV
    UV --> Docker
    Docker --> DockerCompose
    
    style Python fill:#3776ab,color:#ffffff
    style FastAPI fill:#009688,color:#ffffff
    style MongoDB fill:#47A248,color:#ffffff
    style ChromaDB fill:#FF6F00,color:#ffffff
    style LangChain fill:#1c3c3c,color:#ffffff
    style OpenAISDK fill:#10a37f,color:#ffffff
```

---

### Detailed Technology Breakdown

#### 1. Core Framework & Runtime

| Technology | Version | Purpose | Category |
|------------|---------|---------|----------|
| **Python** | 3.12+ | Core programming language with modern features (match/case, type hints) | Language |
| **FastAPI** | 0.104+ | High-performance async web framework with automatic OpenAPI docs | Web Framework |
| **Uvicorn** | 0.24+ | Lightning-fast ASGI server with standard support | ASGI Server |
| **Pydantic** | 2.12+ | Data validation and settings management using Python type annotations | Validation |

**FastAPI Features Used:**
- ✅ Async/await for non-blocking I/O
- ✅ Automatic OpenAPI (Swagger) documentation
- ✅ Request/response validation via Pydantic
- ✅ Dependency injection system
- ✅ Background tasks
- ✅ Middleware support
- ✅ WebSocket support (ready for future use)
- ✅ CORS middleware

**Python 3.12 Features:**
- ✅ Type hints and type checking
- ✅ Async/await syntax
- ✅ Context managers
- ✅ Pattern matching (match/case)
- ✅ Dataclasses
- ✅ f-strings for formatting

---

#### 2. Database & ODM

| Technology | Version | Purpose | Category |
|------------|---------|---------|----------|
| **MongoDB** | Atlas (Cloud) | NoSQL document database for users, jobs, applications | Database |
| **Motor** | 3.7+ | Async MongoDB driver for Python (used by Beanie) | Database Driver |
| **Beanie** | 2.0+ | Async ODM (Object-Document Mapper) built on Motor and Pydantic | ODM Framework |
| **ChromaDB** | 1.3+ | Open-source vector database for embeddings and similarity search | Vector Database |

**MongoDB Configuration:**
```python
# Connection String Format
mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?appName=job-portal

# Collections
- seekers: Job seeker profiles and applications
- employers: Company profiles and job postings
```

**Beanie Features:**
- ✅ Pydantic-based document models
- ✅ Async operations (find, insert, update, delete)
- ✅ Aggregation pipelines
- ✅ Index management
- ✅ Relationship management
- ✅ Migration support

**ChromaDB Collections:**
- `Seeker_Resume`: Resume embeddings for semantic search
- `Seeker_Skills`: Skill embeddings for skill matching
- `Employer_JobDescr`: Job description embeddings
- `Employer_Skillswish`: Required skills embeddings

**Embedding Model:**
- OpenAI `text-embedding-3-small` (1536 dimensions)

---

#### 3. AI & Machine Learning Stack

| Technology | Version | Purpose | Category |
|------------|---------|---------|----------|
| **LangChain** | 1.0+ | Framework for building LLM applications with chains and agents | LLM Framework |
| **LangChain Core** | 1.0+ | Core components for LangChain (prompts, parsers, runnables) | Core Library |
| **LangChain OpenAI** | 0.2+ | OpenAI integration for LangChain | Integration |
| **OpenAI SDK** | 2.8+ | Official OpenAI Python SDK for GPT models and embeddings | AI SDK |

**LangChain Components Used:**
- ✅ ChatPromptTemplate: Structured prompts for LLM
- ✅ PydanticOutputParser: Structured output parsing
- ✅ ChatOpenAI: OpenAI model integration
- ✅ Chains: Sequential LLM operations

**OpenAI Models:**
- **GPT-4o-mini**: Main model for scoring and reasoning (configurable)
- **text-embedding-3-small**: Embedding generation (1536 dims, cost-effective)

**AI Configuration:**
```python
# Model Settings
OPENAI_MODEL = "gpt-4o-mini"  # Configurable
DEFAULT_TEMPERATURE = 0.75
EMBEDDING_MODEL = "text-embedding-3-small"

# Optional: LangSmith Tracing
LANGSMITH_TRACING = "true"
LANGSMITH_PROJECT = "job_portal"
```

**LangSmith Integration (Optional):**
- Trace LLM calls for debugging
- Monitor token usage
- Track performance metrics

---

#### 4. Security & Authentication

| Technology | Version | Purpose | Category |
|------------|---------|---------|----------|
| **BCrypt** | 4.1.3 | Password hashing with salt (industry standard) | Cryptography |
| **Python-JOSE** | 3.5+ | JWT (JSON Web Token) encoding/decoding with cryptography | Authentication |
| **Email-Validator** | 2.3+ | Email address validation (RFC 5322 compliant) | Validation |
| **PhoneNumbers** | 9.0+ | Phone number validation (Google's libphonenumber) | Validation |

**Security Features:**
- ✅ BCrypt password hashing (cost factor: 12)
- ✅ JWT tokens with HS256 algorithm
- ✅ Token expiration (30 days default)
- ✅ Role-based access control (seeker/employer)
- ✅ Email and phone number validation
- ✅ US address validation (states, ZIP codes)

**JWT Structure:**
```python
{
    "sub": "user_id",           # User ID (MongoDB ObjectId)
    "role": "seeker|employer",  # User role
    "exp": 1234567890           # Expiration timestamp
}
```

**Password Security:**
- Minimum length: 6 characters (configurable)
- BCrypt hashing with automatic salt
- 72-byte password limit (BCrypt standard)

---

#### 5. File Processing

| Technology | Version | Purpose | Category |
|------------|---------|---------|----------|
| **PyPDF2** | 3.0+ | PDF text extraction for resume parsing | File Processing |
| **Python-Docx** | 1.2+ | DOCX text extraction for resume parsing | File Processing |
| **Aiofiles** | 24.1+ | Async file I/O operations | Async I/O |

**Resume Processing:**
- Supported formats: PDF, DOCX, TXT
- Text extraction from documents
- Resume storage in MongoDB
- Embedding generation for ChromaDB

**File Size Limits:**
- Resume upload: 10MB max (configurable)
- Async file handling for non-blocking uploads

---

#### 6. HTTP & Integration

| Technology | Version | Purpose | Category |
|------------|---------|---------|----------|
| **HTTPX** | 0.28+ | Modern async HTTP client for external API calls | HTTP Client |
| **Requests** | 2.32+ | Synchronous HTTP client (fallback/simple operations) | HTTP Client |

**HTTPX Features:**
- ✅ Async/await support
- ✅ HTTP/2 support
- ✅ Timeout configuration
- ✅ Connection pooling
- ✅ Request/response hooks

**n8n Integration:**
- Webhook-based workflow triggering
- Interview scheduling emails
- Async HTTP calls via HTTPX

---

#### 7. Utilities & Validation

| Technology | Version | Purpose | Category |
|------------|---------|---------|----------|
| **Loguru** | 0.7+ | Modern logging with colors, rotation, and structured output | Logging |
| **Python-Dotenv** | 1.2+ | Environment variable management from .env files | Configuration |
| **GICS** | 0.2+ | Global Industry Classification Standard codes | Industry Data |
| **Pydantic Extra Types** | 2.10+ | Additional Pydantic types (phone numbers, etc.) | Validation |
| **TZData** | 2024+ | Timezone database (IANA time zones) | Time/Date |
| **Annotated Types** | 0.7+ | PEP 593 annotated types for validation | Type Hints |

**Loguru Configuration:**
```python
# Dual log files with rotation
logger.add("Logs/Debug_log.log", level="DEBUG", rotation="50MB")
logger.add("Logs/Error_log.log", level="ERROR", rotation="50MB")
```

**Custom Validators:**
- US State abbreviations (50 states + DC + 5 territories)
- ZIP codes (5-digit and ZIP+4 formats)
- US phone numbers (multiple formats)
- Email addresses (RFC 5322)
- GICS industry codes (2, 4, 6, 8 digit formats)

---

#### 8. Development & Deployment

| Technology | Version | Purpose | Category |
|------------|---------|---------|----------|
| **uv** | Latest | Ultra-fast Python package installer and resolver (Rust-based) | Package Manager |
| **Docker** | Latest | Container platform for consistent deployment | Containerization |
| **Docker Compose** | Latest | Multi-container orchestration | Orchestration |

**uv Features:**
- 10-100x faster than pip
- Automatic dependency resolution
- Lock file generation
- PEP 723 inline script metadata support

**Docker Configuration:**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# Install dependencies
RUN uv sync
# Run application
CMD ["uv", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**Docker Compose Services:**
- `backend`: FastAPI application (port 8000)
- `frontend`: Next.js application (port 3000)
- `n8n`: Workflow automation (port 5678)

---

### Technology Stack Summary Table

| Category | Technologies | Count |
|----------|-------------|-------|
| **Core Framework** | Python, FastAPI, Uvicorn, Pydantic | 4 |
| **Database** | MongoDB, Motor, Beanie, ChromaDB | 4 |
| **AI/ML** | LangChain, LangChain Core, LangChain OpenAI, OpenAI SDK | 4 |
| **Security** | BCrypt, Python-JOSE, Email-Validator, PhoneNumbers | 4 |
| **File Processing** | PyPDF2, Python-Docx, Aiofiles | 3 |
| **HTTP** | HTTPX, Requests | 2 |
| **Utilities** | Loguru, Python-Dotenv, GICS, Pydantic Extra, TZData, Annotated Types | 6 |
| **Dev Tools** | uv, Docker, Docker Compose | 3 |
| **Total Dependencies** | | **30+** |

---

### Dependency Tree Visualization

```mermaid
graph LR
    subgraph "Production Dependencies"
        P1[fastapi 0.104+]
        P2[uvicorn 0.24+]
        P3[beanie 2.0+]
        P4[motor 3.7+]
        P5[chromadb 1.3+]
        P6[langchain 1.0+]
        P7[langchain-core 1.0+]
        P8[langchain-openai 0.2+]
        P9[openai 2.8+]
        P10[pydantic 2.12+]
        P11[bcrypt 4.1.3]
        P12[python-jose 3.5+]
        P13[loguru 0.7+]
        P14[httpx 0.28+]
    end
    
    P1 --> P2
    P1 --> P10
    P3 --> P4
    P3 --> P10
    P6 --> P7
    P6 --> P8
    P8 --> P9
    P5 --> P9
    
    style P1 fill:#009688,color:#fff
    style P3 fill:#47A248,color:#fff
    style P5 fill:#FF6F00,color:#fff
    style P6 fill:#1c3c3c,color:#fff
    style P9 fill:#10a37f,color:#fff
    style P10 fill:#e92063,color:#fff
```

---

### Tech Stack Decision Rationale

#### Why FastAPI?
- ✅ **Performance**: Among the fastest Python frameworks (on par with Node.js)
- ✅ **Modern**: Built on async/await, type hints, and Pydantic
- ✅ **Auto Documentation**: OpenAPI/Swagger docs generated automatically
- ✅ **Type Safety**: Request/response validation via Pydantic
- ✅ **Developer Experience**: Excellent IDE support and debugging

#### Why Beanie ODM?
- ✅ **Async Native**: Built for async/await from the ground up
- ✅ **Pydantic Integration**: Seamless validation and serialization
- ✅ **Type Safety**: Full type hints for MongoDB operations
- ✅ **Modern**: More Pythonic than PyMongo or MongoEngine
- ✅ **Performance**: Direct Motor integration for speed

#### Why ChromaDB?
- ✅ **Open Source**: No vendor lock-in
- ✅ **Easy Setup**: Persistent local storage, no server needed
- ✅ **Python Native**: First-class Python support
- ✅ **Embedding Functions**: Built-in OpenAI integration
- ✅ **Cost Effective**: Self-hosted vector database

#### Why LangChain?
- ✅ **Abstraction**: High-level interface for LLM operations
- ✅ **Prompt Management**: Structured prompt templates
- ✅ **Output Parsing**: Automatic structured output extraction
- ✅ **Tracing**: LangSmith integration for debugging
- ✅ **Ecosystem**: Large community and integrations

#### Why OpenAI?
- ✅ **Quality**: State-of-the-art language models
- ✅ **Cost Effective**: GPT-4o-mini is affordable
- ✅ **Embeddings**: High-quality semantic embeddings
- ✅ **Reliability**: Stable API with good uptime
- ✅ **Integration**: Excellent LangChain support

#### Why uv Package Manager?
- ✅ **Speed**: 10-100x faster than pip
- ✅ **Rust-Based**: Modern, reliable implementation
- ✅ **Lock Files**: Deterministic dependency resolution
- ✅ **PEP 723**: Support for inline script metadata
- ✅ **Drop-in Replacement**: Compatible with pip/poetry workflows

---

## Component Structure

```mermaid
graph TB
    subgraph "Project Root"
        Main[main.py<br/>FastAPI App Entry]
        PyProject[pyproject.toml<br/>Dependencies]
        Dockerfile[Dockerfile<br/>Container Config]
    end
    
    subgraph "API Layer /api/v1"
        Routes[routes/]
        AuthRouter[auth_router.py<br/>Auth Endpoints]
        SeekerRouter[seeker_router.py<br/>Seeker Endpoints]
        EmployerRouter[employer_router.py<br/>Employer Endpoints]
    end
    
    subgraph "Core Layer /core"
        Security[security.py<br/>JWT & Password]
        AIConfig[ai_config.py<br/>LLM Configuration]
    end
    
    subgraph "Services Layer /services"
        SeekerSvc[seeker_services.py<br/>Seeker Business Logic]
        EmployerSvc[employer_services.py<br/>Employer Business Logic]
        N8nSvc[n8n_service.py<br/>Email Integration]
    end
    
    subgraph "AI Layer /ai"
        Chains[chains/<br/>LLM Chains]
        MatchingService[matching_service.py<br/>Job Matching]
        CandidateService[candidate_matching_service.py<br/>Candidate Matching]
        ScoringChain[scoring_chain.py<br/>LLM Scoring]
        RAG[rag/<br/>Vector Ops]
        VectorStore[vector_store.py<br/>ChromaDB Interface]
    end
    
    subgraph "Database Layer /db"
        Settings[settings.py<br/>DB Config]
        SeekerCRUD[seeker_db_ops.py<br/>Seeker CRUD]
        EmployerCRUD[employer_db_ops.py<br/>Employer CRUD]
        ChromaCRUD[chroma_crud_ops.py<br/>Vector CRUD]
        Ingestion[ingestion/<br/>Data Seeding]
    end
    
    subgraph "Schemas Layer /schemas"
        SeekerSchema[seeker.py<br/>Seeker Models]
        EmployerSchema[employer.py<br/>Employer Models]
    end
    
    subgraph "Utils Layer /utils"
        Validators[validators.py<br/>Custom Validators]
        GICSHelper[gics_helper.py<br/>Industry Codes]
    end
    
    Main --> AuthRouter
    Main --> SeekerRouter
    Main --> EmployerRouter
    
    AuthRouter --> Security
    SeekerRouter --> SeekerSvc
    EmployerRouter --> EmployerSvc
    
    SeekerSvc --> SeekerCRUD
    EmployerSvc --> EmployerCRUD
    EmployerSvc --> N8nSvc
    
    SeekerSvc --> MatchingService
    EmployerSvc --> CandidateService
    
    MatchingService --> ScoringChain
    MatchingService --> VectorStore
    CandidateService --> ScoringChain
    CandidateService --> VectorStore
    
    ScoringChain --> AIConfig
    VectorStore --> ChromaCRUD
    
    SeekerCRUD --> Settings
    EmployerCRUD --> Settings
    ChromaCRUD --> Settings
    
    SeekerCRUD --> SeekerSchema
    EmployerCRUD --> EmployerSchema
    
    SeekerSchema --> Validators
    EmployerSchema --> Validators
    EmployerSchema --> GICSHelper
    
    style Main fill:#009688,color:#fff
    style AuthRouter fill:#f57c00,color:#fff
    style MatchingService fill:#10a37f,color:#fff
    style ScoringChain fill:#10a37f,color:#fff
```

### Directory Structure

```
backend/
├── main.py                          # FastAPI application entry point
├── Dockerfile                       # Container configuration
├
├── api/                             # API layer
│   └── v1/                         # API version 1
│       └── routes/                 # Route handlers
│           ├── auth_router.py      # Authentication endpoints
│           ├── seeker_router.py    # Job seeker endpoints
│           └── employer_router.py  # Employer endpoints
│
├── core/                            # Core utilities
│   ├── security.py                 # JWT, password hashing
│   └── ai_config.py                # LLM configuration
│
├── services/                        # Business logic
│   ├── seeker_services.py          # Seeker operations
│   ├── employer_services.py        # Employer operations
│   └── n8n_service.py              # Email integration
│
├── ai/                              # AI/ML components
│   ├── chains/                     # LangChain implementations
│   │   ├── matching_service.py     # Job matching for seekers
│   │   ├── candidate_matching_service.py  # Candidate matching for employers
│   │   └── scoring_chain.py        # LLM scoring logic
│   └── rag/                        # Vector operations
│       └── vector_store.py         # ChromaDB interface
│
├── db/                              # Database layer
│   ├── settings.py                 # DB connection config
│   ├── seeker_db_ops.py            # Seeker CRUD operations
│   ├── employer_db_ops.py          # Employer CRUD operations
│   ├── chroma_crud_ops.py          # Vector DB operations
│   └── ingestion/                  # Data seeding scripts
│       ├── ingest_seeker.py
│       ├── ingest_employer.py
│       ├── ingest_mongo_seeker.py
│       └── ingest_mongo_employer.py
│
├── schemas/                         # Pydantic models
│   ├── seeker.py                   # Seeker document model
│   └── employer.py                 # Employer document model
│
└── utils/                           # Utility functions
    ├── validators.py               # Custom validators (address, phone, email)
    └── gics_helper.py              # Industry classification helper
```

---

## Data Layer Architecture

```mermaid
graph TB
    subgraph "Application Layer"
        Services[Business Services]
    end
    
    subgraph "ODM Layer"
        Beanie[Beanie ODM]
        Pydantic[Pydantic Models]
    end
    
    subgraph "Document Models"
        Seeker[Seeker Document]
        Employer[Employer Document]
    end
    
    subgraph "Sub-Documents"
        Information[Information<br/>Personal Data]
        Application[Application<br/>Job Applications]
        CompanyInfo[CompanyInformation<br/>Company Data]
        OpenJob[OpenJob<br/>Job Postings]
        AppsReceived[ApplicationsReceived<br/>Received Apps]
    end
    
    subgraph "MongoDB Collections"
        SeekersCol[(seekers)]
        EmployersCol[(employers)]
    end
    
    subgraph "ChromaDB Collections"
        SeekerResume[(Seeker_Resume)]
        SeekerSkills[(Seeker_Skills)]
        EmployerJobDescr[(Employer_JobDescr)]
        EmployerSkills[(Employer_Skillswish)]
    end
    
    Services --> Beanie
    Beanie --> Pydantic
    Pydantic --> Seeker
    Pydantic --> Employer
    
    Seeker --> Information
    Seeker --> Application
    Employer --> CompanyInfo
    Employer --> OpenJob
    Employer --> AppsReceived
    
    Seeker --> SeekersCol
    Employer --> EmployersCol
    
    Seeker -.->|Embeddings| SeekerResume
    Seeker -.->|Embeddings| SeekerSkills
    Employer -.->|Embeddings| EmployerJobDescr
    Employer -.->|Embeddings| EmployerSkills
    
    style Beanie fill:#47A248,color:#fff
    style SeekersCol fill:#47A248,color:#fff
    style EmployersCol fill:#47A248,color:#fff
    style SeekerResume fill:#FF6F00,color:#fff
    style SeekerSkills fill:#FF6F00,color:#fff
    style EmployerJobDescr fill:#FF6F00,color:#fff
    style EmployerSkills fill:#FF6F00,color:#fff
```

### MongoDB Schema

#### Seeker Document

```python
{
    "_id": ObjectId("..."),                    # MongoDB primary key
    "seeker_id": PydanticObjectId,            # MongoDB ObjectId
    "seeker_identification": UUID,             # UUID for ChromaDB
    "temperature": 0.75,                       # AI model temperature
    "information": {                           # Personal information
        "first_name": str,
        "last_name": str,
        "email": EmailStr,
        "phone": USPhoneNumber,
        "address": {
            "street": str,
            "city": str,
            "state": StateAbbr,                # Validated US state
            "zip_code": ZipCode                # 5-digit or ZIP+4
        }
    },
    "password_hash": str,                      # BCrypt hashed password
    "created_at": datetime,                    # Account creation
    "resume": str | None,                      # Resume text
    "pay_range": [int, int],                   # [min, max] salary
    "pay_unit": Literal["Hourly", "Monthly", "Yearly"],
    "education_level": Literal["BA", "BS", "MA", "MS", "MBA", "PhD"],
    "edu_focus": str,                          # Field of study
    "key_skills": List[str],                   # Max 15 skills
    "applications": [                          # Job applications
        {
            "job_id": str,                     # Job UUID
            "employer_id": str,                # Employer UUID
            "date_applied": datetime,
            "application_status": Literal["Submitted", "Interviewed", "Offered", "Rejected"]
        }
    ]
}
```

#### Employer Document

```python
{
    "_id": ObjectId("..."),                    # MongoDB primary key
    "employer_id": PydanticObjectId,           # MongoDB ObjectId
    "employer_identification": UUID,           # UUID for ChromaDB
    "company_information": {                   # Company details
        "company_name": str,
        "address": {
            "street": str,
            "city": str,
            "state": StateAbbr,
            "zip_code": ZipCode
        },
        "industry": [                          # Exactly 2 GICS codes
            {
                "code": str,                   # 2, 4, 6, or 8 digits
                "description": str
            }
        ],
        "benefits": str
    },
    "contact_person": {                        # Primary contact
        "contact_first_name": str,
        "contact_last_name": str,
        "email": EmailStr
    },
    "password_hash": str,                      # BCrypt hashed password
    "created_at": datetime,                    # Account creation
    "open_jobs": [                             # Job postings
        {
            "job_id": PydanticObjectId,
            "job_identification": UUID,        # UUID for ChromaDB
            "employer_identification": UUID,    # Employer UUID
            "job_title": str,
            "job_description": str,
            "posted_date": datetime,
            "department": str,
            "hire_mgr_first": str,
            "hire_mgr_last": str,
            "current_status": Literal["Posted", "Withdrawn", "Pending", "Canceled"],
            "pay_range": [int, int],
            "pay_unit": Literal["Hourly", "Monthly", "Yearly"],
            "education_level": Literal["BA", "BS", "MA", "MS", "MBA", "PhD"],
            "edu_focus": str,
            "key_skills": List[str]            # Max 15 skills
        }
    ],
    "apps_received": [                         # Applications received
        {
            "applicant_id": str,               # Seeker UUID
            "job_id": str,                     # Job UUID
            "initial_daterec": datetime,
            "current_status": str,
            "previous_status": str | None,
            "current_status_date": datetime
        }
    ]
}
```

### ChromaDB Schema

#### Collection Structure

Each ChromaDB collection stores:
- **ID**: Unique identifier (seeker_id, job_id, etc.)
- **Embedding**: 1536-dimensional vector from OpenAI
- **Metadata**: Additional searchable fields
- **Document**: Original text content

#### Seeker_Resume Collection

```python
{
    "id": str(seeker_identification),      # UUID
    "embedding": List[float],               # 1536 dimensions
    "metadata": {
        "seeker_id": str,                   # MongoDB ObjectId
        "first_name": str,
        "last_name": str,
        "education_level": str,
        "edu_focus": str,
        "created_at": str
    },
    "document": str                         # Resume text
}
```

#### Employer_JobDescr Collection

```python
{
    "id": str(job_identification),          # UUID
    "embedding": List[float],               # 1536 dimensions
    "metadata": {
        "job_id": str,                      # MongoDB ObjectId
        "employer_id": str,
        "job_title": str,
        "department": str,
        "education_level": str,
        "posted_date": str
    },
    "document": str                         # Job description text
}
```

---

## API Architecture

### API Endpoints Overview

```mermaid
graph LR
    subgraph "Authentication /api/v1/auth"
        A1[POST /auth/login]
        A2[POST /auth/register/seeker]
        A3[POST /auth/register/employer]
        A4[GET /auth/me]
    end
    
    subgraph "Seeker /api/v1/seekers"
        S1[GET /seekers/me]
        S2[PUT /seekers/me]
        S3[POST /seekers/resume]
        S4[GET /seekers/jobs]
        S5[GET /seekers/jobs/:id]
        S6[GET /seekers/recommendations]
        S7[POST /seekers/applications]
        S8[GET /seekers/applications]
        S9[DELETE /seekers/applications/:id]
    end
    
    subgraph "Employer /api/v1/employers"
        E1[GET /employers/me]
        E2[PUT /employers/me]
        E3[GET /employers/jobs]
        E4[POST /employers/jobs]
        E5[GET /employers/jobs/:id]
        E6[PUT /employers/jobs/:id]
        E7[DELETE /employers/jobs/:id]
        E8[GET /employers/jobs/:id/candidates]
        E9[POST /employers/jobs/:id/candidates/:sid/schedule-interview]
        E10[GET /employers/applications]
        E11[GET /employers/n8n/status]
    end
    
    style A1 fill:#f57c00,color:#fff
    style S6 fill:#10a37f,color:#fff
    style E8 fill:#10a37f,color:#fff
```

### API Endpoint Details

#### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/v1/auth/login` | Login and receive JWT token | No |
| `POST` | `/api/v1/auth/register/seeker` | Register new job seeker | No |
| `POST` | `/api/v1/auth/register/employer` | Register new employer | No |
| `GET` | `/api/v1/auth/me` | Get current user information | Yes |

#### Seeker Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/seekers/me` | Get current seeker profile | Yes (Seeker) |
| `PUT` | `/api/v1/seekers/me` | Update seeker profile | Yes (Seeker) |
| `POST` | `/api/v1/seekers/resume` | Upload resume (PDF/DOCX/TXT) | Yes (Seeker) |
| `GET` | `/api/v1/seekers/jobs` | Search available jobs | Yes (Seeker) |
| `GET` | `/api/v1/seekers/jobs/:id` | Get specific job details | Yes (Seeker) |
| `GET` | `/api/v1/seekers/recommendations` | Get AI job recommendations | Yes (Seeker) |
| `POST` | `/api/v1/seekers/applications` | Apply to a job | Yes (Seeker) |
| `GET` | `/api/v1/seekers/applications` | Get all applications | Yes (Seeker) |
| `DELETE` | `/api/v1/seekers/applications/:id` | Withdraw application | Yes (Seeker) |

#### Employer Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/employers/me` | Get current employer profile | Yes (Employer) |
| `PUT` | `/api/v1/employers/me` | Update employer profile | Yes (Employer) |
| `GET` | `/api/v1/employers/jobs` | Get all job postings | Yes (Employer) |
| `POST` | `/api/v1/employers/jobs` | Create new job posting | Yes (Employer) |
| `GET` | `/api/v1/employers/jobs/:id` | Get specific job details | Yes (Employer) |
| `PUT` | `/api/v1/employers/jobs/:id` | Update job posting | Yes (Employer) |
| `DELETE` | `/api/v1/employers/jobs/:id` | Delete job posting | Yes (Employer) |
| `GET` | `/api/v1/employers/jobs/:id/candidates` | Get AI candidate recommendations | Yes (Employer) |
| `POST` | `/api/v1/employers/jobs/:id/candidates/:sid/schedule-interview` | Schedule interview | Yes (Employer) |
| `GET` | `/api/v1/employers/applications` | Get all applications received | Yes (Employer) |
| `GET` | `/api/v1/employers/n8n/status` | Check n8n service status | Yes (Employer) |

### Request/Response Flow

```mermaid
sequenceDiagram
    participant Client
    participant FastAPI
    participant Auth
    participant Service
    participant Database
    participant AI
    
    Note over Client,AI: API Request Flow
    
    Client->>FastAPI: HTTP Request + JWT Token
    FastAPI->>Auth: Validate Token
    
    alt Token Invalid
        Auth-->>FastAPI: 401 Unauthorized
        FastAPI-->>Client: Error Response
    else Token Valid
        Auth->>Auth: Extract User ID & Role
        Auth-->>FastAPI: User Context
        
        FastAPI->>Service: Call Business Logic
        Service->>Database: Query Data
        Database-->>Service: Data
        
        alt AI Operation Required
            Service->>AI: Process with AI
            AI->>AI: LLM/Vector Search
            AI-->>Service: AI Results
        end
        
        Service-->>FastAPI: Processed Data
        FastAPI->>FastAPI: Validate Response
        FastAPI-->>Client: JSON Response
    end
```

---

## AI/ML Architecture

### AI Matching Pipeline

```mermaid
graph TB
    subgraph "Input Layer"
        SeekerReq[Seeker Request<br/>Get Recommendations]
        EmployerReq[Employer Request<br/>Get Candidates]
    end
    
    subgraph "Vector Search Layer"
        GetEmbedding[Retrieve Seeker/Job<br/>Embedding from ChromaDB]
        VectorSearch[Cosine Similarity<br/>Search in ChromaDB]
        TopN[Get Top N Results<br/>n=20 default]
    end
    
    subgraph "Data Enrichment"
        FetchDetails[Fetch Full Details<br/>from MongoDB]
        PrepareContext[Prepare Context<br/>for LLM]
    end
    
    subgraph "LLM Scoring Layer"
        BuildPrompt[Build LLM Prompt<br/>with Seeker & Job Data]
        CallLLM[Call OpenAI GPT-4o-mini]
        ParseOutput[Parse Structured Output<br/>Pydantic Parser]
    end
    
    subgraph "Output Layer"
        ScoreBreakdown[Match Score Breakdown<br/>Skills, Education, Pay, Experience]
        Reasoning[LLM Reasoning<br/>Explanation]
        RankResults[Rank by Overall Score]
        FilterResults[Filter by Min Score<br/>min_score default=0.0]
        ReturnJSON[Return JSON Response]
    end
    
    SeekerReq --> GetEmbedding
    EmployerReq --> GetEmbedding
    
    GetEmbedding --> VectorSearch
    VectorSearch --> TopN
    TopN --> FetchDetails
    FetchDetails --> PrepareContext
    
    PrepareContext --> BuildPrompt
    BuildPrompt --> CallLLM
    CallLLM --> ParseOutput
    
    ParseOutput --> ScoreBreakdown
    ParseOutput --> Reasoning
    ScoreBreakdown --> RankResults
    RankResults --> FilterResults
    FilterResults --> ReturnJSON
    
    style GetEmbedding fill:#FF6F00,color:#fff
    style VectorSearch fill:#FF6F00,color:#fff
    style CallLLM fill:#10a37f,color:#fff
    style ParseOutput fill:#10a37f,color:#fff
```

### LLM Scoring Chain

```mermaid
graph LR
    subgraph "Input Data"
        SeekerData[Seeker Profile<br/>Skills, Education,<br/>Pay, Resume]
        JobData[Job Posting<br/>Requirements,<br/>Description, Pay]
    end
    
    subgraph "Prompt Template"
        SystemPrompt[System Prompt<br/>Expert Analyst Role]
        HumanPrompt[Human Prompt<br/>Match Analysis Request]
        FormatInstr[Format Instructions<br/>Pydantic Schema]
    end
    
    subgraph "LLM Processing"
        ChatOpenAI[ChatOpenAI<br/>gpt-4o-mini<br/>temp=0.75]
    end
    
    subgraph "Output Parsing"
        PydanticParser[Pydantic Parser<br/>MatchScoreBreakdown]
    end
    
    subgraph "Structured Output"
        SkillsScore[skills_score: 0-100]
        EduScore[education_score: 0-100]
        PayScore[pay_score: 0-100]
        ExpScore[experience_score: 0-100]
        OverallScore[overall_score: 0-100<br/>Weighted Average]
        Reasoning[reasoning: str<br/>Explanation]
    end
    
    SeekerData --> HumanPrompt
    JobData --> HumanPrompt
    
    SystemPrompt --> ChatOpenAI
    HumanPrompt --> ChatOpenAI
    FormatInstr --> ChatOpenAI
    
    ChatOpenAI --> PydanticParser
    
    PydanticParser --> SkillsScore
    PydanticParser --> EduScore
    PydanticParser --> PayScore
    PydanticParser --> ExpScore
    PydanticParser --> OverallScore
    PydanticParser --> Reasoning
    
    style ChatOpenAI fill:#10a37f,color:#fff
    style PydanticParser fill:#10a37f,color:#fff
```

### Scoring Weights

```python
# Overall Score Calculation (Weighted Average)
overall_score = (
    skills_score * 0.40 +        # 40% weight - most important
    education_score * 0.20 +     # 20% weight
    pay_score * 0.20 +           # 20% weight
    experience_score * 0.20      # 20% weight
)
```

### Match Score Interpretation

| Score Range | Match Quality | Description |
|-------------|---------------|-------------|
| 0-40 | Poor | Significant mismatches in requirements |
| 41-70 | Moderate | Some alignment but notable gaps |
| 71-85 | Good | Strong alignment with minor gaps |
| 86-100 | Excellent | Exceptional match, highly recommended |

---

## Security Architecture

### Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant FastAPI
    participant Security
    participant MongoDB
    
    Note over User,MongoDB: Registration Flow
    
    User->>Frontend: Enter Registration Data
    Frontend->>FastAPI: POST /auth/register/{role}
    FastAPI->>Security: hash_password(password)
    Security-->>FastAPI: hashed_password
    FastAPI->>MongoDB: Create User Document
    MongoDB-->>FastAPI: User Created
    FastAPI-->>Frontend: Success Response
    
    Note over User,MongoDB: Login Flow
    
    User->>Frontend: Enter Credentials
    Frontend->>FastAPI: POST /auth/login
    FastAPI->>MongoDB: Find User by Email & Role
    MongoDB-->>FastAPI: User Document
    FastAPI->>Security: verify_password(plain, hash)
    
    alt Password Invalid
        Security-->>FastAPI: False
        FastAPI-->>Frontend: 401 Unauthorized
    else Password Valid
        Security-->>FastAPI: True
        FastAPI->>Security: create_access_token(user_id, role)
        Security-->>FastAPI: JWT Token
        FastAPI-->>Frontend: Token + User Data
        Frontend->>Frontend: Store Token in localStorage
    end
    
    Note over User,MongoDB: Protected Request
    
    User->>Frontend: Access Protected Page
    Frontend->>FastAPI: GET /api/... + Bearer Token
    FastAPI->>Security: decode_access_token(token)
    
    alt Token Invalid/Expired
        Security-->>FastAPI: 401 Exception
        FastAPI-->>Frontend: 401 Unauthorized
        Frontend->>Frontend: Clear Token & Redirect Login
    else Token Valid
        Security-->>FastAPI: User ID & Role
        FastAPI->>MongoDB: Fetch User Data
        MongoDB-->>FastAPI: User Data
        FastAPI-->>Frontend: Protected Resource
    end
```

### Role-Based Access Control (RBAC)

```mermaid
graph TB
    subgraph "User Roles"
        Seeker[Seeker Role]
        Employer[Employer Role]
    end
    
    subgraph "Seeker Permissions"
        S1[View Own Profile]
        S2[Update Own Profile]
        S3[Upload Resume]
        S4[Search Jobs]
        S5[View Job Details]
        S6[Apply to Jobs]
        S7[View Own Applications]
        S8[Get Recommendations]
    end
    
    subgraph "Employer Permissions"
        E1[View Own Profile]
        E2[Update Own Profile]
        E3[Create Job Postings]
        E4[Update Job Postings]
        E5[Delete Job Postings]
        E6[View Applications]
        E7[Get Candidate Recommendations]
        E8[Schedule Interviews]
    end
    
    Seeker --> S1
    Seeker --> S2
    Seeker --> S3
    Seeker --> S4
    Seeker --> S5
    Seeker --> S6
    Seeker --> S7
    Seeker --> S8
    
    Employer --> E1
    Employer --> E2
    Employer --> E3
    Employer --> E4
    Employer --> E5
    Employer --> E6
    Employer --> E7
    Employer --> E8
    
    style Seeker fill:#4caf50,color:#fff
    style Employer fill:#2196f3,color:#fff
```

### Security Features

#### 1. Password Security
- **Algorithm**: BCrypt with automatic salt generation
- **Cost Factor**: 12 rounds (2^12 = 4096 iterations)
- **Password Limit**: 72 bytes (BCrypt standard)
- **Minimum Length**: 6 characters (configurable)

#### 2. JWT Token Security
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Secret Key**: Stored in environment variable
- **Expiration**: 30 days (configurable)
- **Payload**: User ID (sub), role, expiration (exp)
- **Storage**: localStorage on frontend

#### 3. Input Validation
- **Email**: RFC 5322 compliant validation
- **Phone**: Google libphonenumber validation
- **Address**: US state/ZIP code validation
- **GICS Codes**: Industry code validation

#### 4. API Security
- **CORS**: Whitelist of allowed origins
- **Rate Limiting**: (Ready for implementation)
- **HTTPS**: Production deployment requirement
- **Token Refresh**: (Ready for implementation)

---

## Integration Architecture

### n8n Workflow Integration

```mermaid
graph LR
    subgraph "Backend"
        Employer[Employer Action<br/>Schedule Interview]
        N8nService[N8n Service]
    end
    
    subgraph "n8n Workflow"
        Webhook[Webhook Trigger<br/>/webhook/interview-schedule]
        ParseData[Parse Interview Data]
        FormatEmail[Format Email Template]
        SendEmail[Send Email Node]
    end
    
    subgraph "External"
        EmailService[Email Service<br/>Gmail/SMTP]
        Seeker[Job Seeker Email]
    end
    
    Employer --> N8nService
    N8nService -->|POST JSON| Webhook
    Webhook --> ParseData
    ParseData --> FormatEmail
    FormatEmail --> SendEmail
    SendEmail --> EmailService
    EmailService --> Seeker
    
    style Webhook fill:#ea4b71,color:#fff
    style SendEmail fill:#ea4b71,color:#fff
```

### Interview Scheduling Flow

```mermaid
sequenceDiagram
    participant Employer
    participant Backend
    participant N8nService
    participant n8n
    participant EmailService
    participant Seeker
    
    Employer->>Backend: Schedule Interview
    Backend->>Backend: Validate Interview Data
    Backend->>N8nService: trigger_interview_workflow()
    
    N8nService->>N8nService: Prepare Payload
    N8nService->>n8n: POST /webhook/interview-schedule
    
    alt n8n Available
        n8n->>n8n: Parse Interview Data
        n8n->>n8n: Format Email Template
        n8n->>EmailService: Send Email
        EmailService->>Seeker: Interview Invitation Email
        n8n-->>N8nService: 200 OK
        N8nService-->>Backend: Success
        Backend-->>Employer: Interview Scheduled
    else n8n Unavailable
        n8n-->>N8nService: Timeout/Error
        N8nService-->>Backend: Failed
        Backend-->>Employer: Warning (n8n unavailable)
    end
```

### Email Template Data

```python
{
    "seeker_email": "john@example.com",
    "job_title": "Senior Software Engineer",
    "employer_name": "Tech Company Inc.",
    "employer_email": "hr@techcompany.com",
    "interview_date": "December 15, 2024",
    "interview_time": "2:00 PM",
    "interview_type": "Video",  # In-person | Video | Phone
    "location_or_link": "https://meet.google.com/abc-defg-hij",
    "notes": "Please bring your portfolio"
}
```

---

## User Flow Diagrams

### 1. Job Seeker Registration & Recommendations Flow

```mermaid
flowchart TD
    Start([Seeker Visits Site]) --> Register[Registration Page]
    Register --> FillForm[Fill Seeker Form<br/>Name, Email, Skills, etc.]
    FillForm --> UploadResume{Upload Resume?}
    
    UploadResume -->|Yes| ProcessFile[Backend Processes File<br/>PDF/DOCX/TXT]
    UploadResume -->|No| SkipResume[Continue without Resume]
    
    ProcessFile --> ExtractText[Extract Text Content]
    ExtractText --> HashPwd[Hash Password with BCrypt]
    SkipResume --> HashPwd
    
    HashPwd --> CreateMongo[Create Seeker in MongoDB<br/>with UUID]
    CreateMongo --> GenerateEmbed[Generate OpenAI Embeddings<br/>for Resume & Skills]
    GenerateEmbed --> StoreChroma[Store in ChromaDB<br/>4 Collections]
    
    StoreChroma --> LoginPage[Redirect to Login]
    LoginPage --> EnterCreds[Enter Credentials]
    EnterCreds --> ValidateAuth{Credentials Valid?}
    
    ValidateAuth -->|No| ShowError[Show Error]
    ShowError --> LoginPage
    
    ValidateAuth -->|Yes| CreateJWT[Create JWT Token<br/>30 day expiry]
    CreateJWT --> Dashboard[Seeker Dashboard]
    
    Dashboard --> Action{Choose Action}
    
    Action -->|Recommendations| GetRecs[GET /seekers/recommendations]
    GetRecs --> RetrieveEmbed[Retrieve Seeker Embedding<br/>from ChromaDB]
    RetrieveEmbed --> VectorSearch[Vector Similarity Search<br/>Top 20 Jobs]
    VectorSearch --> FetchJobs[Fetch Job Details<br/>from MongoDB]
    FetchJobs --> LLMScore[LLM Scoring for Each Job<br/>GPT-4o-mini]
    LLMScore --> Breakdown[Score Breakdown<br/>Skills, Education, Pay, Experience]
    Breakdown --> RankJobs[Rank by Overall Score]
    RankJobs --> DisplayRecs[Display Recommendations<br/>with Scores & Reasoning]
    
    Action -->|Search Jobs| SearchJobs[GET /seekers/jobs]
    SearchJobs --> FilterJobs[Filter by Title/Company/Skills]
    FilterJobs --> ViewJob[View Job Details]
    
    ViewJob --> Apply{Apply?}
    Apply -->|Yes| SubmitApp[POST /seekers/applications]
    Apply -->|No| SearchJobs
    
    SubmitApp --> UpdateMongo[Update MongoDB<br/>Add to Applications Array]
    UpdateMongo --> NotifyEmployer[Add to Employer<br/>apps_received Array]
    NotifyEmployer --> ConfirmApp[Show Confirmation]
    
    style GetRecs fill:#10a37f,color:#fff
    style VectorSearch fill:#FF6F00,color:#fff
    style LLMScore fill:#10a37f,color:#fff
```

### 2. Employer Job Posting & Candidate Matching Flow

```mermaid
flowchart TD
    Start([Employer Visits Site]) --> Register[Registration Page]
    Register --> FillForm[Fill Employer Form<br/>Company, Industry, etc.]
    FillForm --> ValidateGICS[Validate GICS Codes<br/>Industry Classification]
    ValidateGICS --> HashPwd[Hash Password with BCrypt]
    HashPwd --> CreateMongo[Create Employer in MongoDB<br/>with UUID]
    CreateMongo --> Login[Login Page]
    
    Login --> CreateJWT[Create JWT Token]
    CreateJWT --> Dashboard[Employer Dashboard]
    
    Dashboard --> Action{Choose Action}
    
    Action -->|Create Job| NewJob[Create Job Form]
    NewJob --> FillJob[Fill Job Details<br/>Title, Description, Skills, etc.]
    FillJob --> SubmitJob[POST /employers/jobs]
    
    SubmitJob --> JobToMongo[Add Job to MongoDB<br/>open_jobs Array]
    JobToMongo --> GenerateJobEmbed[Generate OpenAI Embeddings<br/>for Job Description & Skills]
    GenerateJobEmbed --> StoreJobChroma[Store in ChromaDB<br/>2 Collections]
    StoreJobChroma --> JobCreated[Job Posted Successfully]
    
    Action -->|View Candidates| SelectJob[Select Job Posting]
    SelectJob --> GetCandidates[GET /employers/jobs/:id/candidates]
    GetCandidates --> RetrieveJobEmbed[Retrieve Job Embedding<br/>from ChromaDB]
    RetrieveJobEmbed --> VectorSearchSeekers[Vector Similarity Search<br/>Top 20 Seekers]
    VectorSearchSeekers --> FetchSeekers[Fetch Seeker Details<br/>from MongoDB]
    FetchSeekers --> LLMScoreCand[LLM Scoring for Each Candidate<br/>GPT-4o-mini]
    LLMScoreCand --> CandBreakdown[Score Breakdown<br/>Skills, Education, Pay, Experience]
    CandBreakdown --> RankCandidates[Rank by Overall Score]
    RankCandidates --> FilterApplied[Check if Already Applied]
    FilterApplied --> DisplayCands[Display Candidates<br/>with Scores & Reasoning]
    
    DisplayCands --> ReviewCand[Review Candidate Profile]
    ReviewCand --> ScheduleInt{Schedule Interview?}
    
    ScheduleInt -->|Yes| InterviewForm[Fill Interview Form<br/>Date, Time, Type, Location]
    InterviewForm --> SubmitInterview[POST /employers/jobs/:id/candidates/:sid/schedule-interview]
    SubmitInterview --> TriggerN8n[Trigger n8n Workflow<br/>via Webhook]
    
    TriggerN8n --> CheckN8n{n8n Available?}
    CheckN8n -->|Yes| SendEmail[n8n Sends Email<br/>to Candidate]
    CheckN8n -->|No| ShowWarning[Show Warning<br/>Email not sent]
    
    SendEmail --> UpdateStatus[Update Application Status]
    ShowWarning --> UpdateStatus
    UpdateStatus --> ConfirmSchedule[Show Confirmation]
    
    ScheduleInt -->|No| DisplayCands
    
    style GetCandidates fill:#10a37f,color:#fff
    style VectorSearchSeekers fill:#FF6F00,color:#fff
    style LLMScoreCand fill:#10a37f,color:#fff
    style TriggerN8n fill:#ea4b71,color:#fff
```

### 3. AI Matching Pipeline Detailed Flow

```mermaid
flowchart TD
    Start([Matching Request]) --> CheckType{Request Type}
    
    CheckType -->|Seeker Recommendations| SeekerFlow[Seeker Flow]
    CheckType -->|Employer Candidates| EmployerFlow[Employer Flow]
    
    SeekerFlow --> GetSeekerEmbed[Get Seeker Embedding<br/>from ChromaDB]
    GetSeekerEmbed --> SearchJobs[Vector Search in<br/>Employer_JobDescr Collection]
    SearchJobs --> TopJobs[Top N Jobs<br/>by Cosine Similarity]
    
    EmployerFlow --> GetJobEmbed[Get Job Embedding<br/>from ChromaDB]
    GetJobEmbed --> SearchSeekers[Vector Search in<br/>Seeker_Resume Collection]
    SearchSeekers --> TopSeekers[Top N Seekers<br/>by Cosine Similarity]
    
    TopJobs --> FetchJobData[Fetch Complete Job Data<br/>from MongoDB]
    TopSeekers --> FetchSeekerData[Fetch Complete Seeker Data<br/>from MongoDB]
    
    FetchJobData --> PreparePrompt[Prepare LLM Prompt]
    FetchSeekerData --> PreparePrompt
    
    PreparePrompt --> BuildContext[Build Full Context:<br/>Seeker Profile + Job Requirements]
    
    BuildContext --> ForEachMatch{For Each Match}
    
    ForEachMatch --> CallLLM[Call OpenAI GPT-4o-mini<br/>with Scoring Prompt]
    CallLLM --> LLMAnalysis[LLM Analyzes Match]
    
    LLMAnalysis --> ParseStruct[Parse Structured Output<br/>Pydantic Parser]
    ParseStruct --> ExtractScores[Extract Scores:<br/>Skills, Education, Pay, Experience]
    ExtractScores --> CalcOverall[Calculate Weighted Overall<br/>Skills 40%, Others 20% each]
    CalcOverall --> ExtractReason[Extract Reasoning<br/>from LLM]
    
    ExtractReason --> MoreMatches{More Matches?}
    MoreMatches -->|Yes| ForEachMatch
    MoreMatches -->|No| RankAll[Rank All Results<br/>by Overall Score]
    
    RankAll --> FilterScore[Filter by min_score<br/>default: 0.0]
    FilterScore --> FormatResponse[Format JSON Response]
    FormatResponse --> Return[Return to Client]
    
    style GetSeekerEmbed fill:#FF6F00,color:#fff
    style GetJobEmbed fill:#FF6F00,color:#fff
    style SearchJobs fill:#FF6F00,color:#fff
    style SearchSeekers fill:#FF6F00,color:#fff
    style CallLLM fill:#10a37f,color:#fff
    style LLMAnalysis fill:#10a37f,color:#fff
```

---

## Performance Considerations

### 1. Database Optimization
- **MongoDB Indexes**: Automatic indexing on _id, email, UUIDs
- **Beanie Caching**: Document caching for frequently accessed data
- **Connection Pooling**: Motor async connection pooling
- **ChromaDB**: Local persistent storage for fast vector ops

### 2. AI/ML Optimization
- **Batch Processing**: Score multiple candidates/jobs in parallel
- **Embedding Caching**: Store embeddings to avoid regeneration
- **LLM Model**: GPT-4o-mini for cost and speed balance
- **Vector Search**: Cosine similarity for efficient nearest neighbor

### 3. API Optimization
- **Async Operations**: Non-blocking I/O throughout stack
- **Response Streaming**: (Ready for large result sets)
- **Compression**: Gzip response compression
- **Caching**: (Ready for Redis implementation)

### 4. Scalability
- **Stateless API**: Easy horizontal scaling
- **Database Sharding**: MongoDB Atlas auto-sharding
- **Load Balancing**: Ready for multi-instance deployment
- **Microservices**: Modular architecture for service separation

---

## Deployment Architecture

```mermaid
graph TB
    subgraph "Docker Compose"
        Backend[Backend Container<br/>Python 3.12-slim<br/>Port 8000]
        Frontend[Frontend Container<br/>Node 20-slim<br/>Port 3000]
        N8n[n8n Container<br/>Latest<br/>Port 5678]
    end
    
    subgraph "External Services"
        MongoDB[MongoDB Atlas<br/>Cloud Database]
        OpenAI[OpenAI API<br/>GPT-4o-mini + Embeddings]
        LangSmith[LangSmith<br/>Optional Tracing]
    end
    
    subgraph "Persistent Storage"
        ChromaVolume[./chroma_db<br/>ChromaDB Persistent Storage]
        LogsVolume[./Logs<br/>Application Logs]
        N8nVolume[./n8n_data<br/>Workflow Data]
    end
    
    Backend --> MongoDB
    Backend --> OpenAI
    Backend --> ChromaVolume
    Backend --> LogsVolume
    Backend -.->|Optional| LangSmith
    
    Backend <--> N8n
    N8n --> N8nVolume
    
    Frontend --> Backend
    
    style Backend fill:#009688,color:#fff
    style Frontend fill:#000000,color:#fff
    style N8n fill:#ea4b71,color:#fff
    style MongoDB fill:#47A248,color:#fff
    style OpenAI fill:#10a37f,color:#fff
```

### Environment Variables

```bash
# MongoDB Configuration
MONGO_DB_USER=test_db_user
MONGO_DB_PASSWORD=<secret>
MONGO_DB_URL=mongodb+srv://${MONGO_DB_USER}:${MONGO_DB_PASSWORD}@cluster.mongodb.net/?appName=job-portal
MONGO_DB_NAME=job-portal

# ChromaDB Configuration
CHROMA_PC_PATH=./chroma_db

# OpenAI Configuration
OPENAI_API_KEY=<secret>
OPENAI_MODEL=gpt-4o-mini

# LangSmith Configuration (Optional)
LANGSMITH_API_KEY=<secret>
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=job_portal

# n8n Configuration
N8N_WEBHOOK_URL=http://n8n:5678/webhook/interview-schedule

# CORS Configuration
CORS_ORIGINS=http://localhost:3000
ALLOW_ORIGINS=http://localhost:3000
```

---

## Error Handling & Logging

### Logging Strategy

```mermaid
graph LR
    subgraph "Log Levels"
        Debug[DEBUG<br/>Development Info]
        Info[INFO<br/>General Events]
        Warning[WARNING<br/>Potential Issues]
        Error[ERROR<br/>Caught Exceptions]
        Critical[CRITICAL<br/>System Failures]
    end
    
    subgraph "Log Destinations"
        Console[Console Output<br/>Development]
        DebugLog[Debug_log.log<br/>All DEBUG+ events]
        ErrorLog[Error_log.log<br/>Only ERROR+ events]
    end
    
    Debug --> Console
    Info --> Console
    Warning --> Console
    Error --> Console
    Critical --> Console
    
    Debug --> DebugLog
    Info --> DebugLog
    Warning --> DebugLog
    Error --> DebugLog
    Critical --> DebugLog
    
    Error --> ErrorLog
    Critical --> ErrorLog
    
    style Console fill:#78909c
    style DebugLog fill:#4caf50,color:#fff
    style ErrorLog fill:#f44336,color:#fff
```

### Error Response Format

```python
{
    "detail": "Error message",
    "status_code": 400,
    "error_type": "ValidationError"
}
```

---

## Future Enhancements

1. **Performance Improvements**
   - Redis caching for frequent queries
   - Celery for background job processing
   - Database query optimization

2. **Advanced Features**
   - WebSocket support for real-time updates
   - GraphQL API option
   - Advanced search filters
   - Saved searches and alerts

3. **AI Enhancements**
   - Fine-tuned models for domain-specific matching
   - Resume parsing with AI
   - Interview question generation
   - Candidate skill gap analysis

4. **Security Enhancements**
   - OAuth2 provider integration
   - Two-factor authentication
   - API rate limiting with Redis
   - Token refresh mechanism

5. **Monitoring & Observability**
   - Prometheus metrics
   - Grafana dashboards
   - Error tracking (Sentry)
   - Performance monitoring (New Relic)

---

## Conclusion

The WorkAtlas backend is a modern, scalable, and AI-powered job portal API built with FastAPI, MongoDB, ChromaDB, and LangChain. It provides:

- **High Performance**: Async operations throughout the stack
- **Type Safety**: Pydantic validation and Python type hints
- **AI-Powered**: LLM-based matching with detailed reasoning
- **Secure**: JWT authentication, BCrypt hashing, input validation
- **Scalable**: Stateless architecture ready for horizontal scaling
- **Developer Friendly**: Auto-generated docs, structured code, comprehensive logging

The modular architecture and clean separation of concerns provide a solid foundation for future enhancements and scalability.

---

**Document Version**: 1.0  
**Last Updated**: November 17, 2025  
**Author**: System Architecture Analysis  
**Project**: WorkAtlas Job Portal Backend

