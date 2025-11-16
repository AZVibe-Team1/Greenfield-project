"""
Employer API routes.

Handles employer profile management, job posting, and application management.
"""
from datetime import datetime
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from backend.ai.chains.candidate_matching_service import get_candidate_matching_service
from backend.core.security import get_current_user_id, get_current_user_role
from backend.db.employer_db_ops import EmployerCRUD
from backend.db.seeker_db_ops import SeekerCRUD
from backend.services.employer_services import EmployerService
from backend.services.n8n_service import get_n8n_service


router = APIRouter(prefix="/employers", tags=["Employers"])


# Response Models
class EmployerProfileResponse(BaseModel):
    """Employer profile response."""
    id: str
    company_name: str
    contact_first_name: str
    contact_last_name: str
    address: dict[str, str]
    industry: list[dict[str, str]]
    benefits: str
    open_jobs: list[dict[str, Any]]
    apps_received: list[dict[str, Any]]


class CreateJobRequest(BaseModel):
    """Create job request."""
    job_title: str = Field(..., min_length=1)
    job_description: str = Field(..., min_length=1)
    department: str = Field(..., min_length=1)
    hire_mgr_first: str = Field(..., min_length=1)
    hire_mgr_last: str = Field(..., min_length=1)
    pay_range: list[int] = Field(..., min_length=2, max_length=2)
    pay_unit: str
    education_level: str
    edu_focus: str
    key_skills: list[str] | None = None


class UpdateJobRequest(BaseModel):
    """Update job request."""
    job_title: str | None = None
    job_description: str | None = None
    department: str | None = None
    hire_mgr_first: str | None = None
    hire_mgr_last: str | None = None
    pay_range: list[int] | None = None
    pay_unit: str | None = None
    education_level: str | None = None
    edu_focus: str | None = None
    key_skills: list[str] | None = None
    current_status: str | None = None


class JobResponse(BaseModel):
    """Job response."""
    job_id: str
    job_title: str
    job_description: str
    posted_date: str
    department: str
    hire_mgr_first: str
    hire_mgr_last: str
    current_status: str
    pay_range: list[int]
    pay_unit: str
    education_level: str
    edu_focus: str
    key_skills: list[str]


class UpdateEmployerRequest(BaseModel):
    """Update employer profile request."""
    contact_first_name: str | None = None
    contact_last_name: str | None = None
    benefits: str | None = None


class ScoreBreakdown(BaseModel):
    """Match score breakdown."""
    skills_score: float
    education_score: float
    pay_score: float
    experience_score: float
    reasoning: str


class CandidateRecommendationResponse(BaseModel):
    """AI-powered candidate recommendation response."""
    seeker_id: str
    first_name: str
    last_name: str
    email: str
    match_score: float
    score_breakdown: ScoreBreakdown
    has_applied: bool
    resume_preview: str
    key_skills: list[str]
    education_level: str
    edu_focus: str
    pay_range: list[int]
    pay_unit: str
    phone: str
    address: dict[str, str]


class ScheduleInterviewRequest(BaseModel):
    """Schedule interview request."""
    interview_date: datetime = Field(..., description="Date of the interview")
    interview_time: str = Field(..., min_length=1, description="Time of the interview (e.g., '14:00')")
    interview_type: Literal["In-person", "Video", "Phone"] = Field(..., description="Type of interview")
    location_or_link: str = Field(..., min_length=1, description="Location address or video call link")
    notes: str | None = Field(None, description="Optional notes about the interview")


class N8nStatusResponse(BaseModel):
    """n8n service status response."""
    status: Literal["connected", "disconnected"]
    message: str


# Dependency to verify employer role
async def verify_employer_role(role: str = Depends(get_current_user_role)) -> str:
    """Verify that the current user is an employer."""
    if role != "employer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Employer role required"
        )
    return role


