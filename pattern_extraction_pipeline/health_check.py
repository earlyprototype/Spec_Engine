"""
Health Check

System health checks for verifying all dependencies and services are operational.
Checks Neo4j, Gemini API, GitHub API, and IDE Rule Library availability.
"""

import os
import logging
from typing import Dict, Tuple
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def check_neo4j() -> Tuple[bool, str]:
    """
    Check Neo4j database connectivity.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        from neo4j import GraphDatabase
        
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7688")  # Default to spec-engine-neo4j
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD")
        
        if not password:
            return False, "NEO4J_PASSWORD not set"
        
        driver = GraphDatabase.driver(uri, auth=(user, password))
        
        # Test connection with a simple query
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            record = result.single()
            result.consume()
            
            if record and record['test'] == 1:
                driver.close()
                return True, f"Connected to {uri}"
            else:
                driver.close()
                return False, "Query test failed"
    
    except ImportError:
        return False, "neo4j package not installed"
    except Exception as e:
        return False, f"Connection failed: {str(e)}"


def check_gemini() -> Tuple[bool, str]:
    """
    Check Gemini API connectivity and authentication.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        import google.generativeai as genai
        
        load_dotenv(override=True)
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            return False, "GEMINI_API_KEY not set"
        
        # Configure and test with a simple request
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Simple test prompt
        response = model.generate_content("Respond with 'OK' if you can read this.")
        
        if response and response.text:
            return True, "API key valid, model responsive"
        else:
            return False, "Model did not respond"
    
    except ImportError:
        return False, "google-generativeai package not installed"
    except Exception as e:
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg or "invalid_api_key" in error_msg:
            return False, "Invalid API key"
        elif "quota" in error_msg.lower():
            return False, "Quota exceeded"
        else:
            return False, f"API check failed: {error_msg[:100]}"


def check_github() -> Tuple[bool, str]:
    """
    Check GitHub API connectivity and authentication.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        from github import Github
        
        # Load config to get token_env, fallback to default if config unavailable
        try:
            import yaml
            from pathlib import Path
            config_path = Path(__file__).parent / "config.yaml"
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f)
            token_env = config_data.get('github', {}).get('token_env', 'GITHUB_TOKEN')
        except Exception:
            token_env = 'GITHUB_TOKEN'  # Fallback to default
        
        token = os.getenv(token_env)
        
        if not token:
            return False, f"{token_env} not set"
        
        from github import Auth
        gh = Github(auth=Auth.Token(token))
        
        # Test with a simple API call
        user = gh.get_user()
        login = user.login
        
        # Check rate limit
        rate_limit = gh.get_rate_limit()
        remaining = rate_limit.core.remaining
        
        return True, f"Authenticated as {login}, rate limit: {remaining} requests remaining"
    
    except ImportError:
        return False, "PyGithub package not installed"
    except Exception as e:
        error_msg = str(e)
        if "Bad credentials" in error_msg:
            return False, "Invalid GitHub token"
        else:
            return False, f"API check failed: {error_msg[:100]}"


def check_ide_rule_library() -> Tuple[bool, str]:
    """
    Check IDE Rule Library availability.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        from ide_rule_library.enhanced_rule_extractor import EnhancedRuleExtractor
        from ide_rule_library.quality_scorer import RepoQualityScorer
        
        # Try to instantiate (without actually calling APIs)
        try:
            extractor = EnhancedRuleExtractor(model_name='gemini-2.5-flash', logger=logger)
            scorer = RepoQualityScorer()
            return True, "IDE Rule Library available and importable"
        except Exception as init_error:
            return True, f"Importable but init warning: {str(init_error)[:50]}"
    
    except ImportError as e:
        return False, f"Not available: {str(e)}"


def check_health(verbose: bool = False) -> Dict:
    """
    Run all health checks.
    
    Args:
        verbose: If True, log results
    
    Returns:
        dict: Health check results
            {
                'healthy': bool,
                'checks': {
                    'neo4j': {'ok': bool, 'message': str},
                    'gemini_api': {'ok': bool, 'message': str},
                    'github_api': {'ok': bool, 'message': str},
                    'ide_rule_library': {'ok': bool, 'message': str}
                }
            }
    """
    results = {
        'neo4j': check_neo4j(),
        'gemini_api': check_gemini(),
        'github_api': check_github(),
        'ide_rule_library': check_ide_rule_library()
    }
    
    # Format results
    checks = {
        name: {'ok': success, 'message': message}
        for name, (success, message) in results.items()
    }
    
    # Overall health: core services must pass, IDE library is optional
    core_healthy = all([
        checks['neo4j']['ok'],
        checks['gemini_api']['ok'],
        checks['github_api']['ok']
    ])
    
    health = {
        'healthy': core_healthy,
        'checks': checks
    }
    
    if verbose:
        logger.info("Health check results:")
        for name, check in checks.items():
            status = "OK" if check['ok'] else "FAIL"
            logger.info(f"  [{status}] {name}: {check['message']}")
        
        if health['healthy']:
            logger.info("System is healthy")
        else:
            logger.warning("System is unhealthy - some checks failed")
    
    return health


def print_health_report():
    """Print a human-readable health check report."""
    print("\n" + "="*60)
    print("SYSTEM HEALTH CHECK")
    print("="*60)
    
    health = check_health(verbose=False)
    
    for name, check in health['checks'].items():
        status = "OK" if check['ok'] else "FAIL"
        symbol = "[+]" if check['ok'] else "[X]"
        print(f"{symbol} {name:20s}: {check['message']}")
    
    print("="*60)
    
    if health['healthy']:
        print("Status: HEALTHY - All core services operational")
    else:
        print("Status: UNHEALTHY - Some core services are down")
        print("\nCore services required: Neo4j, Gemini API, GitHub API")
        print("Optional: IDE Rule Library (for rule extraction)")
    
    print("="*60 + "\n")
    
    return health['healthy']


if __name__ == "__main__":
    # Run health check when executed directly
    logging.basicConfig(level=logging.INFO)
    healthy = print_health_report()
    
    # Exit with appropriate code
    exit(0 if healthy else 1)
