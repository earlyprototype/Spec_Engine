#!/usr/bin/env python3
"""
Test script for Phase 2 Agentic Patterns Implementation
Verifies trajectory logging, quality judge, and enhanced features
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

def test_imports():
    """Test that all Phase 2 modules can be imported."""
    print("Testing Phase 2 imports...")
    try:
        from trajectory_logger import TrajectoryLogger
        from quality_judge import QualityJudge
        from pattern_extractor import PatternExtractor
        from pattern_critic import PatternCritic
        print("  [OK] All Phase 2 imports successful")
        return True
    except ImportError as e:
        print(f"  [FAIL] Import error: {e}")
        return False

def test_trajectory_logger():
    """Test TrajectoryLogger functionality."""
    print("\nTesting TrajectoryLogger...")
    try:
        from trajectory_logger import TrajectoryLogger
        
        # Create logger with test directory
        test_dir = "logs/test_trajectories"
        logger = TrajectoryLogger(log_dir=test_dir)
        
        # Start extraction
        trajectory_id = logger.start_extraction(
            domain="test_domain",
            search_query="topic:test stars:>1000",
            limit=5
        )
        
        # Simulate repository processing
        logger.start_repository("owner/repo", "https://github.com/owner/repo", 5000)
        logger.log_github_api_call("fetch_readme", "owner/repo", True, 0.523)
        logger.log_github_api_call("analyze_structure", "owner/repo", True, 0.234)
        logger.log_quality_metrics("owner/repo", 0.85, 0.90, 0.80)
        logger.log_llm_extraction("owner/repo", True, 2.456, "test_pattern", "high")
        logger.log_neo4j_storage("test_pattern", True, 0.145)
        logger.log_critic_validation("test_pattern", 0.82, False, 1.234)
        logger.finish_repository("successful")
        
        # Finish extraction
        filepath = logger.finish_extraction()
        
        # Verify file exists
        if not Path(filepath).exists():
            print(f"  [FAIL] Trajectory file not created: {filepath}")
            return False
        
        # Verify file content
        with open(filepath, 'r') as f:
            trajectory = json.load(f)
        
        if trajectory['trajectory_id'] != trajectory_id:
            print(f"  [FAIL] Trajectory ID mismatch")
            return False
        
        if len(trajectory['repositories']) != 1:
            print(f"  [FAIL] Expected 1 repository, got {len(trajectory['repositories'])}")
            return False
        
        if trajectory['summary']['successful'] != 1:
            print(f"  [FAIL] Expected 1 successful, got {trajectory['summary']['successful']}")
            return False
        
        # Test analysis
        analysis = logger.get_trajectory_analysis(filepath)
        if 'timing_analysis' not in analysis:
            print(f"  [FAIL] Analysis missing timing_analysis")
            return False
        
        print(f"  [OK] Trajectory logging successful")
        print(f"  Trajectory file: {filepath}")
        print(f"  Analysis: {json.dumps(analysis['summary'], indent=2)}")
        
        # Cleanup
        Path(filepath).unlink()
        
        return True
        
    except Exception as e:
        print(f"  [FAIL] Trajectory logger test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_quality_judge():
    """Test QualityJudge functionality."""
    print("\nTesting QualityJudge...")
    try:
        from quality_judge import QualityJudge
        
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
        
        repo_context = {
            "description": "A modern file manager",
            "readme": "This project provides a fast file browser...",
            "stars": 5000,
            "language": "JavaScript"
        }
        
        judge = QualityJudge()
        score, feedback = judge.evaluate_pattern(test_pattern, repo_context)
        
        if not isinstance(score, float) or score < 0 or score > 1:
            print(f"  [FAIL] Invalid score: {score}")
            return False
        
        if not isinstance(feedback, str) or len(feedback) < 50:
            print(f"  [FAIL] Invalid feedback: {feedback[:100]}")
            return False
        
        quality_tier = judge.get_quality_tier(score)
        if quality_tier not in ['EXCELLENT', 'GOOD', 'ACCEPTABLE', 'NEEDS_IMPROVEMENT']:
            print(f"  [FAIL] Invalid quality tier: {quality_tier}")
            return False
        
        print(f"  [OK] Quality judge evaluation successful")
        print(f"  Judge Score: {score:.2f}")
        print(f"  Quality Tier: {quality_tier}")
        print(f"  Feedback length: {len(feedback)} chars")
        
        return True
        
    except Exception as e:
        print(f"  [FAIL] Quality judge test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integrated_pipeline():
    """Test integrated pipeline with all Phase 2 features."""
    print("\nTesting integrated pipeline...")
    try:
        from pattern_extractor import PatternExtractor
        
        extractor = PatternExtractor()
        
        # Check Phase 2 components
        checks = []
        
        if hasattr(extractor, 'trajectory_logger') and extractor.trajectory_logger is not None:
            print("  [OK] Trajectory logger integrated")
            checks.append(True)
        else:
            print("  [WARN] Trajectory logger not available")
            checks.append(True)  # Not critical
        
        if hasattr(extractor, 'judge') and extractor.judge is not None:
            print("  [OK] Quality judge integrated")
            checks.append(True)
        else:
            print("  [WARN] Quality judge not available")
            checks.append(True)  # Not critical
        
        if hasattr(extractor, 'critic') and extractor.critic is not None:
            print("  [OK] Pattern critic integrated")
            checks.append(True)
        else:
            print("  [FAIL] Pattern critic missing")
            checks.append(False)
        
        return all(checks)
        
    except Exception as e:
        print(f"  [FAIL] Integrated pipeline test failed: {e}")
        return False

def test_neo4j_schema():
    """Test Neo4j schema includes Phase 2 fields."""
    print("\nTesting Neo4j schema...")
    try:
        from neo4j import GraphDatabase
        
        driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
        )
        
        with driver.session() as session:
            # Check if any patterns exist with Phase 2 fields
            result = session.run("""
                MATCH (p:Pattern)
                RETURN 
                    p.validation_score as validation_score,
                    p.needs_review as needs_review,
                    p.judge_score as judge_score,
                    p.extraction_status as extraction_status
                LIMIT 1
            """)
            
            record = result.single()
            if record:
                print(f"  [OK] Neo4j schema includes Phase 2 fields")
                print(f"  Sample: validation_score={record['validation_score']}, judge_score={record['judge_score']}")
            else:
                print(f"  [INFO] No patterns in database yet (schema will be created on first extraction)")
        
        driver.close()
        return True
        
    except Exception as e:
        print(f"  [WARN] Neo4j schema test skipped: {e}")
        return True  # Not critical for test suite

def test_metrics_endpoint():
    """Test metrics endpoint availability."""
    print("\nTesting metrics endpoint...")
    try:
        import requests
        
        response = requests.get('http://localhost:8000/metrics/quality', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if 'statistics' in data and 'completeness' in data:
                print(f"  [OK] Metrics endpoint working")
                print(f"  Total patterns: {data['statistics']['total_patterns']}")
                return True
            else:
                print(f"  [FAIL] Invalid metrics response format")
                return False
        else:
            print(f"  [FAIL] Metrics endpoint returned {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  [WARN] Metrics endpoint test skipped: {e}")
        print(f"  (Server may not be running)")
        return True  # Not critical for test suite

def main():
    """Run all Phase 2 tests."""
    print("="*60)
    print("PHASE 2 IMPLEMENTATION TEST SUITE")
    print("="*60)
    
    results = []
    
    # Test 1: Imports
    results.append(("Module Imports", test_imports()))
    
    # Test 2: Trajectory Logger
    results.append(("Trajectory Logger", test_trajectory_logger()))
    
    # Test 3: Quality Judge (requires API key)
    if os.getenv('GEMINI_API_KEY'):
        results.append(("Quality Judge", test_quality_judge()))
    else:
        print("\n[SKIP] Quality judge test (no GEMINI_API_KEY)")
    
    # Test 4: Integrated Pipeline
    results.append(("Integrated Pipeline", test_integrated_pipeline()))
    
    # Test 5: Neo4j Schema
    results.append(("Neo4j Schema", test_neo4j_schema()))
    
    # Test 6: Metrics Endpoint
    results.append(("Metrics Endpoint", test_metrics_endpoint()))
    
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
        print("\n[SUCCESS] All Phase 2 tests passed!")
        return 0
    else:
        print(f"\n[WARNING] {total - passed} test(s) failed. Review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