@router.get("/me", response_model=EmployerProfileResponse)
async def get_my_profile(
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_employer_role)
):
    """
    Get current employer's profile.

    Returns:
        Employer profile information
    """
    def raise_not_found() -> None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employer profile not found"
        )

    try:
        employer = await EmployerCRUD.get_employer_by_id(user_id)
        if employer is None:
            raise_not_found()

        assert employer is not None  # Type narrowing

        return EmployerProfileResponse(
            id=str(employer.id),
            company_name=employer.company_information.company_name,
            contact_first_name=employer.contact_first_name,
            contact_last_name=employer.contact_last_name,
            address={
                "street": employer.company_information.address.street,
                "city": employer.company_information.address.city,
                "state": employer.company_information.address.state,
                "zip_code": employer.company_information.address.zip_code
            },
            industry=[
                {"code": ind.code, "description": ind.description}
                for ind in employer.company_information.industry
            ],
            benefits=employer.company_information.benefits,
            open_jobs=[
                {
                    "job_id": str(job.job_id),
                    "job_title": job.job_title,
                    "job_description": job.job_description,
                    "posted_date": job.posted_date.isoformat(),
                    "department": job.department,
                    "hire_mgr_first": job.hire_mgr_first,
                    "hire_mgr_last": job.hire_mgr_last,
                    "current_status": job.current_status,
                    "pay_range": job.pay_range,
                    "pay_unit": job.pay_unit,
                    "education_level": job.education_level,
                    "edu_focus": job.edu_focus,
                    "key_skills": job.key_skills
                }
                for job in employer.open_jobs
            ],
            apps_received=[
                {
                    "applicant_id": app.applicant_id,
                    "job_id": app.job_id,
                    "initial_daterec": app.initial_daterec.isoformat(),
                    "current_status": app.candidate_tracking.current_status
                }
                for app in employer.apps_received
            ]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get profile: {e!s}"
        ) from e


@router.put("/me")
async def update_my_profile(
    request: UpdateEmployerRequest,
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_employer_role)
):
    """
    Update current employer's profile.

    Args:
        request: Fields to update

    Returns:
        Success message
    """
    def raise_update_failed() -> None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )

    try:
        # Build update dictionary (only include non-None fields)
        update_data = {}

        if request.contact_first_name is not None:
            update_data["contact_first_name"] = request.contact_first_name
        if request.contact_last_name is not None:
            update_data["contact_last_name"] = request.contact_last_name
        if request.benefits is not None:
            update_data["company_information.benefits"] = request.benefits

        updated_employer = await EmployerService.update_employer(user_id, update_data)

        if not updated_employer:
            raise_update_failed()
        else:
            return {"message": "Profile updated successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update profile: {e!s}"
        ) from e


@router.post("/jobs", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    request: CreateJobRequest,
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_employer_role)
):
    """
    Create a new job posting.

    Args:
        request: Job posting data

    Returns:
        Created job information
    """
    def raise_creation_failed() -> None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create job"
        )

    try:
        updated_employer = await EmployerService.create_job(
            employer_id=user_id,
            job_title=request.job_title,
            job_description=request.job_description,
            department=request.department,
            hire_mgr_first=request.hire_mgr_first,
            hire_mgr_last=request.hire_mgr_last,
            pay_range=request.pay_range,
            pay_unit=request.pay_unit,
            education_level=request.education_level,
            edu_focus=request.edu_focus,
            key_skills=request.key_skills
        )

        if not updated_employer:
            raise_creation_failed()

        assert updated_employer is not None  # Type narrowing

        # Get the last added job
        new_job = updated_employer.open_jobs[-1]

        return JobResponse(
            job_id=str(new_job.job_id),
            job_title=new_job.job_title,
            job_description=new_job.job_description,
            posted_date=new_job.posted_date.isoformat(),
            department=new_job.department,
            hire_mgr_first=new_job.hire_mgr_first,
            hire_mgr_last=new_job.hire_mgr_last,
            current_status=new_job.current_status,
            pay_range=new_job.pay_range,
            pay_unit=new_job.pay_unit,
            education_level=new_job.education_level,
            edu_focus=new_job.edu_focus,
            key_skills=new_job.key_skills
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create job: {e!s}"
        ) from e


