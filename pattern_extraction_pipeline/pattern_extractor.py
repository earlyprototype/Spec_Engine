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
    
    def __init__(self, progress_callback=None):
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
        
        # Progress callback for real-time updates
        self.progress_callback = progress_callback
    
    def validate_and_refine_query(self, search_query, min_results=5, max_retries=5):
        """
        Validate query returns enough results. If not, ask LLM to refine it.
        
        Args:
            search_query: GitHub search query
            min_results: Minimum number of results required
            max_retries: Maximum refinement attempts
        
        Returns:
            tuple: (status, refined_query, result_count)
            status: 'ok', 'refined', or 'failed'
        """
        original_query = search_query
        
        for attempt in range(max_retries):
            try:
                # Check result count without fetching all repos
                results = self.github.search_repositories(query=search_query)
                count = results.totalCount
                
                if count >= min_results:
                    # Success - enough results
                    if search_query == original_query:
                        return 'ok', search_query, count
                    else:
                        return 'refined', search_query, count
                
                if count == 0:
                    print(f"  Attempt {attempt + 1}/{max_retries}: 0 results, refining...")
                else:
                    print(f"  Attempt {attempt + 1}/{max_retries}: Only {count} results (need {min_results}), refining...")
                
                # Escalating refinement strategy based on attempt number
                if attempt < 2:
                    # First 2 attempts: Conservative refinement
                    refine_prompt = f"""This GitHub search query returned only {count} results:
Query: {search_query}

Refine it to get more results. Be SIMPLE and CONSERVATIVE:
1. If it has "stars:>X", lower X significantly (e.g., >5000 → >1000, >1000 → >100)
2. If it has multiple terms, remove the least important ones
3. Keep it simple - avoid complex OR operators unless necessary

Return ONLY the refined query, nothing else."""
                
                elif attempt < 4:
                    # Attempts 3-4: More aggressive simplification
                    refine_prompt = f"""This query still returns only {count} results after refinement:
Query: {search_query}

SIMPLIFY DRASTICALLY:
1. Remove all "stars:" filters
2. Extract just the 1-2 most important keywords
3. Avoid complex syntax - just use simple terms or "topic:keyword"

Return ONLY the simplified query, nothing else."""
                
                else:
                    # Final attempt: Completely new query based on original intent
                    refine_prompt = f"""Previous query failed: {search_query}
Original query was: {original_query}

Generate a COMPLETELY NEW, SIMPLE query for the same concept:
- Use just 1-2 keywords, OR
- Use "topic:keyword" format, OR  
- Use "keyword in:readme" format

Return ONLY the new query, nothing else."""

                response = self.llm.generate_content(refine_prompt)
                search_query = response.text.strip()
                
            except Exception as e:
                print(f"  [ERROR] Validation failed: {e}")
                # Don't fail immediately, try a simple fallback
                if attempt == 0:
                    continue
                return 'failed', original_query, 0
        
        # Max retries reached - check final count and accept if > 0
        try:
            results = self.github.search_repositories(query=search_query)
            count = results.totalCount
            
            if count == 0:
                # Last resort: try just the first word of the original query
                print(f"  All attempts failed. Trying ultra-simple fallback...")
                fallback = original_query.split()[0].replace('topic:', '').replace('stars:', '')
                results = self.github.search_repositories(query=f"topic:{fallback}")
                count = results.totalCount
                
                if count > 0:
                    print(f"  Fallback succeeded: {count} results")
                    return 'refined', f"topic:{fallback}", count
                else:
                    return 'failed', search_query, 0
            elif count < min_results:
                # Accept it anyway if we got some results
                return 'refined', search_query, count
            else:
                return 'refined', search_query, count
                
        except:
            return 'failed', search_query, 0
    
    def extract_patterns(self, search_query, limit=100, validate=True, min_results=5):
        """
        Main extraction pipeline.
        
        Args:
            search_query: GitHub search (e.g., "topic:file-manager stars:>5000")
            limit: Max repos to analyze
            validate: Whether to validate and refine query first
            min_results: Minimum results required if validating
        
        Returns:
            List of extracted patterns
        """
        # Validate query first
        if validate:
            search_query, result_count = self.validate_and_refine_query(search_query, min_results)
            if result_count < min_results:
                print(f"[WARNING] Query still only returns {result_count} results, proceeding anyway...")
        
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
                try:
                    pattern = self._extract_with_llm(
                        repo_name=repo.full_name,
                        repo_url=repo.html_url,
                        stars=repo.stargazers_count,
                        readme=readme,
                        structure=structure,
                        dependencies=deps
                    )
                except Exception as llm_error:
                    print(f"  [ERROR] LLM extraction failed: {llm_error}")
                    continue
                
                # Add quality metrics to pattern
                pattern['quality_score'] = quality_metrics['composite_score']
                pattern['freshness_score'] = quality_metrics['freshness_score']
                pattern['maintenance_score'] = quality_metrics['maintenance_score']
                
                # Store in graph
                try:
                    self._store_pattern(pattern)
                    patterns.append(pattern)
                    print(f"  [OK] Pattern: {pattern['pattern_name']}")
                    
                    # Notify callback if provided
                    if self.progress_callback:
                        self.progress_callback(pattern)
                except Exception as store_error:
                    print(f"  [ERROR] Failed to store pattern: {store_error}")
                    continue
                
            except Exception as e:
                print(f"  [ERROR] Unexpected error: {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()
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
        
        try:
            parsed = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"  [ERROR] Failed to parse LLM response as JSON: {e}")
            print(f"  Response: {response_text[:500]}...")
            raise ValueError(f"Invalid JSON from LLM: {e}")
        
        # Handle both single pattern (dict) and multiple patterns (list)
        # LLM sometimes returns a list when it detects multiple architectural patterns
        if isinstance(parsed, list):
            if len(parsed) == 0:
                raise ValueError("LLM returned empty list")
            print(f"  [INFO] LLM returned {len(parsed)} patterns, extracting the primary one")
            pattern = parsed[0]  # Take the first/primary pattern
        elif isinstance(parsed, dict):
            pattern = parsed
        else:
            raise ValueError(f"Expected dict or list from LLM, got {type(parsed)}")
        
        # Validate it's now a dict
        if not isinstance(pattern, dict):
            raise ValueError(f"Pattern must be a dict, got {type(pattern)}")
        
        if 'pattern_name' not in pattern:
            raise ValueError("LLM response missing 'pattern_name'")
        
        if 'requirements' not in pattern or not isinstance(pattern['requirements'], dict):
            print(f"  [WARNING] Missing or invalid requirements, using defaults")
            pattern['requirements'] = {'type': 'general', 'domain': 'unknown'}
        
        # Clean output - remove verbose debug logs since we've fixed the core issue
        
        pattern['source_repo'] = kwargs['repo_url']
        pattern['stars'] = kwargs['stars']
        return pattern
    
    def _store_pattern(self, pattern):
        """Store pattern in Neo4j with normalized data and weights."""
        # Normalize technologies with weights
        normalized_techs = []
        technologies = pattern.get('technologies', [])
        
        # Ensure technologies is a list
        if not isinstance(technologies, list):
            technologies = [technologies] if technologies else []
        
        for tech in technologies:
            try:
                # Handle both old format (string) and new format (dict)
                if isinstance(tech, dict):
                    tech_name = tech.get('name', str(tech))
                    normalized_techs.append({
                        'name': self.normalize_technology_name(tech_name),
                        'role': tech.get('role', 'unknown').lower(),
                        'criticality': float(tech.get('criticality', 0.5)),
                        'adoption_confidence': float(tech.get('adoption_confidence', 0.5)),
                        'can_substitute': tech.get('can_substitute', [])
                    })
                else:
                    # Fallback for old format (string)
                    normalized_techs.append({
                        'name': self.normalize_technology_name(str(tech)),
                        'role': 'unknown',
                        'criticality': 0.5,
                        'adoption_confidence': 0.5,
                        'can_substitute': []
                    })
            except Exception as e:
                print(f"  Warning: Skipping malformed technology: {tech} ({e})")
                continue
        
        # Normalize constraints with weights
        normalized_constraints = []
        constraints = pattern.get('constraints', [])
        
        # Ensure constraints is a list
        if not isinstance(constraints, list):
            constraints = [constraints] if constraints else []
        
        for c in constraints:
            try:
                # Handle both old format (string) and new format (dict)
                if isinstance(c, dict):
                    normalized_constraints.append({
                        'rule': self.normalize_constraint(c.get('rule', str(c))),
                        'criticality': c.get('criticality', 'should'),
                        'enforcement': c.get('enforcement', 'implementation'),
                        'violation_impact': c.get('violation_impact', 'medium'),
                        'reasoning': c.get('reasoning', '')
                    })
                else:
                    # Fallback for old format (string)
                    normalized_constraints.append({
                        'rule': self.normalize_constraint(str(c)),
                        'criticality': 'should',
                        'enforcement': 'implementation',
                        'violation_impact': 'medium',
                        'reasoning': ''
                    })
            except Exception as e:
                print(f"  Warning: Skipping malformed constraint: {c} ({e})")
                continue
        
        # Get quality metrics (if available)
        quality_score = pattern.get('quality_score', 0.5)
        freshness_score = pattern.get('freshness_score', 0.5)
        maintenance_score = pattern.get('maintenance_score', 0.5)
        
        # Ensure we have at least one technology
        if not normalized_techs:
            normalized_techs = [{
                'name': 'unknown',
                'role': 'unknown',
                'criticality': 0.5,
                'adoption_confidence': 0.5,
                'can_substitute': []
            }]
        
        # Ensure we have at least one constraint (optional but good practice)
        if not normalized_constraints:
            normalized_constraints = [{
                'rule': 'no_constraints_specified',
                'criticality': 'nice-to-have',
                'enforcement': 'style',
                'violation_impact': 'low',
                'reasoning': 'No specific constraints identified'
            }]
        
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
                ON CREATE SET 
                    u.role = tech.role,
                    u.criticality = tech.criticality,
                    u.adoption_confidence = tech.adoption_confidence,
                    u.can_substitute = tech.can_substitute
                ON MATCH SET
                    u.role = tech.role,
                    u.criticality = tech.criticality,
                    u.adoption_confidence = tech.adoption_confidence,
                    u.can_substitute = tech.can_substitute
            """,
                pattern_name=pattern['pattern_name'],
                confidence=pattern.get('confidence', 'medium'),
                source_repo=pattern['source_repo'],
                stars=pattern['stars'],
                reasoning=pattern.get('reasoning', ''),
                quality_score=float(quality_score),
                freshness_score=float(freshness_score),
                maintenance_score=float(maintenance_score),
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
