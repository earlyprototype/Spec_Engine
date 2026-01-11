#!/usr/bin/env python3
"""
Pydantic V2 Validator Tests

Tests that the migrated @field_validator decorators work correctly.
Validates error handling and constraint enforcement.
"""

import pytest
from pydantic import ValidationError
from pattern_extraction_pipeline.config_validator import (
    RuleExtractionConfig,
    GeminiConfig,
    Neo4jConfig,
    GitHubConfig,
    PipelineConfig
)


def test_rule_extraction_file_patterns_empty():
    """Test that empty file_patterns raises error"""
    with pytest.raises(ValidationError, match="file_patterns cannot be empty"):
        RuleExtractionConfig(
            enabled=True,
            max_file_size=100000,
            file_patterns=[]
        )


def test_rule_extraction_max_file_size_negative():
    """Test that negative max_file_size raises error"""
    with pytest.raises(ValidationError, match="greater than 0"):
        RuleExtractionConfig(
            enabled=True,
            max_file_size=-1000,
            file_patterns=['.cursorrules']
        )


def test_rule_extraction_max_file_size_too_large():
    """Test that max_file_size > 10MB raises error"""
    with pytest.raises(ValidationError, match="less than or equal to 10000000"):
        RuleExtractionConfig(
            enabled=True,
            max_file_size=20_000_000,  # 20MB
            file_patterns=['.cursorrules']
        )


def test_gemini_max_retries_too_low():
    """Test that max_retries < 1 raises error"""
    with pytest.raises(ValidationError, match="greater than or equal to 1"):
        GeminiConfig(
            api_key_env='TEST_KEY',
            model_name='test-model',
            max_retries=0
        )


def test_gemini_max_retries_too_high():
    """Test that max_retries > 10 raises error"""
    with pytest.raises(ValidationError, match="less than or equal to 10"):
        GeminiConfig(
            api_key_env='TEST_KEY',
            model_name='test-model',
            max_retries=20
        )


def test_neo4j_invalid_uri_scheme():
    """Test that invalid URI scheme raises error"""
    with pytest.raises(ValidationError, match="Invalid Neo4j URI scheme"):
        Neo4jConfig(
            uri="http://localhost:7687",  # Wrong scheme
            user='neo4j',
            password_env='NEO4J_PASSWORD'
        )


def test_neo4j_valid_uri_schemes():
    """Test that all valid Neo4j URI schemes are accepted"""
    valid_schemes = [
        "bolt://localhost:7687",
        "neo4j://localhost:7687",
        "neo4j+s://localhost:7687",
        "neo4j+ssc://localhost:7687"
    ]
    
    for uri in valid_schemes:
        config = Neo4jConfig(
            uri=uri,
            user='neo4j',
            password_env='NEO4J_PASSWORD'
        )
        assert config.uri == uri


def test_github_rate_limit_pause_within_range():
    """Test that rate_limit_pause must be within valid range"""
    # Valid: 0-3600 seconds
    config = GitHubConfig(
        token_env='TEST_TOKEN',
        max_repos_per_query=100,
        rate_limit_pause=60
    )
    assert config.rate_limit_pause == 60


def test_valid_rule_extraction_config():
    """Test that valid configuration passes"""
    config = RuleExtractionConfig(
        enabled=True,
        max_file_size=100000,
        file_patterns=['.cursorrules', 'CLAUDE.md']
    )
    assert config.enabled == True
    assert config.max_file_size == 100000
    assert len(config.file_patterns) == 2


def test_valid_pipeline_config():
    """Test that valid pipeline config passes all validation"""
    config = PipelineConfig(
        rule_extraction={
            'enabled': True,
            'max_file_size': 100000,
            'file_patterns': ['.cursorrules']
        },
        gemini={
            'api_key_env': 'TEST_KEY',
            'model_name': 'test-model',
            'max_retries': 3
        },
        neo4j={
            'uri': 'bolt://localhost:7687',
            'user': 'neo4j',
            'password_env': 'NEO4J_PASSWORD'
        },
        github={
            'token_env': 'GITHUB_TOKEN',
            'max_repos_per_query': 100,
            'rate_limit_pause': 60
        }
    )
    
    assert config.gemini.max_retries == 3
    assert config.rule_extraction.enabled == True
    assert config.neo4j.uri == 'bolt://localhost:7687'
    assert config.github.max_repos_per_query == 100


def test_pipeline_config_with_defaults():
    """Test that pipeline config works with minimal input"""
    config = PipelineConfig(
        rule_extraction={},
        gemini={},
        neo4j={},
        github={}
    )
    
    # Check defaults are applied
    assert config.gemini.model_name == 'gemini-2.5-flash'
    assert config.gemini.max_retries == 3
    assert config.neo4j.uri == 'bolt://localhost:7687'
    assert config.github.max_repos_per_query == 100


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
