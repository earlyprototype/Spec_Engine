# query_patterns.py
# Query graph for pattern recommendations

import os
from neo4j import GraphDatabase

class PatternQuery:
    def __init__(self):
        self.neo4j = GraphDatabase.driver(
            os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
        )
    
    def recommend_pattern(self, requirements):
        """
        Get pattern recommendations for requirements.
        
        Args:
            requirements: dict with type, domain, context
        
        Returns:
            List of recommended patterns with confidence
        """
        with self.neo4j.session() as session:
            result = session.run("""
                MATCH (r:Requirement)
                WHERE r.type = $req_type
                  AND r.domain = $req_domain
                MATCH (r)-[:SOLVED_BY]->(p:Pattern)
                MATCH (p)-[:REQUIRES]->(c:Constraint)
                OPTIONAL MATCH (p)-[:USES]->(t:Technology)
                
                RETURN 
                    p.name AS pattern,
                    p.confidence AS confidence,
                    p.source_repo AS source,
                    p.stars AS stars,
                    collect(DISTINCT c.rule) AS constraints,
                    collect(DISTINCT t.name) AS technologies
                
                ORDER BY p.stars DESC
                LIMIT 5
            """,
                req_type=requirements['type'],
                req_domain=requirements['domain']
            )
            
            return [dict(record) for record in result]
    
    def search_by_technology(self, tech_name):
        """
        Find patterns that use a specific technology.
        
        Args:
            tech_name: Technology name (e.g., "react", "postgres")
        
        Returns:
            List of patterns using this technology
        """
        with self.neo4j.session() as session:
            result = session.run("""
                MATCH (t:Technology {name: $tech_name})
                MATCH (p:Pattern)-[:USES]->(t)
                MATCH (r:Requirement)-[:SOLVED_BY]->(p)
                
                RETURN 
                    p.name AS pattern,
                    p.confidence AS confidence,
                    p.source_repo AS source,
                    p.stars AS stars,
                    r.type AS requirement_type,
                    r.domain AS requirement_domain
                
                ORDER BY p.stars DESC
                LIMIT 10
            """,
                tech_name=tech_name
            )
            
            return [dict(record) for record in result]
    
    def find_anti_patterns(self, requirements):
        """
        Find anti-patterns to avoid for given requirements.
        
        Args:
            requirements: dict with type, domain, context
        
        Returns:
            List of anti-patterns with reasons
        """
        with self.neo4j.session() as session:
            result = session.run("""
                MATCH (r:Requirement)
                WHERE r.type = $req_type
                  AND r.domain = $req_domain
                MATCH (r)-[:AVOID]->(ap:AntiPattern)
                
                RETURN 
                    ap.name AS anti_pattern,
                    ap.why_fails AS reason,
                    ap.alternative AS recommended_instead
                
                LIMIT 5
            """,
                req_type=requirements['type'],
                req_domain=requirements['domain']
            )
            
            return [dict(record) for record in result]
    
    def get_pattern_details(self, pattern_name):
        """
        Get full details of a specific pattern.
        
        Args:
            pattern_name: Name of the pattern
        
        Returns:
            Dict with all pattern information
        """
        with self.neo4j.session() as session:
            result = session.run("""
                MATCH (p:Pattern {name: $pattern_name})
                MATCH (r:Requirement)-[:SOLVED_BY]->(p)
                MATCH (p)-[:REQUIRES]->(c:Constraint)
                OPTIONAL MATCH (p)-[:USES]->(t:Technology)
                
                RETURN 
                    p.name AS pattern,
                    p.confidence AS confidence,
                    p.source_repo AS source,
                    p.stars AS stars,
                    p.reasoning AS reasoning,
                    r.type AS requirement_type,
                    r.domain AS requirement_domain,
                    collect(DISTINCT c.rule) AS constraints,
                    collect(DISTINCT {name: t.name, role: p.role}) AS technologies
            """,
                pattern_name=pattern_name
            )
            
            record = result.single()
            return dict(record) if record else None
    
    def get_statistics(self):
        """
        Get graph statistics.
        
        Returns:
            Dict with counts of nodes and relationships
        """
        with self.neo4j.session() as session:
            result = session.run("""
                MATCH (p:Pattern)
                WITH count(p) as pattern_count
                MATCH (r:Requirement)
                WITH pattern_count, count(r) as requirement_count
                MATCH (t:Technology)
                WITH pattern_count, requirement_count, count(t) as tech_count
                MATCH (c:Constraint)
                WITH pattern_count, requirement_count, tech_count, count(c) as constraint_count
                
                RETURN 
                    pattern_count,
                    requirement_count,
                    tech_count,
                    constraint_count
            """)
            
            record = result.single()
            return dict(record) if record else {}

# Test with Dashboard requirements
if __name__ == "__main__":
    query = PatternQuery()
    
    dashboard_requirements = {
        'type': 'data_management',
        'domain': 'file_system',
        'context': ['existing_files', 'web_ui']
    }
    
    print("=== Pattern Recommendations ===")
    recommendations = query.recommend_pattern(dashboard_requirements)
    
    for rec in recommendations:
        print(f"\n{rec['pattern']} (confidence: {rec['confidence']})")
        print(f"  Stars: {rec['stars']}")
        print(f"  Source: {rec['source']}")
        print(f"  Constraints: {rec['constraints']}")
        print(f"  Technologies: {rec['technologies']}")
    
    print("\n=== Graph Statistics ===")
    stats = query.get_statistics()
    print(f"Patterns: {stats.get('pattern_count', 0)}")
    print(f"Requirements: {stats.get('requirement_count', 0)}")
    print(f"Technologies: {stats.get('tech_count', 0)}")
    print(f"Constraints: {stats.get('constraint_count', 0)}")
