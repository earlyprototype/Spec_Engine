# pattern_query.py
# Python interface for querying the knowledge graph

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from typing import List, Dict, Optional

load_dotenv()

class PatternQuery:
    """Query interface for architectural pattern knowledge graph."""
    
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            auth=(os.getenv("NEO4J_USER", "neo4j"), 
                  os.getenv("NEO4J_PASSWORD", "password"))
        )
    
    def close(self):
        """Close database connection."""
        self.driver.close()
    
    def recommend_patterns(
        self,
        requirement_type: str,
        domain: Optional[str] = None,
        technologies: Optional[List[str]] = None,
        min_stars: int = 1000,
        confidence: str = "high"
    ) -> List[Dict]:
        """
        Get pattern recommendations based on requirements.
        
        Args:
            requirement_type: Type of requirement (e.g., 'data_management')
            domain: Specific domain (e.g., 'file_system')
            technologies: List of preferred technologies (e.g., ['typescript', 'react'])
            min_stars: Minimum GitHub stars
            confidence: Pattern confidence ('high', 'medium', 'low')
        
        Returns:
            List of recommended patterns with metadata
        """
        with self.driver.session() as session:
            query = """
                MATCH (r:Requirement {type: $req_type})-[:SOLVED_BY]->(p:Pattern)
                WHERE p.stars >= $min_stars
                  AND p.confidence = $confidence
            """
            
            if domain:
                query += " AND r.domain = $domain"
            
            query += """
                OPTIONAL MATCH (p)-[:USES]->(t:Technology)
                OPTIONAL MATCH (p)-[:REQUIRES]->(c:Constraint)
            """
            
            if technologies:
                query += """
                WITH p, r, collect(DISTINCT t.name) AS all_techs, 
                     collect(DISTINCT c.rule) AS constraints
                WHERE any(tech IN $technologies WHERE tech IN all_techs)
                """
            else:
                query += """
                WITH p, r, collect(DISTINCT t.name) AS all_techs,
                     collect(DISTINCT c.rule) AS constraints
                """
            
            query += """
                RETURN p.name AS pattern,
                       p.confidence AS confidence,
                       p.stars AS stars,
                       p.source_repo AS source,
                       p.reasoning AS reasoning,
                       all_techs AS technologies,
                       constraints
                ORDER BY p.stars DESC
                LIMIT 10
            """
            
            params = {
                "req_type": requirement_type,
                "min_stars": min_stars,
                "confidence": confidence
            }
            
            if domain:
                params["domain"] = domain
            
            if technologies:
                params["technologies"] = technologies
            
            result = session.run(query, params)
            
            return [dict(record) for record in result]
    
    def get_pattern_details(self, pattern_name: str) -> Dict:
        """Get complete details for a specific pattern."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Pattern {name: $pattern_name})
                OPTIONAL MATCH (p)-[:USES]->(t:Technology)
                OPTIONAL MATCH (p)-[:REQUIRES]->(c:Constraint)
                OPTIONAL MATCH (r:Requirement)-[:SOLVED_BY]->(p)
                RETURN p.name AS pattern,
                       p.confidence AS confidence,
                       p.stars AS stars,
                       p.source_repo AS source,
                       p.reasoning AS reasoning,
                       collect(DISTINCT {name: t.name}) AS technologies,
                       collect(DISTINCT c.rule) AS constraints,
                       r.type AS requirement_type,
                       r.domain AS requirement_domain
            """, pattern_name=pattern_name)
            
            record = result.single()
            return dict(record) if record else None
    
    def find_similar_patterns(
        self,
        pattern_name: str,
        limit: int = 5
    ) -> List[Dict]:
        """Find patterns similar to a given pattern (by shared technologies)."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p1:Pattern {name: $pattern_name})-[:USES]->(t:Technology)<-[:USES]-(p2:Pattern)
                WHERE p1 <> p2
                WITH p2, collect(DISTINCT t.name) AS shared_techs
                RETURN p2.name AS pattern,
                       p2.confidence AS confidence,
                       p2.stars AS stars,
                       shared_techs AS shared_technologies,
                       size(shared_techs) AS similarity_score
                ORDER BY similarity_score DESC, p2.stars DESC
                LIMIT $limit
            """, pattern_name=pattern_name, limit=limit)
            
            return [dict(record) for record in result]
    
    def get_technology_stack(self, pattern_name: str) -> List[Dict]:
        """Get the complete technology stack for a pattern."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Pattern {name: $pattern_name})-[r:USES]->(t:Technology)
                RETURN t.name AS technology,
                       r.role AS role
                ORDER BY 
                    CASE r.role
                        WHEN 'primary' THEN 1
                        WHEN 'framework' THEN 2
                        WHEN 'runtime' THEN 3
                        WHEN 'library' THEN 4
                        WHEN 'cache' THEN 5
                        WHEN 'queue' THEN 6
                        ELSE 7
                    END
            """, pattern_name=pattern_name)
            
            return [dict(record) for record in result]
    
    def validate_spec_requirements(
        self,
        requirement_type: str,
        domain: str,
        technologies: List[str]
    ) -> Dict:
        """
        Validate SPEC requirements against known patterns.
        
        Returns confidence score and recommendations.
        """
        patterns = self.recommend_patterns(
            requirement_type=requirement_type,
            domain=domain,
            technologies=technologies,
            min_stars=5000
        )
        
        if not patterns:
            return {
                "confidence": "low",
                "message": "No established patterns found for this combination",
                "recommendation": "Consider reviewing requirements or exploring alternative approaches"
            }
        
        top_pattern = patterns[0]
        
        # Calculate confidence based on star count and pattern confidence
        if top_pattern['stars'] > 20000 and top_pattern['confidence'] == 'high':
            confidence = "high"
        elif top_pattern['stars'] > 10000:
            confidence = "medium"
        else:
            confidence = "low"
        
        return {
            "confidence": confidence,
            "validated_pattern": top_pattern['pattern'],
            "stars": top_pattern['stars'],
            "reasoning": top_pattern['reasoning'],
            "recommended_technologies": top_pattern['technologies'],
            "constraints": top_pattern['constraints'],
            "source": top_pattern['source']
        }

# Example usage
if __name__ == "__main__":
    query = PatternQuery()
    
    # Example 1: Recommend patterns for file management
    print("=== File Management Patterns ===")
    patterns = query.recommend_patterns(
        requirement_type="data_management",
        domain="file_system",
        technologies=["typescript", "sqlite"]
    )
    
    for p in patterns:
        print(f"\n{p['pattern']} ({p['stars']} stars)")
        print(f"  Technologies: {', '.join(p['technologies'])}")
        print(f"  Source: {p['source']}")
    
    # Example 2: Get pattern details
    print("\n=== Pattern Details ===")
    if patterns:
        details = query.get_pattern_details(patterns[0]['pattern'])
        if details:
            print(f"Pattern: {details['pattern']}")
            print(f"Reasoning: {details['reasoning']}")
    
    # Example 3: Validate SPEC requirements
    print("\n=== Validate SPEC Requirements ===")
    validation = query.validate_spec_requirements(
        requirement_type="data_management",
        domain="file_system",
        technologies=["typescript", "react", "sqlite"]
    )
    
    print(f"Confidence: {validation.get('confidence', 'N/A')}")
    if 'validated_pattern' in validation:
        print(f"Validated Pattern: {validation['validated_pattern']}")
        print(f"Recommended Technologies: {', '.join(validation['recommended_technologies'])}")
    else:
        print(f"Message: {validation.get('message', 'No validation performed')}")
    
    query.close()
