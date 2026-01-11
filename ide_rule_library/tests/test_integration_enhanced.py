#!/usr/bin/env python3
"""
Integration tests for enhanced quality system.

Tests all critical paths with real components (no mocks).
"""

import os
import sys
import unittest
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import Mock, patch

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from quality_scorer import RepoQualityScorer, enhance_repo_metadata
from exceptions import (
    ExtractionError,
    ValidationError,
    QueryError,
    NoRulesFoundError,
    MissingEnvironmentVariableError
)


class TestQualityScorer(unittest.TestCase):
    """Test quality scoring with realistic data"""
    
    def setUp(self):
        self.scorer = RepoQualityScorer()
    
    def test_production_repo_scoring(self):
        """Test scoring a production-grade repository"""
        repo_data = {
            'stars': 10000,
            'forks': 1200,
            'created_at': datetime(2022, 1, 1, tzinfo=timezone.utc),
            'updated_at': datetime(2025, 12, 15, tzinfo=timezone.utc),
            'open_issues': 45,
            'closed_issues': 380,
            'contributors': ['user1', 'user2', 'user3', 'user4', 'user5'],
            'files': [
                'Dockerfile',
                '.github/workflows/ci.yml',
                'tests/test_main.py',
                'pytest.ini',
                'CHANGELOG.md',
                'README.md',
                'kubernetes/deployment.yaml',
                'prometheus.yml'
            ],
            'readme_length': 4500
        }
        
        score, breakdown = self.scorer.calculate_quality_score(repo_data)
        
        # Should score reasonably high
        self.assertGreater(score, 50, "Production repo should score > 50")
        self.assertLess(score, 100, "Score should be < 100")
        
        # Check all factors present
        expected_factors = [
            'star_velocity', 'freshness', 'issue_health',
            'diversity', 'production_ready', 'documentation', 'usage_signal'
        ]
        for factor in expected_factors:
            self.assertIn(factor, breakdown)
            self.assertGreaterEqual(breakdown[factor], 0)
    
    def test_tutorial_repo_scoring(self):
        """Test scoring a tutorial/example repository"""
        repo_data = {
            'stars': 500,
            'forks': 20,
            'created_at': datetime(2024, 6, 1, tzinfo=timezone.utc),
            'updated_at': datetime(2024, 7, 1, tzinfo=timezone.utc),  # Old
            'open_issues': 5,
            'closed_issues': 2,
            'contributors': ['author'],  # Single contributor
            'files': ['README.md', 'example.py'],  # Minimal files
            'readme_length': 500
        }
        
        score, breakdown = self.scorer.calculate_quality_score(repo_data)
        
        # Should score lower
        self.assertLess(score, 50, "Tutorial repo should score < 50")
        self.assertGreater(score, 0, "Score should be > 0")
    
    def test_production_signal_detection(self):
        """Test production signal detection accuracy"""
        files = [
            'Dockerfile',
            'docker-compose.yml',
            '.github/workflows/test.yml',
            'tests/test_main.py',
            'pytest.ini',
            '.coveragerc',
            'kubernetes/deployment.yaml',
            'helm/Chart.yaml',
            'prometheus.yml',
            'CHANGELOG.md',
            'CONTRIBUTING.md',
            'ruff.toml',
            '.pre-commit-config.yaml'
        ]
        
        score, signals = self.scorer.assess_production_maturity(files)
        
        # Should detect multiple categories
        self.assertGreater(len(signals), 4, "Should detect multiple signal categories")
        
        # Check specific categories
        self.assertIn('deployment', signals)
        self.assertIn('ci_cd', signals)
        self.assertIn('testing', signals)
        self.assertIn('documentation', signals)
        self.assertIn('quality_tools', signals)
    
    def test_case_insensitive_matching(self):
        """Test that pattern matching is case-insensitive"""
        files_lower = ['dockerfile', 'readme.md']
        files_upper = ['Dockerfile', 'README.md']
        files_mixed = ['DockerFile', 'ReadMe.md']
        
        score_lower, signals_lower = self.scorer.assess_production_maturity(files_lower)
        score_upper, signals_upper = self.scorer.assess_production_maturity(files_upper)
        score_mixed, signals_mixed = self.scorer.assess_production_maturity(files_mixed)
        
        # All should detect Dockerfile
        self.assertIn('deployment', signals_lower)
        self.assertIn('deployment', signals_upper)
        self.assertIn('deployment', signals_mixed)
    
    def test_directory_pattern_matching(self):
        """Test directory pattern matching (no false positives)"""
        files_with_tests = [
            'tests/test_main.py',
            'tests/test_utils.py',
            'src/main.py'
        ]
        
        files_with_best_practices = [
            'docs/best_practices.md',
            'src/main.py'
        ]
        
        _, signals_tests = self.scorer.assess_production_maturity(files_with_tests)
        _, signals_best = self.scorer.assess_production_maturity(files_with_best_practices)
        
        # Should detect tests/ directory
        self.assertIn('testing', signals_tests)
        
        # Should NOT detect tests/ in best_practices
        self.assertNotIn('testing', signals_best)
    
    def test_enhance_repo_metadata(self):
        """Test full metadata enhancement"""
        repo_data = {
            'stars': 5000,
            'forks': 600,
            'created_at': datetime(2023, 1, 1, tzinfo=timezone.utc),
            'updated_at': datetime(2025, 12, 1, tzinfo=timezone.utc),
            'open_issues': 20,
            'closed_issues': 150,
            'contributors': ['u1', 'u2', 'u3'],
            'files': ['Dockerfile', '.github/workflows/ci.yml', 'tests/'],
            'readme_length': 2000
        }
        
        enhanced = enhance_repo_metadata(repo_data)
        
        # Check all required fields added
        self.assertIn('quality_score', enhanced)
        self.assertIn('quality_breakdown', enhanced)
        self.assertIn('confidence_level', enhanced)
        self.assertIn('has_ci_cd', enhanced)
        self.assertIn('has_deployment', enhanced)
        self.assertIn('has_tests', enhanced)
        self.assertIn('repo_age_days', enhanced)
        self.assertIn('days_since_update', enhanced)
        
        # Confidence should be reasonable
        self.assertIn(enhanced['confidence_level'], [1, 2, 3, 4, 5])
    
    def test_defensive_checks_missing_data(self):
        """Test that scorer handles missing data gracefully"""
        # Minimal data
        repo_data = {
            'stars': 100,
            'forks': 10
        }
        
        # Should not crash
        score, breakdown = self.scorer.calculate_quality_score(repo_data)
        
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
    
    def test_defensive_checks_malformed_dates(self):
        """Test handling of malformed date data"""
        repo_data = {
            'stars': 1000,
            'forks': 100,
            'created_at': 'invalid_date',  # Malformed
            'updated_at': None,  # Missing
            'files': []
        }
        
        # Should not crash
        score, breakdown = self.scorer.calculate_quality_score(repo_data)
        
        # Freshness should be 0 (can't calculate)
        self.assertEqual(breakdown['freshness'], 0.0)


