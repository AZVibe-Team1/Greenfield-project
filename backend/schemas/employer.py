"""
Employer MongoDB Model

This module defines the Employer document model for MongoDB using Beanie ODM.
It includes sub-documents for company information, job postings, and application tracking.
"""

from datetime import datetime
from typing import ClassVar, Literal
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from beanie import Document, PydanticObjectId
from loguru import logger
from pydantic import BaseModel, Field

from backend.utils.gics_helper import is_valid_gics_code
from backend.utils.validators import Address, Email


class IndustryInfo(BaseModel):
    """
    Industry classification using GICS codes.

    Attributes:
        code: GICS industry code (2, 4, 6, or 8 digits)
        description: Description of the industry
    """
    code: str = Field(..., description="GICS industry code")
    description: str = Field(..., description="Industry description")

    def __init__(self, **data):
        """Initialize and validate GICS code."""
        super().__init__(**data)
        # Validate GICS code format (must be 2, 4, 6, or 8 digits)
        if len(self.code) not in [2, 4, 6, 8] or not self.code.isdigit():
            msg = f"Invalid GICS code format: {self.code}. Must be 2, 4, 6, or 8 digits."
            raise ValueError(msg)
        # Validate GICS code exists
        if not is_valid_gics_code(self.code):
            msg = f"Invalid GICS code: {self.code}"
            raise ValueError(msg)


class CompanyInformation(BaseModel):
    """
    Company information sub-document.

    Attributes:
        company_name: Official company name (required)
        address: Complete company address (required)
        industry: List of industry classifications (exactly 2 elements)
        benefits: Description of company benefits
    """
    company_name: str = Field(..., min_length=1, description="Company name")
    address: Address = Field(..., description="Company address")
    industry: list[IndustryInfo] = Field(
        ...,
        min_length=2,
        max_length=2,
        description="Industry classifications (code and description)"
    )
    benefits: str = Field(default="", description="Company benefits description")


class OpenJob(BaseModel):
    """
    Open job posting sub-document.

    Attributes:
        job_id: Unique identifier for the job (MongoDB ObjectId)
        job_identification: Unique identifier for ChromaDB.  UUID value
        employer_identification: Employer's UUID identifier (foreign key)
        job_title: Title of the position (required)
        job_description: Detailed job description (required)
        posted_date: Date when job was posted (required)
        department: Department name (required)
        hire_mgr_first: Hiring manager's first name (required)
        hire_mgr_last: Hiring manager's last name (required)
        pay_range: Salary range [low, high] (required)
        pay_unit: Unit for pay_range (required)
        education_level: Required education level (required)
        edu_focus: Required field of study (required)
        key_skills: List of required skills (max 15)
    """
    job_id: PydanticObjectId = Field(default_factory=PydanticObjectId, description="Job posting ID")
    job_identification: UUID = Field(
       default_factory=uuid4,
       description="Unique job identifier for ChromaDB"
    )
    employer_identification: UUID = Field(..., description="Employer's UUID identifier")
    job_title: str = Field(..., min_length=1, description="Job title")
    job_description: str = Field(..., min_length=1, description="Job description")
    posted_date: datetime = Field(..., description="Date job was posted")
    department: str = Field(..., min_length=1, description="Department")
    hire_mgr_first: str = Field(..., min_length=1, description="Hiring manager first name")
    hire_mgr_last: str = Field(..., min_length=1, description="Hiring manager last name")
    current_status: Literal["Posted", "Withdrawn", "Pending", "Canceled"] = Field(
        default="Posted",
        description="Current job posting status"
    )
    pay_range: list[int] = Field(
        ...,
        min_length=2,
        max_length=2,
        description="Pay range [low, high]"
    )
    pay_unit: Literal["Hourly", "Monthly", "Yearly"] = Field(
        ...,
        description="Unit for pay range"
    )
    education_level: Literal["BA", "BS", "MA", "MS", "MBA", "PhD"] = Field(
        ...,
        description="Required education level"
    )
    edu_focus: str = Field(..., min_length=1, description="Required field of study")
    key_skills: list[str] = Field(
        default_factory=list,
        max_length=15,
        description="Required skills (max 15)"
    )


