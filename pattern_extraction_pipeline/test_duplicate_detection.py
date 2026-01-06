# test_duplicate_detection.py
# Unit tests for duplicate detection functionality

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(override=True)

# Test database connection setup
def get_test_db():
    """Get Neo4j connection for testing"""
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7688")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    return GraphDatabase.driver(uri, auth=(user, password), connection_timeout=5.0)

def test_check_repo_exists_query():
    """Test that duplicate check query works correctly"""
    print("\n=== Test 1: Duplicate Check Query ===")
    driver = get_test_db()
    
    try:
        with driver.session() as session:
            # Test with non-existent repo
            result = session.run("""
                MATCH (p:Pattern {source_repo: $repo_url})
                RETURN p.name as name,
                       p.extracted_at as extracted_at,
                       p.quality_score as quality_score,
                       p.stars as stars
                LIMIT 1
            """, repo_url="https://github.com/nonexistent/repo-12345-xyz")
            
            record = result.single()
            
            if record is None:
                print("   [PASS] Correctly returned None for non-existent repo")
                return True
            else:
                print(f"   [FAIL] Expected None, got: {record}")
                return False
    finally:
        driver.close()

def test_check_repo_exists_real():
    """Test duplicate check with real pattern from database"""
    print("\n=== Test 2: Check Existing Repository ===")
    driver = get_test_db()
    
    try:
        with driver.session() as session:
            # Get a real pattern
            result = session.run("""
                MATCH (p:Pattern)
                WHERE p.source_repo IS NOT NULL
                RETURN p.source_repo as repo
                LIMIT 1
            """)
            
            record = result.single()
            if not record:
                print("   [SKIP] No patterns in database to test with")
                return True
            
            test_repo = record['repo']
            print(f"   Testing with: {test_repo}")
            
            # Now check if it exists (should return data)
            result = session.run("""
                MATCH (p:Pattern {source_repo: $repo_url})
                RETURN p.name as name,
                       p.extracted_at as extracted_at,
                       p.quality_score as quality_score,
                       p.stars as stars
                LIMIT 1
            """, repo_url=test_repo)
            
            record = result.single()
            
            if record is not None:
                print(f"   [PASS] Found pattern: {record['name']}")
                return True
            else:
                print("   [FAIL] Should have found existing pattern")
                return False
    finally:
        driver.close()

def test_constraint_exists():
    """Test that uniqueness constraint was created"""
    print("\n=== Test 3: Uniqueness Constraint ===")
    driver = get_test_db()
    
    try:
        with driver.session() as session:
            result = session.run("SHOW CONSTRAINTS")
            constraints = list(result)
            
            pattern_constraint = None
            for c in constraints:
                if 'pattern' in c.get('name', '').lower() and 'source_repo' in str(c):
                    pattern_constraint = c
                    break
            
            if pattern_constraint:
                print(f"   [PASS] Constraint found: {pattern_constraint.get('name', 'unnamed')}")
                return True
            else:
                print("   [FAIL] Pattern.source_repo constraint not found")
                print(f"   Available constraints: {[c.get('name') for c in constraints]}")
                return False
    finally:
        driver.close()

def test_no_duplicates_remain():
    """Test that no duplicate patterns exist after merge"""
    print("\n=== Test 4: No Duplicate Patterns ===")
    driver = get_test_db()
    
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (p:Pattern)
                WITH p.source_repo as repo, count(*) as cnt
                WHERE cnt > 1
                RETURN repo, cnt
            """)
            
            duplicates = list(result)
            
            if len(duplicates) == 0:
                print("   [PASS] No duplicate patterns found")
                return True
            else:
                print(f"   [FAIL] Found {len(duplicates)} duplicate groups:")
                for dup in duplicates[:5]:
                    print(f"     - {dup['repo']}: {dup['cnt']} copies")
                return False
    finally:
        driver.close()

def test_pattern_count():
    """Test pattern count and report statistics"""
    print("\n=== Test 5: Pattern Statistics ===")
    driver = get_test_db()
    
    try:
        with driver.session() as session:
            result = session.run("MATCH (p:Pattern) RETURN count(p) as count")
            count = result.single()['count']
            
            print(f"   Total patterns: {count}")
            
            # Check how many have source_repo
            result = session.run("""
                MATCH (p:Pattern)
                WHERE p.source_repo IS NOT NULL
                RETURN count(p) as count
            """)
            with_repo = result.single()['count']
            
            print(f"   With source_repo: {with_repo}")
            print(f"   [PASS] Database statistics collected")
            return True
    finally:
        driver.close()

def run_all_tests():
    """Run all tests and report results"""
    print("=" * 70)
    print("DUPLICATE DETECTION - UNIT TESTS")
    print("=" * 70)
    
    tests = [
        ("Query for Non-Existent Repo", test_check_repo_exists_query),
        ("Query for Existing Repo", test_check_repo_exists_real),
        ("Uniqueness Constraint", test_constraint_exists),
        ("No Duplicates Remain", test_no_duplicates_remain),
        ("Pattern Statistics", test_pattern_count)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"   [ERROR] {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {name}")
    
    print(f"\nPassed: {passed_count}/{total_count}")
    
    if passed_count == total_count:
        print("\n[SUCCESS] All unit tests passed!")
        return 0
    else:
        print(f"\n[FAILURE] {total_count - passed_count} test(s) failed")
        return 1

if __name__ == "__main__":
    exit(run_all_tests())
