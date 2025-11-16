"""Interview scheduling API routes."""

from datetime import datetime
from typing import Literal

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from pydantic import BaseModel, Field

from backend.core.security import get_current_user_id, get_current_user_role
from backend.schemas.interview import Interview, InterviewDetails
from backend.services.interview_services import InterviewService
from backend.services.n8n_service import n8n_service


router = APIRouter(prefix="/interviews", tags=["Interviews"])


class ScheduleInterviewRequest(BaseModel):
    """Request model for scheduling an interview."""
    job_id: str = Field(..., description="Job posting ID")
    seeker_id: str = Field(..., description="Job seeker ID")
    interview_type: Literal["In-person", "Video", "Phone"] = Field(..., description="Type of interview")
    scheduled_date: datetime = Field(..., description="Interview date")
    scheduled_time: str = Field(..., description="Interview time")
    duration_minutes: int = Field(default=60, description="Duration in minutes")
    location_or_link: str = Field(..., description="Location or video link")
    interviewer_name: str = Field(..., description="Interviewer name")
    interviewer_email: str | None = Field(None, description="Interviewer email")
    notes: str = Field(default="", description="Additional notes")


class InterviewResponse(BaseModel):
    """Response model for interview data."""
    interview_id: str
    job_id: str
    job_title: str
    employer_id: str
    company_name: str
    seeker_id: str
    seeker_name: str
    seeker_email: str
    interview_type: str
    scheduled_date: datetime
    scheduled_time: str
    duration_minutes: int
    location_or_link: str
    interviewer_name: str
    status: str
    created_at: datetime
    n8n_notification_sent: bool


class UpdateInterviewStatusRequest(BaseModel):
    """Request model for updating interview status."""
    status: str = Field(..., description="New status")
    cancellation_reason: str | None = Field(None, description="Cancellation reason")


@router.post("/", response_model=InterviewResponse, status_code=status.HTTP_201_CREATED)
async def schedule_interview(
    request: ScheduleInterviewRequest,
    user_id: str = Depends(get_current_user_id),
    role: str = Depends(get_current_user_role)
):
    """
    Schedule a new interview and send notification via n8n.
    
    **Employer only endpoint**
    
    The interview is created in MongoDB first, then n8n is triggered to send
    the email notification. If n8n fails, the interview is still created
    (graceful degradation).
    """
    # Verify user is employer
    if role != "employer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employers can schedule interviews"
        )
    
    try:
        interview_details = InterviewDetails(
            interview_type=request.interview_type,
            scheduled_date=request.scheduled_date,
            scheduled_time=request.scheduled_time,
            duration_minutes=request.duration_minutes,
            location_or_link=request.location_or_link,
            interviewer_name=request.interviewer_name,
            interviewer_email=request.interviewer_email,
            notes=request.notes
        )
        
        # 1. Create interview in MongoDB
        interview = await InterviewService.create_interview(
            job_id=request.job_id,
            employer_id=user_id,
            seeker_id=request.seeker_id,
            interview_details=interview_details,
            scheduled_by=user_id
        )
        
        logger.info(f"Interview {interview.interview_id} created successfully")
        
        # 2. Trigger n8n notification (non-blocking - graceful failure)
        notification_sent = False
        try:
            success, message = await n8n_service.trigger_interview_notification(
                seeker_email=interview.seeker_email,
                seeker_name=interview.seeker_name,
                job_title=interview.job_title,
                company_name=interview.company_name,
                interview_date=interview.interview_details.scheduled_date,
                interview_time=interview.interview_details.scheduled_time,
                interview_type=interview.interview_details.interview_type,
                location_or_link=interview.interview_details.location_or_link,
                notes=interview.interview_details.notes
            )
            
            if success:
                # Mark notification as sent in database
                await InterviewService.mark_notification_sent(str(interview.interview_id))
                notification_sent = True
                logger.info(f"Email notification sent for interview {interview.interview_id}")
            else:
                logger.warning(
                    f"Failed to send email notification for interview {interview.interview_id}: {message}"
                )
                # Interview is still created - email failure is logged but not blocking
                
        except Exception as e:
            # Catch any unexpected errors from n8n service
            logger.error(f"Error triggering n8n notification: {e}")
            # Continue - interview is created, email just failed
        
        # 3. Return success response (even if email failed)
        return InterviewResponse(
            interview_id=str(interview.interview_id),
            job_id=interview.job_id,
            job_title=interview.job_title,
            employer_id=interview.employer_id,
            company_name=interview.company_name,
            seeker_id=interview.seeker_id,
            seeker_name=interview.seeker_name,
            seeker_email=interview.seeker_email,
            interview_type=interview.interview_details.interview_type,
            scheduled_date=interview.interview_details.scheduled_date,
            scheduled_time=interview.interview_details.scheduled_time,
            duration_minutes=interview.interview_details.duration_minutes,
            location_or_link=interview.interview_details.location_or_link,
            interviewer_name=interview.interview_details.interviewer_name,
            status=interview.status,
            created_at=interview.created_at,
            n8n_notification_sent=notification_sent  # This reflects actual status
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error scheduling interview: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to schedule interview"
        )


