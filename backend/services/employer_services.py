"""
Employer Services Module

This module provides business logic services for employer operations including
account management, job posting management, and application tracking.
"""

from datetime import datetime
from typing import Any
from uuid import uuid4
from zoneinfo import ZoneInfo

from beanie import PydanticObjectId

from backend.db.chroma_crud_ops import update_collection, write_collection
from backend.db.employer_db_ops import EmployerCRUD
from backend.db.settings import (
    Employer_JobDescr_collection,
    Employer_Skillswish_collection,
)
from backend.schemas.employer import Employer
from backend.utils.gics_helper import is_valid_gics_code
from backend.utils.validators import Email


class EmployerService:
    """Business logic services for employers."""

    @staticmethod
    async def create_new_employer(
        company_name: str,
        address: dict[str, str],
        industry: list[dict[str, str]],
        contact_first_name: str,
        contact_last_name: str,
        email: Email,
        password_hash: str,
        benefits: str = "",
        open_jobs: list[dict[str, Any]] | None = None
    ) -> Employer | None:
        """
        Create a new employer account.

        Args:
            company_name: Official company name
            address: Company address dictionary with street, city, state, zip_code
            industry: List of 2 industry classifications with code and description
            contact_first_name: Primary contact's first name
            contact_last_name: Primary contact's last name
            email: Contact email address (for authentication)
            password_hash: Hashed password for authentication
            benefits: Description of company benefits (optional)
            open_jobs: List of open job postings (optional, defaults to empty list)

        Returns:
            Created Employer document or None if creation fails

        Raises:
            ValueError: If GICS code validation fails

        Example:
            >>> employer = await create_new_employer(
            ...     company_name="Tech Corp",
            ...     address={"street": "123 Main St", "city": "Boston", "state": "MA", "zip_code": "02101"},
            ...     industry=[
            ...         {"code": "45", "description": "Information Technology"},
            ...         {"code": "4510", "description": "Software & Services"}
            ...     ],
            ...     contact_first_name="John",
            ...     contact_last_name="Doe",
            ...     email="john@techcorp.com",
            ...     password_hash="hashed_password",
            ...     benefits="Health, 401k"
            ... )
        """
        # Validate GICS codes if industry info is provided
        if industry:
            for industry_item in industry:
                code = industry_item.get("code", "")
                if not is_valid_gics_code(code):
                    msg = f"Invalid GICS code: {code}"
                    raise ValueError(msg)

        # Generate unique EmployerID
        employer_identification = uuid4()

        # Build employer data structure
        employer_data = {
            "employer_identification": employer_identification,
            "temperature": 0.75,
            "company_information": {
                "company_name": company_name,
                "address": address,
                "industry": industry,
                "benefits": benefits
            },
            "contact_first_name": contact_first_name,
            "contact_last_name": contact_last_name,
            "email": email,
            "password_hash": password_hash,
            "created_at": datetime.now(ZoneInfo("America/Denver")),
            "updated_at": datetime.now(ZoneInfo("America/Denver")),
            "open_jobs": open_jobs if open_jobs else [],
            "apps_received": []
        }

        # Create employer in database
        return await EmployerCRUD.create_employer(employer_data)

    @staticmethod
    async def update_employer(
        employer_id: str | PydanticObjectId,
        update_data: dict[str, Any]
    ) -> Employer | None:
        """
        Update employer information (excluding company_name).

        Updates any employer fields except company_name, and sets updated_at timestamp.

        Args:
            employer_id: Employer's ObjectId
            update_data: Dictionary of fields to update

        Returns:
            Updated Employer document or None if update fails

        Example:
            >>> updated_employer = await update_employer(
            ...     employer_id="507f1f77bcf86cd799439011",
            ...     update_data={
            ...         "company_information.benefits": "Updated benefits package",
            ...         "contact_first_name": "Jane"
            ...     }
            ... )
        """
        # Ensure company_name cannot be updated
        if "company_information.company_name" in update_data:
            msg = "Company name cannot be updated"
            raise ValueError(msg)

        # Add updated_at timestamp
        update_data["updated_at"] = datetime.now(ZoneInfo("America/Denver"))

        # Update employer in database
        return await EmployerCRUD.update_employer(employer_id, update_data)

    @staticmethod
    async def create_job(
        employer_id: str | PydanticObjectId,
        job_title: str,
        job_description: str,
        department: str,
        hire_mgr_first: str,
        hire_mgr_last: str,
        pay_range: list[int],
        pay_unit: str,
        education_level: str,
        edu_focus: str,
        key_skills: list[str] | None = None
    ) -> Employer | None:
        """
        Create a new job posting for an employer.

        Creates an OpenJob record with status set to 'Posted' and adds it to
        the employer's document.

        Args:
            employer_id: Employer's ObjectId
            job_title: Title of the position
            job_description: Detailed job description
            department: Department name
            hire_mgr_first: Hiring manager's first name
            hire_mgr_last: Hiring manager's last name
            pay_range: Salary range [low, high]
            pay_unit: Unit for pay_range ("Hourly", "Monthly", or "Yearly")
            education_level: Required education ("BA", "BS", "MA", "MS", "MBA", "PhD")
            edu_focus: Required field of study
            key_skills: List of required skills (optional, max 15)

        Returns:
            Updated Employer document with new job or None if creation fails

        Example:
            >>> employer = await create_job(
            ...     employer_id="507f1f77bcf86cd799439011",
            ...     job_title="Senior Software Engineer",
            ...     job_description="Build scalable systems...",
            ...     department="Engineering",
            ...     hire_mgr_first="John",
            ...     hire_mgr_last="Smith",
            ...     pay_range=[120000, 180000],
            ...     pay_unit="Yearly",
            ...     education_level="BS",
            ...     edu_focus="Computer Science",
            ...     key_skills=["Python", "FastAPI", "MongoDB"]
            ... )
        """
        # Fetch employer to get employer_identification
        employer = await EmployerCRUD.get_employer_by_id(employer_id)
        if not employer:
            return None

        # Generate unique job ID and job identification
        job_id = PydanticObjectId()
        job_identification = uuid4()

        # Create job posting data
        job_data = {
            "job_id": job_id,
            "job_identification": job_identification,
            "employer_identification": employer.employer_identification,
            "job_title": job_title,
            "job_description": job_description,
            "posted_date": datetime.now(ZoneInfo("America/Denver")),
            "department": department,
            "hire_mgr_first": hire_mgr_first,
            "hire_mgr_last": hire_mgr_last,
            "current_status": "Posted",
            "pay_range": pay_range,
            "pay_unit": pay_unit,
            "education_level": education_level,
            "edu_focus": edu_focus,
            "key_skills": key_skills if key_skills else []
        }

        # Store job description in ChromaDB if not empty
        if job_description:
            metadata_descr = {
                "Title": job_title,
                "Post_Date": str(job_data["posted_date"]),
                "Employer_UUID": str(employer.employer_identification)
            }
            write_collection(
                Employer_JobDescr_collection,
                "Employer_JobDescr_Collection",
                str(job_identification),
                job_description,
                metadata_descr
            )

        # Store skills in ChromaDB if any skill data exists
        if key_skills or education_level or edu_focus:
            skills_list = []
            if key_skills:
                skills_list.extend(key_skills)
            if education_level:
                skills_list.append(f"Education: {education_level}")
            if edu_focus:
                skills_list.append(f"Focus: {edu_focus}")

            skills = ", ".join(skills_list)
            metadata_skill = {"Desired Skills": skills}
            write_collection(
                Employer_Skillswish_collection,
                "Employer_Skillswish_Collection",
                str(job_identification),
                skills,
                metadata_skill
            )

        # Add job posting to employer
        return await EmployerCRUD.add_job_posting(employer_id, job_data)

    @staticmethod
    async def modify_job(
        employer_id: str | PydanticObjectId,
        job_id: str | PydanticObjectId,
        update_data: dict[str, Any]
    ) -> Employer | None:
        """
        Modify an existing job posting.

        Updates any job fields including status for a specific job posting.

        Args:
            employer_id: Employer's ObjectId
            job_id: Job posting ID
            update_data: Dictionary of job fields to update

        Returns:
            Updated Employer document or None if update fails

        Example:
            >>> employer = await modify_job(
            ...     employer_id="507f1f77bcf86cd799439011",
            ...     job_id="507f1f77bcf86cd799439022",
            ...     update_data={
            ...         "current_status": "Withdrawn",
            ...         "job_description": "Updated description"
            ...     }
            ... )
        """
        # Fetch employer to get job details
        employer = await EmployerCRUD.get_employer_by_id(employer_id)
        if not employer:
            return None

        # Find the job to get its identification and current data
        job = None
        for open_job in employer.open_jobs:
            if str(open_job.job_id) == str(job_id):
                job = open_job
                break

        if not job:
            return None

        # Update ChromaDB if job description is being updated
        job_description = update_data.get("job_description")
        if job_description:
            metadata_descr = {
                "Title": update_data.get("job_title", job.job_title),
                "Post_Date": str(update_data.get("posted_date", job.posted_date)),
                "Employer_UUID": str(employer.employer_identification)
            }
            update_collection(
                Employer_JobDescr_collection,
                "Employer_JobDescr_Collection",
                str(job.job_identification),
                job_description,
                metadata_descr
            )

        # Update ChromaDB skills if any skill fields are being updated
        key_skills = update_data.get("key_skills", job.key_skills)
        education_level = update_data.get("education_level", job.education_level)
        edu_focus = update_data.get("edu_focus", job.edu_focus)

        if key_skills or education_level or edu_focus:
            skills_list = []
            if key_skills:
                skills_list.extend(key_skills if isinstance(key_skills, list) else [key_skills])
            if education_level:
                skills_list.append(f"Education: {education_level}")
            if edu_focus:
                skills_list.append(f"Focus: {edu_focus}")

            skills = ", ".join(skills_list)
            metadata_skill = {"Desired Skills": skills}
            update_collection(
                Employer_Skillswish_collection,
                "Employer_Skillswish_Collection",
                str(job.job_identification),
                skills,
                metadata_skill
            )

        # Update job posting in database
        return await EmployerCRUD.update_job_posting(
            employer_id,
            job_id,
            update_data
        )

    @staticmethod
    async def delete_employer(
        company_name: str
    ) -> bool:
        """
        Delete an employer by company name.

        Args:
            company_name: Company name to identify the employer

        Returns:
            True if deletion was successful, False otherwise

        Example:
            >>> success = await delete_employer("Tech Corp")
        """
        try:
            # Find employer by company name
            employer = await EmployerCRUD.get_employer_by_company_name(company_name)

            if not employer or not employer.id:
                return False

            # Delete employer
            return await EmployerCRUD.delete_employer(employer.id)

        except Exception:
            return False

    @staticmethod
    async def delete_job(
        company_name: str,
        job_id: str
    ) -> bool:
        """
        Delete a job posting from an employer.

        Args:
            company_name: Company name to identify the employer
            job_id: Job posting ID to delete

        Returns:
            True if deletion was successful, False otherwise

        Example:
            >>> success = await delete_job("Tech Corp", "507f1f77bcf86cd799439022")
        """
        try:
            # Find employer by company name
            employer = await EmployerCRUD.get_employer_by_company_name(company_name)

            if not employer or not employer.id:
                return False

            # Remove job posting
            updated_employer = await EmployerCRUD.remove_job_posting(
                employer.id,
                job_id
            )
            return updated_employer is not None  # noqa

        except Exception:
            return False

    @staticmethod
    async def search_all_jobs(
        skip: int = 0,
        limit: int = 100
    ) -> list[dict[str, Any]]:
        """
        Search and return all jobs in the employer collection.

        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return

        Returns:
            List of dictionaries containing job information with company details

        Example:
            >>> jobs = await search_all_jobs(skip=0, limit=50)
            >>> for job in jobs:
            ...     print(f"{job['job_title']} at {job['company_name']}")
        """
        try:
            # Get employers with open jobs
            employers = await EmployerCRUD.get_employers_with_open_jobs()

            # Flatten job listings with company information
            all_jobs = []
            for employer in employers:
                for job in employer.open_jobs:
                    job_info = {
                        "job_id": job.job_id,
                        "job_title": job.job_title,
                        "job_description": job.job_description,
                        "posted_date": job.posted_date,
                        "department": job.department,
                        "hire_mgr_first": job.hire_mgr_first,
                        "hire_mgr_last": job.hire_mgr_last,
                        "current_status": job.current_status,
                        "pay_range": job.pay_range,
                        "pay_unit": job.pay_unit,
                        "education_level": job.education_level,
                        "edu_focus": job.edu_focus,
                        "key_skills": job.key_skills,
                        "company_name": employer.company_information.company_name,
                        "company_address": {
                            "street": employer.company_information.address.street,
                            "city": employer.company_information.address.city,
                            "state": employer.company_information.address.state,
                            "zip_code": employer.company_information.address.zip_code
                        },
                        "employer_id": str(employer.id)
                    }
                    all_jobs.append(job_info)

            # Apply pagination
            return all_jobs[skip:skip + limit]

        except Exception:
            return []

    @staticmethod
    async def search_by_parameter(
        parameter: str,
        value: str,
        skip: int = 0,
        limit: int = 100
    ) -> list[dict[str, Any]]:
        """
        Search employers/jobs by parameter.

        Searches the employer collection for matches on job title, company name,
        or skill, and returns matching results.

        Args:
            parameter: Search parameter ("jobtitle", "companyname", or "skill")
            value: Value to search for
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return

        Returns:
            List of dictionaries containing matching job/employer information

        Example:
            >>> # Search by job title
            >>> results = await search_by_parameter("jobtitle", "engineer")
            >>>
            >>> # Search by company name
            >>> results = await search_by_parameter("companyname", "Tech Corp")
            >>>
            >>> # Search by skill
            >>> results = await search_by_parameter("skill", "Python")
        """
        # Validate parameter
        parameter_lower = parameter.lower()
        if parameter_lower not in ["companyname", "jobtitle", "skill"]:
            msg = f"Invalid search parameter: {parameter}. Use 'jobtitle', 'companyname', or 'skill'"
            raise ValueError(msg)

        results = []

        if parameter_lower == "companyname":
            # Search by company name
            employers = await EmployerCRUD.get_all_employers()
            for employer in employers:
                if value.lower() in employer.company_information.company_name.lower():
                    employer_info = {
                        "employer_id": str(employer.id),
                        "company_name": employer.company_information.company_name,
                        "contact_name": f"{employer.contact_first_name} {employer.contact_last_name}",
                        "address": {
                            "street": employer.company_information.address.street,
                            "city": employer.company_information.address.city,
                            "state": employer.company_information.address.state,
                            "zip_code": employer.company_information.address.zip_code
                        },
                        "benefits": employer.company_information.benefits,
                        "open_jobs_count": len(employer.open_jobs),
                        "open_jobs": [
                            {
                                "job_id": job.job_id,
                                "job_title": job.job_title,
                                "department": job.department,
                                "current_status": job.current_status
                            }
                            for job in employer.open_jobs
                        ]
                    }
                    results.append(employer_info)

        elif parameter_lower == "jobtitle":
            # Search by job title
            employers = await EmployerCRUD.get_employers_with_open_jobs()
            for employer in employers:
                for job in employer.open_jobs:
                    if value.lower() in job.job_title.lower():
                        job_info = {
                            "job_id": job.job_id,
                            "job_title": job.job_title,
                            "job_description": job.job_description,
                            "posted_date": job.posted_date,
                            "department": job.department,
                            "current_status": job.current_status,
                            "pay_range": job.pay_range,
                            "pay_unit": job.pay_unit,
                            "education_level": job.education_level,
                            "edu_focus": job.edu_focus,
                            "key_skills": job.key_skills,
                            "company_name": employer.company_information.company_name,
                            "employer_id": str(employer.id)
                        }
                        results.append(job_info)

        elif parameter_lower == "skill":
            # Search by skill
            employers = await EmployerCRUD.get_employers_with_open_jobs()
            for employer in employers:
                for job in employer.open_jobs:
                    # Check if skill exists in key_skills list
                    if any(value.lower() in skill.lower() for skill in job.key_skills):
                        job_info = {
                            "job_id": job.job_id,
                            "job_title": job.job_title,
                            "job_description": job.job_description,
                            "posted_date": job.posted_date,
                            "department": job.department,
                            "current_status": job.current_status,
                            "pay_range": job.pay_range,
                            "pay_unit": job.pay_unit,
                            "education_level": job.education_level,
                            "edu_focus": job.edu_focus,
                            "key_skills": job.key_skills,
                            "company_name": employer.company_information.company_name,
                            "employer_id": str(employer.id)
                        }
                        results.append(job_info)

        # Apply pagination
        return results[skip:skip + limit]


# Example usage
if __name__ == "__main__":
    import asyncio

    async def test_employer_services():
        """Test employer services."""

        # Note: These are example function calls
        # Actual execution requires MongoDB connection via Beanie





    # Run tests
    asyncio.run(test_employer_services())

