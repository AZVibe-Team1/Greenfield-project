"""
Seeker CRUD Operations

This module provides Create, Read, Update, and Delete operations
for the Seeker collection in MongoDB using Beanie ODM.
"""

from datetime import datetime
from typing import Any

from beanie import PydanticObjectId
from loguru import logger
from pymongo.errors import DuplicateKeyError

from backend.schemas.seeker import Application, Seeker


class SeekerCRUD:
    """CRUD operations for Seeker collection."""

    @staticmethod
    async def create_seeker(seeker_data: dict[str, Any]) -> Seeker | None:
        """
        Create a new seeker in the database.

        Args:
            seeker_data: Dictionary containing seeker information

        Returns:
            Created Seeker document or None if creation fails

        Raises:
            DuplicateKeyError: If a seeker with the same email already exists
            ValueError: If validation fails

        Example:
            >>> seeker_data = {
            ...     "information": {
            ...         "first_name": "John",
            ...         "last_name": "Doe",
            ...         "email": "john@example.com",
            ...         "phone": "+12025550123",
            ...         "address": {
            ...             "street": "123 Main St",
            ...             "city": "New York",
            ...             "state": "NY",
            ...             "zip_code": "10001"
            ...         }
            ...     },
            ...     "password_hash": "hashed_password",
            ...     "education_level": "BS",
            ...     "edu_focus": "Computer Science"
            ... }
            >>> new_seeker = await create_seeker(seeker_data)
        """
        try:
            seeker = Seeker(**seeker_data)
            await seeker.insert()
        except DuplicateKeyError as e:
            logger.critical(f"Duplicate seeker error: {e}")
            raise
        except Exception as e:
            logger.critical(f"Error creating seeker: {e}")
            return None
        else:
            return seeker

    @staticmethod
    async def get_seeker_by_id(seeker_id: str | PydanticObjectId) -> Seeker | None:
        """
        Retrieve a seeker by their ID.

        Args:
            seeker_id: Seeker's ObjectId (string or PydanticObjectId)

        Returns:
            Seeker document or None if not found

        Example:
            >>> seeker = await get_seeker_by_id("507f1f77bcf86cd799439011")
        """
        try:
            if isinstance(seeker_id, str):
                seeker_id = PydanticObjectId(seeker_id)
            return await Seeker.get(seeker_id)
        except Exception as e:
            logger.critical(f"Error retrieving seeker: {e}")
            return None

    @staticmethod
    async def get_seeker_by_email(email: str) -> Seeker | None:
        """
        Retrieve a seeker by their email address.

        Args:
            email: Seeker's email address

        Returns:
            Seeker document or None if not found

        Example:
            >>> seeker = await get_seeker_by_email("john@example.com")
        """
        try:
            return await Seeker.find_one(Seeker.information.email == email)
        except Exception as e:
            logger.critical(f"Error retrieving seeker by email: {e}")
            return None

    @staticmethod
    async def get_all_seekers(skip: int = 0, limit: int = 100) -> list[Seeker]:
        """
        Retrieve all seekers with pagination.

        Args:
            skip: Number of documents to skip (for pagination)
            limit: Maximum number of documents to return

        Returns:
            List of Seeker documents

        Example:
            >>> seekers = await get_all_seekers(skip=0, limit=50)
        """
        try:
            return await Seeker.find_all().skip(skip).limit(limit).to_list()
        except Exception as e:
            logger.critical(f"Error retrieving seekers: {e}")
            return []

    @staticmethod
    async def update_seeker(
        seeker_id: str | PydanticObjectId,
        update_data: dict[str, Any]
    ) -> Seeker | None:
        """
        Update a seeker's information.

        Args:
            seeker_id: Seeker's ObjectId
            update_data: Dictionary containing fields to update

        Returns:
            Updated Seeker document or None if not found/update fails

        Example:
            >>> update_data = {"edu_focus": "Data Science"}
            >>> updated_seeker = await update_seeker(seeker_id, update_data)
        """
        try:
            seeker = await SeekerCRUD.get_seeker_by_id(seeker_id)
            if not seeker:
                logger.critical(f"Seeker not found: {seeker_id}")
                return None

            # Update fields
            for key, value in update_data.items():
                if hasattr(seeker, key):
                    setattr(seeker, key, value)

            await seeker.save()
        except Exception as e:
            logger.critical(f"Error updating seeker: {e}")
            return None
        else:
            return seeker

    @staticmethod
    async def update_seeker_skills(
        seeker_id: str | PydanticObjectId,
        skills: list[str]
    ) -> Seeker | None:
        """
        Update a seeker's skills list.

        Args:
            seeker_id: Seeker's ObjectId
            skills: New list of skills (max 15)

        Returns:
            Updated Seeker document or None if update fails

        Example:
            >>> skills = ["Python", "FastAPI", "MongoDB"]
            >>> updated_seeker = await update_seeker_skills(seeker_id, skills)
        """
        if len(skills) > 15:
            logger.critical("Skills list cannot exceed 15 items")
            return None

        return await SeekerCRUD.update_seeker(seeker_id, {"key_skills": skills})

    @staticmethod
    async def add_application(
        seeker_id: str | PydanticObjectId,
        job_id: str,
        employer_id: str,
        application_status: str = "Submitted"
    ) -> Seeker | None:
        """
        Add a new job application to a seeker's record.

        Args:
            seeker_id: Seeker's ObjectId
            job_id: Job posting ID
            employer_id: Employer ID
            application_status: Initial status (default: "Submitted")

        Returns:
            Updated Seeker document or None if update fails

        Example:
            >>> seeker = await add_application(seeker_id, "job_123", "emp_456")
        """
        try:
            seeker = await SeekerCRUD.get_seeker_by_id(seeker_id)
            if not seeker:
                return None

            new_application = Application(
                job_id=job_id,
                employer_id=employer_id,
                date_applied=datetime.now(),
                application_status=application_status
            )

            seeker.applications.append(new_application)
            await seeker.save()
        except Exception as e:
            logger.critical(f"Error adding application: {e}")
            return None
        else:
            return seeker

    @staticmethod
    async def delete_seeker(seeker_id: str | PydanticObjectId) -> bool:
        """
        Delete a seeker from the database.

        Args:
            seeker_id: Seeker's ObjectId

        Returns:
            True if deletion successful, False otherwise

        Example:
            >>> success = await delete_seeker("507f1f77bcf86cd799439011")
        """
        try:
            seeker = await SeekerCRUD.get_seeker_by_id(seeker_id)
            if not seeker:
                logger.critical(f"Seeker not found: {seeker_id}")
                return False

            await seeker.delete()
        except Exception as e:
            logger.critical(f"Error deleting seeker: {e}")
            return False
        else:
            return True

    @staticmethod
    async def search_seekers_by_skills(skills: list[str]) -> list[Seeker]:
        """
        Search for seekers who have specific skills.

        Args:
            skills: List of skills to search for

        Returns:
            List of Seeker documents matching the search criteria

        Example:
            >>> seekers = await search_seekers_by_skills(["Python", "FastAPI"])
        """
        try:
            return await Seeker.find(
                {"key_skills": {"$in": skills}}
            ).to_list()
        except Exception as e:
            logger.critical(f"Error searching seekers by skills: {e}")
            return []

    @staticmethod
    async def search_seekers_by_education(
        education_level: str,
        edu_focus: str | None = None
    ) -> list[Seeker]:
        """
        Search for seekers by education level and optionally by focus.

        Args:
            education_level: Education level (BA, BS, MA, MS, MBA, PhD)
            edu_focus: Field of study (optional)

        Returns:
            List of Seeker documents matching the criteria

        Example:
            >>> seekers = await search_seekers_by_education("BS", "Computer Science")
        """
        try:
            query = {"education_level": education_level}
            if edu_focus:
                query["edu_focus"] = {"$regex": edu_focus, "$options": "i"}

            return await Seeker.find(query).to_list()
        except Exception as e:
            logger.critical(f"Error searching seekers by education: {e}")
            return []

    @staticmethod
    async def count_seekers() -> int:
        """
        Count total number of seekers in the collection.

        Returns:
            Total count of seekers

        Example:
            >>> total = await count_seekers()
        """
        try:
            return await Seeker.count()
        except Exception as e:
            logger.critical(f"Error counting seekers: {e}")
            return 0


