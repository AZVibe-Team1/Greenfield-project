# Job Portal - Greenfield Project

A secure, scalable, and user-friendly platform connecting job seekers and employers with AI-powered recommendations.

## Docker Setup

This project uses Docker Compose for containerized development and deployment.

### Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose v2.0+

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