#!/usr/bin/env python3
"""
Enhanced .cursorrules generation with quality-aware synthesis.

Uses the enhanced query engine to find high-quality, context-appropriate rules
and synthesizes them with awareness of trade-offs and alternatives.
"""

import argparse
import os
import sys
import yaml
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv
from neo4j import GraphDatabase
import google.generativeai as genai

from ide_rule_library.enhanced_query_engine import EnhancedRuleQueryEngine
from ide_rule_library.logger import StructuredLogger
from ide_rule_library.exceptions import (
    NoRulesFoundError,
    DatabaseError,
    GeminiError,
    MissingEnvironmentVariableError
)
from ide_rule_library.retry_handler import call_gemini_with_retry

load_dotenv(override=True)


def format_rules_for_synthesis(rules: List[Dict]) -> str:
    """Format rules with quality metadata for Gemini synthesis"""
    formatted = []
    
    for i, rule in enumerate(rules, 1):
        quality = rule.get('repo_quality_score', 0)
        confidence = rule.get('confidence_level', 0)
        
        # Production signals
        signals = []
        if rule.get('has_ci_cd'): signals.append('CI/CD')
        if rule.get('has_tests'): signals.append('Tests')
        if rule.get('has_deployment'): signals.append('Deployment')
        signal_str = ', '.join(signals) if signals else 'None'
        
        # Context
        project_sizes = rule.get('suitable_project_sizes', [])
        team_sizes = rule.get('suitable_team_sizes', [])
        
        formatted.append(f"""
## Example {i}: {rule['source_repo']} 
**Quality Score:** {quality:.1f}/100 | **Confidence:** {confidence}/5 | **Stars:** {rule['stars']:,}
**Production Signals:** {signal_str}
**Updated:** {rule.get('days_since_update', 999)} days ago
**File:** {rule['file_path']}

**Purpose:** {rule['purpose']}

**Context (AI-inferred, unvalidated):**
- Suitable for: {', '.join(project_sizes) if project_sizes else 'All project sizes (best guess)'}
- Team sizes: {', '.join(team_sizes) if team_sizes else 'All team sizes (best guess)'}

**Key Practices:**
{chr(10).join(f"  - {practice}" for practice in rule.get('key_practices', [])[:10])}

**Trade-offs:**
Benefits: {', '.join(rule.get('trade_offs', {}).get('benefits', [])[:3])}
Costs: {', '.join(rule.get('trade_offs', {}).get('costs', [])[:3])}

**Alternatives:** {', '.join(rule.get('alternative_approaches', [])[:2]) if rule.get('alternative_approaches') else 'None mentioned'}

**Content Preview:**
```
{rule['content'][:800]}
...
```
""")
    
    return "\n".join(formatted)


