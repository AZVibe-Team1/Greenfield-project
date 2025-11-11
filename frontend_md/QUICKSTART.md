# 🚀 Job Portal - Quick Start Guide

## Prerequisites
- Docker Desktop installed and running
- Git (optional, if cloning)

## Step 1: Start the Application

### Method 1: Using the Start Script (Recommended)

Open terminal in the project root and run:

```bash
./start.sh
```

This script will automatically:
- Stop any process using port 3000
- Start the Job Portal with docker-compose

### Method 2: Manual Start

If you prefer to start manually:

```bash
# First, stop any process on port 3000
lsof -ti:3000 | xargs kill -9

# Then start docker-compose
docker-compose up --build
```

This command will:
1. Build the backend (FastAPI) container
2. Build the frontend (Next.js) container
3. Start both services with hot-reload enabled

**Wait for the following messages:**
```
jobportal-backend   | ✅ Application startup complete
jobportal-frontend  | ▲ Next.js 14.1.0
jobportal-frontend  | - Local:        http://localhost:3000
```

## Step 2: Access the Application

Open your browser and navigate to:

### Frontend
**URL:** http://localhost:3000

You should see the Job Portal landing page with:
- "Find Your Dream Job Today" hero section
- Login and Register buttons
- Feature cards

### Backend API
**URL:** http://localhost:8000
**API Docs:** http://localhost:8000/docs (Interactive Swagger UI)

## Step 3: Test the Application

### Option A: Register as Job Seeker

1. Click **"Register"** or visit http://localhost:3000/register
2. Select **"Job Seeker"** role
3. Click **"Continue"**
4. Fill in the registration form:
   - First Name: John
   - Last Name: Doe
   - Email: john.doe@example.com
   - Phone: +12025550123
   - Password: password123
   - Confirm Password: password123
   - Address: 123 Main St, New York, NY, 10001
   - Education Level: BS
   - Field of Study: Computer Science
   - Skills: Python, JavaScript, React
5. Click **"Create Account"**
6. You'll be redirected to login page

### Option B: Register as Employer

1. Visit http://localhost:3000/register
2. Select **"Employer"** role
3. Click **"Continue"**
4. Fill in the form:
   - Company Name: Tech Innovations Inc
   - Contact First Name: Jane
   - Contact Last Name: Smith
   - Email: jane@techinnovations.com
   - Password: password123
   - Confirm Password: password123
   - Address: 456 Innovation Dr, San Francisco, CA, 94105
   - Benefits: Health insurance, 401k, Remote work
5. Click **"Create Account"**

## Step 4: Login and Explore

### Job Seeker Flow
1. Login with your seeker credentials
2. You'll see the **Seeker Dashboard**
3. Click **"Search Jobs"** to browse available positions
4. Use filters to search by title, company, or skill
5. Click **"Apply Now"** on any job
6. View your applications in **"My Applications"**

### Employer Flow
1. Login with your employer credentials
2. You'll see the **Employer Dashboard**
3. Click **"+ Post New Job"**
4. Fill in the job details:
   - Job Title: Senior Software Engineer
   - Description: Build scalable systems...
   - Department: Engineering
   - Hiring Manager: Jane Smith
   - Salary: 120000 - 180000 Yearly
   - Education: BS
   - Field: Computer Science
   - Skills: Python, FastAPI, MongoDB
5. Click **"Post Job"**
6. View your jobs in **"My Jobs"**
7. Check applications in **"Applications"**

## Step 5: Stop the Application

In the terminal where docker-compose is running, press:

```bash
Ctrl + C
```

Then stop and remove containers:

```bash
docker-compose down
```

## 🐛 Troubleshooting

### "Wrong application loads" or "Port already in use" error

**Problem:** When visiting http://localhost:3000, you see a different project (e.g., agentic customer service).

**Solution:**
```bash
# Option 1: Use the start script (automatically handles this)
./start.sh

# Option 2: Manually stop processes on port 3000
lsof -ti:3000 | xargs kill -9

# Then start Job Portal
docker-compose up --build
```

**Why this happens:** Multiple Next.js projects can't run on the same port. The start script automatically stops any conflicting processes.

### "Port already in use" error (Backend)
```bash
# Kill processes on port 8000
lsof -ti:8000 | xargs kill -9

# Then restart
docker-compose up --build
```

### "Cannot connect to backend" error
1. Check that backend is running: http://localhost:8000
2. Verify backend health: http://localhost:8000/health
3. Check logs: `docker-compose logs backend`

### Frontend not loading
1. Clear browser cache
2. Check logs: `docker-compose logs frontend`
3. Verify frontend is running: `docker ps`

### Database connection errors
1. Check your `.env` file has correct MongoDB credentials
2. Verify MongoDB Atlas allows connections from your IP
3. Test connection: http://localhost:8000/db-status

## 📚 What's Included

### Backend Features
- ✅ User authentication (JWT)
- ✅ Job seeker registration & profile
- ✅ Employer registration & profile
- ✅ Job posting management
- ✅ Job application system
- ✅ Job search with filters

### Frontend Features
- ✅ Modern, responsive UI
- ✅ Role-based dashboards
- ✅ Job search and filtering
- ✅ Application tracking
- ✅ Profile management
- ✅ Job posting management

## 🔗 Useful URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Main application |
| Backend | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Health Check | http://localhost:8000/health | Backend status |
| DB Status | http://localhost:8000/db-status | MongoDB connection |

## 📖 More Information

- Full setup guide: `README_FRONTEND.md`
- Implementation details: `IMPLEMENTATION_SUMMARY.md`
- Backend guidelines: `docs/backend_guidelines.txt`
- Frontend guidelines: `docs/frontend_guidelines.txt`

## 🎯 Sample Test Scenario

**Complete End-to-End Test:**

1. **Register Employer**
   - Company: "Tech Corp"
   - Email: tech@example.com
   - Password: test123

2. **Login as Employer**
   - Post a job: "Full Stack Developer"
   - Set salary: $80k-$120k
   - Add skills: Python, React, MongoDB

3. **Register Job Seeker**
   - Name: John Doe
   - Email: john@example.com
   - Password: test123
   - Skills: Python, React

4. **Login as Job Seeker**
   - Search for "Full Stack"
   - Apply to the job
   - View application status

5. **Login as Employer**
   - View received applications
   - See John Doe's application

✅ **Success!** The application is working end-to-end!

---

**Need Help?** Check `README_FRONTEND.md` for detailed documentation.

**Happy Testing! 🎉**

