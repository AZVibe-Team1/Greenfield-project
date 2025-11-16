"""Interview business logic and database operations."""

from datetime import datetime
from zoneinfo import ZoneInfo

from beanie import PydanticObjectId
from loguru import logger

from backend.schemas.employer import Employer
from backend.schemas.interview import Interview, InterviewDetails
from backend.schemas.seeker import Seeker


class InterviewService:
    """Service for interview management."""
    
    @staticmethod
    async def create_interview(
        job_id: str,
        employer_id: str,
        seeker_id: str,
        interview_details: InterviewDetails,
        scheduled_by: str
    ) -> Interview:
        """
        Create a new interview.
        
        Args:
            job_id: Job posting ID (ObjectId string)
            employer_id: Employer ID (ObjectId string)
            seeker_id: Seeker ID (ObjectId string)
            interview_details: Interview scheduling details
            scheduled_by: User ID who scheduled the interview
        
        Returns:
            Created Interview document
        
        Raises:
            ValueError: If employer, seeker, or job not found
        """
        # Fetch related data for denormalization
        employer = await Employer.get(PydanticObjectId(employer_id))
        if not employer:
            error_msg = f"Employer {employer_id} not found"
            raise ValueError(error_msg)

        seeker = await Seeker.get(PydanticObjectId(seeker_id))
        if not seeker:
            error_msg = f"Seeker {seeker_id} not found"
            raise ValueError(error_msg)

        # Find job in employer's open_jobs
        job = next((j for j in employer.open_jobs if str(j.job_id) == job_id), None)
        if not job:
            error_msg = f"Job {job_id} not found"
            raise ValueError(error_msg)
        
        # Create interview
        interview = Interview(
            job_id=job_id,
            job_identification=job.job_identification,
            job_title=job.job_title,
            employer_id=employer_id,
            employer_identification=employer.employer_identification,
            company_name=employer.company_information.company_name,
            seeker_id=seeker_id,
            seeker_identification=seeker.seeker_identification,
            seeker_name=f"{seeker.information.first_name} {seeker.information.last_name}",
            seeker_email=seeker.information.email,
            interview_details=interview_details,
            scheduled_by=scheduled_by
        )
        
        await interview.insert()
        logger.info(f"Created interview {interview.interview_id} for job {job_id}")
        return interview
    
    @staticmethod
    async def get_interviews_by_seeker(seeker_id: str) -> list[Interview]:
        """
        Get all interviews for a seeker.

        Args:
            seeker_id: Seeker ID (ObjectId string)

        Returns:
            List of Interview documents sorted by creation date (newest first)
        """
        return await Interview.find(
            Interview.seeker_id == seeker_id
        ).sort("-created_at").to_list()
    
    @staticmethod
    async def get_interviews_by_employer(employer_id: str) -> list[Interview]:
        """
        Get all interviews for an employer.

        Args:
            employer_id: Employer ID (ObjectId string)

        Returns:
            List of Interview documents sorted by creation date (newest first)
        """
        return await Interview.find(
            Interview.employer_id == employer_id
        ).sort("-created_at").to_list()
    
    @staticmethod
    async def get_interviews_by_job(job_id: str) -> list[Interview]:
        """
        Get all interviews for a job.

        Args:
            job_id: Job posting ID (ObjectId string)

        Returns:
            List of Interview documents sorted by scheduled date
        """
        return await Interview.find(
            Interview.job_id == job_id
        ).sort("-interview_details.scheduled_date").to_list()
    
    @staticmethod
    async def get_interview_by_id(interview_id: str) -> Interview | None:
        """
        Get an interview by ID.
        
        Args:
            interview_id: Interview ID (ObjectId string)
        
        Returns:
            Interview document or None if not found
        """
        try:
            return await Interview.get(PydanticObjectId(interview_id))
        except Exception as e:
            logger.error(f"Error fetching interview {interview_id}: {e}")
            return None
    
    @staticmethod
    async def update_interview_status(
        interview_id: str,
        status: str,
        cancellation_reason: str | None = None
    ) -> Interview:
        """
        Update interview status.

        Args:
            interview_id: Interview ID (ObjectId string)
            status: New status
            cancellation_reason: Reason for cancellation (if applicable)

        Returns:
            Updated Interview document

        Raises:
            ValueError: If interview not found
        """
        interview = await Interview.get(PydanticObjectId(interview_id))
        if not interview:
            error_msg = f"Interview {interview_id} not found"
            raise ValueError(error_msg)

        # Type assertion to satisfy type checker
        interview.status = status  # type: ignore[assignment]
        if cancellation_reason:
            interview.cancellation_reason = cancellation_reason
        interview.update_timestamp()

        await interview.save()
        logger.info(f"Updated interview {interview_id} status to {status}")
        return interview
    
    @staticmethod
    async def mark_notification_sent(interview_id: str) -> Interview:
        """
        Mark that n8n notification was sent.

        Args:
            interview_id: Interview ID (ObjectId string)

        Returns:
            Updated Interview document

        Raises:
            ValueError: If interview not found
        """
        interview = await Interview.get(PydanticObjectId(interview_id))
        if not interview:
            error_msg = f"Interview {interview_id} not found"
            raise ValueError(error_msg)

        interview.n8n_notification_sent = True
        interview.n8n_notification_sent_at = datetime.now(ZoneInfo("America/Denver"))
        interview.update_timestamp()

        await interview.save()
        logger.info(f"Marked notification sent for interview {interview_id}")
        return interview

