"""
Seeker Job Matching Service

This module provides the core matching logic for matching job seekers to job postings.
It uses ChromaDB for vector similarity search and LangChain for detailed scoring.
"""

from typing import Any

from loguru import logger

from backend.ai.chains.scoring_chain import get_scoring_chain
from backend.ai.rag.vector_store import get_vector_store
from backend.db.employer_db_ops import EmployerCRUD
from backend.db.seeker_db_ops import SeekerCRUD


class MatchingService:
    """
    Service for matching job seekers to job postings.

    Uses ChromaDB for initial vector similarity search, then LangChain
    for detailed scoring and ranking.
    """

    def __init__(self):
        """Initialize the matching service with vector store and scoring chain."""
        self.vector_store = get_vector_store()
        self.scoring_chain = get_scoring_chain()

    async def get_seeker_embedding(self, seeker_id: str) -> list[float] | None:
        """
        Retrieve seeker embedding from ChromaDB.

        Args:
            seeker_id: Seeker's MongoDB ObjectId as string

        Returns:
            Embedding vector or None if not found
        """
        try:
            seeker_data = self.vector_store.get_seeker_by_id(seeker_id)
            if seeker_data and "embedding" in seeker_data and seeker_data["embedding"] is not None:
                return seeker_data["embedding"]
            logger.warning(f"Seeker embedding not found for ID: {seeker_id}")
            return None
        except Exception as e:
            logger.error(f"Error retrieving seeker embedding: {e}")
            return None

    async def search_similar_jobs(
        self,
        query_embedding: list[float],
        n_results: int = 20
    ) -> list[dict[str, Any]]:
        """
        Search for similar jobs using vector similarity.

        Args:
            query_embedding: Seeker's embedding vector
            n_results: Number of results to return

        Returns:
            List of job matches with metadata
        """
        try:
            results = self.vector_store.search_similar_jobs(
                query_embedding=query_embedding,
                n_results=n_results
            )

            # Format results
            matches = []
            if results and "ids" in results and results["ids"]:
                ids = results["ids"][0] if isinstance(results["ids"][0], list) else results["ids"]
                metadatas = results.get("metadatas", [[]])[0] if results.get("metadatas") else []
                distances = results.get("distances", [[]])[0] if results.get("distances") else []

                for idx, job_id in enumerate(ids):
                    metadata = metadatas[idx] if idx < len(metadatas) else {}
                    distance = distances[idx] if idx < len(distances) else None

                    matches.append({
                        "job_id": job_id,
                        "metadata": metadata,
                        "distance": distance,
                        "similarity_score": 1 - distance if distance is not None else None
                    })

            return matches
        except Exception as e:
            logger.error(f"Error searching similar jobs: {e}")
            return []

    async def fetch_job_details(self, job_identification: str) -> dict[str, Any] | None:
        """
        Fetch full job details from MongoDB using job_identification UUID.

        Args:
            job_identification: Job's UUID from ChromaDB

        Returns:
            Dictionary with job details or None if not found
        """
        try:
            # Search through all employers to find the job
            employers = await EmployerCRUD.get_all_employers(limit=1000)

            for employer in employers:
                for job in employer.open_jobs:
                    if str(job.job_identification) == job_identification:
                        return {
                            "job_id": str(job.job_identification),
                            "job_title": job.job_title,
                            "job_description": job.job_description,
                            "employer_id": str(employer.employer_identification),
                            "company_name": employer.company_information.company_name,
                            "key_skills": job.key_skills,
                            "education_level": job.education_level,
                            "edu_focus": job.edu_focus,
                            "pay_range": job.pay_range,
                            "pay_unit": job.pay_unit,
                            "current_status": job.current_status,
                            "department": job.department,
                            "posted_date": job.posted_date,
                            "hire_mgr_first": job.hire_mgr_first,
                            "hire_mgr_last": job.hire_mgr_last
                        }

            logger.warning(f"Job not found: {job_identification}")
            return None
        except Exception as e:
            logger.error(f"Error fetching job details: {e}")
            return None

    async def calculate_match_score(
        self,
        seeker_data: dict[str, Any],
        job_data: dict[str, Any]
    ) -> float:
        """
        Calculate match score between seeker and job using LangChain.

        Args:
            seeker_data: Seeker profile data
            job_data: Job posting data

        Returns:
            Match score (0-100)
        """
        try:
            score_breakdown = await self.scoring_chain.calculate_match_score(
                seeker_data=seeker_data,
                job_data=job_data
            )
            return score_breakdown.overall_score
        except Exception as e:
            logger.error(f"Error calculating match score: {e}")
            return 0.0

    async def match_seeker_to_jobs(
        self,
        seeker_id: str,
        n_results: int = 20,
        min_score: float = 0.0
    ) -> list[dict[str, Any]]:
        """
        Match a seeker to jobs with percentage scores.

        Process:
        1. Get seeker details from MongoDB
        2. Get seeker embedding from ChromaDB using seeker_identification
        3. Query ChromaDB for similar jobs
        4. For each job, fetch full details from MongoDB
        5. Use LangChain to analyze match factors and calculate score
        6. Filter to only active jobs (current_status == "Posted")
        7. Sort by match score (descending)

        Args:
            seeker_id: Seeker's MongoDB ObjectId as string
            n_results: Maximum number of results to return
            min_score: Minimum match score threshold (0-100)

        Returns:
            List of job recommendations with match scores, sorted by score (descending)
            Each recommendation contains:
                - job_id: str
                - job_title: str
                - company_name: str
                - employer_id: str
                - match_score: float (0-100)
                - score_breakdown: dict
                - job_description: str
                - ... other job fields
        """
        try:
            logger.info(f"[RECOMMENDATIONS] Starting match for seeker_id: {seeker_id}")
            
            # 1. Get seeker full details from MongoDB
            seeker = await SeekerCRUD.get_seeker_by_id(seeker_id)
            if not seeker:
                logger.warning(f"[RECOMMENDATIONS] Seeker not found in MongoDB: {seeker_id}")
                return []
            
            logger.info(f"[RECOMMENDATIONS] Found seeker in MongoDB: {seeker.information.email}")
            
            # 2. Get seeker embedding from ChromaDB using seeker_identification
            seeker_identification = seeker.seeker_identification
            logger.info(f"[RECOMMENDATIONS] Seeker identification UUID: {seeker_identification}")
            
            if not seeker_identification:
                logger.warning(f"[RECOMMENDATIONS] Seeker has no seeker_identification: {seeker_id}")
                return []
            
            seeker_embedding = await self.get_seeker_embedding(str(seeker_identification))
            if seeker_embedding is None or len(seeker_embedding) == 0:
                logger.warning(f"[RECOMMENDATIONS] No embedding found for seeker_identification: {seeker_identification}")
                return []
            
            logger.info(f"[RECOMMENDATIONS] Found seeker embedding in ChromaDB")

            seeker_data = {
                "key_skills": seeker.key_skills,
                "education_level": seeker.education_level,
                "edu_focus": seeker.edu_focus,
                "pay_range": seeker.pay_range,
                "pay_unit": seeker.pay_unit,
                "resume": seeker.resume or ""
            }

            # 3. Query ChromaDB for similar jobs
            job_matches = await self.search_similar_jobs(
                query_embedding=seeker_embedding,
                n_results=n_results * 2  # Get more to filter later
            )

            if not job_matches or len(job_matches) == 0:
                logger.info(f"No similar jobs found for seeker: {seeker_id}")
                return []

            # Deduplicate jobs by job_id before processing
            seen_job_ids = set()
            unique_job_matches = []
            for match in job_matches:
                job_id = match.get("job_id")
                if job_id and job_id not in seen_job_ids:
                    seen_job_ids.add(job_id)
                    unique_job_matches.append(match)
            
            logger.info(f"[RECOMMENDATIONS] Deduplicated to {len(unique_job_matches)} unique jobs (from {len(job_matches)} results)")

            # 4. Fetch full job details and calculate scores
            recommendations = []
            processed_job_ids = set()

            for match in unique_job_matches:
                job_id = match["job_id"]
                
                # Skip if we've already processed this job
                if job_id in processed_job_ids:
                    logger.debug(f"[RECOMMENDATIONS] Skipping duplicate job: {job_id}")
                    continue
                
                job_details = await self.fetch_job_details(job_id)

                if not job_details:
                    continue

                # Filter to only active jobs
                if job_details.get("current_status") != "Posted":
                    continue

                # Mark as processed before calculating score
                processed_job_ids.add(job_id)

                # 5. Calculate match score using LangChain
                job_data = {
                    "job_title": job_details["job_title"],
                    "key_skills": job_details["key_skills"],
                    "education_level": job_details["education_level"],
                    "edu_focus": job_details["edu_focus"],
                    "pay_range": job_details["pay_range"],
                    "pay_unit": job_details["pay_unit"],
                    "job_description": job_details["job_description"]
                }

                try:
                    score_breakdown = await self.scoring_chain.calculate_match_score(
                        seeker_data=seeker_data,
                        job_data=job_data
                    )

                    match_score = score_breakdown.overall_score

                    # Filter by minimum score
                    if match_score < min_score:
                        continue

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
                        "department": job_details.get("department", ""),
                        "posted_date": job_details.get("posted_date"),
                        "hire_mgr_first": job_details.get("hire_mgr_first", ""),
                        "hire_mgr_last": job_details.get("hire_mgr_last", "")
                    }

                    recommendations.append(recommendation)

                except Exception as e:
                    logger.error(f"Error calculating score for job {job_id}: {e}")
                    continue

            # 6. Sort by match score (descending)
            recommendations.sort(key=lambda x: x["match_score"], reverse=True)

            # Limit to n_results
            recommendations = recommendations[:n_results]

            logger.info(f"Found {len(recommendations)} job recommendations for seeker {seeker_id}")
            return recommendations

        except Exception as e:
            logger.error(f"Error matching seeker to jobs: {e}")
            return []


# Global matching service instance
_matching_service: MatchingService | None = None


def get_matching_service() -> MatchingService:
    """Get or create the global matching service instance."""
    global _matching_service  # noqa: PLW0603

    if _matching_service is None:
        _matching_service = MatchingService()

    return _matching_service

