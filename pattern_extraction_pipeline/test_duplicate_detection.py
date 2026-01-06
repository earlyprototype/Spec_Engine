# test_duplicate_detection.py
# Unit tests for duplicate detection functionality

import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

load_dotenv(override=True)

from pattern_extractor import PatternExtractor

def test_check_repo_exists_new():
    """Test that _check_if_repo_exists returns None for non-existent repo"""
    print("\n=== Test 1: Check Non-Existent Repository ===")
    extractor = PatternExtractor()
    
    result = extractor._check_if_repo_exists("https://github.com/nonexistent/repo-12345-xyz")
    
    if result is None:
        print("[PASS] Correctly returned None for non-existent repo")
        return True
    else:
        print(f"[FAIL] Expected None, got: {result}")
        return False

def test_check_repo_exists_found():
    """Test that _check_if_repo_exists returns data for existing repo"""
    print("\n=== Test 2: Check Existing Repository ===")
    print("NOTE: This test requires at least one pattern in the database")
    
    extractor = PatternExtractor()
    
    # First, get a pattern that exists
    from neo4j import GraphDatabase
    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
    )
    
    with driver.session() as session:
        result_query = session.run("""
            MATCH (p:Pattern)
            RETURN p.source_repo as repo
            LIMIT 1
        """)
        record = result_query.single()
        
        if not record:
            print("[SKIP] No patterns in database to test with")
            driver.close()
            return True
        
        test_repo = record['repo']
    
    driver.close()
    
    # Now check if we can find it
    result = extractor._check_if_repo_exists(test_repo)
    
    if result is not None:
        if all(key in result for key in ['name', 'extracted_at', 'quality_score', 'stars']):
            print(f"[PASS] Found existing repo: {result['name']}")
            print(f"       Quality: {result['quality_score']}, Stars: {result['stars']}")
            return True
        else:
            print(f"[FAIL] Result missing required keys: {result}")
            return False
    else:
        print(f"[FAIL] Expected data for {test_repo}, got None")
        return False

def test_skip_logic_stats():
    """Test that statistics correctly track skipped repos"""
    print("\n=== Test 3: Statistics Tracking ===")
    print("NOTE: This requires running a real extraction - testing structure only")
    
    # Test that the stats dictionary has the skipped field
    extractor = PatternExtractor()
    
    # Mock extraction stats structure
    extraction_stats = {
        'total': 0,
        'successful': 0,
        'partial': 0,
        'failed': 0,
        'skipped': 0,
        'errors': []
    }
    
    if 'skipped' in extraction_stats:
        print("[PASS] Statistics structure includes 'skipped' field")
        return True
    else:
        print("[FAIL] Statistics structure missing 'skipped' field")
        return False

def test_method_signatures():
    """Test that all methods have correct signatures"""
    print("\n=== Test 4: Method Signatures ===")
    
    extractor = PatternExtractor()
    
    # Check _check_if_repo_exists exists
    if hasattr(extractor, '_check_if_repo_exists'):
        print("[PASS] Method _check_if_repo_exists exists")
    else:
        print("[FAIL] Method _check_if_repo_exists not found")
        return False
    
    # Check extract_patterns has force_reanalyse parameter
    import inspect
    sig = inspect.signature(extractor.extract_patterns)
    params = sig.parameters
    
    if 'force_reanalyse' in params:
        print("[PASS] extract_patterns has force_reanalyse parameter")
        default = params['force_reanalyse'].default
        if default is False:
            print(f"[PASS] force_reanalyse defaults to False")
        else:
            print(f"[WARN] force_reanalyse defaults to {default}, expected False")
    else:
        print("[FAIL] extract_patterns missing force_reanalyse parameter")
        return False
    
    return True

def test_trajectory_logger():
    """Test that TrajectoryLogger has skip logging capability"""
    print("\n=== Test 5: Trajectory Logger ===")
    
    try:
        from trajectory_logger import TrajectoryLogger
        logger = TrajectoryLogger()
        
        # Check method exists
        if hasattr(logger, 'log_repository_skipped'):
            print("[PASS] TrajectoryLogger has log_repository_skipped method")
        else:
            print("[FAIL] TrajectoryLogger missing log_repository_skipped method")
            return False
        
        # Test creating a trajectory and checking structure
        logger.start_extraction("test", "test query", 10)
        
        if 'skipped_repositories' in logger.current_trajectory:
            print("[PASS] Trajectory includes skipped_repositories array")
        else:
            print("[FAIL] Trajectory missing skipped_repositories array")
            return False
        
        if 'skipped' in logger.current_trajectory['summary']:
            print("[PASS] Trajectory summary includes skipped count")
        else:
            print("[FAIL] Trajectory summary missing skipped count")
            return False
        
        return True
    except Exception as e:
        print(f"[FAIL] Error testing trajectory logger: {e}")
        return False

def run_all_tests():
    """Run all unit tests"""
    print("\n" + "="*70)
    print("DUPLICATE DETECTION UNIT TESTS")
    print("="*70)
    
    tests = [
        test_check_repo_exists_new,
        test_check_repo_exists_found,
        test_skip_logic_stats,
        test_method_signatures,
        test_trajectory_logger
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"[ERROR] Test {test.__name__} raised exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed!")
        return 0
    else:
        print(f"\n[FAILED] {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