def synthesize_with_validation(rules: List[Dict], description: str, 
                               technologies: List[str], project_type: str,
                               model_name: str, logger) -> str:
    """
    Synthesize .cursorrules with quality awareness and validation.
    
    Args:
        rules: List of rule dictionaries
        description: Project description
        technologies: List of technologies
        project_type: Type of project
        model_name: Gemini model name
        logger: Logger instance
        
    Returns:
        Generated .cursorrules content
        
    Raises:
        GeminiError: If synthesis fails
    """
    
    if not rules:
        raise ValueError("Cannot synthesize with empty rules list")
    
    # Calculate aggregate quality metrics
    avg_quality = sum(r.get('repo_quality_score', 0) for r in rules) / len(rules) if rules else 0
    avg_confidence = sum(r.get('confidence_level', 0) for r in rules) / len(rules) if rules else 0
    total_stars = sum(r.get('stars', 0) for r in rules)
    
    # Count production signals
    with_ci_cd = sum(1 for r in rules if r.get('has_ci_cd'))
    with_tests = sum(1 for r in rules if r.get('has_tests'))
    
    # Build synthesis prompt with quality context
    prompt = f"""
Generate a production-ready .cursorrules file for Cursor IDE.

PROJECT REQUIREMENTS:
- Description: {description}
- Technologies: {', '.join(technologies)}
- Project Type: {project_type}

SOURCE QUALITY METRICS:
- {len(rules)} high-quality examples analyzed
- Average quality score: {avg_quality:.1f}/100
- Average confidence level: {avg_confidence:.1f}/5
- Total GitHub stars: {total_stars:,}
- With CI/CD: {with_ci_cd}/{len(rules)}
- With Tests: {with_tests}/{len(rules)}

These examples were filtered for:
✓ Quality score > 60/100
✓ Confidence level >= 3/5
✓ Recently maintained (< 1 year)
✓ Production signals (CI/CD or tests)

VALIDATED PATTERNS (from proven, production-grade repos):
{format_rules_for_synthesis(rules)}

YOUR TASK:
Generate a comprehensive .cursorrules file that:

1. **Focuses on consensus patterns** - Include practices validated by multiple high-quality sources
2. **Matches project context** - Appropriate for the {project_type} project type
3. **Explains trade-offs** - When recommending complex patterns, mention costs/benefits
4. **Warns about anti-patterns** - Include "What to avoid" sections
5. **Provides alternatives** - When patterns conflict, explain the trade-offs
6. **Production-ready focus** - Prioritize patterns from repos with CI/CD and tests

FORMAT:
```
---
globs: **/*.{{ext1}},**/*.{{ext2}}
---

# Project Context
[Brief description tailored to user's requirements]

# Code Style & Conventions
[Consensus patterns from examples]

# Architecture
[Structural patterns with trade-offs explained]

# Best Practices
[Validated practices with reasoning]

# Anti-Patterns to Avoid
[What NOT to do based on examples' explicit warnings]

# Testing & Quality
[If examples have testing practices]

# Performance Considerations
[If mentioned in examples]

# Common Pitfalls
[Known issues from trade-offs and anti-patterns]
```

CRITICAL GUIDELINES:
- Be specific and actionable
- Include concrete examples where helpful
- Mention trade-offs for complex decisions
- Focus on patterns with consensus (multiple sources)
- Prioritize production-ready practices over tutorial code
- Keep it concise but comprehensive

Generate the .cursorrules file now.
"""
    
    try:
        model = genai.GenerativeModel(model_name)
        response = call_gemini_with_retry(
            model,
            prompt,
            max_attempts=3,
            logger=logger
        )
        
        if not response or not response.text:
            raise GeminiError("Empty response from Gemini during synthesis")
        
        return response.text.strip()
        
    except Exception as e:
        logger.error(f"Synthesis failed: {e}", exc_info=True)
        raise GeminiError(f"Failed to synthesize .cursorrules: {e}") from e


