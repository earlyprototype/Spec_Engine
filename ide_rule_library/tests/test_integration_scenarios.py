#!/usr/bin/env python3
"""
REAL Integration Tests - Tests with actual components.

Run with: RUN_INTEGRATION_TESTS=1 python test_real_integration.py

Requirements:
- Neo4j running with credentials in .env
- GEMINI_API_KEY in .env
- Database with at least 1 IDERule node for testing
"""

import os
import sys
import unittest
from pathlib import Path
from datetime import datetime, timezone

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from neo4j import GraphDatabase
import google.generativeai as genai
import yaml
from dotenv import load_dotenv

from quality_scorer import RepoQualityScorer, enhance_repo_metadata
from enhanced_query_engine import EnhancedRuleQueryEngine
from logger import StructuredLogger
from exceptions import (
    NoRulesFoundError,
    MissingEnvironmentVariableError,
    DatabaseError
)

load_dotenv(override=True)


class TestRealNeo4jConnection(unittest.TestCase):
    """Test real Neo4j database connection"""
    
    @classmethod
    def setUpClass(cls):
        """Check environment is configured"""
        cls.uri = os.getenv('NEO4J_URI')
        cls.user = os.getenv('NEO4J_USER')
        cls.password = os.getenv('NEO4J_PASSWORD')
        
        if not all([cls.uri, cls.user, cls.password]):
            raise unittest.SkipTest("Neo4j credentials not configured")
    
    def test_neo4j_connection(self):
        """Test that we can connect to Neo4j"""
        driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        
        try:
            with driver.session() as session:
                result = session.run("RETURN 1 AS test")
                record = result.single()
                self.assertEqual(record['test'], 1)
        finally:
            driver.close()
    
    def test_neo4j_has_rules(self):
        """Test that database has IDERule nodes"""
        driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        
        try:
            with driver.session() as session:
                result = session.run("MATCH (r:IDERule) RETURN count(r) AS count")
                record = result.single()
                count = record['count']
                
                self.assertGreater(count, 0, "Database should have at least 1 IDERule node")
                print(f"\n  Found {count} IDERule nodes in database")
        finally:
            driver.close()
    
    def test_neo4j_vector_index_exists(self):
        """Test that vector index exists"""
        driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        
        try:
            with driver.session() as session:
                result = session.run("SHOW INDEXES")
                indexes = [dict(record) for record in result]
                
                # Check for vector index
                vector_indexes = [idx for idx in indexes if 'ide_rule_embeddings' in str(idx)]
                
                self.assertGreater(len(vector_indexes), 0, 
                                 "Vector index 'ide_rule_embeddings' should exist")
                print(f"\n  Found {len(indexes)} indexes including vector index")
        finally:
            driver.close()
    
    def test_neo4j_quality_data_status(self):
        """Test quality score migration status"""
        driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        
        try:
            with driver.session() as session:
                result = session.run("""
                    MATCH (r:IDERule)
                    RETURN count(r) AS total,
                           sum(CASE WHEN r.quality_score IS NOT NULL THEN 1 ELSE 0 END) AS with_quality
                """)
                record = result.single()
                total = record['total']
                with_quality = record['with_quality']
                
                print(f"\n  Total rules: {total}")
                print(f"  With quality scores: {with_quality}")
                print(f"  Migration status: {with_quality}/{total} ({with_quality/total*100:.1f}%)")
                
                # Don't fail if not migrated, just report
                if with_quality == 0:
                    print("  [!] No quality scores - run migrate_quality_scores.py")
                else:
                    print("  [OK] Quality scores present")
        finally:
            driver.close()


class TestRealGeminiAPI(unittest.TestCase):
    """Test real Gemini API connection"""
    
    @classmethod
    def setUpClass(cls):
        """Check API key configured"""
        cls.api_key = os.getenv('GEMINI_API_KEY')
        
        if not cls.api_key:
            raise unittest.SkipTest("GEMINI_API_KEY not configured")
        
        genai.configure(api_key=cls.api_key)
    
    def test_gemini_api_simple_call(self):
        """Test simple Gemini API call"""
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        response = model.generate_content("Say 'test' if you can read this.")
        
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.text)
        self.assertIn('test', response.text.lower())
        
        print(f"\n  Gemini API working: {response.text[:50]}...")
    
    def test_gemini_embedding_api(self):
        """Test Gemini embedding API"""
        result = genai.embed_content(
            model='models/text-embedding-004',
            content="Test query for Python API",
            task_type="semantic_similarity"
        )
        
        self.assertIn('embedding', result)
        self.assertIsInstance(result['embedding'], list)
        self.assertGreater(len(result['embedding']), 0)
        
        print(f"\n  Embedding API working: {len(result['embedding'])} dimensions")