@router.get("/seeker/me", response_model=list[InterviewResponse])
async def get_my_interviews_seeker(
    user_id: str = Depends(get_current_user_id),
    role: str = Depends(get_current_user_role)
):
    """
    Get all interviews for current seeker.
    
    **Seeker only endpoint**
    """
    if role != "seeker":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only seekers can access this endpoint"
        )
    
    interviews = await InterviewService.get_interviews_by_seeker(user_id)
    return [
        InterviewResponse(
            interview_id=str(i.interview_id),
            job_id=i.job_id,
            job_title=i.job_title,
            employer_id=i.employer_id,
            company_name=i.company_name,
            seeker_id=i.seeker_id,
            seeker_name=i.seeker_name,
            seeker_email=i.seeker_email,
            interview_type=i.interview_details.interview_type,
            scheduled_date=i.interview_details.scheduled_date,
            scheduled_time=i.interview_details.scheduled_time,
            duration_minutes=i.interview_details.duration_minutes,
            location_or_link=i.interview_details.location_or_link,
            interviewer_name=i.interview_details.interviewer_name,
            status=i.status,
            created_at=i.created_at,
            n8n_notification_sent=i.n8n_notification_sent
        )
        for i in interviews
    ]


@router.get("/employer/me", response_model=list[InterviewResponse])
async def get_my_interviews_employer(
    user_id: str = Depends(get_current_user_id),
    role: str = Depends(get_current_user_role)
):
    """
    Get all interviews for current employer.
    
    **Employer only endpoint**
    """
    if role != "employer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employers can access this endpoint"
        )
    
    interviews = await InterviewService.get_interviews_by_employer(user_id)
    return [
        InterviewResponse(
            interview_id=str(i.interview_id),
            job_id=i.job_id,
            job_title=i.job_title,
            employer_id=i.employer_id,
            company_name=i.company_name,
            seeker_id=i.seeker_id,
            seeker_name=i.seeker_name,
            seeker_email=i.seeker_email,
            interview_type=i.interview_details.interview_type,
            scheduled_date=i.interview_details.scheduled_date,
            scheduled_time=i.interview_details.scheduled_time,
            duration_minutes=i.interview_details.duration_minutes,
            location_or_link=i.interview_details.location_or_link,
            interviewer_name=i.interview_details.interviewer_name,
            status=i.status,
            created_at=i.created_at,
            n8n_notification_sent=i.n8n_notification_sent
        )
        for i in interviews
    ]


