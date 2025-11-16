"""
Candidate Matching Service

This module provides matching logic for employers to find suitable candidates
for their job postings. It uses ChromaDB for vector similarity search and
LangChain for detailed scoring.
"""

import asyncio
import hashlib
import json
from typing import Any

from loguru import logger

from backend.ai.chains.scoring_chain import get_scoring_chain
from backend.ai.rag.vector_store import get_vector_store
from backend.db.employer_db_ops import EmployerCRUD
from backend.db.seeker_db_ops import SeekerCRUD


class CandidateMatchingService:
    """
    Service for matching candidates to job postings.

    Uses ChromaDB for initial vector similarity search, then LangChain
    for detailed scoring and ranking.
    """

    def __init__(self):
        """Initialize the candidate matching service with vector store and scoring chain."""
        self.vector_store = get_vector_store()
        self.scoring_chain = get_scoring_chain()
        self._score_cache = {}  # In-memory cache for match scores

    async def get_job_embedding(self, job_id: str) -> list[float] | None:
        """
        Retrieve job embedding from ChromaDB.

        Args:
            job_id: Job's MongoDB ObjectId as string

        Returns:
            Embedding vector or None if not found
        """
        try:
            job_data = self.vector_store.get_job_by_id(job_id)
            if job_data and job_data.get("embedding") is not None:
                embedding = job_data["embedding"]
                # Check if embedding has data (ChromaDB returns numpy arrays or lists)
                if hasattr(embedding, '__len__') and len(embedding) > 0:
                    return embedding
            logger.warning(f"Job embedding not found for ID: {job_id}")
            return None
        except Exception as e:
            logger.error(f"Error retrieving job embedding: {e}")
            return None

    async def search_similar_seekers(
        self,
        query_embedding: list[float],
        n_results: int = 50
    ) -> list[dict[str, Any]]:
        """
        Search for similar seekers using vector similarity.

        Args:
            query_embedding: Job's embedding vector
            n_results: Number of results to return

        Returns:
            List of seeker matches with metadata
        """
        try:
            results = self.vector_store.search_similar_seekers(
                query_embedding=query_embedding,
                n_results=n_results
            )

            # Format results
            matches = []
            if results and "ids" in results and results["ids"]:
                ids = results["ids"][0] if isinstance(results["ids"][0], list) else results["ids"]
                metadatas = results.get("metadatas", [[]])[0] if results.get("metadatas") else []
                distances = results.get("distances", [[]])[0] if results.get("distances") else []

                for idx, seeker_id in enumerate(ids):
                    metadata = metadatas[idx] if idx < len(metadatas) else {}
                    distance = distances[idx] if idx < len(distances) else None

                    matches.append({
                        "seeker_id": seeker_id,
                        "metadata": metadata,
                        "distance": distance,
                        "similarity_score": 1 - distance if distance is not None else None
                    })

            return matches
        except Exception as e:
            logger.error(f"Error searching similar seekers: {e}")
            return []

    async def fetch_seeker_details(self, seeker_uuid: str) -> dict[str, Any] | None:
        """
        Fetch full seeker details from MongoDB.

        Args:
            seeker_uuid: Seeker's UUID as string (from ChromaDB)

        Returns:
            Dictionary with seeker details or None if not found
        """
        try:
            seeker = await SeekerCRUD.get_seeker_by_uuid(seeker_uuid)
            if not seeker:
                logger.warning(f"Seeker not found in MongoDB for UUID: {seeker_uuid}")
                return None

            return {
                "seeker_id": str(seeker.seeker_id),
                "first_name": seeker.information.first_name,
                "last_name": seeker.information.last_name,
                "email": str(seeker.information.email),
                "key_skills": seeker.key_skills,
                "education_level": seeker.education_level,
                "edu_focus": seeker.edu_focus,
                "pay_range": seeker.pay_range,
                "pay_unit": seeker.pay_unit,
                "resume": seeker.resume or "",
                "phone": str(seeker.information.phone),
                "address": {
                    "street": seeker.information.address.street,
                    "city": seeker.information.address.city,
                    "state": seeker.information.address.state,
                    "zip_code": seeker.information.address.zip_code
                }
            }
        except Exception as e:
            logger.error(f"Error fetching seeker details: {e}")
            return None

    async def check_seeker_applied(
        self,
        employer_id: str,
        job_id: str,
        seeker_id: str
    ) -> bool:
        """
        Check if a seeker has already applied for the job.

        Args:
            employer_id: Employer's MongoDB ObjectId as string
            job_id: Job's MongoDB ObjectId as string
            seeker_id: Seeker's MongoDB ObjectId as string

        Returns:
            True if seeker has applied, False otherwise
        """
        try:
            employer = await EmployerCRUD.get_employer_by_id(employer_id)
            if not employer:
                return False

            for app in employer.apps_received:
                if app.applicant_id == seeker_id and app.job_id == job_id:
                    return True

            return False
        except Exception as e:
            logger.error(f"Error checking application status: {e}")
            return False

    def _get_cache_key(self, seeker_data: dict, job_data: dict) -> str:
        """
        Generate cache key from seeker and job data.

        Args:
            seeker_data: Seeker information
            job_data: Job information

        Returns:
            MD5 hash of combined data for cache lookup
        """
        combined = {
            "seeker": {
                "skills": sorted(seeker_data.get("key_skills", [])),
                "education": seeker_data.get("education_level", ""),
                "pay": seeker_data.get("pay_range", [])
            },
            "job": {
                "skills": sorted(job_data.get("key_skills", [])),
                "education": job_data.get("education_level", ""),
                "pay": job_data.get("pay_range", [])
            }
        }
        return hashlib.md5(json.dumps(combined, sort_keys=True).encode()).hexdigest()

    async def _calculate_score_with_cache(
        self,
        seeker_data: dict,
        job_data: dict
    ):
        """
        Calculate match score with caching to avoid redundant LLM calls.

        Args:
            seeker_data: Seeker information
            job_data: Job information

        Returns:
            Score breakdown from LLM or cache
        """
        cache_key = self._get_cache_key(seeker_data, job_data)

        if cache_key in self._score_cache:
            logger.debug(f"Cache hit for match calculation: {cache_key}")
            return self._score_cache[cache_key]

        # Calculate and cache
        logger.debug(f"Cache miss - calculating score: {cache_key}")
        score_breakdown = await self.scoring_chain.calculate_match_score(
            seeker_data=seeker_data,
            job_data=job_data
        )

        self._score_cache[cache_key] = score_breakdown
        return score_breakdown

    async def _process_single_candidate(
        self,
        match: dict,
        job_data: dict,
        employer_id: str,
        job_id: str,
        min_score: float
    ) -> dict | None:
        """
        Process a single candidate match (for parallel processing).

        Args:
            match: Candidate match from vector search
            job_data: Job information
            employer_id: Employer's ID
            job_id: Job's ID
            min_score: Minimum score threshold

        Returns:
            Candidate recommendation dict or None if filtered out
        """
        try:
            seeker_id = match["seeker_id"]
            seeker_details = await self.fetch_seeker_details(seeker_id)

            if not seeker_details:
                return None

            # Prepare seeker data for scoring
            seeker_data = {
                "key_skills": seeker_details["key_skills"],
                "education_level": seeker_details["education_level"],
                "edu_focus": seeker_details["edu_focus"],
                "pay_range": seeker_details["pay_range"],
                "pay_unit": seeker_details["pay_unit"],
                "resume": seeker_details["resume"]
            }

            # Calculate match score (with caching)
            score_breakdown = await self._calculate_score_with_cache(
                seeker_data=seeker_data,
                job_data=job_data
            )

            match_score = score_breakdown.overall_score

            # Filter by minimum score
            if match_score < min_score:
                logger.debug(f"Candidate {seeker_id} filtered out: score {match_score} < {min_score}")
                return None

            # Check if seeker has applied
            has_applied = await self.check_seeker_applied(
                employer_id=employer_id,
                job_id=job_id,
                seeker_id=seeker_id
            )

            # Get resume preview
            resume_preview = seeker_details["resume"][:500] if seeker_details["resume"] else "No resume provided"

            return {
                "seeker_id": seeker_details["seeker_id"],
                "first_name": seeker_details["first_name"],
                "last_name": seeker_details["last_name"],
                "email": seeker_details["email"],
                "match_score": match_score,
                "score_breakdown": {
                    "skills_score": score_breakdown.skills_score,
                    "education_score": score_breakdown.education_score,
                    "pay_score": score_breakdown.pay_score,
                    "experience_score": score_breakdown.experience_score,
                    "reasoning": score_breakdown.reasoning
                },
                "has_applied": has_applied,
                "resume_preview": resume_preview,
                "key_skills": seeker_details["key_skills"],
                "education_level": seeker_details["education_level"],
                "edu_focus": seeker_details["edu_focus"],
                "pay_range": seeker_details["pay_range"],
                "pay_unit": seeker_details["pay_unit"],
                "phone": seeker_details["phone"],
                "address": seeker_details["address"]
            }
        except Exception as e:
            logger.error(f"Error processing candidate {match.get('seeker_id')}: {e}")
            return None

    async def match_job_to_candidates(
        self,
        job_id: str,
        employer_id: str,
        n_results: int = 20,
        min_score: float = 0.0
    ) -> list[dict[str, Any]]:
        """
        Match a job posting to candidates with percentage scores.

        Process:
        1. Get job embedding from ChromaDB
        2. Query ChromaDB for similar seekers
        3. For each seeker, fetch full details from MongoDB
        4. Use LangChain to analyze match factors and calculate score
        5. Check if seeker has applied (from apps_received array)
        6. Sort by match score (descending)

        Args:
            job_id: Job's MongoDB ObjectId as string
            employer_id: Employer's MongoDB ObjectId as string
            n_results: Maximum number of results to return
            min_score: Minimum match score threshold (0-100)

        Returns:
            List of candidate recommendations with match scores, sorted by score (descending)
            Each recommendation contains:
                - seeker_id: str
                - first_name: str
                - last_name: str
                - email: str
                - match_score: float (0-100)
                - score_breakdown: dict
                - has_applied: bool
                - resume_preview: str
                - ... other seeker fields
        """
        try:
            # 1. Get job full details from MongoDB first to get the UUID
            employer = await EmployerCRUD.get_employer_by_id(employer_id)
            if not employer:
                logger.warning(f"Employer not found: {employer_id}")
                return []

            job = None
            for open_job in employer.open_jobs:
                if str(open_job.job_id) == job_id:
                    job = open_job
                    break

            if not job:
                logger.warning(f"Job not found: {job_id}")
                return []

            # 2. Get job embedding from ChromaDB using the job's UUID
            job_uuid = str(job.job_identification)
            logger.info(f"Looking up job in ChromaDB with UUID: {job_uuid}")
            job_embedding = await self.get_job_embedding(job_uuid)
            if job_embedding is None or (hasattr(job_embedding, '__len__') and len(job_embedding) == 0):
                logger.warning(f"No embedding found for job UUID: {job_uuid}")
                return []

            job_data = {
                "job_title": job.job_title,
                "key_skills": job.key_skills,
                "education_level": job.education_level,
                "edu_focus": job.edu_focus,
                "pay_range": job.pay_range,
                "pay_unit": job.pay_unit,
                "job_description": job.job_description
            }

            # 3. Query ChromaDB for similar seekers
            seeker_matches = await self.search_similar_seekers(
                query_embedding=job_embedding,
                n_results=n_results * 2  # Get more to filter later
            )

            if not seeker_matches:
                logger.info(f"No similar seekers found for job: {job_id}")
                return []

            # 4. Fetch full seeker details and calculate scores IN PARALLEL
            recommendations = []

            # Process in batches to avoid overwhelming the LLM API
            # Batch size of 5 allows parallel processing while respecting rate limits
            batch_size = 5
            logger.info(f"Processing {len(seeker_matches)} candidates in batches of {batch_size}")

            for i in range(0, len(seeker_matches), batch_size):
                batch = seeker_matches[i:i + batch_size]
                logger.debug(f"Processing batch {i//batch_size + 1} ({len(batch)} candidates)")

                # Process entire batch in parallel
                tasks = [
                    self._process_single_candidate(
                        match=match,
                        job_data=job_data,
                        employer_id=employer_id,
                        job_id=job_id,
                        min_score=min_score
                    )
                    for match in batch
                ]

                # Wait for all candidates in batch to complete
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)

                # Filter out None results and exceptions
                for result in batch_results:
                    if result and not isinstance(result, Exception):
                        recommendations.append(result)
                    elif isinstance(result, Exception):
                        logger.error(f"Exception in batch processing: {result}")

            # 7. Sort by match score (descending)
            recommendations.sort(key=lambda x: x["match_score"], reverse=True)

            # Limit to n_results
            recommendations = recommendations[:n_results]

            logger.info(f"Found {len(recommendations)} candidate recommendations for job {job_id}")
            return recommendations

        except Exception as e:
            logger.error(f"Error matching job to candidates: {e}")
            return []


# Global candidate matching service instance
_candidate_matching_service: CandidateMatchingService | None = None


def get_candidate_matching_service() -> CandidateMatchingService:
    """Get or create the global candidate matching service instance."""
    global _candidate_matching_service  # noqa: PLW0603

    if _candidate_matching_service is None:
        _candidate_matching_service = CandidateMatchingService()

    return _candidate_matching_service

