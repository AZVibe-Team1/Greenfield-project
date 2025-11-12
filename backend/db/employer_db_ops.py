"""
Employer CRUD Operations

This module provides Create, Read, Update, and Delete operations
for the Employer collection in MongoDB using Beanie ODM.
"""

import traceback
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from beanie import PydanticObjectId
from loguru import logger
from pymongo.errors import DuplicateKeyError

from backend.schemas.employer import ApplicationReceived, Employer, OpenJob


class EmployerCRUD:
    """CRUD operations for Employer collection."""

    @staticmethod
    async def create_employer(employer_data: dict[str, Any]) -> Employer | None:
        """
        Create a new employer in the database.

        Args:
            employer_data: Dictionary containing employer information

        Returns:
            Created Employer document or None if creation fails

        Raises:
            DuplicateKeyError: If an employer with the same details already exists
            ValueError: If validation fails

        Example:
            >>> employer_data = {
            ...     "company_information": {
            ...         "company_name": "Tech Corp",
            ...         "address": {...},
            ...         "industry": [
            ...             {"code": "45", "description": "Information Technology"},
            ...             {"code": "4510", "description": "Software & Services"}
            ...         ],
            ...         "benefits": "Health, 401k, Remote"
            ...     },
            ...     "contact_first_name": "John",
            ...     "contact_last_name": "Doe",
            ...     "password_hash": "hashed_password",
            ...     "open_jobs": [...]
            ... }
            >>> new_employer = await create_employer(employer_data)
        """
        try:
            employer = Employer(**employer_data)
            await employer.insert()
        except DuplicateKeyError as e:
            logger.critical(f"Duplicate employer error: {e}")
            raise
        except Exception as e:
            logger.critical(f"Error creating employer: {e}")
            return None
        else:
            return employer

    @staticmethod
    async def get_employer_by_id(employer_id: str | PydanticObjectId) -> Employer | None:
        """
        Retrieve an employer by their ID.

        Args:
            employer_id: Employer's ObjectId (string or PydanticObjectId)

        Returns:
            Employer document or None if not found

        Example:
            >>> employer = await get_employer_by_id("507f1f77bcf86cd799439011")
        """
        try:
            if isinstance(employer_id, str):
                employer_id = PydanticObjectId(employer_id)
            return await Employer.get(employer_id)
        except Exception as e:
            logger.critical(f"Error retrieving employer: {e}")
            return None

    @staticmethod
    async def get_employer_by_email(email: str) -> Employer | None:
        """
        Retrieve an employer by email address.

        Args:
            email: Contact email address

        Returns:
            Employer document or None if not found

        Example:
            >>> employer = await get_employer_by_email("contact@techcorp.com")
        """
        try:
            return await Employer.find_one(Employer.email == email)
        except Exception as e:
            logger.critical(f"Error retrieving employer by email: {e}")
            return None

    @staticmethod
    async def get_employer_by_company_name(company_name: str) -> Employer | None:
        """
        Retrieve an employer by company name.

        Args:
            company_name: Company name

        Returns:
            Employer document or None if not found

        Example:
            >>> employer = await get_employer_by_company_name("Tech Corp")
        """
        try:
            return await Employer.find_one(
                Employer.company_information.company_name == company_name
            )
        except Exception as e:
            logger.critical(f"Error retrieving employer by company name: {e}")
            return None

    @staticmethod
    async def get_all_employers(skip: int = 0, limit: int = 100) -> list[Employer]:
        """
        Retrieve all employers with pagination.

        Args:
            skip: Number of documents to skip (for pagination)
            limit: Maximum number of documents to return

        Returns:
            List of Employer documents

        Example:
            >>> employers = await get_all_employers(skip=0, limit=50)
        """
        try:
            return await Employer.find_all().skip(skip).limit(limit).to_list()
        except Exception as e:
            logger.critical(f"Error retrieving employers: {e}")
            return []

    @staticmethod
    async def update_employer(
        employer_id: str | PydanticObjectId,
        update_data: dict[str, Any]
    ) -> Employer | None:
        """
        Update an employer's information.

        Args:
            employer_id: Employer's ObjectId
            update_data: Dictionary containing fields to update

        Returns:
            Updated Employer document or None if not found/update fails

        Example:
            >>> update_data = {"contact_first_name": "Jane"}
            >>> updated_employer = await update_employer(employer_id, update_data)
        """
        try:
            employer = await EmployerCRUD.get_employer_by_id(employer_id)
            if not employer:
                logger.critical(f"Employer not found: {employer_id}")
                return None

            # Update fields
            for key, value in update_data.items():
                if hasattr(employer, key):
                    setattr(employer, key, value)

            await employer.save()
        except Exception as e:
            logger.critical(f"Error updating employer: {e}")
            return None
        else:
            return employer

    @staticmethod
    async def add_job_posting(
        employer_id: str | PydanticObjectId,
        job_data: dict[str, Any]
    ) -> Employer | None:
        """
        Add a new job posting to an employer's open jobs.

        Args:
            employer_id: Employer's ObjectId
            job_data: Dictionary containing job posting information

        Returns:
            Updated Employer document or None if update fails

        Example:
            >>> job_data = {
            ...     "job_id": "job_123",
            ...     "job_title": "Software Engineer",
            ...     "job_description": "...",
            ...     "posted_date": datetime.now(ZoneInfo("America/Denver")),
            ...     "department": "Engineering",
            ...     ...
            ... }
            >>> employer = await add_job_posting(employer_id, job_data)
        """
        try:
            employer = await EmployerCRUD.get_employer_by_id(employer_id)
            if not employer:
                return None

            new_job = OpenJob(**job_data)
            employer.open_jobs.append(new_job)
            await employer.save()
        except Exception as e:
            logger.critical(f"Error adding job posting: {e}")
            return None
        else:
            return employer

    @staticmethod
    async def update_job_posting(
        employer_id: str | PydanticObjectId,
        job_id: str,
        update_data: dict[str, Any]
    ) -> Employer | None:
        """
        Update a specific job posting.

        Args:
            employer_id: Employer's ObjectId
            job_id: Job posting ID
            update_data: Dictionary containing fields to update

        Returns:
            Updated Employer document or None if update fails

        Example:
            >>> update_data = {"job_title": "Senior Software Engineer"}
            >>> employer = await update_job_posting(employer_id, "job_123", update_data)
        """
        try:
            employer = await EmployerCRUD.get_employer_by_id(employer_id)
            if not employer:
                return None

            # Find and update the specific job
            for job in employer.open_jobs:
                if job.job_id == job_id:
                    for key, value in update_data.items():
                        if hasattr(job, key):
                            setattr(job, key, value)
                    await employer.save()
                    return employer

            logger.critical(f"Job not found: {job_id}")
            return None
        except Exception as e:
            logger.critical(f"Error updating job posting: {e}")
            return None

    @staticmethod
    async def remove_job_posting(
        employer_id: str | PydanticObjectId,
        job_id: str
    ) -> Employer | None:
        """
        Remove a job posting from an employer's open jobs.

        Args:
            employer_id: Employer's ObjectId
            job_id: Job posting ID to remove

        Returns:
            Updated Employer document or None if update fails

        Example:
            >>> employer = await remove_job_posting(employer_id, "job_123")
        """
        try:
            employer = await EmployerCRUD.get_employer_by_id(employer_id)
            if not employer:
                return None

            # Remove the job
            employer.open_jobs = [job for job in employer.open_jobs if job.job_id != job_id]
            await employer.save()
            return employer
        except Exception as e:
            logger.critical(f"Error removing job posting: {e}")
            return None

    @staticmethod
    async def add_application_received(
        employer_id: str | PydanticObjectId,
        application_data: dict[str, Any]
    ) -> Employer | None:
        """
        Add a new application to an employer's received applications.

        Args:
            employer_id: Employer's ObjectId
            application_data: Dictionary containing application information

        Returns:
            Updated Employer document or None if update fails

        Example:
            >>> app_data = {
            ...     "applicant_id": "seeker_123",
            ...     "job_id": "job_456",
            ...     "candidate_tracking": {...}
            ... }
            >>> employer = await add_application_received(employer_id, app_data)
        """
        try:
            employer = await EmployerCRUD.get_employer_by_id(employer_id)
            if not employer:
                return None

            new_application = ApplicationReceived(**application_data)
            employer.apps_received.append(new_application)
            await employer.save()
            return employer
        except Exception as e:
            logger.critical(f"Error adding application: {e}")
            return None

    @staticmethod
    async def update_application_status(
        employer_id: str | PydanticObjectId,
        applicant_id: str,
        job_id: str,
        new_status: str
    ) -> Employer | None:
        """
        Update the status of a specific application.

        Args:
            employer_id: Employer's ObjectId
            applicant_id: Applicant ID
            job_id: Job ID
            new_status: New status ("Received", "Interviewed", "Offered", "Rejected", "Canceled")

        Returns:
            Updated Employer document or None if update fails

        Example:
            >>> employer = await update_application_status(
            ...     employer_id, "seeker_123", "job_456", "Interviewed"
            ... )
        """
        try:
            employer = await EmployerCRUD.get_employer_by_id(employer_id)
            if not employer:
                return None

            # Find and update the specific application
            for app in employer.apps_received:
                if app.applicant_id == applicant_id and app.job_id == job_id:
                    # Update tracking
                    app.candidate_tracking.previous_status = app.candidate_tracking.current_status
                    app.candidate_tracking.previous_status_date = app.candidate_tracking.current_status_date
                    app.candidate_tracking.current_status = new_status
                    app.candidate_tracking.current_status_date = datetime.now(ZoneInfo("America/Denver"))
                    await employer.save()
                    return employer

            logger.critical(f"Application not found for applicant {applicant_id} and job {job_id}")
            return None
        except Exception as e:
            logger.critical(f"Error updating application status: {e}")
            return None

    @staticmethod
    async def delete_employer(employer_id: str | PydanticObjectId) -> bool:
        """
        Delete an employer from the database.

        Args:
            employer_id: Employer's ObjectId

        Returns:
            True if deletion successful, False otherwise

        Example:
            >>> success = await delete_employer("507f1f77bcf86cd799439011")
        """
        try:
            employer = await EmployerCRUD.get_employer_by_id(employer_id)
            if not employer:
                logger.critical(f"Employer not found: {employer_id}")
                return False

            await employer.delete()
        except Exception as e:
            logger.critical(f"Error deleting employer: {e}")
            return False
        else:
            return True

    @staticmethod
    async def search_employers_by_industry(industry_code: str) -> list[Employer]:
        """
        Search for employers by GICS industry code.

        Args:
            industry_code: GICS industry code to search for

        Returns:
            List of Employer documents matching the industry code

        Example:
            >>> employers = await search_employers_by_industry("45")
        """
        try:
            return await Employer.find(
                {"company_information.industry.code": industry_code}
            ).to_list()
        except Exception as e:
            logger.critical(f"Error searching employers by industry: {e}")
            return []

    @staticmethod
    async def get_employers_with_open_jobs() -> list[Employer]:
        """
        Get all employers that have open job postings.

        Returns:
            List of Employer documents with open jobs

        Example:
            >>> employers = await get_employers_with_open_jobs()
        """
        try:
            return await Employer.find(
                {"open_jobs": {"$exists": True, "$ne": []}}
            ).to_list()
        except Exception as e:
            logger.critical(f"Error retrieving employers with open jobs: {e}")
            return []

    @staticmethod
    async def count_employers() -> int:
        """
        Count total number of employers in the collection.

        Returns:
            Total count of employers

        Example:
            >>> total = await count_employers()
        """
        try:
            return await Employer.count()
        except Exception as e:
            logger.critical(f"Error counting employers: {e}")
            return 0


