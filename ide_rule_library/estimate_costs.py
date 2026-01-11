#!/usr/bin/env python3
"""
Cost estimation tool for Gemini API usage.

Estimates costs before running extraction or generation operations.
"""

import os
from pathlib import Path
from typing import Dict, Optional
import yaml
from dotenv import load_dotenv
from neo4j import GraphDatabase

from ide_rule_library.logger import StructuredLogger

load_dotenv(override=True)


class GeminiCostEstimator:
    """Estimate Gemini API costs for various operations"""
    
    # Gemini Flash pricing (as of 2025)
    PRICING = {
        'gemini-2.0-flash-exp': {
            'input_per_1m': 0.00,  # Free tier
            'output_per_1m': 0.00,  # Free tier
            'name': 'Gemini 2.0 Flash (Experimental)'
        },
        'gemini-1.5-flash': {
            'input_per_1m': 0.075,
            'output_per_1m': 0.30,
            'name': 'Gemini 1.5 Flash'
        },
        'gemini-1.5-pro': {
            'input_per_1m': 1.25,
            'output_per_1m': 5.00,
            'name': 'Gemini 1.5 Pro'
        },
        'text-embedding-004': {
            'input_per_1m': 0.00,  # Free
            'output_per_1m': 0.00,
            'name': 'Text Embedding 004'
        }
    }
    
    # Token estimates for different operations
    TOKEN_ESTIMATES = {
        'rule_extraction': {
            'input_tokens': 3500,  # Prompt + rule content
            'output_tokens': 1000,  # JSON response
            'description': 'Enhanced rule extraction with context analysis'
        },
        'cursorrules_synthesis': {
            'input_tokens': 8000,  # Multiple rules + synthesis prompt
            'output_tokens': 2000,  # Generated .cursorrules
            'description': '.cursorrules generation from examples'
        },
        'embedding_generation': {
            'input_tokens': 100,  # Query text
            'output_tokens': 0,  # Embeddings don't count as output
            'description': 'Query embedding for semantic search'
        }
    }
    
    def __init__(self, logger):
        self.logger = logger
    
    def estimate_extraction_cost(self, num_rules: int, model: str = 'gemini-2.0-flash-exp') -> Dict:
        """
        Estimate cost for extracting N rules.
        
        Args:
            num_rules: Number of rules to extract
            model: Model name
            
        Returns:
            Dictionary with cost breakdown
        """
        if model not in self.PRICING:
            self.logger.warning(f"Unknown model {model}, using gemini-1.5-flash pricing")
            model = 'gemini-1.5-flash'
        
        pricing = self.PRICING[model]
        estimates = self.TOKEN_ESTIMATES['rule_extraction']
        
        total_input_tokens = num_rules * estimates['input_tokens']
        total_output_tokens = num_rules * estimates['output_tokens']
        
        input_cost = (total_input_tokens / 1_000_000) * pricing['input_per_1m']
        output_cost = (total_output_tokens / 1_000_000) * pricing['output_per_1m']
        total_cost = input_cost + output_cost
        
        # Estimate time (roughly 2 seconds per rule)
        estimated_seconds = num_rules * 2
        estimated_minutes = estimated_seconds / 60
        
        return {
            'operation': 'Rule Extraction',
            'model': pricing['name'],
            'num_rules': num_rules,
            'total_input_tokens': total_input_tokens,
            'total_output_tokens': total_output_tokens,
            'input_cost': input_cost,
            'output_cost': output_cost,
            'total_cost': total_cost,
            'estimated_time_seconds': estimated_seconds,
            'estimated_time_minutes': estimated_minutes,
            'cost_per_rule': total_cost / num_rules if num_rules > 0 else 0
        }
    
    def estimate_generation_cost(self, num_generations: int = 1, model: str = 'gemini-2.0-flash-exp') -> Dict:
        """
        Estimate cost for generating .cursorrules files.
        
        Args:
            num_generations: Number of .cursorrules to generate
            model: Model name
            
        Returns:
            Dictionary with cost breakdown
        """
        if model not in self.PRICING:
            model = 'gemini-1.5-flash'
        
        pricing = self.PRICING[model]
        estimates = self.TOKEN_ESTIMATES['cursorrules_synthesis']
        
        total_input_tokens = num_generations * estimates['input_tokens']
        total_output_tokens = num_generations * estimates['output_tokens']
        
        input_cost = (total_input_tokens / 1_000_000) * pricing['input_per_1m']
        output_cost = (total_output_tokens / 1_000_000) * pricing['output_per_1m']
        total_cost = input_cost + output_cost
        
        estimated_seconds = num_generations * 10  # ~10 seconds per generation
        
        return {
            'operation': '.cursorrules Generation',
            'model': pricing['name'],
            'num_generations': num_generations,
            'total_input_tokens': total_input_tokens,
            'total_output_tokens': total_output_tokens,
            'input_cost': input_cost,
            'output_cost': output_cost,
            'total_cost': total_cost,
            'estimated_time_seconds': estimated_seconds,
            'cost_per_generation': total_cost / num_generations if num_generations > 0 else 0
        }
    
    def estimate_query_cost(self, num_queries: int = 1, embedding_model: str = 'text-embedding-004') -> Dict:
        """
        Estimate cost for semantic queries.
        
        Args:
            num_queries: Number of queries
            embedding_model: Embedding model name
            
        Returns:
            Dictionary with cost breakdown
        """
        pricing = self.PRICING.get(embedding_model, self.PRICING['text-embedding-004'])
        estimates = self.TOKEN_ESTIMATES['embedding_generation']
        
        total_input_tokens = num_queries * estimates['input_tokens']
        
        input_cost = (total_input_tokens / 1_000_000) * pricing['input_per_1m']
        
        return {
            'operation': 'Semantic Query',
            'model': pricing['name'],
            'num_queries': num_queries,
            'total_input_tokens': total_input_tokens,
            'total_output_tokens': 0,
            'input_cost': input_cost,
            'output_cost': 0.0,
            'total_cost': input_cost,
            'estimated_time_seconds': num_queries * 0.5,
            'cost_per_query': input_cost / num_queries if num_queries > 0 else 0
        }
    
    def get_database_stats(self, driver) -> Dict:
        """Get database statistics for cost estimation"""
        with driver.session() as session:
            result = session.run("""
                MATCH (r:IDERule)
                RETURN count(r) AS total_rules,
                       sum(CASE WHEN r.quality_score IS NULL THEN 1 ELSE 0 END) AS rules_without_quality
            """)
            
            record = result.single()
            return dict(record) if record else {'total_rules': 0, 'rules_without_quality': 0}
    
    def print_cost_estimate(self, estimate: Dict):
        """Print formatted cost estimate"""
        print("\n" + "="*70)
        print(f"COST ESTIMATE: {estimate['operation']}")
        print("="*70)
        print(f"Model: {estimate['model']}")
        
        if 'num_rules' in estimate:
            print(f"Number of rules: {estimate['num_rules']}")
        elif 'num_generations' in estimate:
            print(f"Number of generations: {estimate['num_generations']}")
        elif 'num_queries' in estimate:
            print(f"Number of queries: {estimate['num_queries']}")
        
        print(f"\nToken Usage:")
        print(f"  Input tokens:  {estimate['total_input_tokens']:,}")
        print(f"  Output tokens: {estimate['total_output_tokens']:,}")
        print(f"  Total tokens:  {estimate['total_input_tokens'] + estimate['total_output_tokens']:,}")
        
        print(f"\nCost Breakdown:")
        print(f"  Input cost:  ${estimate['input_cost']:.4f}")
        print(f"  Output cost: ${estimate['output_cost']:.4f}")
        print(f"  Total cost:  ${estimate['total_cost']:.4f}")
        
        if 'cost_per_rule' in estimate:
            print(f"  Per rule:    ${estimate['cost_per_rule']:.6f}")
        elif 'cost_per_generation' in estimate:
            print(f"  Per generation: ${estimate['cost_per_generation']:.6f}")
        elif 'cost_per_query' in estimate:
            print(f"  Per query:   ${estimate['cost_per_query']:.6f}")
        
        print(f"\nEstimated Time:")
        if estimate['estimated_time_seconds'] < 60:
            print(f"  {estimate['estimated_time_seconds']:.0f} seconds")
        else:
            minutes = estimate.get('estimated_time_minutes', estimate['estimated_time_seconds'] / 60)
            print(f"  {minutes:.1f} minutes ({estimate['estimated_time_seconds']:.0f} seconds)")
        
        print("="*70)
    
    def estimate_migration_cost(self, driver, model: str = 'gemini-2.0-flash-exp') -> Dict:
        """
        Estimate cost for migrating existing rules.
        
        Args:
            driver: Neo4j driver
            model: Model to use (not used for migration)
            
        Returns:
            Cost estimate dictionary
        """
        stats = self.get_database_stats(driver)
        rules_to_migrate = stats['rules_without_quality']
        
        if rules_to_migrate == 0:
            return {
                'operation': 'Migration',
                'message': 'No rules need migration',
                'total_cost': 0.0
            }
        
        # Migration uses CACHED data from Neo4j Pattern nodes
        # NO external API calls (GitHub or Gemini)
        return {
            'operation': 'Quality Score Migration',
            'rules_to_migrate': rules_to_migrate,
            'gemini_cost': 0.0,
            'github_api_calls': 0,  # Uses cached data from Pattern nodes
            'estimated_time_minutes': rules_to_migrate * 0.05,  # ~3 seconds per rule
            'total_cost': 0.0,
            'note': 'Migration uses cached repo data from Neo4j (no API calls, no cost)'
        }


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Estimate Gemini API costs')
    parser.add_argument('--operation', choices=['extraction', 'generation', 'query', 'migration', 'all'],
                       default='all', help='Operation to estimate')
    parser.add_argument('--num-rules', type=int, help='Number of rules (for extraction)')
    parser.add_argument('--num-generations', type=int, default=1, help='Number of generations')
    parser.add_argument('--num-queries', type=int, default=1, help='Number of queries')
    parser.add_argument('--model', default='gemini-2.0-flash-exp', help='Model to use')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Load config
    config_path = Path(__file__).parent / 'config.yaml'
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    logger = StructuredLogger("cost_estimator", config.get('logging', {}))
    estimator = GeminiCostEstimator(logger)
    
    # Connect to Neo4j for database stats
    uri = os.getenv('NEO4J_URI')
    user = os.getenv('NEO4J_USER')
    password = os.getenv('NEO4J_PASSWORD')
    
    driver = None
    if all([uri, user, password]):
        driver = GraphDatabase.driver(uri, auth=(user, password))
    
    try:
        estimates = []
        
        if args.operation in ['extraction', 'all']:
            if args.num_rules:
                num_rules = args.num_rules
            elif driver:
                stats = estimator.get_database_stats(driver)
                num_rules = stats['rules_without_quality']
            else:
                num_rules = 171  # Default estimate
            
            estimate = estimator.estimate_extraction_cost(num_rules, args.model)
            estimates.append(estimate)
            if not args.json:
                estimator.print_cost_estimate(estimate)
        
        if args.operation in ['generation', 'all']:
            estimate = estimator.estimate_generation_cost(args.num_generations, args.model)
            estimates.append(estimate)
            if not args.json:
                estimator.print_cost_estimate(estimate)
        
        if args.operation in ['query', 'all']:
            estimate = estimator.estimate_query_cost(args.num_queries)
            estimates.append(estimate)
            if not args.json:
                estimator.print_cost_estimate(estimate)
        
        if args.operation in ['migration', 'all'] and driver:
            estimate = estimator.estimate_migration_cost(driver, args.model)
            estimates.append(estimate)
            if not args.json:
                print("\n" + "="*70)
                print(f"MIGRATION ESTIMATE")
                print("="*70)
                print(f"Rules to migrate: {estimate.get('rules_to_migrate', 0)}")
                print(f"API calls: {estimate.get('github_api_calls', 0)} (uses cached data)")
                print(f"Gemini cost: ${estimate.get('gemini_cost', 0):.4f}")
                print(f"Estimated time: {estimate.get('estimated_time_minutes', 0):.1f} minutes")
                print(f"\n{estimate.get('note', '')}")
                print("="*70)
        
        if args.json:
            import json
            print(json.dumps(estimates, indent=2))
        
        return 0
        
    except Exception as e:
        logger.error(f"Cost estimation failed: {e}", exc_info=True)
        return 1
        
    finally:
        if driver:
            driver.close()


if __name__ == '__main__':
    import sys
    sys.exit(main())
