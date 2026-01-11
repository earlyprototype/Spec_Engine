"""
Migrate Pattern Extraction Data to New Container
Exports from old shared container, imports to new dedicated container
"""

import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# OLD CONTAINER (plasticflower-neo4j)
OLD_NEO4J_URI = "bolt://localhost:7687"  # Original container
OLD_NEO4J_USER = "neo4j"
OLD_NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'specengine123')  # Will ask if needed

# NEW CONTAINER (spec-engine-neo4j) - from docker-compose.yml
NEW_NEO4J_URI = "bolt://localhost:7688"
NEW_NEO4J_USER = "neo4j"
NEW_NEO4J_PASSWORD = "specengine123"

# Database is always 'neo4j' in Community Edition
DATABASE = "neo4j"

# Labels that belong to the pattern extraction system
PATTERN_EXTRACTION_LABELS = [
    "Pattern",
    "Requirement",
    "Constraint",
    "Technology",
    "ReferenceNode"
]


class ContainerMigration:
    def __init__(self):
        # Connect to both containers
        print("[ACTION] Connecting to OLD container (plasticflower-neo4j)...")
        self.old_driver = GraphDatabase.driver(OLD_NEO4J_URI, auth=(OLD_NEO4J_USER, OLD_NEO4J_PASSWORD))
        
        print("[ACTION] Connecting to NEW container (spec-engine-neo4j)...")
        self.new_driver = GraphDatabase.driver(NEW_NEO4J_URI, auth=(NEW_NEO4J_USER, NEW_NEO4J_PASSWORD))
        print("[OK] Connected to both containers")
        
    def close(self):
        self.old_driver.close()
        self.new_driver.close()
        
    def get_statistics(self, driver, labels_filter=None):
        """Get statistics about the database"""
        with driver.session(database=DATABASE) as session:
            try:
                if labels_filter:
                    # Count only nodes with specified labels
                    labels_str = "|".join(labels_filter)
                    node_result = session.run(f"MATCH (n:{labels_str}) RETURN count(n) as count")
                    node_count = node_result.single()["count"]
                    
                    # Count only relationships between filtered nodes
                    rel_result = session.run(f"MATCH (a:{labels_str})-[r]->(b:{labels_str}) RETURN count(r) as count")
                    rel_count = rel_result.single()["count"]
                else:
                    # Count all nodes
                    node_result = session.run("MATCH (n) RETURN count(n) as count")
                    node_count = node_result.single()["count"]
                    
                    # Count all relationships
                    rel_result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
                    rel_count = rel_result.single()["count"]
                
                # Get node labels
                label_result = session.run("CALL db.labels()")
                labels = [record["label"] for record in label_result]
                
                return {
                    "nodes": node_count,
                    "relationships": rel_count,
                    "labels": labels
                }
            except Exception as e:
                print(f"[ERROR] Failed to get statistics: {e}")
                return None
                
    def export_data(self, labels_filter):
        """Export pattern extraction data from old container"""
        print(f"\n[ACTION] Exporting pattern extraction data from OLD container...")
        with self.old_driver.session(database=DATABASE) as session:
            try:
                labels_str = "|".join(labels_filter)
                
                # Export nodes
                nodes_result = session.run(f"""
                    MATCH (n:{labels_str})
                    RETURN id(n) as id, labels(n) as labels, properties(n) as props
                """)
                nodes = list(nodes_result)
                print(f"[OK] Exported {len(nodes)} nodes")
                
                # Export relationships
                rels_result = session.run(f"""
                    MATCH (a:{labels_str})-[r]->(b:{labels_str})
                    RETURN id(a) as start_id, id(b) as end_id, 
                           type(r) as type, properties(r) as props
                """)
                relationships = list(rels_result)
                print(f"[OK] Exported {len(relationships)} relationships")
                
                return {"nodes": nodes, "relationships": relationships}
            except Exception as e:
                print(f"[ERROR] Failed to export data: {e}")
                raise
                
    def import_data(self, data):
        """Import data into new container"""
        print(f"\n[ACTION] Importing data into NEW container...")
        
        with self.new_driver.session(database=DATABASE) as session:
            try:
                # Create a mapping of old IDs to new nodes
                id_mapping = {}
                
                # Import nodes
                print(f"[ACTION] Importing {len(data['nodes'])} nodes...")
                for i, node in enumerate(data['nodes']):
                    if i % 100 == 0 and i > 0:
                        print(f"  Progress: {i}/{len(data['nodes'])} nodes...")
                    
                    old_id = node['id']
                    labels = ':'.join(node['labels'])
                    props = node['props']
                    
                    # Create node with properties
                    result = session.run(f"""
                        CREATE (n:{labels})
                        SET n = $props
                        RETURN id(n) as new_id
                    """, props=props)
                    
                    new_id = result.single()['new_id']
                    id_mapping[old_id] = new_id
                
                print(f"[OK] Imported {len(data['nodes'])} nodes")
                
                # Import relationships
                print(f"[ACTION] Importing {len(data['relationships'])} relationships...")
                for i, rel in enumerate(data['relationships']):
                    if i % 100 == 0 and i > 0:
                        print(f"  Progress: {i}/{len(data['relationships'])} relationships...")
                    
                    start_id = id_mapping[rel['start_id']]
                    end_id = id_mapping[rel['end_id']]
                    rel_type = rel['type']
                    props = rel['props']
                    
                    # Create relationship
                    session.run(f"""
                        MATCH (a), (b)
                        WHERE id(a) = $start_id AND id(b) = $end_id
                        CREATE (a)-[r:{rel_type}]->(b)
                        SET r = $props
                    """, start_id=start_id, end_id=end_id, props=props)
                
                print(f"[OK] Imported {len(data['relationships'])} relationships")
                
            except Exception as e:
                print(f"[ERROR] Failed to import data: {e}")
                raise
                
    def delete_old_data(self, labels_filter):
        """Delete pattern extraction data from old container"""
        print(f"\n[WARNING] This will delete pattern extraction data from OLD container")
        print(f"Labels to delete: {', '.join(labels_filter)}")
        print(f"Other project data will remain intact.")
        print()
        response = input("Are you sure you want to proceed? (yes/no): ")
        
        if response.lower() != 'yes':
            print("[SKIP] Cleanup cancelled")
            return
            
        with self.old_driver.session(database=DATABASE) as session:
            try:
                labels_str = "|".join(labels_filter)
                
                print(f"[ACTION] Deleting relationships...")
                result = session.run(f"MATCH (:{labels_str})-[r]-() DELETE r RETURN count(r) as count")
                rel_count = result.single()['count']
                print(f"[OK] Deleted {rel_count} relationships")
                
                print(f"[ACTION] Deleting nodes...")
                result = session.run(f"MATCH (n:{labels_str}) DELETE n RETURN count(n) as count")
                node_count = result.single()['count']
                print(f"[OK] Deleted {node_count} nodes")
                
                print(f"[OK] Pattern extraction data cleaned from OLD container")
                print(f"[OK] Other project data remains intact")
            except Exception as e:
                print(f"[ERROR] Failed to clean old data: {e}")
                raise


