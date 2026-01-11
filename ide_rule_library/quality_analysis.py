#!/usr/bin/env python3
"""
Quality score distribution analysis and smart threshold calculation.

Provides percentile-based thresholds instead of arbitrary hardcoded values.
"""

import os
from typing import Dict, List, Optional
from pathlib import Path
import yaml
from dotenv import load_dotenv
from neo4j import GraphDatabase

from ide_rule_library.logger import StructuredLogger
from ide_rule_library.exceptions import DatabaseError, MissingDataError

load_dotenv(override=True)


class QualityAnalyzer:
    """Analyze quality score distribution and calculate smart thresholds"""
    
    def __init__(self, neo4j_driver, logger):
        self.driver = neo4j_driver
        self.logger = logger
    
    def get_quality_distribution(self) -> Dict:
        """
        Calculate quality score distribution statistics.
        
        Returns:
            Dictionary with distribution metrics:
            - total: Total number of rules
            - mean: Average quality score
            - median: Median quality score
            - min: Minimum quality score
            - max: Maximum quality score
            - p10, p25, p50, p75, p90, p95: Percentiles
            - std_dev: Standard deviation
        """
        with self.driver.session() as session:
            try:
                result = session.run("""
                    MATCH (r:IDERule)
                    WHERE r.quality_score IS NOT NULL
                    WITH r.quality_score AS score
                    ORDER BY score
                    WITH collect(score) AS scores
                    RETURN 
                        size(scores) AS total,
                        reduce(sum = 0.0, x IN scores | sum + x) / size(scores) AS mean,
                        scores[toInteger(size(scores) * 0.10)] AS p10,
                        scores[toInteger(size(scores) * 0.25)] AS p25,
                        scores[toInteger(size(scores) * 0.50)] AS p50,
                        scores[toInteger(size(scores) * 0.75)] AS p75,
                        scores[toInteger(size(scores) * 0.90)] AS p90,
                        scores[toInteger(size(scores) * 0.95)] AS p95,
                        scores[0] AS min,
                        scores[size(scores) - 1] AS max
                """)
                
                record = result.single()
                
                if not record or record['total'] == 0:
                    raise MissingDataError("No rules with quality scores found in database")
                
                distribution = dict(record)
                
                # Calculate standard deviation
                std_result = session.run("""
                    MATCH (r:IDERule)
                    WHERE r.quality_score IS NOT NULL
                    WITH avg(r.quality_score) AS mean
                    MATCH (r:IDERule)
                    WHERE r.quality_score IS NOT NULL
                    WITH sqrt(avg((r.quality_score - mean) ^ 2)) AS std_dev
                    RETURN std_dev
                """)
                
                std_record = std_result.single()
                distribution['std_dev'] = std_record['std_dev'] if std_record else 0.0
                
                # Add median alias
                distribution['median'] = distribution['p50']
                
                self.logger.info(f"Analyzed {distribution['total']} rules with quality scores")
                
                return distribution
                
            except Exception as e:
                raise DatabaseError(f"Failed to calculate distribution: {e}") from e
    
    def get_confidence_distribution(self) -> Dict:
        """
        Get confidence level distribution.
        
        Returns:
            Dictionary with counts per confidence level
        """
        with self.driver.session() as session:
            try:
                result = session.run("""
                    MATCH (r:IDERule)
                    WHERE r.confidence_level IS NOT NULL
                    WITH r.confidence_level AS level
                    RETURN level, count(level) AS count
                    ORDER BY level
                """)
                
                distribution = {record['level']: record['count'] for record in result}
                
                return distribution
                
            except Exception as e:
                raise DatabaseError(f"Failed to get confidence distribution: {e}") from e
    
    def get_production_signal_stats(self) -> Dict:
        """
        Get production signal statistics.
        
        Returns:
            Dictionary with counts for each signal type
        """
        with self.driver.session() as session:
            try:
                result = session.run("""
                    MATCH (r:IDERule)
                    WHERE r.quality_score IS NOT NULL
                    RETURN 
                        count(r) AS total,
                        sum(CASE WHEN r.has_ci_cd THEN 1 ELSE 0 END) AS with_ci_cd,
                        sum(CASE WHEN r.has_deployment THEN 1 ELSE 0 END) AS with_deployment,
                        sum(CASE WHEN r.has_tests THEN 1 ELSE 0 END) AS with_tests,
                        sum(CASE WHEN r.has_monitoring THEN 1 ELSE 0 END) AS with_monitoring,
                        sum(CASE WHEN r.has_security THEN 1 ELSE 0 END) AS with_security,
                        sum(CASE WHEN r.has_ci_cd OR r.has_tests THEN 1 ELSE 0 END) AS with_any_production
                """)
                
                return dict(result.single())
                
            except Exception as e:
                raise DatabaseError(f"Failed to get production signal stats: {e}") from e
    
    def get_smart_threshold(self, percentile: int = 50, metric: str = 'quality_score') -> float:
        """
        Get smart threshold based on percentile.
        
        Args:
            percentile: Percentile to use (10, 25, 50, 75, 90, 95)
            metric: Metric to calculate threshold for ('quality_score' or 'confidence_level')
            
        Returns:
            Threshold value at the specified percentile
        """
        if percentile not in [10, 25, 50, 75, 90, 95]:
            raise ValueError(f"Invalid percentile: {percentile}. Must be one of [10, 25, 50, 75, 90, 95]")
        
        distribution = self.get_quality_distribution()
        
        threshold = distribution[f'p{percentile}']
        
        self.logger.info(f"Smart threshold at p{percentile}: {threshold:.1f}")
        
        return threshold
    
    def recommend_thresholds(self) -> Dict:
        """
        Recommend quality and confidence thresholds based on data distribution.
        
        Returns:
            Dictionary with recommended thresholds for different use cases
        """
        distribution = self.get_quality_distribution()
        confidence_dist = self.get_confidence_distribution()
        prod_stats = self.get_production_signal_stats()
        
        # Calculate percentages
        total = distribution['total']
        with_prod_pct = (prod_stats['with_any_production'] / total * 100) if total > 0 else 0
        
        recommendations = {
            'strict': {
                'min_quality_score': distribution['p75'],
                'min_confidence': 4,
                'require_production_signals': True,
                'description': 'High quality only (top 25%)',
                'expected_results_pct': 25
            },
            'balanced': {
                'min_quality_score': distribution['p50'],
                'min_confidence': 3,
                'require_production_signals': True,
                'description': 'Good quality (top 50%)',
                'expected_results_pct': 50 * (with_prod_pct / 100)
            },
            'permissive': {
                'min_quality_score': distribution['p25'],
                'min_confidence': 2,
                'require_production_signals': False,
                'description': 'Acceptable quality (top 75%)',
                'expected_results_pct': 75
            },
            'minimal': {
                'min_quality_score': distribution['p10'],
                'min_confidence': 1,
                'require_production_signals': False,
                'description': 'Any quality (top 90%)',
                'expected_results_pct': 90
            }
        }
        
        return recommendations
    
    def print_analysis_report(self):
        """Print comprehensive analysis report"""
        print("\n" + "="*70)
        print("QUALITY SCORE DISTRIBUTION ANALYSIS")
        print("="*70)
        
        # Quality distribution
        dist = self.get_quality_distribution()
        
        print("\nQuality Score Statistics:")
        print(f"  Total rules: {dist['total']}")
        print(f"  Mean: {dist['mean']:.1f}")
        print(f"  Median: {dist['median']:.1f}")
        print(f"  Std Dev: {dist['std_dev']:.1f}")
        print(f"  Range: {dist['min']:.1f} - {dist['max']:.1f}")
        
        print("\nPercentiles:")
        print(f"  P10 (bottom 10%): {dist['p10']:.1f}")
        print(f"  P25 (bottom 25%): {dist['p25']:.1f}")
        print(f"  P50 (median):     {dist['p50']:.1f}")
        print(f"  P75 (top 25%):    {dist['p75']:.1f}")
        print(f"  P90 (top 10%):    {dist['p90']:.1f}")
        print(f"  P95 (top 5%):     {dist['p95']:.1f}")
        
        # Confidence distribution
        conf_dist = self.get_confidence_distribution()
        
        print("\nConfidence Level Distribution:")
        for level in sorted(conf_dist.keys()):
            count = conf_dist[level]
            pct = (count / dist['total'] * 100) if dist['total'] > 0 else 0
            print(f"  Level {level}: {count:3d} rules ({pct:5.1f}%)")
        
        # Production signals
        prod_stats = self.get_production_signal_stats()
        
        print("\nProduction Signals:")
        print(f"  With CI/CD:      {prod_stats['with_ci_cd']:3d} ({prod_stats['with_ci_cd']/dist['total']*100:5.1f}%)")
        print(f"  With Deployment: {prod_stats['with_deployment']:3d} ({prod_stats['with_deployment']/dist['total']*100:5.1f}%)")
        print(f"  With Tests:      {prod_stats['with_tests']:3d} ({prod_stats['with_tests']/dist['total']*100:5.1f}%)")
        print(f"  With Monitoring: {prod_stats['with_monitoring']:3d} ({prod_stats['with_monitoring']/dist['total']*100:5.1f}%)")
        print(f"  With Security:   {prod_stats['with_security']:3d} ({prod_stats['with_security']/dist['total']*100:5.1f}%)")
        print(f"  With Any Prod:   {prod_stats['with_any_production']:3d} ({prod_stats['with_any_production']/dist['total']*100:5.1f}%)")
        
        # Recommendations
        recommendations = self.recommend_thresholds()
        
        print("\n" + "="*70)
        print("RECOMMENDED THRESHOLDS")
        print("="*70)
        
        for level, config in recommendations.items():
            print(f"\n{level.upper()} ({config['description']}):")
            print(f"  min_quality_score: {config['min_quality_score']:.1f}")
            print(f"  min_confidence: {config['min_confidence']}")
            print(f"  require_production_signals: {config['require_production_signals']}")
            print(f"  Expected results: ~{config['expected_results_pct']:.0f}% of database")
        
        print("\n" + "="*70)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze quality score distribution')
    parser.add_argument('--percentile', type=int, choices=[10, 25, 50, 75, 90, 95],
                       help='Get threshold at specific percentile')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Load config
    config_path = Path(__file__).parent / 'config.yaml'
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Setup logger
    logger = StructuredLogger("quality_analysis", config.get('logging', {}))
    
    # Connect to Neo4j
    uri = os.getenv('NEO4J_URI')
    user = os.getenv('NEO4J_USER')
    password = os.getenv('NEO4J_PASSWORD')
    
    if not all([uri, user, password]):
        logger.error("Missing Neo4j environment variables")
        return 1
    
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    try:
        analyzer = QualityAnalyzer(driver, logger)
        
        if args.percentile:
            threshold = analyzer.get_smart_threshold(args.percentile)
            if args.json:
                import json
                print(json.dumps({'percentile': args.percentile, 'threshold': threshold}))
            else:
                print(f"P{args.percentile} threshold: {threshold:.1f}")
        else:
            if args.json:
                import json
                dist = analyzer.get_quality_distribution()
                recommendations = analyzer.recommend_thresholds()
                output = {
                    'distribution': dist,
                    'recommendations': recommendations
                }
                print(json.dumps(output, indent=2))
            else:
                analyzer.print_analysis_report()
        
        return 0
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        return 1
        
    finally:
        driver.close()


if __name__ == '__main__':
    import sys
    sys.exit(main())
