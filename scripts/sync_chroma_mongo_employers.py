#!/usr/bin/env python3
"""
Sync MongoDB Employers and Job Postings to ChromaDB

This script ensures that all employers and their job postings in MongoDB
are also ingested into ChromaDB for AI-powered matching.

It processes:
- All employers in MongoDB
- All open_jobs for each employer
- Ingests job descriptions into Employer_JobDescr_Collection
- Ingests skills into Employer_Skillswish_Collection
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger
from backend.db.settings import (
    connect_to_mongodb,
    close_mongodb_connection,
    Employer_JobDescr_collection,
    Employer_Skillswish_collection,
)
from backend.db.employer_db_ops import EmployerCRUD
from backend.db.chroma_crud_ops import write_collection

# Add stdout handler for script output visibility
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    colorize=True
)


def check_job_in_chromadb(job_identification: str) -> tuple[bool, bool]:
    """
    Check if a job exists in ChromaDB collections.
    
    Args:
        job_identification: UUID string of the job
        
    Returns:
        Tuple of (exists_in_descr, exists_in_skills)
    """
    try:
        # Check in job description collection
        descr_results = Employer_JobDescr_collection.get(ids=[job_identification])
        exists_descr = len(descr_results["ids"]) > 0
        
        # Check in skills collection
        skills_results = Employer_Skillswish_collection.get(ids=[job_identification])
        exists_skills = len(skills_results["ids"]) > 0
        
        return (exists_descr, exists_skills)
    except Exception as e:
        logger.warning(f"Error checking job {job_identification} in ChromaDB: {e}")
        return (False, False)


def ingest_job_description(
    job_identification: str,
    employer_identification: str,
    job_title: str,
    job_description: str,
    posted_date: datetime | str | None = None
) -> int:
    """
    Ingest a job description into ChromaDB.
    
    Args:
        job_identification: Unique UUID identifier for the job posting
        employer_identification: Unique UUID identifier for the employer
        job_title: Title of the job posting
        job_description: Full job description text
        posted_date: ISO format timestamp or datetime (optional, defaults to now)
        
    Returns:
        1 if successful, -1 if failed
    """
    try:
        # Prepare metadata
        if posted_date:
            if isinstance(posted_date, datetime):
                post_date = str(posted_date)
            else:
                post_date = posted_date
        else:
            post_date = str(datetime.now(ZoneInfo("America/Denver")))
            
        metadata = {
            "Title": job_title,
            "Post_Date": post_date,
            "Employer_UUID": str(employer_identification)
        }
        
        # Write to ChromaDB
        result = write_collection(
            collection=Employer_JobDescr_collection,
            collection_name="Employer_JobDescr_Collection",
            id_value=str(job_identification),
            text_value=job_description,
            metadata=metadata
        )
        
        if result == 1:
            logger.info(f"Successfully ingested job description for job {job_identification}")
        return result
        
    except Exception as e:
        logger.error(f"Failed to ingest job description for job {job_identification}: {e}")
        return -1


def ingest_employer_skills(
    job_identification: str,
    education_level: str,
    edu_focus: str,
    key_skills: list[str]
) -> int:
    """
    Ingest employer's desired skills into ChromaDB.
    
    Args:
        job_identification: Unique UUID identifier for the job posting
        education_level: Required education level (BA, BS, MA, MS, MBA, PhD)
        edu_focus: Required field of study/focus
        key_skills: List of desired skills (up to 15)
        
    Returns:
        1 if successful, -1 if failed
    """
    try:
        # Concatenate education and skills
        skills_parts = []
        if key_skills:
            skills_parts.append(", ".join(key_skills[:15]))  # Max 15 skills
        if education_level:
            skills_parts.append(f"Education: {education_level}")
        if edu_focus:
            skills_parts.append(f"Focus: {edu_focus}")
        
        skills_text = ", ".join(skills_parts)
        
        # Prepare metadata
        metadata = {"Desired Skills": skills_text}
        
        # Write to ChromaDB
        result = write_collection(
            collection=Employer_Skillswish_collection,
            collection_name="Employer_Skillswish_Collection",
            id_value=str(job_identification),
            text_value=skills_text,
            metadata=metadata
        )
        
        if result == 1:
            logger.info(f"Successfully ingested skills for job {job_identification}")
        return result
        
    except Exception as e:
        logger.error(f"Failed to ingest skills for job {job_identification}: {e}")
        return -1


async def process_employer(employer, stats: dict) -> None:
    """
    Process a single employer and ingest all their jobs into ChromaDB.
    
    Args:
        employer: Employer document from MongoDB
        stats: Dictionary to track statistics
    """
    employer_name = employer.company_information.company_name
    employer_uuid = str(employer.employer_identification)
    
    logger.info(f"\n📋 Processing employer: {employer_name} (UUID: {employer_uuid})")
    logger.info(f"   Email: {employer.email}")
    logger.info(f"   Open jobs: {len(employer.open_jobs)}")
    
    stats["employers_processed"] += 1
    
    if not employer.open_jobs:
        logger.info(f"   ⚠️  No open jobs for this employer, skipping...")
        stats["employers_no_jobs"] += 1
        return
    
    # Process each job
    for job in employer.open_jobs:
        job_uuid = str(job.job_identification)
        job_title = job.job_title
        
        logger.info(f"\n   🔍 Processing job: {job_title} (UUID: {job_uuid})")
        
        # Check if already in ChromaDB
        exists_descr, exists_skills = check_job_in_chromadb(job_uuid)
        
        # Ingest job description
        if not exists_descr:
            if job.job_description:
                logger.info(f"      📝 Ingesting job description...")
                result = ingest_job_description(
                    job_identification=job_uuid,
                    employer_identification=employer_uuid,
                    job_title=job_title,
                    job_description=job.job_description,
                    posted_date=job.posted_date
                )
                if result == 1:
                    stats["jobs_descr_ingested"] += 1
                    logger.info(f"      ✅ Job description ingested successfully")
                else:
                    stats["jobs_descr_failed"] += 1
                    logger.error(f"      ❌ Failed to ingest job description")
            else:
                logger.warning(f"      ⚠️  Job has no description, skipping...")
                stats["jobs_no_description"] += 1
        else:
            logger.info(f"      ✅ Job description already exists in ChromaDB")
            stats["jobs_descr_existing"] += 1
        
        # Ingest skills
        if not exists_skills:
            has_skills_data = bool(job.key_skills) or bool(job.education_level) or bool(job.edu_focus)
            if has_skills_data:
                logger.info(f"      🎯 Ingesting skills...")
                result = ingest_employer_skills(
                    job_identification=job_uuid,
                    education_level=job.education_level or "",
                    edu_focus=job.edu_focus or "",
                    key_skills=job.key_skills or []
                )
                if result == 1:
                    stats["jobs_skills_ingested"] += 1
                    logger.info(f"      ✅ Skills ingested successfully")
                else:
                    stats["jobs_skills_failed"] += 1
                    logger.error(f"      ❌ Failed to ingest skills")
            else:
                logger.warning(f"      ⚠️  Job has no skills data, skipping...")
                stats["jobs_no_skills"] += 1
        else:
            logger.info(f"      ✅ Skills already exist in ChromaDB")
            stats["jobs_skills_existing"] += 1
        
        stats["jobs_processed"] += 1


async def main():
    """Main execution function."""
    logger.info("=" * 70)
    logger.info("MongoDB to ChromaDB Employer & Job Posting Sync")
    logger.info("=" * 70)
    
    # Initialize statistics
    stats = {
        "employers_processed": 0,
        "employers_no_jobs": 0,
        "jobs_processed": 0,
        "jobs_descr_ingested": 0,
        "jobs_descr_existing": 0,
        "jobs_descr_failed": 0,
        "jobs_no_description": 0,
        "jobs_skills_ingested": 0,
        "jobs_skills_existing": 0,
        "jobs_skills_failed": 0,
        "jobs_no_skills": 0,
    }
    
    try:
        # Connect to MongoDB
        logger.info("\n🔌 Connecting to MongoDB...")
        await connect_to_mongodb()
        logger.info("✅ Connected to MongoDB successfully")
        
        # Get all employers
        logger.info("\n📊 Fetching all employers from MongoDB...")
        employers = await EmployerCRUD.get_all_employers()
        total_employers = len(employers)
        logger.info(f"✅ Found {total_employers} employer(s) in MongoDB")
        
        if total_employers == 0:
            logger.warning("⚠️  No employers found in MongoDB. Nothing to sync.")
            return
        
        # Process each employer
        logger.info(f"\n🚀 Starting to process {total_employers} employer(s)...")
        logger.info("=" * 70)
        
        for i, employer in enumerate(employers, 1):
            logger.info(f"\n{'=' * 70}")
            logger.info(f"Employer {i}/{total_employers}")
            logger.info(f"{'=' * 70}")
            
            try:
                await process_employer(employer, stats)
            except Exception as e:
                logger.error(f"❌ Error processing employer {employer.company_information.company_name}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        # Print summary
        logger.info("\n" + "=" * 70)
        logger.info("📊 SYNC SUMMARY")
        logger.info("=" * 70)
        logger.info(f"Employers:")
        logger.info(f"  ✅ Processed: {stats['employers_processed']}")
        logger.info(f"  ⚠️  No jobs: {stats['employers_no_jobs']}")
        logger.info(f"\nJobs:")
        logger.info(f"  ✅ Total processed: {stats['jobs_processed']}")
        logger.info(f"\nJob Descriptions:")
        logger.info(f"  ✅ Ingested: {stats['jobs_descr_ingested']}")
        logger.info(f"  ✅ Already existed: {stats['jobs_descr_existing']}")
        logger.info(f"  ❌ Failed: {stats['jobs_descr_failed']}")
        logger.info(f"  ⚠️  No description: {stats['jobs_no_description']}")
        logger.info(f"\nSkills:")
        logger.info(f"  ✅ Ingested: {stats['jobs_skills_ingested']}")
        logger.info(f"  ✅ Already existed: {stats['jobs_skills_existing']}")
        logger.info(f"  ❌ Failed: {stats['jobs_skills_failed']}")
        logger.info(f"  ⚠️  No skills data: {stats['jobs_no_skills']}")
        logger.info("=" * 70)
        
        # Calculate success rate
        total_ingested = stats['jobs_descr_ingested'] + stats['jobs_skills_ingested']
        total_failed = stats['jobs_descr_failed'] + stats['jobs_skills_failed']
        total_operations = total_ingested + total_failed
        
        if total_operations > 0:
            success_rate = (total_ingested / total_operations) * 100
            logger.info(f"\n🎯 Success Rate: {success_rate:.1f}% ({total_ingested}/{total_operations})")
        
        logger.info("\n✅ Sync complete!")
        
    except Exception as e:
        logger.error(f"\n❌ Fatal error during sync: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
        
    finally:
        # Close MongoDB connection
        logger.info("\n🔌 Closing MongoDB connection...")
        await close_mongodb_connection()
        logger.info("✅ Connection closed")


if __name__ == "__main__":
    asyncio.run(main())

