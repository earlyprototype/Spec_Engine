# setup_data_quality.py
# Establish data quality constraints and clean existing duplicates

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

def setup_constraints_and_cleanup():
    """Create unique constraints and merge duplicate nodes."""
    
    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
    )
    
    with driver.session() as session:
        print("\n=== Step 1: Creating Unique Constraints ===")
        
        # Create unique constraint for Technology names
        try:
            session.run("CREATE CONSTRAINT tech_unique IF NOT EXISTS FOR (t:Technology) REQUIRE t.name IS UNIQUE")
            print("[OK] Technology.name unique constraint created")
        except Exception as e:
            print(f"[WARN] Technology constraint: {e}")
        
        # Create unique constraint for Constraint rules
        try:
            session.run("CREATE CONSTRAINT constraint_unique IF NOT EXISTS FOR (c:Constraint) REQUIRE c.rule IS UNIQUE")
            print("[OK] Constraint.rule unique constraint created")
        except Exception as e:
            print(f"[WARN] Constraint constraint: {e}")
        
        print("\n=== Step 2: Finding Duplicates ===")
        
        # Find duplicate technologies (case-insensitive)
        result = session.run("""
            MATCH (t:Technology)
            WITH toLower(t.name) AS normalized_name, collect(t) AS nodes
            WHERE size(nodes) > 1
            RETURN normalized_name, size(nodes) AS duplicate_count, 
                   [n IN nodes | n.name] AS duplicate_names
        """)
        
        duplicates = list(result)
        if duplicates:
            print(f"Found {len(duplicates)} duplicate technology groups:")
            for record in duplicates:
                print(f"  - {record['duplicate_names']} ({record['duplicate_count']} nodes)")
        else:
            print("No technology duplicates found")
        
        # Find duplicate constraints
        result = session.run("""
            MATCH (c:Constraint)
            WITH toLower(c.rule) AS normalized_rule, collect(c) AS nodes
            WHERE size(nodes) > 1
            RETURN normalized_rule, size(nodes) AS duplicate_count,
                   [n IN nodes | n.rule] AS duplicate_names
        """)
        
        duplicates = list(result)
        if duplicates:
            print(f"Found {len(duplicates)} duplicate constraint groups:")
            for record in duplicates:
                print(f"  - {record['duplicate_names']} ({record['duplicate_count']} nodes)")
        else:
            print("No constraint duplicates found")
        
        print("\n=== Step 3: Merging Duplicate Technologies ===")
        
        # Get all duplicate groups
        dup_groups = session.run("""
            MATCH (t:Technology)
            WITH toLower(t.name) AS normalized_name, collect(t) AS nodes
            WHERE size(nodes) > 1
            RETURN normalized_name, nodes
        """)
        
        merged_count = 0
        for group in dup_groups:
            nodes = group['nodes']
            primary = nodes[0]
            duplicates = nodes[1:]
            
            for dup in duplicates:
                # Transfer relationships manually
                session.run("""
                    MATCH (dup) WHERE elementId(dup) = $dup_id
                    MATCH (primary) WHERE elementId(primary) = $primary_id
                    OPTIONAL MATCH (p:Pattern)-[r:USES]->(dup)
                    WITH dup, primary, p, r
                    WHERE p IS NOT NULL
                    MERGE (p)-[new:USES]->(primary)
                    ON CREATE SET new.role = r.role
                    DELETE r
                """, dup_id=dup.element_id, primary_id=primary.element_id)
                
                # Delete duplicate
                session.run("""
                    MATCH (dup) WHERE elementId(dup) = $dup_id
                    DETACH DELETE dup
                """, dup_id=dup.element_id)
                
                merged_count += 1
        
        print(f"[OK] Merged {merged_count} duplicate technology nodes")
        
        print("\n=== Step 4: Merging Duplicate Constraints ===")
        
        # Get all duplicate groups
        dup_groups = session.run("""
            MATCH (c:Constraint)
            WITH toLower(c.rule) AS normalized_rule, collect(c) AS nodes
            WHERE size(nodes) > 1
            RETURN normalized_rule, nodes
        """)
        
        merged_count = 0
        for group in dup_groups:
            nodes = group['nodes']
            primary = nodes[0]
            duplicates = nodes[1:]
            
            for dup in duplicates:
                # Transfer relationships manually
                session.run("""
                    MATCH (dup) WHERE elementId(dup) = $dup_id
                    MATCH (primary) WHERE elementId(primary) = $primary_id
                    OPTIONAL MATCH (p:Pattern)-[r:REQUIRES]->(dup)
                    WITH dup, primary, p, r
                    WHERE p IS NOT NULL
                    MERGE (p)-[:REQUIRES]->(primary)
                    DELETE r
                """, dup_id=dup.element_id, primary_id=primary.element_id)
                
                # Delete duplicate
                session.run("""
                    MATCH (dup) WHERE elementId(dup) = $dup_id
                    DETACH DELETE dup
                """, dup_id=dup.element_id)
                
                merged_count += 1
        
        print(f"[OK] Merged {merged_count} duplicate constraint nodes")
        
        print("\n=== Step 5: Normalizing Existing Data ===")
        
        # Normalize all technology names to lowercase
        result = session.run("""
            MATCH (t:Technology)
            WHERE t.name <> toLower(t.name)
            SET t.name = toLower(t.name)
            RETURN count(t) AS normalized_count
        """)
        
        normalized = list(result)
        if normalized and normalized[0]['normalized_count'] > 0:
            print(f"[OK] Normalized {normalized[0]['normalized_count']} technology names")
        else:
            print("[OK] All technology names already normalized")
        
        # Normalize all constraint rules
        result = session.run("""
            MATCH (c:Constraint)
            WHERE c.rule <> toLower(replace(c.rule, ' ', '_'))
            SET c.rule = toLower(replace(c.rule, ' ', '_'))
            RETURN count(c) AS normalized_count
        """)
        
        normalized = list(result)
        if normalized and normalized[0]['normalized_count'] > 0:
            print(f"[OK] Normalized {normalized[0]['normalized_count']} constraint rules")
        else:
            print("[OK] All constraint rules already normalized")
        
        print("\n=== Step 6: Removing Duplicate Relationships ===")
        
        # Remove duplicate USES relationships
        result = session.run("""
            MATCH (p:Pattern)-[r:USES]->(t:Technology)
            WITH p, t, collect(r) AS rels
            WHERE size(rels) > 1
            FOREACH (rel IN tail(rels) | DELETE rel)
            RETURN count(p) AS cleaned_patterns
        """)
        
        cleaned = list(result)
        if cleaned and cleaned[0]['cleaned_patterns'] > 0:
            print(f"[OK] Removed duplicate USES relationships for {cleaned[0]['cleaned_patterns']} patterns")
        else:
            print("[OK] No duplicate USES relationships found")
        
        print("\n=== Data Quality Setup Complete ===")
        print("\nFuture extractions will automatically:")
        print("  1. Normalize all technology names to lowercase")
        print("  2. Normalize all constraint rules to lowercase_snake_case")
        print("  3. Prevent duplicate nodes via unique constraints")
        print("  4. Prevent duplicate relationships via MERGE")
    
    driver.close()

if __name__ == "__main__":
    setup_constraints_and_cleanup()
