#!/usr/bin/env python3
"""Neo4j writer for IDERule nodes with duplicate detection"""

from neo4j import GraphDatabase
from typing import Dict, Optional


class Neo4jRuleWriter:
    """Write IDERule nodes with duplicate detection and pattern linking"""
    
    def __init__(self, driver, config: dict, logger):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.batch_size = config['neo4j'].get('batch_size', 50)
        self.duplicate_check = config['neo4j'].get('duplicate_check', True)
    
    def write_rule(self, rule_data: Dict, pattern_name: Optional[str] = None) -> bool:
        """Write IDERule node, skip if duplicate"""
        
        with self.driver.session() as session:
            # Check for duplicate by content hash
            if self.duplicate_check and self._is_duplicate(session, rule_data['content_hash']):
                self.logger.info(f"Skipping duplicate: {rule_data['id']}")
                return False
            
            try:
                # Create IDERule node
                session.run("""
                    CREATE (r:IDERule {
                        id: $id,
                        source_repo: $source_repo,
                        file_path: $file_path,
                        file_format: $file_format,
                        content: $content,
                        content_hash: $content_hash,
                        purpose: $purpose,
                        categories: $categories,
                        key_practices: $key_practices,
                        reasoning: $reasoning,
                        ide_types: $ide_types,
                        technologies: $technologies,
                        project_types: $project_types,
                        stars: $stars,
                        embedding: $embedding,
                        extracted_date: datetime($extracted_date)
                    })
                """, **rule_data)
                
                self.logger.info(f"Created IDERule: {rule_data['id']}")
                
                # Link to Pattern node if provided
                if pattern_name:
                    result = session.run("""
                        MATCH (p:Pattern {name: $pattern_name})
                        MATCH (r:IDERule {id: $rule_id})
                        MERGE (p)-[:HAS_IDE_RULES]->(r)
                        RETURN p.name AS linked
                    """, pattern_name=pattern_name, rule_id=rule_data['id'])
                    
                    if result.single():
                        self.logger.debug(f"Linked to Pattern: {pattern_name}")
                    else:
                        self.logger.warning(f"Could not link to Pattern: {pattern_name} (not found)")
                
                return True
                
            except Exception as e:
                self.logger.error(f"Failed to write rule {rule_data['id']}: {e}", exc_info=True)
                return False
    
    def _is_duplicate(self, session, content_hash: str) -> bool:
        """Check if content hash already exists"""
        try:
            result = session.run("""
                MATCH (r:IDERule {content_hash: $hash})
                RETURN count(r) AS count
            """, hash=content_hash)
            
            record = result.single()
            return record['count'] > 0 if record else False
            
        except Exception as e:
            self.logger.warning(f"Error checking duplicate: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """Get IDERule statistics"""
        database = os.getenv("NEO4J_DATABASE", "neo4j")
        with self.driver.session(database=database) as session:
            result = session.run("""
                MATCH (r:IDERule)
                RETURN count(r) AS total_rules,
                       count(DISTINCT r.source_repo) AS unique_repos,
                       count(DISTINCT r.file_format) AS unique_formats,
                       avg(r.stars) AS avg_stars
            """)
            
            record = result.single()
            if record:
                return {
                    'total_rules': record['total_rules'],
                    'unique_repos': record['unique_repos'],
                    'unique_formats': record['unique_formats'],
                    'avg_stars': record['avg_stars']
                }
            return {}
    
    def get_rules_by_format(self) -> Dict[str, int]:
        """Get count of rules by file format"""
        database = os.getenv("NEO4J_DATABASE", "neo4j")
        with self.driver.session(database=database) as session:
            result = session.run("""
                MATCH (r:IDERule)
                RETURN r.file_format AS format, count(r) AS count
                ORDER BY count DESC
            """)
            
            return {record['format']: record['count'] for record in result}
    
    def delete_rule(self, rule_id: str) -> bool:
        """Delete a specific IDERule node"""
        with self.driver.session() as session:
            try:
                result = session.run("""
                    MATCH (r:IDERule {id: $rule_id})
                    DETACH DELETE r
                    RETURN count(r) AS deleted
                """, rule_id=rule_id)
                
                deleted = result.single()['deleted']
                if deleted:
                    self.logger.info(f"Deleted IDERule: {rule_id}")
                    return True
                else:
                    self.logger.warning(f"IDERule not found: {rule_id}")
                    return False
                    
            except Exception as e:
                self.logger.error(f"Failed to delete rule {rule_id}: {e}", exc_info=True)
                return False
    
    def clear_all_rules(self, confirm: bool = False) -> int:
        """Delete all IDERule nodes (requires confirmation)"""
        if not confirm:
            raise ValueError("Must set confirm=True to clear all rules")
        
        with self.driver.session() as session:
            try:
                result = session.run("""
                    MATCH (r:IDERule)
                    DETACH DELETE r
                    RETURN count(r) AS deleted
                """)
                
                deleted = result.single()['deleted']
                self.logger.warning(f"Deleted {deleted} IDERule nodes")
                return deleted
                
            except Exception as e:
                self.logger.error(f"Failed to clear rules: {e}", exc_info=True)
                return 0
