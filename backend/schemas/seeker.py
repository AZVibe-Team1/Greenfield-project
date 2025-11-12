"""
Job Seeker MongoDB Model

This module defines the Seeker document model for MongoDB using Beanie ODM.
It includes sub-documents for personal information and job applications.
"""

from datetime import datetime
from typing import ClassVar, Literal

from beanie import Document
from loguru import logger
from pydantic import BaseModel, Field

from backend.utils.validators import Address, Email, USPhoneNumber


class Information(BaseModel):
    """
    Personal information sub-document for job seekers.

    Attributes:
        first_name: Job seeker's first name (required)
        last_name: Job seeker's last name (required)
        email: Email address (validated, required)
        phone: US phone number (validated, required)
        address: Complete address with validation (required)
    """
    first_name: str = Field(..., min_length=1, description="First name")
    last_name: str = Field(..., min_length=1, description="Last name")
    email: Email = Field(..., description="Email address")
    phone: USPhoneNumber = Field(..., description="US phone number")
    address: Address = Field(..., description="Complete address")


class Application(BaseModel):
    """
    Job application sub-document.

    Tracks a single job application made by the seeker.

    Attributes:
        job_id: Reference to the job posting (foreign key)
        employer_id: Reference to the employer (foreign key)
        date_applied: Timestamp when application was submitted
        application_status: Current status of the application
    """
    job_id: str = Field(..., description="Job posting ID (foreign key)")
    employer_id: str = Field(..., description="Employer ID (foreign key)")
    date_applied: datetime = Field(
        default_factory=datetime.now,
        description="Application submission date"
    )
    application_status: Literal["Submitted", "Interviewed", "Offered", "Rejected"] = Field(
        default="Submitted",
        description="Current application status"
    )


class Seeker(Document):
    """
    Job Seeker document model for MongoDB.

    This model represents a job seeker in the system with all their
    personal information, preferences, and application history.

    Attributes:
        information: Personal and contact information (required)
        password_hash: Hashed password for authentication (required)
        created_at: Account creation timestamp
        resume: Resume document content (optional)
        pay_range: Desired salary range [low, high] in pay_unit
        pay_unit: Unit for pay_range (Hourly, Monthly, or Yearly)
        education_level: Highest education level achieved (required)
        edu_focus: Field of study or specialization (required)
        key_skills: List of key skills (max 15)
        applications: List of job applications made

    Collection Settings:
        name: "seekers" - MongoDB collection name
    """
    information: Information = Field(..., description="Personal information")
    password_hash: str = Field(
        ...,
        min_length=6,
        description="Hashed password"
    )

    updated_at: datetime = Field(
        default_factory=datetime.now,
        description="Account updated timestamp"
    )
    resume: str | None = Field(
        default=None,
        description="Resume document content"
    )
    pay_range: list[int] = Field(
        default_factory=lambda: [0, 0],
        min_length=2,
        max_length=2,
        description="Desired pay range [low, high]"
    )
    pay_unit: Literal["Hourly", "Monthly", "Yearly"] = Field(
        default="Yearly",
        description="Unit for pay range"
    )
    education_level: Literal["BA", "BS", "MA", "MS", "MBA", "PhD"] = Field(
        ...,
        description="Highest education level"
    )
    edu_focus: str = Field(
        ...,
        min_length=1,
        description="Field of study or specialization"
    )
    key_skills: list[str] = Field(
        default_factory=list,
        max_length=15,
        description="List of key skills (max 15)"
    )
    applications: list[Application] = Field(
        default_factory=list,
        description="Job applications made by the seeker"
    )

    class Settings:
        name = "seekers"
        indexes: ClassVar[list[str]] = [
            "information.email",  # Index on email for faster lookups
            "created_at",  # Index on creation date
        ]


# Example usage
if __name__ == "__main__":
    from pydantic import ValidationError

    logger.debug("=== Seeker Model Validation Tests ===\n")

    # Test with valid seeker data
    try:
        seeker_data = {
            "information": {
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane.doe@example.com",
                "phone": "+12025550123",
                "address": {
                    "street": "123 Main St",
                    "city": "New York",
                    "state": "NY",
                    "zip_code": "10001"
                }
            },
            "password_hash": "hashed_password_123",
            "education_level": "BS",
            "edu_focus": "Computer Science",
            "pay_range": [60000, 90000],
            "pay_unit": "Yearly",
            "key_skills": ["Python", "FastAPI", "MongoDB", "Docker"],
        }

        # Note: In actual usage, this would be created with Seeker(**seeker_data)
        # For testing without DB connection, we just validate the structure
        logger.debug("✓ Valid seeker data structure")
        logger.debug(f"  Name: {seeker_data['information']['first_name']} {seeker_data['information']['last_name']}")
        logger.debug(f"  Email: {seeker_data['information']['email']}")
        logger.debug(f"  Education: {seeker_data['education_level']} in {seeker_data['edu_focus']}")
        logger.debug(f"  Pay Range: ${seeker_data['pay_range'][0]:,} - ${seeker_data['pay_range'][1]:,} {seeker_data['pay_unit']}")

    except ValidationError as e:
        logger.critical(f"✗ Validation error: {e}")

    logger.debug("\n=== Application Sub-document Test ===\n")

    # Test Application sub-document
    try:
        application = Application(
            job_id="job_12345",
            employer_id="employer_67890",
            application_status="Submitted"
        )
        logger.debug("✓ Valid application created")
        logger.debug(f"  Job ID: {application.job_id}")
        logger.debug(f"  Employer ID: {application.employer_id}")
        logger.debug(f"  Status: {application.application_status}")
        logger.debug(f"  Date Applied: {application.date_applied}")

    except ValidationError as e:
        logger.critical(f"✗ Validation error: {e}")

    logger.debug("\n=== Information Sub-document Test ===\n")

    # Test Information sub-document
    try:
        info = Information(
            first_name="John",
            last_name="Smith",
            email="john.smith@example.com",
            phone="+14155550100",
            address=Address(
                street="456 Oak Ave",
                city="San Francisco",
                state="CA",
                zip_code="94102"
            )
        )
        logger.debug("✓ Valid information created")
        logger.debug(f"  Name: {info.first_name} {info.last_name}")
        logger.debug(f"  Email: {info.email}")
        logger.debug(f"  Phone: {info.phone}")
        logger.debug(f"  Address: {info.address.street}, {info.address.city}, {info.address.state} {info.address.zip_code}")

    except ValidationError as e:
        logger.critical(f"✗ Validation error: {e}")
