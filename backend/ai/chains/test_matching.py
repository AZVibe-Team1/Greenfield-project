"""
Unit Tests for Matching Services

Tests for scoring chain, seeker matching service, and candidate matching service.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.ai.chains.candidate_matching_service import CandidateMatchingService
from backend.ai.chains.matching_service import MatchingService
from backend.ai.chains.scoring_chain import MatchScoreBreakdown, ScoringChain


class TestScoringChain:
    """Tests for ScoringChain."""

    @pytest.fixture
    def scoring_chain(self):
        """Create a ScoringChain instance for testing."""
        with patch("backend.ai.chains.scoring_chain.get_llm_client"):
            return ScoringChain()

    @pytest.mark.asyncio
    async def test_calculate_match_score_valid_input(self, scoring_chain):
        """Test match score calculation with valid input."""
        seeker_data = {
            "key_skills": ["Python", "FastAPI", "MongoDB"],
            "education_level": "BS",
            "edu_focus": "Computer Science",
            "pay_range": [60000, 90000],
            "pay_unit": "Yearly",
            "resume": "Experienced software engineer with 5 years in Python development."
        }

        job_data = {
            "job_title": "Senior Software Engineer",
            "key_skills": ["Python", "FastAPI", "Docker"],
            "education_level": "BS",
            "edu_focus": "Computer Science",
            "pay_range": [80000, 120000],
            "pay_unit": "Yearly",
            "job_description": "We are looking for an experienced Python developer."
        }

        # Mock the LLM response
        mock_breakdown = MatchScoreBreakdown(
            skills_score=85.0,
            education_score=100.0,
            pay_score=80.0,
            experience_score=75.0,
            overall_score=85.0,
            reasoning="Strong skills match, perfect education alignment, good pay compatibility."
        )

        with patch.object(scoring_chain, "prompt") as mock_prompt:
            mock_chain = AsyncMock()
            mock_chain.ainvoke = AsyncMock(return_value=mock_breakdown)
            mock_prompt.__or__ = MagicMock(return_value=mock_chain)

            result = await scoring_chain.calculate_match_score(seeker_data, job_data)

            assert result.overall_score == 85.0
            assert result.skills_score == 85.0
            assert result.education_score == 100.0
            assert isinstance(result.reasoning, str)

    @pytest.mark.asyncio
    async def test_calculate_match_score_missing_fields(self, scoring_chain):
        """Test that missing required fields raise ValueError."""
        seeker_data = {
            "key_skills": ["Python"],
            # Missing other required fields
        }

        job_data = {
            "job_title": "Software Engineer",
            # Missing other required fields
        }

        with pytest.raises(ValueError):
            await scoring_chain.calculate_match_score(seeker_data, job_data)


class TestMatchingService:
    """Tests for MatchingService."""

    @pytest.fixture
    def matching_service(self):
        """Create a MatchingService instance for testing."""
        with patch("backend.ai.chains.matching_service.get_vector_store"), \
             patch("backend.ai.chains.matching_service.get_scoring_chain"):
            return MatchingService()

    @pytest.mark.asyncio
    async def test_get_seeker_embedding_found(self, matching_service):
        """Test retrieving seeker embedding when found."""
        mock_embedding = [0.1] * 1536
        mock_vector_store = MagicMock()
        mock_vector_store.get_seeker_by_id.return_value = {
            "embedding": mock_embedding,
            "metadata": {},
            "document": "test"
        }
        matching_service.vector_store = mock_vector_store

        result = await matching_service.get_seeker_embedding("seeker_123")

        assert result == mock_embedding
        mock_vector_store.get_seeker_by_id.assert_called_once_with("seeker_123")

    @pytest.mark.asyncio
    async def test_get_seeker_embedding_not_found(self, matching_service):
        """Test retrieving seeker embedding when not found."""
        mock_vector_store = MagicMock()
        mock_vector_store.get_seeker_by_id.return_value = None
        matching_service.vector_store = mock_vector_store

        result = await matching_service.get_seeker_embedding("seeker_123")

        assert result is None

    @pytest.mark.asyncio
    async def test_search_similar_jobs(self, matching_service):
        """Test searching for similar jobs."""
        mock_results = {
            "ids": [["job_1", "job_2"]],
            "metadatas": [[{"title": "Job 1"}, {"title": "Job 2"}]],
            "distances": [[0.1, 0.2]]
        }

        mock_vector_store = MagicMock()
        mock_vector_store.search_similar_jobs.return_value = mock_results
        matching_service.vector_store = mock_vector_store

        query_embedding = [0.1] * 1536
        results = await matching_service.search_similar_jobs(query_embedding, n_results=2)

        assert len(results) == 2
        assert results[0]["job_id"] == "job_1"
        assert results[0]["similarity_score"] == 0.9  # 1 - 0.1
        assert results[1]["job_id"] == "job_2"

    @pytest.mark.asyncio
    async def test_fetch_job_details(self, matching_service):
        """Test fetching job details from MongoDB."""
        from backend.schemas.employer import Employer, OpenJob, CompanyInformation
        from datetime import datetime
        from zoneinfo import ZoneInfo

        mock_job = OpenJob(
            job_id="job_123",
            employer_identification="emp_uuid",
            job_title="Software Engineer",
            job_description="Test job",
            posted_date=datetime.now(ZoneInfo("America/Denver")),
            department="Engineering",
            hire_mgr_first="John",
            hire_mgr_last="Doe",
            pay_range=[80000, 120000],
            pay_unit="Yearly",
            education_level="BS",
            edu_focus="Computer Science",
            key_skills=["Python", "FastAPI"]
        )

        mock_employer = MagicMock()
        mock_employer.employer_id = "emp_123"
        mock_employer.company_information.company_name = "Test Corp"
        mock_employer.open_jobs = [mock_job]

        with patch("backend.ai.chains.matching_service.EmployerCRUD.get_all_employers") as mock_get:
            mock_get.return_value = [mock_employer]

            result = await matching_service.fetch_job_details("job_123")

            assert result is not None
            assert result["job_id"] == "job_123"
            assert result["job_title"] == "Software Engineer"
            assert result["company_name"] == "Test Corp"


class TestCandidateMatchingService:
    """Tests for CandidateMatchingService."""

    @pytest.fixture
    def candidate_service(self):
        """Create a CandidateMatchingService instance for testing."""
        with patch("backend.ai.chains.candidate_matching_service.get_vector_store"), \
             patch("backend.ai.chains.candidate_matching_service.get_scoring_chain"):
            return CandidateMatchingService()

    @pytest.mark.asyncio
    async def test_get_job_embedding_found(self, candidate_service):
        """Test retrieving job embedding when found."""
        mock_embedding = [0.2] * 1536
        mock_vector_store = MagicMock()
        mock_vector_store.get_job_by_id.return_value = {
            "embedding": mock_embedding,
            "metadata": {},
            "document": "test job"
        }
        candidate_service.vector_store = mock_vector_store

        result = await candidate_service.get_job_embedding("job_123")

        assert result == mock_embedding

    @pytest.mark.asyncio
    async def test_check_seeker_applied_true(self, candidate_service):
        """Test checking if seeker has applied (returns True)."""
        from backend.schemas.employer import ApplicationReceived, CandidateTracking
        from datetime import datetime
        from zoneinfo import ZoneInfo

        mock_app = ApplicationReceived(
            applicant_id="seeker_123",
            job_id="job_456",
            candidate_tracking=CandidateTracking(current_status="Received")
        )

        mock_employer = MagicMock()
        mock_employer.apps_received = [mock_app]

        with patch("backend.ai.chains.candidate_matching_service.EmployerCRUD.get_employer_by_id") as mock_get:
            mock_get.return_value = mock_employer

            result = await candidate_service.check_seeker_applied(
                "emp_123", "job_456", "seeker_123"
            )

            assert result is True

    @pytest.mark.asyncio
    async def test_check_seeker_applied_false(self, candidate_service):
        """Test checking if seeker has applied (returns False)."""
        mock_employer = MagicMock()
        mock_employer.apps_received = []

        with patch("backend.ai.chains.candidate_matching_service.EmployerCRUD.get_employer_by_id") as mock_get:
            mock_get.return_value = mock_employer

            result = await candidate_service.check_seeker_applied(
                "emp_123", "job_456", "seeker_123"
            )

            assert result is False


# Integration test example (requires actual database connections)
@pytest.mark.integration
class TestMatchingIntegration:
    """Integration tests for matching services (requires DB connections)."""

    @pytest.mark.asyncio
    async def test_end_to_end_seeker_matching(self):
        """Test end-to-end seeker to job matching."""
        # This would require actual database setup
        # Skip for unit tests, implement in integration test suite
        pytest.skip("Requires database connection")

    @pytest.mark.asyncio
    async def test_end_to_end_candidate_matching(self):
        """Test end-to-end job to candidate matching."""
        # This would require actual database setup
        # Skip for unit tests, implement in integration test suite
        pytest.skip("Requires database connection")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

