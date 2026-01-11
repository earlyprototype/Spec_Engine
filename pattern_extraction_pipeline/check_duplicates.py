# check_duplicates.py
# Check for existing duplicate patterns before implementing constraint

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(override=True)

def check_duplicates():
    """Check for duplicate patterns in Neo4j."""
    
    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
    )
    
    print("\n" + "="*70)
    print("CHECKING FOR DUPLICATE PATTERNS")
    print("="*70)
    
    with driver.session() as session:
        # Check for duplicates
        result = session.run("""
            MATCH (p:Pattern)
            WITH p.source_repo as repo, count(*) as cnt
            WHERE cnt > 1
            RETURN repo, cnt
            ORDER BY cnt DESC
        """)
        
        duplicates = list(result)
        
        if duplicates:
            print(f"\n[WARNING] Found {len(duplicates)} repositories with duplicate patterns:")
            for i, record in enumerate(duplicates[:10], 1):
                print(f"  {i}. {record['repo']}: {record['cnt']} duplicates")
            if len(duplicates) > 10:
                print(f"  ... and {len(duplicates) - 10} more")
            
            total_duplicates = sum(r['cnt'] - 1 for r in duplicates)
            print(f"\nTotal duplicate nodes: {total_duplicates}")
            print("\n[ACTION REQUIRED] Run cleanup script before adding constraint:")
            print("  python pattern_extraction_pipeline/setup_data_quality.py")
            return False
        else:
            print("\n[OK] No duplicate patterns found")
            print("Safe to add uniqueness constraint")
            return True
        
        # Get total pattern count
        count_result = session.run("MATCH (p:Pattern) RETURN count(p) as total")
        total = count_result.single()['total']
        print(f"\nTotal patterns in database: {total}")
    
    driver.close()

if __name__ == "__main__":
    clean = check_duplicates()
    exit(0 if clean else 1)
