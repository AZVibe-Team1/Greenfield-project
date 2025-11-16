"""
Job Seeker API routes.

Handles job seeker profile management, job search, and applications.
"""
import asyncio
import json
import tempfile
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from loguru import logger

from backend.ai.chains.matching_service import get_matching_service
from backend.core.security import get_current_user_id, get_current_user_role
from backend.db.seeker_db_ops import SeekerCRUD
from backend.services.seeker_services import (
    DOCXExtractionError,
    FileValidationError,
    PDFExtractionError,
    SeekerService,
)


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


class ScoreBreakdown(BaseModel):
    """Match score breakdown."""
    skills_score: float
    education_score: float
    pay_score: float
    experience_score: float
    reasoning: str


class JobRecommendationResponse(BaseModel):
    """AI-powered job recommendation response."""
    job_id: str
    job_title: str
    company_name: str
    employer_id: str
    match_score: float
    score_breakdown: ScoreBreakdown
    job_description: str
    key_skills: list[str]
    education_level: str
    edu_focus: str
    pay_range: list[int]
    pay_unit: str
    department: str
    posted_date: str | None = None
    hire_mgr_first: str
    hire_mgr_last: str


class AutoApplySettingsRequest(BaseModel):
    """Auto-apply settings request."""
    enabled: bool
    threshold: float = 80.0  # Default 80%


class AutoApplySettingsResponse(BaseModel):
    """Auto-apply settings response."""
    enabled: bool
    threshold: float


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
    file: UploadFile | None = File(None),
    resume_text: str | None = Form(None),
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_seeker_role)
):
    """
    Upload or update resume.

    Accepts either a file upload (PDF, DOCX, TXT) or direct text content.
    Both MongoDB and ChromaDB are automatically updated.

    Args:
        file: Resume file (PDF, DOCX, or TXT) - optional
        resume_text: Direct text content - optional (at least one required)

    Returns:
        Success message

    Raises:
        HTTPException: If upload fails or validation errors occur
    """
    def raise_missing_input() -> None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either file or resume_text must be provided"
        )

    def raise_upload_failed() -> None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload resume"
        )

    def raise_invalid_file_type() -> None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PDF, DOCX, and TXT files are supported"
        )

    def raise_file_too_large() -> None:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds maximum allowed size (10MB)"
        )

    def raise_parse_error(error_msg: str) -> None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to parse file: {error_msg}"
        )

    temp_file_path: Path | None = None

    try:
        # Validate that at least one input is provided
        if not file and not resume_text:
            raise_missing_input()

        # Handle file upload
        if file:
            # Validate file
            try:
                # Get file size (need to read content first to get size)
                file_content = await file.read()
                file_size = len(file_content)
                
                # Validate file
                SeekerService.validate_resume_file(
                    filename=file.filename or "unknown",
                    file_size=file_size
                )
            except FileValidationError as e:
                if "exceeds" in str(e).lower():
                    raise_file_too_large()
                else:
                    raise_invalid_file_type()
            except Exception as e:
                logger.error(f"File validation error: {e}")
                raise_invalid_file_type()

            # Create temporary file
            suffix = Path(file.filename or "resume").suffix.lower()
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix,
                prefix="resume_upload_"
            ) as temp_file:
                temp_file_path = Path(temp_file.name)
                # Write file content to temp file
                temp_file.write(file_content)

            try:
                # Upload resume using file path
                updated_seeker = await SeekerService.upload_resume(
                    seeker_id=user_id,
                    file_path=temp_file_path
                )
            except (PDFExtractionError, DOCXExtractionError) as e:
                raise_parse_error(str(e))
            except ValueError as e:
                # Handle unsupported file type or other value errors
                raise_invalid_file_type()
            finally:
                # Clean up temporary file
                if temp_file_path and temp_file_path.exists():
                    try:
                        temp_file_path.unlink()
                    except Exception as cleanup_error:
                        logger.warning(f"Failed to delete temp file: {cleanup_error}")

        else:
            # Handle text-only upload
            updated_seeker = await SeekerService.upload_resume(
                seeker_id=user_id,
                resume_content=resume_text
            )

        if not updated_seeker:
            raise_upload_failed()

        return {"message": "Resume uploaded successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error uploading resume: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload resume: {e!s}"
        ) from e
    finally:
        # Ensure temp file is cleaned up even if an error occurs
        if temp_file_path and temp_file_path.exists():
            try:
                temp_file_path.unlink()
            except Exception:
                pass  # Ignore cleanup errors in finally block


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


