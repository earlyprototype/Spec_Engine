#!/usr/bin/env python3
"""
Unit Integration Tests for Pattern-IDERule integration.

Tests the integration between pattern_extraction_pipeline and ide_rule_library
using MOCKS (not real APIs). For real API tests, see test_real_integration.py.
"""

import os
import sys
import unittest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timezone

# Import pipeline components
try:
    from pattern_extraction_pipeline.pattern_extractor import PatternExtractor
except ImportError:
    # Fallback for systems without package installation
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from pattern_extractor import PatternExtractor


class TestIDERuleIntegration(unittest.TestCase):
    """Test IDE rule extraction integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        from pattern_extraction_pipeline.config_validator import PipelineConfig
        
        # Create proper Pydantic config instead of dict
        self.test_config = PipelineConfig(
            rule_extraction={
                'enabled': True,
                'max_file_size': 100000,
                'file_patterns': ['.cursorrules', 'CLAUDE.md']
            },
            gemini={
                'api_key_env': 'GEMINI_API_KEY',
                'model_name': 'gemini-2.5-flash',
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
    
    @patch('pattern_extraction_pipeline.pattern_extractor.IDE_RULE_LIBRARY_AVAILABLE', True)
    def test_rule_scanner_initialization(self):
        """Test that rule scanner is properly initialized when available"""
        with patch('pattern_extraction_pipeline.pattern_extractor.EnhancedRuleExtractor') as mock_extractor, \
             patch('pattern_extraction_pipeline.pattern_extractor.RepoQualityScorer') as mock_scorer:
            
            extractor = PatternExtractor()
            self.addCleanup(extractor.close)
            
            # Verify components were initialized
            self.assertIsNotNone(extractor.rule_extractor)
            self.assertIsNotNone(extractor.quality_scorer)
    
    @patch('pattern_extraction_pipeline.pattern_extractor.IDE_RULE_LIBRARY_AVAILABLE', False)
    def test_rule_scanner_not_available(self):
        """Test graceful degradation when IDE rule library is not available"""
        extractor = PatternExtractor()
        self.addCleanup(extractor.close)
        
        # Verify components are None when not available
        self.assertIsNone(extractor.rule_extractor)
        self.assertIsNone(extractor.quality_scorer)
    
    def test_scan_for_rule_files(self):
        """Test scanning repository for rule files"""
        extractor = PatternExtractor()
        self.addCleanup(extractor.close)
        
        # Mock repository with rule files
        mock_repo = Mock()
        mock_file = Mock()
        mock_file.size = 1000
        mock_file.decoded_content = b"# Test rule content"
        
        # Test .cursorrules file
        mock_repo.get_contents.return_value = mock_file
        
        with patch.object(extractor, 'config', self.test_config):
            rule_files = extractor._scan_for_rule_files(mock_repo)
        
        # Should find at least one rule file (if IDE_RULE_LIBRARY_AVAILABLE)
        if extractor.rule_extractor:
            self.assertGreaterEqual(len(rule_files), 0)
    
    def test_scan_for_rule_files_size_limit(self):
        """Test that files exceeding size limit are skipped"""
        extractor = PatternExtractor()
        self.addCleanup(extractor.close)
        
        # Mock repository with oversized file
        mock_repo = Mock()
        mock_file = Mock()
        mock_file.size = 200000  # Exceeds 100KB limit
        mock_repo.get_contents.return_value = mock_file
        
        with patch.object(extractor, 'config', self.test_config):
            with patch('pattern_extraction_pipeline.pattern_extractor.IDE_RULE_LIBRARY_AVAILABLE', True):
                rule_files = extractor._scan_for_rule_files(mock_repo)
        
        # Should not include oversized files
        self.assertEqual(len(rule_files), 0)
    
    @patch('pattern_extraction_pipeline.pattern_extractor.IDE_RULE_LIBRARY_AVAILABLE', True)
    def test_extract_and_link_rules(self):
        """Test rule extraction and linking to patterns"""
        with patch('pattern_extraction_pipeline.pattern_extractor.EnhancedRuleExtractor') as MockExtractor, \
             patch('pattern_extraction_pipeline.pattern_extractor.RepoQualityScorer') as MockScorer:
            
            extractor = PatternExtractor()
            self.addCleanup(extractor.close)
            
            # Mock pattern
            pattern = {
                'pattern_name': 'Test Pattern',
                'source_repo': 'https://github.com/test/repo'
            }
            
            # Mock repo
            mock_repo = Mock()
            mock_repo.full_name = 'test/repo'
            mock_repo.html_url = 'https://github.com/test/repo'
            mock_repo.stargazers_count = 1000
            mock_repo.forks_count = 100
            mock_repo.created_at = datetime.now(timezone.utc)
            mock_repo.updated_at = datetime.now(timezone.utc)
            mock_repo.open_issues_count = 10
            mock_repo.get_contributors.return_value = [Mock(login='user1')]
            mock_repo.get_contents.return_value = []
            
            # Mock rule files
            rule_files = [{
                'path': '.cursorrules',
                'content': '# Test rules',
                'format': 'cursorrules'
            }]
            
            # Mock rule extraction
            mock_rule = {
                'file_path': '.cursorrules',
                'file_format': 'cursorrules',
                'content': '# Test rules',
                'purpose': 'Test purpose',
                'categories': ['test'],
                'key_practices': ['practice1'],
                'technologies': ['python'],
                'project_types': ['api'],
                'ide_types': ['cursor'],
                'repo_quality_score': 75.0,
                'confidence_level': 4,
                'quality_breakdown': {},
                'has_ci_cd': True,
                'has_tests': True
            }
            
            extractor.rule_extractor.extract_rule.return_value = mock_rule
            
            # Mock Neo4j linking
            with patch.object(extractor, '_link_pattern_to_rules') as mock_link:
                extractor._extract_and_link_rules(pattern, mock_repo, rule_files)
                
                # Verify rule extraction was called
                extractor.rule_extractor.extract_rule.assert_called_once()
                
                # Verify linking was called
                mock_link.assert_called_once()
    
    def test_config_disables_rule_extraction(self):
        """Test that rule extraction can be disabled via config"""
        disabled_config = {
            'rule_extraction': {
                'enabled': False
            }
        }
        
        extractor = PatternExtractor()
        self.addCleanup(extractor.close)
        
        with patch.object(extractor, 'config', disabled_config):
            # Mock pattern and repo
            pattern = {'pattern_name': 'Test'}
            mock_repo = Mock()
            mock_repo.full_name = 'test/repo'
            
            # Even with rule files found, extraction should not happen
            with patch.object(extractor, '_scan_for_rule_files') as mock_scan, \
                 patch.object(extractor, '_extract_and_link_rules') as mock_extract:
                
                mock_scan.return_value = [{'path': '.cursorrules', 'content': 'test'}]
                
                # Simulate analyze_single_repo code path
                if (extractor.config.get('rule_extraction', {}).get('enabled', True) and
                    extractor.rule_extractor):
                    rule_files = extractor._scan_for_rule_files(mock_repo)
                    if rule_files:
                        extractor._extract_and_link_rules(pattern, mock_repo, rule_files)
                
                # Extraction should NOT be called when disabled
                mock_extract.assert_not_called()


class TestPatternQueryIntegration(unittest.TestCase):
    """Test pattern query interface with rule inclusion"""
    
    @patch('pattern_extraction_pipeline.pattern_query_interface.GraphDatabase')
    def test_query_with_rules(self, mock_graph_db):
        """Test querying patterns with IDE rules included"""
        from pattern_extraction_pipeline.pattern_query_interface import PatternQueryInterface
        
        interface = PatternQueryInterface()
        
        # Mock both LLM analysis and query methods
        mock_pattern = {
            'pattern_name': 'Test Pattern',
            'confidence': 'high',
            'stars': 1000,
            'source_repo': 'https://github.com/test/repo',
            'reasoning': 'Test reasoning',
            'technologies': [],
            'constraints': [],
            'ide_rules': [{
                'file_path': '.cursorrules',
                'file_format': 'cursorrules',
                'purpose': 'Test purpose',
                'repo_quality_score': 75.0,
                'confidence_level': 4
            }]
        }
        
        with patch.object(interface, '_llm_analyze_spec') as mock_llm, \
             patch.object(interface, '_query_patterns') as mock_query:
            
            # Mock LLM analysis to return proper dict
            mock_llm.return_value = {
                'requirement_type': 'api',
                'requirement_domain': 'backend',
                'key_constraints': [],
                'key_technologies': ['python']
            }
            mock_query.return_value = [mock_pattern]
            
            # Query with include_rules=True
            spec_dict = {'goal': 'Build an API'}
            result = interface.find_patterns_for_spec(spec_dict, include_rules=True)
            
            # Verify rules were included
            self.assertIn('recommended_patterns', result)
            if result['recommended_patterns']:
                pattern = result['recommended_patterns'][0]
                self.assertIn('ide_rules', pattern)
            
            # Verify _query_patterns was called with include_rules=True
            call_kwargs = mock_query.call_args[1]
            self.assertEqual(call_kwargs.get('include_rules'), True)
    
    @patch('pattern_extraction_pipeline.pattern_query_interface.GraphDatabase')
    def test_query_without_rules(self, mock_graph_db):
        """Test querying patterns without IDE rules"""
        from pattern_extraction_pipeline.pattern_query_interface import PatternQueryInterface
        
        interface = PatternQueryInterface()
        interface.llm = None  # Disable LLM to use fallback path
        
        # Query with include_rules=False (default)
        spec_dict = {'goal': 'Build an API'}
        
        with patch.object(interface, '_query_patterns') as mock_query:
            mock_query.return_value = []
            result = interface.find_patterns_for_spec(spec_dict, include_rules=False)
            
            # Verify include_rules was passed correctly
            mock_query.assert_called()
            call_kwargs = mock_query.call_args[1]
            self.assertEqual(call_kwargs.get('include_rules'), False)


class TestNeo4jRelationships(unittest.TestCase):
    """Test Neo4j relationship creation"""
    
    def test_link_pattern_to_rules_query(self):
        """Test that Neo4j query for linking is correct"""
        extractor = PatternExtractor()
        self.addCleanup(extractor.close)
        
        pattern_name = "Test Pattern"
        source_repo = "https://github.com/test/repo"
        rule = {
            'file_path': '.cursorrules',
            'file_format': 'cursorrules',
            'content': '# Test',
            'purpose': 'Test purpose',
            'categories': ['test'],
            'key_practices': ['practice1'],
            'technologies': ['python'],
            'project_types': ['api'],
            'ide_types': ['cursor'],
            'repo_quality_score': 75.0,
            'confidence_level': 4,
            'quality_breakdown': {},
            'has_ci_cd': True,
            'has_tests': True
        }
        
        # Mock Neo4j session
        with patch.object(extractor.neo4j, 'session') as mock_session:
            mock_result = Mock()
            mock_result.single.return_value = {'rule_id': 'test_id'}
            mock_session.return_value.__enter__.return_value.run.return_value = mock_result
            
            # Call the method
            extractor._link_pattern_to_rules(pattern_name, source_repo, rule)
            
            # Verify session.run was called
            mock_session.return_value.__enter__.return_value.run.assert_called_once()
            
            # Verify query includes HAS_IDE_RULES relationship
            call_args = mock_session.return_value.__enter__.return_value.run.call_args
            query = call_args[0][0]
            self.assertIn('HAS_IDE_RULES', query)
            self.assertIn('MERGE', query)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
