import os
print("START")
os.environ["NEO4J_URI"] = "bolt://localhost:7688"
os.environ["NEO4J_USER"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "specengine123"

from neo4j import GraphDatabase

print("Connecting...")
driver = GraphDatabase.driver(
    "bolt://localhost:7688",
    auth=("neo4j", "specengine123"),
    connection_timeout=5.0
)

with driver.session() as session:
    result = session.run("RETURN 1 as test")
    print(f"Result: {result.single()['test']}")
    
driver.close()
print("END")
