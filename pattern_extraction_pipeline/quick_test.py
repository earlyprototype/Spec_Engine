import os
from dotenv import load_dotenv

# Load .env
load_dotenv(override=True)

print("=" * 50)
print("Environment Variables Loaded:")
print("=" * 50)
print(f"NEO4J_URI: {os.getenv('NEO4J_URI', 'NOT SET')}")
print(f"NEO4J_USER: {os.getenv('NEO4J_USER', 'NOT SET')}")
print(f"NEO4J_PASSWORD: {os.getenv('NEO4J_PASSWORD', 'NOT SET')}")
print(f"NEO4J_DATABASE: {os.getenv('NEO4J_DATABASE', 'NOT SET')}")
print("=" * 50)

# Try quick connection
from neo4j import GraphDatabase
import sys

uri = os.getenv("NEO4J_URI", "bolt://localhost:7688")
user = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "password")

print(f"\nAttempting connection to {uri}...")
print(f"Username: {user}")
print(f"Password: {'*' * len(password)}")

try:
    driver = GraphDatabase.driver(uri, auth=(user, password), connection_timeout=5.0)
    driver.verify_connectivity()
    print("\n[SUCCESS] Connected!")
    
    with driver.session() as session:
        result = session.run("MATCH (p:Pattern) RETURN count(p) as count")
        count = result.single()["count"]
        print(f"[OK] Found {count} patterns")
    
    driver.close()
    print("[OK] Test complete\n")
    sys.exit(0)
    
except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {e}\n")
    sys.exit(1)