class TestExceptions(unittest.TestCase):
    """Test custom exception hierarchy"""
    
    def test_exception_hierarchy(self):
        """Test that custom exceptions inherit correctly"""
        from exceptions import IDERuleLibraryError
        
        # All custom exceptions should inherit from base
        self.assertTrue(issubclass(ExtractionError, IDERuleLibraryError))
        self.assertTrue(issubclass(ValidationError, IDERuleLibraryError))
        self.assertTrue(issubclass(QueryError, IDERuleLibraryError))
        self.assertTrue(issubclass(NoRulesFoundError, QueryError))
    
    def test_exception_messages(self):
        """Test that exceptions carry messages"""
        msg = "Test error message"
        
        exc = ExtractionError(msg)
        self.assertEqual(str(exc), msg)
        
        exc = ValidationError(msg)
        self.assertEqual(str(exc), msg)


class TestRetryHandler(unittest.TestCase):
    """Test retry logic"""
    
    def test_retry_decorator_success_first_try(self):
        """Test that successful calls don't retry"""
        from retry_handler import retry_with_backoff
        
        call_count = [0]
        
        @retry_with_backoff(max_attempts=3, exceptions=(ValueError,))
        def success_func():
            call_count[0] += 1
            return "success"
        
        result = success_func()
        
        self.assertEqual(result, "success")
        self.assertEqual(call_count[0], 1, "Should only call once")
    
    def test_retry_decorator_success_after_failures(self):
        """Test that function retries on failure"""
        from retry_handler import retry_with_backoff, RetryError
        
        call_count = [0]
        
        @retry_with_backoff(max_attempts=3, initial_delay=0.1, exceptions=(ValueError,))
        def flaky_func():
            call_count[0] += 1
            if call_count[0] < 2:
                raise ValueError("Simulated failure")
            return "success"
        
        result = flaky_func()
        
        self.assertEqual(result, "success")
        self.assertEqual(call_count[0], 2, "Should retry once")
    
    def test_retry_decorator_exhausts_attempts(self):
        """Test that retry gives up after max attempts"""
        from retry_handler import retry_with_backoff, RetryError
        
        call_count = [0]
        
        @retry_with_backoff(max_attempts=3, initial_delay=0.1, exceptions=(ValueError,))
        def always_fails():
            call_count[0] += 1
            raise ValueError("Always fails")
        
        with self.assertRaises(RetryError):
            always_fails()
        
        self.assertEqual(call_count[0], 3, "Should try 3 times")


