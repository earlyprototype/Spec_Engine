"""
Selective Neo4j Database Migration Script
Migrates ONLY pattern extraction data from 'neo4j' database to 'specengine' database
Leaves other project data intact in 'neo4j'
"""

import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USER = os.getenv('NEO4J_USER')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

SOURCE_DB = "neo4j"  # Default database where data currently resides
TARGET_DB = "specengine"

# Labels that belong to the pattern extraction system
PATTERN_EXTRACTION_LABELS = [
    "Pattern",
    "Requirement",
    "Constraint",
    "Technology",
    "ReferenceNode"
]


class Neo4jSelectiveMigration:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()
        
    def database_exists(self, db_name):
        """Check if a database exists"""
        with self.driver.session(database="system") as session:
            try:
                result = session.run("SHOW DATABASES")
                existing_dbs = [record["name"] for record in result]
                return db_name in existing_dbs
            except Exception as e:
                print(f"[ERROR] Failed to check databases: {e}")
                return False
        
    def create_database(self, db_name):
        """Create a new database if it doesn't exist"""
        with self.driver.session(database="system") as session:
            try:
                if self.database_exists(db_name):
                    print(f"[INFO] Database '{db_name}' already exists")
                    response = input(f"Do you want to drop and recreate '{db_name}'? (yes/no): ")
                    if response.lower() == 'yes':
                        print(f"[ACTION] Dropping database '{db_name}'...")
                        session.run(f"DROP DATABASE {db_name} IF EXISTS")
                        print(f"[ACTION] Creating database '{db_name}'...")
                        session.run(f"CREATE DATABASE {db_name}")
                        print(f"[OK] Database '{db_name}' created successfully")
                    else:
                        print(f"[SKIP] Keeping existing '{db_name}' database")
                else:
                    print(f"[ACTION] Creating database '{db_name}'...")
                    session.run(f"CREATE DATABASE {db_name}")
                    print(f"[OK] Database '{db_name}' created successfully")
            except Exception as e:
                print(f"[ERROR] Failed to create database: {e}")
                raise
                
    def get_statistics(self, db_name, labels_filter=None):
        """Get statistics about the database (optionally filtered by labels)"""
        if not self.database_exists(db_name):
            print(f"[WARNING] Database '{db_name}' does not exist")
            return {
                "nodes": 0,
                "relationships": 0,
                "labels": [],
                "relationship_types": []
            }
        
        with self.driver.session(database=db_name) as session:
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
                
                # Get relationship types
                type_result = session.run("CALL db.relationshipTypes()")
                rel_types = [record["relationshipType"] for record in type_result]
                
                return {
                    "nodes": node_count,
                    "relationships": rel_count,
                    "labels": labels,
                    "relationship_types": rel_types
                }
            except Exception as e:
                print(f"[ERROR] Failed to get statistics: {e}")
                return None
                
    def export_selective_data(self, db_name, labels_filter):
        """Export only nodes matching the label filter"""
        print(f"\n[ACTION] Exporting pattern extraction data from '{db_name}'...")
        with self.driver.session(database=db_name) as session:
            try:
                labels_str = "|".join(labels_filter)
                
                # Export nodes with specified labels
                nodes_result = session.run(f"""
                    MATCH (n:{labels_str})
                    RETURN id(n) as id, labels(n) as labels, properties(n) as props
                """)
                nodes = list(nodes_result)
                print(f"[OK] Exported {len(nodes)} pattern extraction nodes")
                
                # Export relationships between filtered nodes
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
                
    def import_data(self, db_name, data):
        """Import data into a database"""
        print(f"\n[ACTION] Importing data into '{db_name}'...")
        
        with self.driver.session(database=db_name) as session:
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
                
    def delete_selective_data(self, db_name, labels_filter):
        """Delete only nodes matching the label filter from source database"""
        print(f"\n[WARNING] This will delete pattern extraction data from '{db_name}'")
        print(f"Labels to delete: {', '.join(labels_filter)}")
        print(f"Other data in '{db_name}' will remain intact.")
        response = input("Are you sure you want to proceed? (yes/no): ")
        
        if response.lower() != 'yes':
            print("[SKIP] Database cleanup cancelled")
            return
            
        with self.driver.session(database=db_name) as session:
            try:
                labels_str = "|".join(labels_filter)
                
                print(f"[ACTION] Deleting relationships for pattern extraction nodes...")
                # Delete relationships connected to filtered nodes
                session.run(f"MATCH (:{labels_str})-[r]-() DELETE r")
                
                print(f"[ACTION] Deleting pattern extraction nodes...")
                # Delete nodes with filtered labels
                session.run(f"MATCH (n:{labels_str}) DELETE n")
                
                print(f"[OK] Pattern extraction data cleaned from '{db_name}'")
                print(f"[OK] Other project data remains intact")
            except Exception as e:
                print(f"[ERROR] Failed to clean database: {e}")
                raise


