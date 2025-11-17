# Job Portal - Technical Documentation

## Overview

This is a full-stack Job Portal application connecting job seekers with employers through an intuitive, modern interface.

### Technology Stack

- **Backend**: FastAPI (Python 3.12+) with MongoDB
- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS, and lucide-react icons
- **Package Management**: `uv` for Python, `npm` for Node.js
- **Docker**: Containerized services with hot-reload for development
- **Design**: Modern, unified design system with role-based color themes (Emerald for seekers, Blue for employers)

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Git (optional)

### Option 1: Using the Start Script (Recommended)

```bash
./start.sh
```

This automatically handles port conflicts and starts all services.

### Option 2: Manual Start

```bash
# Stop any conflicting processes
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9

# Start services
docker-compose up --build
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Health Check**: http://localhost:8000/health
- **DB Status**: http://localhost:8000/db-status

### Stop Services

```bash
# Press Ctrl+C in the terminal, then:
docker-compose down

# To remove volumes and clean up completely:
docker-compose down -v --remove-orphans
```

## 📋 API Endpoints

### Authentication (`/api/v1/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/login` | Login (seeker or employer) | No |
| POST | `/api/v1/auth/register/seeker` | Register as job seeker | No |
| POST | `/api/v1/auth/register/employer` | Register as employer | No |

### Job Seeker Routes (`/api/v1/seekers`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/seekers/me` | Get current user profile | Yes (Seeker) |
| PUT | `/api/v1/seekers/me` | Update profile | Yes (Seeker) |
| POST | `/api/v1/seekers/resume` | Upload resume | Yes (Seeker) |
| POST | `/api/v1/seekers/applications` | Apply for a job | Yes (Seeker) |
| GET | `/api/v1/seekers/applications` | Get my applications | Yes (Seeker) |
| DELETE | `/api/v1/seekers/applications/{job_id}` | Withdraw application | Yes (Seeker) |
| GET | `/api/v1/seekers/jobs` | Search jobs with filters | Yes (Seeker) |
| GET | `/api/v1/seekers/jobs/{job_id}` | Get job details | Yes (Seeker) |

**Job Search Filters:**
- `title`: Filter by job title
- `company_name`: Filter by company
- `skill`: Filter by required skill

### Employer Routes (`/api/v1/employers`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/employers/me` | Get current profile | Yes (Employer) |
| PUT | `/api/v1/employers/me` | Update profile | Yes (Employer) |
| POST | `/api/v1/employers/jobs` | Create job posting | Yes (Employer) |
| GET | `/api/v1/employers/jobs` | Get my job postings | Yes (Employer) |
| GET | `/api/v1/employers/jobs/{job_id}` | Get job details | Yes (Employer) |
| PUT | `/api/v1/employers/jobs/{job_id}` | Update job posting | Yes (Employer) |
| DELETE | `/api/v1/employers/jobs/{job_id}` | Delete job posting | Yes (Employer) |
| GET | `/api/v1/employers/applications` | Get applications received | Yes (Employer) |

## 🎨 Frontend Architecture

### Pages & Routes

#### Public Pages (No Authentication Required)
- **`/`** - Landing page with hero section, features, and call-to-action
- **`/login`** - Login page for both seekers and employers
- **`/register`** - Multi-step registration flow with role selection

#### Job Seeker Pages (Seeker Authentication Required)
- **`/seeker/dashboard`** - Overview with recent applications and recommended jobs
- **`/seeker/jobs`** - Job search with real-time filtering (title, company, skills)
- **`/seeker/applications`** - Track application status and history
- **`/seeker/profile`** - Manage profile, education, and skills

#### Employer Pages (Employer Authentication Required)
- **`/employer/dashboard`** - Overview with job postings and application stats
- **`/employer/jobs`** - Manage all job postings (edit, delete, view)
- **`/employer/jobs/new`** - Create new job posting with rich form
- **`/employer/applications`** - Review and manage received applications

### Design System

#### Color Themes
- **Job Seeker**: Emerald green (`emerald-600`, `emerald-50`)
- **Employer**: Blue (`blue-600`, `blue-50`)
- **Neutral**: Slate grays for backgrounds and text

#### Components
- Unified button styles with hover states
- Consistent form inputs with validation
- Card layouts for content organization
- Responsive navigation with role-based menus
- Icons from `lucide-react`

### State Management
- **Authentication**: Zustand store (`store/auth-store.ts`)
- **Local Storage**: JWT tokens for persistent sessions
- **API Client**: Centralized HTTP client (`lib/api-client.ts`) with automatic token injection

## 🛠️ Local Development (Without Docker)

### Backend Setup

