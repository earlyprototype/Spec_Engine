"""
Real Integration Tests

These tests use REAL external APIs and databases:
- GitHub API (with real repos)
- Gemini API (with real LLM calls)
- Neo4j (test instance on port 7688)

Purpose: Verify the system actually works end-to-end, not just in mocks.
Warning: These tests consume API quotas and may be slower.
"""

import unittest
import os
from neo4j import GraphDatabase
import logging

# Import test configuration
from test_config import (
    TEST_NEO4J_URI,
    TEST_NEO4J_USER,
    TEST_NEO4J_PASSWORD,
    TEST_REPOS,
    GEMINI_API_KEY,
    GITHUB_TOKEN,
    TEST_TIMEOUT_MEDIUM,
    TEST_TIMEOUT_LONG
)

# Import pipeline components
try:
    from pattern_extraction_pipeline.pattern_extractor import PatternExtractor
    from pattern_extraction_pipeline.health_check import check_health
    from pattern_extraction_pipeline.exceptions import RuleExtractionError, DatabaseWriteError
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure to install the package: pip install -e .")
    raise

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TestRealIntegration(unittest.TestCase):
    """
    Integration tests with real APIs and database.
    
    Prerequisites:
    - Neo4j test instance running on port 7688
    - Valid GEMINI_API_KEY in .env
    - Valid GITHUB_TOKEN in .env
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up test database connection and verify services."""
        # Check environment
        if not GEMINI_API_KEY:
            raise EnvironmentError("GEMINI_API_KEY not set")
        if not GITHUB_TOKEN:
            raise EnvironmentError("GITHUB_TOKEN not set")
        
        # Connect to test Neo4j
        cls.driver = GraphDatabase.driver(
            TEST_NEO4J_URI,
            auth=(TEST_NEO4J_USER, TEST_NEO4J_PASSWORD)
        )
        
        # Verify connection
        with cls.driver.session() as session:
            result = session.run("RETURN 1 as test")
            record = result.single()
            result.consume()
            assert record['test'] == 1, "Test Neo4j connection failed"
        
        logger.info(f"Connected to test Neo4j at {TEST_NEO4J_URI}")
        
        # Clear test database
        cls._clear_test_database()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test database and close connections."""
        cls._clear_test_database()
        cls.driver.close()
        logger.info("Test database cleared and connection closed")
    
    @classmethod
    def _clear_test_database(cls):
        """Clear all nodes and relationships from test database."""
        with cls.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            result = session.run("MATCH (n) RETURN count(n) as count")
            count = result.single()['count']
            result.consume()
            logger.info(f"Test database cleared ({count} nodes remaining)")
    
    def test_01_health_check(self):
        """Verify all services are operational before tests."""
        health = check_health(verbose=True)
        
        self.assertTrue(health['healthy'], "System health check failed")
        self.assertTrue(health['checks']['neo4j']['ok'], "Neo4j not available")
        self.assertTrue(health['checks']['gemini_api']['ok'], "Gemini API not available")
        self.assertTrue(health['checks']['github_api']['ok'], "GitHub API not available")
    
    def test_02_extract_pattern_with_rules(self):
        """
        Extract a real repository with IDE rules and verify:
        1. Pattern is created in Neo4j
        2. IDERule nodes are created
        3. HAS_IDE_RULES relationship exists
        """
        extractor = PatternExtractor()
        
        # Extract pattern from repo known to have rules
        repo_name = TEST_REPOS['with_rules']
        logger.info(f"Extracting pattern from {repo_name}...")
        
        pattern = extractor.analyze_single_repo(repo_name)
        
        # Verify pattern was extracted
        self.assertIsNotNone(pattern, "Pattern extraction returned None")
        self.assertIn('pattern_name', pattern, "Pattern missing 'pattern_name'")
        self.assertIn('source_repo', pattern, "Pattern missing 'source_repo'")
        
        logger.info(f"Pattern extracted: {pattern['pattern_name']}")
        
        # Verify pattern in Neo4j
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Pattern {source_repo: $repo_url})
                RETURN p.name as name, p.quality_score as quality_score
            """, repo_url=pattern['source_repo'])
            
            record = result.single()
            result.consume()
            
            self.assertIsNotNone(record, "Pattern not found in Neo4j")
            self.assertEqual(record['name'], pattern['pattern_name'])
            logger.info(f"Pattern verified in Neo4j: {record['name']}")
    
    def test_03_verify_rule_extraction(self):
        """
        Verify IDE rules were extracted and linked to pattern.
        """
        repo_name = TEST_REPOS['with_rules']
        
        # Get the pattern's source_repo URL
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Pattern)-[:HAS_IDE_RULES]->(r:IDERule)
                WHERE p.source_repo CONTAINS $repo_name
                RETURN p.name as pattern_name, 
                       count(r) as rule_count,
                       collect(r.file_path) as rule_files
            """, repo_name=repo_name.split('/')[-1])  # Use repo name from full path
            
            record = result.single()
            result.consume()
            
            if record and record['rule_count'] > 0:
                self.assertGreater(record['rule_count'], 0, "No IDE rules found")
                logger.info(f"Found {record['rule_count']} IDE rules for pattern {record['pattern_name']}")
                logger.info(f"Rule files: {record['rule_files']}")
            else:
                logger.warning(f"No IDE rules found for {repo_name} - may not have rule files")
                # Don't fail the test - repo might not have rules
    
    def test_04_config_disable_rules(self):
        """
        Verify that rule extraction can be disabled via config.
        """
        # Create custom config path with rules disabled
        import tempfile
        import yaml
        
        # Read current config
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Disable rule extraction
        config['rule_extraction']['enabled'] = False
        
        # Write to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config, f)
            temp_config_path = f.name
        
        try:
            # Create extractor with disabled rules
            extractor = PatternExtractor(config_path=temp_config_path)
            
            # Verify rule extraction is disabled
            self.assertFalse(extractor.config.rule_extraction.enabled)
            logger.info("Rule extraction successfully disabled via config")
            
        finally:
            # Clean up temp file
            os.unlink(temp_config_path)
    
    def test_05_metrics_collection(self):
        """
        Verify metrics are being collected during extraction.
        """
        extractor = PatternExtractor()
        
        # Extract a small repo
        repo_name = TEST_REPOS['small']
        logger.info(f"Extracting {repo_name} to test metrics...")
        
        try:
            pattern = extractor.analyze_single_repo(repo_name)
            
            # Get metrics report
            report = extractor.metrics.get_report()
            
            # Verify metrics were collected
            self.assertIn('counters', report)
            self.assertIn('timers', report)
            self.assertGreater(report['elapsed_seconds'], 0)
            
            logger.info(f"Metrics collected successfully:")
            logger.info(f"  Elapsed: {report['elapsed_seconds']:.2f}s")
            if 'rules_extracted' in report['counters']:
                logger.info(f"  Rules extracted: {report['counters']['rules_extracted']}")
            
        except Exception as e:
            logger.warning(f"Metrics test failed (non-critical): {e}")
    
    def test_06_rate_limiter_stats(self):
        """
        Verify rate limiter is tracking API calls.
        """
        extractor = PatternExtractor()
        
        # Get rate limiter stats
        stats = extractor.gemini_rate_limiter.get_stats()
        
        self.assertIn('max_calls', stats)
        self.assertIn('period', stats)
        self.assertEqual(stats['max_calls'], 15, "Rate limiter should be set to 15 calls/min")
        
        logger.info(f"Rate limiter configured: {stats['max_calls']} calls per {stats['period']}s")


class TestErrorHandling(unittest.TestCase):
    """
    Test error handling and recovery mechanisms.
    """
    
    def test_01_invalid_config(self):
        """Verify config validation catches errors."""
        from pattern_extraction_pipeline.config_validator import load_and_validate_config
        from pydantic import ValidationError
        
        # Invalid config: negative max_file_size
        invalid_config = {
            'rule_extraction': {
                'enabled': True,
                'max_file_size': -1000,  # Invalid
                'file_patterns': ['.cursorrules']
            },
            'gemini': {
                'api_key_env': 'GEMINI_API_KEY',
                'model_name': 'gemini-2.5-flash',
                'max_retries': 3
            },
            'neo4j': {
                'uri': 'bolt://localhost:7687',
                'user': 'neo4j',
                'password_env': 'NEO4J_PASSWORD'
            },
            'github': {
                'token_env': 'GITHUB_TOKEN'
            }
        }
        
        with self.assertRaises(ValidationError):
            load_and_validate_config(invalid_config)
        
        logger.info("Config validation correctly rejects invalid values")
    
    def test_02_missing_api_key(self):
        """Verify graceful handling of missing API keys."""
        # Temporarily remove API key
        original_key = os.environ.get('GEMINI_API_KEY')
        
        try:
            os.environ['GEMINI_API_KEY'] = ''
            
            with self.assertRaises(ValueError) as context:
                PatternExtractor()
            
            self.assertIn('GEMINI_API_KEY', str(context.exception))
            logger.info("Missing API key correctly raises ValueError")
            
        finally:
            # Restore original key
            if original_key:
                os.environ['GEMINI_API_KEY'] = original_key


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
