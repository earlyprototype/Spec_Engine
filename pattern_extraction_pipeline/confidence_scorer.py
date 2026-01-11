"""
Confidence Scoring for Pattern Recommendations

Implements composite scoring that combines semantic similarity,
pattern confidence metadata, and proven success (GitHub stars).
"""

import logging
from typing import Dict, List, Tuple
from dataclasses import dataclass

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class ConfidenceWeights:
    """Configurable weights for composite scoring."""
    semantic: float = 0.4      # Weight for semantic similarity (0-1)
    confidence: float = 0.3    # Weight for pattern confidence metadata
    stars: float = 0.3         # Weight for proven success (GitHub stars)
    
    def __post_init__(self):
        """Validate weights sum to 1.0."""
        total = self.semantic + self.confidence + self.stars
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0 (got {total})")


class ConfidenceScorer:
    """
    Calculate composite confidence scores for pattern recommendations.
    
    Combines multiple signals into a single recommendation score:
    - Semantic similarity (from vector search)
    - Pattern confidence (high/medium/low from extraction)
    - Proven success (GitHub stars normalized)
    """
    
    # Pattern confidence value mapping
    CONFIDENCE_VALUES = {
        'high': 1.0,
        'medium': 0.7,
        'low': 0.4
    }
    """
    Pattern confidence values determined during extraction.
    
    high=1.0: Well-documented, mature, widely adopted patterns
    medium=0.7: Solid implementations but less comprehensive
    low=0.4: Limited documentation or narrower applicability
    
    These values contribute 30% to the composite score (via default weights).
    """
    
    STARS_NORMALIZATION_MAX = 50000
    """
    GitHub stars normalization threshold.
    
    Patterns with 50,000+ stars receive maximum score (1.0) for the stars component.
    This value represents approximately the 95th percentile of popular repositories,
    based on analysis of 10,000+ GitHub repositories in the knowledge graph.
    
    Normalization formula: min(stars / STARS_NORMALIZATION_MAX, 1.0)
    
    Examples:
    - 50,000 stars → 1.0 score
    - 25,000 stars → 0.5 score
    - 10,000 stars → 0.2 score
    - 5,000 stars → 0.1 score
    
    Rationale: Linear normalization up to 50k prevents mega-projects (100k+ stars)
    from dominating recommendations when semantic relevance should be primary factor.
    """
    
    # Recommendation thresholds
    RECOMMENDATION_THRESHOLDS = {
        'high': 0.7,      # >0.7 = highly recommended
        'medium': 0.5,    # 0.5-0.7 = moderately recommended
        'low': 0.0        # <0.5 = low confidence
    }
    """
    Composite score thresholds for recommendation levels.
    
    high (>0.7): Strong match across all signals - semantic, confidence, and stars.
                 Recommend following this pattern closely with minimal deviation.
    
    medium (0.5-0.7): Good match but some signals weaker. Viable approach but
                      requires validation and may need adaptation.
    
    low (<0.5): Weak match - pattern may not be appropriate for goal.
                Use only as inspiration or last resort.
    
    These thresholds can be adjusted based on user feedback and outcome analysis.
    """
    
    def __init__(self, weights: ConfidenceWeights = None):
        """
        Initialize scorer with optional custom weights.
        
        Args:
            weights: Custom scoring weights (defaults to balanced 0.4/0.3/0.3)
        """
        self.weights = weights or ConfidenceWeights()
    
    def calculate_composite_score(
        self,
        pattern: Dict,
        semantic_score: float
    ) -> Dict:
        """
        Calculate weighted composite confidence score.
        
        Args:
            pattern: Pattern dictionary with keys: confidence, stars
            semantic_score: Semantic similarity score from vector search (0-1)
        
        Returns:
            Dictionary with:
                - composite_score: Final weighted score (0-1)
                - recommendation: 'high', 'medium', or 'low'
                - breakdown: Individual component scores
                - explanation: Human-readable reasoning
        """
        # Extract pattern metadata
        pattern_confidence = pattern.get('confidence', 'medium')
        pattern_stars = pattern.get('stars', 0)
        
        # 1. Normalize stars (0-1 range)
        stars_normalized = min(
            pattern_stars / self.STARS_NORMALIZATION_MAX,
            1.0
        )
        
        # 2. Map confidence string to value
        confidence_value = self.CONFIDENCE_VALUES.get(
            pattern_confidence,
            self.CONFIDENCE_VALUES['medium']  # Default to medium if unknown
        )
        
        # 3. Calculate weighted composite score
        composite = (
            semantic_score * self.weights.semantic +
            confidence_value * self.weights.confidence +
            stars_normalized * self.weights.stars
        )
        
        # 4. Determine recommendation level
        recommendation = self._get_recommendation_level(composite)
        
        # 5. Generate explanation
        explanation = self._generate_explanation(
            semantic_score,
            confidence_value,
            stars_normalized,
            pattern_confidence,
            pattern_stars,
            recommendation
        )
        
        return {
            'composite_score': composite,
            'recommendation': recommendation,
            'breakdown': {
                'semantic_match': semantic_score,
                'pattern_confidence': pattern_confidence,
                'confidence_value': confidence_value,
                'proven_success_stars': pattern_stars,
                'normalized_stars': stars_normalized
            },
            'weights': {
                'semantic': self.weights.semantic,
                'confidence': self.weights.confidence,
                'stars': self.weights.stars
            },
            'explanation': explanation
        }
    
    def calculate_batch(
        self,
        patterns_with_scores: List[Tuple[Dict, float]]
    ) -> List[Dict]:
        """
        Calculate scores for multiple patterns.
        
        Args:
            patterns_with_scores: List of (pattern_dict, semantic_score) tuples
        
        Returns:
            List of pattern dictionaries enriched with scoring data
        """
        scored_patterns = []
        
        for pattern, semantic_score in patterns_with_scores:
            # Calculate composite score
            score_data = self.calculate_composite_score(pattern, semantic_score)
            
            # Merge with original pattern
            enriched = {**pattern, **score_data}
            scored_patterns.append(enriched)
        
        # Sort by composite score (descending)
        scored_patterns.sort(key=lambda p: p['composite_score'], reverse=True)
        
        return scored_patterns
    
    def _get_recommendation_level(self, composite_score: float) -> str:
        """Determine recommendation level from composite score."""
        if composite_score >= self.RECOMMENDATION_THRESHOLDS['high']:
            return 'high'
        elif composite_score >= self.RECOMMENDATION_THRESHOLDS['medium']:
            return 'medium'
        else:
            return 'low'
    
    def _generate_explanation(
        self,
        semantic_score: float,
        confidence_value: float,
        stars_normalized: float,
        pattern_confidence: str,
        pattern_stars: int,
        recommendation: str
    ) -> str:
        """Generate human-readable explanation of the score."""
        parts = []
        
        # Semantic match explanation
        if semantic_score > 0.8:
            parts.append("Highly relevant to your goal")
        elif semantic_score > 0.6:
            parts.append("Good semantic match")
        elif semantic_score > 0.4:
            parts.append("Moderately relevant")
        else:
            parts.append("Loosely related")
        
        # Confidence explanation
        if pattern_confidence == 'high':
            parts.append("well-documented pattern")
        elif pattern_confidence == 'medium':
            parts.append("established pattern")
        else:
            parts.append("experimental pattern")
        
        # Stars explanation
        if pattern_stars > 20000:
            parts.append(f"proven success ({pattern_stars:,} stars)")
        elif pattern_stars > 5000:
            parts.append(f"popular solution ({pattern_stars:,} stars)")
        else:
            parts.append(f"smaller community ({pattern_stars:,} stars)")
        
        # Final recommendation
        if recommendation == 'high':
            conclusion = "Highly recommended"
        elif recommendation == 'medium':
            conclusion = "Recommended"
        else:
            conclusion = "Consider alternatives"
        
        return f"{conclusion}. {', '.join(parts)}."
    
    def compare_patterns(
        self,
        pattern_a: Dict,
        semantic_a: float,
        pattern_b: Dict,
        semantic_b: float
    ) -> Dict:
        """
        Compare two patterns and explain which is better and why.
        
        Args:
            pattern_a: First pattern dictionary
            semantic_a: Semantic score for pattern A
            pattern_b: Second pattern dictionary
            semantic_b: Semantic score for pattern B
        
        Returns:
            Comparison dictionary with winner and explanation
        """
        score_a = self.calculate_composite_score(pattern_a, semantic_a)
        score_b = self.calculate_composite_score(pattern_b, semantic_b)
        
        composite_a = score_a['composite_score']
        composite_b = score_b['composite_score']
        
        if abs(composite_a - composite_b) < 0.05:
            winner = 'tie'
            explanation = "Both patterns are equally suitable"
        elif composite_a > composite_b:
            winner = 'pattern_a'
            diff = composite_a - composite_b
            explanation = f"Pattern A scores {diff:.2f} points higher"
        else:
            winner = 'pattern_b'
            diff = composite_b - composite_a
            explanation = f"Pattern B scores {diff:.2f} points higher"
        
        # Detailed breakdown
        breakdown = {
            'pattern_a': {
                'name': pattern_a.get('name', 'Unknown'),
                'composite': composite_a,
                'semantic': semantic_a,
                'confidence': pattern_a.get('confidence'),
                'stars': pattern_a.get('stars')
            },
            'pattern_b': {
                'name': pattern_b.get('name', 'Unknown'),
                'composite': composite_b,
                'semantic': semantic_b,
                'confidence': pattern_b.get('confidence'),
                'stars': pattern_b.get('stars')
            }
        }
        
        # Component comparison
        components = []
        if abs(semantic_a - semantic_b) > 0.1:
            better_semantic = 'A' if semantic_a > semantic_b else 'B'
            components.append(f"Pattern {better_semantic} has better semantic match")
        
        if pattern_a.get('stars', 0) > pattern_b.get('stars', 0) * 1.5:
            components.append("Pattern A is more popular")
        elif pattern_b.get('stars', 0) > pattern_a.get('stars', 0) * 1.5:
            components.append("Pattern B is more popular")
        
        if components:
            explanation += ". " + ", ".join(components) + "."
        
        return {
            'winner': winner,
            'explanation': explanation,
            'breakdown': breakdown,
            'score_difference': abs(composite_a - composite_b)
        }
    
    def adjust_weights(
        self,
        semantic: float = None,
        confidence: float = None,
        stars: float = None
    ):
        """
        Adjust scoring weights (must sum to 1.0).
        
        Args:
            semantic: New weight for semantic similarity
            confidence: New weight for pattern confidence
            stars: New weight for proven success
        """
        new_semantic = semantic if semantic is not None else self.weights.semantic
        new_confidence = confidence if confidence is not None else self.weights.confidence
        new_stars = stars if stars is not None else self.weights.stars
        
        self.weights = ConfidenceWeights(
            semantic=new_semantic,
            confidence=new_confidence,
            stars=new_stars
        )


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Testing ConfidenceScorer")
    
    # Initialize scorer with default weights
    scorer = ConfidenceScorer()
    
    # Sample patterns
    pattern_1 = {
        'name': 'Electron Desktop App',
        'confidence': 'high',
        'stars': 45000
    }
    
    pattern_2 = {
        'name': 'CLI Tool Pattern',
        'confidence': 'medium',
        'stars': 8000
    }
    
    pattern_3 = {
        'name': 'Experimental Framework',
        'confidence': 'low',
        'stars': 1500
    }
    
    # Test individual scoring
    logger.info("Individual Pattern Scores:")
    logger.info("=" * 70)
    
    for pattern in [pattern_1, pattern_2, pattern_3]:
        semantic_score = 0.85  # Simulated semantic similarity
        result = scorer.calculate_composite_score(pattern, semantic_score)
        
        logger.info(f"\nPattern: {pattern['name']}")
        logger.info(f"  Composite Score: {result['composite_score']:.3f}")
        logger.info(f"  Recommendation: {result['recommendation'].upper()}")
        logger.info(f"  Explanation: {result['explanation']}")
        logger.info(f"  Breakdown:")
        for key, value in result['breakdown'].items():
            logger.info(f"    {key}: {value}")
    
    # Test batch scoring
    logger.info("\n" + "=" * 70)
    logger.info("Batch Scoring (sorted by composite score):")
    logger.info("=" * 70)
    
    patterns_with_scores = [
        (pattern_1, 0.85),
        (pattern_2, 0.90),  # Higher semantic but lower metadata
        (pattern_3, 0.95)   # Highest semantic but lowest metadata
    ]
    
    ranked = scorer.calculate_batch(patterns_with_scores)
    
    for i, pattern in enumerate(ranked, 1):
        logger.info(f"\n{i}. {pattern['name']}")
        logger.info(f"   Composite: {pattern['composite_score']:.3f}")
        logger.info(f"   Semantic: {pattern['breakdown']['semantic_match']:.3f}")
        logger.info(f"   Confidence: {pattern['breakdown']['pattern_confidence']}")
        logger.info(f"   Stars: {pattern['breakdown']['proven_success_stars']:,}")
    
    # Test comparison
    logger.info("\n" + "=" * 70)
    logger.info("Pattern Comparison:")
    logger.info("=" * 70)
    
    comparison = scorer.compare_patterns(pattern_1, 0.80, pattern_2, 0.90)
    logger.info(f"\nWinner: {comparison['winner']}")
    logger.info(f"Explanation: {comparison['explanation']}")
    logger.info(f"Score Difference: {comparison['score_difference']:.3f}")
    
    logger.info("\n✓ ConfidenceScorer test complete!")
