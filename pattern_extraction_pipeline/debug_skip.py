from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv(override=True)

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)

with driver.session() as session:
    # Check what's stored
    result = session.run("""
        MATCH (p:Pattern)
        WHERE p.source_repo CONTAINS 'genai-stack'
        RETURN p.source_repo, p.name
        LIMIT 1
    """)
    
    record = result.single()
    if record:
        print(f"Found in DB: {record['p.source_repo']}")
        print(f"Pattern: {record['p.name']}")
        
        # Now test the exact query used by skip logic
        test_url = "https://github.com/docker/genai-stack"
        result2 = session.run("""
            MATCH (p:Pattern {source_repo: $repo_url})
            RETURN p.name
            LIMIT 1
        """, repo_url=test_url)
        
        if result2.single():
            print(f"\n[OK] Skip query WORKS for: {test_url}")
        else:
            print(f"\n[FAIL] Skip query FAILED for: {test_url}")
            print("URLs don't match!")
    else:
        print("genai-stack NOT in database")

driver.close()
