"""
Check what databases exist in Neo4j and their contents
"""

import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USER = os.getenv('NEO4J_USER')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

def check_databases():
    print("="*60)
    print("Neo4j Database Discovery")
    print("="*60)
    print(f"\nConnection: {NEO4J_URI}")
    print(f"User: {NEO4J_USER}")
    print()
    
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    try:
        # List all databases
        with driver.session(database="system") as session:
            print("[STEP 1] Listing all databases...")
            result = session.run("SHOW DATABASES")
            databases = []
            
            print("\nAvailable Databases:")
            print("-" * 60)
            for record in result:
                db_name = record["name"]
                status = record.get("currentStatus", "unknown")
                databases.append(db_name)
                print(f"  - {db_name} (status: {status})")
            print()
        
        # Check contents of each database
        print("[STEP 2] Checking database contents...")
        print("-" * 60)
        
        for db_name in databases:
            if db_name == "system":
                continue  # Skip system database
                
            try:
                with driver.session(database=db_name) as session:
                    # Count nodes
                    node_result = session.run("MATCH (n) RETURN count(n) as count")
                    node_count = node_result.single()["count"]
                    
                    # Count relationships
                    rel_result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
                    rel_count = rel_result.single()["count"]
                    
                    print(f"\nDatabase: {db_name}")
                    print(f"  Nodes: {node_count}")
                    print(f"  Relationships: {rel_count}")
                    
                    if node_count > 0:
                        # Get node labels
                        label_result = session.run("CALL db.labels()")
                        labels = [record["label"] for record in label_result]
                        print(f"  Labels: {', '.join(labels) if labels else 'None'}")
                        
                        # Get relationship types
                        type_result = session.run("CALL db.relationshipTypes()")
                        rel_types = [record["relationshipType"] for record in type_result]
                        print(f"  Relationship Types: {', '.join(rel_types) if rel_types else 'None'}")
                        
            except Exception as e:
                print(f"\nDatabase: {db_name}")
                print(f"  Error: {e}")
        
        print()
        print("="*60)
        print("Recommendations:")
        print("="*60)
        
        # Find database with data
        data_found = False
        for db_name in databases:
            if db_name == "system":
                continue
            try:
                with driver.session(database=db_name) as session:
                    node_result = session.run("MATCH (n) RETURN count(n) as count")
                    node_count = node_result.single()["count"]
                    if node_count > 0:
                        data_found = True
                        print(f"\n  Data found in '{db_name}' database")
                        print(f"  If this is your pattern extraction data, you should:")
                        print(f"    1. Update .env to: NEO4J_DATABASE={db_name}")
                        print(f"    OR")
                        print(f"    2. Migrate from '{db_name}' to 'specengine'")
            except:
                pass
        
        if not data_found:
            print("\n  No data found in any database")
            print(f"  This is a fresh Neo4j instance")
            print(f"  You can:")
            print(f"    1. Create the 'specengine' database and start fresh")
            print(f"    2. Update .env to: NEO4J_DATABASE=specengine")
        
        print()
        
    finally:
        driver.close()

if __name__ == "__main__":
    check_databases()