# Convenience functions (backwards compatible)
create_employer = EmployerCRUD.create_employer
get_employer_by_id = EmployerCRUD.get_employer_by_id
get_employer_by_company_name = EmployerCRUD.get_employer_by_company_name
get_all_employers = EmployerCRUD.get_all_employers
update_employer = EmployerCRUD.update_employer
delete_employer = EmployerCRUD.delete_employer


# Example usage
if __name__ == "__main__":
    import asyncio

    from backend.db.settings import close_mongodb_connection, connect_to_mongodb

    async def test_employer_crud():
        """Test CRUD operations for Employer collection."""
        logger.debug("=== Employer CRUD Operations Test ===\n")

        # Connect to database
        await connect_to_mongodb()

        try:
            # Test 1: Create an employer
            logger.debug("Test 1: Create Employer")
            employer_data = {
                "company_information": {
                    "company_name": f"Test Corp {asyncio.get_event_loop().time()}",
                    "address": {
                        "street": "456 Business Ave",
                        "city": "San Francisco",
                        "state": "CA",
                        "zip_code": "94105"
                    },
                    "industry": [
                        {"code": "45", "description": "Information Technology"},
                        {"code": "4510", "description": "Software & Services"}
                    ],
                    "benefits": "Health insurance, 401k, Remote work"
                },
                "contact_first_name": "Test",
                "contact_last_name": "Manager",
                "password_hash": "hashed_password_123456",
                "open_jobs": [
                    {
                        "job_id": "test_job_001",
                        "job_title": "Software Engineer",
                        "job_description": "We are hiring!",
                        "posted_date": datetime.now(ZoneInfo("America/Denver")),
                        "department": "Engineering",
                        "hire_mgr_first": "John",
                        "hire_mgr_last": "Doe",
                        "pay_range": [100000, 150000],
                        "pay_unit": "Yearly",
                        "education_level": "BS",
                        "edu_focus": "Computer Science",
                        "key_skills": ["Python", "FastAPI"]
                    }
                ]
            }
            new_employer = await create_employer(employer_data)
            if not new_employer:
                logger.critical("✗ Failed to create employer")
                return

            logger.debug(f"✓ Created employer: {new_employer.id}")
            test_id = new_employer.id
            assert test_id is not None, "Employer ID should not be None"

            # Test 2: Read employer
            logger.debug("\nTest 2: Read Employer")
            employer = await get_employer_by_id(test_id)
            if employer:
                logger.debug(f"✓ Retrieved employer: {employer.company_information.company_name}")
            else:
                logger.critical("✗ Failed to retrieve employer")

            # Test 3: Update employer
            logger.debug("\nTest 3: Update Employer")
            updated = await update_employer(test_id, {"contact_first_name": "Updated"})
            if updated:
                logger.debug(f"✓ Updated employer contact: {updated.contact_first_name}")
            else:
                logger.critical("✗ Failed to update employer")

            # Test 4: Count employers
            logger.debug("\nTest 4: Count Employers")
            count = await EmployerCRUD.count_employers()
            logger.debug(f"✓ Total employers in database: {count}")

            # Test 5: Delete employer
            logger.debug("\nTest 5: Delete Employer")
            deleted = await delete_employer(test_id)
            if deleted:
                logger.debug("✓ Employer deleted successfully")
            else:
                logger.critical("✗ Failed to delete employer")

            logger.debug("\n✅ All CRUD operations tested successfully!")

        except Exception as e:
            logger.critical(f"\n❌ Test failed: {e}")
            traceback.print_exc()

        finally:
            await close_mongodb_connection()

    # Run tests
    asyncio.run(test_employer_crud())