1. **Install Python dependencies using `uv`:**

```bash
# From project root
uv sync
```

2. **Configure environment variables:**

Create a `.env` file in the project root (see `.env.template` for reference).

3. **Run the backend:**

```bash
cd backend
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

### Frontend Setup

1. **Install Node.js dependencies:**

```bash
cd frontend
npm install
```

2. **Set environment variable:**

Ensure `NEXT_PUBLIC_BACKEND_URL=http://localhost:8000` is set (check `docker-compose.yml` or create `.env.local`).

3. **Run the development server:**

```bash
npm run dev
```

The frontend will be available at http://localhost:3000

### Hot Reload

Both services support hot-reload:
- **Backend**: FastAPI automatically reloads on Python file changes
- **Frontend**: Next.js fast refresh on React component changes

## 🧪 Testing Guide

### Test Credentials

See `TEST_CREDENTIALS.md` for pre-configured test accounts, or create new ones following the flows below.

### End-to-End Test Flow

#### 1. Register as Employer

1. Navigate to http://localhost:3000/register
2. Select **"Employer"** role → Click **"Continue"**
3. Fill in the form:
   - **Company Name**: Tech Innovations Inc
   - **First Name**: Jane
   - **Last Name**: Smith
   - **Email**: jane@techinnovations.com
   - **Password**: password123
   - **Confirm Password**: password123
   - **Address**: 456 Innovation Dr, San Francisco, CA, 94105
   - **Phone**: +14155551234
   - **Benefits**: Health insurance, 401k, Remote work options
4. Click **"Create Account"**
5. You'll be redirected to login

#### 2. Post a Job (as Employer)

1. Login with employer credentials
2. Navigate to **"Post New Job"** or click **"+ Post New Job"**
3. Fill in job details:
   - **Title**: Senior Software Engineer
   - **Description**: We're looking for an experienced developer...
   - **Department**: Engineering
   - **Hiring Manager**: Jane Smith
   - **Employment Type**: Full-time
   - **Salary Range**: $120,000 - $180,000 (Yearly)
   - **Education**: BS
   - **Field of Study**: Computer Science
   - **Skills**: Python, FastAPI, MongoDB, React
4. Click **"Post Job"**
5. View the job in **"My Jobs"**

#### 3. Register as Job Seeker

1. Navigate to http://localhost:3000/register
2. Select **"Job Seeker"** role → Click **"Continue"**
3. Fill in the form:
   - **First Name**: John
   - **Last Name**: Doe
   - **Email**: john.doe@example.com
   - **Password**: password123
   - **Confirm Password**: password123
   - **Address**: 123 Main St, New York, NY, 10001
   - **Phone**: +12025550123
   - **Education Level**: BS
   - **Field of Study**: Computer Science
   - **Skills**: Python, React, MongoDB
4. Click **"Create Account"**

#### 4. Search and Apply for Jobs (as Seeker)

1. Login with seeker credentials
2. Navigate to **"Search Jobs"**
3. Use filters:
   - Search by **title**: "Senior Software"
   - Search by **company**: "Tech Innovations"
   - Search by **skill**: "Python"
4. Click on the job posting
5. Click **"Apply Now"**
6. Confirm application
7. Navigate to **"My Applications"** to see status

#### 5. Review Applications (as Employer)

1. Logout and login as employer
2. Navigate to **"Applications"**
3. View John Doe's application
4. See applicant details, skills match, and application date

### Feature Testing Checklist

- [ ] User can register as job seeker
- [ ] User can register as employer
- [ ] User can login with correct credentials
- [ ] Login fails with incorrect credentials
- [ ] Job seeker can search jobs by title
- [ ] Job seeker can filter by company
- [ ] Job seeker can filter by skill
- [ ] Job seeker can apply for jobs
- [ ] Job seeker can view application history
- [ ] Employer can create job postings
- [ ] Employer can edit job postings
- [ ] Employer can delete job postings
- [ ] Employer can view received applications
- [ ] Dashboard shows correct statistics
- [ ] Logout works correctly
- [ ] Protected routes redirect to login

## 🐛 Troubleshooting

### Port Conflicts

**Problem**: Wrong application loads at http://localhost:3000 (e.g., different Next.js project)

**Solution**:
```bash
# Option 1: Use the start script (automatically handles this)
./start.sh

# Option 2: Manually kill processes
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
docker-compose up --build
```

See `PORT_CONFLICT_SOLVED.md` for detailed explanation.

### Docker Issues

**Container won't start:**
```bash
# Check container logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild from scratch
docker-compose down -v --remove-orphans
docker-compose up --build
```

