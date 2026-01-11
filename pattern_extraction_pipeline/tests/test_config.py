"""
Test Configuration

Centralized configuration for integration and E2E tests.
Uses separate test Neo4j instance to avoid interfering with production data.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test Neo4j Configuration (separate from production)
TEST_NEO4J_URI = os.getenv("TEST_NEO4J_URI", "bolt://localhost:7688")
TEST_NEO4J_USER = os.getenv("TEST_NEO4J_USER", "neo4j")
TEST_NEO4J_PASSWORD = os.getenv("TEST_NEO4J_PASSWORD", os.getenv("NEO4J_PASSWORD", "test"))

# Test repositories with known characteristics
TEST_REPOS = {
    # Repository with IDE rules
    'with_rules': "anthropics/anthropic-sdk-python",
    
    # Repository without IDE rules (for negative testing)
    'without_rules': "torvalds/linux",
    
    # Small repository for quick tests
    'small': "bentoml/BentoML"
}

# API Keys (use same as production, but with rate limiting)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Test Timeouts
TEST_TIMEOUT_SHORT = 10  # seconds
TEST_TIMEOUT_MEDIUM = 30  # seconds
TEST_TIMEOUT_LONG = 60  # seconds

# Feature Flags for Tests
TEST_ENABLE_RULE_EXTRACTION = True
TEST_ENABLE_QUALITY_METRICS = True
