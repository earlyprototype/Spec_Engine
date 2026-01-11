#!/usr/bin/env python3
"""
Retry handler with exponential backoff for Gemini API calls.

Handles transient failures, rate limits, and network issues.
"""

import time
import logging
from typing import Callable, TypeVar, Any, Optional
from functools import wraps

# Import exceptions from central module
from ide_rule_library.exceptions import GeminiQuotaExceededError, GeminiTimeoutError

# Type variable for generic return type
T = TypeVar('T')


class RetryError(Exception):
    """Raised when all retry attempts are exhausted"""
    pass


def retry_with_backoff(
    max_attempts: int = 3,
    initial_delay: float = 2.0,
    max_delay: float = 10.0,
    exponential_base: float = 2.0,
    exceptions: tuple = (Exception,),
    logger: Optional[logging.Logger] = None
) -> Callable:
    """
    Decorator for retrying functions with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential backoff calculation
        exceptions: Tuple of exception types to retry on
        logger: Logger instance for logging retry attempts
        
    Returns:
        Decorated function with retry logic
        
    Example:
        @retry_with_backoff(max_attempts=3, exceptions=(GeminiTimeout, GeminiQuotaExceeded))
        def call_gemini_api():
            return model.generate_content(prompt)
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            attempt = 0
            delay = initial_delay
            
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                    
                except exceptions as e:
                    attempt += 1
                    
                    if attempt >= max_attempts:
                        error_msg = f"Failed after {max_attempts} attempts: {e}"
                        if logger:
                            logger.error(error_msg, exc_info=True)
                        raise RetryError(error_msg) from e
                    
                    # Calculate backoff delay
                    backoff_delay = min(delay * (exponential_base ** (attempt - 1)), max_delay)
                    
                    if logger:
                        logger.warning(
                            f"Attempt {attempt}/{max_attempts} failed: {e}. "
                            f"Retrying in {backoff_delay:.1f}s..."
                        )
                    
                    time.sleep(backoff_delay)
                    
        return wrapper
    return decorator


def call_gemini_with_retry(
    model: Any,
    prompt: str,
    max_attempts: int = 3,
    logger: Optional[logging.Logger] = None
) -> Any:
    """
    Call Gemini API with automatic retry logic.
    
    Args:
        model: Gemini model instance
        prompt: Prompt to send to the model
        max_attempts: Maximum number of retry attempts
        logger: Logger instance
        
    Returns:
        Gemini response object
        
    Raises:
        RetryError: If all retry attempts fail
        GeminiQuotaExceeded: If quota is exceeded
        GeminiTimeout: If request times out
    """
    @retry_with_backoff(
        max_attempts=max_attempts,
        initial_delay=2.0,
        max_delay=10.0,
        exceptions=(GeminiTimeoutError, ConnectionError, TimeoutError),
        logger=logger
    )
    def _call():
        try:
            response = model.generate_content(prompt)
            
            # Check for quota exceeded in response
            if hasattr(response, 'prompt_feedback'):
                feedback = response.prompt_feedback
                if hasattr(feedback, 'block_reason'):
                    if 'QUOTA' in str(feedback.block_reason).upper():
                        raise GeminiQuotaExceededError(f"Gemini API quota exceeded: {feedback.block_reason}")
            
            return response
            
        except Exception as e:
            error_str = str(e).lower()
            
            # Classify errors
            if 'quota' in error_str or 'rate limit' in error_str:
                raise GeminiQuotaExceededError(f"Gemini API quota/rate limit exceeded: {e}")
            elif 'timeout' in error_str or 'timed out' in error_str:
                raise GeminiTimeoutError(f"Gemini API timeout: {e}")
            elif 'connection' in error_str:
                raise ConnectionError(f"Connection error: {e}")
            else:
                # Re-raise unknown errors
                raise
    
    return _call()


def call_gemini_embedding_with_retry(
    content: str,
    embedding_model: str,
    task_type: str = "semantic_similarity",
    max_attempts: int = 3,
    logger: Optional[logging.Logger] = None
) -> list:
    """
    Call Gemini embedding API with automatic retry logic.
    
    Args:
        content: Content to embed
        embedding_model: Model name for embeddings
        task_type: Task type for embedding
        max_attempts: Maximum number of retry attempts
        logger: Logger instance
        
    Returns:
        Embedding vector as list of floats
        
    Raises:
        RetryError: If all retry attempts fail
    """
    import google.generativeai as genai
    
    @retry_with_backoff(
        max_attempts=max_attempts,
        initial_delay=2.0,
        max_delay=10.0,
        exceptions=(GeminiTimeoutError, ConnectionError, TimeoutError),
        logger=logger
    )
    def _call():
        try:
            result = genai.embed_content(
                model=embedding_model,
                content=content,
                task_type=task_type
            )
            return result['embedding']
            
        except Exception as e:
            error_str = str(e).lower()
            
            if 'quota' in error_str or 'rate limit' in error_str:
                raise GeminiQuotaExceededError(f"Gemini embedding API quota exceeded: {e}")
            elif 'timeout' in error_str:
                raise GeminiTimeoutError(f"Gemini embedding API timeout: {e}")
            elif 'connection' in error_str:
                raise ConnectionError(f"Connection error: {e}")
            else:
                raise
    
    return _call()


if __name__ == '__main__':
    # Test retry logic
    import logging
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Simulate flaky function
    call_count = 0
    
    @retry_with_backoff(max_attempts=3, exceptions=(ValueError,), logger=logger)
    def flaky_function():
        global call_count
        call_count += 1
        
        if call_count < 2:
            logger.info(f"Call {call_count}: Simulating failure")
            raise ValueError("Simulated failure")
        
        logger.info(f"Call {call_count}: Success")
        return "Success!"
    
    try:
        result = flaky_function()
        print(f"\nResult: {result}")
        print(f"Total calls: {call_count}")
    except RetryError as e:
        print(f"\nFailed: {e}")
