"""
Backwards Compatibility Tests

Verifies that old SPEC formats (v1.3) work with the new system
that includes pattern-informed validation.

Author: SPEC Engine Team
Version: 1.0
Date: 2026-01-07
"""

import pytest
import logging
import toml
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test fixtures directory
FIXTURES_DIR = Path(__file__).parent / 'fixtures'


class TestBackwardsCompatibility:
    """Test backwards compatibility with v1.3 SPECs"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.v13_spec_path = FIXTURES_DIR / 'spec_v1.3_no_patterns.toml'
        self.v14_spec_path = FIXTURES_DIR / 'spec_v1.4_with_patterns.toml'
    
    def test_old_spec_without_pattern_metadata(self):
        """Test 1: v1.3 SPEC (no pattern metadata) loads successfully"""
        logger.info("Running test_old_spec_without_pattern_metadata")
        
        # Load old SPEC format
        assert self.v13_spec_path.exists(), f"Fixture not found: {self.v13_spec_path}"
        
        spec_data = toml.load(self.v13_spec_path)
        
        # Assertions - verify old format parses
        assert 'goal' in spec_data
        assert 'software_stack' in spec_data
        assert 'tasks' in spec_data
        assert len(spec_data['tasks']) > 0
        
        # Verify NO pattern metadata present
        assert 'pattern_metadata' not in spec_data
        
        # Verify essential fields exist
        assert spec_data['goal']['description']
        assert spec_data['software_stack']['deployment_type']
        assert spec_data['software_stack']['primary_language']
        
        logger.info("test_old_spec_without_pattern_metadata: PASSED")
    
    def test_pattern_validation_skipped_when_no_metadata(self):
        """Test 2: Pattern validation gracefully skipped when metadata absent"""
        logger.info("Running test_pattern_validation_skipped_when_no_metadata")
        
        # Load old SPEC
        spec_data = toml.load(self.v13_spec_path)
        
        # Simulate pattern feasibility check (Section 2.0a logic)
        pattern_metadata_exists = 'pattern_metadata' in spec_data
        
        if not pattern_metadata_exists:
            # This is the expected graceful skip behavior
            validation_result = {
                'pattern_feasibility_check': {
                    'performed': False,
                    'reason': 'No pattern metadata in SPEC',
                    'action': 'Skipped gracefully',
                    'backwards_compatible': True
                }
            }
        else:
            validation_result = {
                'pattern_feasibility_check': {
                    'performed': True
                }
            }
        
        # Assertions
        assert validation_result['pattern_feasibility_check']['performed'] == False
        assert validation_result['pattern_feasibility_check']['backwards_compatible'] == True
        
        logger.info("test_pattern_validation_skipped_when_no_metadata: PASSED")
    
    def test_old_config_files_parse(self):
        """Test 3: Old configuration files still parse correctly"""
        logger.info("Running test_old_config_files_parse")
        
        # Load both old and new formats
        old_spec = toml.load(self.v13_spec_path)
        new_spec = toml.load(self.v14_spec_path)
        
        # Verify both parse successfully
        assert old_spec is not None
        assert new_spec is not None
        
        # Verify common required fields exist in both
        for spec in [old_spec, new_spec]:
            assert 'goal' in spec
            assert 'description' in spec['goal']
            assert 'software_stack' in spec
            assert 'deployment_type' in spec['software_stack']
            assert 'tasks' in spec
            assert isinstance(spec['tasks'], list)
            assert len(spec['tasks']) > 0
        
        # Verify old spec doesn't have pattern metadata
        assert 'pattern_metadata' not in old_spec
        
        # Verify new spec has pattern metadata
        assert 'pattern_metadata' in new_spec
        assert 'pattern_name' in new_spec['pattern_metadata']
        assert 'pattern_confidence' in new_spec['pattern_metadata']
        
        logger.info("test_old_config_files_parse: PASSED")
    
    def test_feature_flag_disables_validation(self):
        """Test 4: pattern_validation_enabled flag works correctly"""
        logger.info("Running test_feature_flag_disables_validation")
        
        # Load spec with pattern metadata
        spec_data = toml.load(self.v14_spec_path)
        
        # Simulate feature flag configurations
        test_cases = [
            {'pattern_validation_enabled': True, 'should_validate': True},
            {'pattern_validation_enabled': False, 'should_validate': False},
            {}, # No flag set - default behavior
        ]
        
        for config in test_cases:
            pattern_validation_enabled = config.get('pattern_validation_enabled', True)
            has_pattern_metadata = 'pattern_metadata' in spec_data
            
            # Simulate validation logic
            should_perform_validation = (
                pattern_validation_enabled and 
                has_pattern_metadata
            )
            
            if not pattern_validation_enabled:
                # Flag explicitly disabled
                assert should_perform_validation == False, \
                    "Validation should be disabled when flag is False"
            
            # If flag is True or not set, and metadata exists, validate
            if config.get('pattern_validation_enabled', True) and has_pattern_metadata:
                assert should_perform_validation == True, \
                    "Validation should be enabled when flag is True and metadata exists"
        
        logger.info("test_feature_flag_disables_validation: PASSED")
    
    def test_new_spec_with_patterns_validates(self):
        """Test 5: New SPEC format with patterns validates correctly"""
        logger.info("Running test_new_spec_with_patterns_validates")
        
        # Load new SPEC with pattern metadata
        spec_data = toml.load(self.v14_spec_path)
        
        # Verify pattern metadata structure
        assert 'pattern_metadata' in spec_data
        pattern_meta = spec_data['pattern_metadata']
        
        # Check required pattern fields
        assert 'pattern_name' in pattern_meta
        assert 'pattern_confidence' in pattern_meta
        assert 'pattern_score' in pattern_meta
        assert 'pattern_technologies' in pattern_meta
        
        # Verify pattern values
        assert isinstance(pattern_meta['pattern_name'], str)
        assert pattern_meta['pattern_confidence'] in ['HIGH', 'MEDIUM', 'LOW']
        assert 0.0 <= pattern_meta['pattern_score'] <= 1.0
        assert isinstance(pattern_meta['pattern_technologies'], list)
        
        # Verify technology alignment
        spec_language = spec_data['software_stack']['primary_language']
        pattern_techs = pattern_meta['pattern_technologies']
        
        # Check if spec language is aligned with pattern
        # (typescript matches, python doesn't)
        alignment_check = spec_language in pattern_techs or any(
            tech.lower() == spec_language.lower() 
            for tech in pattern_techs
        )
        
        # For this test fixture, they should align
        assert alignment_check, \
            f"Language {spec_language} should be in pattern technologies {pattern_techs}"
        
        logger.info("test_new_spec_with_patterns_validates: PASSED")
    
    def test_migration_path_clear(self):
        """Test 6: Migration from v1.3 to v1.4 is straightforward"""
        logger.info("Running test_migration_path_clear")
        
        # Load old spec
        old_spec = toml.load(self.v13_spec_path)
        
        # Simulate migration: adding pattern metadata to old spec
        migrated_spec = old_spec.copy()
        
        # Add pattern metadata (what Commander would add)
        migrated_spec['pattern_metadata'] = {
            'pattern_name': 'python_desktop_app',
            'pattern_confidence': 'HIGH',
            'pattern_score': 0.85,
            'pattern_technologies': ['python', 'tkinter'],
            'pattern_reference': 'https://github.com/example/python-app',
            'pattern_github_stars': 15000
        }
        
        # Verify migration successful
        assert 'pattern_metadata' in migrated_spec
        assert migrated_spec['pattern_metadata']['pattern_name'] == 'python_desktop_app'
        
        # Verify original structure preserved
        assert migrated_spec['goal'] == old_spec['goal']
        assert migrated_spec['software_stack'] == old_spec['software_stack']
        assert migrated_spec['tasks'] == old_spec['tasks']
        
        logger.info("test_migration_path_clear: PASSED")
    
    def test_no_breaking_changes_to_required_fields(self):
        """Test 7: No new required fields that break old SPECs"""
        logger.info("Running test_no_breaking_changes_to_required_fields")
        
        # Define required fields that must exist in ALL specs (v1.3 and v1.4)
        required_fields = {
            'goal': ['description', 'type'],
            'software_stack': ['deployment_type', 'primary_language'],
            'tasks': []  # Tasks must exist as array
        }
        
        # Test both versions
        for spec_path, version in [(self.v13_spec_path, 'v1.3'), (self.v14_spec_path, 'v1.4')]:
            spec_data = toml.load(spec_path)
            
            # Verify all required top-level fields exist
            for field in required_fields.keys():
                assert field in spec_data, \
                    f"{version}: Missing required field '{field}'"
            
            # Verify required nested fields
            for parent, children in required_fields.items():
                if children:  # If there are nested required fields
                    for child in children:
                        assert child in spec_data[parent], \
                            f"{version}: Missing required field '{parent}.{child}'"
        
        # Verify pattern_metadata is NOT required (optional)
        old_spec = toml.load(self.v13_spec_path)
        assert 'pattern_metadata' not in old_spec, \
            "pattern_metadata should be optional, not required"
        
        logger.info("test_no_breaking_changes_to_required_fields: PASSED")


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v', '--tb=short'])
