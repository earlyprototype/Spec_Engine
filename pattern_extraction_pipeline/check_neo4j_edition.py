"""
Check Neo4j Edition and Version
"""

import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USER = os.getenv('NEO4J_USER')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

try:
    with driver.session(database="system") as session:
        # Get version and edition info
        result = session.run("CALL dbms.components() YIELD name, versions, edition")
        
        print("="*60)
        print("Neo4j Instance Information")
        print("="*60)
        
        for record in result:
            print(f"\nComponent: {record['name']}")
            print(f"Version: {', '.join(record['versions'])}")
            print(f"Edition: {record['edition']}")
        
        print("\n" + "="*60)
        
        # Check if multiple databases are supported
        try:
            result = session.run("SHOW DATABASES")
            db_count = len(list(result))
            print(f"\nMultiple databases supported: YES")
            print(f"Current database count: {db_count}")
        except Exception as e:
            print(f"\nMultiple databases supported: NO")
            print(f"Reason: Community Edition only supports one database")
            
        print("="*60)
        
finally:
    driver.close()
