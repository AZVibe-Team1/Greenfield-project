"""
Job Seeker API routes.

Handles job seeker profile management, job search, and applications.
"""
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from backend.core.security import get_current_user_id, get_current_user_role
from backend.db.seeker_db_ops import SeekerCRUD
from backend.services.seeker_services import SeekerService


router = APIRouter(prefix="/seekers", tags=["Job Seekers"])


# Response Models
class SeekerProfileResponse(BaseModel):
    """Job seeker profile response."""
    id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    address: dict[str, str]
    education_level: str
    edu_focus: str
    pay_range: list[int]
    pay_unit: str
    key_skills: list[str]
    resume: str | None = None
    applications: list[dict[str, Any]]


class UpdateSeekerRequest(BaseModel):
    """Update seeker profile request."""
    phone: str | None = None
    street: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    education_level: str | None = None
    edu_focus: str | None = None
    pay_range: list[int] | None = None
    pay_unit: str | None = None
    key_skills: list[str] | None = None


class UploadResumeRequest(BaseModel):
    """Upload resume request."""
    resume_content: str


class ApplyForJobRequest(BaseModel):
    """Apply for job request."""
    job_id: str
    employer_id: str


class JobSearchResponse(BaseModel):
    """Job search response."""
    job_id: str
    job_title: str
    job_description: str
    company_name: str
    employer_id: str
    posted_date: str
    department: str
    pay_range: list[int]
    pay_unit: str
    education_level: str
    edu_focus: str
    key_skills: list[str]
    hiring_manager: str


# Dependency to verify seeker role
async def verify_seeker_role(role: str = Depends(get_current_user_role)) -> str:
    """Verify that the current user is a job seeker."""
    if role != "seeker":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Job seeker role required"
        )
    return role


