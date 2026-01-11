"""
Semantic Extension for Pattern Query Interface

Extends PatternQueryInterface with vector search capabilities.
Adds hybrid queries combining semantic similarity with structural filtering.
"""

import os
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
from pattern_query_interface import PatternQueryInterface
from embedding_generator import EmbeddingGenerator
from confidence_scorer import ConfidenceScorer
from hybrid_query_builder import HybridQueryBuilder, QueryConstraints

load_dotenv()


class PatternQueryInterfaceSemantic(PatternQueryInterface):
    """
    Extended pattern query interface with semantic vector search.
    
    Backward compatible with original PatternQueryInterface while adding:
    - Semantic similarity search via embeddings
    - Hybrid queries (semantic + structural)
    - Cross-pattern discovery
    - Confidence scoring
    """
    
    def __init__(self):
        """Initialize with embedding generator and scoring capabilities."""
        # Initialize parent class
        super().__init__()
        
        # Add semantic capabilities
        self.embedding_generator = EmbeddingGenerator()
        self.confidence_scorer = ConfidenceScorer()
        self.query_builder = HybridQueryBuilder()
        
        print("PatternQueryInterfaceSemantic initialized with vector search")
    
    def close(self):
        """Close all connections."""
        super().close()
        # Embedding generator doesn't need explicit close
    
    # ========================================================================
    # NEW: Semantic Search Methods
    # ========================================================================
    
    def _embed_query(self, query_text: str) -> Tuple[List[float], Dict]:
        """
        Generate embedding for query text.
        
        Args:
            query_text: Natural language query or goal description
        
        Returns:
            (embedding_vector, metadata)
        """
        return self.embedding_generator.generate_embedding(query_text, use_cache=True)
    
    def _vector_search(
        self,
        embedding: List[float],
        top_k: int = 20,
        min_similarity: float = 0.0
    ) -> List[Dict]:
        """
        Execute vector similarity search against pattern embeddings.
        
        Args:
            embedding: Query embedding vector (768 dimensions)
            top_k: Number of top results to return
            min_similarity: Minimum similarity threshold (0-1)
        
        Returns:
            List of patterns with similarity scores
        """
        query, params = self.query_builder.build_semantic_search(top_k, min_similarity)
        params['embedding'] = embedding
        
        with self.neo4j.session() as session:
            result = session.run(query, **params)
            
            patterns = []
            for record in result:
                p = record['p']
                pattern = {
                    'name': p['name'],
                    'reasoning': p.get('reasoning'),
                    'description': p.get('description'),
                    'confidence': p.get('confidence'),
                    'stars': p.get('stars'),
                    'source_repo': p.get('source_repo'),
                    'semantic_similarity': record['score']
                }
                patterns.append(pattern)
            
            return patterns
    
    def find_patterns_semantic(
        self,
        goal: str,
        top_k: int = 10,
        min_similarity: float = 0.5
    ) -> Dict:
        """
        Find patterns using semantic similarity only (no structural constraints).
        
        Args:
            goal: Natural language description of the goal
            top_k: Number of patterns to return
            min_similarity: Minimum semantic similarity threshold
        
        Returns:
            Dictionary with patterns and metadata
        """
        # Generate embedding for goal
        embedding, embed_meta = self._embed_query(goal)
        
        # Execute vector search
        patterns = self._vector_search(embedding, top_k=top_k*2, min_similarity=min_similarity)
        
        # Apply confidence scoring
        patterns_with_scores = [(p, p['semantic_similarity']) for p in patterns]
        scored_patterns = self.confidence_scorer.calculate_batch(patterns_with_scores)
        
        # Return top-k
        return {
            'patterns': scored_patterns[:top_k],
            'query': goal,
            'method': 'semantic_only',
            'embedding_time_ms': embed_meta['duration_ms'],
            'total_candidates': len(patterns)
        }
    
    def find_patterns_hybrid(
        self,
        goal: str,
        constraints: Optional[Dict] = None,
        top_k: int = 10,
        semantic_top_k: int = 20
    ) -> Dict:
        """
        Find patterns using hybrid search (semantic + structural).
        
        This is the recommended default search method.
        
        Args:
            goal: Natural language description of the goal
            constraints: Dictionary with keys:
                - technologies: List[str] - Required technologies
                - deployment_type: str - Deployment type filter
                - min_stars: int - Minimum GitHub stars
                - min_confidence: str - Minimum pattern confidence
                - domains: List[str] - Domain filters
            top_k: Number of final results to return
            semantic_top_k: Number of candidates from vector search
        
        Returns:
            Dictionary with patterns, metadata, and user review format
        """
        # Parse constraints
        query_constraints = QueryConstraints(
            technologies=constraints.get('technologies') if constraints else None,
            deployment_type=constraints.get('deployment_type') if constraints else None,
            min_stars=constraints.get('min_stars', 0) if constraints else 0,
            min_confidence=constraints.get('min_confidence', 'low') if constraints else 'low',
            domains=constraints.get('domains') if constraints else None
        )
        
        # Generate embedding
        embedding, embed_meta = self._embed_query(goal)
        
        # Build and execute hybrid query
        query, params = self.query_builder.build_hybrid_search(
            query_constraints,
            top_k=top_k,
            semantic_top_k=semantic_top_k
        )
        params['embedding'] = embedding
        
        with self.neo4j.session() as session:
            result = session.run(query, **params)
            
            patterns = []
            for record in result:
                pattern = {
                    'name': record['name'],
                    'reasoning': record['reasoning'],
                    'description': record['description'],
                    'confidence': record['confidence'],
                    'stars': record['stars'],
                    'source_repo': record['source_repo'],
                    'semantic_similarity': record['semantic_similarity'],
                    'technologies': record['technologies'],
                    'constraints': record['constraints'],
                    'requirement_types': record['requirement_types'],
                    'domains': record['domains']
                }
                patterns.append(pattern)
        
        # Apply confidence scoring
        patterns_with_scores = [(p, p['semantic_similarity']) for p in patterns]
        scored_patterns = self.confidence_scorer.calculate_batch(patterns_with_scores)
        
        # Format for user review
        user_review_text = self.query_builder.format_for_user_review(scored_patterns, max_display=top_k)
        
        return {
            'patterns': scored_patterns,
            'query': goal,
            'constraints': constraints,
            'method': 'hybrid',
            'embedding_time_ms': embed_meta['duration_ms'],
            'user_review_text': user_review_text,
            'recommendation': 'Review patterns and select best fit for your SPEC'
        }
    
    def discover_alternatives(
        self,
        goal: str,
        include_different_tech: bool = True,
        min_similarity: float = 0.7,
        top_k: int = 15
    ) -> Dict:
        """
        Discover alternative architectural approaches (cross-pattern discovery).
        
        Finds conceptually similar patterns even if they use different technologies.
        
        Args:
            goal: Goal description
            include_different_tech: If True, includes patterns with different tech stacks
            min_similarity: Minimum conceptual similarity
            top_k: Number of results
        
        Returns:
            Dictionary with patterns grouped by approach
        """
        # Generate embedding
        embedding, embed_meta = self._embed_query(goal)
        
        # Build cross-pattern discovery query
        query, params = self.query_builder.build_cross_pattern_discovery(
            min_similarity=min_similarity,
            top_k=top_k
        )
        params['embedding'] = embedding
        
        with self.neo4j.session() as session:
            result = session.run(query, **params)
            
            patterns = []
            for record in result:
                pattern = {
                    'name': record['name'],
                    'reasoning': record['reasoning'],
                    'confidence': record['confidence'],
                    'stars': record['stars'],
                    'conceptual_similarity': record['conceptual_similarity'],
                    'tech_stack': record['tech_stack'],
                    'related_patterns': record['related_patterns']
                }
                patterns.append(pattern)
        
        # Group by architectural approach (extracted from reasoning)
        approaches = {}
        for pattern in patterns:
            # Simple grouping by first keyword in reasoning
            reasoning = pattern['reasoning'] or ""
            approach_key = reasoning.split()[0] if reasoning else "unknown"
            
            if approach_key not in approaches:
                approaches[approach_key] = []
            approaches[approach_key].append(pattern)
        
        return {
            'patterns': patterns,
            'approaches': approaches,
            'query': goal,
            'method': 'cross_pattern_discovery',
            'embedding_time_ms': embed_meta['duration_ms'],
            'total_approaches': len(approaches)
        }
    
    def find_similar_patterns(
        self,
        pattern_name: str,
        top_k: int = 5,
        min_similarity: float = 0.6
    ) -> Dict:
        """
        Find patterns similar to a given pattern (for backup suggestions).
        
        Args:
            pattern_name: Name of reference pattern
            top_k: Number of similar patterns to return
            min_similarity: Minimum similarity threshold
        
        Returns:
            Dictionary with similar patterns and metadata
        """
        query, params = self.query_builder.build_similar_patterns(
            pattern_name,
            top_k,
            min_similarity
        )
        
        with self.neo4j.session() as session:
            result = session.run(query, **params)
            
            similar = []
            for record in result:
                pattern = {
                    'name': record['name'],
                    'reasoning': record['reasoning'],
                    'confidence': record['confidence'],
                    'stars': record['stars'],
                    'similarity': record['similarity'],
                    'shared_technologies': record['shared_techs'],
                    'all_technologies': record['technologies'],
                    'tech_overlap_count': record['tech_overlap']
                }
                similar.append(pattern)
            
            return {
                'reference_pattern': pattern_name,
                'similar_patterns': similar,
                'count': len(similar),
                'method': 'vector_similarity'
            }
    
    # ========================================================================
    # ENHANCED: Override Parent Methods with Semantic Defaults
    # ========================================================================
    
    def find_patterns_for_spec(
        self,
        spec_dict: dict,
        top_k: int = 5,
        mode: str = 'hybrid'
    ) -> Dict:
        """
        Enhanced version that uses hybrid search by default.
        
        Args:
            spec_dict: SPEC dictionary with 'goal' key
            top_k: Number of patterns to return
            mode: 'hybrid' (default), 'semantic', or 'structural' (original)
        
        Returns:
            Pattern recommendations with confidence scores
        """
        goal = spec_dict.get('goal', '')
        
        if mode == 'hybrid':
            # Use hybrid semantic + structural search
            constraints = {
                'technologies': spec_dict.get('tech_stack', {}).get('languages', []),
                'deployment_type': spec_dict.get('deployment_type'),
                'min_stars': 5000
            }
            return self.find_patterns_hybrid(goal, constraints, top_k)
        
        elif mode == 'semantic':
            # Pure semantic search
            return self.find_patterns_semantic(goal, top_k)
        
        else:
            # Fall back to original structural method
            return super().find_patterns_for_spec(spec_dict, top_k)
    
    def verify_spec_feasibility(
        self,
        spec_dict: dict,
        use_semantic: bool = True
    ) -> Dict:
        """
        Enhanced feasibility check using semantic search.
        
        Args:
            spec_dict: SPEC dictionary
            use_semantic: If True, uses hybrid search for verification
        
        Returns:
            Feasibility assessment with confidence scores
        """
        if use_semantic:
            goal = spec_dict.get('goal', '')
            result = self.find_patterns_hybrid(goal, top_k=10)
            patterns = result['patterns']
            
            if not patterns:
                return {
                    'feasibility_score': 0.2,
                    'confidence': 'low',
                    'supporting_patterns': [],
                    'concerns': ['No similar patterns found via semantic search'],
                    'recommendations': ['Consider more proven approaches', 'Simplify requirements']
                }
            
            # Calculate feasibility from composite scores
            avg_composite = sum(p['composite_score'] for p in patterns) / len(patterns)
            top_composite = patterns[0]['composite_score']
            
            feasibility_score = (avg_composite * 0.4) + (top_composite * 0.6)
            
            if feasibility_score > 0.7:
                confidence = 'high'
            elif feasibility_score > 0.5:
                confidence = 'medium'
            else:
                confidence = 'low'
            
            return {
                'feasibility_score': round(feasibility_score, 2),
                'confidence': confidence,
                'supporting_patterns': patterns[:5],
                'concerns': [] if confidence != 'low' else ['Lower than ideal confidence score'],
                'recommendations': [patterns[0]['explanation']] if patterns else [],
                'method': 'semantic_hybrid'
            }
        else:
            # Fall back to original method
            return super().verify_spec_feasibility(spec_dict)


