# pattern_extractor.py
# Automated pattern extraction from GitHub → LLM → Neo4j

import os
import json
from github import Github
import google.generativeai as genai
from neo4j import GraphDatabase

try:
    from quality_metrics import QualityMetricsCalculator
    QUALITY_METRICS_AVAILABLE = True
except ImportError:
    QUALITY_METRICS_AVAILABLE = False

class PatternExtractor:
    @staticmethod
    def normalize_technology_name(name):
        """Normalize technology names to prevent duplicates."""
        return name.strip().lower()
    
    @staticmethod
    def normalize_constraint(constraint):
        """Normalize constraint rules."""
        return constraint.strip().lower().replace(' ', '_')
    
    def __init__(self):
        self.github = Github(os.getenv("GITHUB_TOKEN"))
        
        # Configure Google Gemini with direct API key (disable Cloud SDK auth)
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        # Unset Google Cloud auth env vars to force API key usage
        for var in ['GOOGLE_APPLICATION_CREDENTIALS', 'GCLOUD_PROJECT']:
            os.environ.pop(var, None)
        
        genai.configure(api_key=api_key)
        self.llm = genai.GenerativeModel('gemini-2.5-flash')
        
        self.neo4j = GraphDatabase.driver(
            os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
        )
        
        # Quality metrics calculator
        if QUALITY_METRICS_AVAILABLE:
            self.quality_calculator = QualityMetricsCalculator()
        else:
            self.quality_calculator = None
    
    def extract_patterns(self, search_query, limit=100):
        """
        Main extraction pipeline.
        
        Args:
            search_query: GitHub search (e.g., "topic:file-manager stars:>5000")
            limit: Max repos to analyze
        
        Returns:
            List of extracted patterns
        """
        print(f"Searching GitHub: {search_query}")
        repos = list(self.github.search_repositories(query=search_query))[:limit]
        print(f"Found {len(repos)} repos")
        
        patterns = []
        for i, repo in enumerate(repos, 1):
            print(f"\n[{i}/{len(repos)}] Analyzing {repo.full_name}...")
            
            try:
                # Calculate quality metrics
                if self.quality_calculator:
                    quality_metrics = self.quality_calculator.calculate_quality_score(repo)
                    print(f"  Quality: {quality_metrics['composite_score']:.2f} "
                          f"({self.quality_calculator.get_quality_tier(quality_metrics['composite_score'])})")
                else:
                    quality_metrics = {
                        'composite_score': 0.5,
                        'freshness_score': 0.5,
                        'maintenance_score': 0.5
                    }
                
                # Fetch repo data
                readme = self._fetch_readme(repo)
                structure = self._analyze_structure(repo)
                deps = self._fetch_dependencies(repo)
                
                # LLM analysis
                pattern = self._extract_with_llm(
                    repo_name=repo.full_name,
                    repo_url=repo.html_url,
                    stars=repo.stargazers_count,
                    readme=readme,
                    structure=structure,
                    dependencies=deps
                )
                
                # Add quality metrics to pattern
                pattern['quality_score'] = quality_metrics['composite_score']
                pattern['freshness_score'] = quality_metrics['freshness_score']
                pattern['maintenance_score'] = quality_metrics['maintenance_score']
                
                # Store in graph
                self._store_pattern(pattern)
                patterns.append(pattern)
                
                print(f"  [OK] Pattern: {pattern['pattern_name']}")
                
            except Exception as e:
                print(f"  [ERROR] {e}")
                continue
        
        print(f"\nExtracted {len(patterns)} patterns")
        return patterns
    
    def _fetch_readme(self, repo):
        """Fetch README content."""
        try:
            readme = repo.get_readme()
            content = readme.decoded_content.decode('utf-8')
            return content[:5000]  # First 5000 chars
        except:
            return "No README found"
    
    def _analyze_structure(self, repo):
        """Analyze repo file structure."""
        try:
            contents = repo.get_contents("")
            dirs = [c.path for c in contents if c.type == "dir"]
            return {"directories": dirs[:20]}  # Top 20 dirs
        except:
            return {"directories": []}
    
    def _fetch_dependencies(self, repo):
        """Fetch package.json or requirements.txt."""
        try:
            # Try package.json (Node.js)
            pkg = repo.get_contents("package.json")
            return json.loads(pkg.decoded_content)
        except:
            pass
        
        try:
            # Try requirements.txt (Python)
            reqs = repo.get_contents("requirements.txt")
            return {"requirements": reqs.decoded_content.decode('utf-8')}
        except:
            return {}
    
    def _extract_with_llm(self, **kwargs):
        """Use LLM to extract pattern from repo."""
        prompt = f"""
        Analyze this GitHub repository and extract architectural pattern with WEIGHTS.
        
        Repository: {kwargs['repo_name']}
        Stars: {kwargs['stars']}
        URL: {kwargs['repo_url']}
        
        README:
        {kwargs['readme']}
        
        Structure:
        {kwargs['structure']}
        
        Dependencies:
        {json.dumps(kwargs['dependencies'], indent=2)}
        
        Extract in JSON format with CRITICALITY SCORES:
        {{
            "pattern_name": "filesystem_browser",
            "confidence": "high",
            "requirements": {{
                "type": "data_management",
                "domain": "file_system",
                "context": ["existing_files", "web_ui"]
            }},
            "constraints": [
                {{
                    "rule": "filesystem_is_source_of_truth",
                    "criticality": "must",
                    "enforcement": "architectural",
                    "violation_impact": "high",
                    "reasoning": "Core principle for data integrity"
                }},
                {{
                    "rule": "database_for_metadata_only",
                    "criticality": "should",
                    "enforcement": "implementation",
                    "violation_impact": "medium",
                    "reasoning": "Improves performance"
                }}
            ],
            "technologies": [
                {{
                    "name": "react",
                    "role": "primary",
                    "criticality": 0.95,
                    "adoption_confidence": 0.9,
                    "can_substitute": ["vue", "preact"]
                }},
                {{
                    "name": "sqlite",
                    "role": "cache",
                    "criticality": 0.6,
                    "adoption_confidence": 0.85,
                    "can_substitute": ["indexeddb", "localstorage"]
                }}
            ],
            "reasoning": "Brief explanation..."
        }}
        
        IMPORTANT SCORING GUIDELINES:
        - Technology criticality: 0-1 scale (1.0 = absolutely required, 0.3 = nice to have)
        - Adoption confidence: 0-1 scale (1.0 = industry standard, 0.5 = experimental)
        - Constraint criticality: "must" (breaks pattern if violated), "should" (recommended), "nice-to-have" (optional)
        - Constraint enforcement: "architectural" (core design), "implementation" (code level), "style" (conventions)
        - Violation impact: "high" (breaks functionality), "medium" (reduces quality), "low" (minor)
        
        Be specific. If unclear, set confidence to "low".
        """
        
        # Use Gemini to generate response
        response = self.llm.generate_content(prompt)
        
        # Extract JSON from response
        response_text = response.text
        
        # Try to extract JSON (Gemini might wrap it in markdown code blocks)
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()
        
        pattern = json.loads(response_text)
        pattern['source_repo'] = kwargs['repo_url']
        pattern['stars'] = kwargs['stars']
        return pattern
    
    def _store_pattern(self, pattern):
        """Store pattern in Neo4j with normalized data and weights."""
        # Normalize technologies with weights
        normalized_techs = []
        for tech in pattern['technologies']:
            # Handle both old format (string constraints) and new format (dict)
            if isinstance(tech, dict):
                normalized_techs.append({
                    'name': self.normalize_technology_name(tech['name']),
                    'role': tech.get('role', 'unknown').lower(),
                    'criticality': tech.get('criticality', 0.5),
                    'adoption_confidence': tech.get('adoption_confidence', 0.5),
                    'can_substitute': tech.get('can_substitute', [])
                })
            else:
                # Fallback for old format
                normalized_techs.append({
                    'name': self.normalize_technology_name(tech),
                    'role': 'unknown',
                    'criticality': 0.5,
                    'adoption_confidence': 0.5,
                    'can_substitute': []
                })
        
        # Normalize constraints with weights
        normalized_constraints = []
        for c in pattern['constraints']:
            # Handle both old format (string) and new format (dict)
            if isinstance(c, dict):
                normalized_constraints.append({
                    'rule': self.normalize_constraint(c['rule']),
                    'criticality': c.get('criticality', 'should'),
                    'enforcement': c.get('enforcement', 'implementation'),
                    'violation_impact': c.get('violation_impact', 'medium'),
                    'reasoning': c.get('reasoning', '')
                })
            else:
                # Fallback for old format
                normalized_constraints.append({
                    'rule': self.normalize_constraint(c),
                    'criticality': 'should',
                    'enforcement': 'implementation',
                    'violation_impact': 'medium',
                    'reasoning': ''
                })
        
        # Get quality metrics (if available)
        quality_score = pattern.get('quality_score', 0.5)
        freshness_score = pattern.get('freshness_score', 0.5)
        maintenance_score = pattern.get('maintenance_score', 0.5)
        
        with self.neo4j.session() as session:
            session.run("""
                // Create pattern node with quality metrics
                CREATE (p:Pattern {
                    name: $pattern_name,
                    confidence: $confidence,
                    source_repo: $source_repo,
                    stars: $stars,
                    reasoning: $reasoning,
                    quality_score: $quality_score,
                    freshness_score: $freshness_score,
                    maintenance_score: $maintenance_score,
                    extracted_at: datetime()
                })
                
                // MERGE requirement node (reuse if exists)
                MERGE (r:Requirement {
                    type: $req_type,
                    domain: $req_domain
                })
                
                CREATE (r)-[:SOLVED_BY]->(p)
                
                // MERGE constraints with weights
                WITH p
                UNWIND $constraints AS constraint
                MERGE (c:Constraint {rule: constraint.rule})
                MERGE (p)-[req:REQUIRES]->(c)
                SET req.criticality = constraint.criticality,
                    req.enforcement = constraint.enforcement,
                    req.violation_impact = constraint.violation_impact,
                    req.reasoning = constraint.reasoning
                
                // MERGE technologies with weights
                WITH p
                UNWIND $technologies AS tech
                MERGE (t:Technology {name: tech.name})
                MERGE (p)-[u:USES]->(t)
                SET u.role = tech.role,
                    u.criticality = tech.criticality,
                    u.adoption_confidence = tech.adoption_confidence,
                    u.can_substitute = tech.can_substitute
                ON MATCH SET u.role = tech.role
            """,
                pattern_name=pattern['pattern_name'],
                confidence=pattern['confidence'],
                source_repo=pattern['source_repo'],
                stars=pattern['stars'],
                reasoning=pattern['reasoning'],
                req_type=pattern['requirements']['type'],
                req_domain=pattern['requirements']['domain'],
                constraints=normalized_constraints,
                technologies=normalized_techs
            )
    
    def analyze_single_repo(self, repo_name, domain="general"):
        """
        Analyze a single repository by name.
        
        Args:
            repo_name: Full repo name (e.g., "microsoft/vscode")
            domain: Domain hint for pattern extraction
        
        Returns:
            Extracted pattern dict
        """
        print(f"Analyzing single repo: {repo_name}")
        
        try:
            repo = self.github.get_repo(repo_name)
            
            # Fetch repo data
            readme = self._fetch_readme(repo)
            structure = self._analyze_structure(repo)
            deps = self._fetch_dependencies(repo)
            
            # LLM analysis
            pattern = self._extract_with_llm(
                repo_name=repo.full_name,
                repo_url=repo.html_url,
                stars=repo.stargazers_count,
                readme=readme,
                structure=structure,
                dependencies=deps
            )
            
            print(f"[OK] Pattern extracted: {pattern['pattern_name']}")
            return pattern
            
        except Exception as e:
            print(f"[ERROR] {e}")
            raise
    
    def store_pattern(self, pattern):
        """Public method to store a pattern."""
        self._store_pattern(pattern)

# Usage
if __name__ == "__main__":
    extractor = PatternExtractor()
    
    # Extract file managers
    print("\n=== Extracting File Managers ===")
    file_managers = extractor.extract_patterns(
        "topic:file-manager stars:>5000",
        limit=10  # Start with 10 for testing
    )
    
    # Extract dashboards
    print("\n=== Extracting Dashboards ===")
    dashboards = extractor.extract_patterns(
        "topic:dashboard stars:>10000",
        limit=10
    )
    
    print(f"\n[OK] Total patterns extracted: {len(file_managers) + len(dashboards)}")
    print(f"[OK] Cost: ~${(len(file_managers) + len(dashboards)) * 0.01:.2f}")
