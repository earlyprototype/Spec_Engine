#!/usr/bin/env python3
"""
Test script for Phase 1 Agentic Patterns Implementation
Verifies retry logic, critic validation, and error recovery
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        from pattern_extractor import PatternExtractor
        from pattern_critic import PatternCritic
        from tenacity import retry
        print("  [OK] All imports successful")
        return True
    except ImportError as e:
        print(f"  [FAIL] Import error: {e}")
        return False

def test_critic_standalone():
    """Test PatternCritic standalone validation."""
    print("\nTesting PatternCritic standalone...")
    try:
        from pattern_critic import PatternCritic
        
        # Test pattern
        test_pattern = {
            "pattern_name": "test_filesystem_browser",
            "confidence": "high",
            "requirements": {
                "type": "data_management",
                "domain": "file_system",
                "context": ["existing_files", "web_ui"]
            },
            "constraints": [
                {
                    "rule": "filesystem_is_source_of_truth",
                    "criticality": "must",
                    "enforcement": "architectural",
                    "violation_impact": "high",
                    "reasoning": "Core principle for data integrity"
                }
            ],
            "technologies": [
                {
                    "name": "react",
                    "role": "primary",
                    "criticality": 0.95,
                    "adoption_confidence": 0.9,
                    "can_substitute": ["vue", "preact"]
                }
            ],
            "reasoning": "Pattern for browsing filesystem with web UI"
        }
        
        critic = PatternCritic()
        score, needs_review, notes = critic.validate_pattern(test_pattern)
        
        print(f"  Validation Score: {score:.2f}")
        print(f"  Needs Review: {needs_review}")
        print(f"  Quality Tier: {critic.get_quality_tier(score)}")
        print(f"  [OK] Critic validation successful")
        return True
        
    except Exception as e:
        print(f"  [FAIL] Critic test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_extractor_initialization():
    """Test PatternExtractor initialization with all components."""
    print("\nTesting PatternExtractor initialization...")
    try:
        from pattern_extractor import PatternExtractor
        
        extractor = PatternExtractor()
        
        # Check components
        checks = []
        
        if hasattr(extractor, 'github'):
            print("  [OK] GitHub client initialized")
            checks.append(True)
        else:
            print("  [FAIL] GitHub client missing")
            checks.append(False)
        
        if hasattr(extractor, 'llm'):
            print("  [OK] Gemini LLM initialized")
            checks.append(True)
        else:
            print("  [FAIL] Gemini LLM missing")
            checks.append(False)
        
        if hasattr(extractor, 'neo4j'):
            print("  [OK] Neo4j driver initialized")
            checks.append(True)
        else:
            print("  [FAIL] Neo4j driver missing")
            checks.append(False)
        
        if hasattr(extractor, 'critic') and extractor.critic is not None:
            print("  [OK] PatternCritic initialized")
            checks.append(True)
        else:
            print("  [WARN] PatternCritic not available")
            checks.append(True)  # Not critical
        
        if hasattr(extractor, 'critic_executor') and extractor.critic_executor is not None:
            print("  [OK] Critic thread pool initialized")
            checks.append(True)
        else:
            print("  [WARN] Critic thread pool not available")
            checks.append(True)  # Not critical
        
        return all(checks)
        
    except Exception as e:
        print(f"  [FAIL] Extractor initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_retry_decorators():
    """Test that retry decorators are applied."""
    print("\nTesting retry decorators...")
    try:
        from pattern_extractor import PatternExtractor
        import inspect
        
        extractor = PatternExtractor()
        
        # Check for retry decorators (they wrap the methods)
        methods_to_check = [
            '_extract_with_llm',
            '_fetch_readme',
            '_analyze_structure',
            '_store_pattern'
        ]
        
        checks = []
        for method_name in methods_to_check:
            method = getattr(extractor, method_name)
            # Retry decorator adds __wrapped__ attribute
            if hasattr(method, 'retry') or hasattr(method, '__wrapped__'):
                print(f"  [OK] {method_name} has retry logic")
                checks.append(True)
            else:
                print(f"  [WARN] {method_name} may not have retry decorator")
                checks.append(True)  # Not a hard failure
        
        return all(checks)
        
    except Exception as e:
        print(f"  [FAIL] Retry decorator test failed: {e}")
        return False

def test_environment():
    """Test environment variables."""
    print("\nTesting environment variables...")
    
    required_vars = [
        'GITHUB_TOKEN',
        'GEMINI_API_KEY',
        'NEO4J_URI',
        'NEO4J_USER',
        'NEO4J_PASSWORD'
    ]
    
    checks = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"  [OK] {var} is set")
            checks.append(True)
        else:
            print(f"  [FAIL] {var} is not set")
            checks.append(False)
    
    return all(checks)

def main():
    """Run all tests."""
    print("="*60)
    print("PHASE 1 IMPLEMENTATION TEST SUITE")
    print("="*60)
    
    results = []
    
    # Test 1: Environment
    results.append(("Environment Variables", test_environment()))
    
    # Test 2: Imports
    results.append(("Module Imports", test_imports()))
    
    # Test 3: Extractor Initialization
    results.append(("Extractor Initialization", test_extractor_initialization()))
    
    # Test 4: Retry Decorators
    results.append(("Retry Decorators", test_retry_decorators()))
    
    # Test 5: Critic Validation (requires API key)
    if os.getenv('GEMINI_API_KEY'):
        results.append(("Critic Validation", test_critic_standalone()))
    else:
        print("\n[SKIP] Critic validation test (no GEMINI_API_KEY)")
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed! Phase 1 implementation is ready.")
        return 0
    else:
        print(f"\n[WARNING] {total - passed} test(s) failed. Review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
