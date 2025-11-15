#!/usr/bin/env python3
"""
Employer MongoDB Ingestion Script

This script ingests employer test data into MongoDB.
Loads test data from JSON files in ./backend/db/mongo_data/employer/

Usage:
    # From project root
    python backend/db/ingest_mongo_employer.py

    # From Docker
    docker compose exec backend uv run python backend/db/ingest_mongo_employer.py

Collection:
    - employers: MongoDB collection for employer documents
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from loguru import logger

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from backend.db.employer_db_ops import EmployerCRUD
from backend.db.settings import close_mongodb_connection, connect_to_mongodb

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
        List of dictionaries containing test employer data

    Raises:
        FileNotFoundError: If data directory doesn't exist
    """
    if not data_dir.exists():
        msg = f"Data directory not found: {data_dir}"
        logger.error(msg)
        raise FileNotFoundError(msg)

    # Load employer test files
    test_files = sorted(data_dir.glob("test_employer_*.json"))

    if not test_files:
        logger.warning(f"No test files found in {data_dir}")
        return []

    test_data = []
    for test_file in test_files:
        try:
            with test_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                test_data.append(data)
                logger.debug(f"Loaded test data from {test_file.name}")
        except Exception as e:
            logger.error(f"Error loading {test_file.name}: {e}")

    return test_data


async def ingest_employer(employer_data: dict[str, Any]) -> bool:
    """
    Ingest a single employer record into MongoDB.

    Args:
        employer_data: Dictionary containing employer information

    Returns:
        True if successful, False if failed
    """
    try:
        # Check if employer with this email already exists
        email = employer_data["email"]
        existing_employer = await EmployerCRUD.get_employer_by_email(email)
        
        if existing_employer:
            logger.warning(
                f"Employer with email {email} already exists "
                f"(Company: {existing_employer.company_information.company_name}). Skipping."
            )
            return False

        # Also check by company name
        company_name = employer_data["company_information"]["company_name"]
        existing_company = await EmployerCRUD.get_employer_by_company_name(company_name)
        
        if existing_company:
            logger.warning(
                f"Employer with company name '{company_name}' already exists (ID: {existing_company.id}). Skipping."
            )
            return False

        # Create employer using CRUD operation
        new_employer = await EmployerCRUD.create_employer(employer_data)

        if new_employer:
            job_count = len(employer_data.get("open_jobs", []))
            logger.info(
                f"Successfully ingested employer: {company_name} "
                f"with {job_count} job posting(s) (ID: {new_employer.id})"
            )
            return True
        else:
            logger.error(f"Failed to ingest employer: {company_name}")
            return False

    except Exception as e:
        logger.error(
            f"Error ingesting employer {employer_data.get('company_information', {}).get('company_name', 'unknown')}: {e}"
        )
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main execution function."""
    logger.info("=" * 60)
    logger.info("MongoDB Employer Data Ingestion Script")
    logger.info("=" * 60)

    success_count = 0
    failure_count = 0
    skipped_count = 0
    total_jobs = 0

    # Determine the correct path (works both locally and in Docker)
    project_root = Path(__file__).parent.parent.parent.parent
    data_dir = project_root / "backend" / "db" / "mongo_data" / "employer"

    if not data_dir.exists():
        # Try alternative path for Docker
        data_dir = Path("/app/backend/db/mongo_data/employer")

    logger.info(f"Loading test data from: {data_dir}")

    try:
        # Load test data
        test_records = load_test_data(data_dir)
        logger.info(f"Found {len(test_records)} test record(s)")

        if not test_records:
            logger.warning("No test data to ingest")
            return

        # Count total jobs
        for record in test_records:
            total_jobs += len(record.get("open_jobs", []))

        logger.info(f"Total job postings to ingest: {total_jobs}")

        # Connect to MongoDB
        logger.info("Connecting to MongoDB...")
        await connect_to_mongodb()
        logger.info("✓ Connected to MongoDB")

        # Ingest each record
        for idx, record in enumerate(test_records, 1):
            logger.info(f"\nProcessing record {idx}/{len(test_records)}...")
            
            result = await ingest_employer(record)
            
            if result:
                success_count += 1
            elif result is False:
                # Check if it was skipped due to duplicate
                email = record.get("email", "")
                existing = await EmployerCRUD.get_employer_by_email(email)
                if existing:
                    skipped_count += 1
                else:
                    failure_count += 1

    except FileNotFoundError as e:
        logger.error(f"Data directory not found: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error processing test data: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Close MongoDB connection
        await close_mongodb_connection()
        logger.info("✓ Disconnected from MongoDB")

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Ingestion Summary")
    logger.info("=" * 60)
    logger.info(f"Successfully ingested: {success_count} employer(s)")
    logger.info(f"Job postings ingested: {total_jobs if success_count > 0 else 0}")
    logger.info(f"Skipped (duplicates): {skipped_count}")
    logger.info(f"Failed: {failure_count}")
    logger.info("=" * 60)

    sys.exit(0 if failure_count == 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())

