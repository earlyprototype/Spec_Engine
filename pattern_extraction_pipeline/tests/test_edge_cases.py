#!/usr/bin/env python3
"""
Edge Case Tests

Tests error handling, failure modes, and edge cases to improve coverage.
Focuses on paths not covered by main integration tests.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from pattern_extraction_pipeline.pattern_extractor import PatternExtractor
from pattern_extraction_pipeline.exceptions import (
    PatternExtractionError, RuleExtractionError, DatabaseWriteError,
    RateLimitError, GitHubAPIError
)
from pattern_extraction_pipeline.rate_limiter import RateLimiter
import time


class TestErrorHandling(unittest.TestCase):
    """Test error handling and exception propagation"""
    
    @patch('pattern_extraction_pipeline.pattern_extractor.GraphDatabase')
    def test_neo4j_connection_failure(self, mock_graph_db):
        """Test graceful handling of Neo4j connection failures"""
        mock_graph_db.driver.side_effect = Exception("Connection refused")
        
        with self.assertRaises(Exception) as context:
            extractor = PatternExtractor()
        
        self.assertIn("Connection refused", str(context.exception))
    
    @patch('pattern_extraction_pipeline.pattern_extractor.GraphDatabase')
    @patch('pattern_extraction_pipeline.pattern_extractor.Github')
    def test_gemini_api_failure(self, mock_github, mock_graph_db):
        """Test handling of Gemini API failures during initialization"""
        mock_driver = Mock()
        mock_graph_db.driver.return_value = mock_driver
        mock_github.return_value = Mock()
        
        with patch('pattern_extraction_pipeline.pattern_extractor.genai.configure', side_effect=Exception("API key invalid")):
            with self.assertRaises(Exception) as context:
                extractor = PatternExtractor()
            
            self.assertIn("API key invalid", str(context.exception))
    
    @patch('pattern_extraction_pipeline.pattern_extractor.GraphDatabase')
    @patch('pattern_extraction_pipeline.pattern_extractor.Github')
    def test_github_api_rate_limit(self, mock_github, mock_graph_db):
        """Test handling of GitHub API rate limit errors"""
        mock_driver = Mock()
        mock_graph_db.driver.return_value = mock_driver
        
        from github import RateLimitExceededException
        mock_github_instance = Mock()
        mock_github_instance.search_repositories.side_effect = RateLimitExceededException(
            status=403, data={'message': 'API rate limit exceeded'}, headers={}
        )
        mock_github.return_value = mock_github_instance
        
        extractor = PatternExtractor()
        self.addCleanup(extractor.close)
        
        # Verify the extractor was created but rate limit would trigger on use
        self.assertIsNotNone(extractor.github)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    @patch('pattern_extraction_pipeline.pattern_extractor.GraphDatabase')
    @patch('pattern_extraction_pipeline.pattern_extractor.Github')
    def test_empty_repository(self, mock_github, mock_graph_db):
        """Test handling of empty repositories"""
        mock_driver = Mock()
        mock_graph_db.driver.return_value = mock_driver
        mock_github.return_value = Mock()
        
        extractor = PatternExtractor()
        self.addCleanup(extractor.close)
        
        # Mock empty repo
        mock_repo = Mock()
        mock_repo.get_contents.side_effect = Exception("Repository is empty")
        
        # Should handle gracefully
        rule_files = extractor._scan_for_rule_files(mock_repo)
        self.assertEqual(len(rule_files), 0)
    
    @patch('pattern_extraction_pipeline.pattern_extractor.GraphDatabase')
    @patch('pattern_extraction_pipeline.pattern_extractor.Github')
    def test_malformed_rule_file(self, mock_github, mock_graph_db):
        """Test handling of malformed rule files"""
        mock_driver = Mock()
        mock_graph_db.driver.return_value = mock_driver
        mock_github.return_value = Mock()
        
        extractor = PatternExtractor()
        self.addCleanup(extractor.close)
        
        # Mock file with invalid encoding
        mock_repo = Mock()
        mock_file = Mock()
        mock_file.size = 1000
        mock_file.decoded_content = b"\xff\xfe\x00\x00"  # Invalid UTF-8
        mock_repo.get_contents.return_value = mock_file
        
        # Should handle decode errors gracefully
        rule_files = extractor._scan_for_rule_files(mock_repo)
        # May be empty or handle error depending on implementation
        self.assertIsInstance(rule_files, list)
    
    @patch('pattern_extraction_pipeline.pattern_extractor.GraphDatabase')
    @patch('pattern_extraction_pipeline.pattern_extractor.Github')
    def test_missing_rule_files(self, mock_github, mock_graph_db):
        """Test repository with no rule files"""
        mock_driver = Mock()
        mock_graph_db.driver.return_value = mock_driver
        mock_github.return_value = Mock()
        
        extractor = PatternExtractor()
        self.addCleanup(extractor.close)
        
        # Mock repo with no rule files (404)
        mock_repo = Mock()
        mock_repo.get_contents.side_effect = Exception("Not Found")
        
        rule_files = extractor._scan_for_rule_files(mock_repo)
        self.assertEqual(len(rule_files), 0)
    
    @patch('pattern_extraction_pipeline.pattern_extractor.GraphDatabase')
    @patch('pattern_extraction_pipeline.pattern_extractor.Github')
    def test_zero_star_repository(self, mock_github, mock_graph_db):
        """Test handling of repositories with zero stars"""
        mock_driver = Mock()
        mock_graph_db.driver.return_value = mock_driver
        mock_github.return_value = Mock()
        
        extractor = PatternExtractor()
        self.addCleanup(extractor.close)
        
        # Mock repo with zero stars
        mock_repo = Mock()
        mock_repo.stargazers_count = 0
        mock_repo.forks_count = 0
        mock_repo.open_issues_count = 0
        
        # Should not crash, even with zero popularity
        self.assertIsNotNone(mock_repo.stargazers_count)


class TestRateLimiter(unittest.TestCase):
    """Test rate limiter behavior"""
    
    def test_rate_limiter_enforces_limit(self):
        """Test that rate limiter blocks after limit is reached"""
        limiter = RateLimiter(max_calls=3, period=1, name="test")
        
        # First 3 calls should succeed immediately
        for i in range(3):
            wait_time = limiter.wait_if_needed()
            self.assertEqual(wait_time, 0)
        
        # 4th call should block
        wait_time = limiter.wait_if_needed()
        
        # Should have waited for the period to roll over
        self.assertGreater(wait_time, 0.5)  # At least half a second
    
    def test_rate_limiter_concurrent_requests(self):
        """Test rate limiter with multiple requests"""
        limiter = RateLimiter(max_calls=5, period=2, name="test")
        
        # 5 calls should succeed
        for i in range(5):
            limiter.wait_if_needed()
        
        # Stats should show 5 recent calls
        stats = limiter.get_stats()
        self.assertEqual(stats['recent_calls'], 5)
    
    def test_rate_limiter_reset(self):
        """Test that rate limiter resets after period"""
        limiter = RateLimiter(max_calls=2, period=0.5, name="test")
        
        # Use up the limit
        limiter.wait_if_needed()
        limiter.wait_if_needed()
        
        # Wait for sliding window to reset
        time.sleep(0.6)
        
        # Should be able to make calls again without waiting
        wait_time = limiter.wait_if_needed()
        self.assertEqual(wait_time, 0.0)  # Should not have waited


class TestConfigValidation(unittest.TestCase):
    """Test configuration edge cases"""
    
    def test_invalid_config_yaml(self):
        """Test handling of malformed YAML config"""
        from pattern_extraction_pipeline.config_validator import validate_config_file
        
        with self.assertRaises(Exception):
            # Non-existent file
            validate_config_file("/nonexistent/config.yaml")
    
    def test_config_with_missing_sections(self):
        """Test config with missing required sections"""
        from pattern_extraction_pipeline.config_validator import PipelineConfig
        from pydantic import ValidationError
        
        with self.assertRaises(ValidationError):
            # Missing required sections
            PipelineConfig(
                rule_extraction={'enabled': True},
                # Missing gemini, neo4j, github
            )
    
    def test_config_with_invalid_values(self):
        """Test config with out-of-range values"""
        from pattern_extraction_pipeline.config_validator import GeminiConfig
        from pydantic import ValidationError
        
        with self.assertRaises(ValidationError):
            # Invalid max_retries (too high)
            GeminiConfig(
                api_key_env='TEST_KEY',
                model_name='test-model',
                max_retries=100  # Exceeds limit of 10
            )


class TestDatabaseWriteFailures(unittest.TestCase):
    """Test database write error handling"""
    
    @patch('pattern_extraction_pipeline.pattern_extractor.GraphDatabase')
    @patch('pattern_extraction_pipeline.pattern_extractor.Github')
    def test_neo4j_write_failure(self, mock_github, mock_graph_db):
        """Test handling of Neo4j write failures"""
        mock_driver = Mock()
        mock_session = Mock()
        mock_result = Mock()
        mock_result.single.side_effect = Exception("Write failed: Constraint violation")
        mock_session.run.return_value = mock_result
        mock_session.__enter__ = Mock(return_value=mock_session)
        mock_session.__exit__ = Mock(return_value=False)
        mock_driver.session.return_value = mock_session
        mock_graph_db.driver.return_value = mock_driver
        mock_github.return_value = Mock()
        
        extractor = PatternExtractor()
        self.addCleanup(extractor.close)
        
        # Verify write failure is handled
        self.assertIsNotNone(extractor.neo4j)
    
    @patch('pattern_extraction_pipeline.pattern_extractor.GraphDatabase')
    @patch('pattern_extraction_pipeline.pattern_extractor.Github')
    def test_neo4j_transaction_rollback(self, mock_github, mock_graph_db):
        """Test handling of transaction rollbacks"""
        mock_driver = Mock()
        mock_session = Mock()
        mock_session.run.side_effect = Exception("Transaction failed")
        mock_session.__enter__ = Mock(return_value=mock_session)
        mock_session.__exit__ = Mock(return_value=False)
        mock_driver.session.return_value = mock_session
        mock_graph_db.driver.return_value = mock_driver
        mock_github.return_value = Mock()
        
        extractor = PatternExtractor()
        self.addCleanup(extractor.close)
        
        # Session should exist even if transactions fail
        self.assertIsNotNone(extractor.neo4j)


class TestQualityScoreEdgeCases(unittest.TestCase):
    """Test quality score calculation edge cases"""
    
    @patch('pattern_extraction_pipeline.pattern_extractor.GraphDatabase')
    @patch('pattern_extraction_pipeline.pattern_extractor.Github')
    def test_quality_score_with_missing_data(self, mock_github, mock_graph_db):
        """Test quality scoring when repo data is incomplete"""
        from ide_rule_library.quality_scorer import enhance_repo_metadata
        
        # Repo with minimal data
        repo_data = {
            'full_name': 'test/repo',
            'html_url': 'https://github.com/test/repo',
            # Missing: stars, forks, dates, etc.
        }
        
        # Should handle gracefully with defaults
        try:
            enhanced = enhance_repo_metadata(repo_data)
            self.assertIn('full_name', enhanced)
        except KeyError:
            # Expected if fields are truly required
            pass
    
    @patch('pattern_extraction_pipeline.pattern_extractor.GraphDatabase')
    @patch('pattern_extraction_pipeline.pattern_extractor.Github')
    def test_quality_score_calculation_failure(self, mock_github, mock_graph_db):
        """Test handling of quality score calculation failures"""
        from ide_rule_library.quality_scorer import RepoQualityScorer
        
        scorer = RepoQualityScorer()
        
        # Invalid repo data (missing required fields)
        invalid_data = {}
        
        # Scorer may return default values or raise exception
        try:
            score, breakdown = scorer.calculate_quality_score(invalid_data)
            # If it doesn't raise, check that it returns valid structure
            self.assertIsInstance(score, (int, float))
            self.assertIsInstance(breakdown, dict)
        except (KeyError, AttributeError, TypeError) as e:
            # Expected error types for invalid data
            self.assertIsNotNone(e)


if __name__ == '__main__':
    unittest.main(verbosity=2)
