#!/usr/bin/env python3
"""
Migrate existing IDERule nodes to add quality scores.

Backfills quality data for all existing rules in the database by:
1. Fetching all IDERule nodes without repo_quality_score
2. Getting parent Pattern node for repo metadata
3. Calculating quality scores using quality_scorer
4. Updating Neo4j nodes with quality fields

Includes progress tracking, checkpointing, and resume capability.
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv
from neo4j import GraphDatabase
import yaml

from ide_rule_library.quality_scorer import RepoQualityScorer, enhance_repo_metadata
from ide_rule_library.logger import StructuredLogger
from ide_rule_library.exceptions import (
    MigrationError,
    CheckpointError,
    DatabaseError,
    MissingDataError
)

load_dotenv(override=True)


class QualityScoreMigration:
    """Migrate existing rules to add quality scores"""
    
    def __init__(self, neo4j_driver, logger, checkpoint_file: str = 'migration_checkpoint.json'):
        self.driver = neo4j_driver
        self.logger = logger
        self.scorer = RepoQualityScorer()
        self.checkpoint_file = Path(checkpoint_file)
        self.stats = {
            'total_rules': 0,
            'migrated': 0,
            'skipped': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }
    
    def load_checkpoint(self) -> Dict:
        """Load checkpoint data to resume migration"""
        if not self.checkpoint_file.exists():
            return {'processed_ids': [], 'last_update': None}
        
        try:
            with open(self.checkpoint_file) as f:
                checkpoint = json.load(f)
            self.logger.info(f"Loaded checkpoint: {len(checkpoint['processed_ids'])} rules already processed")
            return checkpoint
        except Exception as e:
            self.logger.warning(f"Failed to load checkpoint: {e}")
            return {'processed_ids': [], 'last_update': None}
    
    def save_checkpoint(self, processed_ids: List[str]):
        """Save checkpoint for resume capability"""
        try:
            checkpoint = {
                'processed_ids': processed_ids,
                'last_update': datetime.utcnow().isoformat(),
                'stats': self.stats
            }
            
            self.checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.checkpoint_file, 'w') as f:
                json.dump(checkpoint, f, indent=2)
            
            self.logger.debug(f"Checkpoint saved: {len(processed_ids)} rules processed")
            
        except Exception as e:
            raise CheckpointError(f"Failed to save checkpoint: {e}") from e
    
    def get_rules_to_migrate(self) -> List[Dict]:
        """
        Get all IDERule nodes that need quality scores.
        
        Returns:
            List of rule dictionaries with id and basic metadata
        """
        with self.driver.session() as session:
            try:
                # Get rules without quality_score
                result = session.run("""
                    MATCH (r:IDERule)
                    WHERE r.repo_quality_score IS NULL
                    RETURN r.id AS id,
                           r.source_repo AS source_repo,
                           r.file_path AS file_path,
                           r.stars AS stars
                    ORDER BY r.id
                """)
                
                rules = [dict(record) for record in result]
                self.logger.info(f"Found {len(rules)} rules needing quality scores")
                return rules
                
            except Exception as e:
                raise DatabaseError(f"Failed to fetch rules: {e}") from e
    
    def get_repo_metadata(self, rule_id: str) -> Dict:
        """
        Get repository metadata from Pattern node.
        
        Args:
            rule_id: IDERule node ID
            
        Returns:
            Repository metadata dictionary
            
        Raises:
            MissingDataError: If Pattern node not found
        """
        with self.driver.session() as session:
            try:
                result = session.run("""
                    MATCH (r:IDERule {id: $rule_id})<-[:HAS_RULE]-(p:Pattern)
                    RETURN p.repo_name AS name,
                           p.repo_url AS html_url,
                           p.stars AS stars,
                           p.forks AS forks,
                           p.created_at AS created_at,
                           p.updated_at AS updated_at,
                           p.open_issues AS open_issues,
                           p.closed_issues AS closed_issues,
                           p.contributors AS contributors,
                           p.files AS files,
                           p.readme_length AS readme_length
                """, rule_id=rule_id)
                
                record = result.single()
                
                if not record:
                    raise MissingDataError(f"No Pattern node found for rule {rule_id}")
                
                repo_data = dict(record)
                
                # Convert datetime strings if needed
                for date_field in ['created_at', 'updated_at']:
                    if date_field in repo_data and isinstance(repo_data[date_field], str):
                        try:
                            repo_data[date_field] = datetime.fromisoformat(
                                repo_data[date_field].replace('Z', '+00:00')
                            )
                        except (ValueError, AttributeError):
                            self.logger.warning(f"Invalid date format for {date_field}: {repo_data[date_field]}")
                            repo_data[date_field] = None
                
                return repo_data
                
            except Exception as e:
                raise DatabaseError(f"Failed to get repo metadata for {rule_id}: {e}") from e
    
    def update_rule_quality(self, rule_id: str, quality_data: Dict):
        """
        Update IDERule node with quality scores.
        
        Args:
            rule_id: IDERule node ID
            quality_data: Dictionary with quality fields
        """
        with self.driver.session() as session:
            try:
                session.run("""
                    MATCH (r:IDERule {id: $rule_id})
                    SET r.repo_quality_score = $repo_quality_score,
                        r.quality_breakdown = $quality_breakdown,
                        r.confidence_level = $confidence_level,
                        r.has_ci_cd = $has_ci_cd,
                        r.has_deployment = $has_deployment,
                        r.has_tests = $has_tests,
                        r.has_monitoring = $has_monitoring,
                        r.has_security = $has_security,
                        r.production_signals = $production_signals,
                        r.repo_age_days = $repo_age_days,
                        r.days_since_update = $days_since_update,
                        r.contributor_count = $contributor_count,
                        r.quality_migrated_at = datetime()
                """, 
                    rule_id=rule_id,
                    repo_quality_score=quality_data['quality_score'],
                    quality_breakdown=quality_data['quality_breakdown'],
                    confidence_level=quality_data['confidence_level'],
                    has_ci_cd=quality_data['has_ci_cd'],
                    has_deployment=quality_data['has_deployment'],
                    has_tests=quality_data['has_tests'],
                    has_monitoring=quality_data['has_monitoring'],
                    has_security=quality_data['has_security'],
                    production_signals=quality_data['production_signals'],
                    repo_age_days=quality_data.get('repo_age_days', 0),
                    days_since_update=quality_data.get('days_since_update', 999),
                    contributor_count=quality_data.get('contributor_count', 0)
                )
                
            except Exception as e:
                raise DatabaseError(f"Failed to update rule {rule_id}: {e}") from e
    
    def migrate_rule(self, rule: Dict) -> bool:
        """
        Migrate a single rule.
        
        Args:
            rule: Rule dictionary with id and metadata
            
        Returns:
            True if successful, False if skipped
            
        Raises:
            MigrationError: If migration fails
        """
        rule_id = rule['id']
        
        try:
            # Get repo metadata from Pattern node
            repo_data = self.get_repo_metadata(rule_id)
            
            # Calculate quality scores
            enhanced_repo = enhance_repo_metadata(repo_data)
            
            # Extract quality fields
            quality_data = {
                'quality_score': enhanced_repo['quality_score'],
                'quality_breakdown': enhanced_repo['quality_breakdown'],
                'confidence_level': enhanced_repo['confidence_level'],
                'has_ci_cd': enhanced_repo['has_ci_cd'],
                'has_deployment': enhanced_repo['has_deployment'],
                'has_tests': enhanced_repo['has_tests'],
                'has_monitoring': enhanced_repo['has_monitoring'],
                'has_security': enhanced_repo['has_security'],
                'production_signals': enhanced_repo.get('production_signals', {}),
                'repo_age_days': enhanced_repo.get('repo_age_days', 0),
                'days_since_update': enhanced_repo.get('days_since_update', 999),
                'contributor_count': len(enhanced_repo.get('contributors', []))
            }
            
            # Update Neo4j
            self.update_rule_quality(rule_id, quality_data)
            
            self.logger.info(
                f"Migrated {rule_id}: "
                f"quality={quality_data['quality_score']:.1f}, "
                f"confidence={quality_data['confidence_level']}"
            )
            
            return True
            
        except MissingDataError as e:
            self.logger.warning(f"Skipping {rule_id}: {e}")
            self.stats['skipped'] += 1
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to migrate {rule_id}: {e}", exc_info=True)
            self.stats['errors'] += 1
            raise MigrationError(f"Migration failed for {rule_id}: {e}") from e
    
    def run_migration(self, batch_size: int = 10, dry_run: bool = False):
        """
        Run the migration for all rules.
        
        Args:
            batch_size: Number of rules to process before checkpointing
            dry_run: If True, don't actually update the database
        """
        self.stats['start_time'] = datetime.utcnow().isoformat()
        
        self.logger.info("="*60)
        self.logger.info("QUALITY SCORE MIGRATION")
        self.logger.info("="*60)
        
        if dry_run:
            self.logger.info("DRY RUN MODE - No database changes will be made")
        
        # Load checkpoint
        checkpoint = self.load_checkpoint()
        processed_ids = set(checkpoint['processed_ids'])
        
        # Get rules to migrate
        rules = self.get_rules_to_migrate()
        self.stats['total_rules'] = len(rules)
        
        if len(rules) == 0:
            self.logger.info("No rules need migration. All rules already have quality scores.")
            return
        
        # Filter out already processed
        rules_to_process = [r for r in rules if r['id'] not in processed_ids]
        
        self.logger.info(f"Total rules: {len(rules)}")
        self.logger.info(f"Already processed: {len(processed_ids)}")
        self.logger.info(f"Remaining: {len(rules_to_process)}")
        self.logger.info(f"Batch size: {batch_size}")
        
        if dry_run:
            self.logger.info("\nDRY RUN: Processing first 3 rules as test...")
            rules_to_process = rules_to_process[:3]
        
        # Process rules
        for i, rule in enumerate(rules_to_process, 1):
            try:
                self.logger.info(f"\n[{i}/{len(rules_to_process)}] Processing {rule['id']}...")
                
                if not dry_run:
                    success = self.migrate_rule(rule)
                    if success:
                        self.stats['migrated'] += 1
                        processed_ids.add(rule['id'])
                else:
                    # Dry run: just fetch and calculate, don't update
                    repo_data = self.get_repo_metadata(rule['id'])
                    enhanced = enhance_repo_metadata(repo_data)
                    self.logger.info(
                        f"  Would set: quality={enhanced['quality_score']:.1f}, "
                        f"confidence={enhanced['confidence_level']}"
                    )
                    self.stats['migrated'] += 1
                
                # Checkpoint every batch_size rules
                if i % batch_size == 0 and not dry_run:
                    self.save_checkpoint(list(processed_ids))
                    self.logger.info(f"Checkpoint saved at {i} rules")
                
                # Rate limiting
                time.sleep(0.1)
                
            except MigrationError as e:
                self.logger.error(f"Migration error: {e}")
                continue
        
        # Final checkpoint
        if not dry_run:
            self.save_checkpoint(list(processed_ids))
        
        self.stats['end_time'] = datetime.utcnow().isoformat()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print migration summary"""
        self.logger.info("\n" + "="*60)
        self.logger.info("MIGRATION SUMMARY")
        self.logger.info("="*60)
        self.logger.info(f"Total rules: {self.stats['total_rules']}")
        self.logger.info(f"Migrated: {self.stats['migrated']}")
        self.logger.info(f"Skipped: {self.stats['skipped']}")
        self.logger.info(f"Errors: {self.stats['errors']}")
        
        if self.stats['start_time'] and self.stats['end_time']:
            start = datetime.fromisoformat(self.stats['start_time'])
            end = datetime.fromisoformat(self.stats['end_time'])
            duration = (end - start).total_seconds()
            self.logger.info(f"Duration: {duration:.1f}s")
        
        self.logger.info("="*60)
    
    def verify_migration(self):
        """Verify migration completed successfully"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (r:IDERule)
                RETURN count(r) AS total,
                       sum(CASE WHEN r.repo_quality_score IS NOT NULL THEN 1 ELSE 0 END) AS with_quality,
                       avg(r.repo_quality_score) AS avg_quality,
                       min(r.repo_quality_score) AS min_quality,
                       max(r.repo_quality_score) AS max_quality
            """)
            
            stats = result.single()
            
            self.logger.info("\n" + "="*60)
            self.logger.info("VERIFICATION RESULTS")
            self.logger.info("="*60)
            self.logger.info(f"Total rules: {stats['total']}")
            self.logger.info(f"With quality scores: {stats['with_quality']}")
            self.logger.info(f"Average quality: {stats['avg_quality']:.1f}/100")
            self.logger.info(f"Quality range: {stats['min_quality']:.1f} - {stats['max_quality']:.1f}")
            
            if stats['total'] == stats['with_quality']:
                self.logger.info("\nSUCCESS: All rules have quality scores")
            else:
                missing = stats['total'] - stats['with_quality']
                self.logger.warning(f"\nWARNING: {missing} rules still missing quality scores")
            
            self.logger.info("="*60)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Migrate IDERule nodes to add quality scores')
    parser.add_argument('--dry-run', action='store_true', help='Test run without database updates')
    parser.add_argument('--batch-size', type=int, default=10, help='Checkpoint every N rules')
    parser.add_argument('--verify-only', action='store_true', help='Only verify migration status')
    
    args = parser.parse_args()
    
    # Load config
    config_path = Path(__file__).parent / 'config.yaml'
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Setup logger
    logger = StructuredLogger("migration", config.get('logging', {}))
    
    # Connect to Neo4j
    uri = os.getenv('NEO4J_URI')
    user = os.getenv('NEO4J_USER')
    password = os.getenv('NEO4J_PASSWORD')
    
    if not all([uri, user, password]):
        logger.error("Missing Neo4j environment variables (NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)")
        return 1
    
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    try:
        # Test connection
        with driver.session() as session:
            session.run("RETURN 1")
        logger.info("Neo4j connection successful")
        
        # Create migration instance
        migration = QualityScoreMigration(driver, logger)
        
        if args.verify_only:
            migration.verify_migration()
        else:
            migration.run_migration(
                batch_size=args.batch_size,
                dry_run=args.dry_run
            )
            
            if not args.dry_run:
                migration.verify_migration()
        
        return 0
        
    except Exception as e:
        logger.error(f"Migration failed: {e}", exc_info=True)
        return 1
        
    finally:
        driver.close()


if __name__ == '__main__':
    import sys
    sys.exit(main())
