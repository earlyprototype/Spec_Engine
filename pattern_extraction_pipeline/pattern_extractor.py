# pattern_extractor.py
# Automated pattern extraction from GitHub → LLM → Neo4j

import os
import json
import time
import yaml
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from github import Github, GithubException, RateLimitExceededException
import google.generativeai as genai
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, TransientError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
    after_log
)
import logging

# Configure logging for retry attempts
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from quality_metrics import QualityMetricsCalculator
    QUALITY_METRICS_AVAILABLE = True
except ImportError:
    QUALITY_METRICS_AVAILABLE = False

try:
    from pattern_critic import PatternCritic
    PATTERN_CRITIC_AVAILABLE = True
except ImportError:
    PATTERN_CRITIC_AVAILABLE = False
    logger.warning("PatternCritic not available - validation will be skipped")

try:
    from trajectory_logger import TrajectoryLogger
    TRAJECTORY_LOGGER_AVAILABLE = True
except ImportError:
    TRAJECTORY_LOGGER_AVAILABLE = False
    logger.warning("TrajectoryLogger not available - trajectory logging will be skipped")

try:
    from quality_judge import QualityJudge
    QUALITY_JUDGE_AVAILABLE = True
except ImportError:
    QUALITY_JUDGE_AVAILABLE = False
    logger.warning("QualityJudge not available - judge evaluation will be skipped")

try:
    from ide_rule_library.enhanced_rule_extractor import EnhancedRuleExtractor
    from ide_rule_library.quality_scorer import RepoQualityScorer
    IDE_RULE_LIBRARY_AVAILABLE = True
except ImportError as e:
    IDE_RULE_LIBRARY_AVAILABLE = False
    logger.warning(f"IDE Rule Library not available - rule extraction will be skipped: {e}")

# Import custom exceptions, rate limiter, and metrics
from pattern_extraction_pipeline.exceptions import (
    IntegrationError,
    RuleExtractionError,
    DatabaseWriteError,
    RateLimitError,
    PatternExtractionError,
    GitHubAPIError
)
from pattern_extraction_pipeline.rate_limiter import RateLimiter
from pattern_extraction_pipeline.metrics import Metrics

# Retry decorator configurations
# GitHub API: Handle rate limits and transient errors
github_retry = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((GithubException, RateLimitExceededException, ConnectionError, TimeoutError)),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    after=after_log(logger, logging.INFO)
)

# Gemini LLM: Handle quota/service errors
llm_retry = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((Exception,)),  # Catch Gemini-specific errors
    before_sleep=before_sleep_log(logger, logging.WARNING),
    after=after_log(logger, logging.INFO)
)

# Neo4j: Handle connection and transient errors
neo4j_retry = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((ServiceUnavailable, TransientError, ConnectionError)),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    after=after_log(logger, logging.INFO)
)

