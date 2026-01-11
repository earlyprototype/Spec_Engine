#!/usr/bin/env python3
"""
Property Normalization Migration Script

This script performs two operations:
1. Renames IDERule.quality_score to IDERule.repo_quality_score
2. Scales Pattern.quality_score from 0-1 to 0-100

Run this ONCE after updating code to use new property names.
"""

import os
import sys
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()


class PropertyNormalizer:
    """Normalize quality properties in Neo4j"""
    
    def __init__(self):
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD")
        
        if not password:
            raise ValueError("NEO4J_PASSWORD not found in environment")
        
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        print(f"Connected to Neo4j at {uri}")
    
    def close(self):
        self.driver.close()
    
    def analyze_current_state(self):
        """Analyze current property state before migration"""
        print("\n=== Current State Analysis ===\n")
        
        with self.driver.session() as session:
            # Check IDERule nodes
            result = session.run("""
                MATCH (r:IDERule)
                RETURN 
                    count(r) AS total_rules,
                    sum(CASE WHEN r.quality_score IS NOT NULL THEN 1 ELSE 0 END) AS with_quality_score,
                    sum(CASE WHEN r.repo_quality_score IS NOT NULL THEN 1 ELSE 0 END) AS with_repo_quality_score,
                    avg(r.quality_score) AS avg_old_quality,
                    avg(r.repo_quality_score) AS avg_new_quality
            """)
            
            rule_stats = result.single()
            if rule_stats:
                print("IDERule Nodes:")
                print(f"  Total: {rule_stats['total_rules']}")
                print(f"  With quality_score: {rule_stats['with_quality_score']}")
                print(f"  With repo_quality_score: {rule_stats['with_repo_quality_score']}")
                if rule_stats['avg_old_quality']:
                    print(f"  Avg quality_score: {rule_stats['avg_old_quality']:.2f}")
                if rule_stats['avg_new_quality']:
                    print(f"  Avg repo_quality_score: {rule_stats['avg_new_quality']:.2f}")
            
            # Check Pattern nodes
            result = session.run("""
                MATCH (p:Pattern)
                RETURN 
                    count(p) AS total_patterns,
                    sum(CASE WHEN p.quality_score IS NOT NULL THEN 1 ELSE 0 END) AS with_quality,
                    avg(p.quality_score) AS avg_quality,
                    min(p.quality_score) AS min_quality,
                    max(p.quality_score) AS max_quality
            """)
            
            pattern_stats = result.single()
            if pattern_stats:
                print("\nPattern Nodes:")
                print(f"  Total: {pattern_stats['total_patterns']}")
                print(f"  With quality_score: {pattern_stats['with_quality']}")
                if pattern_stats['avg_quality']:
                    print(f"  Avg quality_score: {pattern_stats['avg_quality']:.4f}")
                    print(f"  Min quality_score: {pattern_stats['min_quality']:.4f}")
                    print(f"  Max quality_score: {pattern_stats['max_quality']:.4f}")
                    
                    # Detect scale
                    if pattern_stats['max_quality'] and pattern_stats['max_quality'] <= 1.0:
                        print("  Scale: 0-1 (needs scaling)")
                    elif pattern_stats['max_quality'] and pattern_stats['max_quality'] > 1.0:
                        print("  Scale: 0-100 (already scaled)")
    
    def rename_iderule_property(self, dry_run=True):
        """Rename IDERule.quality_score to IDERule.repo_quality_score"""
        print(f"\n=== {'DRY RUN: ' if dry_run else ''}Renaming IDERule.quality_score ===\n")
        
        with self.driver.session() as session:
            # Find nodes to update
            result = session.run("""
                MATCH (r:IDERule)
                WHERE r.quality_score IS NOT NULL 
                  AND r.repo_quality_score IS NULL
                RETURN count(r) AS count_to_update
            """)
            
            count_record = result.single()
            count = count_record['count_to_update'] if count_record else 0
            
            print(f"Found {count} IDERule nodes to update")
            
            if count == 0:
                print("No updates needed (already migrated or no quality_score data)")
                return 0
            
            if dry_run:
                print("Dry run complete. Run with --execute to apply changes.")
                return count
            
            # Perform rename
            result = session.run("""
                MATCH (r:IDERule)
                WHERE r.quality_score IS NOT NULL 
                  AND r.repo_quality_score IS NULL
                SET r.repo_quality_score = r.quality_score
                REMOVE r.quality_score
                RETURN count(r) AS updated
            """)
            
            updated = result.single()['updated']
            print(f"Updated {updated} IDERule nodes")
            return updated
    
    def scale_pattern_quality(self, dry_run=True):
        """Scale Pattern.quality_score from 0-1 to 0-100"""
        print(f"\n=== {'DRY RUN: ' if dry_run else ''}Scaling Pattern.quality_score ===\n")
        
        with self.driver.session() as session:
            # Find nodes to update (quality_score < 2 means it's on 0-1 scale)
            result = session.run("""
                MATCH (p:Pattern)
                WHERE p.quality_score IS NOT NULL 
                  AND p.quality_score < 2
                RETURN count(p) AS count_to_update,
                       avg(p.quality_score) AS avg_before
            """)
            
            stats = result.single()
            count = stats['count_to_update'] if stats else 0
            avg_before = stats['avg_before'] if stats else 0
            
            print(f"Found {count} Pattern nodes to scale")
            if avg_before:
                print(f"Current avg: {avg_before:.4f} (0-1 scale)")
                print(f"Will become: {avg_before * 100:.2f} (0-100 scale)")
            
            if count == 0:
                print("No updates needed (already scaled or no quality_score data)")
                return 0
            
            if dry_run:
                print("Dry run complete. Run with --execute to apply changes.")
                return count
            
            # Perform scaling (multiply by 100, also scale component scores)
            result = session.run("""
                MATCH (p:Pattern)
                WHERE p.quality_score IS NOT NULL 
                  AND p.quality_score < 2
                SET p.quality_score = p.quality_score * 100,
                    p.freshness_score = COALESCE(p.freshness_score, 0) * 100,
                    p.maintenance_score = COALESCE(p.maintenance_score, 0) * 100
                RETURN count(p) AS updated,
                       avg(p.quality_score) AS avg_after
            """)
            
            result_data = result.single()
            updated = result_data['updated']
            avg_after = result_data['avg_after']
            
            print(f"Updated {updated} Pattern nodes")
            print(f"New avg: {avg_after:.2f} (0-100 scale)")
            return updated
    
    def verify_migration(self):
        """Verify migration completed successfully"""
        print("\n=== Verification ===\n")
        
        with self.driver.session() as session:
            # Check IDERule migration
            result = session.run("""
                MATCH (r:IDERule)
                RETURN 
                    count(r) AS total,
                    sum(CASE WHEN r.quality_score IS NOT NULL THEN 1 ELSE 0 END) AS with_old_prop,
                    sum(CASE WHEN r.repo_quality_score IS NOT NULL THEN 1 ELSE 0 END) AS with_new_prop
            """)
            
            rule_stats = result.single()
            if rule_stats:
                print("IDERule Status:")
                print(f"  Total: {rule_stats['total']}")
                print(f"  Still has quality_score: {rule_stats['with_old_prop']}")
                print(f"  Has repo_quality_score: {rule_stats['with_new_prop']}")
                
                if rule_stats['with_old_prop'] > 0:
                    print("  WARNING: Some nodes still have old property!")
                else:
                    print("  SUCCESS: All nodes migrated to repo_quality_score")
            
            # Check Pattern migration
            result = session.run("""
                MATCH (p:Pattern)
                WHERE p.quality_score IS NOT NULL
                RETURN 
                    count(p) AS total,
                    sum(CASE WHEN p.quality_score < 2 THEN 1 ELSE 0 END) AS still_0_1_scale,
                    sum(CASE WHEN p.quality_score >= 2 THEN 1 ELSE 0 END) AS on_0_100_scale,
                    avg(p.quality_score) AS avg_quality
            """)
            
            pattern_stats = result.single()
            if pattern_stats:
                print("\nPattern Status:")
                print(f"  Total: {pattern_stats['total']}")
                print(f"  Still 0-1 scale: {pattern_stats['still_0_1_scale']}")
                print(f"  On 0-100 scale: {pattern_stats['on_0_100_scale']}")
                print(f"  Avg quality: {pattern_stats['avg_quality']:.2f}")
                
                if pattern_stats['still_0_1_scale'] > 0:
                    print("  WARNING: Some nodes still on 0-1 scale!")
                else:
                    print("  SUCCESS: All nodes on 0-100 scale")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Normalize quality properties in Neo4j")
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Execute the migration (default is dry run)'
    )
    parser.add_argument(
        '--skip-iderule',
        action='store_true',
        help='Skip IDERule property rename'
    )
    parser.add_argument(
        '--skip-pattern',
        action='store_true',
        help='Skip Pattern quality scaling'
    )
    
    args = parser.parse_args()
    
    dry_run = not args.execute
    
    print("=" * 60)
    print("Property Normalization Migration")
    print("=" * 60)
    
    if dry_run:
        print("\nRUNNING IN DRY RUN MODE")
        print("No changes will be made to the database")
        print("Run with --execute to apply changes\n")
    else:
        print("\nEXECUTING MIGRATION")
        print("Changes will be applied to the database\n")
        
        response = input("Are you sure? Type 'yes' to continue: ")
        if response.lower() != 'yes':
            print("Migration cancelled")
            return
    
    normalizer = PropertyNormalizer()
    
    try:
        # Analyze current state
        normalizer.analyze_current_state()
        
        # Perform migrations
        if not args.skip_iderule:
            normalizer.rename_iderule_property(dry_run=dry_run)
        
        if not args.skip_pattern:
            normalizer.scale_pattern_quality(dry_run=dry_run)
        
        # Verify if executed
        if not dry_run:
            normalizer.verify_migration()
            print("\n" + "=" * 60)
            print("Migration complete!")
            print("=" * 60)
        
    finally:
        normalizer.close()


if __name__ == "__main__":
    main()
