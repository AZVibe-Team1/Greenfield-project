"""
LangChain Scoring Chain Module

This module provides LLM-based scoring analysis for matching seekers to jobs
and jobs to candidates. Uses gpt-4o-mini to analyze match factors and return
structured scores (0-100%) with detailed breakdowns.
"""

from typing import Any

from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from loguru import logger
from pydantic import BaseModel, Field

from backend.core.ai_config import AIConfig, get_llm_client


class MatchScoreBreakdown(BaseModel):
    """
    Detailed breakdown of match score components.

    Attributes:
        skills_score: Skills overlap score (0-100)
        education_score: Education compatibility score (0-100)
        pay_score: Pay range alignment score (0-100)
        experience_score: Experience relevance score (0-100)
        overall_score: Composite score (0-100)
        reasoning: Explanation of the scoring
    """
    skills_score: float = Field(..., ge=0, le=100, description="Skills overlap score")
    education_score: float = Field(..., ge=0, le=100, description="Education compatibility score")
    pay_score: float = Field(..., ge=0, le=100, description="Pay range alignment score")
    experience_score: float = Field(..., ge=0, le=100, description="Experience relevance score")
    overall_score: float = Field(..., ge=0, le=100, description="Composite match score")
    reasoning: str = Field(..., description="Explanation of the scoring")


class ScoringChain:
    """
    LangChain chain for analyzing and scoring job-seeker matches.

    Uses gpt-4o-mini to analyze match factors and return structured scores.
    """

    def __init__(self):
        """Initialize the scoring chain with LLM client and prompt template."""
        self.llm = get_llm_client()
        self.parser = PydanticOutputParser(pydantic_object=MatchScoreBreakdown)
        self._setup_prompt()

    def _setup_prompt(self) -> None:
        """Set up the prompt template for match analysis."""
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert job matching analyst. Your task is to analyze 
the compatibility between a job seeker and a job posting, considering the following factors:

1. **Skills Match**: How well do the seeker's skills align with the job requirements?
2. **Education Compatibility**: Does the seeker's education level and focus match the job requirements?
3. **Pay Range Alignment**: Is the job's pay range compatible with the seeker's expectations?
4. **Experience Relevance**: How relevant is the seeker's experience to the job requirements?

For each factor, provide a score from 0-100, where:
- 0-40: Poor match
- 41-70: Moderate match
- 71-85: Good match
- 86-100: Excellent match

Calculate an overall_score as a weighted average:
- Skills: 40% weight
- Education: 20% weight
- Pay: 20% weight
- Experience: 20% weight

Provide clear reasoning for each score.

{format_instructions}"""),
            ("human", """Analyze the match between this job seeker and job posting:

**Job Seeker Profile:**
- Skills: {seeker_skills}
- Education Level: {seeker_education_level}
- Education Focus: {seeker_education_focus}
- Pay Range: {seeker_pay_range} {seeker_pay_unit}
- Resume/Experience: {seeker_resume}

**Job Posting:**
- Job Title: {job_title}
- Required Skills: {job_skills}
- Required Education: {job_education_level} in {job_education_focus}
- Pay Range: {job_pay_range} {job_pay_unit}
- Job Description: {job_description}

Provide a detailed match analysis with scores for each factor.""")
        ])

    async def calculate_match_score(
        self,
        seeker_data: dict[str, Any],
        job_data: dict[str, Any]
    ) -> MatchScoreBreakdown:
        """
        Calculate match score between a seeker and a job.

        Args:
            seeker_data: Dictionary containing seeker information:
                - key_skills: list[str]
                - education_level: str
                - edu_focus: str
                - pay_range: list[int]
                - pay_unit: str
                - resume: str | None
            job_data: Dictionary containing job information:
                - job_title: str
                - key_skills: list[str]
                - education_level: str
                - edu_focus: str
                - pay_range: list[int]
                - pay_unit: str
                - job_description: str

        Returns:
            MatchScoreBreakdown with detailed scores and reasoning

        Raises:
            ValueError: If required data is missing
            Exception: If LLM call fails
        """
        try:
            # Validate required fields
            required_seeker_fields = ["key_skills", "education_level", "edu_focus", "pay_range", "pay_unit"]
            required_job_fields = ["job_title", "key_skills", "education_level", "edu_focus", "pay_range", "pay_unit", "job_description"]

            for field in required_seeker_fields:
                if field not in seeker_data:
                    raise ValueError(f"Missing required seeker field: {field}")

            for field in required_job_fields:
                if field not in job_data:
                    raise ValueError(f"Missing required job field: {field}")

            # Format data for prompt
            seeker_skills = ", ".join(seeker_data.get("key_skills", []))
            job_skills = ", ".join(job_data.get("key_skills", []))
            seeker_pay_range = f"${seeker_data['pay_range'][0]:,} - ${seeker_data['pay_range'][1]:,}"
            job_pay_range = f"${job_data['pay_range'][0]:,} - ${job_data['pay_range'][1]:,}"
            seeker_resume = seeker_data.get("resume", "No resume provided")

            # Format prompt with format instructions
            format_instructions = self.parser.get_format_instructions()

            # Create chain
            chain = self.prompt | self.llm | self.parser

            # Invoke chain
            result = await chain.ainvoke({
                "seeker_skills": seeker_skills,
                "seeker_education_level": seeker_data["education_level"],
                "seeker_education_focus": seeker_data["edu_focus"],
                "seeker_pay_range": seeker_pay_range,
                "seeker_pay_unit": seeker_data["pay_unit"],
                "seeker_resume": seeker_resume,
                "job_title": job_data["job_title"],
                "job_skills": job_skills,
                "job_education_level": job_data["education_level"],
                "job_education_focus": job_data["edu_focus"],
                "job_pay_range": job_pay_range,
                "job_pay_unit": job_data["pay_unit"],
                "job_description": job_data["job_description"],
                "format_instructions": format_instructions
            })

            logger.debug(f"Match score calculated: {result.overall_score}%")
            return result

        except Exception as e:
            logger.error(f"Error calculating match score: {e}")
            raise

    def calculate_match_score_sync(
        self,
        seeker_data: dict[str, Any],
        job_data: dict[str, Any]
    ) -> MatchScoreBreakdown:
        """
        Synchronous version of calculate_match_score.

        Args:
            seeker_data: Dictionary containing seeker information
            job_data: Dictionary containing job information

        Returns:
            MatchScoreBreakdown with detailed scores and reasoning
        """
        import asyncio

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(
            self.calculate_match_score(seeker_data, job_data)
        )


# Global scoring chain instance
_scoring_chain: ScoringChain | None = None


def get_scoring_chain() -> ScoringChain:
    """Get or create the global scoring chain instance."""
    global _scoring_chain  # noqa: PLW0603

    if _scoring_chain is None:
        _scoring_chain = ScoringChain()

    return _scoring_chain

