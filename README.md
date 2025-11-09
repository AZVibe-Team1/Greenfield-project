# Job Portal - Greenfield Project

A secure, scalable, and user-friendly platform connecting job seekers and employers with AI-powered recommendations.


**JM!!** - Right now, the containers bring up only the backend as I thought it would be easiest to start with one container.
The code added to /backend is temporary to show that the backend FastAPI runs at a basic level.

## Docker Setup

This project uses Docker Compose for containerized development and deployment.

### Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose v2.0+

### Installing Docker

#### Windows

1. **Download Docker Desktop:**
   - Visit [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
   - Click "Download for Windows"
   - Download the installer (`Docker Desktop Installer.exe`)

2. **Install Docker Desktop:**
   - Run the installer
   - Follow the installation wizard
   - When prompted, ensure "Use WSL 2 instead of Hyper-V" is checked (recommended)
   - Restart your computer if prompted

3. **Launch Docker Desktop:**
   - After restart, launch Docker Desktop from the Start menu
   - Accept the service agreement
   - Wait for Docker to start (the Docker icon in the system tray will show "Docker Desktop is running")

4. **Verify Installation:**
   ```bash
   docker --version
   docker compose version
   ```

#### macOS

1. **Choose Your Mac Type:**
   - **Apple Silicon (M1/M2/M3)**: Download "Mac with Apple chip"
   - **Intel Mac**: Download "Mac with Intel chip"

2. **Download Docker Desktop:**
   - Visit [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
   - Click "Download for Mac"
   - The download will be a `.dmg` file

3. **Install Docker Desktop:**
   - Open the downloaded `.dmg` file
   - Drag Docker.app to your Applications folder
   - Open Docker from Applications (or Spotlight search)
   - Click "Open" when macOS asks for confirmation

4. **Complete Setup:**
   - Docker Desktop will start and may ask for your password to install networking components
   - Wait for Docker to finish starting (the Docker icon in the menu bar will show "Docker Desktop is running")

5. **Verify Installation:**
   ```bash
   docker --version
   docker compose version
   ```

**Note:** Docker Desktop includes Docker Compose, so you don't need to install it separately.

### Quick Start

1. **Copy environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and fill in your configuration values.

2. **Run the backend service:**
   ```bash
   docker compose run backend
   ```
   The backend API will be available at `http://localhost:8000`

   JM!! - Open a terminal in the backend container: 
    ```bash
   docker compose run backend bash
   ```

3. **Run the frontend service** (when ready):
   ```bash
   docker compose run frontend
   ```
   The frontend will be available at `http://localhost:3000`

4. **Run all services together:**
   ```bash
   docker compose up
   ```
   This starts all services (backend, frontend, and MongoDB) defined in `docker-compose.yml`


   **JM!!** - Rebuild all containers (start fresh build):
   ```bash
   docker compose up --build
   ```

   **JM!!** - Clean up containers (good to run after done with developing session):
   ```bash
   docker compose down -v --remove-orphans
   ```

   **JM!!** - To view what containers you have running:
   ```bash
   docker ps
   ```

### Docker Services

- **backend**: FastAPI application (Python 3.12+, uv package manager)
- **frontend**: Next.js 14 application (currently commented out)
- **mongodb**: MongoDB 6.x database (currently commented out)

### Development

The Docker setup includes volume mounts for hot-reload during development. Code changes will be reflected automatically without rebuilding containers.

### Environment Variables

See `.env.example` for all required environment variables. Key variables include:
- Database connection strings
- JWT secrets
- AI/LLM API keys
- Email configuration
- CORS settings

---

## Project Structure

- `backend/` - FastAPI backend application
- `frontend/` - Next.js frontend application
- `docker-compose.yml` - Docker Compose configuration
- `.env.example` - Environment variables template

## ChromaDB Quick Start Guide

### Overview

✅ **ChromaDB RAG setup is complete!** Vector database configured with OpenAI embeddings for intelligent job portal features.

### Components

**Mock Data** (`backend/chroma_data/`):
- `job_postings.txt` - Sample tech job listings
- `company_profiles.txt` - Company information
- `interview_tips.txt` - Interview preparation
- `resume_writing.txt` - Resume best practices
- `career_development.txt` - Career advice

**Ingestion Script** (`backend/ingest_data.py`):
- Loads and chunks text documents
- Generates embeddings via OpenAI's `text-embedding-3-small`
- Persists to ChromaDB at `CHROMA_PC_PATH`
- Includes verification and logging

**Dependencies** (`pyproject.toml`):
- `chromadb` - Vector database
- `openai` - Embeddings API
- `python-dotenv` - Environment management

### Usage

### 1. Configure Environment

Ensure `.env` file contains:
```env
OPENAI_API_KEY=your-api-key-here
CHROMA_PC_PATH=./chroma_db
```

### 2. Run Ingestion

**Docker (Recommended):**
```bash
docker compose run backend uv run backend/ingest_data.py
```

**Local:**
```bash
uv run backend/ingest_data.py
```

### 3. Verify

Successful output:
```
✓ Loaded 5 documents
✓ Created 61 chunks from 5 documents
✓ OpenAI embeddings initialized
✓ Vector store created with 61 chunks
✅ Data ingestion completed successfully!
```

### 4. Query the Vector Store

```python
import chromadb
from chromadb.config import Settings
from openai import OpenAI

# Load persisted ChromaDB
client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=Settings(anonymized_telemetry=False)
)
collection = client.get_collection(name="job_portal_knowledge")

# Generate query embedding
openai_client = OpenAI()
query = "What are the requirements for a backend engineer?"
embedding = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input=[query]
).data[0].embedding

# Search
results = collection.query(
    query_embeddings=[embedding],
    n_results=3
)
```

### Configuration

**Required Environment Variables:**
```env
OPENAI_API_KEY=sk-...              # Required for embeddings
CHROMA_PC_PATH=./chroma_db         # Vector store location
```

**ChromaDB Settings:**
- **Collection Name:** `job_portal_knowledge`
- **Embedding Model:** `text-embedding-3-small` (1536 dimensions)
- **Persistence:** Enabled via `PersistentClient`
- **Settings:** `anonymized_telemetry=False`, `allow_reset=True`

### Adding More Data

1. Add `.txt` files to `backend/chroma_data/`
2. Re-run ingestion: `docker compose run backend uv run backend/ingest_data.py`

### File Structure

```
backend/
├── chroma_data/           # Source documents
├── ingest_data.py         # Ingestion script
└── ai/rag/               # RAG implementation (TODO)

chroma_db/                # Persisted vector store
└── [generated files]
```

### Next Steps

1. Implement RAG endpoints in `backend/ai/rag/`
2. Build AI features: job recommendations, resume analysis, interview prep
3. Integrate with frontend for intelligent responses

### Troubleshooting

| Issue | Solution |
|-------|----------|
| No documents found | Verify `.txt` files exist in `backend/chroma_data/` |
| Dependencies missing | Run `uv sync` or rebuild Docker: `docker compose build backend` |
| OpenAI API errors | Verify `OPENAI_API_KEY` is set correctly in `.env` |

---

**Status:** ✅ Ready for RAG implementation