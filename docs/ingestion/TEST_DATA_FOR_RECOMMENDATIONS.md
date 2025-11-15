# Test Data for AI Recommendations Feature

## Overview

Created comprehensive test data for demonstrating the AI-powered job recommendations feature for the test seeker: **john.jobseeker@test.com**

## Test Seeker Profile

**Name:** John Jobseeker  
**Email:** john.jobseeker@test.com  
**Password:** SecurePass123!  
**Location:** San Francisco, CA 94102  
**Education:** BS in Computer Science  
**Skills:** Python, JavaScript, HTML, CSS, Git, SQL, REST APIs, Web Development  
**Salary Range:** $70,000 - $110,000 Yearly

## Created Test Jobs

I created 6 new job postings specifically tailored to match the test seeker's profile:

### 1. Junior Software Engineer (Excellent Match - 85-95%)
- **Company:** CodeCraft Innovations
- **Location:** San Francisco, CA
- **Salary:** $75,000 - $105,000
- **Education:** BS in Computer Science (Perfect match!)
- **Skills:** JavaScript, Python, Git, Web Development, REST APIs, SQL
- **Why it matches:** Entry-level position, perfect education match, skills align well, same city

### 2. Frontend Developer - Entry Level (Good Match - 75-85%)
- **Company:** PixelPerfect Design Co
- **Location:** San Francisco, CA
- **Salary:** $80,000 - $110,000
- **Education:** BS in Computer Science
- **Skills:** React, JavaScript, TypeScript, HTML, CSS, Git
- **Why it matches:** Entry-level, strong frontend focus matches seeker's HTML/CSS/JS skills

### 3. Full Stack Developer (Good Match - 70-80%)
- **Company:** DataFlow Systems
- **Location:** San Francisco, CA
- **Salary:** $95,000 - $140,000
- **Education:** BS in Computer Science
- **Skills:** Python, JavaScript, React, FastAPI, PostgreSQL, MongoDB
- **Why it matches:** Requires both Python and JavaScript which seeker knows

### 4. Python Developer - Backend Focus (Good Match - 75-85%)
- **Company:** FinTech Solutions Inc
- **Location:** San Francisco, CA
- **Salary:** $85,000 - $120,000
- **Education:** BS in Computer Science
- **Skills:** Python, FastAPI, Django, PostgreSQL, REST APIs
- **Why it matches:** Python-focused, matches seeker's Python skills and CS degree

### 5. Junior DevOps Engineer (Moderate Match - 60-70%)
- **Company:** CloudNative Technologies
- **Location:** San Francisco, CA
- **Salary:** $75,000 - $105,000
- **Education:** BS in Computer Science
- **Skills:** Linux, Python, Bash, AWS, Docker, CI/CD
- **Why it matches:** Python skills match, CS degree matches, but DevOps is somewhat different focus

### 6. Software QA Engineer - Automation (Moderate Match - 65-75%)
- **Company:** QualityFirst Software
- **Location:** San Francisco, CA
- **Salary:** $70,000 - $100,000
- **Education:** BS in Computer Science
- **Skills:** Python, Selenium, API Testing, Test Automation
- **Why it matches:** Python skills, CS degree, but QA role is different career path

## Files Created

### ChromaDB Data (for vector embeddings)
Located in `backend/db/chroma_data/`:

#### Employer Jobs:
- `employer/test_employer_job_3_junior_swe.json`
- `employer/test_employer_job_4_frontend.json`
- `employer/test_employer_job_5_fullstack.json`
- `employer/test_employer_job_6_python.json`
- `employer/test_employer_job_7_devops.json`
- `employer/test_employer_job_8_qa.json`

#### Seeker Resume:
- `seeker/test_seeker_john_resume.json`

### MongoDB Data (for full document storage)
Located in `backend/db/mongo_data/`:

#### Employers:
- `employer/test_employer_3_startup.json` (CodeCraft Innovations)
- `employer/test_employer_4_frontend_startup.json` (PixelPerfect Design Co)
- `employer/test_employer_5_saas.json` (DataFlow Systems)
- `employer/test_employer_6_fintech.json` (FinTech Solutions Inc)
- `employer/test_employer_7_cloud.json` (CloudNative Technologies)
- `employer/test_employer_8_qa_company.json` (QualityFirst Software)

#### Seeker:
- `seeker/test_seeker_john.json`

## How to Ingest the Data

### Step 1: Ingest to MongoDB

