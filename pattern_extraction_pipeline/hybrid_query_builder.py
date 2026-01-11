"""
Hybrid Query Builder

Composes queries that combine semantic vector search with structural
graph filtering for optimal pattern discovery.
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class QueryConstraints:
    """Constraints for filtering patterns."""
    technologies: Optional[List[str]] = None
    deployment_type: Optional[str] = None
    min_stars: int = 0
    min_confidence: str = 'low'
    domains: Optional[List[str]] = None
    requirement_types: Optional[List[str]] = None


class HybridQueryBuilder:
    """
    Builds Cypher queries that combine vector search with graph traversal.
    
    Strategy:
    1. Vector search for semantic similarity (cast wide net)
    2. Graph traversal for structural filtering (narrow down)
    3. Enrichment with related data (technologies, constraints)
    4. Ranking by composite score
    """
    
    # Confidence level ordering for filtering
    CONFIDENCE_LEVELS = {
        'high': 3,
        'medium': 2,
        'low': 1
    }
    
    def __init__(self):
        """Initialize query builder."""
        pass
    
    def build_semantic_search(
        self,
        top_k: int = 20,
        min_similarity: float = 0.0
    ) -> Tuple[str, Dict]:
        """
        Build vector similarity search query.
        
        Args:
            top_k: Number of top similar patterns to retrieve
            min_similarity: Minimum similarity threshold (0-1)
        
        Returns:
            (cypher_query, parameters_dict)
        """
        query = """
            // Step 1: Vector similarity search
            CALL db.index.vector.queryNodes('pattern_embeddings', $top_k, $embedding)
            YIELD node AS p, score
            WHERE score >= $min_similarity
            RETURN p, score
            ORDER BY score DESC
        """
        
        params = {
            'top_k': top_k,
            'min_similarity': min_similarity,
            # 'embedding' will be provided at query execution
        }
        
        return query, params
    
    def build_hybrid_search(
        self,
        constraints: QueryConstraints,
        top_k: int = 10,
        semantic_top_k: int = 20
    ) -> Tuple[str, Dict]:
        """
        Build hybrid search query (semantic + structural).
        
        Args:
            constraints: Structural constraints for filtering
            top_k: Number of final results to return
            semantic_top_k: Number of candidates from vector search
        
        Returns:
            (cypher_query, parameters_dict)
        """
        # Start with vector search
        query_parts = ["""
            // Step 1: Semantic vector search (cast wide net)
            CALL db.index.vector.queryNodes('pattern_embeddings', $semantic_top_k, $embedding)
            YIELD node AS p, score
        """]
        
        # Build WHERE clauses for filtering
        where_clauses = []
        params = {
            'semantic_top_k': semantic_top_k,
            'top_k': top_k
        }
        
        # Confidence filter
        if constraints.min_confidence:
            min_conf_value = self.CONFIDENCE_LEVELS.get(constraints.min_confidence, 1)
            where_clauses.append("""
                CASE p.confidence
                    WHEN 'high' THEN 3
                    WHEN 'medium' THEN 2
                    ELSE 1
                END >= $min_confidence_value
            """)
            params['min_confidence_value'] = min_conf_value
        
        # Stars filter
        if constraints.min_stars > 0:
            where_clauses.append("p.stars >= $min_stars")
            params['min_stars'] = constraints.min_stars
        
        # Add WHERE clause if we have filters
        if where_clauses:
            query_parts.append("WHERE " + " AND ".join(where_clauses))
        
        # Step 2: Technology filtering (if specified)
        if constraints.technologies:
            query_parts.append("""
                // Step 2: Filter by required technologies
                MATCH (p)-[:USES]->(t:Technology)
                WHERE t.name IN $technologies
                WITH p, score, collect(DISTINCT t.name) AS pattern_techs
                WHERE size(pattern_techs) >= $min_tech_matches
            """)
            params['technologies'] = constraints.technologies
            # Require at least 50% of requested technologies
            params['min_tech_matches'] = max(1, len(constraints.technologies) // 2)
        else:
            query_parts.append("""
                // Step 2: Collect technologies (no filtering)
                OPTIONAL MATCH (p)-[:USES]->(t:Technology)
                WITH p, score, collect(DISTINCT t.name) AS pattern_techs
            """)
        
        # Step 3: Enrichment with constraints and requirements
        query_parts.append("""
            // Step 3: Enrich with constraints and requirements
            OPTIONAL MATCH (p)-[:REQUIRES]->(c:Constraint)
            OPTIONAL MATCH (r:Requirement)-[:SOLVED_BY]->(p)
        """)
        
        # Domain filter (if specified)
        if constraints.domains:
            query_parts.append("WHERE r.domain IN $domains")
            params['domains'] = constraints.domains
        
        # Deployment type filter (if specified via requirement)
        if constraints.deployment_type:
            query_parts.append("""
                AND (
                    r.deployment_type = $deployment_type
                    OR r.deployment_type IS NULL
                )
            """)
            params['deployment_type'] = constraints.deployment_type
        
        # Step 4: Return enriched results
        query_parts.append("""
            // Step 4: Return enriched results
            WITH p, score, pattern_techs,
                 collect(DISTINCT c.rule) AS constraints,
                 collect(DISTINCT r.type) AS requirement_types,
                 collect(DISTINCT r.domain) AS domains
            RETURN p.name AS name,
                   p.reasoning AS reasoning,
                   p.description AS description,
                   p.confidence AS confidence,
                   p.stars AS stars,
                   p.source_repo AS source_repo,
                   score AS semantic_similarity,
                   pattern_techs AS technologies,
                   constraints,
                   requirement_types,
                   domains
            ORDER BY score DESC
            LIMIT $top_k
        """)
        
        return "\n".join(query_parts), params
    
    def build_cross_pattern_discovery(
        self,
        min_similarity: float = 0.7,
        top_k: int = 15,
        exclude_techs: Optional[List[str]] = None
    ) -> Tuple[str, Dict]:
        """
        Build query for cross-pattern discovery (conceptual similarity without tech constraints).
        
        Args:
            min_similarity: Minimum semantic similarity (higher = more similar)
            top_k: Number of results to return
            exclude_techs: Technologies to exclude (optional)
        
        Returns:
            (cypher_query, parameters_dict)
        """
        query = """
            // Step 1: High-similarity semantic search (no tech filtering)
            CALL db.index.vector.queryNodes('pattern_embeddings', $top_k, $embedding)
            YIELD node AS p, score
            WHERE score >= $min_similarity
            
            // Step 2: Get technologies without filtering
            OPTIONAL MATCH (p)-[:USES]->(t:Technology)
        """
        
        params = {
            'top_k': top_k,
            'min_similarity': min_similarity
        }
        
        # Optional: exclude certain technologies
        if exclude_techs:
            query += """
                WHERE NOT t.name IN $exclude_techs
            """
            params['exclude_techs'] = exclude_techs
        
        query += """
            // Step 3: Find patterns sharing technologies (conceptual relationships)
            WITH p, score, collect(DISTINCT t.name) AS techs, t
            OPTIONAL MATCH (similar:Pattern)-[:USES]->(t)
            WHERE similar <> p
            
            // Step 4: Return with conceptual grouping
            WITH p, score, techs,
                 collect(DISTINCT similar.name) AS similar_by_tech
            RETURN p.name AS name,
                   p.reasoning AS reasoning,
                   p.confidence AS confidence,
                   p.stars AS stars,
                   score AS conceptual_similarity,
                   techs AS tech_stack,
                   similar_by_tech AS related_patterns
            ORDER BY score DESC
        """
        
        return query, params
    
    def build_pattern_details(
        self,
        pattern_name: str
    ) -> Tuple[str, Dict]:
        """
        Build query to fetch complete pattern details.
        
        Args:
            pattern_name: Name of the pattern to fetch
        
        Returns:
            (cypher_query, parameters_dict)
        """
        query = """
            MATCH (p:Pattern {name: $pattern_name})
            
            // Get technologies
            OPTIONAL MATCH (p)-[:USES]->(t:Technology)
            
            // Get constraints
            OPTIONAL MATCH (p)-[:REQUIRES]->(c:Constraint)
            
            // Get requirements
            OPTIONAL MATCH (r:Requirement)-[:SOLVED_BY]->(p)
            
            RETURN p.name AS name,
                   p.reasoning AS reasoning,
                   p.description AS description,
                   p.confidence AS confidence,
                   p.stars AS stars,
                   p.source_repo AS source_repo,
                   p.extracted_date AS extracted_date,
                   collect(DISTINCT {
                       name: t.name,
                       role: 'primary'
                   }) AS technologies,
                   collect(DISTINCT c.rule) AS constraints,
                   collect(DISTINCT {
                       type: r.type,
                       domain: r.domain
                   }) AS requirements
        """
        
        return query, {'pattern_name': pattern_name}
    
    def build_similar_patterns(
        self,
        pattern_name: str,
        top_k: int = 5,
        min_similarity: float = 0.6
    ) -> Tuple[str, Dict]:
        """
        Build query to find patterns similar to a given pattern.
        
        Args:
            pattern_name: Reference pattern name
            top_k: Number of similar patterns to return
            min_similarity: Minimum similarity threshold
        
        Returns:
            (cypher_query, parameters_dict)
        """
        query = """
            // Step 1: Get reference pattern embedding
            MATCH (p1:Pattern {name: $pattern_name})
            WHERE p1.embedding IS NOT NULL
            
            // Step 2: Find similar patterns via vector search
            CALL db.index.vector.queryNodes('pattern_embeddings', $top_k_plus_one, p1.embedding)
            YIELD node AS p2, score
            WHERE p2 <> p1
                AND score >= $min_similarity
            
            // Step 3: Find shared technologies
            OPTIONAL MATCH (p1)-[:USES]->(t1:Technology)<-[:USES]-(p2)
            WITH p2, score, collect(DISTINCT t1.name) AS shared_techs
            
            // Step 4: Get all technologies for similar pattern
            OPTIONAL MATCH (p2)-[:USES]->(t2:Technology)
            WITH p2, score, shared_techs, collect(DISTINCT t2.name) AS all_techs
            
            RETURN p2.name AS name,
                   p2.reasoning AS reasoning,
                   p2.confidence AS confidence,
                   p2.stars AS stars,
                   score AS similarity,
                   shared_techs,
                   all_techs AS technologies,
                   size(shared_techs) AS tech_overlap
            ORDER BY score DESC
            LIMIT $top_k
        """
        
        params = {
            'pattern_name': pattern_name,
            'top_k': top_k,
            'top_k_plus_one': top_k + 1,  # +1 to account for excluding self
            'min_similarity': min_similarity
        }
        
        return query, params
    
    def format_for_user_review(
        self,
        patterns: List[Dict],
        max_display: int = 10
    ) -> str:
        """
        Format pattern results for user review.
        
        Args:
            patterns: List of pattern dictionaries with scores
            max_display: Maximum number of patterns to display
        
        Returns:
            Formatted string ready for display
        """
        if not patterns:
            return "No patterns found matching your criteria."
        
        output = ["="*70]
        output.append("PATTERN RECOMMENDATIONS")
        output.append("="*70)
        output.append(f"\nFound {len(patterns)} relevant patterns. Top {min(max_display, len(patterns))}:\n")
        
        for i, pattern in enumerate(patterns[:max_display], 1):
            output.append(f"{i}. {pattern.get('name', 'Unknown Pattern')}")
            
            # Composite score (if available)
            if 'composite_score' in pattern:
                score = pattern['composite_score']
                recommendation = pattern.get('recommendation', 'unknown')
                output.append(f"   Score: {score:.3f} ({recommendation.upper()})")
            elif 'semantic_similarity' in pattern:
                score = pattern['semantic_similarity']
                output.append(f"   Semantic Match: {score:.3f}")
            
            # Pattern metadata
            if 'confidence' in pattern:
                output.append(f"   Confidence: {pattern['confidence']}")
            if 'stars' in pattern:
                output.append(f"   Stars: {pattern['stars']:,}")
            
            # Technologies
            if 'technologies' in pattern and pattern['technologies']:
                techs = pattern['technologies']
                tech_str = ', '.join(techs[:5])
                if len(techs) > 5:
                    tech_str += f" (+{len(techs)-5} more)"
                output.append(f"   Technologies: {tech_str}")
            
            # Reasoning (truncated)
            if 'reasoning' in pattern and pattern['reasoning']:
                reasoning = pattern['reasoning']
                if len(reasoning) > 100:
                    reasoning = reasoning[:97] + "..."
                output.append(f"   Why: {reasoning}")
            
            # Source
            if 'source_repo' in pattern:
                output.append(f"   Source: {pattern['source_repo']}")
            
            output.append("")  # Blank line between patterns
        
        output.append("="*70)
        output.append("\nSelect a pattern to inform your SPEC generation.")
        
        return "\n".join(output)


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Testing HybridQueryBuilder")
    
    builder = HybridQueryBuilder()
    
    # Test 1: Hybrid search query
    logger.info("Test 1: Hybrid Search Query")
    logger.info("="*70)
    constraints = QueryConstraints(
        technologies=['typescript', 'react'],
        deployment_type='web',
        min_stars=5000,
        min_confidence='medium'
    )
    query, params = builder.build_hybrid_search(constraints, top_k=5)
    logger.info("Query parameters:")
    for key, value in params.items():
        if key != 'embedding':
            logger.info(f"  {key}: {value}")
    logger.info("\nQuery structure: Vector search → Tech filter → Enrichment → Ranking")
    
    # Test 2: Cross-pattern discovery
    logger.info("\n\nTest 2: Cross-Pattern Discovery Query")
    logger.info("="*70)
    query, params = builder.build_cross_pattern_discovery(min_similarity=0.75, top_k=10)
    logger.info("Query parameters:")
    for key, value in params.items():
        if key != 'embedding':
            logger.info(f"  {key}: {value}")
    logger.info("\nQuery structure: High-similarity search → No tech constraints → Conceptual grouping")
    
    # Test 3: Pattern details
    logger.info("\n\nTest 3: Pattern Details Query")
    logger.info("="*70)
    query, params = builder.build_pattern_details("electron_desktop_app")
    logger.info(f"Fetching complete details for: {params['pattern_name']}")
    
    # Test 4: Similar patterns
    logger.info("\n\nTest 4: Similar Patterns Query")
    logger.info("="*70)
    query, params = builder.build_similar_patterns("electron_desktop_app", top_k=5)
    logger.info(f"Finding patterns similar to: {params['pattern_name']}")
    logger.info(f"Top-K: {params['top_k']}, Min similarity: {params['min_similarity']}")
    
    # Test 5: Format for user review
    logger.info("\n\nTest 5: User Review Formatting")
    logger.info("="*70)
    sample_patterns = [
        {
            'name': 'Electron Desktop Application',
            'composite_score': 0.85,
            'recommendation': 'high',
            'confidence': 'high',
            'stars': 45000,
            'technologies': ['typescript', 'electron', 'react', 'sqlite'],
            'reasoning': 'Cross-platform desktop application with web technologies',
            'source_repo': 'https://github.com/example/electron-app'
        },
        {
            'name': 'CLI Tool Pattern',
            'composite_score': 0.72,
            'recommendation': 'medium',
            'confidence': 'medium',
            'stars': 8000,
            'technologies': ['typescript', 'nodejs'],
            'reasoning': 'Command-line interface for file management',
            'source_repo': 'https://github.com/example/cli-tool'
        }
    ]
    
    formatted = builder.format_for_user_review(sample_patterns)
    print(formatted)  # Keep print for formatted output visibility
    
    logger.info("\n✓ HybridQueryBuilder test complete!")