@router.get("/me", response_model=SeekerProfileResponse)
async def get_my_profile(
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_seeker_role)
):
    """
    Get current seeker's profile.

    Returns:
        Seeker profile information
    """
    def raise_not_found() -> None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seeker profile not found"
        )

    try:
        seeker = await SeekerCRUD.get_seeker_by_id(user_id)
        if not seeker:
            raise_not_found()

        assert seeker is not None  # Type narrowing

        # Convert applications to dict format for response
        applications_list = [
            {
                "job_id": app.job_id,
                "employer_id": app.employer_id,
                "date_applied": app.date_applied.isoformat(),
                "application_status": app.application_status
            }
            for app in seeker.applications
        ]

        return SeekerProfileResponse(
            id=str(seeker.id),
            first_name=seeker.information.first_name,
            last_name=seeker.information.last_name,
            email=seeker.information.email,
            phone=str(seeker.information.phone),
            address={
                "street": seeker.information.address.street,
                "city": seeker.information.address.city,
                "state": seeker.information.address.state,
                "zip_code": seeker.information.address.zip_code
            },
            education_level=seeker.education_level,
            edu_focus=seeker.edu_focus,
            pay_range=seeker.pay_range,
            pay_unit=seeker.pay_unit,
            key_skills=seeker.key_skills,
            resume=seeker.resume,
            applications=applications_list
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
    request: UpdateSeekerRequest,
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_seeker_role)
):
    """
    Update current seeker's profile.

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

        if request.phone is not None:
            update_data["information.phone"] = request.phone
        if request.street is not None or request.city is not None or request.state is not None or request.zip_code is not None:
            # Get current address
            seeker = await SeekerCRUD.get_seeker_by_id(user_id)
            if seeker:
                address = {
                    "street": request.street or seeker.information.address.street,
                    "city": request.city or seeker.information.address.city,
                    "state": request.state or seeker.information.address.state,
                    "zip_code": request.zip_code or seeker.information.address.zip_code
                }
                update_data["information.address"] = address

        if request.education_level is not None:
            update_data["education_level"] = request.education_level
        if request.edu_focus is not None:
            update_data["edu_focus"] = request.edu_focus
        if request.pay_range is not None:
            update_data["pay_range"] = request.pay_range
        if request.pay_unit is not None:
            update_data["pay_unit"] = request.pay_unit
        if request.key_skills is not None:
            update_data["key_skills"] = request.key_skills

        updated_seeker = await SeekerService.update_seeker_profile(user_id, update_data)

        if not updated_seeker:
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


@router.post("/resume")
async def upload_resume(
    request: UploadResumeRequest,
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_seeker_role)
):
    """
    Upload or update resume.

    Args:
        request: Resume content

    Returns:
        Success message
    """
    def raise_upload_failed() -> None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload resume"
        )

    try:
        updated_seeker = await SeekerService.upload_resume(
            seeker_id=user_id,
            resume_content=request.resume_content
        )

        if not updated_seeker:
            raise_upload_failed()
        else:
            return {"message": "Resume uploaded successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload resume: {e!s}"
        ) from e


@router.post("/applications")
async def apply_for_job(
    request: ApplyForJobRequest,
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_seeker_role)
):
    """
    Apply for a job.

    Args:
        request: Job and employer IDs

    Returns:
        Success message
    """
    def raise_apply_failed() -> None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to apply for job"
        )

    try:
        updated_seeker = await SeekerService.apply_for_job(
            seeker_id=user_id,
            job_id=request.job_id,
            employer_id=request.employer_id
        )

        if not updated_seeker:
            raise_apply_failed()
        else:
            return {"message": "Application submitted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to apply for job: {e!s}"
        ) from e


@router.get("/applications")
async def get_my_applications(
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_seeker_role)
):
    """
    Get all applications for current seeker.

    Returns:
        List of applications
    """
    def raise_seeker_not_found() -> None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seeker not found"
        )

    try:
        seeker = await SeekerCRUD.get_seeker_by_id(user_id)
        if not seeker:
            raise_seeker_not_found()

        assert seeker is not None  # Type narrowing

        return {
            "applications": [
                {
                    "job_id": app.job_id,
                    "employer_id": app.employer_id,
                    "date_applied": app.date_applied.isoformat(),
                    "application_status": app.application_status
                }
                for app in seeker.applications
            ]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get applications: {e!s}"
        ) from e


@router.delete("/applications/{job_id}")
async def delete_application(
    job_id: str,
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_seeker_role)
):
    """
    Delete/withdraw an application.

    Args:
        job_id: Job ID to withdraw application from

    Returns:
        Success message
    """
    def raise_application_not_found() -> None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    try:
        updated_seeker = await SeekerService.delete_application(
            seeker_id=user_id,
            job_id=job_id,
            _company_name=""  # Not needed for withdrawal
        )

        if not updated_seeker:
            raise_application_not_found()
        else:
            return {"message": "Application withdrawn successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete application: {e!s}"
        ) from e


@router.get("/jobs", response_model=list[JobSearchResponse])
async def search_jobs(
    title: str | None = None,
    company: str | None = None,
    skill: str | None = None,
    _role: str = Depends(verify_seeker_role)
):
    """
    Search for jobs.

    Args:
        title: Search by job title (optional)
        company: Search by company name (optional)
        skill: Search by required skill (optional)

    Returns:
        List of matching jobs
    """
    try:
        if title:
            jobs = await SeekerService.search_by_parameter("jobtitle", title)
        elif company:
            jobs = await SeekerService.search_by_parameter("companyname", company)
        elif skill:
            jobs = await SeekerService.search_by_parameter("skill", skill)
        else:
            # Get all jobs if no filter specified
            jobs = await SeekerService.search_all_jobs()

        return [
            JobSearchResponse(
                job_id=job["job_id"],
                job_title=job["job_title"],
                job_description=job["job_description"],
                company_name=job["company_name"],
                employer_id=job["employer_id"],
                posted_date=job["posted_date"].isoformat(),
                department=job["department"],
                pay_range=job["pay_range"],
                pay_unit=job["pay_unit"],
                education_level=job["education_level"],
                edu_focus=job["edu_focus"],
                key_skills=job["key_skills"],
                hiring_manager=job["hiring_manager"]
            )
            for job in jobs
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search jobs: {e!s}"
        ) from e


@router.get("/jobs/{job_id}", response_model=JobSearchResponse)
async def get_job_details(
    job_id: str,
    _role: str = Depends(verify_seeker_role)
):
    """
    Get details of a specific job.

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

    try:
        # Search all jobs and find the matching one
        all_jobs = await SeekerService.search_all_jobs()

        for job in all_jobs:
            if job["job_id"] == job_id:
                return JobSearchResponse(
                    job_id=job["job_id"],
                    job_title=job["job_title"],
                    job_description=job["job_description"],
                    company_name=job["company_name"],
                    employer_id=job["employer_id"],
                    posted_date=job["posted_date"].isoformat(),
                    department=job["department"],
                    pay_range=job["pay_range"],
                    pay_unit=job["pay_unit"],
                    education_level=job["education_level"],
                    edu_focus=job["edu_focus"],
                    key_skills=job["key_skills"],
                    hiring_manager=job["hiring_manager"]
                )

        raise_job_not_found()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get job details: {e!s}"
        ) from e

