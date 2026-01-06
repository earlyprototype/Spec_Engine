# test_connection.py
# Quick connection test for Neo4j

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(override=True)

print("\n" + "="*70)
print("NEO4J CONNECTION TEST")
print("="*70)

uri = os.getenv("NEO4J_URI", "bolt://localhost:7688")  # spec-engine-neo4j uses port 7688
user = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "password")

print(f"\nConnection Details:")
print(f"  URI: {uri}")
print(f"  User: {user}")
print(f"  Password: {'*' * len(password)}")

try:
    print("\nConnecting...")
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    with driver.session() as session:
        # Test basic query
        result = session.run("RETURN 1 as test")
        test_value = result.single()["test"]
        print(f"[OK] Connection successful! Test query returned: {test_value}")
        
        # Check for patterns
        result = session.run("MATCH (p:Pattern) RETURN count(p) as count")
        pattern_count = result.single()["count"]
        print(f"[OK] Found {pattern_count} patterns in database")
        
        # Check for constraints
        result = session.run("SHOW CONSTRAINTS")
        constraints = list(result)
        print(f"[OK] Found {len(constraints)} constraints:")
        for constraint in constraints:
            print(f"     - {constraint.get('name', 'unnamed')}")
    
    driver.close()
    print("\n[SUCCESS] All connection tests passed!\n")
    
except Exception as e:
    print(f"\n[ERROR] Connection failed: {e}\n")
    print("Possible issues:")
    print("  1. Neo4j container not running")
    print("  2. Incorrect port (check docker ps)")
    print("  3. Wrong credentials in .env file")
    print("  4. Firewall blocking connection")