@router.get("/jobs", response_model=list[JobResponse])
async def get_my_jobs(
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_employer_role)
):
    """
    Get all jobs for current employer.

    Returns:
        List of jobs
    """
    def raise_employer_not_found() -> None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employer not found"
        )

    try:
        employer = await EmployerCRUD.get_employer_by_id(user_id)
        if not employer:
            raise_employer_not_found()

        assert employer is not None  # Type narrowing

        return [
            JobResponse(
                job_id=str(job.job_id),
                job_title=job.job_title,
                job_description=job.job_description,
                posted_date=job.posted_date.isoformat(),
                department=job.department,
                hire_mgr_first=job.hire_mgr_first,
                hire_mgr_last=job.hire_mgr_last,
                current_status=job.current_status,
                pay_range=job.pay_range,
                pay_unit=job.pay_unit,
                education_level=job.education_level,
                edu_focus=job.edu_focus,
                key_skills=job.key_skills
            )
            for job in employer.open_jobs
        ]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get jobs: {e!s}"
        ) from e


@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_employer_role)
):
    """
    Get a specific job.

    Args:
        job_id: Job ID

    Returns:
        Job details
    """
    def raise_job_not_found() -> None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    def raise_employer_not_found() -> None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employer not found"
        )

    try:
        employer = await EmployerCRUD.get_employer_by_id(user_id)
        if not employer:
            raise_employer_not_found()

        assert employer is not None  # Type narrowing

        for job in employer.open_jobs:
            if str(job.job_id) == job_id:
                return JobResponse(
                    job_id=str(job.job_id),
                    job_title=job.job_title,
                    job_description=job.job_description,
                    posted_date=job.posted_date.isoformat(),
                    department=job.department,
                    hire_mgr_first=job.hire_mgr_first,
                    hire_mgr_last=job.hire_mgr_last,
                    current_status=job.current_status,
                    pay_range=job.pay_range,
                    pay_unit=job.pay_unit,
                    education_level=job.education_level,
                    edu_focus=job.edu_focus,
                    key_skills=job.key_skills
                )

        raise_job_not_found()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get job: {e!s}"
        ) from e


@router.put("/jobs/{job_id}")
async def update_job(
    job_id: str,
    request: UpdateJobRequest,
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_employer_role)
):
    """
    Update a job posting.

    Args:
        job_id: Job ID
        request: Fields to update

    Returns:
        Success message
    """
    def raise_job_not_found() -> None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    try:
        # Build update dictionary (only include non-None fields)
        update_data = {}

        if request.job_title is not None:
            update_data["job_title"] = request.job_title
        if request.job_description is not None:
            update_data["job_description"] = request.job_description
        if request.department is not None:
            update_data["department"] = request.department
        if request.hire_mgr_first is not None:
            update_data["hire_mgr_first"] = request.hire_mgr_first
        if request.hire_mgr_last is not None:
            update_data["hire_mgr_last"] = request.hire_mgr_last
        if request.pay_range is not None:
            update_data["pay_range"] = request.pay_range
        if request.pay_unit is not None:
            update_data["pay_unit"] = request.pay_unit
        if request.education_level is not None:
            update_data["education_level"] = request.education_level
        if request.edu_focus is not None:
            update_data["edu_focus"] = request.edu_focus
        if request.key_skills is not None:
            update_data["key_skills"] = request.key_skills
        if request.current_status is not None:
            update_data["current_status"] = request.current_status

        updated_employer = await EmployerService.modify_job(
            employer_id=user_id,
            job_id=job_id,
            update_data=update_data
        )

        if not updated_employer:
            raise_job_not_found()
        else:
            return {"message": "Job updated successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update job: {e!s}"
        ) from e


