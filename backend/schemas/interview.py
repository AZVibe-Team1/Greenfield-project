"""
Interview MongoDB Model

This module defines the Interview document model for MongoDB using Beanie ODM.
It tracks interview scheduling between employers and job seekers.
"""

from datetime import datetime
from typing import ClassVar, Literal
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field

from backend.utils.validators import Email


class InterviewDetails(BaseModel):
    """
    Interview scheduling details sub-document.
    
    Attributes:
        interview_type: Type of interview (In-person, Video, Phone)
        scheduled_date: Date of the interview
        scheduled_time: Time of the interview (e.g., "10:00 AM")
        duration_minutes: Expected duration in minutes
        location_or_link: Physical location or video call link
        interviewer_name: Name of the person conducting the interview
        interviewer_email: Email of the interviewer (optional)
        notes: Additional notes or instructions
    """
    interview_type: Literal["In-person", "Video", "Phone"] = Field(
        ...,
        description="Type of interview"
    )
    scheduled_date: datetime = Field(
        ...,
        description="Interview date"
    )
    scheduled_time: str = Field(
        ...,
        description="Interview time (e.g., '10:00 AM')"
    )
    duration_minutes: int = Field(
        default=60,
        ge=15,
        le=480,
        description="Interview duration in minutes (15-480)"
    )
    location_or_link: str = Field(
        ...,
        min_length=1,
        description="Physical location or video call link"
    )
    interviewer_name: str = Field(
        ...,
        min_length=1,
        description="Name of interviewer"
    )
    interviewer_email: Email | None = Field(
        default=None,
        description="Interviewer's email address"
    )
    notes: str = Field(
        default="",
        description="Additional notes or instructions"
    )


class Interview(Document):
    """
    Interview document model for MongoDB.
    
    This model represents a scheduled interview between an employer and job seeker
    for a specific job posting.
    
    Attributes:
        interview_id: Unique identifier for the interview (MongoDB ObjectId)
        interview_identification: Unique identifier (UUID, required)
        job_id: Reference to the job posting (foreign key)
        job_identification: Job UUID from employer schema
        employer_id: Reference to the employer (foreign key)
        employer_identification: Employer UUID
        seeker_id: Reference to the job seeker (foreign key)
        seeker_identification: Seeker UUID
        interview_details: Scheduling and logistics information
        status: Current interview status
        created_at: When interview was scheduled
        updated_at: Last update timestamp
        scheduled_by: User ID who scheduled the interview
        cancellation_reason: Reason if interview was cancelled (optional)
        n8n_notification_sent: Whether email notification was sent
        n8n_notification_sent_at: When notification was sent
    
    Collection Settings:
        name: "interviews" - MongoDB collection name
    """
    interview_id: PydanticObjectId = Field(
        default_factory=PydanticObjectId,
        description="MongoDB interview ID"
    )
    interview_identification: UUID = Field(
        default_factory=uuid4,
        description="Unique interview identifier"
    )
    
    # Foreign Keys
    job_id: str = Field(
        ...,
        description="Job posting ID (ObjectId string)"
    )
    job_identification: UUID = Field(
        ...,
        description="Job UUID from employer schema"
    )
    job_title: str = Field(
        ...,
        description="Job title (denormalized for queries)"
    )
    
    employer_id: str = Field(
        ...,
        description="Employer ID (ObjectId string)"
    )
    employer_identification: UUID = Field(
        ...,
        description="Employer UUID"
    )
    company_name: str = Field(
        ...,
        description="Company name (denormalized for queries)"
    )
    
    seeker_id: str = Field(
        ...,
        description="Job seeker ID (ObjectId string)"
    )
    seeker_identification: UUID = Field(
        ...,
        description="Seeker UUID"
    )
    seeker_name: str = Field(
        ...,
        description="Seeker full name (denormalized for queries)"
    )
    seeker_email: Email = Field(
        ...,
        description="Seeker email (denormalized for n8n)"
    )
    
    # Interview Details
    interview_details: InterviewDetails = Field(
        ...,
        description="Interview scheduling information"
    )
    
    # Status Tracking
    status: Literal[
        "Scheduled",
        "Confirmed", 
        "Rescheduled",
        "Completed",
        "Cancelled",
        "No-Show"
    ] = Field(
        default="Scheduled",
        description="Current interview status"
    )
    
    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("America/Denver")),
        description="When interview was created"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(ZoneInfo("America/Denver")),
        description="Last update timestamp"
    )
    
    # Additional Fields
    scheduled_by: str = Field(
        ...,
        description="User ID who scheduled the interview"
    )
    cancellation_reason: str | None = Field(
        default=None,
        description="Reason for cancellation (if applicable)"
    )
    
    # n8n Integration Fields
    n8n_notification_sent: bool = Field(
        default=False,
        description="Whether n8n notification was sent"
    )
    n8n_notification_sent_at: datetime | None = Field(
        default=None,
        description="When notification was sent"
    )
    
    class Settings:
        name = "interviews"
        indexes: ClassVar[list[str]] = [
            "seeker_id",  # Index for seeker queries
            "employer_id",  # Index for employer queries
            "job_id",  # Index for job-specific queries
            "status",  # Index for status filtering
            "interview_details.scheduled_date",  # Index for date range queries
            "created_at",  # Index for sorting by creation date
        ]

    def update_timestamp(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now(ZoneInfo("America/Denver"))

