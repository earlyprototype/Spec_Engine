"""
Pattern Extraction Pipeline

Automated pattern extraction from GitHub repositories using LLM analysis and Neo4j storage.
Includes integration with IDE Rule Library for comprehensive rule extraction.
"""

__version__ = "1.0.0"

from pattern_extraction_pipeline.pattern_extractor import PatternExtractor
from pattern_extraction_pipeline.pattern_query_interface import PatternQueryInterface

__all__ = ["PatternExtractor", "PatternQueryInterface"]
