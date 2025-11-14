# ChromaDB Ingestion Scripts

This directory contains scripts for ingesting data into ChromaDB collections for the Job Portal application.

## Overview

Two ingestion scripts are provided:
- `ingest_seeker.py` - Ingests job seeker resume and skills data
- `ingest_employer.py` - Ingests employer job descriptions and desired skills data

## Collections

### Seeker Collections
1. **Seeker_Resume_Collection** - Stores resume text with Post_Date metadata
2. **Seeker_Skills_Collection** - Stores concatenated skills, education level, and focus area

### Employer Collections
1. **Employer_JobDescr_Collection** - Stores job descriptions with title, post date, and employer UUID
2. **Employer_Skillswish_Collection** - Stores desired skills, education requirements, and focus area

## Running from Docker Compose

### Test Data Ingestion

To ingest test data from JSON files in `chroma_data/` directories:

```bash
# Ingest seeker test data
docker compose exec backend uv run python backend/db/ingestion/ingest_seeker.py --test-data

# Ingest employer test data
docker compose exec backend uv run python backend/db/ingestion/ingest_employer.py --test-data
```

### Production Mode (Single Record)

#### Ingest Seeker Data

```bash
docker compose exec backend uv run python backend/db/ingestion/ingest_seeker.py \
  --seeker-id "550e8400-e29b-41d4-a716-446655440001" \
  --resume "Full resume text here..." \
  --education-level "MS" \
  --edu-focus "Computer Science" \
  --skills "Python" "FastAPI" "Docker" "AWS"
```

#### Ingest Employer Job Posting

```bash
docker compose exec backend uv run python backend/db/ingestion/ingest_employer.py \
  --job-id "660e8400-e29b-41d4-a716-446655440101" \
  --employer-id "770e8400-e29b-41d4-a716-446655440201" \
  --title "Senior Backend Engineer" \
  --description "Full job description here..." \
  --education-level "BS" \
  --edu-focus "Computer Science" \
  --skills "Python" "FastAPI" "Docker" "Kubernetes"
```

## Running Locally (Without Docker)

### Test Data Ingestion

```bash
# From project root
uv run python backend/db/ingestion/ingest_seeker.py --test-data
uv run python backend/db/ingestion/ingest_employer.py --test-data
```

### Production Mode

```bash
# Seeker data
uv run python backend/db/ingestion/ingest_seeker.py \
  --seeker-id "UUID" \
  --resume "Resume text..." \
  --education-level "MS" \
  --edu-focus "Computer Science" \
  --skills "Python" "FastAPI"

# Employer data
uv run python backend/db/ingestion/ingest_employer.py \
  --job-id "UUID" \
  --employer-id "UUID" \
  --title "Job Title" \
  --description "Job description..." \
  --education-level "BS" \
  --edu-focus "Computer Science" \
  --skills "Python" "FastAPI"
```

## Test Data Format

### Seeker Resume Test Data

Create JSON files in `backend/db/chroma_data/seeker/`:

**test_seeker_resume_N.json:**
```json
{
  "seeker_identification": "550e8400-e29b-41d4-a716-446655440001",
  "resume": "Full resume text...",
  "created_at": "2024-11-10T10:30:00-07:00"
}
```

**test_seeker_skills_N.json:**
```json
{
  "seeker_identification": "550e8400-e29b-41d4-a716-446655440001",
  "education_level": "MS",
  "edu_focus": "Computer Science",
  "key_skills": ["Python", "FastAPI", "Docker", "AWS"]
}
```

### Employer Job Test Data

Create JSON files in `backend/db/chroma_data/employer/`:

**test_employer_job_N.json:**
```json
{
  "job_identification": "660e8400-e29b-41d4-a716-446655440101",
  "employer_identification": "770e8400-e29b-41d4-a716-446655440201",
  "job_title": "Senior Backend Engineer",
  "job_description": "Full job description...",
  "posted_date": "2024-11-12T09:00:00-07:00"
}
```

**test_employer_skills_N.json:**
```json
{
  "job_identification": "660e8400-e29b-41d4-a716-446655440101",
  "employer_identification": "770e8400-e29b-41d4-a716-446655440201",
  "education_level": "BS",
  "edu_focus": "Computer Science",
  "key_skills": ["Python", "FastAPI", "Docker", "Kubernetes"]
}
```

## Integration with Application

These scripts are designed to be called programmatically when:

### For Seekers
- A job seeker first uploads their resume
- A seeker updates their profile or skills

The `backend/services/seeker_services.py` module already has integration with ChromaDB writes in:
- `create_new_seeker()` - Writes resume and skills on account creation
- `update_seeker_profile()` - Updates resume and skills in ChromaDB
- `upload_resume()` - Updates resume in ChromaDB

### For Employers
- An employer creates a new job posting
- A job posting is updated

The `backend/services/employer_services.py` module already has integration with ChromaDB writes in:
- `create_job()` - Writes job description and skills on job creation
- `modify_job()` - Updates job description and skills in ChromaDB

## Troubleshooting

### Path Issues in Docker

The scripts automatically detect if running in Docker and adjust paths accordingly:
- Local: `./backend/db/chroma_data/`
- Docker: `/app/backend/db/chroma_data/`

### OpenAI API Key

Ensure the `OPENAI_API_KEY` environment variable is set in your `.env` file for text embeddings.

### ChromaDB Location

The ChromaDB database is stored at:
- Local: `./chroma_db` (project root)
- Docker: `/app/chroma_db` (mounted volume)

## Script Output

Both scripts provide detailed logging:
- DEBUG level: Individual operations and file loading
- INFO level: Summary of operations
- ERROR level: Failures and errors
- Exit code: 0 for success, 1 for any failures

Example output:
```
============================================================
Seeker Data Ingestion Script
============================================================
Running in TEST DATA mode
Loading test data from: /app/backend/db/chroma_data/seeker
Found 2 test record(s)

Processing seeker: 550e8400-e29b-41d4-a716-446655440001
Successfully ingested resume for seeker 550e8400-e29b-41d4-a716-446655440001
Successfully ingested skills for seeker 550e8400-e29b-41d4-a716-446655440001

============================================================
Ingestion Summary
============================================================
Successful operations: 4
Failed operations: 0
============================================================
```

## Notes

- Maximum of 15 skills can be stored per seeker/job posting
- UUIDs are used for identification in ChromaDB (not MongoDB ObjectIds)
- Embeddings use OpenAI's `text-embedding-3-small` model
- All timestamps use America/Denver timezone
- Scripts preserve existing ChromaDB operations in services modules