```bash
# Using Docker (recommended):
docker compose run backend uv run python backend/db/ingestion/ingest_mongo_employer.py
docker compose run backend uv run python backend/db/ingestion/ingest_mongo_seeker.py

# Or locally:
cd backend/db/ingestion
uv run python ingest_mongo_employer.py
uv run python ingest_mongo_seeker.py
```

This will load all employer and seeker profiles into MongoDB.

**Note:** All employer JSON files have been updated with required fields:
- `employer_identification` (UUID) at employer level
- `job_identification` (UUID) for each job
- `employer_identification` (UUID) for each job
- `posted_date` (datetime) for each job

### Step 2: Ingest to ChromaDB

```bash
# Still in backend/db/ingestion directory
uv run ingest_to_chroma.py
```

This will create vector embeddings for all job descriptions and seeker resumes in ChromaDB.

### Step 3: Verify Ingestion

Check the logs to ensure all data was loaded successfully:
- MongoDB: Check for "Successfully inserted" messages
- ChromaDB: Check for embedding generation messages

## Testing the Recommendations

1. **Start the application:**
   ```bash
   docker compose up --build
   ```

2. **Login as the test seeker:**
   - Navigate to http://localhost:3000/login
   - Email: john.jobseeker@test.com
   - Password: SecurePass123!

3. **View AI Recommendations:**
   - Click on "AI Recommendations" in the navigation
   - Or navigate to http://localhost:3000/seeker/recommendations

4. **Expected Results:**
   - You should see 6 job recommendations
   - Jobs should be sorted by match score (highest first)
   - Junior Software Engineer should have the highest match (85-95%)
   - Each job should show:
     - Match percentage
     - Score breakdown (Skills, Education, Pay, Experience)
     - Company name and location
     - Salary range
     - Required skills
     - AI reasoning for the match

5. **Test Auto-Apply Feature:**
   - Navigate to Profile page
   - Scroll to "AI Auto-Apply Settings"
   - Enable auto-apply
   - Set threshold (e.g., 80%)
   - Future jobs above threshold will auto-apply (when background job is implemented)

## Key Match Factors

The AI scoring algorithm considers:
- **Skills Match (40% weight):** Python, JavaScript, HTML, CSS overlap
- **Education Match (20% weight):** BS in Computer Science requirement
- **Pay Range Match (20% weight):** $70k-$110k seeker range vs job offers
- **Experience Match (20% weight):** Entry-level suitable for recent grad

## Notes

- All jobs are located in San Francisco to maximize location match
- All jobs require BS in Computer Science to ensure education match
- Salary ranges overlap with seeker's expectations ($70k-$110k)
- Skills requirements vary to demonstrate different match scores
- Companies are realistic SF Bay Area tech companies
- Job descriptions are detailed and professional

## UUID Mappings

For reference, here are the UUID mappings:

### Seeker:
- John Jobseeker: `550e8400-e29b-41d4-a716-446655440999`

### Jobs:
- Junior Software Engineer: `660e8400-e29b-41d4-a716-446655440103`
- Frontend Developer: `660e8400-e29b-41d4-a716-446655440104`
- Full Stack Developer: `660e8400-e29b-41d4-a716-446655440105`
- Python Developer: `660e8400-e29b-41d4-a716-446655440106`
- Junior DevOps Engineer: `660e8400-e29b-41d4-a716-446655440107`
- Software QA Engineer: `660e8400-e29b-41d4-a716-446655440108`

### Employers:
- CodeCraft Innovations: `770e8400-e29b-41d4-a716-446655440203`
- PixelPerfect Design Co: `770e8400-e29b-41d4-a716-446655440204`
- DataFlow Systems: `770e8400-e29b-41d4-a716-446655440205`
- FinTech Solutions Inc: `770e8400-e29b-41d4-a716-446655440206`
- CloudNative Technologies: `770e8400-e29b-41d4-a716-446655440207`
- QualityFirst Software: `770e8400-e29b-41d4-a716-446655440208`

## Troubleshooting

If recommendations don't show up:
1. Verify MongoDB has the data: Check `job-portal` database
2. Verify ChromaDB has embeddings: Check `./chroma_db` directory
3. Check backend logs for errors in matching service
4. Ensure OpenAI API key is set for embeddings
5. Verify seeker is logged in and authenticated

## Next Steps

After ingestion:
1. Test the recommendations page
2. Try applying to jobs
3. Test the auto-apply settings
4. Verify match scores make sense
5. Check score breakdowns and AI reasoning

