#!/usr/bin/env python3
"""
Resource Cleanup Tests

Tests that PatternExtractor properly cleans up resources (Neo4j driver, executors).
Verifies context manager and close() method work correctly.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from pattern_extraction_pipeline.pattern_extractor import PatternExtractor


class TestResourceCleanup(unittest.TestCase):
    """Test resource cleanup functionality"""
    
    @patch('pattern_extraction_pipeline.pattern_extractor.GraphDatabase')
    @patch('pattern_extraction_pipeline.pattern_extractor.Github')
    def test_close_method_closes_neo4j(self, mock_github, mock_graph_db):
        """Test that close() closes Neo4j driver"""
        mock_driver = Mock()
        mock_graph_db.driver.return_value = mock_driver
        mock_github.return_value = Mock()
        
        extractor = PatternExtractor()
        extractor.close()
        
        # Verify Neo4j driver was closed
        mock_driver.close.assert_called_once()
        # Verify driver is set to None after closing
        self.assertIsNone(extractor.neo4j)
    
    @patch('pattern_extraction_pipeline.pattern_extractor.GraphDatabase')
    @patch('pattern_extraction_pipeline.pattern_extractor.Github')
    def test_close_method_shuts_down_executor(self, mock_github, mock_graph_db):
        """Test that close() shuts down critic executor if it exists"""
        mock_driver = Mock()
        mock_graph_db.driver.return_value = mock_driver
        mock_github.return_value = Mock()
        
        extractor = PatternExtractor()
        
        # Add a mock executor
        mock_executor = Mock()
        extractor.critic_executor = mock_executor
        
        extractor.close()
        
        # Verify executor was shut down
        mock_executor.shutdown.assert_called_once_with(wait=True, cancel_futures=False)
        # Verify executor is set to None
        self.assertIsNone(extractor.critic_executor)
    
    @patch('pattern_extraction_pipeline.pattern_extractor.GraphDatabase')
    @patch('pattern_extraction_pipeline.pattern_extractor.Github')
    def test_context_manager_closes_resources(self, mock_github, mock_graph_db):
        """Test that context manager closes resources on exit"""
        mock_driver = Mock()
        mock_graph_db.driver.return_value = mock_driver
        mock_github.return_value = Mock()
        
        with PatternExtractor() as extractor:
            # Verify extractor is returned
            self.assertIsInstance(extractor, PatternExtractor)
            # Inside context, driver should still be available
            self.assertIsNotNone(extractor.neo4j)
        
        # After exiting context, driver should be closed
        mock_driver.close.assert_called_once()
    
    @patch('pattern_extraction_pipeline.pattern_extractor.GraphDatabase')
    @patch('pattern_extraction_pipeline.pattern_extractor.Github')
    def test_close_handles_missing_driver(self, mock_github, mock_graph_db):
        """Test that close() handles missing driver gracefully"""
        mock_driver = Mock()
        mock_graph_db.driver.return_value = mock_driver
        mock_github.return_value = Mock()
        
        extractor = PatternExtractor()
        extractor.neo4j = None  # Simulate missing driver
        
        # Should not raise
        try:
            extractor.close()
        except Exception as e:
            self.fail(f"close() raised exception with None driver: {e}")
    
    @patch('pattern_extraction_pipeline.pattern_extractor.GraphDatabase')
    @patch('pattern_extraction_pipeline.pattern_extractor.Github')
    def test_close_handles_driver_close_error(self, mock_github, mock_graph_db):
        """Test that close() handles driver.close() errors gracefully"""
        mock_driver = Mock()
        mock_driver.close.side_effect = Exception("Connection already closed")
        mock_graph_db.driver.return_value = mock_driver
        mock_github.return_value = Mock()
        
        extractor = PatternExtractor()
        
        # Should not raise, just log warning
        try:
            extractor.close()
        except Exception as e:
            self.fail(f"close() raised exception when driver.close() fails: {e}")
        
        # Driver should still be set to None
        self.assertIsNone(extractor.neo4j)
    
    @patch('pattern_extraction_pipeline.pattern_extractor.GraphDatabase')
    @patch('pattern_extraction_pipeline.pattern_extractor.Github')
    def test_close_is_idempotent(self, mock_github, mock_graph_db):
        """Test that calling close() multiple times is safe"""
        mock_driver = Mock()
        mock_graph_db.driver.return_value = mock_driver
        mock_github.return_value = Mock()
        
        extractor = PatternExtractor()
        
        # Call close multiple times
        extractor.close()
        extractor.close()
        extractor.close()
        
        # Driver should only be closed once (first call)
        mock_driver.close.assert_called_once()
    
    @patch('pattern_extraction_pipeline.pattern_extractor.GraphDatabase')
    @patch('pattern_extraction_pipeline.pattern_extractor.Github')
    def test_context_manager_propagates_exceptions(self, mock_github, mock_graph_db):
        """Test that context manager doesn't suppress exceptions"""
        mock_driver = Mock()
        mock_graph_db.driver.return_value = mock_driver
        mock_github.return_value = Mock()
        
        with self.assertRaises(ValueError):
            with PatternExtractor() as extractor:
                raise ValueError("Test exception")
        
        # Even with exception, driver should be closed
        mock_driver.close.assert_called_once()


if __name__ == '__main__':
    unittest.main(verbosity=2)
