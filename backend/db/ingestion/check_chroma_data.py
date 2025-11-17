"""
Quick diagnostic script to check what's in ChromaDB.
"""
import sys
sys.path.insert(0, '/app')

from backend.db.settings import (
    Seeker_Resume_collection,
    Employer_JobDescr_collection
)

print("=" * 60)
print("ChromaDB Data Check")
print("=" * 60)

# Check Seeker Resume collection
print("\n📋 Seeker Resume Collection:")
try:
    seeker_count = Seeker_Resume_collection.count()
    print(f"   Total seekers: {seeker_count}")
    
    if seeker_count > 0:
        # Get all seeker IDs
        result = Seeker_Resume_collection.get(include=["metadatas"])
        print(f"   Seeker IDs: {result['ids']}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Check Employer Job Description collection
print("\n💼 Employer Job Description Collection:")
try:
    job_count = Employer_JobDescr_collection.count()
    print(f"   Total jobs: {job_count}")
    
    if job_count > 0:
        # Get all job IDs
        result = Employer_JobDescr_collection.get(include=["metadatas"])
        print(f"   Job IDs: {result['ids'][:5]}...")  # Show first 5
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("Recommendation")
print("=" * 60)

if seeker_count == 0:
    print("\n⚠️  No seekers in ChromaDB!")
    print("   Run: docker compose run backend uv run python backend/db/ingestion/ingest_chroma_seeker.py")

if job_count == 0:
    print("\n⚠️  No jobs in ChromaDB!")
    print("   Run: docker compose run backend uv run python backend/db/ingestion/ingest_chroma_employer.py")

if seeker_count > 0 and job_count > 0:
    print("\n✅ ChromaDB has data!")
    print("   If recommendations still don't show, check backend logs for errors.")

print()