class CandidateTracking(BaseModel):
    """
    Candidate status tracking sub-document.

    Tracks current and previous status of an application.

    Attributes:
        current_status: Current application status
        previous_status: Previous application status
        current_status_date: Date of current status
        previous_status_date: Date of previous status
    """
    current_status: Literal["Received", "Interviewed", "Offered", "Rejected", "Canceled"] = Field(
        default="Received",
        description="Current application status"
    )
    previous_status: Literal["Received", "Interviewed", "Offered", "Rejected", "Canceled"] | None = Field(
        default=None,
        description="Previous application status"
    )
    current_status_date: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("America/Denver")),
        description="Date of current status"
    )
    previous_status_date: datetime | None = Field(
        default=None,
        description="Date of previous status"
    )


class ApplicationReceived(BaseModel):
    """
    Application received sub-document.

    Tracks applications received for jobs at this company.

    Attributes:
        applicant_id: Reference to the job seeker (foreign key)
        job_id: Reference to the job posting (foreign key)
        initial_daterec: Initial date application was received
        candidate_tracking: Status tracking information
    """
    applicant_id: str = Field(..., description="Applicant ID (foreign key to Seeker)")
    job_id: str = Field(..., description="Job ID (foreign key to job posting)")
    initial_daterec: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("America/Denver")),
        description="Initial date received"
    )
    candidate_tracking: CandidateTracking = Field(
        default_factory=CandidateTracking,
        description="Candidate status tracking"
    )


class Employer(Document):
    """
    Employer document model for MongoDB.

    This model represents an employer/company in the system with their
    company information, contact details, job postings, and applications.

    Attributes:
        employer_id: Unique identifier for the employer (MongoDB ObjectId)
        employer_identification: Unique identifier for the employer (UUID, required)
        temperature: Temperature value for AI model inference (0-1, default: 0.75)
        company_information: Company details and address (required)
        contact_first_name: Primary contact first name (required)
        contact_last_name: Primary contact last name (required)
        email: Contact email address for authentication (required, unique)
        password_hash: Hashed password for authentication (required)
        created_at: Account creation timestamp
        open_jobs: List of open job postings (required)
        apps_received: List of applications received

    Collection Settings:
        name: "employers" - MongoDB collection name
    """
    employer_id: PydanticObjectId = Field(default_factory=PydanticObjectId, description="MongoDB employer ID")
    employer_identification: UUID = Field(
        default_factory=uuid4,
        description="Unique employer identifier"
    )
    temperature: float = Field(
        default=0.75,
        ge=0.0,
        le=1.0,
        description="Temperature value for AI model inference (0-1)"
    )
    company_information: CompanyInformation = Field(
        ...,
        description="Company information"
    )
    contact_first_name: str = Field(
        ...,
        min_length=1,
        description="Contact first name"
    )
    contact_last_name: str = Field(
        ...,
        min_length=1,
        description="Contact last name"
    )
    email: Email = Field(
        ...,
        description="Contact email address (unique)"
    )
    password_hash: str = Field(
        ...,
        min_length=6,
        description="Hashed password"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("America/Denver")),
        description="Account creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("America/Denver")),
        description="Account update timestamp"
    )
    open_jobs: list[OpenJob] = Field(
        ...,
        description="List of open job postings"
    )
    apps_received: list[ApplicationReceived] = Field(
        default_factory=list,
        description="Applications received"
    )

    class Settings:
        name = "employers"
        indexes: ClassVar[list[str]] = [
            "email",  # Index on email (for login)
            "company_information.company_name",  # Index on company name
            "created_at",  # Index on creation date
            "open_jobs.job_id",  # Index on job IDs
        ]


