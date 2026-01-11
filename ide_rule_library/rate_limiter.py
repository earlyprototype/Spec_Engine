#!/usr/bin/env python3
"""GitHub API rate limit handler with exponential backoff"""

import time
from github import Github, RateLimitExceededException, UnknownObjectException, GithubException
from typing import Callable, Any
from datetime import datetime


class GitHubRateLimiter:
    """Automatic rate limit handling with exponential backoff and retries"""
    
    def __init__(self, gh: Github, config: dict, logger):
        self.gh = gh
        self.config = config
        self.logger = logger
        self.threshold = config.get('rate_limit_threshold', 100)
        self.max_retries = config.get('max_retries', 5)
        self.base_delay = config.get('retry_delay_base', 2)
    
    def call_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """Execute GitHub API call with automatic retry and rate limit handling"""
        
        for attempt in range(self.max_retries):
            # Check rate limit before call
            try:
                rate_limit = self.gh.get_rate_limit()
                # Handle both old and new PyGithub API
                if hasattr(rate_limit, 'core'):
                    remaining = rate_limit.core.remaining
                else:
                    remaining = rate_limit.resources['core'].remaining
                
                if remaining < self.threshold:
                    self._wait_for_rate_limit()
            except Exception as e:
                self.logger.debug(f"Could not check rate limit: {e}")
            
            try:
                return func(*args, **kwargs)
                
            except RateLimitExceededException as e:
                if attempt == self.max_retries - 1:
                    self.logger.error("Rate limit exceeded and max retries reached")
                    raise
                
                # Calculate exponential backoff
                delay = self.base_delay ** (attempt + 1)
                self.logger.warning(f"Rate limit hit, waiting {delay}s (attempt {attempt + 1}/{self.max_retries})")
                time.sleep(delay)
                
            except UnknownObjectException as e:
                # 404 - repo not found or private, don't retry
                self.logger.debug(f"Repository not found: {e}")
                raise
                
            except GithubException as e:
                if e.status == 403:
                    # Forbidden - might be rate limit or permissions
                    if 'rate limit' in str(e).lower():
                        if attempt == self.max_retries - 1:
                            raise
                        delay = self.base_delay ** (attempt + 1)
                        self.logger.warning(f"Rate limit (403), waiting {delay}s")
                        time.sleep(delay)
                    else:
                        # Permissions issue, don't retry
                        self.logger.debug(f"Access forbidden: {e}")
                        raise
                        
                elif e.status == 404:
                    # Not found, don't retry
                    self.logger.debug(f"Resource not found: {e}")
                    raise
                    
                elif e.status == 451:
                    # DMCA takedown, don't retry
                    self.logger.debug(f"Repository unavailable (DMCA): {e}")
                    raise
                    
                elif e.status >= 500:
                    # Server error, retry
                    if attempt == self.max_retries - 1:
                        raise
                    delay = self.base_delay ** (attempt + 1)
                    self.logger.warning(f"Server error {e.status}, retrying in {delay}s")
                    time.sleep(delay)
                else:
                    # Other error, don't retry
                    raise
        
        raise Exception(f"Max retries ({self.max_retries}) exceeded")
    
    def _wait_for_rate_limit(self):
        """Wait until rate limit resets"""
        try:
            rate_limit = self.gh.get_rate_limit()
            # Handle both old and new PyGithub API
            if hasattr(rate_limit, 'core'):
                reset_time = rate_limit.core.reset
            else:
                reset_time = rate_limit.resources['core'].reset
            
            wait_seconds = (reset_time - datetime.utcnow()).total_seconds() + 10  # Add 10s buffer
            
            if wait_seconds > 0:
                self.logger.warning(f"Rate limit threshold reached, waiting {wait_seconds:.0f}s until reset")
                time.sleep(wait_seconds)
            
        except Exception as e:
            self.logger.warning(f"Error checking rate limit reset time: {e}, waiting 60s")
            time.sleep(60)
    
    def get_remaining_calls(self) -> int:
        """Get remaining API calls"""
        try:
            rate_limit = self.gh.get_rate_limit()
            # Handle both old and new PyGithub API
            if hasattr(rate_limit, 'core'):
                return rate_limit.core.remaining
            else:
                return rate_limit.resources['core'].remaining
        except:
            return 0
