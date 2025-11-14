"""
AI Chains Module

This module contains LangChain chains and matching services for:
- Scoring job-seeker matches
- Matching seekers to jobs
- Matching jobs to candidates
"""

from backend.ai.chains.candidate_matching_service import (
    CandidateMatchingService,
    get_candidate_matching_service,
)
from backend.ai.chains.matching_service import MatchingService, get_matching_service
from backend.ai.chains.scoring_chain import (
    MatchScoreBreakdown,
    ScoringChain,
    get_scoring_chain,
)

__all__ = [
    "ScoringChain",
    "MatchScoreBreakdown",
    "get_scoring_chain",
    "MatchingService",
    "get_matching_service",
    "CandidateMatchingService",
    "get_candidate_matching_service",
]

