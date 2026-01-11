#!/usr/bin/env python3
"""Quick script to count repos in the database"""

from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv('NEO4J_URI', 'bolt://localhost:7687'),
    auth=(os.getenv('NEO4J_USER', 'neo4j'), os.getenv('NEO4J_PASSWORD', 'password'))
)

with driver.session() as session:
    result = session.run("""
        MATCH (p:Pattern)
        RETURN count(p) AS total_patterns,
               count(DISTINCT p.source_repo) AS unique_repos
    """)
    
    record = result.single()
    print(f"\n{'='*50}")
    print(f"DATABASE STATISTICS")
    print(f"{'='*50}")
    print(f"Total Pattern nodes: {record['total_patterns']}")
    print(f"Unique repositories: {record['unique_repos']}")
    print(f"{'='*50}\n")

driver.close()
