"""
Verify migration was successful
Checks both old and new containers
"""

from neo4j import GraphDatabase

# OLD CONTAINER (plasticflower-neo4j)
OLD_URI = "bolt://localhost:7687"
OLD_USER = "neo4j"
OLD_PASSWORD = "specengine123"

# NEW CONTAINER (spec-engine-neo4j)
NEW_URI = "bolt://localhost:7688"
NEW_USER = "neo4j"
NEW_PASSWORD = "specengine123"

DATABASE = "neo4j"

PATTERN_LABELS = ["Pattern", "Requirement", "Constraint", "Technology", "ReferenceNode"]

def check_container(uri, name):
    """Check a container's data"""
    driver = GraphDatabase.driver(uri, auth=(OLD_USER, OLD_PASSWORD if "7687" in uri else NEW_PASSWORD))
    
    try:
        with driver.session(database=DATABASE) as session:
            # Count all nodes
            all_nodes = session.run("MATCH (n) RETURN count(n) as count").single()["count"]
            all_rels = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()["count"]
            
            # Count pattern extraction nodes
            labels_str = "|".join(PATTERN_LABELS)
            pattern_nodes = session.run(f"MATCH (n:{labels_str}) RETURN count(n) as count").single()["count"]
            pattern_rels = session.run(f"MATCH (a:{labels_str})-[r]->(b:{labels_str}) RETURN count(r) as count").single()["count"]
            
            # Get all labels
            labels = [r["label"] for r in session.run("CALL db.labels()")]
            
            return {
                "all_nodes": all_nodes,
                "all_rels": all_rels,
                "pattern_nodes": pattern_nodes,
                "pattern_rels": pattern_rels,
                "labels": labels
            }
    except Exception as e:
        return {"error": str(e)}
    finally:
        driver.close()

print("="*70)
print("Migration Verification Report")
print("="*70)

print("\n[1] OLD Container (plasticflower-neo4j) - bolt://localhost:7687")
print("-"*70)
old_stats = check_container(OLD_URI, "OLD")
if "error" in old_stats:
    print(f"  ERROR: {old_stats['error']}")
else:
    print(f"  Total nodes:              {old_stats['all_nodes']}")
    print(f"  Total relationships:      {old_stats['all_rels']}")
    print(f"  Pattern extraction nodes: {old_stats['pattern_nodes']}")
    print(f"  Pattern extraction rels:  {old_stats['pattern_rels']}")
    print(f"  Labels: {', '.join(old_stats['labels'])}")

print("\n[2] NEW Container (spec-engine-neo4j) - bolt://localhost:7688")
print("-"*70)
new_stats = check_container(NEW_URI, "NEW")
if "error" in new_stats:
    print(f"  ERROR: {new_stats['error']}")
else:
    print(f"  Total nodes:              {new_stats['all_nodes']}")
    print(f"  Total relationships:      {new_stats['all_rels']}")
    print(f"  Pattern extraction nodes: {new_stats['pattern_nodes']}")
    print(f"  Pattern extraction rels:  {new_stats['pattern_rels']}")
    print(f"  Labels: {', '.join(new_stats['labels'])}")

print("\n" + "="*70)
print("Verification Summary")
print("="*70)

if "error" not in old_stats and "error" not in new_stats:
    if old_stats['pattern_nodes'] == 0 and new_stats['pattern_nodes'] > 0:
        print("\n✓ SUCCESS! Migration completed successfully!")
        print(f"  - Moved {new_stats['pattern_nodes']} pattern extraction nodes to NEW container")
        print(f"  - Moved {new_stats['pattern_rels']} relationships to NEW container")
        print(f"  - Left {old_stats['all_nodes']} other project nodes in OLD container")
        print(f"  - OLD container cleaned of pattern extraction data")
        print("\nYour .env should be configured for NEW container (bolt://localhost:7688)")
    elif old_stats['pattern_nodes'] > 0 and new_stats['pattern_nodes'] > 0:
        print("\n⚠ WARNING: Pattern data exists in BOTH containers!")
        print(f"  - OLD container: {old_stats['pattern_nodes']} pattern nodes")
        print(f"  - NEW container: {new_stats['pattern_nodes']} pattern nodes")
        print("\nYou may want to run the cleanup step on the OLD container.")
    elif old_stats['pattern_nodes'] > 0 and new_stats['pattern_nodes'] == 0:
        print("\n⚠ WARNING: Pattern data still in OLD container, NEW container is empty!")
        print("  Migration may not have completed. Run migrate_to_new_container.py again.")
    else:
        print("\n⚠ No pattern extraction data found in either container!")
else:
    print("\n✗ Could not verify - connection errors")
    if "error" in old_stats:
        print(f"  OLD container error: {old_stats['error']}")
    if "error" in new_stats:
        print(f"  NEW container error: {new_stats['error']}")

print("\n" + "="*70)
print("\nContainer Access:")
print("  OLD: http://localhost:7474 (other project)")
print("  NEW: http://localhost:7475 (pattern extraction)")
print("="*70)