class PatternExtractor:
    @staticmethod
    def normalize_technology_name(name):
        """Normalize technology names to prevent duplicates."""
        return name.strip().lower()
    
    @staticmethod
    def normalize_constraint(constraint):
        """Normalize constraint rules."""
        return constraint.strip().lower().replace(' ', '_')
    
    def _check_if_repo_exists(self, repo_url):
        """
        Check if repository has already been analyzed.
        
        Args:
            repo_url: Repository URL to check
        
        Returns:
            dict or None: Pattern details if exists, None otherwise
                {
                    'name': str,
                    'extracted_at': datetime,
                    'quality_score': float,
                    'stars': int
                }
        """
        with self.neo4j.session() as session:
            result = session.run("""
                MATCH (p:Pattern {source_repo: $repo_url})
                RETURN p.name as name, 
                       p.extracted_at as extracted_at,
                       p.quality_score as quality_score,
                       p.stars as stars
                LIMIT 1
            """, repo_url=repo_url)
            record = result.single()
            return dict(record) if record else None
    
    def __init__(self, progress_callback=None, config_path=None):
        # Warn about proper resource management
        import warnings
        warnings.warn(
            "PatternExtractor manages resources that must be cleaned up. "
            "Use 'with PatternExtractor() as extractor:' pattern or call extractor.close() when done.",
            DeprecationWarning,
            stacklevel=2
        )
        
        # Load and validate configuration with Pydantic
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        
        try:
            from pattern_extraction_pipeline.config_validator import validate_config_file
            self.config = validate_config_file(config_path)
            logger.info(f"Configuration loaded and validated from {config_path}")
        except Exception as config_error:
            logger.error(f"Config validation failed: {config_error}")
            raise ValueError(f"Invalid configuration: {config_error}") from config_error
        
        from github import Auth
        github_token = os.getenv(self.config.github.token_env)
        if not github_token:
            raise ValueError(f"{self.config.github.token_env} not found in environment")
        self.github = Github(auth=Auth.Token(github_token))
        
        # Configure Google Gemini with direct API key (disable Cloud SDK auth)
        from dotenv import load_dotenv
        # Use override=True to ensure .env file takes precedence over system variables
        load_dotenv(override=True)
        api_key = os.getenv(self.config.gemini.api_key_env)
        if not api_key:
            raise ValueError(f"{self.config.gemini.api_key_env} not found in .env file")
        
        # Unset Google Cloud auth env vars to force API key usage
        for var in ['GOOGLE_APPLICATION_CREDENTIALS', 'GCLOUD_PROJECT']:
            os.environ.pop(var, None)
        
        genai.configure(api_key=api_key)
        self.llm = genai.GenerativeModel(self.config.gemini.model_name)
        
        self.neo4j = GraphDatabase.driver(
            self.config.neo4j.uri,
            auth=(self.config.neo4j.user, os.getenv(self.config.neo4j.password_env, "password"))
        )
        
        # Quality metrics calculator
        if QUALITY_METRICS_AVAILABLE:
            self.quality_calculator = QualityMetricsCalculator()
        else:
            self.quality_calculator = None
        
        # Pattern critic for async validation
        if PATTERN_CRITIC_AVAILABLE:
            self.critic = PatternCritic()
            self.critic_executor = ThreadPoolExecutor(max_workers=3, thread_name_prefix="critic_judge")
        else:
            self.critic = None
            self.critic_executor = None
        
        # Quality judge for advanced evaluation
        if QUALITY_JUDGE_AVAILABLE:
            self.judge = QualityJudge()
        else:
            self.judge = None
        
        # Trajectory logger for extraction path tracking
        if TRAJECTORY_LOGGER_AVAILABLE:
            self.trajectory_logger = TrajectoryLogger()
        else:
            self.trajectory_logger = None
        
        # IDE Rule extraction components
        if IDE_RULE_LIBRARY_AVAILABLE:
            self.rule_extractor = EnhancedRuleExtractor(
                model_name=self.config.gemini.model_name,
                logger=logger
            )
            self.quality_scorer = RepoQualityScorer()
            logger.info("IDE Rule Library initialized - rule extraction enabled")
        else:
            self.rule_extractor = None
            self.quality_scorer = None
        
        # Rate limiter for Gemini API (15 requests per minute for free tier)
        self.gemini_rate_limiter = RateLimiter(
            max_calls=15,
            period=60,
            name="gemini_api"
        )
        
        # Metrics collection
        self.metrics = Metrics(name="pattern_extractor")
        logger.info("Metrics collection initialized")
        
        # Progress callback for real-time updates
        self.progress_callback = progress_callback
    
    def __enter__(self):
        """Context manager entry - returns self for use in with statement."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit - cleanup resources.
        
        Args:
            exc_type: Exception type if an exception was raised
            exc_val: Exception value if an exception was raised
            exc_tb: Exception traceback if an exception was raised
        
        Returns:
            False to propagate exceptions (don't suppress them)
        """
        self.close()
        return False  # Don't suppress exceptions
    
    def close(self):
        """
        Close all open connections and cleanup resources.
        
        Call this when done with the extractor, or use as context manager:
            with PatternExtractor() as extractor:
                pattern = extractor.analyze_single_repo('owner/repo')
        
        This method is idempotent - safe to call multiple times.
        """
        if hasattr(self, 'neo4j') and self.neo4j:
            try:
                self.neo4j.close()
                logger.info("Neo4j driver closed")
            except Exception as e:
                logger.warning(f"Error closing Neo4j driver: {e}")
            finally:
                self.neo4j = None
        
        if hasattr(self, 'critic_executor') and self.critic_executor:
            try:
                self.critic_executor.shutdown(wait=True, cancel_futures=False)
                logger.info("Critic executor shutdown")
            except Exception as e:
                logger.warning(f"Error shutting down critic executor: {e}")
            finally:
                self.critic_executor = None
    
    def __del__(self):
        """
        Destructor - warn if resources not properly closed.
        
        This warns developers if they forget to call close() or use context manager.
        """
        if hasattr(self, 'neo4j') and self.neo4j:
            logger.warning(
                "PatternExtractor was not properly closed. "
                "Use 'with PatternExtractor() as extractor:' or call extractor.close()"
            )
    
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
    
    def extract_patterns(self, search_query, limit=100, validate=True, min_results=5, domain="general", force_reanalyse=False):
        """
        Main extraction pipeline.
        
        Args:
            search_query: GitHub search (e.g., "topic:file-manager stars:>5000")
            limit: Max repos to analyze
            validate: Whether to validate and refine query first
            min_results: Minimum results required if validating
            domain: Domain name for trajectory logging
            force_reanalyse: Whether to re-analyze repositories that have already been processed
        
        Returns:
            List of extracted patterns
        """
        # Start trajectory logging
        if self.trajectory_logger:
            self.trajectory_logger.start_extraction(domain, search_query, limit)
        
        # Validate query first
        if validate:
            status, search_query, result_count = self.validate_and_refine_query(search_query, min_results)
            if result_count < min_results:
                print(f"[WARNING] Query still only returns {result_count} results, proceeding anyway...")
        
        print(f"Searching GitHub: {search_query}")
        repos = list(self.github.search_repositories(query=search_query))[:limit]
        print(f"Found {len(repos)} repos")
        
        patterns = []
        extraction_stats = {
            'total': len(repos),
            'successful': 0,
            'partial': 0,
            'failed': 0,
            'skipped': 0,
            'errors': []
        }
        
        for i, repo in enumerate(repos, 1):
            print(f"\n[{i}/{len(repos)}] Analyzing {repo.full_name}...")
            
            # Check if repository already analyzed
            existing = self._check_if_repo_exists(repo.html_url)
            if existing and not force_reanalyse:
                # Handle null extracted_at
                date_str = existing['extracted_at'].strftime('%Y-%m-%d') if existing.get('extracted_at') else 'unknown date'
                print(f"  [SKIP] Already analyzed on {date_str}")
                print(f"         Quality: {existing.get('quality_score', 0):.2f}, Stars: {existing.get('stars', 0)}")
                extraction_stats['skipped'] += 1
                
                # Log trajectory skip
                if self.trajectory_logger:
                    self.trajectory_logger.log_repository_skipped(
                        repo.full_name, 
                        existing.get('extracted_at'),
                        existing.get('quality_score', 0)
                    )
                continue
            
            # Start repository trajectory
            if self.trajectory_logger:
                self.trajectory_logger.start_repository(repo.full_name, repo.html_url, repo.stargazers_count)
            
            # Track what data we successfully fetch
            data_availability = {
                'readme': False,
                'structure': False,
                'dependencies': False,
                'quality_metrics': False
            }
            
            try:
                # Calculate quality metrics (non-critical) - default to mid-range on 0-100 scale
                quality_metrics = {'composite_score': 50.0, 'freshness_score': 50.0, 'maintenance_score': 50.0}
                if self.quality_calculator:
                    try:
                        quality_metrics = self.quality_calculator.calculate_quality_score(repo)
                        data_availability['quality_metrics'] = True
                        print(f"  Quality: {quality_metrics['composite_score']:.2f} "
                              f"({self.quality_calculator.get_quality_tier(quality_metrics['composite_score'])})")
                        
                        # Log quality metrics
                        if self.trajectory_logger:
                            self.trajectory_logger.log_quality_metrics(
                                repo.full_name,
                                quality_metrics['composite_score'],
                                quality_metrics['freshness_score'],
                                quality_metrics['maintenance_score']
                            )
                    except Exception as qm_error:
                        logger.warning(f"Quality metrics calculation failed: {qm_error}")
                
                # Fetch repo data with graceful degradation
                readme = "No README available"
                try:
                    start_time = time.time()
                    readme = self._fetch_readme(repo)
                    response_time = time.time() - start_time
                    data_availability['readme'] = readme != "No README found"
                    if data_availability['readme']:
                        print(f"  README: {len(readme)} chars")
                    
                    # Log GitHub API call
                    if self.trajectory_logger:
                        self.trajectory_logger.log_github_api_call(
                            "fetch_readme", repo.full_name, data_availability['readme'], response_time
                        )
                except Exception as readme_error:
                    logger.warning(f"README fetch failed: {readme_error}")
                    print(f"  [WARN] README unavailable, continuing...")
                    
                    # Log failed API call
                    if self.trajectory_logger:
                        self.trajectory_logger.log_github_api_call(
                            "fetch_readme", repo.full_name, False, 0, str(readme_error)
                        )
                
                structure = {"directories": []}
                try:
                    start_time = time.time()
                    structure = self._analyze_structure(repo)
                    response_time = time.time() - start_time
                    data_availability['structure'] = len(structure.get('directories', [])) > 0
                    if data_availability['structure']:
                        print(f"  Structure: {len(structure['directories'])} directories")
                    
                    # Log GitHub API call
                    if self.trajectory_logger:
                        self.trajectory_logger.log_github_api_call(
                            "analyze_structure", repo.full_name, data_availability['structure'], response_time
                        )
                except Exception as struct_error:
                    logger.warning(f"Structure analysis failed: {struct_error}")
                    print(f"  [WARN] Structure analysis unavailable, continuing...")
                    
                    # Log failed API call
                    if self.trajectory_logger:
                        self.trajectory_logger.log_github_api_call(
                            "analyze_structure", repo.full_name, False, 0, str(struct_error)
                        )
                
                deps = {}
                try:
                    deps = self._fetch_dependencies(repo)
                    data_availability['dependencies'] = bool(deps)
                    if data_availability['dependencies']:
                        print(f"  Dependencies: found")
                except Exception as deps_error:
                    logger.warning(f"Dependencies fetch failed: {deps_error}")
                
                # Check if we have enough data for LLM extraction
                has_readme = data_availability['readme']
                has_structure = data_availability['structure']
                
                if not has_readme and not has_structure:
                    print(f"  [SKIP] Insufficient data (no README or structure)")
                    extraction_stats['failed'] += 1
                    extraction_stats['errors'].append({
                        'repo': repo.full_name,
                        'reason': 'No README or structure data available'
                    })
                    continue
                
                # LLM analysis (critical - must succeed)
                try:
                    start_time = time.time()
                    pattern = self._extract_with_llm(
                        repo_name=repo.full_name,
                        repo_url=repo.html_url,
                        stars=repo.stargazers_count,
                        readme=readme,
                        structure=structure,
                        dependencies=deps
                    )
                    response_time = time.time() - start_time
                    
                    # Log LLM extraction
                    if self.trajectory_logger:
                        self.trajectory_logger.log_llm_extraction(
                            repo.full_name, True, response_time,
                            pattern.get('pattern_name'), pattern.get('confidence')
                        )
                except Exception as llm_error:
                    response_time = time.time() - start_time if 'start_time' in locals() else 0
                    print(f"  [ERROR] LLM extraction failed: {llm_error}")
                    extraction_stats['failed'] += 1
                    extraction_stats['errors'].append({
                        'repo': repo.full_name,
                        'reason': f'LLM extraction error: {str(llm_error)[:100]}'
                    })
                    
                    # Log failed LLM extraction
                    if self.trajectory_logger:
                        self.trajectory_logger.log_llm_extraction(
                            repo.full_name, False, response_time, error=str(llm_error)
                        )
                        self.trajectory_logger.finish_repository("failed")
                    
                    continue
                
                # Add quality metrics to pattern
                pattern['quality_score'] = quality_metrics['composite_score']
                pattern['freshness_score'] = quality_metrics['freshness_score']
                pattern['maintenance_score'] = quality_metrics['maintenance_score']
                
                # Add extraction metadata
                pattern['extraction_status'] = 'partial' if not all(data_availability.values()) else 'complete'
                pattern['data_availability'] = data_availability
                
                # Store in graph (critical - must succeed)
                try:
                    start_time = time.time()
                    self._store_pattern(pattern)
                    response_time = time.time() - start_time
                    patterns.append(pattern)
                    
                    # Log Neo4j storage
                    if self.trajectory_logger:
                        self.trajectory_logger.log_neo4j_storage(
                            pattern['pattern_name'], True, response_time
                        )
                    
                    # Track success type
                    if pattern['extraction_status'] == 'complete':
                        extraction_stats['successful'] += 1
                        print(f"  [OK] Pattern: {pattern['pattern_name']} (complete data)")
                        if self.trajectory_logger:
                            self.trajectory_logger.finish_repository("successful")
                    else:
                        extraction_stats['partial'] += 1
                        missing = [k for k, v in data_availability.items() if not v]
                        print(f"  [OK] Pattern: {pattern['pattern_name']} (partial - missing: {', '.join(missing)})")
                        if self.trajectory_logger:
                            self.trajectory_logger.finish_repository("partial")
                    
                    # Prepare repository context for judge
                    repo_context = {
                        'description': repo.description or '',
                        'readme': readme[:1000] if readme != "No README available" else '',
                        'stars': repo.stargazers_count,
                        'language': repo.language or 'Unknown'
                    }
                    
                    # Trigger async validation and judge evaluation (non-blocking)
                    self._validate_pattern_async(pattern, repo_context)
                    
                    # Notify callback if provided
                    if self.progress_callback:
                        self.progress_callback(pattern)
                        
                except Exception as store_error:
                    response_time = time.time() - start_time if 'start_time' in locals() else 0
                    print(f"  [ERROR] Failed to store pattern: {store_error}")
                    extraction_stats['failed'] += 1
                    extraction_stats['errors'].append({
                        'repo': repo.full_name,
                        'reason': f'Storage error: {str(store_error)[:100]}'
                    })
                    
                    # Log failed storage
                    if self.trajectory_logger:
                        self.trajectory_logger.log_neo4j_storage(
                            pattern.get('pattern_name', 'unknown'), False, response_time, str(store_error)
                        )
                        self.trajectory_logger.finish_repository("failed")
                    
                    continue
                
            except Exception as e:
                print(f"  [ERROR] Unexpected error: {type(e).__name__}: {e}")
                logger.error(f"Unexpected error processing {repo.full_name}", exc_info=True)
                extraction_stats['failed'] += 1
                extraction_stats['errors'].append({
                    'repo': repo.full_name,
                    'reason': f'Unexpected error: {str(e)[:100]}'
                })
                
                # Log failed repository
                if self.trajectory_logger:
                    self.trajectory_logger.finish_repository("failed")
                
                continue
        
        # Print extraction statistics
        self._print_extraction_stats(extraction_stats)
        
        # Finish trajectory logging
        if self.trajectory_logger:
            trajectory_file = self.trajectory_logger.finish_extraction()
            print(f"\nTrajectory saved: {trajectory_file}")
        
        return patterns
        
    def _print_extraction_stats(self, stats):
        """Print detailed extraction statistics."""
        print("\n" + "="*60)
        print("EXTRACTION STATISTICS")
        print("="*60)
        print(f"Total repositories processed: {stats['total']}")
        print(f"  Successful (complete data): {stats['successful']}")
        print(f"  Partial (missing some data): {stats['partial']}")
        print(f"  Failed: {stats['failed']}")
        print(f"  Skipped (duplicates): {stats['skipped']}")
        
        if stats['successful'] + stats['partial'] > 0:
            success_rate = ((stats['successful'] + stats['partial']) / stats['total']) * 100
            print(f"\nSuccess rate: {success_rate:.1f}%")
        
        if stats['skipped'] > 0:
            skip_rate = (stats['skipped'] / stats['total']) * 100
            print(f"Skip rate: {skip_rate:.1f}% (already analyzed)")
        
        if stats['errors']:
            print(f"\nFailed repositories ({len(stats['errors'])}):")
            for error in stats['errors'][:10]:  # Show first 10
                print(f"  - {error['repo']}: {error['reason']}")
            if len(stats['errors']) > 10:
                print(f"  ... and {len(stats['errors']) - 10} more")
        
        print("="*60)
    
    @github_retry
    def _fetch_readme(self, repo):
        """Fetch README content with retry logic for rate limits."""
        try:
            logger.debug(f"Fetching README for {repo.full_name}")
            readme = repo.get_readme()
            content = readme.decoded_content.decode('utf-8')
            return content[:5000]  # First 5000 chars
        except GithubException as e:
            logger.warning(f"GitHub API error fetching README for {repo.full_name}: {e}")
            if e.status == 404:
                return "No README found"
            raise  # Let retry handle it
        except Exception as e:
            logger.error(f"Unexpected error fetching README for {repo.full_name}: {e}")
            return "No README found"
    
    @github_retry
    def _analyze_structure(self, repo):
        """Analyze repo file structure with retry logic."""
        try:
            logger.debug(f"Analyzing structure for {repo.full_name}")
            contents = repo.get_contents("")
            dirs = [c.path for c in contents if c.type == "dir"]
            return {"directories": dirs[:20]}  # Top 20 dirs
        except GithubException as e:
            logger.warning(f"GitHub API error analyzing structure for {repo.full_name}: {e}")
            if e.status == 404:
                return {"directories": []}
            raise  # Let retry handle it
        except Exception as e:
            logger.error(f"Unexpected error analyzing structure for {repo.full_name}: {e}")
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
    
    def _scan_for_rule_files(self, repo):
        """
        Scan repository for IDE rule files.
        
        Looks for common rule file patterns:
        - .cursorrules
        - .aiderules
        - .windsurfrules
        - CLAUDE.md / CLAUDE_*.md
        - AI_INSTRUCTIONS.md / AI_GUIDELINES.md
        - .github/copilot-instructions.md
        
        Returns:
            list: List of dicts with {'path': str, 'content': str, 'format': str}
        """
        if not IDE_RULE_LIBRARY_AVAILABLE:
            return []
        
        rule_files = []
        rule_patterns = [
            '.cursorrules',
            '.aiderules',
            '.windsurfrules',
            'CLAUDE.md',
            'AI_INSTRUCTIONS.md',
            'AI_GUIDELINES.md',
            '.github/copilot-instructions.md'
        ]
        
        # Also check for CLAUDE_*.md variants
        try:
            contents = repo.get_contents("")
            for content_file in contents:
                if content_file.name.startswith('CLAUDE') and content_file.name.endswith('.md'):
                    rule_patterns.append(content_file.name)
        except:
            pass
        
        max_file_size = self.config.rule_extraction.max_file_size
        
        for pattern in rule_patterns:
            try:
                file_content = repo.get_contents(pattern)
                if file_content.size > 0 and file_content.size < max_file_size:
                    decoded = file_content.decoded_content.decode('utf-8', errors='ignore')
                    rule_files.append({
                        'path': pattern,
                        'content': decoded,
                        'format': pattern.split('.')[-1] if '.' in pattern else 'md'
                    })
                    logger.info(f"Found IDE rule file: {pattern} ({file_content.size} bytes)")
            except:
                continue
        
        return rule_files
    
    def _extract_and_link_rules(self, pattern, repo, rule_files):
        """
        Extract IDE rules and link them to the pattern.
        
        Args:
            pattern: The pattern dict with pattern_name
            repo: PyGithub Repository object
            rule_files: List of rule file dicts from _scan_for_rule_files
        """
        if not IDE_RULE_LIBRARY_AVAILABLE or not self.rule_extractor:
            return
        
        # Prepare repo metadata for quality scoring
        from ide_rule_library.quality_scorer import enhance_repo_metadata
        repo_data = {
            'name': repo.full_name,
            'stars': repo.stargazers_count,
            'forks': repo.forks_count,
            'created_at': repo.created_at,
            'updated_at': repo.updated_at,
            'open_issues': repo.open_issues_count,
            'html_url': repo.html_url
        }
        
        # Get contributors (with error handling)
        try:
            contributors = [c.login for c in repo.get_contributors()[:50]]  # Limit to 50
            repo_data['contributors'] = contributors
        except:
            repo_data['contributors'] = []
        
        # Get file list for production signals
        try:
            contents = repo.get_contents("")
            repo_data['files'] = [f.path for f in contents if not f.type == "dir"]
        except:
            repo_data['files'] = []
        
        # Enhance with quality scoring
        enhanced_repo = enhance_repo_metadata(repo_data)
        
        # Log quality metrics for UI
        quality_score = enhanced_repo.get('repo_quality_score', 0)
        quality_breakdown = enhanced_repo.get('quality_breakdown', {})
        prod_signals = []
        if enhanced_repo.get('has_ci_cd'): prod_signals.append('CI/CD')
        if enhanced_repo.get('has_tests'): prod_signals.append('Tests')
        if enhanced_repo.get('has_docker'): prod_signals.append('Docker')
        if enhanced_repo.get('has_monitoring'): prod_signals.append('Monitoring')
        
        logger.info(f"Quality Score: {quality_score:.1f}/100 " + 
                   (f"(Production: {', '.join(prod_signals)})" if prod_signals else "(No production signals)"))
        
        if self.progress_callback:
            self.progress_callback({
                'type': 'quality_score',
                'repo': repo.full_name,
                'score': quality_score,
                'breakdown': quality_breakdown,
                'production_signals': prod_signals
            })
        
        # Extract each rule file
        for rule_file in rule_files:
            try:
                logger.info(f"Extracting rule: {rule_file['path']}")
                
                # Rate limit before API call
                wait_time = self.gemini_rate_limiter.wait_if_needed()
                if wait_time > 0:
                    logger.info(f"Rate limited: waited {wait_time:.2f}s before extracting {rule_file['path']}")
                
                # Extract rule with enhanced analysis
                self.metrics.start_timer('rule_extraction')
                try:
                    rule = self.rule_extractor.extract_rule(
                        file_content=rule_file['content'],
                        file_path=rule_file['path'],
                        repo_data=enhanced_repo
                    )
                    self.metrics.end_timer('rule_extraction')
                    self.metrics.increment('rules_extracted')
                except Exception as extract_error:
                    self.metrics.end_timer('rule_extraction')
                    # Check if it's a known exception type from ide_rule_library
                    error_name = extract_error.__class__.__name__
                    
                    if 'QuotaExceeded' in error_name or 'RateLimit' in error_name:
                        self.metrics.increment('rule_extraction.quota_exceeded')
                        logger.error(f"Gemini quota exceeded for {rule_file['path']}")
                        raise RateLimitError(f"Gemini quota exceeded for {repo.full_name}") from extract_error
                    elif 'Timeout' in error_name:
                        self.metrics.increment('rule_extraction.timeout')
                        logger.warning(f"Timeout extracting rule from {rule_file['path']}, skipping")
                        continue  # Skip this rule, continue with others
                    else:
                        self.metrics.increment('rule_extraction.error')
                        logger.error(f"Unexpected error extracting {rule_file['path']}: {extract_error}", exc_info=True)
                        raise RuleExtractionError(f"Failed to extract {rule_file['path']}") from extract_error
                
                # Link to pattern in Neo4j
                try:
                    self._link_pattern_to_rules(
                        pattern_name=pattern['pattern_name'],
                        source_repo=repo.html_url,
                        rule=rule
                    )
                    self.metrics.increment('rules_linked')
                    
                    # Log rule extraction success with details
                    confidence = rule.get('confidence_level', 3)
                    purpose = rule.get('purpose', 'Unknown purpose')[:80]
                    logger.info(f"Rule extracted: {rule_file['path']} (confidence: {confidence}/5)")
                    
                    if self.progress_callback:
                        self.progress_callback({
                            'type': 'rule_extracted',
                            'repo': repo.full_name,
                            'file': rule_file['path'],
                            'confidence': confidence,
                            'purpose': purpose,
                            'categories': rule.get('categories', [])
                        })
                    
                except Exception as db_error:
                    self.metrics.increment('database_write.error')
                    logger.error(f"Failed to link rule {rule_file['path']} to Neo4j: {db_error}", exc_info=True)
                    raise DatabaseWriteError(f"Failed to link rule {rule_file['path']} to pattern") from db_error
                
            except (RateLimitError, DatabaseWriteError):
                # Re-raise these specific errors to be handled by caller
                raise
            except RuleExtractionError as e:
                logger.error(f"Rule extraction failed for {rule_file['path']}: {e}")
                continue  # Skip to next rule file
            except Exception as e:
                logger.error(f"Unexpected error processing rule {rule_file['path']}: {e}", exc_info=True)
                continue  # Skip to next rule file
    
    def _link_pattern_to_rules(self, pattern_name, source_repo, rule):
        """
        Create HAS_IDE_RULES relationship between Pattern and IDERule in Neo4j.
        
        Args:
            pattern_name: Name of the pattern
            source_repo: Repository URL
            rule: Rule dict from EnhancedRuleExtractor
        """
        with self.neo4j.session() as session:
            # Create IDERule node and link to Pattern
            query = """
            // Find the Pattern node
            MATCH (p:Pattern {name: $pattern_name, source_repo: $source_repo})
            
            // Create or merge IDERule node
            MERGE (r:IDERule {id: $rule_id})
            ON CREATE SET
                r.source_repo = $source_repo,
                r.file_path = $file_path,
                r.file_format = $file_format,
                r.content = $content,
                r.purpose = $purpose,
                r.categories = $categories,
                r.key_practices = $key_practices,
                r.technologies = $technologies,
                r.project_types = $project_types,
                r.ide_types = $ide_types,
                r.repo_quality_score = $repo_quality_score,
                r.confidence_level = $confidence_level,
                r.quality_breakdown_json = $quality_breakdown_json,
                r.has_ci_cd = $has_ci_cd,
                r.has_tests = $has_tests,
                r.extracted_date = datetime()
            ON MATCH SET
                r.content = $content,
                r.purpose = $purpose,
                r.categories = $categories,
                r.key_practices = $key_practices,
                r.technologies = $technologies,
                r.project_types = $project_types,
                r.repo_quality_score = $repo_quality_score,
                r.confidence_level = $confidence_level,
                r.quality_breakdown_json = $quality_breakdown_json,
                r.extracted_date = datetime()
            
            // Create relationship
            MERGE (p)-[:HAS_IDE_RULES]->(r)
            
            RETURN r.id as rule_id
            """
            
            # Prepare parameters
            import json
            params = {
                'pattern_name': pattern_name,
                'source_repo': source_repo,
                'rule_id': f"{source_repo}:{rule['file_path']}",
                'file_path': rule['file_path'],
                'file_format': rule.get('file_format', 'unknown'),
                'content': rule.get('content', ''),
                'purpose': rule.get('purpose', ''),
                'categories': rule.get('categories', []),
                'key_practices': rule.get('key_practices', []),
                'technologies': rule.get('technologies', []),
                'project_types': rule.get('project_types', []),
                'ide_types': rule.get('ide_types', ['cursor']),
                'repo_quality_score': rule.get('repo_quality_score', 0),
                'confidence_level': rule.get('confidence_level', 3),
                'quality_breakdown_json': json.dumps(rule.get('quality_breakdown', {})),
                'has_ci_cd': rule.get('has_ci_cd', False),
                'has_tests': rule.get('has_tests', False)
            }
            
            result = session.run(query, params)
            record = result.single()
            result.consume()  # Close the stream to prevent resource leaks
            
            if record:
                logger.info(f"Linked rule {record['rule_id']} to pattern {pattern_name}")
            else:
                logger.warning(f"Failed to link rule to pattern {pattern_name}")
    
    @llm_retry
    def _extract_with_llm(self, **kwargs):
        """Use LLM to extract pattern from repo with retry logic."""
        logger.info(f"Extracting pattern with LLM for {kwargs.get('repo_name', 'unknown')}")
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
    
    def _validate_pattern_async(self, pattern, repo_context=None):
        """
        Async pattern validation using critic and judge.
        Returns immediately, validation happens in background.
        Updates Neo4j with validation and judge results when complete.
        
        Args:
            pattern: Pattern to validate
            repo_context: Repository context for judge evaluation
        """
        if not self.critic:
            logger.debug("Critic not available, skipping validation")
            return None
        
        # Capture references for closure
        trajectory_logger = self.trajectory_logger
        judge = self.judge
        
        def validation_task():
            try:
                # Step 1: Critic validation
                logger.info(f"Starting async validation for pattern: {pattern.get('pattern_name', 'unknown')}")
                start_time = time.time()
                score, needs_review, notes = self.critic.validate_pattern(pattern)
                response_time = time.time() - start_time
                
                # Update Neo4j with validation results
                self._update_pattern_validation(
                    pattern_name=pattern['pattern_name'],
                    validation_score=score,
                    needs_review=needs_review,
                    critic_notes=notes
                )
                
                # Log critic validation
                if trajectory_logger:
                    trajectory_logger.log_critic_validation(
                        pattern['pattern_name'], score, needs_review, response_time
                    )
                
                logger.info(f"Validation complete: {pattern['pattern_name']} - score={score:.2f}, needs_review={needs_review}")
                
                # Step 2: Judge evaluation (if available and critic passed threshold)
                if judge and score >= 0.6:  # Only judge patterns that pass basic validation
                    try:
                        logger.info(f"Starting judge evaluation for pattern: {pattern['pattern_name']}")
                        judge_start = time.time()
                        judge_score, judge_feedback = judge.evaluate_pattern(pattern, repo_context)
                        judge_time = time.time() - judge_start
                        
                        # Update Neo4j with judge results
                        self._update_pattern_judge_evaluation(
                            pattern_name=pattern['pattern_name'],
                            judge_score=judge_score,
                            judge_feedback=judge_feedback
                        )
                        
                        # Log judge evaluation
                        if trajectory_logger:
                            trajectory_logger.log_event("judge_evaluation", {
                                "pattern": pattern['pattern_name'],
                                "judge_score": round(judge_score, 3),
                                "quality_tier": judge.get_quality_tier(judge_score),
                                "response_time_seconds": round(judge_time, 3)
                            })
                        
                        logger.info(f"Judge evaluation complete: {pattern['pattern_name']} - score={judge_score:.2f}")
                        
                    except Exception as judge_error:
                        logger.error(f"Judge evaluation failed for {pattern['pattern_name']}: {judge_error}")
                
            except Exception as e:
                logger.error(f"Async validation failed for {pattern.get('pattern_name', 'unknown')}: {e}")
        
        # Submit to thread pool (non-blocking)
        future = self.critic_executor.submit(validation_task)
        return future
    
    @neo4j_retry
    def _update_pattern_validation(self, pattern_name, validation_score, needs_review, critic_notes):
        """Update pattern with validation results."""
        with self.neo4j.session() as session:
            session.run("""
                MATCH (p:Pattern {name: $pattern_name})
                SET p.validation_score = $validation_score,
                    p.needs_review = $needs_review,
                    p.critic_notes = $critic_notes,
                    p.validated_at = datetime()
            """,
                pattern_name=pattern_name,
                validation_score=float(validation_score),
                needs_review=needs_review,
                critic_notes=critic_notes
            )
        logger.debug(f"Updated validation for pattern: {pattern_name}")
    
    @neo4j_retry
    def _update_pattern_judge_evaluation(self, pattern_name, judge_score, judge_feedback):
        """Update pattern with judge evaluation results."""
        with self.neo4j.session() as session:
            session.run("""
                MATCH (p:Pattern {name: $pattern_name})
                SET p.judge_score = $judge_score,
                    p.judge_feedback = $judge_feedback,
                    p.judged_at = datetime()
            """,
                pattern_name=pattern_name,
                judge_score=float(judge_score),
                judge_feedback=judge_feedback
            )
        logger.debug(f"Updated judge evaluation for pattern: {pattern_name}")
    
    @neo4j_retry
    def _store_pattern(self, pattern):
        """Store pattern in Neo4j with normalized data and weights with retry logic."""
        logger.info(f"Storing pattern '{pattern.get('pattern_name', 'unknown')}' in Neo4j")
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
        
        # Get quality metrics (if available) - 0-100 scale
        quality_score = pattern.get('quality_score', 50.0)
        freshness_score = pattern.get('freshness_score', 50.0)
        maintenance_score = pattern.get('maintenance_score', 50.0)
        
        # Get extraction metadata
        extraction_status = pattern.get('extraction_status', 'unknown')
        data_availability = pattern.get('data_availability', {})
        
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
                // MERGE pattern node by source_repo (handles both create and update)
                MERGE (p:Pattern {source_repo: $source_repo})
                ON CREATE SET 
                    p.name = $pattern_name,
                    p.confidence = $confidence,
                    p.stars = $stars,
                    p.reasoning = $reasoning,
                    p.quality_score = $quality_score,
                    p.freshness_score = $freshness_score,
                    p.maintenance_score = $maintenance_score,
                    p.validation_score = 0.0,
                    p.needs_review = true,
                    p.critic_notes = "Validation pending...",
                    p.judge_score = 0.0,
                    p.judge_feedback = "Judge evaluation pending...",
                    p.extraction_status = $extraction_status,
                    p.has_readme = $has_readme,
                    p.has_structure = $has_structure,
                    p.has_dependencies = $has_dependencies,
                    p.has_quality_metrics = $has_quality_metrics,
                    p.extracted_at = datetime()
                ON MATCH SET
                    p.name = $pattern_name,
                    p.confidence = $confidence,
                    p.stars = $stars,
                    p.reasoning = $reasoning,
                    p.quality_score = $quality_score,
                    p.freshness_score = $freshness_score,
                    p.maintenance_score = $maintenance_score,
                    p.extraction_status = $extraction_status,
                    p.has_readme = $has_readme,
                    p.has_structure = $has_structure,
                    p.has_dependencies = $has_dependencies,
                    p.has_quality_metrics = $has_quality_metrics,
                    p.extracted_at = datetime()
                
                // MERGE requirement node and relationship
                MERGE (r:Requirement {type: $req_type, domain: $req_domain})
                MERGE (r)-[:SOLVED_BY]->(p)
                
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
                extraction_status=extraction_status,
                has_readme=data_availability.get('readme', False),
                has_structure=data_availability.get('structure', False),
                has_dependencies=data_availability.get('dependencies', False),
                has_quality_metrics=data_availability.get('quality_metrics', False),
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
            
            # Extract IDE rules if available and enabled
            if (self.config.rule_extraction.enabled and
                IDE_RULE_LIBRARY_AVAILABLE and self.rule_extractor):
                try:
                    rule_files = self._scan_for_rule_files(repo)
                    if rule_files:
                        print(f"[INFO] Found {len(rule_files)} IDE rule file(s), extracting...")
                        self._extract_and_link_rules(pattern, repo, rule_files)
                    else:
                        logger.info(f"No IDE rules found in {repo_name}")
                        if self.progress_callback:
                            self.progress_callback({
                                'type': 'no_rules',
                                'repo': repo.full_name
                            })
                except Exception as e:
                    logger.warning(f"Rule extraction failed for {repo_name}: {e}")
                    print(f"[WARN] Rule extraction failed: {e}")
            
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