def main():
    print("="*60)
    print("Container Migration: plasticflower-neo4j -> spec-engine-neo4j")
    print("="*60)
    print("\nThis migration will:")
    print(f"  - Export pattern extraction data from OLD container")
    print(f"    (Labels: {', '.join(PATTERN_EXTRACTION_LABELS)})")
    print(f"  - Import into NEW dedicated container")
    print(f"  - Clean pattern extraction data from OLD container")
    print(f"  - Leave other project data in OLD container")
    print("="*60)
    
    migration = ContainerMigration()
    
    try:
        # Step 1: Analyze old container
        print(f"\n[STEP 1] Analyzing OLD container...")
        old_all_stats = migration.get_statistics(migration.old_driver)
        old_pattern_stats = migration.get_statistics(migration.old_driver, PATTERN_EXTRACTION_LABELS)
        
        if old_all_stats:
            print(f"\nAll Data in OLD container:")
            print(f"  Nodes: {old_all_stats['nodes']}")
            print(f"  Relationships: {old_all_stats['relationships']}")
            
            print(f"\nPattern Extraction Data (to be moved):")
            print(f"  Nodes: {old_pattern_stats['nodes']}")
            print(f"  Relationships: {old_pattern_stats['relationships']}")
            
            other_nodes = old_all_stats['nodes'] - old_pattern_stats['nodes']
            print(f"\nOther Project Data (will remain):")
            print(f"  Nodes: {other_nodes}")
        
        if old_pattern_stats['nodes'] == 0:
            print(f"\n[WARNING] No pattern extraction data found in OLD container.")
            print("[INFO] Nothing to migrate.")
            return
        
        # Step 2: Check new container is empty
        print(f"\n[STEP 2] Checking NEW container...")
        new_stats = migration.get_statistics(migration.new_driver)
        print(f"  Nodes: {new_stats['nodes']}")
        print(f"  Relationships: {new_stats['relationships']}")
        
        if new_stats['nodes'] > 0:
            print(f"\n[WARNING] NEW container is not empty!")
            response = input("Do you want to clear it and proceed? (yes/no): ")
            if response.lower() == 'yes':
                with migration.new_driver.session(database=DATABASE) as session:
                    session.run("MATCH (n) DETACH DELETE n")
                print("[OK] Cleared NEW container")
            else:
                print("[CANCELLED] Migration cancelled")
                return
        
        # Confirm before proceeding
        print(f"\n{'='*60}")
        response = input("Proceed with migration? (yes/no): ")
        if response.lower() != 'yes':
            print("[CANCELLED] Migration cancelled")
            return
        
        # Step 3: Export from old container
        print(f"\n[STEP 3] Exporting from OLD container...")
        data = migration.export_data(PATTERN_EXTRACTION_LABELS)
        
        # Step 4: Import to new container
        print(f"\n[STEP 4] Importing to NEW container...")
        migration.import_data(data)
        
        # Step 5: Verify migration
        print(f"\n[STEP 5] Verifying migration...")
        new_verify_stats = migration.get_statistics(migration.new_driver)
        print(f"\nNEW Container Statistics:")
        print(f"  Nodes: {new_verify_stats['nodes']}")
        print(f"  Relationships: {new_verify_stats['relationships']}")
        
        if (old_pattern_stats['nodes'] == new_verify_stats['nodes'] and 
            old_pattern_stats['relationships'] == new_verify_stats['relationships']):
            print("\n[OK] Migration verified successfully!")
        else:
            print("\n[ERROR] Migration verification failed!")
            print("[WARNING] Do NOT clean the old container yet!")
            return
        
        # Step 6: Clean old container
        print(f"\n[STEP 6] Cleaning pattern extraction data from OLD container...")
        migration.delete_old_data(PATTERN_EXTRACTION_LABELS)
        
        # Final verification
        print(f"\n[STEP 7] Final verification...")
        final_old_stats = migration.get_statistics(migration.old_driver)
        print(f"\nOLD Container (plasticflower-neo4j) after cleanup:")
        print(f"  Remaining nodes: {final_old_stats['nodes']}")
        print(f"  Remaining labels: {', '.join(final_old_stats['labels']) if final_old_stats['labels'] else 'None'}")
        
        print(f"\nNEW Container (spec-engine-neo4j):")
        print(f"  Nodes: {new_verify_stats['nodes']}")
        print(f"  Labels: {', '.join(new_verify_stats['labels']) if new_verify_stats['labels'] else 'None'}")
        
        print("\n" + "="*60)
        print("Migration Completed Successfully!")
        print("="*60)
        print(f"\nWhat happened:")
        print(f"  Moved {old_pattern_stats['nodes']} pattern extraction nodes to NEW container")
        print(f"  Moved {old_pattern_stats['relationships']} relationships to NEW container")
        print(f"  Left {final_old_stats['nodes']} other project nodes in OLD container")
        print(f"\nContainers:")
        print(f"  OLD (plasticflower-neo4j): bolt://localhost:7687 - Other project only")
        print(f"  NEW (spec-engine-neo4j):   bolt://localhost:7688 - Pattern extraction only")
        print(f"\nYour .env should now point to: bolt://localhost:7688")
        
    except Exception as e:
        print(f"\n[ERROR] Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        migration.close()


if __name__ == "__main__":
    main()