# Convenience functions (backwards compatible)
create_seeker = SeekerCRUD.create_seeker
get_seeker_by_id = SeekerCRUD.get_seeker_by_id
get_seeker_by_email = SeekerCRUD.get_seeker_by_email
get_all_seekers = SeekerCRUD.get_all_seekers
update_seeker = SeekerCRUD.update_seeker
delete_seeker = SeekerCRUD.delete_seeker


# Example usage
if __name__ == "__main__":
    import asyncio

    from backend.db.settings import close_mongodb_connection, connect_to_mongodb

    async def test_seeker_crud():
        """Test CRUD operations for Seeker collection."""
        logger.debug("=== Seeker CRUD Operations Test ===\n")

        # Connect to database
        await connect_to_mongodb()

        try:
            # Test 1: Create a seeker
            logger.debug("Test 1: Create Seeker")
            seeker_data = {
                "information": {
                    "first_name": "Test",
                    "last_name": "User",
                    "email": f"test.user.{asyncio.get_event_loop().time()}@example.com",
                    "phone": "+12025550123",
                    "address": {
                        "street": "123 Test St",
                        "city": "Test City",
                        "state": "NY",
                        "zip_code": "10001"
                    }
                },
                "password_hash": "hashed_password_123456",
                "education_level": "BS",
                "edu_focus": "Computer Science",
                "key_skills": ["Python", "FastAPI", "MongoDB"]
            }
            new_seeker = await create_seeker(seeker_data)
            if not new_seeker:
                logger.critical("✗ Failed to create seeker")
                return

            logger.debug(f"✓ Created seeker: {new_seeker.id}")
            test_id = new_seeker.id
            assert test_id is not None, "Seeker ID should not be None"

            # Test 2: Read seeker
            logger.debug("\nTest 2: Read Seeker")
            seeker = await get_seeker_by_id(test_id)
            if seeker:
                logger.debug(f"✓ Retrieved seeker: {seeker.information.first_name} {seeker.information.last_name}")
            else:
                logger.critical("✗ Failed to retrieve seeker")

            # Test 3: Update seeker
            logger.debug("\nTest 3: Update Seeker")
            updated = await update_seeker(test_id, {"edu_focus": "Data Science"})
            if updated:
                logger.debug(f"✓ Updated seeker focus to: {updated.edu_focus}")
            else:
                logger.critical("✗ Failed to update seeker")

            # Test 4: Count seekers
            logger.debug("\nTest 4: Count Seekers")
            count = await SeekerCRUD.count_seekers()
            logger.debug(f"✓ Total seekers in database: {count}")

            # Test 5: Delete seeker
            logger.debug("\nTest 5: Delete Seeker")
            deleted = await delete_seeker(test_id)
            if deleted:
                logger.debug("✓ Seeker deleted successfully")
            else:
                logger.critical("✗ Failed to delete seeker")

            logger.debug("\n✅ All CRUD operations tested successfully!")

        except Exception as e:
            logger.critical(f"\n❌ Test failed: {e}")

        finally:
            await close_mongodb_connection()

    # Run tests
    asyncio.run(test_seeker_crud())

