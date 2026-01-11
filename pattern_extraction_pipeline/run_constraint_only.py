import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(override=True)

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")

print("=" * 70)
print("CONSTRAINT SETUP FOR DUPLICATE DETECTION")
print("=" * 70)

driver = GraphDatabase.driver(uri, auth=(user, password), connection_timeout=5.0)

try:
    with driver.session() as session:
        # Check for existing duplicates
        print("\n1. Checking for duplicate Pattern nodes...")
        result = session.run("""
            MATCH (p:Pattern)
            WITH p.source_repo as repo, count(*) as cnt, collect(p) as patterns
            WHERE cnt > 1
            RETURN repo, cnt, patterns
            ORDER BY cnt DESC
            LIMIT 5
        """)
        
        duplicates = list(result)
        if duplicates:
            print(f"   [WARNING] Found {len(duplicates)} repositories with duplicate patterns:")
            for record in duplicates:
                print(f"     - {record['repo']}: {record['cnt']} copies")
            print("   [INFO] These will be preserved; constraint will prevent future duplicates")
        else:
            print("   [OK] No duplicates found")
        
        # Create the constraint
        print("\n2. Creating Pattern.source_repo uniqueness constraint...")
        try:
            session.run("""
                CREATE CONSTRAINT pattern_repo_unique IF NOT EXISTS 
                FOR (p:Pattern) 
                REQUIRE p.source_repo IS UNIQUE
            """)
            print("   [OK] Constraint created successfully")
        except Exception as e:
            if "already exists" in str(e).lower() or "equivalent" in str(e).lower():
                print("   [OK] Constraint already exists")
            else:
                print(f"   [ERROR] Constraint creation failed: {e}")
                raise
        
        # Verify constraint exists
        print("\n3. Verifying constraints...")
        result = session.run("SHOW CONSTRAINTS")
        constraints = list(result)
        pattern_constraints = [c for c in constraints if 'pattern' in c.get('name', '').lower()]
        
        if pattern_constraints:
            print(f"   [OK] Found {len(pattern_constraints)} Pattern-related constraint(s):")
            for c in pattern_constraints:
                print(f"     - {c.get('name', 'unnamed')}")
        else:
            print("   [WARNING] No Pattern constraints found!")
        
        print("\n" + "=" * 70)
        print("SETUP COMPLETE")
        print("=" * 70)
        
except Exception as e:
    print(f"\n[ERROR] Setup failed: {e}")
    raise
finally:
    driver.close()
