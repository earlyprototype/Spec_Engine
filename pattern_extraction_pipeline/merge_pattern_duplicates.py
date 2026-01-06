import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(override=True)

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")

print("=" * 70)
print("PATTERN DUPLICATE MERGE - SMART DUPLICATE DETECTION")
print("=" * 70)

driver = GraphDatabase.driver(uri, auth=(user, password), connection_timeout=5.0)

try:
    with driver.session() as session:
        print("\n[1/3] Finding duplicate Pattern nodes...")
        
        dup_groups = session.run("""
            MATCH (p:Pattern)
            WITH p.source_repo as repo, collect(p) AS nodes
            WHERE size(nodes) > 1
            RETURN repo, nodes, size(nodes) as count
            ORDER BY count DESC
        """)
        
        groups = list(dup_groups)
        if not groups:
            print("   [OK] No duplicates found - database is clean!")
        else:
            print(f"   [INFO] Found {len(groups)} repositories with duplicates:")
            for g in groups[:10]:
                print(f"     - {g['repo']}: {g['count']} copies")
            if len(groups) > 10:
                print(f"     ... and {len(groups) - 10} more")
        
            print(f"\n[2/3] Merging {len(groups)} duplicate groups...")
            merged_count = 0
            
            for i, group in enumerate(groups, 1):
                nodes = group['nodes']
                repo = group['repo']
                
                # Keep the best one (highest quality or most recent)
                primary = max(nodes, key=lambda n: (
                    n.get('quality_score', 0), 
                    n.get('extracted_at', '')
                ))
                duplicates = [n for n in nodes if n.element_id != primary.element_id]
                
                print(f"   [{i}/{len(groups)}] Merging {repo}...")
                print(f"     - Keeping node with quality {primary.get('quality_score', 'N/A')}")
                print(f"     - Removing {len(duplicates)} duplicates")
                
                for dup in duplicates:
                    # Transfer relationships to primary
                    try:
                        session.run("""
                            MATCH (dup) WHERE elementId(dup) = $dup_id
                            MATCH (primary) WHERE elementId(primary) = $primary_id
                            OPTIONAL MATCH (dup)-[r]-(other)
                            WITH dup, primary, r, other, type(r) as rel_type
                            WHERE other IS NOT NULL AND elementId(other) <> $primary_id
                            CALL apoc.create.relationship(
                                CASE WHEN startNode(r) = dup THEN primary ELSE other END,
                                rel_type,
                                properties(r),
                                CASE WHEN startNode(r) = dup THEN other ELSE primary END
                            ) YIELD rel
                            DELETE r
                        """, dup_id=dup.element_id, primary_id=primary.element_id)
                        
                        # Delete duplicate
                        session.run("""
                            MATCH (dup) WHERE elementId(dup) = $dup_id
                            DETACH DELETE dup
                        """, dup_id=dup.element_id)
                        
                        merged_count += 1
                    except Exception as e:
                        print(f"     [WARN] Error merging {dup.element_id}: {e}")
            
            print(f"\n   [OK] Merged {merged_count} duplicate pattern nodes")
        
        print(f"\n[3/3] Creating uniqueness constraint...")
        try:
            session.run("""
                CREATE CONSTRAINT pattern_repo_unique IF NOT EXISTS 
                FOR (p:Pattern) 
                REQUIRE p.source_repo IS UNIQUE
            """)
            print("   [OK] Constraint created successfully!")
        except Exception as e:
            if "already exists" in str(e).lower() or "equivalent" in str(e).lower():
                print("   [OK] Constraint already exists")
            else:
                print(f"   [ERROR] Failed: {e}")
                raise
        
        # Verify final state
        print("\n[VERIFICATION]")
        result = session.run("MATCH (p:Pattern) WITH p.source_repo as repo, count(*) as cnt WHERE cnt > 1 RETURN count(*) as dup_count")
        dup_count = result.single()['dup_count']
        
        result = session.run("SHOW CONSTRAINTS")
        constraints = [c for c in list(result) if 'pattern' in c.get('name', '').lower()]
        
        print(f"   - Remaining duplicates: {dup_count}")
        print(f"   - Pattern constraints: {len(constraints)}")
        
        if dup_count == 0 and len(constraints) > 0:
            print("\n" + "=" * 70)
            print("SUCCESS! Database is ready for duplicate detection.")
            print("=" * 70)
        else:
            print("\n[WARNING] Database may need additional cleanup")
        
except Exception as e:
    print(f"\n[ERROR] Merge failed: {e}")
    import traceback
    traceback.print_exc()
finally:
    driver.close()
