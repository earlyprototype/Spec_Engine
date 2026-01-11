"""
Neo4j Connection Diagnostic Tool
Checks Neo4j connectivity and environment configuration
"""

import os
import sys
from dotenv import load_dotenv

# Load .env file
load_dotenv(override=True)

print("="*70)
print("NEO4J CONNECTION DIAGNOSTIC")
print("="*70)

# Check environment variables
print("\n[1] ENVIRONMENT VARIABLES")
print("-" * 70)

uri = os.getenv("NEO4J_URI", "bolt://localhost:7688")  # Default to spec-engine-neo4j
user = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD")

print(f"  NEO4J_URI:      {uri}")
print(f"  NEO4J_USER:     {user}")
print(f"  NEO4J_PASSWORD: {'SET' if password else 'NOT SET (MISSING!)'}")

if not password:
    print("\n  [ERROR] NEO4J_PASSWORD is not set!")
    print("  Fix: Add 'NEO4J_PASSWORD=your_password' to .env file")
    sys.exit(1)

# Try to connect
print("\n[2] CONNECTION TEST")
print("-" * 70)

try:
    from neo4j import GraphDatabase
    
    print(f"  Connecting to {uri}...")
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    # Test query
    with driver.session() as session:
        result = session.run("RETURN 1 as test")
        record = result.single()
        if record and record["test"] == 1:
            print(f"  [SUCCESS] Connected to Neo4j!")
            
            # Get database info
            info = session.run("CALL dbms.components() YIELD name, versions, edition")
            for record in info:
                print(f"  Version: {record['versions'][0]}")
                print(f"  Edition: {record['edition']}")
            
            # Count nodes
            count_result = session.run("MATCH (n) RETURN count(n) as count")
            count = count_result.single()["count"]
            print(f"  Total nodes: {count}")
    
    driver.close()
    print("\n[SUCCESS] Neo4j is running and accessible!")
    print("="*70)
    
except Exception as e:
    print(f"  [FAILED] {e}")
    print("\n[3] TROUBLESHOOTING")
    print("-" * 70)
    print("  Possible causes:")
    print("  1. Neo4j is not running")
    print("     - Start Neo4j Desktop and click 'Start' on your database")
    print("     - OR run: docker start neo4j")
    print("")
    print("  2. Wrong connection URI")
    print("     - Check if Neo4j is on a different port")
    print("     - Try: bolt://localhost:7688 (if using spec-engine-neo4j)")
    print("")
    print("  3. Wrong password")
    print("     - Check your .env file")
    print("     - Default Neo4j password is often 'neo4j' or 'password'")
    print("")
    print("  4. Firewall blocking connection")
    print("     - Allow port 7687 (or 7688) in Windows Firewall")
    print("="*70)
    sys.exit(1)
