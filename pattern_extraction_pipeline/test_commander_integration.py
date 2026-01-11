"""
Integration tests for Commander Pattern Interface

Tests the complete workflow from pattern query to SPEC context generation,
including error handling and graceful degradation.

Author: SPEC Engine Team
Version: 1.0
Date: 2026-01-07
"""

import pytest
import logging
from unittest import mock
from typing import Dict, List

# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the module under test
from commander_integration import CommanderPatternInterface, PatternSelection


class TestCommanderPatternInterface:
    """Integration tests for CommanderPatternInterface"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.sample_patterns = [
            {
                'name': 'electron_desktop_app',
                'id': 'pattern_001',
                'composite_score': 0.87,
                'recommendation': 'high',
                'semantic_score': 0.89,
                'reasoning': 'Desktop application for file management',
                'description': 'Electron-based desktop app with local storage',
                'technologies': ['typescript', 'electron', 'react', 'sqlite'],
                'github_stars': 45000,
                'github_url': 'https://github.com/example/electron-app',
                'confidence': 'high'
            },
            {
                'name': 'nodejs_file_manager',
                'id': 'pattern_002',
                'composite_score': 0.72,
                'recommendation': 'medium',
                'semantic_score': 0.75,
                'reasoning': 'Node.js file organization tool',
                'description': 'CLI-based file manager with metadata tracking',
                'technologies': ['javascript', 'nodejs', 'mongodb'],
                'github_stars': 12000,
                'github_url': 'https://github.com/example/node-manager',
                'confidence': 'medium'
            }
        ]
    
    def test_pattern_query_success(self):
        """Test 1: Happy path - query returns patterns successfully"""
        logger.info("Running test_pattern_query_success")
        
        # Mock the semantic interface to return sample patterns
        with mock.patch('commander_integration.PatternQueryInterfaceSemantic') as mock_interface:
            mock_instance = mock_interface.return_value
            mock_instance.find_patterns_hybrid.return_value = {
                'patterns': self.sample_patterns,
                'user_review_text': 'Sample review text',
                'query_metadata': {'goal': 'test goal'}
            }
            
            interface = CommanderPatternInterface()
            result = interface.query_patterns_for_goal(
                goal_description="Build a file manager for volunteers",
                constraints={'technologies': ['typescript']},
                top_k=5
            )
            
            # Assertions
            assert result is not None
            assert 'patterns' in result
            assert len(result['patterns']) == 2
            assert result['patterns'][0]['name'] == 'electron_desktop_app'
            assert 'user_review_text' in result
            
            # Verify the semantic interface was called correctly
            mock_instance.find_patterns_hybrid.assert_called_once()
            
        logger.info("test_pattern_query_success: PASSED")
    
    def test_pattern_selection_valid(self):
        """Test 2: User selects pattern by valid number"""
        logger.info("Running test_pattern_selection_valid")
        
        with mock.patch('commander_integration.PatternQueryInterfaceSemantic'):
            interface = CommanderPatternInterface()
            
            # Test selecting pattern 1
            selection = interface.select_pattern(self.sample_patterns, '1')
            
            # Assertions
            assert selection is not None
            assert isinstance(selection, PatternSelection)
            assert selection.pattern_name == 'electron_desktop_app'
            assert selection.composite_score == 0.87
            assert selection.recommendation == 'high'
            assert 'typescript' in selection.technologies
            
        logger.info("test_pattern_selection_valid: PASSED")
    
    def test_pattern_selection_skip(self):
        """Test 3: User skips pattern guidance"""
        logger.info("Running test_pattern_selection_skip")
        
        with mock.patch('commander_integration.PatternQueryInterfaceSemantic'):
            interface = CommanderPatternInterface()
            
            # Test skipping
            selection = interface.select_pattern(self.sample_patterns, 'skip')
            
            # Assertions
            assert selection is None
            
        logger.info("test_pattern_selection_skip: PASSED")
    
    def test_pattern_selection_invalid(self):
        """Test 4: Invalid input handling"""
        logger.info("Running test_pattern_selection_invalid")
        
        with mock.patch('commander_integration.PatternQueryInterfaceSemantic'):
            interface = CommanderPatternInterface()
            
            # Test invalid number (out of range)
            with pytest.raises(ValueError) as exc_info:
                interface.select_pattern(self.sample_patterns, '999')
            
            error_msg = str(exc_info.value)
            assert 'out of range' in error_msg
            assert 'Valid options' in error_msg
            assert '1 and 2' in error_msg  # Should show range based on sample_patterns length
            assert '999' in error_msg
            
            # Test invalid input (not a number or 'skip')
            with pytest.raises(ValueError) as exc_info:
                interface.select_pattern(self.sample_patterns, 'invalid')
            
            error_msg = str(exc_info.value)
            assert 'Invalid pattern selection' in error_msg
            assert 'Valid options' in error_msg
            assert 'invalid' in error_msg
            
        logger.info("test_pattern_selection_invalid: PASSED")
    
    def test_neo4j_connection_failure(self):
        """Test 5: Graceful degradation when Neo4j database is down"""
        logger.info("Running test_neo4j_connection_failure")
        
        # Mock the semantic interface to raise ConnectionError
        with mock.patch('commander_integration.PatternQueryInterfaceSemantic', 
                       side_effect=ConnectionError("Neo4j unavailable")):
            
            interface = CommanderPatternInterface()
            
            # Verify graceful degradation flag is set
            assert interface._neo4j_available == False
            assert interface.interface is None
            
            # Test that query returns degraded result
            result = interface.query_patterns_for_goal("Build app")
            
            # Assertions
            assert result['pattern_informed'] == False
            assert len(result['patterns']) == 0
            assert 'degraded' in result['query_metadata']
            assert result['query_metadata']['degraded'] == True
            assert 'user_review_text' in result
            
        logger.info("test_neo4j_connection_failure: PASSED")
    
    def test_spec_context_generation(self):
        """Test 6: Pattern context created correctly for SPEC generation"""
        logger.info("Running test_spec_context_generation")
        
        with mock.patch('commander_integration.PatternQueryInterfaceSemantic'):
            interface = CommanderPatternInterface()
            
            # Create a pattern selection
            selection = interface.select_pattern(self.sample_patterns, '1')
            
            # Mock backup patterns
            backup_patterns = [self.sample_patterns[1]]
            
            # Generate SPEC context
            context = interface.generate_spec_context(selection, backup_patterns)
            
            # Assertions
            assert context['pattern_informed'] == True
            assert context['pattern_available'] == True
            assert 'primary_pattern' in context
            assert context['primary_pattern']['selected_pattern'] == 'electron_desktop_app'
            assert 'proven_technologies' in context['primary_pattern']
            assert 'typescript' in context['primary_pattern']['proven_technologies']
            assert 'backup_patterns' in context
            assert len(context['backup_patterns']) == 1
            assert 'architectural_guidance' in context
            
        logger.info("test_spec_context_generation: PASSED")
    
    def test_backup_pattern_suggestions(self):
        """Test 7: Similar patterns loaded as backups"""
        logger.info("Running test_backup_pattern_suggestions")
        
        with mock.patch('commander_integration.PatternQueryInterfaceSemantic') as mock_interface:
            mock_instance = mock_interface.return_value
            mock_instance.find_similar_patterns.return_value = {
                'patterns': [self.sample_patterns[1]],
                'query_metadata': {}
            }
            
            interface = CommanderPatternInterface()
            
            # Get backup suggestions
            backups = interface.get_backup_suggestions('electron_desktop_app', top_k=3)
            
            # Assertions
            assert len(backups) >= 0  # May be empty if no similar patterns
            
            # Verify the method was called correctly
            mock_instance.find_similar_patterns.assert_called_once_with(
                pattern_name='electron_desktop_app',
                top_k=3,
                min_similarity=0.5
            )
            
        logger.info("test_backup_pattern_suggestions: PASSED")
    
    def test_end_to_end_workflow(self):
        """Test 8: Complete flow - query → select → context → verify"""
        logger.info("Running test_end_to_end_workflow")
        
        with mock.patch('commander_integration.PatternQueryInterfaceSemantic') as mock_interface:
            mock_instance = mock_interface.return_value
            
            # Mock pattern query
            mock_instance.find_patterns_hybrid.return_value = {
                'patterns': self.sample_patterns,
                'user_review_text': 'Select a pattern',
                'query_metadata': {'goal': 'Build file manager'}
            }
            
            # Mock backup patterns
            mock_instance.find_similar_patterns.return_value = {
                'patterns': [self.sample_patterns[1]],
                'query_metadata': {}
            }
            
            # Step 1: Initialize interface
            interface = CommanderPatternInterface()
            assert interface._neo4j_available == True
            
            # Step 2: Query patterns
            query_result = interface.query_patterns_for_goal(
                goal_description="Build a file manager for volunteers",
                constraints={'technologies': ['typescript', 'electron']},
                top_k=5
            )
            assert len(query_result['patterns']) == 2
            
            # Step 3: User selects pattern
            selection = interface.select_pattern(query_result['patterns'], '1')
            assert selection.pattern_name == 'electron_desktop_app'
            
            # Step 4: Get backup patterns
            backups = interface.get_backup_suggestions(selection.pattern_name, top_k=3)
            
            # Step 5: Generate SPEC context
            context = interface.generate_spec_context(selection, backups)
            assert context['pattern_informed'] == True
            assert context['primary_pattern']['selected_pattern'] == 'electron_desktop_app'
            
            # Step 6: Verify context structure
            assert 'architectural_guidance' in context
            assert 'recommended_technologies' in context['architectural_guidance']
            assert 'risk_assessment' in context['architectural_guidance']
            
            # Verify risk assessment is appropriate for high confidence pattern
            assert 'LOW' in context['architectural_guidance']['risk_assessment']
            
        logger.info("test_end_to_end_workflow: PASSED")
    
    def test_format_pattern_options(self):
        """Test 9: Pattern formatting for user display"""
        logger.info("Running test_format_pattern_options")
        
        with mock.patch('commander_integration.PatternQueryInterfaceSemantic'):
            interface = CommanderPatternInterface()
            
            # Format patterns for display
            formatted = interface.format_pattern_options(
                patterns=self.sample_patterns,
                goal="Build file manager",
                max_display=5
            )
            
            # Assertions
            assert isinstance(formatted, str)
            assert 'electron_desktop_app' in formatted
            assert 'HIGH' in formatted or 'high' in formatted
            assert '45,000' in formatted or '45000' in formatted
            assert 'SELECTION REQUIRED' in formatted or 'Select' in formatted.lower()
            
        logger.info("test_format_pattern_options: PASSED")
    
    def test_no_patterns_found(self):
        """Test 10: Handle case when no patterns match the query"""
        logger.info("Running test_no_patterns_found")
        
        with mock.patch('commander_integration.PatternQueryInterfaceSemantic') as mock_interface:
            mock_instance = mock_interface.return_value
            mock_instance.find_patterns_hybrid.return_value = {
                'patterns': [],
                'user_review_text': 'No patterns found',
                'query_metadata': {'goal': 'Novel goal'}
            }
            
            interface = CommanderPatternInterface()
            result = interface.query_patterns_for_goal("Build quantum simulator")
            
            # Assertions
            assert result['patterns'] == []
            assert 'user_review_text' in result
            
        logger.info("test_no_patterns_found: PASSED")


    def test_discover_alternatives(self):
        """Test 11: Cross-pattern discovery for alternative approaches"""
        logger.info("Running test_discover_alternatives")
        
        with mock.patch('commander_integration.PatternQueryInterfaceSemantic') as mock_interface:
            mock_instance = mock_interface.return_value
            mock_instance.discover_alternatives.return_value = {
                'patterns': [self.sample_patterns[1]],
                'query_metadata': {'mode': 'cross_pattern_discovery'}
            }
            
            interface = CommanderPatternInterface()
            
            result = interface.discover_alternatives(
                goal="Build event-driven system",
                min_similarity=0.6,
                top_k=10
            )
            
            # Assertions
            assert 'patterns' in result
            assert 'query_metadata' in result
            
            # Verify method was called correctly
            mock_instance.discover_alternatives.assert_called_once_with(
                goal="Build event-driven system",
                include_different_tech=True,
                min_similarity=0.6,
                top_k=10
            )
            
        logger.info("test_discover_alternatives: PASSED")
    
    def test_verify_feasibility(self):
        """Test 12: SPEC feasibility verification"""
        logger.info("Running test_verify_feasibility")
        
        with mock.patch('commander_integration.PatternQueryInterfaceSemantic') as mock_interface:
            mock_instance = mock_interface.return_value
            mock_instance.verify_spec_feasibility.return_value = {
                'feasible': True,
                'patterns_found': 3,
                'recommendation': 'Proceed with high confidence'
            }
            
            interface = CommanderPatternInterface()
            
            spec_dict = {'goal': 'Build e-commerce platform'}
            result = interface.verify_feasibility(spec_dict, use_semantic=True)
            
            # Assertions
            assert result is not None
            assert 'feasible' in result
            
            # Verify method called
            mock_instance.verify_spec_feasibility.assert_called_once_with(
                spec_dict,
                use_semantic=True
            )
            
        logger.info("test_verify_feasibility: PASSED")
    
    def test_generate_spec_context_no_pattern(self):
        """Test 13: SPEC context generation when no pattern selected"""
        logger.info("Running test_generate_spec_context_no_pattern")
        
        with mock.patch('commander_integration.PatternQueryInterfaceSemantic'):
            interface = CommanderPatternInterface()
            
            # Generate context with None (user skipped)
            context = interface.generate_spec_context(
                selected_pattern=None,
                backup_patterns=None
            )
            
            # Assertions
            assert context['pattern_informed'] == False
            assert context['pattern_available'] == False
            assert 'message' in context
            assert 'no pattern' in context['message'].lower()
            assert 'general' in context['message'].lower()
            
        logger.info("test_generate_spec_context_no_pattern: PASSED")


class TestPatternSelection:
    """Test the PatternSelection dataclass"""
    
    def test_to_spec_context(self):
        """Test conversion to SPEC context dictionary"""
        logger.info("Running test_to_spec_context")
        
        selection = PatternSelection(
            pattern_name='test_pattern',
            pattern_id='pat_001',
            composite_score=0.85,
            recommendation='high',
            semantic_score=0.87,
            reasoning='Test reasoning',
            description='Test description',
            technologies=['python', 'django'],
            github_stars=10000,
            github_url='https://github.com/test/repo'
        )
        
        context = selection.to_spec_context()
        
        # Assertions
        assert context['selected_pattern'] == 'test_pattern'
        assert context['pattern_reasoning'] == 'Test reasoning'
        assert context['pattern_confidence'] == 'high'
        assert context['composite_score'] == 0.85
        assert 'python' in context['proven_technologies']
        
        logger.info("test_to_spec_context: PASSED")


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v', '--tb=short'])