def main():
    print("="*60)
    print("Selective Neo4j Migration: Pattern Extraction Data Only")
    print("="*60)
    print("\nThis migration will move ONLY pattern extraction data:")
    print(f"  - Labels: {', '.join(PATTERN_EXTRACTION_LABELS)}")
    print(f"  - From: '{SOURCE_DB}' database")
    print(f"  - To: '{TARGET_DB}' database")
    print(f"\nOther project data will remain in '{SOURCE_DB}'")
    print("="*60)
    
    # Initialize connection
    migration = Neo4jSelectiveMigration(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    
    try:
        # Step 1: Show source database statistics
        print(f"\n[STEP 1] Analyzing '{SOURCE_DB}' database...")
        all_stats = migration.get_statistics(SOURCE_DB)
        pattern_stats = migration.get_statistics(SOURCE_DB, PATTERN_EXTRACTION_LABELS)
        
        if all_stats:
            print(f"\nAll Data in '{SOURCE_DB}':")
            print(f"  Nodes: {all_stats['nodes']}")
            print(f"  Relationships: {all_stats['relationships']}")
            print(f"  Labels: {', '.join(all_stats['labels']) if all_stats['labels'] else 'None'}")
            
            print(f"\nPattern Extraction Data Only:")
            print(f"  Nodes: {pattern_stats['nodes']}")
            print(f"  Relationships: {pattern_stats['relationships']}")
            
            other_nodes = all_stats['nodes'] - pattern_stats['nodes']
            print(f"\nOther Project Data (will remain in '{SOURCE_DB}'):")
            print(f"  Nodes: {other_nodes}")
        
        if pattern_stats['nodes'] == 0:
            print(f"\n[WARNING] No pattern extraction data found in '{SOURCE_DB}'.")
            print("[INFO] Creating target database anyway...")
            migration.create_database(TARGET_DB)
            print("\n[DONE] Target database created. You can now update your .env file.")
            return
        
        # Confirm before proceeding
        print(f"\n{'='*60}")
        response = input("Proceed with selective migration? (yes/no): ")
        if response.lower() != 'yes':
            print("[CANCELLED] Migration cancelled by user")
            return
        
        # Step 2: Create target database
        print(f"\n[STEP 2] Creating target database '{TARGET_DB}'...")
        migration.create_database(TARGET_DB)
        
        # Step 3: Export pattern extraction data only
        print(f"\n[STEP 3] Exporting pattern extraction data from '{SOURCE_DB}'...")
        data = migration.export_selective_data(SOURCE_DB, PATTERN_EXTRACTION_LABELS)
        
        # Step 4: Import data to target
        print(f"\n[STEP 4] Importing data to '{TARGET_DB}'...")
        migration.import_data(TARGET_DB, data)
        
        # Step 5: Verify migration
        print(f"\n[STEP 5] Verifying migration...")
        target_stats = migration.get_statistics(TARGET_DB)
        if target_stats:
            print(f"\nTarget Database '{TARGET_DB}' Statistics:")
            print(f"  Nodes: {target_stats['nodes']}")
            print(f"  Relationships: {target_stats['relationships']}")
            
            # Compare
            if (pattern_stats['nodes'] == target_stats['nodes'] and 
                pattern_stats['relationships'] == target_stats['relationships']):
                print("\n[OK] Migration verified successfully!")
            else:
                print("\n[ERROR] Migration verification failed! Counts don't match.")
                print(f"Expected: {pattern_stats['nodes']} nodes, {pattern_stats['relationships']} relationships")
                print(f"Got: {target_stats['nodes']} nodes, {target_stats['relationships']} relationships")
                print("[WARNING] Please check the data manually before proceeding.")
                return
        
        # Step 6: Clean pattern extraction data from source
        print(f"\n[STEP 6] Cleaning pattern extraction data from '{SOURCE_DB}'...")
        migration.delete_selective_data(SOURCE_DB, PATTERN_EXTRACTION_LABELS)
        
        # Final verification
        print(f"\n[STEP 7] Final verification...")
        final_source_stats = migration.get_statistics(SOURCE_DB)
        print(f"\nSource Database '{SOURCE_DB}' after cleanup:")
        print(f"  Remaining nodes: {final_source_stats['nodes']}")
        print(f"  Remaining relationships: {final_source_stats['relationships']}")
        print(f"  Remaining labels: {', '.join(final_source_stats['labels']) if final_source_stats['labels'] else 'None'}")
        
        print("\n" + "="*60)
        print("Selective migration completed successfully!")
        print("="*60)
        print("\nWhat happened:")
        print(f"  - Moved {pattern_stats['nodes']} pattern extraction nodes to '{TARGET_DB}'")
        print(f"  - Moved {pattern_stats['relationships']} relationships to '{TARGET_DB}'")
        print(f"  - Left {final_source_stats['nodes']} other project nodes in '{SOURCE_DB}'")
        print("\nNext steps:")
        print(f"1. Update your .env file:")
        print(f"   Change: NEO4J_DATABASE=patterns")
        print(f"   To:     NEO4J_DATABASE=specengine")
        print(f"2. Restart any running services that use the database")
        print(f"3. Verify your application works with the new database")
        print(f"\nThe '{SOURCE_DB}' database now contains only the other project's data.")
        
    except Exception as e:
        print(f"\n[ERROR] Migration failed: {e}")
        sys.exit(1)
    finally:
        migration.close()


if __name__ == "__main__":
    main()
