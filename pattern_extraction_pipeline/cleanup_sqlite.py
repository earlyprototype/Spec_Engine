# cleanup_sqlite.py
# Quick cleanup for SQLite duplicate nodes

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI", "bolt://localhost:7687"),
    auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
)

with driver.session() as session:
    print("\n=== Checking for SQLite duplicates ===\n")
    
    # Find all SQLite variants
    result = session.run("""
        MATCH (t:Technology)
        WHERE toLower(t.name) = 'sqlite'
        RETURN t.name AS name, elementId(t) AS id
        ORDER BY t.name
    """)
    
    nodes = list(result)
    print(f"Found {len(nodes)} SQLite node(s):")
    for node in nodes:
        print(f"  - {node['name']} (id: {node['id']})")
    
    if len(nodes) > 1:
        print(f"\n=== Merging {len(nodes) - 1} duplicate(s) ===\n")
        
        # Keep the lowercase one as primary
        primary = [n for n in nodes if n['name'] == 'sqlite'][0] if any(n['name'] == 'sqlite' for n in nodes) else nodes[0]
        duplicates = [n for n in nodes if n['id'] != primary['id']]
        
        print(f"Primary node: {primary['name']}")
        print(f"Duplicates to merge: {[d['name'] for d in duplicates]}")
        
        for dup in duplicates:
            # Transfer relationships
            session.run("""
                MATCH (dup) WHERE elementId(dup) = $dup_id
                MATCH (primary) WHERE elementId(primary) = $primary_id
                OPTIONAL MATCH (p:Pattern)-[r:USES]->(dup)
                WITH dup, primary, p, r
                WHERE p IS NOT NULL
                MERGE (p)-[new:USES]->(primary)
                ON CREATE SET new.role = r.role
                DELETE r
            """, dup_id=dup['id'], primary_id=primary['id'])
            
            # Delete duplicate
            session.run("""
                MATCH (dup) WHERE elementId(dup) = $dup_id
                DETACH DELETE dup
            """, dup_id=dup['id'])
            
            print(f"  [OK] Merged {dup['name']}")
        
        print("\n[OK] SQLite cleanup complete")
    else:
        print("\n[OK] No duplicates found - only one SQLite node exists")
    
    # Remove any duplicate relationships
    result = session.run("""
        MATCH (t:Technology {name: 'sqlite'})
        MATCH (p:Pattern)-[r:USES]->(t)
        WITH p, t, collect(r) AS rels
        WHERE size(rels) > 1
        FOREACH (rel IN tail(rels) | DELETE rel)
        RETURN count(p) AS cleaned_patterns
    """)
    
    cleaned = list(result)
    if cleaned and cleaned[0]['cleaned_patterns'] > 0:
        print(f"\n[OK] Removed duplicate USES relationships for {cleaned[0]['cleaned_patterns']} patterns")

driver.close()
