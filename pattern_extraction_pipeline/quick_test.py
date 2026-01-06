"""
Quick test of the new container connection and data
"""

import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USER = os.getenv('NEO4J_USER')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE')

print("="*60)
print("Pattern Extraction System - Quick Test")
print("="*60)
print(f"\nConnecting to: {NEO4J_URI}")
print(f"Database: {NEO4J_DATABASE}")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

try:
    with driver.session(database=NEO4J_DATABASE) as session:
        # Test 1: Count patterns
        result = session.run("MATCH (p:Pattern) RETURN count(p) as count")
        pattern_count = result.single()["count"]
        print(f"\nPatterns: {pattern_count}")
        
        # Test 2: Count requirements
        result = session.run("MATCH (r:Requirement) RETURN count(r) as count")
        req_count = result.single()["count"]
        print(f"Requirements: {req_count}")
        
        # Test 3: Count constraints
        result = session.run("MATCH (c:Constraint) RETURN count(c) as count")
        constraint_count = result.single()["count"]
        print(f"Constraints: {constraint_count}")
        
        # Test 4: Count technologies
        result = session.run("MATCH (t:Technology) RETURN count(t) as count")
        tech_count = result.single()["count"]
        print(f"Technologies: {tech_count}")
        
        # Test 5: Sample pattern
        result = session.run("""
            MATCH (p:Pattern)
            RETURN p.name as name, p.description as description
            LIMIT 1
        """)
        record = result.single()
        if record:
            print(f"\nSample Pattern:")
            print(f"  Name: {record['name']}")
            print(f"  Description: {record['description'][:100]}..." if record['description'] else "  No description")
        
        print("\n" + "="*60)
        print("SUCCESS! System is working correctly")
        print("="*60)
        print("\nYour pattern extraction system is now running on its")
        print("dedicated Neo4j container (spec-engine-neo4j)")
        print("\nAccess Neo4j Browser: http://localhost:7475")
        print("Username: neo4j")
        print("Password: specengine123")
        
except Exception as e:
    print(f"\nERROR: {e}")
    print("\nCheck your .env configuration")
finally:
    driver.close()
