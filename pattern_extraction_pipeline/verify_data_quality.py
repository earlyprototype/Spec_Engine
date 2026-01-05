# verify_data_quality.py
# Verify data quality in Neo4j graph

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

def verify_data_quality():
    """Verify data quality in Neo4j."""
    
    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
    )
    
    with driver.session() as session:
        print("\n=== Data Quality Verification ===\n")
        
        # Check 1: Duplicate Technologies
        print("Check 1: Duplicate Technology Names (case-insensitive)")
        result = session.run("""
            MATCH (t:Technology)
            WITH toLower(t.name) AS normalized_name, collect(t.name) AS names
            WHERE size(names) > 1
            RETURN normalized_name, names, size(names) AS count
        """)
        
        duplicates = list(result)
        if duplicates:
            print(f"  [X] FAILED: Found {len(duplicates)} duplicate groups")
            for dup in duplicates:
                print(f"      - {dup['names']} ({dup['count']} nodes)")
        else:
            print("  [OK] PASSED: No duplicate technology names")
        
        # Check 2: Technology Name Format
        print("\nCheck 2: Technology Names Are Lowercase")
        result = session.run("""
            MATCH (t:Technology)
            WHERE t.name <> toLower(t.name)
            RETURN t.name AS incorrect_name
            LIMIT 10
        """)
        
        incorrect = list(result)
        if incorrect:
            print(f"  [X] FAILED: Found {len(incorrect)} non-lowercase names")
            for inc in incorrect:
                print(f"      - {inc['incorrect_name']}")
        else:
            print("  [OK] PASSED: All technology names are lowercase")
        
        # Check 3: Duplicate Constraints
        print("\nCheck 3: Duplicate Constraint Rules (case-insensitive)")
        result = session.run("""
            MATCH (c:Constraint)
            WITH toLower(c.rule) AS normalized_rule, collect(c.rule) AS rules
            WHERE size(rules) > 1
            RETURN normalized_rule, rules, size(rules) AS count
        """)
        
        duplicates = list(result)
        if duplicates:
            print(f"  [X] FAILED: Found {len(duplicates)} duplicate groups")
            for dup in duplicates:
                print(f"      - {dup['rules']} ({dup['count']} nodes)")
        else:
            print("  [OK] PASSED: No duplicate constraint rules")
        
        # Check 4: Constraint Rule Format
        print("\nCheck 4: Constraint Rules Are Lowercase Snake Case")
        result = session.run("""
            MATCH (c:Constraint)
            WHERE c.rule <> toLower(replace(c.rule, ' ', '_'))
            RETURN c.rule AS incorrect_rule
            LIMIT 10
        """)
        
        incorrect = list(result)
        if incorrect:
            print(f"  [X] FAILED: Found {len(incorrect)} incorrectly formatted rules")
            for inc in incorrect:
                print(f"      - {inc['incorrect_rule']}")
        else:
            print("  [OK] PASSED: All constraint rules are lowercase_snake_case")
        
        # Check 5: Duplicate Relationships
        print("\nCheck 5: Duplicate USES Relationships")
        result = session.run("""
            MATCH (p:Pattern)-[r:USES]->(t:Technology)
            WITH p, t, count(r) AS rel_count
            WHERE rel_count > 1
            RETURN p.name AS pattern, t.name AS technology, rel_count
            LIMIT 10
        """)
        
        duplicates = list(result)
        if duplicates:
            print(f"  [X] FAILED: Found {len(duplicates)} patterns with duplicate USES relationships")
            for dup in duplicates:
                print(f"      - {dup['pattern']} -> {dup['technology']} ({dup['rel_count']} relationships)")
        else:
            print("  [OK] PASSED: No duplicate USES relationships")
        
        # Check 6: Duplicate Require Relationships
        print("\nCheck 6: Duplicate REQUIRES Relationships")
        result = session.run("""
            MATCH (p:Pattern)-[r:REQUIRES]->(c:Constraint)
            WITH p, c, count(r) AS rel_count
            WHERE rel_count > 1
            RETURN p.name AS pattern, c.rule AS constraint, rel_count
            LIMIT 10
        """)
        
        duplicates = list(result)
        if duplicates:
            print(f"  [X] FAILED: Found {len(duplicates)} patterns with duplicate REQUIRES relationships")
            for dup in duplicates:
                print(f"      - {dup['pattern']} -> {dup['constraint']} ({dup['rel_count']} relationships)")
        else:
            print("  [OK] PASSED: No duplicate REQUIRES relationships")
        
        # Check 7: Constraints Exist
        print("\nCheck 7: Unique Constraints Exist")
        result = session.run("""
            SHOW CONSTRAINTS
            YIELD name, type, labelsOrTypes, properties
            WHERE name IN ['tech_unique', 'constraint_unique']
            RETURN name, type, labelsOrTypes, properties
        """)
        
        constraints = list(result)
        expected_constraints = {'tech_unique', 'constraint_unique'}
        found_constraints = {c['name'] for c in constraints}
        
        if expected_constraints.issubset(found_constraints):
            print("  [OK] PASSED: All unique constraints exist")
            for c in constraints:
                print(f"      - {c['name']}: {c['labelsOrTypes']} ({c['properties']})")
        else:
            missing = expected_constraints - found_constraints
            print(f"  [X] FAILED: Missing constraints: {missing}")
        
        # Summary Statistics
        print("\n=== Summary Statistics ===\n")
        
        result = session.run("""
            MATCH (t:Technology)
            RETURN count(t) AS tech_count
        """)
        print(f"Technologies: {list(result)[0]['tech_count']}")
        
        result = session.run("""
            MATCH (c:Constraint)
            RETURN count(c) AS constraint_count
        """)
        print(f"Constraints: {list(result)[0]['constraint_count']}")
        
        result = session.run("""
            MATCH (p:Pattern)
            RETURN count(p) AS pattern_count
        """)
        print(f"Patterns: {list(result)[0]['pattern_count']}")
        
        result = session.run("""
            MATCH ()-[r:USES]->()
            RETURN count(r) AS uses_count
        """)
        print(f"USES relationships: {list(result)[0]['uses_count']}")
        
        result = session.run("""
            MATCH ()-[r:REQUIRES]->()
            RETURN count(r) AS requires_count
        """)
        print(f"REQUIRES relationships: {list(result)[0]['requires_count']}")
        
        print("\n=== Verification Complete ===\n")
    
    driver.close()

if __name__ == "__main__":
    verify_data_quality()
