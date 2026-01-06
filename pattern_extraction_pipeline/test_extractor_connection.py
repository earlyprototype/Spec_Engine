"""
Test if pattern_extractor can connect to Neo4j
"""
import os
from dotenv import load_dotenv

# Force reload environment
load_dotenv(override=True)

print("Environment variables:")
print(f"  NEO4J_URI: {os.getenv('NEO4J_URI')}")
print(f"  NEO4J_USER: {os.getenv('NEO4J_USER')}")
print(f"  NEO4J_PASSWORD: {os.getenv('NEO4J_PASSWORD')}")
print(f"  NEO4J_DATABASE: {os.getenv('NEO4J_DATABASE')}")
print()

try:
    from pattern_extractor import PatternExtractor
    print("Creating PatternExtractor...")
    extractor = PatternExtractor()
    print("SUCCESS: PatternExtractor created and connected to Neo4j!")
    
    # Test a simple query
    from neo4j import GraphDatabase
    driver = GraphDatabase.driver(
        os.getenv('NEO4J_URI'),
        auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
    )
    with driver.session(database=os.getenv('NEO4J_DATABASE')) as session:
        result = session.run("MATCH (n) RETURN count(n) as count")
        count = result.single()["count"]
        print(f"Neo4j connection verified: {count} total nodes")
    driver.close()
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