@router.get("/recommendations", response_model=list[JobRecommendationResponse])
async def get_job_recommendations(
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_seeker_role),
    n_results: int = 20,
    min_score: float = 0.0
):
    """
    Get AI-powered job recommendations for the current seeker.

    This endpoint uses ChromaDB vector similarity and LangChain LLM scoring
    to provide personalized job recommendations with match scores.

    Args:
        n_results: Maximum number of recommendations to return (default: 20)
        min_score: Minimum match score threshold 0-100 (default: 0.0)

    Returns:
        List of job recommendations sorted by match score (descending)
    """
    try:
        # Get matching service
        matching_service = get_matching_service()

        # Get recommendations
        recommendations = await matching_service.match_seeker_to_jobs(
            seeker_id=user_id,
            n_results=n_results,
            min_score=min_score
        )

        # Convert to response format
        response = []
        for rec in recommendations:
            response.append(JobRecommendationResponse(
                job_id=rec["job_id"],
                job_title=rec["job_title"],
                company_name=rec["company_name"],
                employer_id=rec["employer_id"],
                match_score=rec["match_score"],
                score_breakdown=ScoreBreakdown(**rec["score_breakdown"]),
                job_description=rec["job_description"],
                key_skills=rec["key_skills"],
                education_level=rec["education_level"],
                edu_focus=rec["edu_focus"],
                pay_range=rec["pay_range"],
                pay_unit=rec["pay_unit"],
                department=rec["department"],
                posted_date=rec["posted_date"].isoformat() if rec.get("posted_date") else None,
                hire_mgr_first=rec["hire_mgr_first"],
                hire_mgr_last=rec["hire_mgr_last"]
            ))

        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get recommendations: {e!s}"
        ) from e