**"Cannot find module" errors:**
```bash
# Rebuild frontend with clean install
docker-compose down
docker-compose build --no-cache frontend
docker-compose up
```

### Frontend Issues

**"Cannot connect to backend" or Network Errors:**

1. Verify backend is running:
   ```bash
   curl http://localhost:8000/health
   ```
2. Check `NEXT_PUBLIC_BACKEND_URL` in `docker-compose.yml`:
   ```yaml
   environment:
     - NEXT_PUBLIC_BACKEND_URL=http://localhost:8000  # For local
     # - NEXT_PUBLIC_BACKEND_URL=http://backend:8000  # For Docker network
   ```
3. Verify CORS settings in `backend/main.py`
4. See `API_CLIENT_FIX.md` for API client troubleshooting

**Hot reload not working:**
- Ensure volume mounts are correct in `docker-compose.yml`
- Try restarting the container: `docker-compose restart frontend`
- Clear Next.js cache: `rm -rf frontend/.next`

**Build errors:**
```bash
# Clear node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Backend Issues

**Import errors:**
```bash
# Sync dependencies with uv
uv sync

# If still failing, clear lock and reinstall
rm uv.lock
uv sync
```

**Database connection errors:**
1. Check `.env` file has correct MongoDB credentials:
   ```
   MONGO_DB_USER=your_user
   MONGO_DB_PASSWORD=your_password
   MONGO_DB_URL=mongodb+srv://...
   MONGO_DB_NAME=job-portal
   ```
2. Test connection: http://localhost:8000/db-status
3. Verify IP whitelist in MongoDB Atlas (allow 0.0.0.0/0 for development)
4. Check network connectivity: `ping cluster0.mongodb.net`

**Authentication/JWT errors:**
- Tokens are stored in browser localStorage
- Clear localStorage and re-login
- Check token expiration in `backend/core/security.py`

### Common Error Messages

| Error | Likely Cause | Solution |
|-------|--------------|----------|
| `EADDRINUSE: port 3000` | Port conflict | Use `./start.sh` or kill process |
| `Cannot reach backend` | Backend not running | Check http://localhost:8000/health |
| `401 Unauthorized` | Invalid/expired token | Logout and login again |
| `CORS error` | CORS misconfiguration | Check `backend/main.py` CORS settings |
| `Module not found` | Missing dependencies | Run `npm install` or `uv sync` |
| `MongoDB connection failed` | DB credentials/network | Check `.env` and MongoDB Atlas |

## 📦 Project Structure

```
Greenfield-project/
├── backend/                    # FastAPI Backend
│   ├── api/
│   │   └── v1/
│   │       └── routes/         # API route handlers
│   │           ├── auth_router.py       # Authentication endpoints
│   │           ├── seeker_router.py     # Job seeker endpoints
│   │           └── employer_router.py   # Employer endpoints
│   ├── core/
│   │   └── security.py         # JWT, password hashing
│   ├── db/
│   │   ├── settings.py         # MongoDB connection
│   │   ├── seeker_db_ops.py    # Seeker CRUD operations
│   │   └── employer_db_ops.py  # Employer CRUD operations
│   ├── schemas/                # Pydantic models
│   │   ├── seeker.py
│   │   └── employer.py
│   ├── services/               # Business logic
│   │   ├── seeker_services.py
│   │   └── employer_services.py
│   ├── utils/                  # Helper functions
│   │   ├── validators.py
│   │   └── gics_helper.py
│   ├── main.py                 # FastAPI app entry point
│   └── Dockerfile
├── frontend/                   # Next.js Frontend
│   ├── app/                    # App Router pages
│   │   ├── page.tsx            # Landing page
│   │   ├── login/
│   │   ├── register/
│   │   ├── seeker/
│   │   │   ├── dashboard/
│   │   │   ├── jobs/
│   │   │   ├── applications/
│   │   │   └── profile/
│   │   └── employer/
│   │       ├── dashboard/
│   │       ├── jobs/
│   │       └── applications/
│   ├── services/               # API service layer
│   │   ├── auth-service.ts
│   │   ├── seeker-service.ts
│   │   └── employer-service.ts
│   ├── store/
│   │   └── auth-store.ts       # Zustand auth state
│   ├── lib/
│   │   └── api-client.ts       # HTTP client with auth
│   ├── types/
│   │   └── index.ts            # TypeScript interfaces
│   ├── styles/
│   │   └── globals.css         # Tailwind CSS
│   ├── package.json
│   └── Dockerfile
├── docs/                       # Documentation
│   ├── 01-prd.md               # Product requirements
│   ├── 02-project-structure.md
│   ├── 03-implementation-plan.md
│   ├── backend_guidelines.txt
│   └── frontend_guidelines.txt
├── docker-compose.yml          # Docker orchestration
├── pyproject.toml              # Python dependencies (uv)
├── start.sh                    # Quick start script
├── QUICKSTART.md               # Quick start guide
├── README_FRONTEND.md          # This file
└── TEST_CREDENTIALS.md         # Test account credentials
```

## 🔐 Environment Variables

### Backend Configuration

Create a `.env` file in the project root (see `.env.template`):

```bash
# MongoDB Connection
MONGO_DB_USER=your_username
MONGO_DB_PASSWORD=your_password
MONGO_DB_URL=mongodb+srv://${MONGO_DB_USER}:${MONGO_DB_PASSWORD}@cluster.mongodb.net/?appName=job-portal
MONGO_DB_NAME=job-portal