def generate_enhanced_cursorrules(
    description: str,
    technologies: List[str],
    project_type: str,
    project_size: str = 'medium',
    team_size: str = 'small',
    output_file: str = '.cursorrules',
    min_quality: float = 60.0,
    min_confidence: int = 3,
    top_k: int = 15
):
    """
    Generate enhanced .cursorrules with quality filtering.
    
    Args:
        description: Project description
        technologies: List of technologies
        project_type: Type of project
        project_size: Project size (small, medium, large)
        team_size: Team size (solo, small, medium, large)
        output_file: Output file path
        min_quality: Minimum quality score
        min_confidence: Minimum confidence level
        top_k: Number of examples to use
        
    Returns:
        True if successful, False otherwise
        
    Raises:
        MissingEnvironmentVariableError: If required env vars missing
        DatabaseError: If database connection fails
        NoRulesFoundError: If no rules found
        GeminiError: If Gemini API fails
    """
    
    # Load config first
    config_path = Path(__file__).parent / 'config.yaml'
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    logger = StructuredLogger("enhanced_generator", config.get('logging', {}))
    logger.info("Starting enhanced .cursorrules generation")
    
    # Validate environment variables
    uri = os.getenv('NEO4J_URI')
    user = os.getenv('NEO4J_USER')
    password = os.getenv('NEO4J_PASSWORD')
    
    if not uri:
        raise MissingEnvironmentVariableError("NEO4J_URI not set")
    if not user:
        raise MissingEnvironmentVariableError("NEO4J_USER not set")
    if not password:
        raise MissingEnvironmentVariableError("NEO4J_PASSWORD not set")
    
    # Connect to Neo4j
    try:
        neo4j_driver = GraphDatabase.driver(uri, auth=(user, password))
        # Test connection
        with neo4j_driver.session() as session:
            session.run("RETURN 1")
        logger.info("Neo4j connection successful")
    except Exception as e:
        raise DatabaseError(f"Failed to connect to Neo4j: {e}") from e
    
    try:
        # Initialize enhanced query engine
        engine = EnhancedRuleQueryEngine(
            neo4j_driver,
            logger,
            config['gemini']['embedding_model']
        )
        
        # Query with quality filters and fallback
        logger.info(f"Querying with quality filters (score>={min_quality}, confidence>={min_confidence})")
        
        try:
            rules = engine.query_rules_with_fallback(
                query=description,
                project_type=project_type,
                technologies=technologies,
                ide_type='cursor',
                min_quality_score=min_quality,
                min_confidence=min_confidence,
                max_days_since_update=365,
                require_production_signals=True,
                project_size=project_size,
                team_size=team_size,
                top_k=top_k,
                min_results=5  # Trigger fallback if fewer than 5 results
            )
        except NoRulesFoundError as e:
            print(f"\n[ERROR] {e}")
            print(f"\nDatabase may be empty or needs quality score migration.")
            print(f"Run migrate_quality_scores.py to backfill quality data.")
            return False
        
        print(f"\n{'='*60}")
        print(f"Generating .cursorrules for: {description}")
        print(f"{'='*60}")
        print(f"Technologies: {', '.join(technologies)}")
        print(f"Project Type: {project_type}")
        print(f"Project Size: {project_size}")
        print(f"Team Size: {team_size}")
        print(f"\nQuality Filters Applied:")
        print(f"  Min Quality Score: {min_quality}/100")
        print(f"  Min Confidence: {min_confidence}/5")
        print(f"  Production Signals: Required")
        print(f"\nFound {len(rules)} high-quality examples")
        
        # Show quality metrics
        avg_quality = sum(r.get('repo_quality_score', 0) for r in rules) / len(rules)
        avg_stars = sum(r.get('stars', 0) for r in rules) / len(rules)
        avg_confidence = sum(r.get('confidence_level', 0) for r in rules) / len(rules)
        
        print(f"  Average quality: {avg_quality:.1f}/100")
        print(f"  Average stars: {avg_stars:,.0f}")
        print(f"  Average confidence: {avg_confidence:.1f}/5")
        
        # Synthesize with Gemini
        print(f"\nSynthesizing with {config['gemini']['model']}...")
        
        cursorrules_content = synthesize_with_validation(
            rules,
            description,
            technologies,
            project_type,
            config['gemini']['model'],
            logger
        )
        
        # Write to file
        output_path = Path(output_file)
        output_path.write_text(cursorrules_content, encoding='utf-8')
        
        print(f"\n[OK] Generated {output_file}")
        print(f"     Based on {len(rules)} validated examples")
        print(f"     Average quality: {avg_quality:.1f}/100")
        print(f"     Total characters: {len(cursorrules_content):,}")
        
        logger.info("Successfully generated enhanced .cursorrules")
        
        return True
        
    except Exception as e:
        logger.error(f"Generation failed: {e}", exc_info=True)
        print(f"\n[ERROR] {e}")
        return False
    finally:
        neo4j_driver.close()


def main():
    parser = argparse.ArgumentParser(description='Generate enhanced .cursorrules with quality filtering')
    parser.add_argument('description', help='Project description')
    parser.add_argument('--tech', nargs='+', required=True, help='Technologies used')
    parser.add_argument('--type', required=True, help='Project type (api, web_app, cli, etc.)')
    parser.add_argument('--size', default='medium', choices=['small', 'medium', 'large'], 
                       help='Project size')
    parser.add_argument('--team', default='small', choices=['solo', 'small', 'medium', 'large'],
                       help='Team size')
    parser.add_argument('--output', default='.cursorrules', help='Output file path')
    parser.add_argument('--min-quality', type=float, default=60.0, help='Minimum quality score')
    parser.add_argument('--min-confidence', type=int, default=3, help='Minimum confidence level')
    parser.add_argument('--top-k', type=int, default=15, help='Number of examples to use')
    
    args = parser.parse_args()
    
    success = generate_enhanced_cursorrules(
        args.description,
        args.tech,
        args.type,
        args.size,
        args.team,
        args.output,
        args.min_quality,
        args.min_confidence,
        args.top_k
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
