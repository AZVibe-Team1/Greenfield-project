"""
Seeker Services Module

This module provides business logic services for job seeker operations including
account management, resume handling, job applications, and searches.
"""

from datetime import datetime
from pathlib import Path
from typing import Any

import PyPDF2
from docx import Document

from backend.db.employer_db_ops import EmployerCRUD
from backend.db.seeker_db_ops import SeekerCRUD
from backend.schemas.seeker import Information, Seeker
from backend.utils.validators import Address


class SeekerService:
    """Business logic services for job seekers."""

    @staticmethod
    async def create_new_seeker(
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        street: str,
        city: str,
        state: str,
        zip_code: str,
        password_hash: str,
        education_level: str,
        edu_focus: str,
        pay_range: list[int] | None = None,
        pay_unit: str = "Yearly",
        key_skills: list[str] | None = None,
        resume: str | None = None
    ) -> Seeker | None:
        """
        Create a new seeker account.

        Args:
            first_name: Seeker's first name (required)
            last_name: Seeker's last name (required)
            email: Email address (required)
            phone: Phone number (required)
            street: Street address (required)
            city: City (required)
            state: State abbreviation (required)
            zip_code: ZIP code (required)
            password_hash: Hashed password (required)
            education_level: Education level (required)
            edu_focus: Field of study (required)
            pay_range: Desired salary range [low, high] (optional)
            pay_unit: Pay unit (Hourly/Monthly/Yearly, default: Yearly)
            key_skills: List of skills (optional)
            resume: Resume text (optional)

        Returns:
            Created Seeker object or None if creation fails

        Example:
            >>> seeker = await create_new_seeker(
            ...     first_name="John",
            ...     last_name="Doe",
            ...     email="john@example.com",
            ...     phone="+12025550123",
            ...     street="123 Main St",
            ...     city="New York",
            ...     state="NY",
            ...     zip_code="10001",
            ...     password_hash="hashed_pwd",
            ...     education_level="BS",
            ...     edu_focus="Computer Science"
            ... )
        """
        try:
            # Create address object
            address = Address(
                street=street,
                city=city,
                state=state,
                zip_code=zip_code
            )

            # Create information sub-document
            information = Information(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address
            )

            # Prepare seeker data
            seeker_data = {
                "information": information.model_dump(),
                "password_hash": password_hash,
                "created_at": datetime.now(),
                "education_level": education_level,
                "edu_focus": edu_focus,
                "pay_range": pay_range or [0, 0],
                "pay_unit": pay_unit,
                "key_skills": key_skills or [],
                "resume": resume,
                "applications": []
            }

            # Create seeker in database
            return await SeekerCRUD.create_seeker(seeker_data)

        except Exception:
            return None

    @staticmethod
    def extract_text_from_pdf(file_path: str | Path) -> str:
        """
        Extract text from a PDF file.

        Args:
            file_path: Path to PDF file

        Returns:
            Extracted text content

        Raises:
            Exception: If PDF cannot be read
        """
        try:
            with open(file_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            msg = f"Error extracting text from PDF: {e}"
            raise Exception(msg) from e

    @staticmethod
    def extract_text_from_docx(file_path: str | Path) -> str:
        """
        Extract text from a DOCX file.

        Args:
            file_path: Path to DOCX file

        Returns:
            Extracted text content

        Raises:
            Exception: If DOCX cannot be read
        """
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            msg = f"Error extracting text from DOCX: {e}"
            raise Exception(msg) from e

    @staticmethod
    async def upload_resume(
        seeker_id: str,
        resume_content: str | None = None,
        file_path: str | Path | None = None
    ) -> Seeker | None:
        """
        Upload or update a seeker's resume.

        Accepts either direct text content or a file path (.pdf, .docx, .txt).
        PDF and DOCX files are automatically converted to text.

        Args:
            seeker_id: Seeker's ID
            resume_content: Direct text content (optional)
            file_path: Path to resume file (optional)

        Returns:
            Updated Seeker object or None if update fails

        Raises:
            ValueError: If neither content nor file_path is provided

        Example:
            >>> # Upload text directly
            >>> seeker = await upload_resume(seeker_id, resume_content="My resume text...")
            >>> # Upload from file
            >>> seeker = await upload_resume(seeker_id, file_path="resume.pdf")
        """
        try:
            if not resume_content and not file_path:
                msg = "Either resume_content or file_path must be provided"
                raise ValueError(msg)

            # Extract text from file if file_path is provided
            if file_path:
                file_path = Path(file_path)
                suffix = file_path.suffix.lower()

                if suffix == ".pdf":
                    resume_text = SeekerService.extract_text_from_pdf(file_path)
                elif suffix == ".docx":
                    resume_text = SeekerService.extract_text_from_docx(file_path)
                elif suffix == ".txt":
                    with open(file_path, encoding="utf-8") as f:
                        resume_text = f.read()
                else:
                    msg = f"Unsupported file type: {suffix}. Use .pdf, .docx, or .txt"
                    raise ValueError(msg)
            else:
                resume_text = resume_content

            # Update seeker record
            update_data = {
                "resume": resume_text,
                "updated_at": datetime.now()
            }

            return await SeekerCRUD.update_seeker(seeker_id, update_data)

        except Exception:
            return None

    @staticmethod
    async def update_seeker_profile(
        seeker_id: str,
        update_fields: dict[str, Any]
    ) -> Seeker | None:
        """
        Update seeker profile information.

        All fields except first_name and last_name can be updated.

        Args:
            seeker_id: Seeker's ID
            update_fields: Dictionary of fields to update

        Returns:
            Updated Seeker object or None if update fails

        Example:
            >>> update_fields = {
            ...     "edu_focus": "Data Science",
            ...     "key_skills": ["Python", "Machine Learning"],
            ...     "pay_range": [80000, 120000]
            ... }
            >>> seeker = await update_seeker_profile(seeker_id, update_fields)
        """
        try:
            # Prevent updating first_name and last_name
            restricted_fields = ["first_name", "last_name"]
            for field in restricted_fields:
                update_fields.pop(field, None)

            # Add updated_at timestamp
            update_fields["updated_at"] = datetime.now()

            return await SeekerCRUD.update_seeker(seeker_id, update_fields)

        except Exception:
            return None

    @staticmethod
    async def apply_for_job(
        seeker_id: str,
        job_id: str,
        employer_id: str
    ) -> Seeker | None:
        """
        Submit a job application.

        Creates an application record with status 'Submitted' and adds it
        to the seeker's applications list.

        Args:
            seeker_id: Seeker's ID
            job_id: Job posting ID
            employer_id: Employer's ID

        Returns:
            Updated Seeker object with new application or None if fails

        Example:
            >>> seeker = await apply_for_job(seeker_id, "job_123", "employer_456")
        """
        try:
            return await SeekerCRUD.add_application(
                seeker_id=seeker_id,
                job_id=job_id,
                employer_id=employer_id,
                application_status="Submitted"
            )
        except Exception:
            return None

    @staticmethod
    async def delete_user(first_name: str, last_name: str) -> bool:
        """
        Delete a seeker account by name.

        Args:
            first_name: Seeker's first name
            last_name: Seeker's last name

        Returns:
            True if deletion successful, False otherwise

        Example:
            >>> success = await delete_user("John", "Doe")
        """
        try:
            # Find seeker by name (searching in information sub-document)
            seekers = await SeekerCRUD.get_all_seekers()
            for seeker in seekers:
                if (seeker.information.first_name == first_name and
                    seeker.information.last_name == last_name):
                    return await SeekerCRUD.delete_seeker(seeker.id)

            return False

        except Exception:
            return False

    @staticmethod
    async def delete_application(
        seeker_id: str,
        job_id: str,
        company_name: str
    ) -> Seeker | None:
        """
        Delete a specific job application from a seeker's record.

        Args:
            seeker_id: Seeker's ID
            job_id: Job posting ID
            company_name: Company name (for verification)

        Returns:
            Updated Seeker object or None if deletion fails

        Example:
            >>> seeker = await delete_application(seeker_id, "job_123", "Tech Corp")
        """
        try:
            # Get seeker
            seeker = await SeekerCRUD.get_seeker_by_id(seeker_id)
            if not seeker:
                return None

            # Find and verify the application
            original_count = len(seeker.applications)
            seeker.applications = [
                app for app in seeker.applications
                if app.job_id != job_id
            ]

            if len(seeker.applications) == original_count:
                return None

            # Save updated seeker
            await seeker.save()
            return seeker

        except Exception:
            return None

    @staticmethod
    async def search_all_jobs() -> list[dict[str, Any]]:
        """
        Search and return all available job postings from all employers.

        Returns:
            List of dictionaries containing job information

        Example:
            >>> jobs = await search_all_jobs()
            >>> for job in jobs:
            ...     print(f"{job['job_title']} at {job['company_name']}")
        """
        try:
            employers = await EmployerCRUD.get_employers_with_open_jobs()
            all_jobs = []

            for employer in employers:
                company_name = employer.company_information.company_name
                for job in employer.open_jobs:
                    job_info = {
                        "job_id": job.job_id,
                        "job_title": job.job_title,
                        "job_description": job.job_description,
                        "company_name": company_name,
                        "employer_id": str(employer.id),
                        "posted_date": job.posted_date,
                        "department": job.department,
                        "pay_range": job.pay_range,
                        "pay_unit": job.pay_unit,
                        "education_level": job.education_level,
                        "edu_focus": job.edu_focus,
                        "key_skills": job.key_skills,
                        "hiring_manager": f"{job.hire_mgr_first} {job.hire_mgr_last}"
                    }
                    all_jobs.append(job_info)

            return all_jobs

        except Exception:
            return []

    @staticmethod
    async def search_current_status(
        seeker_id: str,
        status: str
    ) -> list[dict[str, Any]]:
        """
        Search for all job applications with a specific status.

        Args:
            seeker_id: Seeker's ID
            status: Application status to search for
                   ("Submitted", "Interviewed", "Offered", "Rejected")

        Returns:
            List of applications with the specified status

        Example:
            >>> apps = await search_current_status(seeker_id, "Interviewed")
        """
        try:
            seeker = await SeekerCRUD.get_seeker_by_id(seeker_id)
            if not seeker:
                return []

            matching_applications = []
            for app in seeker.applications:
                if app.application_status == status:
                    app_info = {
                        "job_id": app.job_id,
                        "employer_id": app.employer_id,
                        "date_applied": app.date_applied,
                        "application_status": app.application_status
                    }
                    matching_applications.append(app_info)

            return matching_applications

        except Exception:
            return []

    @staticmethod
    async def search_by_parameter(
        parameter_type: str,
        search_value: str
    ) -> list[dict[str, Any]]:
        """
        Search jobs by parameter (job title, company name, or skill).

        Args:
            parameter_type: Type of search ("jobtitle", "companyname", "skill")
            search_value: Value to search for

        Returns:
            List of matching job postings

        Example:
            >>> jobs = await search_by_parameter("jobtitle", "Software Engineer")
            >>> jobs = await search_by_parameter("skill", "Python")
        """
        try:
            all_employers = await EmployerCRUD.get_all_employers()
            matching_jobs = []

            for employer in all_employers:
                company_name = employer.company_information.company_name

                for job in employer.open_jobs:
                    match_found = False

                    # Search by job title
                    if parameter_type.lower() == "jobtitle":
                        if search_value.lower() in job.job_title.lower():
                            match_found = True

                    # Search by company name
                    elif parameter_type.lower() == "companyname":
                        if search_value.lower() in company_name.lower():
                            match_found = True

                    # Search by skill
                    elif parameter_type.lower() == "skill":
                        for skill in job.key_skills:
                            if search_value.lower() in skill.lower():
                                match_found = True
                                break

                    # Add job to results if match found
                    if match_found:
                        job_info = {
                            "job_id": job.job_id,
                            "job_title": job.job_title,
                            "job_description": job.job_description,
                            "company_name": company_name,
                            "employer_id": str(employer.id),
                            "posted_date": job.posted_date,
                            "department": job.department,
                            "pay_range": job.pay_range,
                            "pay_unit": job.pay_unit,
                            "education_level": job.education_level,
                            "edu_focus": job.edu_focus,
                            "key_skills": job.key_skills,
                            "hiring_manager": f"{job.hire_mgr_first} {job.hire_mgr_last}"
                        }
                        matching_jobs.append(job_info)

            return matching_jobs

        except Exception:
            return []


# Convenience function aliases
create_new_seeker = SeekerService.create_new_seeker
upload_resume = SeekerService.upload_resume
update_seeker_profile = SeekerService.update_seeker_profile
apply_for_job = SeekerService.apply_for_job
delete_user = SeekerService.delete_user
delete_application = SeekerService.delete_application
search_all_jobs = SeekerService.search_all_jobs
search_current_status = SeekerService.search_current_status
search_by_parameter = SeekerService.search_by_parameter


# Example usage
if __name__ == "__main__":
    import asyncio

    from backend.db.settings import close_mongodb_connection, connect_to_mongodb

    async def test_seeker_services():
        """Test seeker services."""

        await connect_to_mongodb()

        try:
            # Test 1: Create new seeker
            new_seeker = await create_new_seeker(
                first_name="Service",
                last_name="Test",
                email=f"service.test.{asyncio.get_event_loop().time()}@example.com",
                phone="+12025550199",
                street="789 Service St",
                city="Test City",
                state="CA",
                zip_code="90210",
                password_hash="hashed_password_123456",
                education_level="MS",
                edu_focus="Software Engineering",
                pay_range=[90000, 130000],
                key_skills=["Python", "FastAPI", "MongoDB"]
            )

            if new_seeker:
                test_seeker_id = str(new_seeker.id)
            else:
                return

            # Test 2: Upload resume (text)
            updated_seeker = await upload_resume(
                test_seeker_id,
                resume_content="This is my resume. I have 5 years of experience..."
            )
            if updated_seeker and updated_seeker.resume:
                pass
            else:
                pass

            # Test 3: Search all jobs
            await search_all_jobs()

            # Test 4: Delete user
            deleted = await delete_user("Service", "Test")
            if deleted:
                pass
            else:
                pass


        except Exception:
            import traceback
            traceback.print_exc()

        finally:
            await close_mongodb_connection()

    asyncio.run(test_seeker_services())

