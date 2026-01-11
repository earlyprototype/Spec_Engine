"""
Test connection with both possible passwords
"""

from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7688"
NEO4J_USER = "neo4j"
DATABASE = "neo4j"

PASSWORDS = ["neo4j", "specengine123", "password"]

print("Testing Neo4j connection...")
print(f"URI: {NEO4J_URI}")
print("-" * 60)

for pwd in PASSWORDS:
    try:
        print(f"\nTrying password: {pwd}")
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, pwd))
        with driver.session(database=DATABASE) as session:
            result = session.run("MATCH (n) RETURN count(n) as count")
            count = result.single()["count"]
            print(f"  SUCCESS! Connected with password: {pwd}")
            print(f"  Total nodes: {count}")
            
            # Get pattern count
            result = session.run("MATCH (p:Pattern) RETURN count(p) as count")
            pattern_count = result.single()["count"]
            print(f"  Pattern nodes: {pattern_count}")
            
            print(f"\nUpdate your .env file:")
            print(f"  NEO4J_PASSWORD={pwd}")
            
        driver.close()
        break
    except Exception as e:
        error_msg = str(e)
        if "Unauthorized" in error_msg:
            print(f"  Failed: Wrong password")
        elif "password change required" in error_msg.lower() or "credentials have expired" in error_msg.lower():
            print(f"  Failed: Password change required")
            print(f"\n  Action needed:")
            print(f"  1. Open http://localhost:7475")
            print(f"  2. Login with: neo4j/neo4j")
            print(f"  3. Change password to: specengine123")
        else:
            print(f"  Failed: {error_msg}")
else:
    print("\n" + "="*60)
    print("Could not connect with any password!")
    print("="*60)
    print("\nThe container may need password initialization.")
    print("\nPlease:")
    print("1. Open http://localhost:7475 in your browser")
    print("2. Try to connect with username 'neo4j' and password 'neo4j'")
    print("3. When prompted, change the password to 'specengine123'")
    print("4. Run: python quick_test.py")