class TestLogger(unittest.TestCase):
    """Test structured logging"""
    
    def test_logger_initialization(self):
        """Test that logger initializes correctly"""
        from logger import StructuredLogger
        
        config = {
            'level': 'INFO',
            'file': 'logs/test.log',
            'console_level': 'WARNING'
        }
        
        logger = StructuredLogger("test", config)
        
        self.assertIsNotNone(logger.logger)
        self.assertEqual(logger.logger.name, "test")
    
    def test_logger_methods(self):
        """Test that all logging methods work"""
        from logger import StructuredLogger
        
        config = {'level': 'DEBUG', 'file': 'logs/test.log'}
        logger = StructuredLogger("test", config)
        
        # Should not raise
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")


class TestConfigLoading(unittest.TestCase):
    """Test configuration loading"""
    
    def test_config_file_exists(self):
        """Test that config.yaml exists"""
        config_path = Path(__file__).parent.parent / 'config.yaml'
        self.assertTrue(config_path.exists(), "config.yaml should exist")
    
    def test_config_structure(self):
        """Test that config has required sections"""
        import yaml
        
        config_path = Path(__file__).parent.parent / 'config.yaml'
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        required_sections = ['gemini', 'neo4j', 'logging']
        for section in required_sections:
            self.assertIn(section, config, f"Config should have {section} section")


class TestEndToEndWorkflow(unittest.TestCase):
    """Test end-to-end workflows (requires environment setup)"""
    
    def setUp(self):
        """Check if environment is configured"""
        self.env_configured = all([
            os.getenv('NEO4J_URI'),
            os.getenv('NEO4J_USER'),
            os.getenv('NEO4J_PASSWORD'),
            os.getenv('GEMINI_API_KEY')
        ])
    
    @unittest.skipUnless(os.getenv('RUN_INTEGRATION_TESTS'), "Set RUN_INTEGRATION_TESTS=1 to run")
    def test_validate_system(self):
        """Test system validation script"""
        if not self.env_configured:
            self.skipTest("Environment not configured")
        
        from validate_system import SystemValidator
        from logger import StructuredLogger
        import yaml
        
        config_path = Path(__file__).parent.parent / 'config.yaml'
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        logger = StructuredLogger("test_validator", config.get('logging', {}))
        validator = SystemValidator(logger)
        
        # Run checks (may fail if database empty, that's OK)
        try:
            validator.run_checks()
        except Exception as e:
            self.fail(f"Validation script crashed: {e}")


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestQualityScorer))
    suite.addTests(loader.loadTestsFromTestCase(TestExceptions))
    suite.addTests(loader.loadTestsFromTestCase(TestRetryHandler))
    suite.addTests(loader.loadTestsFromTestCase(TestLogger))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigLoading))
    suite.addTests(loader.loadTestsFromTestCase(TestEndToEndWorkflow))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
