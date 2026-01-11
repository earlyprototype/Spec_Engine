"""
Feature Flags

Centralized feature flag management for gradual rollout and backwards compatibility.
Allows enabling/disabling features at runtime via configuration.
"""

from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


def feature_enabled(config: Any, feature_name: str, default: bool = False) -> bool:
    """
    Check if a feature is enabled in the configuration.
    
    Supports both dict-based and Pydantic-based configs with dot-notation paths.
    
    Args:
        config: Configuration object (dict or Pydantic model)
        feature_name: Name of the feature (e.g., 'rule_extraction.enabled')
        default: Default value if feature not found
    
    Returns:
        bool: True if feature is enabled
    
    Examples:
        >>> feature_enabled(config, 'rule_extraction.enabled', default=True)
        >>> feature_enabled(config, 'pattern_extraction.quality_metrics_enabled')
    """
    try:
        # Handle dot notation (e.g., 'rule_extraction.enabled')
        parts = feature_name.split('.')
        
        # Navigate through nested structure
        current = config
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                # Pydantic model or object with attributes
                current = getattr(current, part, None)
            
            if current is None:
                logger.debug(f"Feature '{feature_name}' not found in config, using default: {default}")
                return default
        
        # Cast to bool
        return bool(current)
    
    except (AttributeError, KeyError, TypeError) as e:
        logger.warning(f"Error checking feature '{feature_name}': {e}, using default: {default}")
        return default


def get_feature_value(config: Any, feature_name: str, default: Any = None) -> Any:
    """
    Get a feature value from configuration (not just boolean).
    
    Args:
        config: Configuration object
        feature_name: Name of the feature with dot notation
        default: Default value if not found
    
    Returns:
        Feature value or default
    
    Examples:
        >>> max_size = get_feature_value(config, 'rule_extraction.max_file_size', 100000)
        >>> model = get_feature_value(config, 'gemini.model_name', 'gemini-2.5-flash')
    """
    try:
        parts = feature_name.split('.')
        current = config
        
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                current = getattr(current, part, None)
            
            if current is None:
                logger.debug(f"Feature value '{feature_name}' not found, using default: {default}")
                return default
        
        return current
    
    except (AttributeError, KeyError, TypeError) as e:
        logger.warning(f"Error getting feature value '{feature_name}': {e}, using default: {default}")
        return default


class FeatureFlags:
    """
    Feature flags manager with caching and logging.
    
    Example:
        >>> flags = FeatureFlags(config)
        >>> if flags.is_enabled('rule_extraction.enabled'):
        >>>     # Extract rules
    """
    
    def __init__(self, config: Any):
        """
        Initialize feature flags manager.
        
        Args:
            config: Configuration object (dict or Pydantic model)
        """
        self.config = config
        self._cache = {}
    
    def is_enabled(self, feature_name: str, default: bool = False) -> bool:
        """
        Check if a feature is enabled.
        
        Results are cached for performance.
        
        Args:
            feature_name: Feature name with dot notation
            default: Default value if not found
        
        Returns:
            bool: True if enabled
        """
        cache_key = f"{feature_name}:{default}"
        
        if cache_key not in self._cache:
            self._cache[cache_key] = feature_enabled(self.config, feature_name, default)
        
        return self._cache[cache_key]
    
    def get_value(self, feature_name: str, default: Any = None) -> Any:
        """Get a feature value (cached)."""
        cache_key = f"value:{feature_name}:{default}"
        
        if cache_key not in self._cache:
            self._cache[cache_key] = get_feature_value(self.config, feature_name, default)
        
        return self._cache[cache_key]
    
    def clear_cache(self):
        """Clear the feature flag cache."""
        self._cache.clear()
        logger.debug("Feature flags cache cleared")
    
    def get_all_flags(self) -> Dict[str, bool]:
        """
        Get all boolean feature flags from config.
        
        Returns:
            dict: Map of feature names to their enabled state
        """
        flags = {}
        
        # Common feature paths
        feature_paths = [
            'rule_extraction.enabled',
            'pattern_extraction.quality_metrics_enabled',
            'pattern_extraction.pattern_critic_enabled',
            'pattern_extraction.quality_judge_enabled',
            'pattern_extraction.trajectory_logging_enabled'
        ]
        
        for path in feature_paths:
            flags[path] = self.is_enabled(path)
        
        return flags


# Convenience function for quick checks
def is_feature_enabled(config: Any, feature_name: str, default: bool = False) -> bool:
    """
    Quick feature flag check without creating a FeatureFlags instance.
    
    Args:
        config: Configuration object
        feature_name: Feature name with dot notation
        default: Default value if not found
    
    Returns:
        bool: True if enabled
    """
    return feature_enabled(config, feature_name, default)
