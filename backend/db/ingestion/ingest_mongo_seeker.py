#!/usr/bin/env python3
"""
Seeker MongoDB Ingestion Script

This script ingests job seeker test data into MongoDB.
Loads test data from JSON files in ./backend/db/mongo_data/seeker/

Usage:
    # From project root
    python backend/db/ingest_mongo_seeker.py

    # From Docker
    docker compose exec backend uv run python backend/db/ingest_mongo_seeker.py

Collection:
    - seekers: MongoDB collection for job seeker documents
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from loguru import logger

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from backend.db.seeker_db_ops import SeekerCRUD
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
        List of dictionaries containing test seeker data

    Raises:
        FileNotFoundError: If data directory doesn't exist
    """
    if not data_dir.exists():
        msg = f"Data directory not found: {data_dir}"
        logger.error(msg)
        raise FileNotFoundError(msg)

    # Load seeker test files
    test_files = sorted(data_dir.glob("test_seeker_*.json"))

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


async def ingest_seeker(seeker_data: dict[str, Any]) -> bool:
    """
    Ingest a single seeker record into MongoDB.

    Args:
        seeker_data: Dictionary containing seeker information

    Returns:
        True if successful, False if failed
    """
    try:
        # Check if seeker with this email already exists
        email = seeker_data["information"]["email"]
        existing_seeker = await SeekerCRUD.get_seeker_by_email(email)
        
        if existing_seeker:
            logger.warning(
                f"Seeker with email {email} already exists (ID: {existing_seeker.id}). Skipping."
            )
            return False

        # Create seeker using CRUD operation
        new_seeker = await SeekerCRUD.create_seeker(seeker_data)

        if new_seeker:
            logger.info(
                f"Successfully ingested seeker: {seeker_data['information']['first_name']} "
                f"{seeker_data['information']['last_name']} (ID: {new_seeker.id})"
            )
            return True
        else:
            logger.error(
                f"Failed to ingest seeker: {seeker_data['information']['first_name']} "
                f"{seeker_data['information']['last_name']}"
            )
            return False

    except Exception as e:
        logger.error(
            f"Error ingesting seeker {seeker_data.get('information', {}).get('email', 'unknown')}: {e}"
        )
        return False


async def main():
    """Main execution function."""
    logger.info("=" * 60)
    logger.info("MongoDB Seeker Data Ingestion Script")
    logger.info("=" * 60)

    success_count = 0
    failure_count = 0
    skipped_count = 0

    # Determine the correct path (works both locally and in Docker)
    project_root = Path(__file__).parent.parent.parent.parent
    data_dir = project_root / "backend" / "db" / "mongo_data" / "seeker"

    if not data_dir.exists():
        # Try alternative path for Docker
        data_dir = Path("/app/backend/db/mongo_data/seeker")

    logger.info(f"Loading test data from: {data_dir}")

    try:
        # Load test data
        test_records = load_test_data(data_dir)
        logger.info(f"Found {len(test_records)} test record(s)")

        if not test_records:
            logger.warning("No test data to ingest")
            return

        # Connect to MongoDB
        logger.info("Connecting to MongoDB...")
        await connect_to_mongodb()
        logger.info("✓ Connected to MongoDB")

        # Ingest each record
        for idx, record in enumerate(test_records, 1):
            logger.info(f"\nProcessing record {idx}/{len(test_records)}...")
            
            result = await ingest_seeker(record)
            
            if result:
                success_count += 1
            elif result is False:
                # Check if it was skipped due to duplicate
                email = record.get("information", {}).get("email", "")
                existing = await SeekerCRUD.get_seeker_by_email(email)
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
    logger.info(f"Successfully ingested: {success_count}")
    logger.info(f"Skipped (duplicates): {skipped_count}")
    logger.info(f"Failed: {failure_count}")
    logger.info("=" * 60)

    sys.exit(0 if failure_count == 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())

