#!/usr/bin/env python3
"""
Employer Job Description and Skills Ingestion Script for ChromaDB

This script ingests employer job descriptions and desired skills into ChromaDB collections.
It can run in two modes:
1. Test mode (--test-data flag): Loads test data from JSON files
2. Production mode: Accepts job posting data as arguments

Usage:
    # Test mode with JSON files
    python ingest_employer.py --test-data

    # Production mode (to be integrated with job posting creation)
    python ingest_employer.py --job-id UUID --employer-id UUID --title "..." --description "..."

Collections:
    - Employer_JobDescr_Collection: Stores job descriptions with title, date, and employer UUID
    - Employer_Skillswish_Collection: Stores desired skills with education and focus
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from loguru import logger

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from backend.db.chroma_crud_ops import write_collection
from backend.db.settings import (
    Employer_JobDescr_collection,
    Employer_Skillswish_collection,
)

# Add stdout handler for script output visibility in Docker/terminal
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    colorize=True
)


def load_test_data(data_dir: Path) -> list[dict[str, Any]]:
    """
    Load test data from JSON files in the specified directory.

    Args:
        data_dir: Path to directory containing test JSON files

    Returns:
        List of dictionaries containing test data

    Raises:
        FileNotFoundError: If data directory doesn't exist
    """
    if not data_dir.exists():
        msg = f"Data directory not found: {data_dir}"
        logger.error(msg)
        raise FileNotFoundError(msg)

    # Load job description and skills files
    job_files = sorted(data_dir.glob("test_employer_job_*.json"))
    skills_files = sorted(data_dir.glob("test_employer_skills_*.json"))

    if not job_files:
        logger.warning(f"No job description test files found in {data_dir}")
    if not skills_files:
        logger.warning(f"No skills test files found in {data_dir}")

    # Create a mapping of job_identification to data
    test_data: dict[str, dict[str, Any]] = {}

    # Load job description data
    for job_file in job_files:
        try:
            with job_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                job_id = data.get("job_identification")
                if job_id:
                    if job_id not in test_data:
                        test_data[job_id] = {}
                    test_data[job_id]["job_identification"] = job_id
                    test_data[job_id]["employer_identification"] = data.get(
                        "employer_identification"
                    )
                    test_data[job_id]["job_title"] = data.get("job_title")
                    test_data[job_id]["job_description"] = data.get("job_description")
                    test_data[job_id]["posted_date"] = data.get("posted_date")
                    logger.debug(f"Loaded job description from {job_file.name}")
        except Exception as e:
            logger.error(f"Error loading {job_file.name}: {e}")

    # Load skills data
    for skills_file in skills_files:
        try:
            with skills_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                job_id = data.get("job_identification")
                if job_id:
                    if job_id not in test_data:
                        test_data[job_id] = {
                            "job_identification": job_id,
                            "employer_identification": data.get("employer_identification")
                        }
                    test_data[job_id]["education_level"] = data.get("education_level")
                    test_data[job_id]["edu_focus"] = data.get("edu_focus")
                    test_data[job_id]["key_skills"] = data.get("key_skills", [])
                    logger.debug(f"Loaded skills from {skills_file.name}")
        except Exception as e:
            logger.error(f"Error loading {skills_file.name}: {e}")

    return list(test_data.values())


def ingest_job_description(
    job_identification: str,
    employer_identification: str,
    job_title: str,
    job_description: str,
    posted_date: str | None = None
) -> int:
    """
    Ingest a job description into ChromaDB.

    Args:
        job_identification: Unique UUID identifier for the job posting
        employer_identification: Unique UUID identifier for the employer
        job_title: Title of the job posting
        job_description: Full job description text
        posted_date: ISO format timestamp (optional, defaults to now)

    Returns:
        1 if successful, -1 if failed
    """
    try:
        # Prepare metadata
        post_date = posted_date or str(datetime.now(ZoneInfo("America/Denver")))
        metadata = {
            "Title": job_title,
            "Post_Date": post_date,
            "Employer_UUID": employer_identification
        }

        # Write to ChromaDB
        result = write_collection(
            collection=Employer_JobDescr_collection,
            collection_name="Employer_JobDescr_Collection",
            id_value=job_identification,
            text_value=job_description,
            metadata=metadata
        )

        if result == 1:
            logger.info(
                f"Successfully ingested job description for job {job_identification}"
            )
        return result

    except Exception as e:
        logger.error(
            f"Failed to ingest job description for job {job_identification}: {e}"
        )
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
            id_value=job_identification,
            text_value=skills_text,
            metadata=metadata
        )

        if result == 1:
            logger.info(
                f"Successfully ingested skills for job {job_identification}"
            )
        return result

    except Exception as e:
        logger.error(
            f"Failed to ingest skills for job {job_identification}: {e}"
        )
        return -1


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Ingest employer job descriptions and skills into ChromaDB"
    )
    parser.add_argument(
        "--test-data",
        action="store_true",
        help="Load test data from JSON files in ./backend/db/chroma_data/employer/"
    )
    parser.add_argument(
        "--job-id",
        type=str,
        help="Job identification UUID (required for non-test mode)"
    )
    parser.add_argument(
        "--employer-id",
        type=str,
        help="Employer identification UUID (required for non-test mode)"
    )
    parser.add_argument(
        "--title",
        type=str,
        help="Job title (required for non-test mode)"
    )
    parser.add_argument(
        "--description",
        type=str,
        help="Job description text (required for non-test mode)"
    )
    parser.add_argument(
        "--education-level",
        type=str,
        help="Required education level (BA, BS, MA, MS, MBA, PhD)"
    )
    parser.add_argument(
        "--edu-focus",
        type=str,
        help="Required field of study/focus"
    )
    parser.add_argument(
        "--skills",
        type=str,
        nargs="+",
        help="List of desired skills (space-separated)"
    )

    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Employer Data Ingestion Script")
    logger.info("=" * 60)

    success_count = 0
    failure_count = 0

    if args.test_data:
        # Test data mode
        logger.info("Running in TEST DATA mode")

        # Determine the correct path (works both locally and in Docker)
        # Try Docker path first, then local path
        project_root = Path(__file__).parent.parent.parent.parent
        data_dir = project_root / "backend" / "db" / "chroma_data" / "employer"

        if not data_dir.exists():
            # Try alternative path for Docker
            data_dir = Path("/app/backend/db/chroma_data/employer")

        logger.info(f"Loading test data from: {data_dir}")

        try:
            test_records = load_test_data(data_dir)
            logger.info(f"Found {len(test_records)} test record(s)")

            for record in test_records:
                job_id = record.get("job_identification")
                employer_id = record.get("employer_identification")
                logger.info(f"\nProcessing job: {job_id}")

                # Ingest job description if present
                if "job_description" in record and record["job_description"]:
                    result = ingest_job_description(
                        job_identification=job_id,
                        employer_identification=employer_id,
                        job_title=record.get("job_title", ""),
                        job_description=record["job_description"],
                        posted_date=record.get("posted_date")
                    )
                    if result == 1:
                        success_count += 1
                    else:
                        failure_count += 1

                # Ingest skills if present
                if any(k in record for k in ["education_level", "edu_focus", "key_skills"]):
                    result = ingest_employer_skills(
                        job_identification=job_id,
                        education_level=record.get("education_level", ""),
                        edu_focus=record.get("edu_focus", ""),
                        key_skills=record.get("key_skills", [])
                    )
                    if result == 1:
                        success_count += 1
                    else:
                        failure_count += 1

        except Exception as e:
            logger.error(f"Error processing test data: {e}")
            sys.exit(1)

    else:
        # Production mode - single record ingestion
        logger.info("Running in PRODUCTION mode")

        if not args.job_id or not args.employer_id:
            logger.error("--job-id and --employer-id are required in production mode")
            parser.print_help()
            sys.exit(1)

        # Ingest job description if provided
        if args.title and args.description:
            result = ingest_job_description(
                job_identification=args.job_id,
                employer_identification=args.employer_id,
                job_title=args.title,
                job_description=args.description
            )
            if result == 1:
                success_count += 1
            else:
                failure_count += 1

        # Ingest skills if provided
        if args.education_level or args.edu_focus or args.skills:
            result = ingest_employer_skills(
                job_identification=args.job_id,
                education_level=args.education_level or "",
                edu_focus=args.edu_focus or "",
                key_skills=args.skills or []
            )
            if result == 1:
                success_count += 1
            else:
                failure_count += 1

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Ingestion Summary")
    logger.info("=" * 60)
    logger.info(f"Successful operations: {success_count}")
    logger.info(f"Failed operations: {failure_count}")
    logger.info("=" * 60)

    sys.exit(0 if failure_count == 0 else 1)


if __name__ == "__main__":
    main()

