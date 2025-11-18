#!/usr/bin/env python3
"""
Seeker Resume and Skills Ingestion Script for ChromaDB

This script ingests job seeker resume and skills data into ChromaDB collections.
It can run in two modes:
1. Test mode (--test-data flag): Loads test data from JSON files
2. Production mode: Accepts resume and skills data as arguments

Usage:
    # Test mode with JSON files
    python ingest_seeker.py --test-data

    # Production mode (to be integrated with actual resume upload)
    python ingest_seeker.py --seeker-id UUID --resume "text" --skills "skills"

Collections:
    - Seeker_Resume_Collection: Stores resume text with Post_Date metadata
    - Seeker_Skills_Collection: Stores concatenated skills with metadata
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
from backend.db.settings import Seeker_Resume_collection, Seeker_Skill_collection

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

    # Load resume files
    resume_files = sorted(data_dir.glob("test_seeker_resume_*.json"))
    skills_files = sorted(data_dir.glob("test_seeker_skills_*.json"))

    if not resume_files:
        logger.warning(f"No resume test files found in {data_dir}")
    if not skills_files:
        logger.warning(f"No skills test files found in {data_dir}")

    # Create a mapping of seeker_identification to data
    test_data: dict[str, dict[str, Any]] = {}

    # Load resume data
    for resume_file in resume_files:
        try:
            with resume_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                seeker_id = data.get("seeker_identification")
                if seeker_id:
                    if seeker_id not in test_data:
                        test_data[seeker_id] = {}
                    test_data[seeker_id]["resume"] = data.get("resume")
                    test_data[seeker_id]["created_at"] = data.get("created_at")
                    test_data[seeker_id]["seeker_identification"] = seeker_id
                    logger.debug(f"Loaded resume from {resume_file.name}")
        except Exception as e:
            logger.error(f"Error loading {resume_file.name}: {e}")

    # Load skills data
    for skills_file in skills_files:
        try:
            with skills_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                seeker_id = data.get("seeker_identification")
                if seeker_id:
                    if seeker_id not in test_data:
                        test_data[seeker_id] = {"seeker_identification": seeker_id}
                    test_data[seeker_id]["education_level"] = data.get("education_level")
                    test_data[seeker_id]["edu_focus"] = data.get("edu_focus")
                    test_data[seeker_id]["key_skills"] = data.get("key_skills", [])
                    logger.debug(f"Loaded skills from {skills_file.name}")
        except Exception as e:
            logger.error(f"Error loading {skills_file.name}: {e}")

    return list(test_data.values())


def ingest_seeker_resume(
    seeker_identification: str,
    resume: str,
    created_at: str | None = None
) -> int:
    """
    Ingest a seeker's resume into ChromaDB.

    Args:
        seeker_identification: Unique UUID identifier for the seeker
        resume: Resume text content
        created_at: ISO format timestamp (optional, defaults to now)

    Returns:
        1 if successful, -1 if failed
    """
    try:
        # Prepare metadata
        post_date = created_at or str(datetime.now(ZoneInfo("America/Denver")))
        metadata = {"Post_Date": post_date}

        # Write to ChromaDB
        result = write_collection(
            collection=Seeker_Resume_collection,
            collection_name="Seeker_Resume_Collection",
            id_value=seeker_identification,
            text_value=resume,
            metadata=metadata
        )

        if result == 1:
            logger.info(
                f"Successfully ingested resume for seeker {seeker_identification}"
            )
        return result

    except Exception as e:
        logger.error(
            f"Failed to ingest resume for seeker {seeker_identification}: {e}"
        )
        return -1


def ingest_seeker_skills(
    seeker_identification: str,
    education_level: str,
    edu_focus: str,
    key_skills: list[str]
) -> int:
    """
    Ingest a seeker's skills into ChromaDB.

    Args:
        seeker_identification: Unique UUID identifier for the seeker
        education_level: Education level (BA, BS, MA, MS, MBA, PhD)
        edu_focus: Field of study/focus
        key_skills: List of key skills (up to 15)

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
            collection=Seeker_Skill_collection,
            collection_name="Seeker_Skills_Collection",
            id_value=seeker_identification,
            text_value=skills_text,
            metadata=metadata
        )

        if result == 1:
            logger.info(
                f"Successfully ingested skills for seeker {seeker_identification}"
            )
        return result

    except Exception as e:
        logger.error(
            f"Failed to ingest skills for seeker {seeker_identification}: {e}"
        )
        return -1


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Ingest seeker resume and skills data into ChromaDB"
    )
    parser.add_argument(
        "--test-data",
        action="store_true",
        help="Load test data from JSON files in ./backend/db/chroma_data/seeker/"
    )
    parser.add_argument(
        "--seeker-id",
        type=str,
        help="Seeker identification UUID (required for non-test mode)"
    )
    parser.add_argument(
        "--resume",
        type=str,
        help="Resume text content (required for non-test mode)"
    )
    parser.add_argument(
        "--education-level",
        type=str,
        help="Education level (BA, BS, MA, MS, MBA, PhD)"
    )
    parser.add_argument(
        "--edu-focus",
        type=str,
        help="Field of study/focus"
    )
    parser.add_argument(
        "--skills",
        type=str,
        nargs="+",
        help="List of key skills (space-separated)"
    )

    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Seeker Data Ingestion Script")
    logger.info("=" * 60)

    success_count = 0
    failure_count = 0

    if args.test_data:
        # Test data mode
        logger.info("Running in TEST DATA mode")

        # Determine the correct path (works both locally and in Docker)
        # Try Docker path first, then local path
        project_root = Path(__file__).parent.parent.parent.parent
        data_dir = project_root / "backend" / "db" / "chroma_data" / "seeker"

        if not data_dir.exists():
            # Try alternative path for Docker
            data_dir = Path("/app/backend/db/chroma_data/seeker")

        logger.info(f"Loading test data from: {data_dir}")

        try:
            test_records = load_test_data(data_dir)
            logger.info(f"Found {len(test_records)} test record(s)")

            for record in test_records:
                seeker_id = record.get("seeker_identification")
                logger.info(f"\nProcessing seeker: {seeker_id}")

                # Ingest resume if present
                if "resume" in record and record["resume"]:
                    result = ingest_seeker_resume(
                        seeker_identification=seeker_id,
                        resume=record["resume"],
                        created_at=record.get("created_at")
                    )
                    if result == 1:
                        success_count += 1
                    else:
                        failure_count += 1

                # Ingest skills if present
                if any(k in record for k in ["education_level", "edu_focus", "key_skills"]):
                    result = ingest_seeker_skills(
                        seeker_identification=seeker_id,
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

        if not args.seeker_id:
            logger.error("--seeker-id is required in production mode")
            parser.print_help()
            sys.exit(1)

        # Ingest resume if provided
        if args.resume:
            result = ingest_seeker_resume(
                seeker_identification=args.seeker_id,
                resume=args.resume
            )
            if result == 1:
                success_count += 1
            else:
                failure_count += 1

        # Ingest skills if provided
        if args.education_level or args.edu_focus or args.skills:
            result = ingest_seeker_skills(
                seeker_identification=args.seeker_id,
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