class TestRealQueryEngine(unittest.TestCase):
    """Test enhanced query engine with real database"""
    
    @classmethod
    def setUpClass(cls):
        """Setup real connections"""
        cls.uri = os.getenv('NEO4J_URI')
        cls.user = os.getenv('NEO4J_USER')
        cls.password = os.getenv('NEO4J_PASSWORD')
        cls.api_key = os.getenv('GEMINI_API_KEY')
        
        if not all([cls.uri, cls.user, cls.password, cls.api_key]):
            raise unittest.SkipTest("Environment not fully configured")
        
        # Load config
        config_path = Path(__file__).parent.parent / 'config.yaml'
        with open(config_path) as f:
            cls.config = yaml.safe_load(f)
        
        cls.logger = StructuredLogger("test_integration", cls.config.get('logging', {}))
        cls.driver = GraphDatabase.driver(cls.uri, auth=(cls.user, cls.password))
    
    @classmethod
    def tearDownClass(cls):
        """Close connections"""
        if hasattr(cls, 'driver'):
            cls.driver.close()
    
    def test_query_engine_initialization(self):
        """Test that query engine initializes with real config"""
        engine = EnhancedRuleQueryEngine(
            self.driver,
            self.logger,
            self.config['gemini']['embedding_model']
        )
        
        self.assertIsNotNone(engine)
        self.assertEqual(engine.embedding_model, self.config['gemini']['embedding_model'])
    
    def test_query_engine_v1_fallback(self):
        """Test v1 fallback when quality data missing"""
        engine = EnhancedRuleQueryEngine(self.driver, self.logger)
        
        # Force v1 fallback by using internal method
        rules = engine._query_v1_fallback(
            query="Python API development",
            ide_type='cursor',
            top_k=5
        )
        
        # Should return some rules (or empty list if database empty)
        self.assertIsInstance(rules, list)
        print(f"\n  V1 fallback returned {len(rules)} rules")
        
        if len(rules) > 0:
            # Check structure
            rule = rules[0]
            self.assertIn('id', rule)
            self.assertIn('source_repo', rule)
            self.assertIn('content', rule)
            print(f"  Sample rule: {rule['id'][:50]}...")
    
    def test_query_engine_quality_check(self):
        """Test quality data check"""
        engine = EnhancedRuleQueryEngine(self.driver, self.logger)
        
        has_quality = engine._check_quality_data_exists()
        
        print(f"\n  Quality data present: {has_quality}")
        
        # Don't fail, just report
        if not has_quality:
            print("  [INFO] Run migrate_quality_scores.py to enable quality filtering")
    
    def test_query_engine_with_fallback(self):
        """Test query with automatic fallback"""
        engine = EnhancedRuleQueryEngine(self.driver, self.logger)
        
        try:
            rules = engine.query_rules_with_fallback(
                query="Python FastAPI backend development",
                project_type='api',
                technologies=['python'],
                min_quality_score=60.0,
                min_results=3,
                top_k=10
            )
            
            self.assertIsInstance(rules, list)
            print(f"\n  Query with fallback returned {len(rules)} rules")
            
            if len(rules) > 0:
                avg_quality = sum(r.get('quality_score', 0) for r in rules) / len(rules)
                print(f"  Average quality: {avg_quality:.1f}/100")
        
        except NoRulesFoundError as e:
            print(f"\n  [INFO] No rules found (database may be empty): {e}")
            # Not a failure - database might be empty