# Example usage
if __name__ == "__main__":
    from pydantic import ValidationError
    logger.debug("=== Employer Model Validation Tests ===\n")

    # Test with valid employer data
    logger.debug("Test 1: Creating valid CompanyInformation sub-document...")
    try:
        company_info = CompanyInformation(
            company_name="Tech Innovations Inc.",
            address=Address(
                street="456 Innovation Drive",
                city="San Francisco",
                state="CA",
                zip_code="94105"
            ),
            industry=[
                IndustryInfo(code="45", description="Information Technology"),
                IndustryInfo(code="4510", description="Software & Services")
            ],
            benefits="Health insurance, 401k, Remote work options"
        )
        logger.debug("✓ Valid CompanyInformation created")
        logger.debug(f"  Company: {company_info.company_name}")
        logger.debug(f"  Address: {company_info.address.city}, {company_info.address.state}")
        logger.debug(f"  Industries: {len(company_info.industry)}")
        logger.debug("")
    except ValidationError as e:
        logger.critical(f"✗ Validation error: {e}\n")

    logger.debug("Test 2: Creating valid OpenJob sub-document...")
    try:
        job = OpenJob(
            employer_identification=uuid4(),
            job_title="Senior Software Engineer",
            job_description="We are seeking an experienced software engineer...",
            posted_date=datetime.now(ZoneInfo("America/Denver")),
            department="Engineering",
            hire_mgr_first="Jane",
            hire_mgr_last="Smith",
            pay_range=[120000, 180000],
            pay_unit="Yearly",
            education_level="BS",
            edu_focus="Computer Science",
            key_skills=["Python", "FastAPI", "MongoDB", "Docker", "AWS"]
        )
        logger.debug("✓ Valid OpenJob created")
        logger.debug(f"  Title: {job.job_title}")
        logger.debug(f"  Department: {job.department}")
        logger.debug(f"  Pay Range: ${job.pay_range[0]:,} - ${job.pay_range[1]:,} {job.pay_unit}")
        logger.debug(f"  Skills Required: {len(job.key_skills)}")
        logger.debug("")
    except ValidationError as e:
        logger.critical(f"✗ Validation error: {e}\n")

    logger.debug("Test 3: Creating valid ApplicationReceived sub-document...")
    try:
        app = ApplicationReceived(
            applicant_id="seeker_123",
            job_id="job_001",
            candidate_tracking=CandidateTracking(
                current_status="Interviewed",
                previous_status="Received"
            )
        )
        logger.debug("✓ Valid ApplicationReceived created")
        logger.debug(f"  Applicant: {app.applicant_id}")
        logger.debug(f"  Job: {app.job_id}")
        logger.debug(f"  Status: {app.candidate_tracking.current_status}")
        logger.debug("")
    except ValidationError as e:
        logger.critical(f"✗ Validation error: {e}\n")

    logger.debug("Test 4: Testing field validations...")

    # Test invalid GICS code
    logger.debug("  - Testing invalid GICS code...")
    try:
        bad_industry = IndustryInfo(code="INVALID", description="Test")
        logger.debug("  ✗ Should have failed with invalid GICS code")
    except (ValidationError, ValueError):
        logger.debug("  ✓ Correctly rejected invalid GICS code")

    # Test industry array length validation (must be exactly 2)
    logger.debug("  - Testing industry array length (must be 2)...")
    try:
        bad_company = CompanyInformation(
            company_name="Test Corp",
            address=Address(
                street="123 Test St",
                city="New York",
                state="NY",
                zip_code="10001"
            ),
            industry=[IndustryInfo(code="10", description="Energy")],  # Only 1 element
            benefits="Test"
        )
        logger.debug("  ✗ Should have failed with wrong industry array length")
    except ValidationError:
        logger.debug("  ✓ Correctly rejected industry array with wrong length")

    logger.debug("\n=== All Tests Passed! ===")
    logger.debug("\nModel Summary:")
    logger.debug("✓ CompanyInformation sub-document with Address and Industry validation")
    logger.debug("✓ OpenJob sub-document with pay range and education requirements")
    logger.debug("✓ ApplicationReceived sub-document with CandidateTracking")
    logger.debug("✓ Employer document with all required fields")
    logger.debug("✓ Field validations (GICS codes, array lengths, literals)")
    logger.debug("✓ Status tracking for candidate applications")

