"""
Custom Exceptions for Pattern Extraction Pipeline

Provides specific exception types for better error handling and recovery.
All exceptions inherit from IntegrationError for easy catching of integration-related failures.
"""


class IntegrationError(Exception):
    """Base exception for all integration errors"""
    pass


class RuleExtractionError(IntegrationError):
    """
    Rule extraction failed.
    
    Raised when IDE rule extraction encounters an error that prevents
    successful extraction and storage of rules.
    """
    pass


class DatabaseWriteError(IntegrationError):
    """
    Neo4j write operation failed.
    
    Raised when writing to Neo4j fails after retries, indicating a persistent
    database issue that requires attention.
    """
    pass


class RateLimitError(IntegrationError):
    """
    API rate limit exceeded.
    
    Raised when an API (Gemini, GitHub) rate limit is hit and cannot be
    automatically recovered via backoff/retry.
    """
    pass


class ConfigValidationError(IntegrationError):
    """
    Configuration validation failed.
    
    Raised when the pipeline configuration is invalid or missing required fields.
    """
    pass


class PatternExtractionError(IntegrationError):
    """
    Pattern extraction from repository failed.
    
    Raised when LLM-based pattern extraction encounters an error.
    """
    pass


class GitHubAPIError(IntegrationError):
    """
    GitHub API request failed.
    
    Raised when GitHub API requests fail after retries.
    """
    pass