@router.get("/job/{job_id}", response_model=list[InterviewResponse])
async def get_interviews_for_job(
    job_id: str,
    user_id: str = Depends(get_current_user_id),
    role: str = Depends(get_current_user_role)
):
    """
    Get all interviews for a specific job.
    
    **Employer only endpoint**
    """
    if role != "employer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employers can access this endpoint"
        )
    
    interviews = await InterviewService.get_interviews_by_job(job_id)
    
    # Verify employer owns this job
    if interviews and interviews[0].employer_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view these interviews"
        )
    
    return [
        InterviewResponse(
            interview_id=str(i.interview_id),
            job_id=i.job_id,
            job_title=i.job_title,
            employer_id=i.employer_id,
            company_name=i.company_name,
            seeker_id=i.seeker_id,
            seeker_name=i.seeker_name,
            seeker_email=i.seeker_email,
            interview_type=i.interview_details.interview_type,
            scheduled_date=i.interview_details.scheduled_date,
            scheduled_time=i.interview_details.scheduled_time,
            duration_minutes=i.interview_details.duration_minutes,
            location_or_link=i.interview_details.location_or_link,
            interviewer_name=i.interview_details.interviewer_name,
            status=i.status,
            created_at=i.created_at,
            n8n_notification_sent=i.n8n_notification_sent
        )
        for i in interviews
    ]


@router.patch("/{interview_id}/status", response_model=InterviewResponse)
async def update_interview_status(
    interview_id: str,
    request: UpdateInterviewStatusRequest,
    user_id: str = Depends(get_current_user_id),
    role: str = Depends(get_current_user_role)
):
    """Update interview status."""
    try:
        interview = await InterviewService.update_interview_status(
            interview_id=interview_id,
            status=request.status,
            cancellation_reason=request.cancellation_reason
        )
        
        return InterviewResponse(
            interview_id=str(interview.interview_id),
            job_id=interview.job_id,
            job_title=interview.job_title,
            employer_id=interview.employer_id,
            company_name=interview.company_name,
            seeker_id=interview.seeker_id,
            seeker_name=interview.seeker_name,
            seeker_email=interview.seeker_email,
            interview_type=interview.interview_details.interview_type,
            scheduled_date=interview.interview_details.scheduled_date,
            scheduled_time=interview.interview_details.scheduled_time,
            duration_minutes=interview.interview_details.duration_minutes,
            location_or_link=interview.interview_details.location_or_link,
            interviewer_name=interview.interview_details.interviewer_name,
            status=interview.status,
            created_at=interview.created_at,
            n8n_notification_sent=interview.n8n_notification_sent
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/n8n/status")
async def check_n8n_status(
    user_id: str = Depends(get_current_user_id),
    role: str = Depends(get_current_user_role)
):
    """
    Check n8n service connection status.
    
    Returns connection status for monitoring/debugging.
    """
    if role != "employer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employers can check n8n status"
        )
    
    status_info = await n8n_service.check_connection()
    return status_info


@router.post("/{interview_id}/retry-notification")
async def retry_notification(
    interview_id: str,
    user_id: str = Depends(get_current_user_id),
    role: str = Depends(get_current_user_role)
):
    """
    Retry sending email notification for an interview.
    
    Useful when n8n was down during initial scheduling.
    """
    if role != "employer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employers can retry notifications"
        )
    
    try:
        # Get interview
        interview = await Interview.get(PydanticObjectId(interview_id))
        if not interview:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview not found"
            )
        
        # Verify employer owns this interview
        if interview.employer_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this interview"
            )
        
        # Retry notification
        success, message = await n8n_service.trigger_interview_notification(
            seeker_email=interview.seeker_email,
            seeker_name=interview.seeker_name,
            job_title=interview.job_title,
            company_name=interview.company_name,
            interview_date=interview.interview_details.scheduled_date,
            interview_time=interview.interview_details.scheduled_time,
            interview_type=interview.interview_details.interview_type,
            location_or_link=interview.interview_details.location_or_link,
            notes=interview.interview_details.notes
        )
        
        if success:
            await InterviewService.mark_notification_sent(interview_id)
            return {"success": True, "message": "Notification sent successfully"}
        else:
            return {"success": False, "message": message}
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrying notification: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retry notification"
        )

