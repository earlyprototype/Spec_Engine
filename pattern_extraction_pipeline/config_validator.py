"""
Configuration Validation

Pydantic models for validating pipeline configuration.
Fails fast on invalid config, provides type safety and clear error messages.
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Dict, Optional


class RuleExtractionConfig(BaseModel):
    """Configuration for IDE rule extraction"""
    
    enabled: bool = True
    max_file_size: int = Field(default=100000, gt=0, le=10000000, description="Maximum rule file size in bytes")
    file_patterns: List[str] = Field(default_factory=lambda: [
        ".cursorrules",
        ".aiderules",
        ".windsurfrules",
        "CLAUDE.md",
        "AI_INSTRUCTIONS.md",
        "AI_GUIDELINES.md",
        ".github/copilot-instructions.md"
    ])
    
    @field_validator('file_patterns')
    @classmethod
    def validate_patterns(cls, v):
        if not v:
            raise ValueError("file_patterns cannot be empty")
        return v


class GeminiConfig(BaseModel):
    """Configuration for Gemini API"""
    
    api_key_env: str = "GEMINI_API_KEY"
    model_name: str = "gemini-2.5-flash"
    max_retries: int = Field(default=3, ge=1, le=10)
    


class Neo4jConfig(BaseModel):
    """Configuration for Neo4j database"""
    
    uri: str = "bolt://localhost:7687"
    user: str = "neo4j"
    password_env: str = "NEO4J_PASSWORD"
    
    @field_validator('uri')
    @classmethod
    def validate_uri(cls, v):
        if not v.startswith(('bolt://', 'neo4j://', 'neo4j+s://', 'neo4j+ssc://')):
            raise ValueError("Invalid Neo4j URI scheme")
        return v


class GitHubConfig(BaseModel):
    """Configuration for GitHub API"""
    
    token_env: str = "GITHUB_TOKEN"
    max_repos_per_query: int = Field(default=100, ge=1, le=1000)
    rate_limit_pause: int = Field(default=60, ge=0, le=3600, description="Seconds to wait on rate limit")


class PatternExtractionConfig(BaseModel):
    """Configuration for pattern extraction features"""
    
    quality_metrics_enabled: bool = True
    pattern_critic_enabled: bool = True
    quality_judge_enabled: bool = True
    trajectory_logging_enabled: bool = True


class PipelineConfig(BaseModel):
    """
    Complete pipeline configuration
    
    Validates all configuration sections and provides type-safe access.
    Fails fast with clear error messages on invalid configuration.
    """
    
    model_config = ConfigDict(
        validate_assignment=True,
        extra='allow'  # Allow extra fields for backwards compatibility
    )
    
    rule_extraction: RuleExtractionConfig
    gemini: GeminiConfig
    neo4j: Neo4jConfig
    github: GitHubConfig
    pattern_extraction: Optional[PatternExtractionConfig] = PatternExtractionConfig()


def load_and_validate_config(config_dict: Dict) -> PipelineConfig:
    """
    Load and validate configuration from dictionary.
    
    Args:
        config_dict: Raw configuration dictionary (from YAML)
    
    Returns:
        Validated PipelineConfig object
    
    Raises:
        ValidationError: If configuration is invalid
    
    Example:
        >>> import yaml
        >>> with open('config.yaml') as f:
        >>>     raw_config = yaml.safe_load(f)
        >>> config = load_and_validate_config(raw_config)
    """
    return PipelineConfig(**config_dict)


def validate_config_file(config_path: str) -> PipelineConfig:
    """
    Load and validate configuration from YAML file.
    
    Args:
        config_path: Path to config.yaml file
    
    Returns:
        Validated PipelineConfig object
    
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If YAML is malformed
        ValidationError: If configuration is invalid
    """
    import yaml
    from pathlib import Path
    
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_file, 'r') as f:
        raw_config = yaml.safe_load(f)
    
    if not raw_config:
        raise ValueError(f"Empty or invalid YAML file: {config_path}")
    
    return load_and_validate_config(raw_config)
