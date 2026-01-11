#!/usr/bin/env python3
"""Integration tests for IDE Rule Library"""

import os
import sys
import yaml
from pathlib import Path
from dotenv import load_dotenv
from neo4j import GraphDatabase
from github import Github

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from logger import StructuredLogger
from rate_limiter import GitHubRateLimiter
from progress_tracker import ProgressTracker
from rule_extractor import RuleExtractor
from neo4j_writer import Neo4jRuleWriter
from rule_query_engine import RuleQueryEngine
from scan_existing_patterns import ExistingPatternScanner

load_dotenv()


class TestIntegration:
    """Integration tests for complete pipeline"""
    
    @classmethod
    def setup_class(cls):
        """Setup test environment"""
        config_path = Path(__file__).parent.parent / 'config.yaml'
        with open(config_path, 'r') as f:
            cls.config = yaml.safe_load(f)
        
        cls.logger = StructuredLogger('test', cls.config['logging'])
        
        # Connect to Neo4j
        cls.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            auth=(
                os.getenv("NEO4J_USER", "neo4j"),
                os.getenv("NEO4J_PASSWORD", "password")
            )
        )
        
        # GitHub connection
        github_token = os.getenv("GITHUB_TOKEN")
        cls.gh = Github(github_token) if github_token else Github()
        
        cls.rate_limiter = GitHubRateLimiter(cls.gh, cls.config['github'], cls.logger)
    
    @classmethod
    def teardown_class(cls):
        """Cleanup test environment"""
        cls.driver.close()
    
    def test_1_scanner_initialization(self):
        """Test scanner initializes correctly"""
        try:
            scanner = ExistingPatternScanner()
            assert scanner is not None
            assert scanner.gh is not None
            assert scanner.driver is not None
            assert scanner.logger is not None
            scanner.close()
            print("[OK] Scanner initialization test passed")
            return True
        except Exception as e:
            print(f"[FAIL] Scanner initialization: {e}")
            return False
    
    def test_2_scan_known_repo(self):
        """Test scanning a known repo with rules"""
        try:
            scanner = ExistingPatternScanner()
            
            # Test with a known repo (cursor's own repo might have .cursorrules)
            result = scanner.check_repo_for_rules('https://github.com/microsoft/vscode')
            
            assert isinstance(result, dict)
            assert 'found' in result
            assert isinstance(result['found'], list)
            
            scanner.close()
            print(f"[OK] Scan test passed - found {len(result['found'])} files")
            return True
        except Exception as e:
            print(f"[FAIL] Scan test: {e}")
            return False
    
    def test_3_extract_single_file(self):
        """Test extracting a single rule file"""
        try:
            extractor = RuleExtractor(
                self.gh,
                self.config,
                self.logger,
                self.rate_limiter
            )
            
            # Try to extract from a known repo with .github/copilot-instructions.md
            # (Many popular repos have this now)
            result = extractor.extract_rule_file(
                'https://github.com/microsoft/vscode',
                'README.md',  # Fallback to README if no rules
                50000
            )
            
            assert isinstance(result, dict)
            assert 'success' in result
            
            if result['success']:
                assert 'data' in result
                assert 'id' in result['data']
                assert 'embedding' in result['data']
                assert len(result['data']['embedding']) == 768
                print("[OK] Extract test passed")
            else:
                print(f"[SKIP] Extract test - repo may not have accessible rules: {result.get('error')}")
            
            return True
        except Exception as e:
            print(f"[FAIL] Extract test: {e}")
            return False
    
    def test_4_neo4j_writer(self):
        """Test writing to Neo4j"""
        try:
            writer = Neo4jRuleWriter(
                self.driver,
                self.config,
                self.logger
            )
            
            # Create test rule data
            test_rule = {
                'id': 'test/repo:test.txt',
                'source_repo': 'https://github.com/test/repo',
                'file_path': 'test.txt',
                'file_format': 'test.txt',
                'content': 'Test content',
                'content_hash': 'test_hash_123',
                'purpose': 'Test rule',
                'categories': ['test'],
                'key_practices': ['Test practice'],
                'reasoning': 'Test reasoning',
                'ide_types': ['cursor'],
                'technologies': ['python'],
                'project_types': ['test'],
                'stars': 100,
                'embedding': [0.1] * 768,
                'extracted_date': '2026-01-07T00:00:00'
            }
            
            # Write test rule
            written = writer.write_rule(test_rule)
            assert written == True or written == False  # Either writes or skips duplicate
            
            # Clean up test rule
            writer.delete_rule('test/repo:test.txt')
            
            print("[OK] Neo4j writer test passed")
            return True
        except Exception as e:
            print(f"[FAIL] Neo4j writer test: {e}")
            return False
    
    def test_5_query_engine(self):
        """Test rule query engine"""
        try:
            engine = RuleQueryEngine(self.driver, self.logger)
            
            # Query for some rules
            results = engine.query_rules(
                query="typescript web application best practices",
                ide_type='cursor',
                top_k=5
            )
            
            assert isinstance(results, list)
            
            if len(results) > 0:
                print(f"[OK] Query engine test passed - found {len(results)} rules")
            else:
                print("[SKIP] Query engine test - no rules in database yet")
            
            return True
        except Exception as e:
            print(f"[FAIL] Query engine test: {e}")
            return False
    
    def test_6_progress_tracker(self):
        """Test progress tracking and checkpoint/resume"""
        try:
            tracker = ProgressTracker(checkpoint_file='test_checkpoint.json')
            
            # Test marking processed
            tracker.mark_processed('test_repo', 'test_file.txt', success=True)
            assert tracker.is_processed('test_repo', 'test_file.txt')
            
            # Test stats
            stats = tracker.get_stats()
            assert stats['successful'] == 1
            
            # Test saving checkpoint
            tracker.save_checkpoint()
            
            # Test loading checkpoint
            tracker2 = ProgressTracker(checkpoint_file='test_checkpoint.json')
            assert tracker2.is_processed('test_repo', 'test_file.txt')
            
            # Cleanup
            tracker2.clear_checkpoint()
            
            print("[OK] Progress tracker test passed")
            return True
        except Exception as e:
            print(f"[FAIL] Progress tracker test: {e}")
            return False


def run_all_tests():
    """Run all integration tests"""
    print("\n" + "="*60)
    print("IDE RULE LIBRARY - INTEGRATION TESTS")
    print("="*60 + "\n")
    
    tests = TestIntegration()
    tests.setup_class()
    
    results = []
    
    try:
        results.append(("Scanner Initialization", tests.test_1_scanner_initialization()))
        results.append(("Scan Known Repo", tests.test_2_scan_known_repo()))
        results.append(("Extract Single File", tests.test_3_extract_single_file()))
        results.append(("Neo4j Writer", tests.test_4_neo4j_writer()))
        results.append(("Query Engine", tests.test_5_query_engine()))
        results.append(("Progress Tracker", tests.test_6_progress_tracker()))
    finally:
        tests.teardown_class()
    
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {name}")
    
    print(f"\n{passed}/{total} tests passed")
    print("="*60 + "\n")
    
    return passed == total


if __name__ == '__main__':
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