# Convenience function for backward compatibility
def create_interface(enable_semantic: bool = True) -> PatternQueryInterface:
    """
    Factory function to create appropriate interface.
    
    Args:
        enable_semantic: If True, returns semantic-enabled interface
    
    Returns:
        PatternQueryInterface or PatternQueryInterfaceSemantic
    """
    if enable_semantic:
        return PatternQueryInterfaceSemantic()
    else:
        return PatternQueryInterface()


# Example usage
if __name__ == "__main__":
    print("Testing PatternQueryInterfaceSemantic...\n")
    
    # Initialize interface
    interface = PatternQueryInterfaceSemantic()
    
    # Test 1: Semantic search
    print("Test 1: Semantic Search")
    print("="*70)
    result = interface.find_patterns_semantic(
        goal="Build a desktop file manager application",
        top_k=5
    )
    print(f"Found {len(result['patterns'])} patterns")
    print(f"Embedding time: {result['embedding_time_ms']}ms")
    for i, p in enumerate(result['patterns'][:3], 1):
        print(f"\n{i}. {p['name']}")
        print(f"   Composite: {p['composite_score']:.3f} ({p['recommendation']})")
        print(f"   Semantic: {p['breakdown']['semantic_match']:.3f}")
    
    # Test 2: Hybrid search
    print("\n\nTest 2: Hybrid Search")
    print("="*70)
    result = interface.find_patterns_hybrid(
        goal="Real-time chat application with message history",
        constraints={
            'technologies': ['nodejs', 'websocket'],
            'min_stars': 5000
        },
        top_k=5
    )
    print(f"Found {len(result['patterns'])} patterns")
    print(f"\n{result['user_review_text']}")
    
    # Test 3: Cross-pattern discovery
    print("\n\nTest 3: Cross-Pattern Discovery")
    print("="*70)
    result = interface.discover_alternatives(
        goal="Event-driven file processing system",
        min_similarity=0.7
    )
    print(f"Found {len(result['patterns'])} conceptually similar patterns")
    print(f"Grouped into {result['total_approaches']} architectural approaches")
    
    # Close interface
    interface.close()
    
    print("\n✓ PatternQueryInterfaceSemantic test complete!")