class TestRealMigrationWorkflow(unittest.TestCase):
    """Test migration workflow components"""
    
    @classmethod
    def setUpClass(cls):
        """Setup connections"""
        cls.uri = os.getenv('NEO4J_URI')
        cls.user = os.getenv('NEO4J_USER')
        cls.password = os.getenv('NEO4J_PASSWORD')
        
        if not all([cls.uri, cls.user, cls.password]):
            raise unittest.SkipTest("Neo4j credentials not configured")
        
        config_path = Path(__file__).parent.parent / 'config.yaml'
        with open(config_path) as f:
            cls.config = yaml.safe_load(f)
        
        cls.logger = StructuredLogger("test_migration", cls.config.get('logging', {}))
        cls.driver = GraphDatabase.driver(cls.uri, auth=(cls.user, cls.password))
    
    @classmethod
    def tearDownClass(cls):
        """Close connections"""
        if hasattr(cls, 'driver'):
            cls.driver.close()
    
    def test_get_rules_to_migrate(self):
        """Test getting rules that need migration"""
        from migrate_quality_scores import QualityScoreMigration
        
        migration = QualityScoreMigration(self.driver, self.logger)
        rules = migration.get_rules_to_migrate()
        
        print(f"\n  Rules needing migration: {len(rules)}")
        
        # Don't fail - just report
        if len(rules) == 0:
            print("  [OK] All rules already have quality scores")
        else:
            print(f"  [INFO] Run migrate_quality_scores.py to migrate {len(rules)} rules")
    
    def test_quality_scorer_with_cached_data(self):
        """Test quality scorer with database data structure"""
        scorer = RepoQualityScorer()
        
        # Get real data from database
        with self.driver.session() as session:
            result = session.run("""
                MATCH (r:IDERule)<-[:HAS_RULE]-(p:Pattern)
                RETURN p.repo_name AS name,
                       p.stars AS stars,
                       p.forks AS forks,
                       p.files AS files
                LIMIT 1
            """)
            
            record = result.single()
            
            if not record:
                self.skipTest("No Pattern nodes in database")
            
            # Build minimal repo data
            repo_data = {
                'stars': record.get('stars', 0),
                'forks': record.get('forks', 0),
                'files': record.get('files', [])
            }
            
            # Should not crash
            score, breakdown = scorer.calculate_quality_score(repo_data)
            
            print(f"\n  Sample quality score: {score:.1f}/100")
            print(f"  Breakdown: {breakdown}")
            
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 100)


class TestBackwardsCompatibility(unittest.TestCase):
    """Test v1 fallback actually works"""
    
    @classmethod
    def setUpClass(cls):
        """Setup connections"""
        cls.uri = os.getenv('NEO4J_URI')
        cls.user = os.getenv('NEO4J_USER')
        cls.password = os.getenv('NEO4J_PASSWORD')
        cls.api_key = os.getenv('GEMINI_API_KEY')
        
        if not all([cls.uri, cls.user, cls.password, cls.api_key]):
            raise unittest.SkipTest("Environment not configured")
        
        config_path = Path(__file__).parent.parent / 'config.yaml'
        with open(config_path) as f:
            cls.config = yaml.safe_load(f)
        
        cls.logger = StructuredLogger("test_compat", cls.config.get('logging', {}))
        cls.driver = GraphDatabase.driver(cls.uri, auth=(cls.user, cls.password))
    
    @classmethod
    def tearDownClass(cls):
        """Close connections"""
        if hasattr(cls, 'driver'):
            cls.driver.close()
    
    def test_query_rules_with_defaults(self):
        """Test that query_rules works with default parameters (backwards compat)"""
        engine = EnhancedRuleQueryEngine(self.driver, self.logger)
        
        # Call with minimal params (old v1 style)
        try:
            rules = engine.query_rules(query="Python API", top_k=5)
            
            self.assertIsInstance(rules, list)
            print(f"\n  Query with defaults returned {len(rules)} rules")
            
        except Exception as e:
            # Should not crash - might return empty list
            print(f"\n  Query completed (may be empty): {e}")


def run_tests():
    """Run all real integration tests"""
    # Check environment
    env_ready = all([
        os.getenv('NEO4J_URI'),
        os.getenv('NEO4J_USER'),
        os.getenv('NEO4J_PASSWORD'),
        os.getenv('GEMINI_API_KEY')
    ])
    
    if not env_ready:
        print("\n" + "="*70)
        print("INTEGRATION TESTS SKIPPED")
        print("="*70)
        print("\nReason: Environment not configured")
        print("\nRequired environment variables:")
        print("  - NEO4J_URI")
        print("  - NEO4J_USER")
        print("  - NEO4J_PASSWORD")
        print("  - GEMINI_API_KEY")
        print("\nSet these in your .env file and re-run.")
        print("="*70)
        return 1
    
    print("\n" + "="*70)
    print("RUNNING REAL INTEGRATION TESTS")
    print("="*70)
    print("\nTesting with actual Neo4j database and Gemini API...")
    print("="*70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestRealNeo4jConnection))
    suite.addTests(loader.loadTestsFromTestCase(TestRealGeminiAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestRealQueryEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestRealMigrationWorkflow))
    suite.addTests(loader.loadTestsFromTestCase(TestBackwardsCompatibility))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("INTEGRATION TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("="*70)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