@router.delete("/jobs/{job_id}")
async def delete_job(
    job_id: str,
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_employer_role)
):
    """
    Delete a job posting.

    Args:
        job_id: Job ID

    Returns:
        Success message
    """
    def raise_employer_not_found() -> None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employer not found"
        )

    def raise_job_not_found() -> None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    try:
        employer = await EmployerCRUD.get_employer_by_id(user_id)
        if not employer:
            raise_employer_not_found()

        assert employer is not None  # Type narrowing

        success = await EmployerService.delete_job(
            company_name=employer.company_information.company_name,
            job_id=job_id
        )

        if not success:
            raise_job_not_found()
        else:
            return {"message": "Job deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete job: {e!s}"
        ) from e


@router.get("/applications")
async def get_applications(
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_employer_role)
):
    """
    Get all applications received by employer.

    Returns:
        List of applications
    """
    def raise_employer_not_found() -> None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employer not found"
        )

    try:
        employer = await EmployerCRUD.get_employer_by_id(user_id)
        if not employer:
            raise_employer_not_found()

        assert employer is not None  # Type narrowing

        return {
            "applications": [
                {
                    "applicant_id": app.applicant_id,
                    "job_id": app.job_id,
                    "initial_daterec": app.initial_daterec.isoformat(),
                    "current_status": app.candidate_tracking.current_status,
                    "previous_status": app.candidate_tracking.previous_status,
                    "current_status_date": app.candidate_tracking.current_status_date.isoformat(),
                }
                for app in employer.apps_received
            ]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get applications: {e!s}"
        ) from e


@router.get("/jobs/{job_id}/candidates", response_model=list[CandidateRecommendationResponse])
async def get_candidate_recommendations(
    job_id: str,
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_employer_role),
    n_results: int = 20,
    min_score: float = 0.0
):
    """
    Get AI-powered candidate recommendations for a specific job.

    This endpoint uses ChromaDB vector similarity and LangChain LLM scoring
    to provide personalized candidate recommendations with match scores.

    Args:
        job_id: Job posting ID
        n_results: Maximum number of recommendations to return (default: 20)
        min_score: Minimum match score threshold 0-100 (default: 0.0)

    Returns:
        List of candidate recommendations sorted by match score (descending)
    """
    try:
        # Get candidate matching service
        matching_service = get_candidate_matching_service()

        # Get recommendations
        recommendations = await matching_service.match_job_to_candidates(
            job_id=job_id,
            employer_id=user_id,
            n_results=n_results,
            min_score=min_score
        )

        # Convert to response format
        response = []
        for rec in recommendations:
            response.append(CandidateRecommendationResponse(
                seeker_id=rec["seeker_id"],
                first_name=rec["first_name"],
                last_name=rec["last_name"],
                email=rec["email"],
                match_score=rec["match_score"],
                score_breakdown=ScoreBreakdown(**rec["score_breakdown"]),
                has_applied=rec["has_applied"],
                resume_preview=rec["resume_preview"],
                key_skills=rec["key_skills"],
                education_level=rec["education_level"],
                edu_focus=rec["edu_focus"],
                pay_range=rec["pay_range"],
                pay_unit=rec["pay_unit"],
                phone=rec["phone"],
                address=rec["address"]
            ))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get candidate recommendations: {e!s}"
        ) from e
    else:
        return response


