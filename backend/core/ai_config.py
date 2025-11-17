"""
AI Configuration Module

This module provides configuration for AI/LLM services including OpenAI and LangSmith tracing.
"""

import os

from langchain_openai import ChatOpenAI
from loguru import logger

from backend.core.token_counter import get_token_counter


class AIConfig:
    """
    Configuration class for AI services.
    
    Manages environment variables and settings for:
    - OpenAI API
    - LangSmith tracing
    - Model selection
    """
    
    def __init__(self):
        """Initialize AI configuration from environment variables."""
        # OpenAI Configuration
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        # LangSmith Configuration
        self.langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
        self.langsmith_tracing = os.getenv("LANGSMITH_TRACING", "true").lower() == "true"
        self.langsmith_endpoint = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
        self.langsmith_project = os.getenv("LANGSMITH_PROJECT", "job_portal")
        
        # Model temperature
        self.default_temperature = float(os.getenv("DEFAULT_TEMPERATURE", "0.75"))
        
        # Validate required configuration
        self._validate_config()
        
        # Configure LangSmith if enabled
        self._configure_langsmith()
    
    def _validate_config(self) -> None:
        """Validate that required configuration is present."""
        if not self.openai_api_key:
            logger.warning("OPENAI_API_KEY not set. AI features may not work.")
        
        if self.langsmith_tracing and not self.langsmith_api_key:
            logger.warning("LANGSMITH_TRACING enabled but LANGSMITH_API_KEY not set. Disabling tracing.")
            self.langsmith_tracing = False
    
    def _configure_langsmith(self) -> None:
        """Configure LangSmith tracing if enabled."""
        if self.langsmith_tracing and self.langsmith_api_key:
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_API_KEY"] = self.langsmith_api_key
            os.environ["LANGCHAIN_ENDPOINT"] = self.langsmith_endpoint
            os.environ["LANGCHAIN_PROJECT"] = self.langsmith_project
            logger.info(f"LangSmith tracing enabled for project: {self.langsmith_project}")
        else:
            os.environ["LANGCHAIN_TRACING_V2"] = "false"
            logger.info("LangSmith tracing disabled")
    
    def get_llm_client(self, temperature: float | None = None) -> ChatOpenAI:
        """
        Get a configured LLM client with token counting enabled.
        
        Args:
            temperature: Optional temperature override (0-1)
        
        Returns:
            Configured ChatOpenAI client with token counter callback
        """
        temp = temperature if temperature is not None else self.default_temperature
        
        # Get token counter callback handler
        token_counter = get_token_counter()
        
        return ChatOpenAI(
            model=self.openai_model,
            temperature=temp,
            api_key=self.openai_api_key,
            callbacks=[token_counter]  # Add token counter callback
        )


# Global AI config instance
_ai_config: AIConfig | None = None


def get_ai_config() -> AIConfig:
    """Get or create the global AI config instance."""
    global _ai_config  # noqa: PLW0603
    
    if _ai_config is None:
        _ai_config = AIConfig()
    
    return _ai_config


def get_llm_client(temperature: float | None = None) -> ChatOpenAI:
    """
    Get a configured LLM client.
    
    Args:
        temperature: Optional temperature override (0-1)
    
    Returns:
        Configured ChatOpenAI client
    """
    config = get_ai_config()
    return config.get_llm_client(temperature)

