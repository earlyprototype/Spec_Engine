# check_readiness.py
# Check if system is ready for full pattern extraction test

import os
import sys
import subprocess

def check_docker():
    """Check if Docker is installed and running."""
    print("\n[1/6] Checking Docker...")
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"  [OK] Docker installed: {result.stdout.strip()}")
            
            # Check if Docker daemon is running
            result = subprocess.run(['docker', 'ps'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("  [OK] Docker is running")
                return True
            else:
                print("  [X] Docker is not running. Start Docker Desktop.")
                return False
        else:
            print("  [X] Docker not found")
            return False
    except Exception as e:
        print(f"  [X] Docker check failed: {e}")
        return False

def check_python():
    """Check Python version."""
    print("\n[2/6] Checking Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  [OK] Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  [X] Python {version.major}.{version.minor} (need 3.8+)")
        return False

def check_dependencies():
    """Check if Python packages are installed."""
    print("\n[3/6] Checking Python dependencies...")
    required = ['github', 'google-generativeai', 'neo4j', 'dotenv']
    missing = []
    
    for package in required:
        try:
            if package == 'github':
                __import__('github')
            elif package == 'dotenv':
                __import__('dotenv')
            elif package == 'google-generativeai':
                __import__('google.generativeai')
            else:
                __import__(package)
            print(f"  [OK] {package}")
        except ImportError:
            print(f"  [X] {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\n  To install: pip install -r requirements.txt")
        return False
    return True

def check_env_file():
    """Check if .env file exists and has required keys."""
    print("\n[4/6] Checking environment configuration...")
    
    if not os.path.exists('.env'):
        print("  [X] .env file not found")
        print("  Run: copy env.template .env")
        print("  Then edit .env and add your API keys")
        return False
    
    print("  [OK] .env file exists")
    
    # Check if keys are configured
    from dotenv import load_dotenv
    load_dotenv()
    
    github_token = os.getenv('GITHUB_TOKEN')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    has_github = github_token and github_token != 'ghp_your_token_here'
    has_gemini = gemini_key and gemini_key != 'YOUR_GEMINI_KEY_HERE'
    
    if has_github:
        print(f"  [OK] GITHUB_TOKEN configured ({github_token[:7]}...)")
    else:
        print("  [X] GITHUB_TOKEN not configured")
    
    if has_gemini:
        print(f"  [OK] GEMINI_API_KEY configured")
    else:
        print("  [X] GEMINI_API_KEY not configured")
    
    return has_github and has_gemini

def check_neo4j():
    """Check if Neo4j container is running."""
    print("\n[5/6] Checking Neo4j...")
    try:
        result = subprocess.run(
            ['docker', 'ps', '--filter', 'name=neo4j', '--format', '{{.Names}}'],
            capture_output=True, text=True, timeout=5
        )
        
        if 'neo4j' in result.stdout:
            # Find which container is actually running
            container_name = result.stdout.strip().split('\n')[0]
            print(f"  [OK] Neo4j container running ({container_name})")
            print("  Browser: http://localhost:7474")
            return True
        else:
            print("  [X] Neo4j container not running")
            print("  Your existing container should be running")
            return False
    except Exception as e:
        print(f"  [X] Neo4j check failed: {e}")
        return False

def test_connections():
    """Test API connections."""
    print("\n[6/6] Testing API connections...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    # Test GitHub
    try:
        from github import Github
        gh = Github(os.getenv('GITHUB_TOKEN'))
        rate = gh.get_rate_limit()
        print(f"  [OK] GitHub API connected (rate limit: {rate.core.remaining}/{rate.core.limit})")
        github_ok = True
    except Exception as e:
        print(f"  [X] GitHub API failed: {e}")
        github_ok = False
    
    # Test Google Gemini
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        # Just check if API key is configured (don't make actual API call)
        print(f"  [OK] Google Gemini API configured")
        gemini_ok = True
    except Exception as e:
        print(f"  [X] Google Gemini API failed: {e}")
        gemini_ok = False
    
    # Test Neo4j
    try:
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "password")
        )
        with driver.session() as session:
            result = session.run("RETURN 1")
            record = result.single()
        driver.close()
        print(f"  [OK] Neo4j connected")
        neo4j_ok = True
    except Exception as e:
        print(f"  [X] Neo4j connection failed: {e}")
        neo4j_ok = False
    
    return github_ok and gemini_ok and neo4j_ok

def main():
    print("="*70)
    print("PATTERN EXTRACTION PIPELINE - READINESS CHECK")
    print("="*70)
    
    checks = [
        check_docker(),
        check_python(),
        check_dependencies(),
        check_env_file(),
        check_neo4j(),
        test_connections()
    ]
    
    print("\n" + "="*70)
    print("READINESS SUMMARY")
    print("="*70)
    
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"\n[OK] ALL CHECKS PASSED ({passed}/{total})")
        print("\nYou're ready to run:")
        print("  python test_extraction.py  (single repo test, FREE)")
        print("  python batch_extract.py    (batch extraction, FREE)")
        print("  python issue_miner.py      (issue mining, FREE)")
    else:
        print(f"\n[X] CHECKS FAILED ({passed}/{total})")
        print("\nFix the issues above, then run this script again.")
        
        if not checks[0]:  # Docker
            print("\n1. Install Docker Desktop")
            print("   https://www.docker.com/products/docker-desktop")
        
        if not checks[3]:  # Env file
            print("\n2. Configure API keys")
            print("   copy env.template .env")
            print("   notepad .env")
            print("   Add GITHUB_TOKEN and GEMINI_API_KEY")
        
        if not checks[4]:  # Neo4j
            print("\n3. Start Neo4j")
            print("   docker-compose up -d")
    
    print("\n" + "="*70)
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
