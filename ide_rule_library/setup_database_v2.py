#!/usr/bin/env python3
"""
Enhanced Neo4j database setup with quality scoring support.

This adds indexes and schema for the enhanced quality system.
"""

from neo4j import GraphDatabase
import os
import sys
from dotenv import load_dotenv


def setup_enhanced_database():
    """Create enhanced Neo4j schema with quality metrics support"""
    
    load_dotenv(override=True)
    
    print("\n" + "="*60)
    print("IDE RULE LIBRARY - ENHANCED DATABASE SETUP")
    print("="*60 + "\n")
    
    # Connect to Neo4j
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    
    print(f"Connecting to Neo4j at {uri}...")
    
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        
        with driver.session() as session:
            # Test connection
            result = session.run("RETURN 1 AS test")
            result.single()
            print("[OK] Connected to Neo4j\n")
            
            # Run base setup first (vector index, basic constraints)
            print("Setting up base schema...")
            run_base_setup(session)
            
            # Add quality scoring indexes
            print("\n" + "="*60)
            print("ENHANCED QUALITY INDEXES")
            print("="*60 + "\n")
            
            # Index on quality_score for fast filtering
            print("Creating index on quality_score...")
            try:
                session.run("""
                    CREATE INDEX ide_rule_quality_score IF NOT EXISTS
                    FOR (r:IDERule) ON (r.quality_score)
                """)
                print("[OK] Index 'ide_rule_quality_score' created")
            except Exception as e:
                if "equivalent index already exists" in str(e).lower():
                    print("[OK] Index 'ide_rule_quality_score' already exists")
                else:
                    raise
            
            # Index on confidence_level for filtering
            print("\nCreating index on confidence_level...")
            try:
                session.run("""
                    CREATE INDEX ide_rule_confidence IF NOT EXISTS
                    FOR (r:IDERule) ON (r.confidence_level)
                """)
                print("[OK] Index 'ide_rule_confidence' created")
            except Exception as e:
                if "equivalent index already exists" in str(e).lower():
                    print("[OK] Index 'ide_rule_confidence' already exists")
                else:
                    raise
            
            # Index on days_since_update for freshness queries
            print("\nCreating index on days_since_update...")
            try:
                session.run("""
                    CREATE INDEX ide_rule_freshness IF NOT EXISTS
                    FOR (r:IDERule) ON (r.days_since_update)
                """)
                print("[OK] Index 'ide_rule_freshness' created")
            except Exception as e:
                if "equivalent index already exists" in str(e).lower():
                    print("[OK] Index 'ide_rule_freshness' already exists")
                else:
                    raise
            
            # Check existing IDERule nodes and show stats
            print("\n" + "="*60)
            print("DATABASE STATISTICS")
            print("="*60 + "\n")
            
            result = session.run("""
                MATCH (r:IDERule)
                RETURN count(r) AS total,
                       avg(r.quality_score) AS avg_quality,
                       max(r.quality_score) AS max_quality,
                       min(r.quality_score) AS min_quality
            """)
            stats = result.single()
            
            if stats and stats['total'] > 0:
                print(f"Total IDERule nodes:    {stats['total']}")
                if stats['avg_quality'] is not None:
                    print(f"Average quality score:  {stats['avg_quality']:.2f}/100")
                    print(f"Highest quality score:  {stats['max_quality']:.2f}/100")
                    print(f"Lowest quality score:   {stats['min_quality']:.2f}/100")
                else:
                    print("Quality scores not yet calculated (run re-extraction)")
            else:
                print("No IDERule nodes found yet")
            
            # Show production signal coverage
            result = session.run("""
                MATCH (r:IDERule)
                WHERE r.has_ci_cd IS NOT NULL
                RETURN sum(CASE WHEN r.has_ci_cd THEN 1 ELSE 0 END) AS with_ci_cd,
                       sum(CASE WHEN r.has_tests THEN 1 ELSE 0 END) AS with_tests,
                       sum(CASE WHEN r.has_deployment THEN 1 ELSE 0 END) AS with_deployment,
                       sum(CASE WHEN r.confidence_level >= 4 THEN 1 ELSE 0 END) AS high_confidence,
                       count(r) AS total
            """)
            prod_stats = result.single()
            
            if prod_stats and prod_stats['total'] > 0:
                print(f"\nProduction Signal Coverage:")
                print(f"  With CI/CD:        {prod_stats['with_ci_cd']}/{prod_stats['total']}")
                print(f"  With Tests:        {prod_stats['with_tests']}/{prod_stats['total']}")
                print(f"  With Deployment:   {prod_stats['with_deployment']}/{prod_stats['total']}")
                print(f"  High Confidence:   {prod_stats['high_confidence']}/{prod_stats['total']}")
        
        driver.close()
        
        print("\n" + "="*60)
        print("ENHANCED DATABASE SETUP COMPLETE")
        print("="*60)
        print("\nTo update existing rules with quality scores:")
        print("  python update_quality_scores.py")
        print("\nTo extract new rules with enhanced quality:")
        print("  python scan_existing_patterns.py --extract\n")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error setting up database: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_base_setup(session):
    """Run the base database setup (from original setup_database.py)"""
    
    # Create vector index for semantic search
    print("Creating vector index for semantic search...")
    try:
        session.run("""
            CREATE VECTOR INDEX ide_rule_embeddings IF NOT EXISTS
            FOR (r:IDERule) ON (r.embedding)
            OPTIONS {indexConfig: {
                `vector.dimensions`: 768,
                `vector.similarity_function`: 'cosine'
            }}
        """)
        print("[OK] Vector index 'ide_rule_embeddings' created")
    except Exception as e:
        if "equivalent index already exists" in str(e).lower():
            print("[OK] Vector index 'ide_rule_embeddings' already exists")
        else:
            raise
    
    # Create text index for source_repo
    print("\nCreating text index on source_repo...")
    try:
        session.run("""
            CREATE INDEX ide_rule_repo IF NOT EXISTS
            FOR (r:IDERule) ON (r.source_repo)
        """)
        print("[OK] Index 'ide_rule_repo' created")
    except Exception as e:
        if "equivalent index already exists" in str(e).lower():
            print("[OK] Index 'ide_rule_repo' already exists")
        else:
            raise
    
    # Create text index for file_format
    print("\nCreating text index on file_format...")
    try:
        session.run("""
            CREATE INDEX ide_rule_format IF NOT EXISTS
            FOR (r:IDERule) ON (r.file_format)
        """)
        print("[OK] Index 'ide_rule_format' created")
    except Exception as e:
        if "equivalent index already exists" in str(e).lower():
            print("[OK] Index 'ide_rule_format' already exists")
        else:
            raise
    
    # Create text index for content_hash
    print("\nCreating text index on content_hash...")
    try:
        session.run("""
            CREATE INDEX ide_rule_hash IF NOT EXISTS
            FOR (r:IDERule) ON (r.content_hash)
        """)
        print("[OK] Index 'ide_rule_hash' created")
    except Exception as e:
        if "equivalent index already exists" in str(e).lower():
            print("[OK] Index 'ide_rule_hash' already exists")
        else:
            raise
    
    # Create constraint for unique rule IDs
    print("\nCreating uniqueness constraint on rule ID...")
    try:
        session.run("""
            CREATE CONSTRAINT ide_rule_id IF NOT EXISTS
            FOR (r:IDERule) REQUIRE r.id IS UNIQUE
        """)
        print("[OK] Constraint 'ide_rule_id' created")
    except Exception as e:
        if "equivalent constraint already exists" in str(e).lower():
            print("[OK] Constraint 'ide_rule_id' already exists")
        else:
            raise


if __name__ == '__main__':
    success = setup_enhanced_database()
    sys.exit(0 if success else 1)
