"""
Token Counter Callback Handler for LangChain

This module provides a callback handler that tracks token usage and costs
for OpenAI API calls made through LangChain. It logs token counts and costs
to the Debug_log.log file using the existing loguru logging infrastructure.
"""

from typing import Any

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from loguru import logger


class TokenCounterCallback(BaseCallbackHandler):
    """
    Callback handler that tracks token usage and costs for OpenAI API calls.
    
    Logs token counts and costs to Debug_log.log using loguru.
    """
    
    # Pricing for gpt-4o-mini (as of 2024)
    # Input: $0.15 per 1M tokens
    # Output: $0.60 per 1M tokens
    INPUT_COST_PER_MILLION = 0.15
    OUTPUT_COST_PER_MILLION = 0.60
    
    def __init__(self):
        """Initialize the token counter callback handler."""
        super().__init__()
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        self.call_count = 0
    
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """
        Called when an LLM call ends. Extracts token usage from the response.
        
        Args:
            response: LLMResult containing the response and metadata
            **kwargs: Additional keyword arguments
        """
        try:
            # Extract token usage from response metadata
            # LangChain stores token usage in response.llm_output["token_usage"]
            token_usage = None
            
            if response.llm_output and isinstance(response.llm_output, dict):
                token_usage = response.llm_output.get("token_usage")
            
            # Handle different token usage formats
            if token_usage:
                if isinstance(token_usage, dict):
                    input_tokens = token_usage.get("prompt_tokens", 0) or token_usage.get("input_tokens", 0)
                    output_tokens = token_usage.get("completion_tokens", 0) or token_usage.get("output_tokens", 0)
                    total_tokens = token_usage.get("total_tokens", 0)
                    
                    # If total_tokens is not provided, calculate it
                    if total_tokens == 0 and (input_tokens > 0 or output_tokens > 0):
                        total_tokens = input_tokens + output_tokens
                    
                    # Only process if we have valid token counts
                    if input_tokens > 0 or output_tokens > 0:
                        # Calculate cost
                        input_cost = (input_tokens / 1_000_000) * self.INPUT_COST_PER_MILLION
                        output_cost = (output_tokens / 1_000_000) * self.OUTPUT_COST_PER_MILLION
                        call_cost = input_cost + output_cost
                        
                        # Update totals
                        self.total_input_tokens += input_tokens
                        self.total_output_tokens += output_tokens
                        self.total_cost += call_cost
                        self.call_count += 1
                        
                        # Log individual call details
                        logger.debug(
                            f"[TOKEN_COUNTER] LLM Call #{self.call_count} - "
                            f"Input: {input_tokens:,} tokens (${input_cost:.6f}), "
                            f"Output: {output_tokens:,} tokens (${output_cost:.6f}), "
                            f"Total: {total_tokens:,} tokens (${call_cost:.6f})"
                        )
                        
                        # Log cumulative totals
                        logger.debug(
                            f"[TOKEN_COUNTER] Cumulative Totals - "
                            f"Input: {self.total_input_tokens:,} tokens, "
                            f"Output: {self.total_output_tokens:,} tokens, "
                            f"Total Cost: ${self.total_cost:.6f} "
                            f"({self.call_count} calls)"
                        )
                    else:
                        logger.debug(
                            "[TOKEN_COUNTER] Token usage data present but contains zero tokens"
                        )
                else:
                    logger.warning(
                        f"[TOKEN_COUNTER] Token usage data not in expected format: {type(token_usage)}"
                    )
            else:
                logger.debug(
                    "[TOKEN_COUNTER] No token usage data available in response. "
                    "This may be normal for some LLM providers or response types."
                )
        except Exception as e:
            logger.error(f"[TOKEN_COUNTER] Error processing token usage: {e}", exc_info=True)
    
    def get_summary(self) -> dict[str, Any]:
        """
        Get a summary of token usage and costs.
        
        Returns:
            Dictionary containing token usage summary
        """
        return {
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost": self.total_cost,
            "call_count": self.call_count,
            "avg_cost_per_call": self.total_cost / self.call_count if self.call_count > 0 else 0.0
        }
    
    def reset(self) -> None:
        """Reset the token counter statistics."""
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        self.call_count = 0
        logger.debug("[TOKEN_COUNTER] Token counter reset")


# Global token counter instance
_token_counter: TokenCounterCallback | None = None


def get_token_counter() -> TokenCounterCallback:
    """
    Get or create the global token counter callback instance.
    
    Returns:
        TokenCounterCallback instance
    """
    global _token_counter  # noqa: PLW0603
    
    if _token_counter is None:
        _token_counter = TokenCounterCallback()
        logger.debug("[TOKEN_COUNTER] Token counter callback initialized")
    
    return _token_counter

