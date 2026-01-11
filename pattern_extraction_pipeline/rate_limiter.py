"""
Rate Limiter

Client-side rate limiting for API calls to prevent quota exhaustion.
Implements a sliding window algorithm with configurable limits.
"""

import time
from collections import deque
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Rate limiter using sliding window algorithm.
    
    Tracks API call timestamps and enforces rate limits by sleeping
    when necessary to stay within quota.
    
    Example:
        >>> limiter = RateLimiter(max_calls=60, period=60)  # 60 calls per minute
        >>> limiter.wait_if_needed()  # Blocks if limit reached
        >>> # Make API call
    """
    
    def __init__(self, max_calls: int, period: float, name: Optional[str] = None):
        """
        Initialize rate limiter.
        
        Args:
            max_calls: Maximum number of calls allowed in the period
            period: Time window in seconds
            name: Optional name for logging purposes
        """
        self.max_calls = max_calls
        self.period = period
        self.name = name or "rate_limiter"
        self.calls = deque()
        self._total_waits = 0
        self._total_wait_time = 0.0
        
        logger.info(f"Rate limiter '{self.name}' initialized: {max_calls} calls per {period}s")
    
    def wait_if_needed(self) -> float:
        """
        Wait if rate limit would be exceeded.
        
        Returns:
            float: Seconds waited (0 if no wait needed)
        """
        now = time.time()
        
        # Remove calls outside the sliding window
        while self.calls and self.calls[0] < now - self.period:
            self.calls.popleft()
        
        # Check if we need to wait
        if len(self.calls) >= self.max_calls:
            # Calculate wait time: time until oldest call exits the window
            wait_time = self.period - (now - self.calls[0])
            
            if wait_time > 0:
                self._total_waits += 1
                self._total_wait_time += wait_time
                
                logger.warning(
                    f"Rate limit reached for '{self.name}': "
                    f"{len(self.calls)}/{self.max_calls} calls in last {self.period}s. "
                    f"Sleeping {wait_time:.2f}s..."
                )
                
                time.sleep(wait_time)
                
                # Clean up old calls after sleeping
                now = time.time()
                while self.calls and self.calls[0] < now - self.period:
                    self.calls.popleft()
        
        # Record this call
        self.calls.append(time.time())
        
        return wait_time if 'wait_time' in locals() and wait_time > 0 else 0.0
    
    def get_stats(self) -> dict:
        """
        Get rate limiter statistics.
        
        Returns:
            dict: Statistics including total waits and wait time
        """
        now = time.time()
        
        # Count recent calls
        recent_calls = sum(1 for call_time in self.calls if call_time > now - self.period)
        
        return {
            'name': self.name,
            'max_calls': self.max_calls,
            'period': self.period,
            'recent_calls': recent_calls,
            'total_waits': self._total_waits,
            'total_wait_time_seconds': round(self._total_wait_time, 2),
            'average_wait_time_seconds': (
                round(self._total_wait_time / self._total_waits, 2)
                if self._total_waits > 0
                else 0.0
            )
        }
    
    def reset(self):
        """Reset rate limiter state."""
        self.calls.clear()
        self._total_waits = 0
        self._total_wait_time = 0.0
        logger.info(f"Rate limiter '{self.name}' reset")


class MultiAPIRateLimiter:
    """
    Manages multiple rate limiters for different APIs.
    
    Example:
        >>> limiters = MultiAPIRateLimiter()
        >>> limiters.add('gemini', max_calls=15, period=60)
        >>> limiters.add('github', max_calls=5000, period=3600)
        >>> limiters.wait('gemini')
    """
    
    def __init__(self):
        self._limiters = {}
    
    def add(self, name: str, max_calls: int, period: float) -> RateLimiter:
        """
        Add a rate limiter for an API.
        
        Args:
            name: API name (e.g., 'gemini', 'github')
            max_calls: Maximum calls per period
            period: Time window in seconds
        
        Returns:
            The created RateLimiter
        """
        limiter = RateLimiter(max_calls, period, name)
        self._limiters[name] = limiter
        return limiter
    
    def wait(self, name: str) -> float:
        """
        Wait if needed for the specified API.
        
        Args:
            name: API name
        
        Returns:
            float: Seconds waited
        
        Raises:
            KeyError: If API name not found
        """
        if name not in self._limiters:
            raise KeyError(f"Rate limiter '{name}' not found")
        
        return self._limiters[name].wait_if_needed()
    
    def get_limiter(self, name: str) -> RateLimiter:
        """Get a specific rate limiter."""
        return self._limiters.get(name)
    
    def get_all_stats(self) -> dict:
        """Get statistics for all rate limiters."""
        return {name: limiter.get_stats() for name, limiter in self._limiters.items()}
    
    def reset_all(self):
        """Reset all rate limiters."""
        for limiter in self._limiters.values():
            limiter.reset()
