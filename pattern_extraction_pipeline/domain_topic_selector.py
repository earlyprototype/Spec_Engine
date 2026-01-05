# domain_topic_selector.py
# LLM-powered domain and topic selector for pattern extraction

import os
import sys
import json
import argparse
import toml
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class DomainTopicSelector:
    """
    LLM-powered assistant for selecting appropriate GitHub topics and domains
    for pattern extraction based on project requirements.
    """
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def analyse_requirements(self, description: str, existing_techs: list = None) -> dict:
        """
        Analyse project requirements and suggest topics and domains.
        
        Args:
            description: Natural language description of the project
            existing_techs: List of technologies already selected
        
        Returns:
            Dictionary with suggested topics, domains, and queries
        """
        
        tech_context = ""
        if existing_techs:
            tech_context = f"\n\nExisting technologies: {', '.join(existing_techs)}"
        
        prompt = f"""You are an expert in software architecture and GitHub repository analysis.

Given this project description:
{description}{tech_context}

Provide recommendations for extracting relevant architectural patterns from GitHub.

Respond with a JSON object (no markdown, just raw JSON) with this exact structure:
{{
  "primary_topics": [
    {{"topic": "topic-name", "relevance": "why this topic is relevant", "estimated_repos": 100}}
  ],
  "secondary_topics": [
    {{"topic": "topic-name", "relevance": "why this topic is relevant", "estimated_repos": 50}}
  ],
  "recommended_domains": [
    {{"domain": "domain_name", "description": "what this domain covers", "priority": "high/medium/low"}}
  ],
  "suggested_queries": [
    {{"query": "topic:xxx stars:>5000", "purpose": "what patterns this finds", "limit": 20}}
  ],
  "tech_stack_suggestions": [
    {{"tech": "technology-name", "reason": "why this tech is commonly used"}}
  ],
  "estimated_extraction_time": "X-Y hours",
  "confidence": "high/medium/low"
}}

Guidelines:
- primary_topics: 3-5 most relevant GitHub topics
- secondary_topics: 3-5 alternative topics for broader coverage
- recommended_domains: Logical groupings for organising patterns
- suggested_queries: Ready-to-use GitHub search queries
- QUERY FORMATS (choose based on specificity needed):
  * Topic-based (narrow, specific): "topic:ecommerce stars:>5000" (use single topic only)
  * Keyword-based (broad, flexible): "ecommerce platform stars:>5000" (can combine multiple keywords)
  * Scoped keyword: "authentication in:description,readme stars:>10000" (search in specific fields)
- Use realistic star counts (>1000 for niche, >5000 for established, >10000 for popular)
- Mix both formats for comprehensive coverage
- Optimise for quality over quantity"""

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Clean up common JSON formatting issues
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()
            
            result = json.loads(result_text)
            return result
            
        except json.JSONDecodeError as e:
            print(f"Error parsing LLM response: {e}")
            print(f"Raw response: {response.text}")
            return self._fallback_recommendations(description)
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return self._fallback_recommendations(description)
    
    def _fallback_recommendations(self, description: str) -> dict:
        """Provide basic recommendations if LLM fails."""
        return {
            "primary_topics": [
                {"topic": "application", "relevance": "General application patterns", "estimated_repos": 500}
            ],
            "secondary_topics": [],
            "recommended_domains": [
                {"domain": "general_app", "description": "General application architecture", "priority": "medium"}
            ],
            "suggested_queries": [
                {"query": "stars:>5000", "purpose": "High-quality general patterns", "limit": 20}
            ],
            "tech_stack_suggestions": [],
            "estimated_extraction_time": "1-2 hours",
            "confidence": "low"
        }
    
    def analyse_from_constitution(self, constitution_path: str) -> dict:
        """
        Analyse project requirements from project_constitution.toml
        
        Args:
            constitution_path: Path to project_constitution.toml
        
        Returns:
            Analysis results with recommendations
        """
        try:
            const = toml.load(constitution_path)
            
            # Extract relevant information
            description = const.get('project', {}).get('description', '')
            if not description:
                description = f"A {const.get('project', {}).get('name', 'software project')}"
            
            # Add more context from constitution
            context_parts = [description]
            
            if 'requirements' in const:
                req_type = const['requirements'].get('type', '')
                domain = const['requirements'].get('domain', '')
                if req_type or domain:
                    context_parts.append(f"Requirement type: {req_type}, Domain: {domain}")
            
            if 'technologies' in const:
                tech_list = const['technologies'].get('required', [])
                if tech_list:
                    context_parts.append(f"Technologies: {', '.join(tech_list)}")
            
            full_description = ". ".join(context_parts)
            existing_techs = const.get('technologies', {}).get('required', [])
            
            return self.analyse_requirements(full_description, existing_techs)
            
        except Exception as e:
            print(f"Error reading constitution file: {e}")
            return None
    
    def interactive_mode(self):
        """Interactive CLI for getting recommendations."""
        print("="*70)
        print("Domain & Topic Selector - LLM-Powered Pattern Extraction Assistant")
        print("="*70)
        print()
        
        print("Describe your project (be specific about features and requirements):")
        print("Example: 'Building a real-time collaborative text editor with WebSocket support'")
        print()
        description = input("> ").strip()
        
        if not description:
            print("Error: Description cannot be empty")
            return
        
        print("\nDo you have any existing technologies in mind? (comma-separated, or press Enter to skip)")
        tech_input = input("> ").strip()
        existing_techs = [t.strip() for t in tech_input.split(",")] if tech_input else None
        
        print("\nAnalysing requirements...")
        print()
        
        result = self.analyse_requirements(description, existing_techs)
        self._display_results(result)
        
        print("\n" + "="*70)
        print("Would you like to generate a batch extraction script? (y/n)")
        if input("> ").strip().lower() == 'y':
            self._generate_batch_script(result)
    
    def _display_results(self, result: dict):
        """Display analysis results in a readable format."""
        print("="*70)
        print("RECOMMENDATIONS")
        print("="*70)
        print()
        
        print(f"Confidence: {result.get('confidence', 'unknown').upper()}")
        print(f"Estimated Extraction Time: {result.get('estimated_extraction_time', 'unknown')}")
        print()
        
        print("PRIMARY TOPICS (Most Relevant)")
        print("-" * 70)
        for topic in result.get('primary_topics', []):
            print(f"  {topic['topic']}")
            print(f"    Relevance: {topic['relevance']}")
            print(f"    Estimated repos: ~{topic['estimated_repos']}")
            print()
        
        if result.get('secondary_topics'):
            print("SECONDARY TOPICS (Broader Coverage)")
            print("-" * 70)
            for topic in result.get('secondary_topics', []):
                print(f"  {topic['topic']}")
                print(f"    Relevance: {topic['relevance']}")
                print()
        
        print("RECOMMENDED DOMAINS (Organisation)")
        print("-" * 70)
        for domain in result.get('recommended_domains', []):
            print(f"  {domain['domain']} [{domain['priority']}]")
            print(f"    {domain['description']}")
            print()
        
        print("SUGGESTED QUERIES (Ready to Use)")
        print("-" * 70)
        for query in result.get('suggested_queries', []):
            print(f"  {query['query']} (limit: {query['limit']})")
            print(f"    Purpose: {query['purpose']}")
            print()
        
        if result.get('tech_stack_suggestions'):
            print("TECHNOLOGY SUGGESTIONS")
            print("-" * 70)
            for tech in result.get('tech_stack_suggestions', []):
                print(f"  {tech['tech']}")
                print(f"    {tech['reason']}")
                print()
    
    def _generate_batch_script(self, result: dict):
        """Generate batch extraction script from recommendations."""
        script_content = """# batch_extract_custom.py
# Auto-generated batch extraction script
# Generated by domain_topic_selector.py

from pattern_extractor import PatternExtractor

extractor = PatternExtractor()

domains = [
"""
        
        for i, query_obj in enumerate(result.get('suggested_queries', [])):
            query = query_obj['query']
            limit = query_obj['limit']
            purpose = query_obj['purpose']
            domain_name = f"domain_{i+1}"
            
            script_content += f'    ("{query}", {limit}, "{domain_name}"),  # {purpose}\n'
        
        script_content += """]

total_extracted = 0

for query, limit, domain_name in domains:
    print(f"\\n{'='*60}")
    print(f"Extracting {domain_name} patterns...")
    print(f"{'='*60}")
    
    try:
        patterns = extractor.extract_patterns(query, limit=limit)
        total_extracted += len(patterns)
        print(f"[OK] {len(patterns)} patterns extracted for {domain_name}")
    except Exception as e:
        print(f"[ERROR] {domain_name}: {e}")

print(f"\\n{'='*60}")
print(f"Total patterns extracted: {total_extracted}")
print(f"{'='*60}")
"""
        
        script_path = Path("batch_extract_custom.py")
        script_path.write_text(script_content, encoding='utf-8')
        
        print(f"\nBatch script generated: {script_path}")
        print("\nTo run the extraction:")
        print(f"  python {script_path}")
        print()
    
    def save_recommendations(self, result: dict, output_path: str = "extraction_recommendations.json"):
        """Save recommendations to file."""
        Path(output_path).write_text(json.dumps(result, indent=2))
        print(f"Recommendations saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="LLM-powered domain and topic selector for pattern extraction"
    )
    parser.add_argument(
        '--description',
        help='Project description',
        type=str
    )
    parser.add_argument(
        '--technologies',
        help='Comma-separated list of existing technologies',
        type=str
    )
    parser.add_argument(
        '--from-constitution',
        help='Path to project_constitution.toml',
        type=str
    )
    parser.add_argument(
        '--output',
        help='Save recommendations to JSON file',
        type=str
    )
    parser.add_argument(
        '--generate-script',
        help='Generate batch extraction script',
        action='store_true'
    )
    
    args = parser.parse_args()
    
    selector = DomainTopicSelector()
    
    # Determine mode
    if args.from_constitution:
        print(f"Analysing project constitution: {args.from_constitution}")
        result = selector.analyse_from_constitution(args.from_constitution)
        if result:
            selector._display_results(result)
            if args.output:
                selector.save_recommendations(result, args.output)
            if args.generate_script:
                selector._generate_batch_script(result)
    
    elif args.description:
        techs = [t.strip() for t in args.technologies.split(",")] if args.technologies else None
        result = selector.analyse_requirements(args.description, techs)
        selector._display_results(result)
        if args.output:
            selector.save_recommendations(result, args.output)
        if args.generate_script:
            selector._generate_batch_script(result)
    
    else:
        # Interactive mode
        selector.interactive_mode()


if __name__ == "__main__":
    main()
