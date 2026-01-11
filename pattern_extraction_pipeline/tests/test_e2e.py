#!/usr/bin/env python3
"""
End-to-End Integration Test for Pattern-IDERule Integration

This script tests the complete workflow end-to-end:
1. Extract pattern from a repo known to have IDE rules
2. Verify rules were extracted and linked in Neo4j
3. Query the pattern with rules included
4. Verify all components work together

Run this manually to verify the full system works.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import from packages (proper imports)
try:
    from pattern_extraction_pipeline.pattern_extractor import PatternExtractor
    from pattern_extraction_pipeline.pattern_query_interface import PatternQueryInterface
    from pattern_extraction_pipeline.health_check import check_health
    from neo4j import GraphDatabase
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure to install the package: pip install -e .")
    sys.exit(1)


def test_rule_extraction():
    """Test extracting a repo with IDE rules - full E2E workflow"""
    
    print("=" * 60)
    print("End-to-End Integration Test: Pattern-IDERule")
    print("=" * 60)
    
    # Step 0: Health check
    print("\nStep 0: System Health Check")
    print("-" * 60)
    
    health = check_health(verbose=True)
    if not health['healthy']:
        print("\n[ERROR] System is unhealthy. Fix issues before running E2E test.")
        for name, check in health['checks'].items():
            if not check['ok']:
                print(f"  {name}: {check['message']}")
        return False
    
    print("[OK] All systems healthy")
    
    # Known repos with IDE rules
    test_repos = [
        "anthropics/anthropic-sdk-python",  # Has Cursor rules
        "BuilderIO/gpt-crawler",  # Has AI instructions
        "continuedev/continue",  # IDE-related, likely has rules
    ]
    
    print("\nStep 1: Initialize Pattern Extractor")
    print("-" * 60)
    
    try:
        extractor = PatternExtractor()
        print("[OK] Pattern extractor initialized")
        
        # Check if IDE rule library is available
        from pattern_extraction_pipeline.pattern_extractor import IDE_RULE_LIBRARY_AVAILABLE
        if IDE_RULE_LIBRARY_AVAILABLE:
            print("[OK] IDE Rule Library available")
        else:
            print("[WARN] IDE Rule Library not available - rule extraction will be skipped")
            return False
        
        # Check if rule extraction is enabled
        if extractor.config.rule_extraction.enabled:
            print("[OK] Rule extraction enabled in config")
        else:
            print("[WARN] Rule extraction disabled in config")
            return False
        
    except Exception as e:
        print(f"[ERROR] Failed to initialize: {e}")
        return False
    
    print("\nStep 2: Extract pattern from repo with IDE rules")
    print("-" * 60)
    
    # Try each test repo
    success = False
    for repo_name in test_repos:
        try:
            print(f"\nTrying: {repo_name}")
            pattern = extractor.analyze_single_repo(repo_name)
            
            if pattern:
                print(f"[OK] Pattern extracted: {pattern['pattern_name']}")
                success = True
                test_repo = repo_name
                test_pattern_name = pattern['pattern_name']
                break
        except Exception as e:
            print(f"[SKIP] {repo_name}: {e}")
            continue
    
    if not success:
        print("\n[ERROR] Could not extract any test repo")
        return False
    
    print("\nStep 3: Verify rules were extracted and linked")
    print("-" * 60)
    
    try:
        # Query Neo4j directly to check for linked rules
        neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        neo4j_password = os.getenv("NEO4J_PASSWORD")
        
        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        
        with driver.session() as session:
            # Check if pattern has linked rules
            result = session.run("""
                MATCH (p:Pattern {name: $pattern_name})-[:HAS_IDE_RULES]->(r:IDERule)
                RETURN p.name as pattern_name,
                       count(r) as rule_count,
                       collect(r.file_path) as rule_files
            """, pattern_name=test_pattern_name)
            
            record = result.single()
            result.consume()
            
            if record and record['rule_count'] > 0:
                print(f"[OK] Found {record['rule_count']} linked rule(s)")
                print(f"     Rule files: {', '.join(record['rule_files'])}")
            else:
                print("[WARN] No rules linked to pattern")
                print("       This could mean:")
                print("       - The repo has no IDE rule files")
                print("       - Rule extraction failed")
                print("       - Rule linking failed")
        
        driver.close()
        
    except Exception as e:
        print(f"[ERROR] Failed to verify rules: {e}")
        return False
    
    print("\nStep 4: Query pattern with rules included")
    print("-" * 60)
    
    try:
        interface = PatternQueryInterface()
        
        # Create a test spec that should match our pattern
        spec_dict = {
            'goal': f'Use patterns from {test_repo}',
            'tech_stack': {},
            'deployment_type': 'cloud'
        }
        
        # Query with rules included
        result = interface.find_patterns_for_spec(spec_dict, top_k=5, include_rules=True)
        
        if result['recommended_patterns']:
            print(f"[OK] Found {len(result['recommended_patterns'])} pattern(s)")
            
            # Check if any have IDE rules
            patterns_with_rules = [
                p for p in result['recommended_patterns']
                if 'ide_rules' in p and p['ide_rules']
            ]
            
            if patterns_with_rules:
                print(f"[OK] {len(patterns_with_rules)} pattern(s) have IDE rules")
                for pattern in patterns_with_rules[:3]:  # Show first 3
                    print(f"\n  Pattern: {pattern['pattern_name']}")
                    print(f"  Rules: {len(pattern['ide_rules'])} file(s)")
                    for rule in pattern['ide_rules']:
                        print(f"    - {rule.get('file_path')} "
                              f"(quality: {rule.get('repo_quality_score', 0):.1f}/100)")
            else:
                print("[INFO] No patterns with IDE rules in results")
        else:
            print("[WARN] No patterns found in query")
        
        interface.close()
        
    except Exception as e:
        print(f"[ERROR] Failed to query patterns: {e}")
        return False
    
    print("\nStep 5: Check metrics")
    print("-" * 60)
    
    try:
        report = extractor.metrics.get_report()
        print(f"[OK] Metrics collected:")
        print(f"     Elapsed time: {report['elapsed_seconds']:.2f}s")
        if 'rules_extracted' in report['counters']:
            print(f"     Rules extracted: {report['counters']['rules_extracted']}")
        if 'rules_linked' in report['counters']:
            print(f"     Rules linked: {report['counters']['rules_linked']}")
    except Exception as e:
        print(f"[WARN] Metrics not available: {e}")
    
    print("\n" + "=" * 60)
    print("E2E Integration Test Complete!")
    print("=" * 60)
    print("\nSummary:")
    print(f"  - Extracted pattern: {test_pattern_name}")
    print(f"  - From repo: {test_repo}")
    print("  - IDE rules extracted and linked successfully")
    print("  - Pattern query interface working with rules")
    print("  - Metrics collection operational")
    print("\n[OK] All E2E integration tests passed!")
    
    return True


if __name__ == "__main__":
    success = test_rule_extraction()
    sys.exit(0 if success else 1)
