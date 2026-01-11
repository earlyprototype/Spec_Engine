# test_query.py
# Test querying the pattern graph

from query_patterns import PatternQuery

def test_dashboard_query():
    """Test querying for Dashboard SPEC requirements."""
    
    query = PatternQuery()
    
    # Dashboard SPEC requirements
    print("\n=== Testing Dashboard Requirements Query ===")
    dashboard_requirements = {
        'type': 'data_management',
        'domain': 'file_system',
        'context': ['existing_files', 'web_ui']
    }
    
    print("Requirements:")
    print(f"  Type: {dashboard_requirements['type']}")
    print(f"  Domain: {dashboard_requirements['domain']}")
    print(f"  Context: {dashboard_requirements['context']}")
    
    results = query.recommend_pattern(dashboard_requirements)
    
    print(f"\n✓ Found {len(results)} recommendations")
    
    if results:
        print("\nRecommendations:")
        for i, r in enumerate(results, 1):
            print(f"\n{i}. {r['pattern']} (confidence: {r['confidence']})")
            print(f"   Stars: {r['stars']}")
            print(f"   Source: {r['source']}")
            print(f"   Constraints: {r['constraints']}")
            print(f"   Technologies: {r['technologies']}")
        
        # Expected result
        print("\n--- Expected Result ---")
        print("✓ Should recommend: filesystem_browser pattern")
        print("✓ Should have constraint: filesystem_is_source_of_truth")
        print("✓ Should flag if database is primary storage")
    else:
        print("\n⚠ No patterns found. Graph may be empty.")
        print("Run test_extraction.py first to populate the graph.")

def test_technology_search():
    """Test searching patterns by technology."""
    
    query = PatternQuery()
    
    print("\n=== Testing Technology Search ===")
    tech = "react"
    print(f"Searching for patterns using: {tech}")
    
    results = query.search_by_technology(tech)
    
    print(f"\n✓ Found {len(results)} patterns using {tech}")
    
    for i, r in enumerate(results, 1):
        print(f"\n{i}. {r['pattern']}")
        print(f"   Stars: {r['stars']}")
        print(f"   Requirement: {r['requirement_type']} / {r['requirement_domain']}")
        print(f"   Source: {r['source']}")

def test_pattern_details():
    """Test getting detailed information about a specific pattern."""
    
    query = PatternQuery()
    
    print("\n=== Testing Pattern Details Query ===")
    
    # First, get recommendations to find a pattern name
    dashboard_requirements = {
        'type': 'data_management',
        'domain': 'file_system',
        'context': ['existing_files', 'web_ui']
    }
    
    results = query.recommend_pattern(dashboard_requirements)
    
    if not results:
        print("⚠ No patterns in graph. Run test_extraction.py first.")
        return
    
    # Get details of first pattern
    pattern_name = results[0]['pattern']
    print(f"Getting details for: {pattern_name}")
    
    details = query.get_pattern_details(pattern_name)
    
    if details:
        print(f"\nPattern: {details['pattern']}")
        print(f"Confidence: {details['confidence']}")
        print(f"Stars: {details['stars']}")
        print(f"Source: {details['source']}")
        print(f"Requirement: {details['requirement_type']} / {details['requirement_domain']}")
        print(f"Constraints: {details['constraints']}")
        print(f"Technologies: {details['technologies']}")
        print(f"\nReasoning: {details['reasoning']}")

def test_statistics():
    """Test getting graph statistics."""
    
    query = PatternQuery()
    
    print("\n=== Graph Statistics ===")
    
    stats = query.get_statistics()
    
    print(f"Patterns: {stats.get('pattern_count', 0)}")
    print(f"Requirements: {stats.get('requirement_count', 0)}")
    print(f"Technologies: {stats.get('tech_count', 0)}")
    print(f"Constraints: {stats.get('constraint_count', 0)}")
    
    if stats.get('pattern_count', 0) == 0:
        print("\n⚠ Graph is empty. Run test_extraction.py first.")
    else:
        print("\n✓ Graph is populated and ready for queries")

if __name__ == "__main__":
    import sys
    
    print("Choose test:")
    print("1. Dashboard requirements query (validates divergence detection)")
    print("2. Technology search (find patterns using specific tech)")
    print("3. Pattern details (get full information about a pattern)")
    print("4. Graph statistics (check graph health)")
    print("5. Run all tests")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == "1":
        test_dashboard_query()
    elif choice == "2":
        test_technology_search()
    elif choice == "3":
        test_pattern_details()
    elif choice == "4":
        test_statistics()
    elif choice == "5":
        print("\n=== Running All Tests ===")
        test_statistics()
        test_dashboard_query()
        test_technology_search()
        test_pattern_details()
    else:
        print("Invalid choice. Running Dashboard query test...")
        test_dashboard_query()
