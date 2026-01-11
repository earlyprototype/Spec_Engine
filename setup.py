#!/usr/bin/env python3
"""
Setup configuration for AI Specs project.

Provides proper package management for pattern_extraction_pipeline and ide_rule_library.
"""

from setuptools import setup, find_packages

setup(
    name="ai-specs",
    version="1.0.0",
    description="AI-powered pattern extraction and IDE rule library with knowledge graph integration",
    author="AI Specs Team",
    python_requires=">=3.8",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=[
        "PyGithub>=2.1.1",
        "google-generativeai>=0.3.2",
        "neo4j>=5.16.0",
        "python-dotenv>=1.0.1",
        "tenacity>=8.2.3",
        "pyyaml>=6.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "extract-patterns=pattern_extraction_pipeline.pattern_extractor:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
