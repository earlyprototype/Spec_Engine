#!/usr/bin/env python3
"""
Custom exceptions for the IDE Rule Library system.

Provides explicit exception types for better error handling and debugging.
"""


class IDERuleLibraryError(Exception):
    """Base exception for all IDE Rule Library errors"""
    pass


# Extraction errors
class ExtractionError(IDERuleLibraryError):
    """Raised when rule extraction fails"""
    pass


class QualityScoreError(IDERuleLibraryError):
    """Raised when quality score calculation fails"""
    pass


class ValidationError(IDERuleLibraryError):
    """Raised when data validation fails"""
    pass


# Query errors
class QueryError(IDERuleLibraryError):
    """Raised when database query fails"""
    pass


class NoRulesFoundError(QueryError):
    """Raised when no rules match the query criteria"""
    pass


# Database errors
class DatabaseError(IDERuleLibraryError):
    """Raised when database operations fail"""
    pass


class ConnectionError(DatabaseError):
    """Raised when database connection fails"""
    pass


# API errors
class APIError(IDERuleLibraryError):
    """Raised when external API calls fail"""
    pass


class QuotaExceededError(APIError):
    """Raised when API quota is exceeded"""
    pass


class TimeoutError(APIError):
    """Raised when API call times out"""
    pass


class RateLimitError(APIError):
    """Raised when API rate limit is hit"""
    pass


# GitHub errors
class GitHubError(APIError):
    """Raised when GitHub API calls fail"""
    pass


class GitHubRateLimitError(GitHubError):
    """Raised when GitHub rate limit is exceeded"""
    pass


# Gemini errors
class GeminiError(APIError):
    """Raised when Gemini API calls fail"""
    pass


class GeminiQuotaExceededError(GeminiError):
    """Raised when Gemini quota is exceeded"""
    pass


class GeminiTimeoutError(GeminiError):
    """Raised when Gemini API times out"""
    pass


# Migration errors
class MigrationError(IDERuleLibraryError):
    """Raised when data migration fails"""
    pass


class CheckpointError(MigrationError):
    """Raised when checkpoint save/load fails"""
    pass


# Configuration errors
class ConfigurationError(IDERuleLibraryError):
    """Raised when configuration is invalid or missing"""
    pass


class MissingEnvironmentVariableError(ConfigurationError):
    """Raised when required environment variable is missing"""
    pass


# Data errors
class DataError(IDERuleLibraryError):
    """Raised when data is malformed or invalid"""
    pass


class MalformedDataError(DataError):
    """Raised when data structure is malformed"""
    pass


class MissingDataError(DataError):
    """Raised when required data is missing"""
    pass