@router.get("/recommendations/stream")
async def get_job_recommendations_stream(
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_seeker_role),
    n_results: int = 10,
    min_score: float = 0.0
):
    """
    Stream AI-powered job recommendations as they are calculated.
    
    This endpoint uses Server-Sent Events (SSE) to stream recommendations
    as each match score is calculated, providing immediate feedback to users.
    
    Args:
        n_results: Maximum number of recommendations to return (default: 10)
        min_score: Minimum match score threshold 0-100 (default: 0.0)
    
    Returns:
        Streaming response with job recommendations in SSE format
    """
    async def generate_recommendations():
        try:
            # Get matching service
            matching_service = get_matching_service()
            
            # Get seeker details and embeddings
            logger.info(f"[STREAM] Starting match for seeker_id: {user_id}")
            
            # Get seeker from MongoDB
            from bson import ObjectId
            seeker = await SeekerCRUD.get_seeker_by_id(ObjectId(user_id))
            if not seeker:
                error_data = json.dumps({"error": "Seeker not found"})
                yield f"data: {error_data}\n\n"
                return
            
            logger.info(f"[STREAM] Found seeker: {seeker.information.email}")
            seeker_identification = str(seeker.seeker_identification)
            logger.info(f"[STREAM] Seeker UUID: {seeker_identification}")
            
            # Get seeker embedding from ChromaDB
            seeker_embedding = await matching_service.get_seeker_embedding(seeker_identification)
            if seeker_embedding is None or len(seeker_embedding) == 0:
                error_data = json.dumps({"error": "Seeker embedding not found in ChromaDB"})
                yield f"data: {error_data}\n\n"
                return
            
            logger.info("[STREAM] Found seeker embedding in ChromaDB")
            
            # Query ChromaDB for similar jobs
            similar_jobs = await matching_service.search_similar_jobs(
                query_embedding=seeker_embedding,
                n_results=n_results * 3  # Get more to filter
            )
            
            logger.info(f"[STREAM] Found {len(similar_jobs)} similar jobs")
            
            # Prepare seeker data for scoring
            seeker_data = {
                "first_name": seeker.information.first_name,
                "last_name": seeker.information.last_name,
                "email": seeker.information.email,
                "education_level": seeker.education_level,
                "edu_focus": seeker.edu_focus,
                "key_skills": seeker.key_skills,
                "pay_range": seeker.pay_range,
                "pay_unit": seeker.pay_unit,
                "resume": seeker.resume or "No resume available"
            }
            
            # Process each job and stream results
            count = 0
            for job_match in similar_jobs:
                job_id = job_match["job_id"]
                if count >= n_results:
                    break
                    
                try:
                    # Fetch job details from MongoDB
                    job_details = await matching_service.fetch_job_details(job_id)
                    if not job_details:
                        logger.warning(f"[STREAM] Job not found: {job_id}")
                        continue
                    
                    # Calculate match score
                    logger.debug(f"[STREAM] Calculating score for job: {job_details['job_title']}")
                    score_breakdown = await matching_service.scoring_chain.calculate_match_score(
                        seeker_data=seeker_data,
                        job_data=job_details
                    )
                    
                    match_score = score_breakdown.overall_score
                    logger.debug(f"[STREAM] Match score calculated: {match_score}%")
                    
                    # Filter by min_score
                    if match_score < min_score:
                        continue
                    
                    # Prepare recommendation
                    recommendation = {
                        "job_id": job_details["job_id"],
                        "job_title": job_details["job_title"],
                        "company_name": job_details["company_name"],
                        "employer_id": job_details["employer_id"],
                        "match_score": match_score,
                        "score_breakdown": {
                            "skills_score": score_breakdown.skills_score,
                            "education_score": score_breakdown.education_score,
                            "pay_score": score_breakdown.pay_score,
                            "experience_score": score_breakdown.experience_score,
                            "reasoning": score_breakdown.reasoning
                        },
                        "job_description": job_details["job_description"],
                        "key_skills": job_details["key_skills"],
                        "education_level": job_details["education_level"],
                        "edu_focus": job_details["edu_focus"],
                        "pay_range": job_details["pay_range"],
                        "pay_unit": job_details["pay_unit"],
                        "department": job_details["department"],
                        "posted_date": job_details["posted_date"].isoformat() if job_details.get("posted_date") else None,
                        "hire_mgr_first": job_details["hire_mgr_first"],
                        "hire_mgr_last": job_details["hire_mgr_last"]
                    }
                    
                    # Stream this recommendation
                    data = json.dumps(recommendation)
                    yield f"data: {data}\n\n"
                    count += 1
                    
                except Exception as e:
                    logger.error(f"[STREAM] Error processing job {job_id}: {e}")
                    continue
            
            # Send completion signal
            yield f"data: {json.dumps({'done': True, 'total': count})}\n\n"
            logger.info(f"[STREAM] Completed streaming {count} recommendations")
            
        except Exception as e:
            logger.error(f"[STREAM] Error in streaming: {e}")
            error_data = json.dumps({"error": str(e)})
            yield f"data: {error_data}\n\n"
    
    return StreamingResponse(
        generate_recommendations(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )


@router.post("/auto-apply/settings", response_model=AutoApplySettingsResponse)
async def set_auto_apply_settings(
    request: AutoApplySettingsRequest,
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_seeker_role)
):
    """
    Set auto-apply settings for the current seeker.

    Args:
        request: Auto-apply settings (enabled, threshold)

    Returns:
        Updated auto-apply settings
    """
    try:
        # Update seeker profile with auto-apply settings
        # Note: We need to add these fields to the Seeker model
        update_data = {
            "auto_apply_enabled": request.enabled,
            "auto_apply_threshold": request.threshold
        }

        updated_seeker = await SeekerService.update_seeker_profile(user_id, update_data)

        if not updated_seeker:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update auto-apply settings"
            )

        return AutoApplySettingsResponse(
            enabled=request.enabled,
            threshold=request.threshold
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to set auto-apply settings: {e!s}"
        ) from e


@router.get("/auto-apply/settings", response_model=AutoApplySettingsResponse)
async def get_auto_apply_settings(
    user_id: str = Depends(get_current_user_id),
    _role: str = Depends(verify_seeker_role)
):
    """
    Get auto-apply settings for the current seeker.

    Returns:
        Current auto-apply settings
    """
    try:
        seeker = await SeekerCRUD.get_seeker_by_id(user_id)

        if not seeker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seeker not found"
            )

        # Get auto-apply settings or return defaults
        enabled = getattr(seeker, "auto_apply_enabled", False)
        threshold = getattr(seeker, "auto_apply_threshold", 80.0)

        return AutoApplySettingsResponse(
            enabled=enabled,
            threshold=threshold
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get auto-apply settings: {e!s}"
        ) from e

