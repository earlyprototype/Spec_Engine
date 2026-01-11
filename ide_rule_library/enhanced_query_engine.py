#!/usr/bin/env python3
"""
Enhanced query engine with quality filtering and context awareness.

Prevents cargo culting by filtering based on:
- Quality scores
- Production signals
- Confidence levels
- Project context matching
"""

import os
from typing import List, Dict, Optional
import google.generativeai as genai
from neo4j import GraphDatabase

from ide_rule_library.exceptions import (
    QueryError,
    NoRulesFoundError,
    DatabaseError,
    GeminiError,
    MissingEnvironmentVariableError
)
from ide_rule_library.retry_handler import call_gemini_embedding_with_retry


class EnhancedRuleQueryEngine:
    """Quality-aware semantic search for IDE rules"""
    
    def __init__(self, driver, logger, embedding_model: str = 'models/text-embedding-004'):
        self.driver = driver
        self.logger = logger
        self.embedding_model = embedding_model
        self._quality_data_available = None  # Cache quality data check
        
        # Configure Gemini
        gemini_key = os.getenv('GEMINI_API_KEY')
        if not gemini_key:
            raise MissingEnvironmentVariableError(
                "GEMINI_API_KEY not found in environment. "
                "Please set it in your .env file or environment variables."
            )
        
        genai.configure(api_key=gemini_key)
        
        self.logger.info("EnhancedRuleQueryEngine initialized")
    
    def _check_quality_data_exists(self) -> bool:
        """
        Check if any rules have quality scores.
        
        Returns:
            True if quality data exists, False otherwise
        """
        if self._quality_data_available is not None:
            return self._quality_data_available
        
        with self.driver.session() as session:
            try:
                result = session.run("""
                    MATCH (r:IDERule)
                    WHERE r.repo_quality_score IS NOT NULL
                    RETURN count(r) AS count
                    LIMIT 1
                """)
                
                record = result.single()
                self._quality_data_available = record['count'] > 0
                
                if not self._quality_data_available:
                    self.logger.warning(
                        "No quality scores found in database. "
                        "Run migrate_quality_scores.py to enable quality filtering."
                    )
                
                return self._quality_data_available
                
            except Exception as e:
                self.logger.error(f"Failed to check quality data: {e}")
                self._quality_data_available = False
                return False
    
    def query_rules(self,
                   query: str,
                   project_type: Optional[str] = None,
                   technologies: Optional[List[str]] = None,
                   ide_type: str = 'cursor',
                   # NEW: Quality filters (keep original defaults for backwards compatibility)
                   min_quality_score: float = 60.0,
                   min_confidence: int = 3,
                   max_days_since_update: int = 365,
                   require_production_signals: bool = True,
                   # NEW: Context filters
                   project_size: Optional[str] = None,
                   team_size: Optional[str] = None,
                   top_k: int = 15) -> List[Dict]:
        """
        Enhanced semantic search with quality and context filtering.
        
        Args:
            query: Search query
            project_type: Type of project (api, web_app, etc.)
            technologies: Required technologies
            ide_type: IDE type (cursor, vscode, etc.)
            min_quality_score: Minimum composite quality score (0-100)
            min_confidence: Minimum confidence level (1-5)
            max_days_since_update: Maximum days since repo update
            require_production_signals: Require at least CI/CD or tests
            project_size: Project size context (small, medium, large)
            team_size: Team size context (solo, small, medium, large)
            top_k: Number of results
            
        Returns:
            List of enhanced rule dictionaries with quality metadata
        """
        
        # Check if quality data exists - if not, fall back to v1 query
        has_quality_data = self._check_quality_data_exists()
        
        if not has_quality_data:
            self.logger.warning(
                "No quality data available. Falling back to v1 query (semantic similarity only). "
                "Run migrate_quality_scores.py to enable quality filtering."
            )
            return self._query_v1_fallback(
                query=query,
                project_type=project_type,
                technologies=technologies,
                ide_type=ide_type,
                top_k=top_k
            )
        
        self.logger.info(f"Enhanced query: '{query}' (quality>={min_quality_score}, confidence>={min_confidence})")
        
        # Validate inputs
        if not query or not query.strip():
            raise QueryError("Query cannot be empty")
        
        # Generate query embedding with retry
        try:
            query_embedding = call_gemini_embedding_with_retry(
                content=query,
                embedding_model=self.embedding_model,
                task_type="semantic_similarity",
                max_attempts=3,
                logger=self.logger
            )
        except Exception as e:
            self.logger.error(f"Failed to generate query embedding: {e}", exc_info=True)
            raise GeminiError(f"Failed to generate embedding for query: {e}") from e
        
        with self.driver.session() as session:
            # Build quality-filtered query
            cypher = """
                CALL db.index.vector.queryNodes('ide_rule_embeddings', $top_k * 3, $embedding)
                YIELD node AS r, score
                WHERE $ide_type IN r.ide_types
            """
            
            params = {
                'embedding': query_embedding,
                'top_k': top_k,
                'ide_type': ide_type
            }
            
            # Quality filters
            cypher += """
                AND r.repo_quality_score >= $min_quality_score
                AND r.confidence_level >= $min_confidence
                AND r.days_since_update <= $max_days_since_update
            """
            params['min_quality_score'] = min_quality_score
            params['min_confidence'] = min_confidence
            params['max_days_since_update'] = max_days_since_update
            
            # Production signals filter
            if require_production_signals:
                cypher += """
                    AND (r.has_ci_cd = true OR r.has_tests = true)
                """
            
            # Context filters
            if project_size:
                cypher += """
                    AND ($project_size IN r.suitable_project_sizes OR size(r.suitable_project_sizes) = 0)
                """
                params['project_size'] = project_size
            
            if team_size:
                cypher += """
                    AND ($team_size IN r.suitable_team_sizes OR size(r.suitable_team_sizes) = 0)
                """
                params['team_size'] = team_size
            
            # Optional filters
            if project_type:
                cypher += """
                    AND $project_type IN r.project_types
                """
                params['project_type'] = project_type
            
            if technologies:
                cypher += """
                    AND ANY(tech IN $technologies WHERE tech IN r.technologies)
                """
                params['technologies'] = technologies
            
            # Return with quality metadata
            cypher += """
                RETURN r.id AS id,
                       r.source_repo AS source_repo,
                       r.file_path AS file_path,
                       r.content AS content,
                       r.purpose AS purpose,
                       r.key_practices AS key_practices,
                       r.categories AS categories,
                       r.reasoning AS reasoning,
                       r.technologies AS technologies,
                       r.project_types AS project_types,
                       r.stars AS stars,
                       r.repo_quality_score AS repo_quality_score,
                       r.confidence_level AS confidence_level,
                       r.confidence_reasoning AS confidence_reasoning,
                       r.suitable_project_sizes AS suitable_project_sizes,
                       r.suitable_team_sizes AS suitable_team_sizes,
                       r.trade_offs AS trade_offs,
                       r.anti_patterns AS anti_patterns,
                       r.alternative_approaches AS alternative_approaches,
                       r.has_ci_cd AS has_ci_cd,
                       r.has_tests AS has_tests,
                       r.has_deployment AS has_deployment,
                       r.production_signals AS production_signals,
                       r.days_since_update AS days_since_update,
                       score
                ORDER BY r.repo_quality_score DESC, score DESC
                LIMIT $top_k
            """
            
            try:
                result = session.run(cypher, **params)
                rules = [dict(record) for record in result]
                
                # Log quality stats
                if rules:
                    avg_quality = sum(r.get('repo_quality_score', 0) for r in rules) / len(rules)
                    avg_confidence = sum(r.get('confidence_level', 0) for r in rules) / len(rules)
                    self.logger.info(
                        f"Found {len(rules)} rules "
                        f"(avg quality: {avg_quality:.1f}/100, "
                        f"avg confidence: {avg_confidence:.1f}/5)"
                    )
                else:
                    self.logger.warning(
                        f"No rules matched quality criteria "
                        f"(quality>={min_quality_score}, confidence>={min_confidence})"
                    )
                
                return rules
                
            except Exception as e:
                self.logger.error(f"Database query failed: {e}", exc_info=True)
                raise DatabaseError(f"Failed to query rules from database: {e}") from e
    
    def _query_v1_fallback(self,
                           query: str,
                           project_type: Optional[str] = None,
                           technologies: Optional[List[str]] = None,
                           ide_type: str = 'cursor',
                           top_k: int = 15) -> List[Dict]:
        """
        V1 fallback query without quality filters.
        
        Used when quality data is not available in the database.
        Returns rules based on semantic similarity only.
        """
        
        self.logger.info(f"V1 fallback query: '{query}' (no quality filters)")
        
        # Generate query embedding
        try:
            query_embedding = call_gemini_embedding_with_retry(
                content=query,
                embedding_model=self.embedding_model,
                task_type="semantic_similarity",
                max_attempts=3,
                logger=self.logger
            )
        except Exception as e:
            raise GeminiError(f"Failed to generate embedding: {e}") from e
        
        with self.driver.session() as session:
            cypher = """
                CALL db.index.vector.queryNodes('ide_rule_embeddings', $top_k, $embedding)
                YIELD node AS r, score
                WHERE $ide_type IN r.ide_types
            """
            
            params = {
                'embedding': query_embedding,
                'top_k': top_k,
                'ide_type': ide_type
            }
            
            # Optional filters
            if project_type:
                cypher += " AND $project_type IN r.project_types"
                params['project_type'] = project_type
            
            if technologies:
                cypher += " AND ANY(tech IN $technologies WHERE tech IN r.technologies)"
                params['technologies'] = technologies
            
            cypher += """
                RETURN r.id AS id,
                       r.source_repo AS source_repo,
                       r.file_path AS file_path,
                       r.content AS content,
                       r.purpose AS purpose,
                       r.key_practices AS key_practices,
                       r.categories AS categories,
                       r.reasoning AS reasoning,
                       r.technologies AS technologies,
                       r.project_types AS project_types,
                       r.stars AS stars,
                       COALESCE(r.repo_quality_score, 0) AS repo_quality_score,
                       COALESCE(r.confidence_level, 1) AS confidence_level,
                       score
                ORDER BY score DESC
                LIMIT $top_k
            """
            
            try:
                result = session.run(cypher, **params)
                rules = [dict(record) for record in result]
                
                self.logger.info(f"V1 fallback found {len(rules)} rules")
                
                return rules
                
            except Exception as e:
                raise DatabaseError(f"V1 fallback query failed: {e}") from e
    
    def validate_pattern_consensus(self, pattern: str, min_sources: int = 3) -> Dict:
        """
        Check if a pattern has consensus across multiple high-quality repos.
        
        Returns validation status with perspectives from different sources.
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (r:IDERule)
                WHERE $pattern IN r.key_practices
                  AND r.repo_quality_score > 60
                  AND r.confidence_level >= 3
                RETURN r.source_repo AS repo,
                       r.reasoning AS reasoning,
                       r.trade_offs AS trade_offs,
                       r.repo_quality_score AS quality,
                       r.confidence_level AS confidence
                ORDER BY r.repo_quality_score DESC
                LIMIT 10
            """, pattern=pattern)
            
            sources = [dict(record) for record in result]
            
            if len(sources) >= min_sources:
                return {
                    'validated': True,
                    'consensus_strength': len(sources),
                    'avg_quality': sum(s['quality'] for s in sources) / len(sources),
                    'avg_confidence': sum(s['confidence'] for s in sources) / len(sources),
                    'perspectives': sources
                }
            else:
                return {
                    'validated': False,
                    'found_sources': len(sources),
                    'warning': f'Only {len(sources)} source(s) recommend this pattern',
                    'risk': 'Potential cargo culting from single source',
                    'perspectives': sources if sources else []
                }
    
    def find_conflicting_patterns(self, rule_id: str) -> List[Dict]:
        """Find rules that contradict a given rule's practices"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (r1:IDERule {id: $rule_id}), (r2:IDERule)
                WHERE r1.id <> r2.id
                  AND (
                    ANY(ap IN r1.anti_patterns WHERE ap IN r2.key_practices)
                    OR ANY(ap IN r2.anti_patterns WHERE ap IN r1.key_practices)
                  )
                RETURN r2.id AS id,
                       r2.source_repo AS source_repo,
                       r2.key_practices AS key_practices,
                       r2.anti_patterns AS anti_patterns,
                       r2.repo_quality_score AS repo_quality_score,
                       'CONFLICT' AS status
                ORDER BY r2.quality_score DESC
            """, rule_id=rule_id)
            
            return [dict(record) for record in result]
    
    def query_rules_with_fallback(self,
                                   query: str,
                                   project_type: Optional[str] = None,
                                   technologies: Optional[List[str]] = None,
                                   ide_type: str = 'cursor',
                                   min_quality_score: float = 60.0,
                                   min_confidence: int = 3,
                                   max_days_since_update: int = 365,
                                   require_production_signals: bool = True,
                                   project_size: Optional[str] = None,
                                   team_size: Optional[str] = None,
                                   top_k: int = 15,
                                   min_results: int = 5) -> List[Dict]:
        """
        Query rules with graceful degradation when too few results.
        
        Falls back through progressively relaxed filters:
        1. Strict filters (as specified)
        2. Relaxed quality (min_quality - 20, no production signals required)
        3. Minimal filters (quality >= 40, confidence >= 2)
        4. No quality filters (return best available by semantic similarity)
        
        Args:
            Same as query_rules, plus:
            min_results: Minimum acceptable number of results before relaxing filters
            
        Returns:
            List of rules, with relaxation level logged
        """
        
        self.logger.info(f"Querying with fallback strategy (min_results={min_results})")
        
        # Try strict filters first
        rules = self.query_rules(
            query=query,
            project_type=project_type,
            technologies=technologies,
            ide_type=ide_type,
            min_quality_score=min_quality_score,
            min_confidence=min_confidence,
            max_days_since_update=max_days_since_update,
            require_production_signals=require_production_signals,
            project_size=project_size,
            team_size=team_size,
            top_k=top_k
        )
        
        if len(rules) >= min_results:
            self.logger.info(f"Strict filters returned {len(rules)} rules")
            return rules
        
        # Fallback 1: Relax quality and production signals
        self.logger.warning(
            f"Only {len(rules)} rules with strict filters. "
            f"Relaxing to quality>={min_quality_score - 20}, no production requirement"
        )
        
        rules = self.query_rules(
            query=query,
            project_type=project_type,
            technologies=technologies,
            ide_type=ide_type,
            min_quality_score=max(min_quality_score - 20, 40),
            min_confidence=max(min_confidence - 1, 2),
            max_days_since_update=max_days_since_update * 2,  # Allow older repos
            require_production_signals=False,
            project_size=project_size,
            team_size=team_size,
            top_k=top_k
        )
        
        if len(rules) >= min_results:
            self.logger.info(f"Relaxed filters returned {len(rules)} rules")
            return rules
        
        # Fallback 2: Minimal quality filters
        self.logger.warning(
            f"Only {len(rules)} rules with relaxed filters. "
            f"Using minimal filters (quality>=40, confidence>=2)"
        )
        
        rules = self.query_rules(
            query=query,
            project_type=project_type,
            technologies=technologies,
            ide_type=ide_type,
            min_quality_score=40.0,
            min_confidence=2,
            max_days_since_update=999999,  # No time limit
            require_production_signals=False,
            project_size=None,  # Remove context filters
            team_size=None,
            top_k=top_k
        )
        
        if len(rules) >= min_results:
            self.logger.info(f"Minimal filters returned {len(rules)} rules")
            return rules
        
        # Fallback 3: No quality filters, pure semantic similarity
        self.logger.warning(
            f"Only {len(rules)} rules with minimal filters. "
            f"Removing all quality filters, using pure semantic search"
        )
        
        rules = self._query_no_quality_filters(
            query=query,
            project_type=project_type,
            technologies=technologies,
            ide_type=ide_type,
            top_k=top_k
        )
        
        if len(rules) == 0:
            raise NoRulesFoundError(
                f"No rules found for query '{query}' even with all filters removed. "
                f"Database may be empty or query embedding failed."
            )
        
        self.logger.warning(f"No quality filters returned {len(rules)} rules")
        return rules
    
    def _query_no_quality_filters(self,
                                   query: str,
                                   project_type: Optional[str] = None,
                                   technologies: Optional[List[str]] = None,
                                   ide_type: str = 'cursor',
                                   top_k: int = 15) -> List[Dict]:
        """
        Query rules without any quality filters (semantic similarity only).
        
        Used as last resort when all filtered queries return too few results.
        """
        
        # Generate query embedding
        try:
            query_embedding = call_gemini_embedding_with_retry(
                content=query,
                embedding_model=self.embedding_model,
                task_type="semantic_similarity",
                max_attempts=3,
                logger=self.logger
            )
        except Exception as e:
            raise GeminiError(f"Failed to generate embedding: {e}") from e
        
        with self.driver.session() as session:
            cypher = """
                CALL db.index.vector.queryNodes('ide_rule_embeddings', $top_k, $embedding)
                YIELD node AS r, score
                WHERE $ide_type IN r.ide_types
            """
            
            params = {
                'embedding': query_embedding,
                'top_k': top_k,
                'ide_type': ide_type
            }
            
            # Optional filters (still apply these if specified)
            if project_type:
                cypher += " AND $project_type IN r.project_types"
                params['project_type'] = project_type
            
            if technologies:
                cypher += " AND ANY(tech IN $technologies WHERE tech IN r.technologies)"
                params['technologies'] = technologies
            
            cypher += """
                RETURN r.id AS id,
                       r.source_repo AS source_repo,
                       r.file_path AS file_path,
                       r.content AS content,
                       r.purpose AS purpose,
                       r.key_practices AS key_practices,
                       r.categories AS categories,
                       r.reasoning AS reasoning,
                       r.technologies AS technologies,
                       r.project_types AS project_types,
                       r.stars AS stars,
                       COALESCE(r.repo_quality_score, 0) AS repo_quality_score,
                       COALESCE(r.confidence_level, 1) AS confidence_level,
                       score
                ORDER BY score DESC
                LIMIT $top_k
            """
            
            try:
                result = session.run(cypher, **params)
                return [dict(record) for record in result]
            except Exception as e:
                raise DatabaseError(f"No-filter query failed: {e}") from e
    
    def get_quality_stats(self) -> Dict:
        """Get database quality statistics"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (r:IDERule)
                WHERE r.quality_score IS NOT NULL
                RETURN count(r) AS total,
                       avg(r.repo_quality_score) AS avg_quality,
                       max(r.repo_quality_score) AS max_quality,
                       min(r.repo_quality_score) AS min_quality,
                       avg(r.confidence_level) AS avg_confidence,
                       sum(CASE WHEN r.has_ci_cd THEN 1 ELSE 0 END) AS with_ci_cd,
                       sum(CASE WHEN r.has_tests THEN 1 ELSE 0 END) AS with_tests,
                       sum(CASE WHEN r.confidence_level >= 4 THEN 1 ELSE 0 END) AS high_confidence
            """)
            
            stats = result.single()
            return dict(stats) if stats else {}