@router.post("/jobs/{job_id}/candidates/{seeker_id}/schedule-interview")
async def schedule_interview(
    job_id: str,
    seeker_id: str,
    request: ScheduleInterviewRequest,
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_employer_role)
):
    """
    Schedule an interview with a candidate and send email notification via n8n.

    Args:
        job_id: Job posting ID
        seeker_id: Job seeker ID
        request: Interview scheduling details

    Returns:
        Success message
    """
    def raise_seeker_not_found() -> None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seeker not found"
        )

    def raise_job_not_found() -> None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    def raise_employer_not_found() -> None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employer not found"
        )

    def raise_n8n_unavailable() -> None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="n8n service is unavailable. Cannot send interview notification."
        )

    try:
        # Get n8n service
        n8n_service = get_n8n_service()

        # Check n8n connection
        is_connected = await n8n_service.check_n8n_connection()
        if not is_connected:
            raise_n8n_unavailable()

        # Get seeker information - try multiple lookup methods
        from loguru import logger
        from beanie import PydanticObjectId
        from backend.schemas.seeker import Seeker
        
        seeker = None
        
        # First, try lookup by _id (MongoDB document ID) using SeekerCRUD
        seeker = await SeekerCRUD.get_seeker_by_id(seeker_id)
        
        # If not found, try lookup by seeker_id field (not _id)
        if not seeker:
            try:
                if isinstance(seeker_id, str):
                    seeker_id_obj = PydanticObjectId(seeker_id)
                else:
                    seeker_id_obj = seeker_id
                seeker = await Seeker.find_one(Seeker.seeker_id == seeker_id_obj)
                if seeker:
                    logger.debug(f"Found seeker by seeker_id field: {seeker_id}")
            except Exception as e:
                logger.debug(f"Seeker lookup by seeker_id field failed: {e}")
        
        # If still not found, try UUID format (only if ID looks like UUID)
        if not seeker and "-" in str(seeker_id):
            try:
                seeker = await SeekerCRUD.get_seeker_by_uuid(str(seeker_id))
                if seeker:
                    logger.debug(f"Found seeker by UUID: {seeker_id}")
            except (ValueError, Exception) as e:
                logger.debug(f"Seeker lookup by UUID failed: {e}")
        
        if not seeker:
            logger.warning(f"Seeker not found with ID: {seeker_id} (tried _id, seeker_id field, and UUID formats)")
            raise_seeker_not_found()

        assert seeker is not None  # Type narrowing
        seeker_email = seeker.information.email

        # Get employer information
        employer = await EmployerCRUD.get_employer_by_id(user_id)
        if not employer:
            raise_employer_not_found()

        assert employer is not None  # Type narrowing
        employer_name = employer.company_information.company_name
        employer_email = employer.email

        # Get job information
        job = None
        for open_job in employer.open_jobs:
            if str(open_job.job_id) == job_id:
                job = open_job
                break

        if not job:
            raise_job_not_found()

        assert job is not None  # Type narrowing

        # Prepare interview details for n8n
        interview_details = {
            "interview_date": request.interview_date,
            "interview_time": request.interview_time,
            "interview_type": request.interview_type,
            "location_or_link": request.location_or_link,
            "notes": request.notes
        }

        # Trigger n8n workflow to send email
        workflow_success = await n8n_service.trigger_interview_workflow(
            seeker_email=seeker_email,
            job_title=job.job_title,
            employer_name=employer_name,
            employer_email=employer_email,
            interview_details=interview_details
        )

        if not workflow_success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to trigger email notification. Interview may not have been scheduled."
            )

        # Update application status to "Interviewed"
        updated_employer = await EmployerCRUD.update_application_status(
            employer_id=user_id,
            applicant_id=seeker_id,
            job_id=job_id,
            new_status="Interviewed"
        )

        if not updated_employer:
            # Log warning but don't fail the request since email was sent
            from loguru import logger
            logger.warning(
                f"Failed to update application status for seeker {seeker_id} "
                f"and job {job_id}, but email notification was sent"
            )

        return {
            "message": "Interview scheduled successfully and email notification sent",
            "seeker_email": seeker_email,
            "job_title": job.job_title,
            "interview_date": request.interview_date.isoformat(),
            "interview_time": request.interview_time
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to schedule interview: {e!s}"
        ) from e


@router.get("/n8n/status", response_model=N8nStatusResponse)
async def get_n8n_status(
    _user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_employer_role)
):
    """
    Get n8n service connection status.

    Returns:
        n8n service status and message
    """
    try:
        n8n_service = get_n8n_service()
        status_info = await n8n_service.get_n8n_status()
        return N8nStatusResponse(**status_info)
    except Exception as e:
        return N8nStatusResponse(
            status="disconnected",
            message=f"Error checking n8n status: {e!s}"
        )

