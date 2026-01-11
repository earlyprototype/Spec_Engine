"""
Check old container status - try different passwords
"""

from neo4j import GraphDatabase

OLD_URI = "bolt://localhost:7687"
OLD_USER = "neo4j"
PASSWORDS = ["specengine123", "password", "plasticflower"]
DATABASE = "neo4j"

PATTERN_LABELS = ["Pattern", "Requirement", "Constraint", "Technology", "ReferenceNode"]

print("Checking OLD container (plasticflower-neo4j)...")
print("-" * 60)

for pwd in PASSWORDS:
    try:
        driver = GraphDatabase.driver(OLD_URI, auth=(OLD_USER, pwd))
        with driver.session(database=DATABASE) as session:
            all_nodes = session.run("MATCH (n) RETURN count(n) as count").single()["count"]
            labels_str = "|".join(PATTERN_LABELS)
            pattern_nodes = session.run(f"MATCH (n:{labels_str}) RETURN count(n) as count").single()["count"]
            labels = [r["label"] for r in session.run("CALL db.labels()")]
            
            print(f"\nConnected with password: {pwd}")
            print(f"  Total nodes: {all_nodes}")
            print(f"  Pattern extraction nodes: {pattern_nodes}")
            print(f"  Labels: {', '.join(labels)}")
            
            if pattern_nodes == 0:
                print("\n  SUCCESS: Pattern extraction data has been cleaned!")
                print(f"  {all_nodes} other project nodes remain")
            else:
                print(f"\n  WARNING: {pattern_nodes} pattern nodes still present")
                print("  You may want to run the cleanup step")
            
            driver.close()
            break
    except Exception as e:
        continue
else:
    print("\nCould not connect to OLD container with any known password")
    print("This is OK - the important thing is your NEW container has the data")
