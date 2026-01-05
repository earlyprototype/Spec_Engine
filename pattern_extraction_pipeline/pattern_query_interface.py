# pattern_query_interface.py
# LLM-friendly interface for querying architectural patterns during SPEC creation

import os
import json
from dotenv import load_dotenv
from neo4j import GraphDatabase
import google.generativeai as genai

load_dotenv()


class PatternQueryInterface:
    """
    Query interface optimized for LLM-assisted SPEC building.
    Translates natural language requirements into pattern recommendations.
    """
    
    def __init__(self):
        # Neo4j connection
        neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        neo4j_password = os.getenv("NEO4J_PASSWORD")
        
        if not neo4j_password:
            raise ValueError("NEO4J_PASSWORD not set in environment")
        
        self.neo4j = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        
        # Gemini LLM for semantic matching
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.llm = genai.GenerativeModel('gemini-2.0-flash-exp')
        else:
            self.llm = None
    
    def close(self):
        """Close Neo4j connection."""
        self.neo4j.close()
    
    # ========================================================================
    # PRIMARY INTERFACE: SPEC-to-Pattern Matching
    # ========================================================================
    
    def find_patterns_for_spec(self, spec_dict: dict, top_k: int = 5) -> dict:
        """
        Given a SPEC (as a dict), find relevant architectural patterns.
        
        Args:
            spec_dict: Dictionary with keys like 'goal', 'tech_stack', 'deployment_type', etc.
            top_k: Number of top patterns to return
        
        Returns:
            {
                'recommended_patterns': [list of patterns with confidence scores],
                'alternative_patterns': [patterns with lower confidence],
                'technologies': {tech_name: [patterns using this tech]},
                'constraints': {constraint: [patterns with this constraint]},
                'reasoning': 'Why these patterns were selected'
            }
        """
        # Extract key information from SPEC
        goal = spec_dict.get('goal', '')
        tech_stack = spec_dict.get('tech_stack', {})
        deployment_type = spec_dict.get('deployment_type', '')
        user_type = spec_dict.get('user_type', '')
        
        # Use LLM to analyze requirements and generate query strategy
        if self.llm:
            analysis = self._llm_analyze_spec(spec_dict)
            req_type = analysis.get('requirement_type', 'general')
            req_domain = analysis.get('requirement_domain', 'general')
            key_constraints = analysis.get('key_constraints', [])
            key_techs = analysis.get('key_technologies', [])
        else:
            # Fallback: basic extraction
            req_type = self._infer_requirement_type(goal)
            req_domain = self._infer_domain(goal)
            key_constraints = []
            key_techs = list(tech_stack.values()) if isinstance(tech_stack, dict) else []
        
        # Query Neo4j for matching patterns
        patterns = self._query_patterns(
            req_type=req_type,
            req_domain=req_domain,
            technologies=key_techs,
            constraints=key_constraints,
            top_k=top_k * 2  # Get more candidates for filtering
        )
        
        # Rank patterns using LLM semantic matching
        if self.llm and patterns:
            ranked_patterns = self._llm_rank_patterns(spec_dict, patterns, top_k)
        else:
            ranked_patterns = patterns[:top_k]
        
        # Group patterns by technology and constraints
        tech_groups = self._group_by_technology(patterns)
        constraint_groups = self._group_by_constraints(patterns)
        
        return {
            'recommended_patterns': ranked_patterns[:top_k],
            'alternative_patterns': ranked_patterns[top_k:top_k*2],
            'technologies': tech_groups,
            'constraints': constraint_groups,
            'reasoning': self._generate_reasoning(ranked_patterns[:top_k], spec_dict)
        }
    
    # ========================================================================
    # DIRECT QUERIES: Specific Pattern Lookups
    # ========================================================================
    
    def query_by_technology(self, tech_name: str, role: str = None) -> list:
        """
        Find patterns that use a specific technology.
        
        Args:
            tech_name: Technology name (e.g., 'react', 'flask', 'sqlite')
            role: Optional role filter ('primary', 'cache', 'ui', etc.)
        
        Returns:
            List of patterns with metadata
        """
        with self.neo4j.session() as session:
            if role:
                result = session.run("""
                    MATCH (t:Technology {name: $tech_name})<-[u:USES]-(p:Pattern)
                    WHERE u.role = $role
                    OPTIONAL MATCH (r:Requirement)-[:SOLVED_BY]->(p)
                    OPTIONAL MATCH (p)-[:REQUIRES]->(c:Constraint)
                    RETURN p, r, collect(DISTINCT c.rule) as constraints, u.role as role
                    ORDER BY p.stars DESC
                """, tech_name=tech_name.lower(), role=role.lower())
            else:
                result = session.run("""
                    MATCH (t:Technology {name: $tech_name})<-[u:USES]-(p:Pattern)
                    OPTIONAL MATCH (r:Requirement)-[:SOLVED_BY]->(p)
                    OPTIONAL MATCH (p)-[:REQUIRES]->(c:Constraint)
                    RETURN p, r, collect(DISTINCT c.rule) as constraints, u.role as role
                    ORDER BY p.stars DESC
                """, tech_name=tech_name.lower())
            
            return [self._format_pattern_result(record) for record in result]
    
    def query_by_requirement(self, req_type: str, req_domain: str = None) -> list:
        """
        Find patterns that solve a specific requirement type/domain.
        
        Args:
            req_type: Requirement type (e.g., 'data_management', 'ui_component')
            req_domain: Optional domain (e.g., 'file_system', 'e-commerce')
        
        Returns:
            List of patterns
        """
        with self.neo4j.session() as session:
            if req_domain:
                result = session.run("""
                    MATCH (r:Requirement {type: $req_type, domain: $req_domain})-[:SOLVED_BY]->(p:Pattern)
                    OPTIONAL MATCH (p)-[:USES]->(t:Technology)
                    OPTIONAL MATCH (p)-[:REQUIRES]->(c:Constraint)
                    RETURN p, r, 
                           collect(DISTINCT {name: t.name, role: 'unknown'}) as technologies,
                           collect(DISTINCT c.rule) as constraints
                    ORDER BY p.confidence DESC, p.stars DESC
                """, req_type=req_type, req_domain=req_domain)
            else:
                result = session.run("""
                    MATCH (r:Requirement {type: $req_type})-[:SOLVED_BY]->(p:Pattern)
                    OPTIONAL MATCH (p)-[:USES]->(t:Technology)
                    OPTIONAL MATCH (p)-[:REQUIRES]->(c:Constraint)
                    RETURN p, r,
                           collect(DISTINCT {name: t.name, role: 'unknown'}) as technologies,
                           collect(DISTINCT c.rule) as constraints
                    ORDER BY p.confidence DESC, p.stars DESC
                """, req_type=req_type)
            
            return [self._format_pattern_result(record) for record in result]
    
    def query_by_constraint(self, constraint: str) -> list:
        """Find patterns with a specific constraint."""
        with self.neo4j.session() as session:
            result = session.run("""
                MATCH (c:Constraint {rule: $constraint})<-[:REQUIRES]-(p:Pattern)
                OPTIONAL MATCH (r:Requirement)-[:SOLVED_BY]->(p)
                OPTIONAL MATCH (p)-[:USES]->(t:Technology)
                RETURN p, r,
                       collect(DISTINCT {name: t.name, role: 'unknown'}) as technologies
                ORDER BY p.stars DESC
            """, constraint=constraint)
            
            return [self._format_pattern_result(record) for record in result]
    
    def natural_language_query(self, query: str, top_k: int = 5) -> dict:
        """
        Natural language query interface.
        
        Example: "Find patterns for building a file browser with React"
        
        Returns:
            {
                'patterns': [list of matching patterns],
                'interpretation': 'How the query was interpreted',
                'suggestions': ['Related queries you might want to try']
            }
        """
        if not self.llm:
            return {
                'error': 'LLM not configured. Set GEMINI_API_KEY in .env',
                'patterns': [],
                'suggestions': []
            }
        
        # Use LLM to parse natural language query
        interpretation = self._llm_interpret_query(query)
        
        # Execute structured query based on interpretation
        patterns = self._query_patterns(
            req_type=interpretation.get('requirement_type'),
            req_domain=interpretation.get('domain'),
            technologies=interpretation.get('technologies', []),
            constraints=interpretation.get('constraints', []),
            top_k=top_k
        )
        
        return {
            'patterns': patterns,
            'interpretation': interpretation.get('interpretation', query),
            'suggestions': interpretation.get('suggestions', [])
        }
    
    # ========================================================================
    # VERIFICATION: Check SPEC Against Patterns
    # ========================================================================
    
    def verify_spec_feasibility(self, spec_dict: dict) -> dict:
        """
        Verify if a SPEC is feasible based on existing patterns.
        
        Returns:
            {
                'feasibility_score': 0.0-1.0,
                'confidence': 'high/medium/low',
                'supporting_patterns': [patterns that support this approach],
                'concerns': [list of potential issues],
                'recommendations': [suggested modifications]
            }
        """
        patterns = self.find_patterns_for_spec(spec_dict, top_k=10)
        
        recommended = patterns['recommended_patterns']
        
        if len(recommended) == 0:
            return {
                'feasibility_score': 0.2,
                'confidence': 'low',
                'supporting_patterns': [],
                'concerns': ['No similar patterns found in knowledge base'],
                'recommendations': ['Consider using more proven technologies', 'Simplify architecture']
            }
        
        # Calculate feasibility based on pattern matches
        avg_confidence = sum(1 if p.get('confidence') == 'high' else 0.5 for p in recommended) / len(recommended)
        avg_stars = sum(p.get('stars', 0) for p in recommended) / len(recommended)
        
        feasibility_score = (avg_confidence * 0.6) + (min(avg_stars / 10000, 1.0) * 0.4)
        
        # Generate concerns and recommendations using LLM
        if self.llm:
            analysis = self._llm_verify_spec(spec_dict, recommended)
        else:
            analysis = {
                'concerns': [],
                'recommendations': [],
                'confidence': 'medium' if feasibility_score > 0.5 else 'low'
            }
        
        return {
            'feasibility_score': round(feasibility_score, 2),
            'confidence': analysis.get('confidence', 'medium'),
            'supporting_patterns': recommended,
            'concerns': analysis.get('concerns', []),
            'recommendations': analysis.get('recommendations', [])
        }
    
    # ========================================================================
    # INTERNAL: Neo4j Query Helpers
    # ========================================================================
    
    def _query_patterns(self, req_type=None, req_domain=None, technologies=None, 
                       constraints=None, top_k=10):
        """Internal method to query patterns with multiple filters."""
        with self.neo4j.session() as session:
            # Build dynamic Cypher query
            query_parts = []
            params = {'top_k': top_k}
            
            if req_type:
                query_parts.append("MATCH (r:Requirement {type: $req_type})-[:SOLVED_BY]->(p:Pattern)")
                params['req_type'] = req_type
                if req_domain:
                    query_parts.append("WHERE r.domain = $req_domain")
                    params['req_domain'] = req_domain
            else:
                query_parts.append("MATCH (p:Pattern)")
            
            if technologies:
                query_parts.append("MATCH (p)-[:USES]->(t:Technology)")
                query_parts.append("WHERE t.name IN $technologies")
                params['technologies'] = [t.lower() for t in technologies]
            
            query_parts.append("OPTIONAL MATCH (req:Requirement)-[:SOLVED_BY]->(p)")
            query_parts.append("OPTIONAL MATCH (p)-[:USES]->(tech:Technology)")
            query_parts.append("OPTIONAL MATCH (p)-[:REQUIRES]->(c:Constraint)")
            query_parts.append("""
                RETURN p, req,
                       collect(DISTINCT {name: tech.name, role: 'unknown'}) as technologies,
                       collect(DISTINCT c.rule) as constraints
                ORDER BY p.confidence DESC, p.stars DESC
                LIMIT $top_k
            """)
            
            query = "\n".join(query_parts)
            result = session.run(query, **params)
            
            return [self._format_pattern_result(record) for record in result]
    
    def _format_pattern_result(self, record) -> dict:
        """Format Neo4j record into clean dict."""
        p = record['p']
        r = record.get('r')
        
        return {
            'pattern_name': p['name'],
            'confidence': p['confidence'],
            'stars': p['stars'],
            'source_repo': p['source_repo'],
            'reasoning': p.get('reasoning', ''),
            'requirement': {
                'type': r['type'] if r else 'unknown',
                'domain': r['domain'] if r else 'unknown'
            },
            'technologies': record.get('technologies', []),
            'constraints': record.get('constraints', [])
        }
    
    # ========================================================================
    # INTERNAL: LLM-Powered Analysis
    # ========================================================================
    
    def _llm_analyze_spec(self, spec_dict: dict) -> dict:
        """Use LLM to analyze SPEC and extract structured requirements."""
        prompt = f"""Analyze this SPEC and extract structured requirements.

SPEC:
{json.dumps(spec_dict, indent=2)}

Return JSON with:
{{
  "requirement_type": "data_management|ui_component|api_service|cli_tool|real_time|etc",
  "requirement_domain": "file_system|e-commerce|authentication|media|etc",
  "key_technologies": ["tech1", "tech2"],
  "key_constraints": ["constraint1", "constraint2"],
  "interpretation": "Brief summary of requirements"
}}
"""
        
        response = self.llm.generate_content(prompt)
        text = response.text.strip()
        
        # Extract JSON
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text:
            text = text.split('```')[1].split('```')[0].strip()
        
        try:
            return json.loads(text)
        except:
            return {
                'requirement_type': 'general',
                'requirement_domain': 'general',
                'key_technologies': [],
                'key_constraints': []
            }
    
    def _llm_rank_patterns(self, spec_dict: dict, patterns: list, top_k: int) -> list:
        """Use LLM to semantically rank patterns based on SPEC requirements."""
        if not patterns:
            return []
        
        # Limit to top 20 for LLM analysis (avoid token limits)
        patterns_sample = patterns[:20]
        
        prompt = f"""Rank these architectural patterns based on relevance to the SPEC.

SPEC GOAL: {spec_dict.get('goal', 'Not specified')}
TECH STACK: {spec_dict.get('tech_stack', {})}
DEPLOYMENT: {spec_dict.get('deployment_type', 'Not specified')}

PATTERNS:
{json.dumps([{
    'id': i,
    'name': p['pattern_name'],
    'stars': p['stars'],
    'technologies': p['technologies'],
    'reasoning': p['reasoning']
} for i, p in enumerate(patterns_sample)], indent=2)}

Return JSON array of pattern IDs ranked by relevance (most relevant first):
["0", "3", "1", ...]

Only return the top {top_k} most relevant IDs.
"""
        
        response = self.llm.generate_content(prompt)
        text = response.text.strip()
        
        # Extract JSON array
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text:
            text = text.split('```')[1].split('```')[0].strip()
        
        try:
            ranked_ids = json.loads(text)
            return [patterns_sample[int(i)] for i in ranked_ids if int(i) < len(patterns_sample)]
        except:
            # Fallback: return original order
            return patterns_sample[:top_k]
    
    def _llm_interpret_query(self, query: str) -> dict:
        """Use LLM to interpret natural language query."""
        prompt = f"""Interpret this natural language query about architectural patterns.

QUERY: {query}

Return JSON:
{{
  "requirement_type": "data_management|ui_component|etc",
  "domain": "file_system|e-commerce|etc",
  "technologies": ["tech1", "tech2"],
  "constraints": ["constraint1"],
  "interpretation": "What the user is looking for",
  "suggestions": ["Related query 1", "Related query 2"]
}}
"""
        
        response = self.llm.generate_content(prompt)
        text = response.text.strip()
        
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text:
            text = text.split('```')[1].split('```')[0].strip()
        
        try:
            return json.loads(text)
        except:
            return {
                'requirement_type': 'general',
                'domain': 'general',
                'technologies': [],
                'constraints': [],
                'interpretation': query,
                'suggestions': []
            }
    
    def _llm_verify_spec(self, spec_dict: dict, patterns: list) -> dict:
        """Use LLM to verify SPEC feasibility based on patterns."""
        prompt = f"""Verify this SPEC's feasibility based on proven patterns.

SPEC:
{json.dumps(spec_dict, indent=2)}

SUPPORTING PATTERNS:
{json.dumps([{
    'name': p['pattern_name'],
    'stars': p['stars'],
    'technologies': p['technologies'],
    'reasoning': p['reasoning']
} for p in patterns[:5]], indent=2)}

Return JSON:
{{
  "confidence": "high|medium|low",
  "concerns": ["Concern 1", "Concern 2"],
  "recommendations": ["Recommendation 1", "Recommendation 2"]
}}
"""
        
        response = self.llm.generate_content(prompt)
        text = response.text.strip()
        
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text:
            text = text.split('```')[1].split('```')[0].strip()
        
        try:
            return json.loads(text)
        except:
            return {
                'confidence': 'medium',
                'concerns': [],
                'recommendations': []
            }
    
    # ========================================================================
    # HELPERS
    # ========================================================================
    
    def _infer_requirement_type(self, goal: str) -> str:
        """Simple keyword-based requirement type inference."""
        goal_lower = goal.lower()
        if 'file' in goal_lower or 'browse' in goal_lower:
            return 'data_management'
        elif 'dashboard' in goal_lower or 'ui' in goal_lower:
            return 'ui_component'
        elif 'api' in goal_lower or 'backend' in goal_lower:
            return 'api_service'
        elif 'cli' in goal_lower or 'command' in goal_lower:
            return 'cli_tool'
        else:
            return 'general'
    
    def _infer_domain(self, goal: str) -> str:
        """Simple keyword-based domain inference."""
        goal_lower = goal.lower()
        if 'file' in goal_lower:
            return 'file_system'
        elif 'shop' in goal_lower or 'store' in goal_lower:
            return 'e-commerce'
        elif 'auth' in goal_lower or 'login' in goal_lower:
            return 'authentication'
        else:
            return 'general'
    
    def _group_by_technology(self, patterns: list) -> dict:
        """Group patterns by technology."""
        groups = {}
        for pattern in patterns:
            for tech in pattern.get('technologies', []):
                tech_name = tech['name']
                if tech_name not in groups:
                    groups[tech_name] = []
                groups[tech_name].append(pattern)
        return groups
    
    def _group_by_constraints(self, patterns: list) -> dict:
        """Group patterns by constraints."""
        groups = {}
        for pattern in patterns:
            for constraint in pattern.get('constraints', []):
                if constraint not in groups:
                    groups[constraint] = []
                groups[constraint].append(pattern)
        return groups
    
    def _generate_reasoning(self, patterns: list, spec_dict: dict) -> str:
        """Generate human-readable reasoning for pattern selection."""
        if not patterns:
            return "No matching patterns found in knowledge base."
        
        tech_count = {}
        for p in patterns:
            for tech in p.get('technologies', []):
                tech_count[tech['name']] = tech_count.get(tech['name'], 0) + 1
        
        common_techs = sorted(tech_count.items(), key=lambda x: x[1], reverse=True)[:3]
        tech_list = ', '.join([f"{t[0]} ({t[1]} patterns)" for t in common_techs])
        
        avg_stars = sum(p['stars'] for p in patterns) / len(patterns)
        
        return f"Selected {len(patterns)} patterns based on SPEC requirements. Common technologies: {tech_list}. Average popularity: {int(avg_stars)} stars."


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Query architectural patterns")
    parser.add_argument('--tech', help='Query by technology')
    parser.add_argument('--requirement', help='Query by requirement type')
    parser.add_argument('--domain', help='Requirement domain')
    parser.add_argument('--query', help='Natural language query')
    parser.add_argument('--spec-file', help='Path to SPEC JSON file for analysis')
    
    args = parser.parse_args()
    
    interface = PatternQueryInterface()
    
    try:
        if args.tech:
            patterns = interface.query_by_technology(args.tech)
            print(f"\nPatterns using {args.tech}:")
            for p in patterns:
                print(f"  - {p['pattern_name']} ({p['stars']} stars)")
                print(f"    Repo: {p['source_repo']}")
                print()
        
        elif args.requirement:
            patterns = interface.query_by_requirement(args.requirement, args.domain)
            print(f"\nPatterns for {args.requirement}" + (f"/{args.domain}" if args.domain else "") + ":")
            for p in patterns:
                print(f"  - {p['pattern_name']} ({p['stars']} stars)")
                print(f"    Repo: {p['source_repo']}")
                print()
        
        elif args.query:
            result = interface.natural_language_query(args.query)
            print(f"\nInterpretation: {result['interpretation']}")
            print(f"\nFound {len(result['patterns'])} patterns:")
            for p in result['patterns']:
                print(f"  - {p['pattern_name']} ({p['stars']} stars)")
                print(f"    Repo: {p['source_repo']}")
                print()
        
        elif args.spec_file:
            with open(args.spec_file, 'r') as f:
                spec_dict = json.load(f)
            
            verification = interface.verify_spec_feasibility(spec_dict)
            print(f"\nFeasibility Score: {verification['feasibility_score']}")
            print(f"Confidence: {verification['confidence']}")
            print(f"\nSupporting Patterns: {len(verification['supporting_patterns'])}")
            for p in verification['supporting_patterns']:
                print(f"  - {p['pattern_name']} ({p['stars']} stars)")
            
            if verification['concerns']:
                print("\nConcerns:")
                for c in verification['concerns']:
                    print(f"  - {c}")
            
            if verification['recommendations']:
                print("\nRecommendations:")
                for r in verification['recommendations']:
                    print(f"  - {r}")
        
        else:
            parser.print_help()
    
    finally:
        interface.close()


if __name__ == "__main__":
    main()