# JWT Security
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000
FRONTEND_URL=http://localhost:3000

# AWS (if using Bedrock for AI features)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1

# OpenAI (if using ChatGPT)
OPENAI_API_KEY=your_key
```

### Frontend Configuration

Set in `docker-compose.yml` or create `.env.local`:

```bash
# For Docker (container-to-container communication)
NEXT_PUBLIC_BACKEND_URL=http://backend:8000

# For Local Development (host-to-host communication)
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

## 📝 Technical Notes

### Authentication & Security
- **JWT Tokens**: Used for authentication, stored in browser `localStorage`
- **Password Hashing**: bcrypt with salt rounds
- **Token Expiration**: Configurable (default 30 minutes)
- **CORS**: Configured for `localhost:3000` in development

### Database
- **MongoDB**: Document-based storage with Beanie ODM
- **Collections**: `seekers`, `employers`, `jobs`, `applications`
- **Indexes**: Email (unique), skills, job titles for fast queries

### API Design
- **REST Architecture**: Standard HTTP methods (GET, POST, PUT, DELETE)
- **Response Format**: JSON with consistent structure
- **Error Handling**: Proper HTTP status codes (400, 401, 404, 500)
- **Validation**: Pydantic models for request/response validation

### Frontend Architecture
- **App Router**: Next.js 14 file-based routing
- **State Management**: Zustand for global auth state
- **Styling**: Tailwind CSS utility classes
- **Icons**: lucide-react icon library
- **Forms**: Controlled components with validation

### Development Features
- **Hot Reload**: Both backend and frontend support live reloading
- **Type Safety**: TypeScript in frontend, Pydantic in backend
- **Logging**: Console logs visible with `docker-compose logs -f`
- **API Documentation**: Auto-generated Swagger UI at `/docs`

## 🚀 Deployment Considerations

### Production Checklist
- [ ] Update `JWT_SECRET_KEY` to strong random value
- [ ] Set `CORS_ORIGINS` to production domain
- [ ] Configure MongoDB IP whitelist for production servers
- [ ] Enable HTTPS/SSL certificates
- [ ] Set appropriate token expiration times
- [ ] Configure environment-specific `NEXT_PUBLIC_BACKEND_URL`
- [ ] Enable production logging and monitoring
- [ ] Set up database backups
- [ ] Configure rate limiting for API endpoints

## 📚 Resources & Documentation

### Official Documentation
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [Next.js](https://nextjs.org/docs) - Frontend framework
- [Tailwind CSS](https://tailwindcss.com/docs) - Styling
- [MongoDB with Beanie](https://beanie-odm.dev/) - ODM
- [Zustand](https://github.com/pmndrs/zustand) - State management

### Project Documentation
- `QUICKSTART.md` - Quick start guide for new users
- `TEST_CREDENTIALS.md` - Test account credentials
- `API_CLIENT_FIX.md` - API client troubleshooting
- `PORT_CONFLICT_SOLVED.md` - Port conflict resolution
- `IMPLEMENTATION_SUMMARY.md` - Implementation details
- `docs/backend_guidelines.txt` - Backend coding standards
- `docs/frontend_guidelines.txt` - Frontend coding standards

## 🤝 Contributing

### Development Workflow
1. Create a feature branch from `main`
2. Make changes following project guidelines
3. Test locally with Docker
4. Run linters: `uv run ruff check` (backend), `npm run lint` (frontend)
5. Commit with descriptive messages
6. Push and create pull request

### Code Standards
- **Backend**: Follow PEP 8, use type hints, add docstrings
- **Frontend**: Follow TypeScript best practices, use functional components
- **Commits**: Use conventional commits (feat, fix, docs, etc.)
- **Testing**: Add tests for new features (future implementation)

---

**Questions?** Check the documentation files or contact the development team.

**Happy Coding! 🚀**

