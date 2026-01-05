# example_spec_builder.py
# Demonstrates how an LLM would use the Pattern Query Interface during SPEC creation

import json
from pattern_query_interface import PatternQueryInterface


def build_spec_with_pattern_guidance(user_request: str):
    """
    Example: How an LLM builds a SPEC using the knowledge graph.
    
    This simulates what happens when a user says:
    "Build me a file browser application"
    """
    
    interface = PatternQueryInterface()
    
    try:
        print("="*70)
        print(f"USER REQUEST: {user_request}")
        print("="*70)
        print()
        
        # Step 1: Create initial SPEC draft from user request
        print("[LLM] Creating initial SPEC draft...")
        spec_draft = {
            'goal': user_request,
            'deployment_type': 'Web Application',  # inferred from "application"
            'user_type': 'general users',
            'tech_stack': {}  # To be filled based on patterns
        }
        
        # Step 2: Query knowledge graph for relevant patterns
        print("[LLM] Querying knowledge graph for relevant patterns...")
        print()
        
        patterns = interface.find_patterns_for_spec(spec_draft, top_k=5)
        
        print(f"Found {len(patterns['recommended_patterns'])} recommended patterns")
        print(f"Reasoning: {patterns['reasoning']}")
        print()
        
        # Step 3: Analyze patterns to inform tech stack decisions
        print("[LLM] Analyzing patterns to build tech stack...")
        print()
        
        tech_votes = {}
        for pattern in patterns['recommended_patterns']:
            print(f"  Pattern: {pattern['pattern_name']} ({pattern['stars']} stars)")
            print(f"    Source: {pattern['source_repo']}")
            print(f"    Technologies: {[t['name'] for t in pattern['technologies']]}")
            print(f"    Reasoning: {pattern['reasoning'][:100]}...")
            print()
            
            for tech in pattern['technologies']:
                tech_name = tech['name']
                tech_votes[tech_name] = tech_votes.get(tech_name, 0) + 1
        
        # Step 4: Build tech stack based on pattern analysis
        most_common_techs = sorted(tech_votes.items(), key=lambda x: x[1], reverse=True)
        
        print("[LLM] Tech stack recommendations based on patterns:")
        for tech, count in most_common_techs[:5]:
            print(f"  - {tech}: used in {count}/{len(patterns['recommended_patterns'])} patterns")
        print()
        
        # Step 5: Update SPEC with recommendations
        spec_draft['tech_stack'] = {
            'primary': most_common_techs[0][0] if most_common_techs else 'react',
            'recommended_techs': [t[0] for t in most_common_techs[:3]]
        }
        
        # Step 6: Extract common constraints
        all_constraints = []
        for pattern in patterns['recommended_patterns']:
            all_constraints.extend(pattern['constraints'])
        
        constraint_freq = {}
        for c in all_constraints:
            constraint_freq[c] = constraint_freq.get(c, 0) + 1
        
        common_constraints = [c for c, count in constraint_freq.items() if count >= 2]
        
        if common_constraints:
            print("[LLM] Common architectural constraints found:")
            for constraint in common_constraints:
                print(f"  - {constraint}")
            print()
            spec_draft['constraints'] = common_constraints
        
        # Step 7: Verify feasibility
        print("[LLM] Verifying SPEC feasibility...")
        verification = interface.verify_spec_feasibility(spec_draft)
        
        print(f"  Feasibility Score: {verification['feasibility_score']}")
        print(f"  Confidence: {verification['confidence']}")
        print()
        
        if verification['concerns']:
            print("  Concerns:")
            for concern in verification['concerns']:
                print(f"    - {concern}")
            print()
        
        if verification['recommendations']:
            print("  Recommendations:")
            for rec in verification['recommendations']:
                print(f"    - {rec}")
            print()
        
        # Step 8: Present final SPEC
        print("="*70)
        print("FINAL SPEC")
        print("="*70)
        print(json.dumps(spec_draft, indent=2))
        print()
        
        return spec_draft
    
    finally:
        interface.close()


def query_specific_technology(tech_name: str):
    """
    Example: User asks "Can I use Flask for this?"
    LLM queries knowledge graph to provide informed answer.
    """
    
    interface = PatternQueryInterface()
    
    try:
        print("="*70)
        print(f"USER QUESTION: Can I use {tech_name}?")
        print("="*70)
        print()
        
        patterns = interface.query_by_technology(tech_name)
        
        if not patterns:
            print(f"[LLM] No patterns found using {tech_name}.")
            print("This doesn't mean you can't use it, but there are no proven examples in the knowledge graph yet.")
            print()
            return
        
        print(f"[LLM] Found {len(patterns)} proven patterns using {tech_name}:")
        print()
        
        for i, pattern in enumerate(patterns[:3], 1):
            print(f"{i}. {pattern['pattern_name']} ({pattern['stars']} stars)")
            print(f"   Purpose: {pattern['requirement']['type']} / {pattern['requirement']['domain']}")
            print(f"   Repo: {pattern['source_repo']}")
            print(f"   Reasoning: {pattern['reasoning'][:150]}...")
            print()
        
        print(f"[LLM] Yes, {tech_name} is well-proven for these use cases. I recommend it.")
        print()
    
    finally:
        interface.close()


def natural_language_exploration(query: str):
    """
    Example: User asks open-ended question about patterns.
    """
    
    interface = PatternQueryInterface()
    
    try:
        print("="*70)
        print(f"USER QUERY: {query}")
        print("="*70)
        print()
        
        result = interface.natural_language_query(query, top_k=3)
        
        print(f"[LLM] Interpretation: {result['interpretation']}")
        print()
        
        if result['patterns']:
            print(f"Found {len(result['patterns'])} relevant patterns:")
            print()
            
            for i, pattern in enumerate(result['patterns'], 1):
                print(f"{i}. {pattern['pattern_name']} ({pattern['stars']} stars)")
                print(f"   Technologies: {', '.join([t['name'] for t in pattern['technologies']][:3])}")
                print(f"   {pattern['reasoning'][:120]}...")
                print()
        else:
            print("No patterns found for this query.")
            print()
        
        if result['suggestions']:
            print("You might also want to try:")
            for suggestion in result['suggestions']:
                print(f"  - {suggestion}")
            print()
    
    finally:
        interface.close()


if __name__ == "__main__":
    import sys
    
    print("\n" + "="*70)
    print("SPEC Builder with Pattern Guidance - Examples")
    print("="*70)
    print()
    
    # Example 1: Build SPEC with pattern guidance
    print("\nEXAMPLE 1: Building a SPEC with pattern guidance")
    print("-" * 70)
    spec = build_spec_with_pattern_guidance("Build a file browser application")
    
    print("\n" + "="*70)
    
    # Example 2: Query specific technology
    print("\nEXAMPLE 2: Checking if a technology is proven")
    print("-" * 70)
    query_specific_technology("react")
    
    print("\n" + "="*70)
    
    # Example 3: Natural language exploration
    print("\nEXAMPLE 3: Natural language pattern query")
    print("-" * 70)
    natural_language_exploration("Show me patterns for real-time dashboards")
    
    print("="*70)
    print("\nAll examples complete!")
    print()
