# grep_app_mcp Integration Plan

**Status:** Implementation Roadmap  
**Date:** 5 January 2026  
**Parent:** Pattern Extraction Pipeline v1.0

---

## Executive Summary

Integrate grep_app_mcp to enhance pattern extraction with actual code analysis, moving from documentation-based inference to code-verified patterns.

**Goals:**
1. Validate low-confidence patterns with actual code evidence
2. Extract concrete implementation examples for patterns
3. Enable code-level anti-pattern detection
4. Compare implementations across repositories

**Timeline:** 2 weeks (Weeks 7-8)  
**Estimated Cost:** +$6 (selective approach)  
**Expected ROI:** 50% confidence increase for low-confidence patterns

---

## High Priority Tasks (Week 7)

### Task 1.1: Setup grep_app_mcp Server (Day 1 - Monday)

**Objective:** Install and configure grep_app_mcp as MCP server

**Steps:**

1. **Clone grep_app_mcp repository**
```powershell
cd C:\Users\Fab2\Desktop\AI\Specs
git clone https://github.com/ai-tools-all/grep_app_mcp.git
cd grep_app_mcp
```

2. **Install dependencies**
```powershell
npm install
```

3. **Build the project**
```powershell
npm run build
```

4. **Test the server**
```powershell
# HTTP mode (recommended)
.\run.sh http dev

# Verify endpoints:
# - HTTP: http://localhost:8603/mcp
# - SSE: http://localhost:8603/sse
```

5. **Configure for production**
```powershell
# Start in production mode
.\run.sh http prod

# Verify server is running
curl http://localhost:8603/mcp
```

**Success Criteria:**
- [ ] grep_app_mcp server running on localhost:8603
- [ ] Can execute test search: `searchCode("async function")`
- [ ] Can retrieve file: `github_file("microsoft", "vscode", "README.md")`

**Time Estimate:** 2 hours  
**Cost:** $0

---

### Task 1.2: Create grep_app_mcp Python Client (Day 1 - Monday)

**Objective:** Build Python wrapper to interact with grep_app_mcp server

**File:** `pattern_extraction_pipeline/grep_app_client.py`

**Implementation:**

```python
# grep_app_client.py
# Python client for grep_app_mcp server

import requests
import json
from typing import List, Dict, Optional

class GrepAppClient:
    def __init__(self, base_url="http://localhost:8603"):
        self.base_url = base_url
        self.mcp_endpoint = f"{base_url}/mcp"
    
    def search_code(
        self,
        query: str,
        repo_filter: Optional[str] = None,
        lang_filter: Optional[str] = None,
        numbered_output: bool = False,
        use_regex: bool = False
    ) -> List[Dict]:
        """
        Search for code across GitHub repositories.
        
        Args:
            query: Search query string
            repo_filter: Filter by repository name pattern
            lang_filter: Filter by programming language(s)
            numbered_output: Return numbered list format
            use_regex: Treat query as regex pattern
        
        Returns:
            List of search results with file paths and snippets
        """
        payload = {
            "method": "tools/call",
            "params": {
                "name": "searchCode",
                "arguments": {
                    "query": query,
                    "numberedOutput": numbered_output,
                    "useRegex": use_regex
                }
            }
        }
        
        if repo_filter:
            payload["params"]["arguments"]["repoFilter"] = repo_filter
        if lang_filter:
            payload["params"]["arguments"]["langFilter"] = lang_filter
        
        try:
            response = requests.post(
                self.mcp_endpoint,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            result = response.json()
            return self._parse_search_results(result)
            
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def github_file(
        self,
        owner: str,
        repo: str,
        path: str,
        ref: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Fetch a single file from GitHub repository.
        
        Args:
            owner: Repository owner
            repo: Repository name
            path: File path
            ref: Branch/commit/tag reference
        
        Returns:
            File content and metadata
        """
        payload = {
            "method": "tools/call",
            "params": {
                "name": "github_file",
                "arguments": {
                    "owner": owner,
                    "repo": repo,
                    "path": path
                }
            }
        }
        
        if ref:
            payload["params"]["arguments"]["ref"] = ref
        
        try:
            response = requests.post(
                self.mcp_endpoint,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            result = response.json()
            return self._parse_file_result(result)
            
        except Exception as e:
            print(f"File fetch error: {e}")
            return None
    
    def batch_retrieve_files(
        self,
        files: List[Dict[str, str]]
    ) -> List[Dict]:
        """
        Retrieve multiple files in parallel.
        
        Args:
            files: List of dicts with owner, repo, path, optional ref
        
        Returns:
            List of file contents
        """
        payload = {
            "method": "tools/call",
            "params": {
                "name": "github_batch_files",
                "arguments": {
                    "files": files
                }
            }
        }
        
        try:
            response = requests.post(
                self.mcp_endpoint,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            result = response.json()
            return self._parse_batch_results(result)
            
        except Exception as e:
            print(f"Batch fetch error: {e}")
            return []
    
    def _parse_search_results(self, result: Dict) -> List[Dict]:
        """Parse search results from MCP response."""
        # Extract content from MCP response format
        if "result" in result and "content" in result["result"]:
            content = result["result"]["content"]
            
            # Parse content into structured format
            # (Implementation depends on grep_app_mcp response format)
            return content if isinstance(content, list) else []
        
        return []
    
    def _parse_file_result(self, result: Dict) -> Optional[Dict]:
        """Parse file result from MCP response."""
        if "result" in result and "content" in result["result"]:
            return result["result"]["content"]
        return None
    
    def _parse_batch_results(self, result: Dict) -> List[Dict]:
        """Parse batch results from MCP response."""
        if "result" in result and "content" in result["result"]:
            content = result["result"]["content"]
            return content if isinstance(content, list) else []
        return []
    
    def health_check(self) -> bool:
        """Check if grep_app_mcp server is available."""
        try:
            response = requests.get(f"{self.base_url}/sse")
            return response.status_code == 200
        except:
            return False

# Usage example
if __name__ == "__main__":
    client = GrepAppClient()
    
    # Health check
    if not client.health_check():
        print("Error: grep_app_mcp server not available")
        exit(1)
    
    print("✓ grep_app_mcp server available")
    
    # Test search
    print("\nTesting code search...")
    results = client.search_code(
        query="fs.watch",
        lang_filter="JavaScript,TypeScript"
    )
    print(f"Found {len(results)} results")
    
    # Test file retrieval
    print("\nTesting file retrieval...")
    file_content = client.github_file(
        owner="microsoft",
        repo="vscode",
        path="README.md"
    )
    if file_content:
        print("✓ File retrieved successfully")
    else:
        print("✗ File retrieval failed")
```

**Success Criteria:**
- [ ] Client can connect to grep_app_mcp server
- [ ] `search_code()` returns results
- [ ] `github_file()` retrieves content
- [ ] `batch_retrieve_files()` works
- [ ] Error handling works gracefully

**Time Estimate:** 3 hours  
**Cost:** $0

---

### Task 1.3: Enhance Pattern Extractor with Code Analysis (Day 2-3 - Tuesday-Wednesday)

**Objective:** Integrate grep_app_mcp into pattern extraction for low-confidence pattern validation

**File:** `pattern_extraction_pipeline/code_enhanced_extractor.py`

**Implementation:**

```python
# code_enhanced_extractor.py
# Enhanced pattern extractor with code analysis

import os
import json
from pattern_extractor import PatternExtractor
from grep_app_client import GrepAppClient

class CodeEnhancedExtractor(PatternExtractor):
    """Enhanced pattern extractor with code-level analysis."""
    
    def __init__(self):
        super().__init__()
        self.grep_client = GrepAppClient()
        
        # Check if grep_app_mcp is available
        if not self.grep_client.health_check():
            print("⚠ grep_app_mcp server not available")
            print("  Falling back to standard extraction")
            self.code_analysis_enabled = False
        else:
            print("✓ grep_app_mcp server available")
            self.code_analysis_enabled = True
        
        # Pattern-to-code search mapping
        self.pattern_searches = {
            'filesystem_browser': [
                'fs.watch',
                'chokidar.watch',
                'watchdog.Observer',
                'FileSystemWatcher'
            ],
            'database_primary_storage': [
                'db.query',
                'prisma.findMany',
                'mongoose.find',
                'sequelize.findAll'
            ],
            'api_gateway': [
                'express.Router',
                'fastify.route',
                'app.route',
                'APIGateway'
            ],
            'event_driven': [
                'EventEmitter',
                'on(.*event',
                'addEventListener',
                'pubsub.publish'
            ]
        }
    
    def analyze_single_repo_enhanced(self, repo_name, domain="general"):
        """
        Enhanced single repo analysis with code verification.
        
        Args:
            repo_name: Full repo name (e.g., "microsoft/vscode")
            domain: Domain hint for pattern extraction
        
        Returns:
            Enhanced pattern dict with code examples
        """
        print(f"\n=== Analyzing {repo_name} (Enhanced) ===")
        
        # 1. Standard analysis (README, structure, deps)
        pattern = super().analyze_single_repo(repo_name, domain)
        
        # 2. If low confidence, validate with code
        if pattern.get('confidence') == 'low' and self.code_analysis_enabled:
            print(f"\n→ Low confidence detected, searching code...")
            
            code_evidence = self._search_code_evidence(
                repo_name=repo_name,
                pattern_name=pattern['pattern_name']
            )
            
            if code_evidence:
                print(f"  ✓ Found {len(code_evidence)} code examples")
                pattern['confidence'] = 'medium'
                pattern['code_evidence'] = code_evidence
                pattern['validation_method'] = 'code_analysis'
            else:
                print(f"  ⚠ No code evidence found")
        
        # 3. Extract implementation examples
        if self.code_analysis_enabled:
            print(f"\n→ Extracting implementation examples...")
            
            implementations = self._extract_implementation_files(
                repo_name=repo_name,
                pattern_name=pattern['pattern_name']
            )
            
            if implementations:
                print(f"  ✓ Found {len(implementations)} implementation files")
                pattern['implementations'] = implementations
        
        return pattern
    
    def _search_code_evidence(self, repo_name, pattern_name):
        """
        Search for code evidence of pattern in repository.
        
        Args:
            repo_name: Repository to search
            pattern_name: Pattern to validate
        
        Returns:
            List of code evidence dicts
        """
        searches = self.pattern_searches.get(pattern_name, [])
        if not searches:
            return []
        
        evidence = []
        
        for search_term in searches[:3]:  # Limit to 3 searches per pattern
            print(f"    Searching: {search_term}")
            
            try:
                results = self.grep_client.search_code(
                    query=search_term,
                    repo_filter=repo_name,
                    numbered_output=True,
                    use_regex='(' in search_term  # Use regex if contains (
                )
                
                for result in results[:2]:  # Top 2 results per search
                    evidence.append({
                        'search_term': search_term,
                        'file_path': result.get('file_path', 'unknown'),
                        'snippet': result.get('snippet', '')[:200],  # First 200 chars
                        'line_number': result.get('line', 0)
                    })
                    
            except Exception as e:
                print(f"    Search error: {e}")
                continue
        
        return evidence
    
    def _extract_implementation_files(self, repo_name, pattern_name):
        """
        Extract key implementation files for pattern.
        
        Args:
            repo_name: Repository name
            pattern_name: Pattern name
        
        Returns:
            List of implementation file dicts
        """
        # Map patterns to key file search terms
        file_searches = {
            'filesystem_browser': ['watcher', 'explorer', 'filesystem', 'filemanager'],
            'database_primary_storage': ['repository', 'model', 'schema', 'database'],
            'api_gateway': ['router', 'controller', 'handler', 'endpoint'],
            'event_driven': ['event', 'emitter', 'subscriber', 'listener']
        }
        
        search_terms = file_searches.get(pattern_name, [])
        if not search_terms:
            return []
        
        owner, repo = repo_name.split('/')
        files_to_fetch = []
        
        # Search for key files
        for term in search_terms[:2]:  # Limit to 2 terms
            print(f"    Searching files with: {term}")
            
            try:
                results = self.grep_client.search_code(
                    query=f"class.*{term}|function.*{term}|interface.*{term}",
                    repo_filter=repo_name,
                    use_regex=True,
                    lang_filter="TypeScript,JavaScript,Python,Java,Go"
                )
                
                # Extract unique file paths
                for result in results[:3]:  # Top 3 files per term
                    file_path = result.get('file_path')
                    if file_path and not any(f['path'] == file_path for f in files_to_fetch):
                        files_to_fetch.append({
                            'owner': owner,
                            'repo': repo,
                            'path': file_path
                        })
                        
            except Exception as e:
                print(f"    Search error: {e}")
                continue
        
        # Batch retrieve files (limit to 5 total)
        if files_to_fetch:
            print(f"    Retrieving {len(files_to_fetch[:5])} implementation files...")
            
            try:
                file_contents = self.grep_client.batch_retrieve_files(files_to_fetch[:5])
                
                implementations = []
                for content in file_contents:
                    implementations.append({
                        'file_path': content.get('path', 'unknown'),
                        'language': content.get('language', 'unknown'),
                        'size': len(content.get('content', '')),
                        'url': content.get('url', ''),
                        'snippet': content.get('content', '')[:500]  # First 500 chars
                    })
                
                return implementations
                
            except Exception as e:
                print(f"    Batch fetch error: {e}")
                return []
        
        return []
    
    def _store_pattern(self, pattern):
        """Enhanced storage with code examples."""
        
        # Store standard pattern data
        super()._store_pattern(pattern)
        
        # Store code examples if present
        if pattern.get('implementations'):
            self._store_code_examples(pattern)
    
    def _store_code_examples(self, pattern):
        """Store code examples in Neo4j."""
        
        implementations = pattern.get('implementations', [])
        if not implementations:
            return
        
        with self.neo4j.session() as session:
            for impl in implementations:
                session.run("""
                    MATCH (p:Pattern {name: $pattern_name})
                    
                    CREATE (ce:CodeExample {
                        id: $id,
                        file_path: $file_path,
                        language: $language,
                        snippet: $snippet,
                        url: $url,
                        size: $size
                    })
                    
                    CREATE (p)-[:IMPLEMENTED_IN]->(ce)
                """,
                    pattern_name=pattern['pattern_name'],
                    id=f"{pattern['source_repo']}/{impl['file_path']}",
                    file_path=impl['file_path'],
                    language=impl['language'],
                    snippet=impl['snippet'],
                    url=impl['url'],
                    size=impl['size']
                )

# Usage
if __name__ == "__main__":
    extractor = CodeEnhancedExtractor()
    
    # Test on single repo
    pattern = extractor.analyze_single_repo_enhanced(
        repo_name="microsoft/vscode",
        domain="file_management"
    )
    
    print(f"\n=== Extraction Complete ===")
    print(f"Pattern: {pattern['pattern_name']}")
    print(f"Confidence: {pattern['confidence']}")
    print(f"Code Evidence: {len(pattern.get('code_evidence', []))}")
    print(f"Implementations: {len(pattern.get('implementations', []))}")
```

**Success Criteria:**
- [ ] Can enhance low-confidence patterns
- [ ] Searches code for pattern evidence
- [ ] Retrieves implementation files
- [ ] Stores code examples in Neo4j
- [ ] Falls back gracefully if grep_app unavailable

**Time Estimate:** 8 hours (2 days)  
**Cost:** $0 (development only)

---

### Task 1.4: Validate Low-Confidence Patterns (Day 4 - Thursday)

**Objective:** Run enhanced extraction on existing low-confidence patterns

**File:** `pattern_extraction_pipeline/validate_low_confidence.py`

**Implementation:**

```python
# validate_low_confidence.py
# Validate low-confidence patterns with code analysis

from code_enhanced_extractor import CodeEnhancedExtractor
from neo4j import GraphDatabase
import os

def get_low_confidence_patterns():
    """Fetch low-confidence patterns from graph."""
    
    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        auth=(os.getenv("NEO4J_USER", "neo4j"), 
              os.getenv("NEO4J_PASSWORD", "password"))
    )
    
    with driver.session() as session:
        result = session.run("""
            MATCH (p:Pattern)
            WHERE p.confidence = 'low'
            RETURN p.name AS pattern_name,
                   p.source_repo AS repo,
                   p.stars AS stars
            ORDER BY p.stars DESC
            LIMIT 20
        """)
        
        return [dict(r) for r in result]

def update_pattern_confidence(pattern_name, new_confidence, evidence_count):
    """Update pattern confidence in graph."""
    
    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        auth=(os.getenv("NEO4J_USER", "neo4j"), 
              os.getenv("NEO4J_PASSWORD", "password"))
    )
    
    with driver.session() as session:
        session.run("""
            MATCH (p:Pattern {name: $pattern_name})
            SET p.confidence = $new_confidence,
                p.code_validated = true,
                p.code_evidence_count = $evidence_count,
                p.validation_date = datetime()
        """,
            pattern_name=pattern_name,
            new_confidence=new_confidence,
            evidence_count=evidence_count
        )

def main():
    print("=== Validating Low-Confidence Patterns ===\n")
    
    # Get patterns to validate
    patterns = get_low_confidence_patterns()
    print(f"Found {len(patterns)} low-confidence patterns\n")
    
    if not patterns:
        print("No low-confidence patterns to validate")
        return
    
    extractor = CodeEnhancedExtractor()
    
    if not extractor.code_analysis_enabled:
        print("Error: grep_app_mcp server not available")
        print("Start server with: cd grep_app_mcp && npm run start")
        return
    
    results = {
        'upgraded': 0,
        'unchanged': 0,
        'failed': 0
    }
    
    for i, pattern_info in enumerate(patterns, 1):
        print(f"\n[{i}/{len(patterns)}] Validating: {pattern_info['pattern_name']}")
        print(f"  Repo: {pattern_info['repo']}")
        print(f"  Stars: {pattern_info['stars']}")
        
        try:
            # Re-analyze with code enhancement
            pattern = extractor.analyze_single_repo_enhanced(
                repo_name=pattern_info['repo']
            )
            
            # Check if confidence improved
            if pattern.get('confidence') != 'low':
                results['upgraded'] += 1
                evidence_count = len(pattern.get('code_evidence', []))
                
                # Update in graph
                update_pattern_confidence(
                    pattern_name=pattern_info['pattern_name'],
                    new_confidence=pattern['confidence'],
                    evidence_count=evidence_count
                )
                
                print(f"  ✓ Upgraded: low → {pattern['confidence']}")
                print(f"    Evidence: {evidence_count} code examples")
            else:
                results['unchanged'] += 1
                print(f"  → No change: remains low confidence")
                
        except Exception as e:
            results['failed'] += 1
            print(f"  ✗ Error: {e}")
    
    # Summary
    print(f"\n=== Validation Complete ===")
    print(f"Upgraded: {results['upgraded']}")
    print(f"Unchanged: {results['unchanged']}")
    print(f"Failed: {results['failed']}")
    print(f"\nConfidence improvement: {results['upgraded']}/{len(patterns)} " \
          f"({results['upgraded']/len(patterns)*100:.0f}%)")
    
    # Cost estimate
    total_searches = results['upgraded'] + results['unchanged']
    estimated_cost = total_searches * 0.02  # $0.02 per repo with code analysis
    print(f"\nEstimated cost: ${estimated_cost:.2f}")

if __name__ == "__main__":
    main()
```

**Success Criteria:**
- [ ] Identifies all low-confidence patterns
- [ ] Re-analyzes with code evidence
- [ ] Updates confidence in Neo4j
- [ ] Reports improvement percentage
- [ ] Target: >50% upgrade rate

**Time Estimate:** 4 hours  
**Cost:** ~$0.40 (20 repos × $0.02)

---

### Task 1.5: Extract Implementation Examples for Top Patterns (Day 5 - Friday)

**Objective:** Add code examples to top 50 most-used patterns

**File:** `pattern_extraction_pipeline/extract_code_examples.py`

**Implementation:**

```python
# extract_code_examples.py
# Extract implementation examples for top patterns

from code_enhanced_extractor import CodeEnhancedExtractor
from neo4j import GraphDatabase
import os

def get_top_patterns(limit=50):
    """Get top patterns by stars."""
    
    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        auth=(os.getenv("NEO4J_USER", "neo4j"), 
              os.getenv("NEO4J_PASSWORD", "password"))
    )
    
    with driver.session() as session:
        result = session.run("""
            MATCH (p:Pattern)
            WHERE NOT exists((p)-[:IMPLEMENTED_IN]->(:CodeExample))
            RETURN p.name AS pattern_name,
                   p.source_repo AS repo,
                   p.stars AS stars,
                   p.confidence AS confidence
            ORDER BY p.stars DESC
            LIMIT $limit
        """, limit=limit)
        
        return [dict(r) for r in result]

def main():
    print("=== Extracting Implementation Examples ===\n")
    
    # Get top patterns without code examples
    patterns = get_top_patterns(limit=50)
    print(f"Found {len(patterns)} patterns without code examples\n")
    
    if not patterns:
        print("All patterns have code examples!")
        return
    
    extractor = CodeEnhancedExtractor()
    
    if not extractor.code_analysis_enabled:
        print("Error: grep_app_mcp server not available")
        return
    
    results = {
        'success': 0,
        'no_examples': 0,
        'failed': 0
    }
    
    for i, pattern_info in enumerate(patterns, 1):
        print(f"\n[{i}/{len(patterns)}] {pattern_info['pattern_name']}")
        print(f"  Repo: {pattern_info['repo']}")
        print(f"  Stars: {pattern_info['stars']}")
        
        try:
            # Extract implementations
            implementations = extractor._extract_implementation_files(
                repo_name=pattern_info['repo'],
                pattern_name=pattern_info['pattern_name']
            )
            
            if implementations:
                results['success'] += 1
                print(f"  ✓ Found {len(implementations)} implementation files")
                
                # Store in graph
                pattern_data = {
                    'pattern_name': pattern_info['pattern_name'],
                    'implementations': implementations,
                    'source_repo': pattern_info['repo']
                }
                extractor._store_code_examples(pattern_data)
            else:
                results['no_examples'] += 1
                print(f"  → No implementation examples found")
                
        except Exception as e:
            results['failed'] += 1
            print(f"  ✗ Error: {e}")
    
    # Summary
    print(f"\n=== Extraction Complete ===")
    print(f"Success: {results['success']}")
    print(f"No examples: {results['no_examples']}")
    print(f"Failed: {results['failed']}")
    print(f"\nCoverage: {results['success']}/{len(patterns)} " \
          f"({results['success']/len(patterns)*100:.0f}%)")
    
    # Cost estimate
    estimated_cost = len(patterns) * 0.01  # $0.01 per repo for file extraction
    print(f"\nEstimated cost: ${estimated_cost:.2f}")

if __name__ == "__main__":
    main()
```

**Success Criteria:**
- [ ] Extracts implementation files for top 50 patterns
- [ ] Stores CodeExample nodes in Neo4j
- [ ] Links patterns to code examples
- [ ] Target: >70% success rate

**Time Estimate:** 3 hours  
**Cost:** ~$0.50 (50 repos × $0.01)

---

## Medium Priority Tasks (Week 8)

### Task 2.1: Code-Level Anti-Pattern Detection (Day 1-2 - Monday-Tuesday)

**Objective:** Search for anti-pattern code across repositories

**File:** `pattern_extraction_pipeline/code_antipattern_detector.py`

**Implementation:**

```python
# code_antipattern_detector.py
# Detect anti-patterns at code level

from grep_app_client import GrepAppClient
from neo4j import GraphDatabase
import os

class CodeAntiPatternDetector:
    """Detect anti-patterns through code search."""
    
    def __init__(self):
        self.grep_client = GrepAppClient()
        self.neo4j = GraphDatabase.driver(
            os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            auth=(os.getenv("NEO4J_USER", "neo4j"), 
                  os.getenv("NEO4J_PASSWORD", "password"))
        )
        
        # Known anti-pattern code signatures
        self.anti_pattern_signatures = {
            'database_file_sync': [
                'db.sync.*filesystem',
                'database.update.*file.read',
                'setInterval.*syncFiles'
            ],
            'blocking_io': [
                'fs.readFileSync',
                'fs.writeFileSync',
                'readSync(',
                'writeSync('
            ],
            'sql_injection': [
                'execute.*\\+.*request',
                'query.*\\+.*input',
                'sql.*\\+.*params'
            ],
            'memory_leak': [
                'setInterval.*=>',
                'addEventListener.*=>.*global',
                'new.*every.*seconds'
            ]
        }
    
    def detect_anti_patterns_in_repo(self, repo_name):
        """Search for anti-patterns in specific repository."""
        
        print(f"\nSearching for anti-patterns in: {repo_name}")
        
        found_anti_patterns = []
        
        for anti_pattern, signatures in self.anti_pattern_signatures.items():
            print(f"\n  Checking: {anti_pattern}")
            
            for signature in signatures:
                print(f"    Pattern: {signature}")
                
                try:
                    results = self.grep_client.search_code(
                        query=signature,
                        repo_filter=repo_name,
                        use_regex=True,
                        numbered_output=True
                    )
                    
                    if results:
                        print(f"      ⚠ Found {len(results)} instances")
                        
                        for result in results[:3]:  # Top 3 examples
                            found_anti_patterns.append({
                                'anti_pattern': anti_pattern,
                                'signature': signature,
                                'file_path': result.get('file_path'),
                                'line': result.get('line'),
                                'snippet': result.get('snippet', '')[:200],
                                'repo': repo_name
                            })
                    
                except Exception as e:
                    print(f"      Error: {e}")
        
        return found_anti_patterns
    
    def search_anti_patterns_cross_repo(self, anti_pattern_name, limit=100):
        """Search for anti-pattern across all repos."""
        
        print(f"\n=== Cross-Repo Anti-Pattern Search ===")
        print(f"Anti-Pattern: {anti_pattern_name}")
        print(f"Limit: {limit} repositories\n")
        
        signatures = self.anti_pattern_signatures.get(anti_pattern_name, [])
        if not signatures:
            print(f"Unknown anti-pattern: {anti_pattern_name}")
            return []
        
        all_results = []
        
        for signature in signatures:
            print(f"Searching: {signature}")
            
            try:
                results = self.grep_client.search_code(
                    query=signature,
                    use_regex=True,
                    lang_filter="JavaScript,TypeScript,Python,Java,Go"
                )
                
                print(f"  Found in {len(results)} locations")
                all_results.extend(results[:limit])
                
            except Exception as e:
                print(f"  Error: {e}")
        
        return all_results
    
    def store_anti_pattern_evidence(self, evidence):
        """Store anti-pattern evidence in Neo4j."""
        
        with self.neo4j.session() as session:
            for item in evidence:
                session.run("""
                    MERGE (ap:AntiPattern {name: $anti_pattern})
                    ON CREATE SET
                        ap.frequency = 1,
                        ap.evidence = [$url]
                    ON MATCH SET
                        ap.frequency = ap.frequency + 1,
                        ap.evidence = CASE 
                            WHEN size(ap.evidence) < 100 
                            THEN ap.evidence + $url 
                            ELSE ap.evidence 
                        END
                    
                    CREATE (ce:CodeExample {
                        id: $id,
                        file_path: $file_path,
                        snippet: $snippet,
                        line: $line,
                        repo: $repo,
                        type: 'anti_pattern'
                    })
                    
                    CREATE (ap)-[:FOUND_IN]->(ce)
                """,
                    anti_pattern=item['anti_pattern'],
                    url=f"https://github.com/{item['repo']}/blob/main/{item['file_path']}#L{item['line']}",
                    id=f"{item['repo']}/{item['file_path']}:{item['line']}",
                    file_path=item['file_path'],
                    snippet=item['snippet'],
                    line=item['line'],
                    repo=item['repo']
                )

# Usage
if __name__ == "__main__":
    detector = CodeAntiPatternDetector()
    
    print("=== Anti-Pattern Detection ===")
    print("\nOptions:")
    print("1. Detect in specific repository")
    print("2. Cross-repo search")
    
    choice = input("\nChoice (1-2): ").strip()
    
    if choice == "1":
        repo = input("Repository (e.g., microsoft/vscode): ").strip()
        evidence = detector.detect_anti_patterns_in_repo(repo)
        
        if evidence:
            print(f"\n✓ Found {len(evidence)} anti-pattern instances")
            detector.store_anti_pattern_evidence(evidence)
        else:
            print("\n✓ No anti-patterns detected")
    
    elif choice == "2":
        anti_pattern = input("Anti-pattern name (e.g., database_file_sync): ").strip()
        results = detector.search_anti_patterns_cross_repo(anti_pattern, limit=50)
        
        print(f"\n✓ Found across {len(set(r.get('repo') for r in results))} repos")
```

**Success Criteria:**
- [ ] Searches for known anti-pattern signatures
- [ ] Finds code examples across repos
- [ ] Stores evidence in Neo4j
- [ ] Links to AntiPattern nodes

**Time Estimate:** 8 hours (2 days)  
**Cost:** $0 (free code search)

---

### Task 2.2: Cross-Repository Pattern Comparison (Day 3 - Wednesday)

**Objective:** Compare how different repos implement the same pattern

**File:** `pattern_extraction_pipeline/pattern_comparator.py`

**Implementation:**

```python
# pattern_comparator.py
# Compare pattern implementations across repositories

from grep_app_client import GrepAppClient
from neo4j import GraphDatabase
import os
from collections import Counter

class PatternComparator:
    """Compare pattern implementations across repos."""
    
    def __init__(self):
        self.grep_client = GrepAppClient()
        self.neo4j = GraphDatabase.driver(
            os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            auth=(os.getenv("NEO4J_USER", "neo4j"), 
                  os.getenv("NEO4J_PASSWORD", "password"))
        )
    
    def compare_pattern_implementations(self, pattern_name):
        """Compare implementations of a pattern across repos."""
        
        print(f"\n=== Comparing Implementations: {pattern_name} ===\n")
        
        # Get repos that use this pattern
        repos = self._get_repos_with_pattern(pattern_name)
        print(f"Found in {len(repos)} repositories")
        
        if len(repos) < 2:
            print("Need at least 2 repos for comparison")
            return None
        
        # Search for implementation in each repo
        comparison = {
            'pattern': pattern_name,
            'repos': [],
            'common_technologies': Counter(),
            'common_patterns': Counter()
        }
        
        for repo in repos[:10]:  # Compare top 10
            print(f"\nAnalyzing: {repo}")
            
            implementation = self._analyze_implementation(repo, pattern_name)
            comparison['repos'].append(implementation)
            
            # Track technologies
            for tech in implementation.get('technologies', []):
                comparison['common_technologies'][tech] += 1
            
            # Track code patterns
            for code_pattern in implementation.get('code_patterns', []):
                comparison['common_patterns'][code_pattern] += 1
        
        # Identify consensus
        comparison['consensus_technologies'] = [
            tech for tech, count in comparison['common_technologies'].most_common(5)
            if count >= len(repos) * 0.5  # Used by >50% of repos
        ]
        
        comparison['consensus_patterns'] = [
            pattern for pattern, count in comparison['common_patterns'].most_common(5)
            if count >= len(repos) * 0.5
        ]
        
        self._print_comparison(comparison)
        return comparison
    
    def _get_repos_with_pattern(self, pattern_name):
        """Get repositories using this pattern."""
        
        with self.neo4j.session() as session:
            result = session.run("""
                MATCH (p:Pattern {name: $pattern_name})
                RETURN p.source_repo AS repo
                
                UNION
                
                MATCH (p:Pattern {name: $pattern_name})
                MATCH (ce:CodeExample)<-[:IMPLEMENTED_IN]-(p)
                RETURN DISTINCT ce.repo AS repo
            """, pattern_name=pattern_name)
            
            return [r['repo'] for r in result]
    
    def _analyze_implementation(self, repo, pattern_name):
        """Analyze how a repo implements the pattern."""
        
        # Search for key implementation files
        results = self.grep_client.search_code(
            query=f"class.*{pattern_name}|function.*{pattern_name}",
            repo_filter=repo,
            use_regex=True
        )
        
        # Extract technologies from code
        technologies = set()
        code_patterns = set()
        
        for result in results[:5]:
            snippet = result.get('snippet', '')
            
            # Detect technologies
            if 'import' in snippet or 'require' in snippet:
                # Extract import statements
                for line in snippet.split('\n'):
                    if 'import' in line or 'require' in line:
                        # Parse technology name
                        # (simplified - could be more sophisticated)
                        for word in line.split():
                            if word.startswith('"') or word.startswith("'"):
                                tech = word.strip('"\'')
                                if '/' not in tech:  # Root package
                                    technologies.add(tech)
            
            # Detect code patterns
            if 'async' in snippet:
                code_patterns.add('async/await')
            if 'Promise' in snippet:
                code_patterns.add('promises')
            if 'EventEmitter' in snippet:
                code_patterns.add('event-driven')
        
        return {
            'repo': repo,
            'technologies': list(technologies),
            'code_patterns': list(code_patterns),
            'file_count': len(results)
        }
    
    def _print_comparison(self, comparison):
        """Print comparison results."""
        
        print(f"\n=== Comparison Results ===")
        print(f"\nPattern: {comparison['pattern']}")
        print(f"Analyzed: {len(comparison['repos'])} repositories")
        
        print(f"\nConsensus Technologies (used by >50%):")
        for tech in comparison['consensus_technologies']:
            count = comparison['common_technologies'][tech]
            percentage = (count / len(comparison['repos'])) * 100
            print(f"  • {tech} ({percentage:.0f}%)")
        
        print(f"\nConsensus Patterns (used by >50%):")
        for pattern in comparison['consensus_patterns']:
            count = comparison['common_patterns'][pattern]
            percentage = (count / len(comparison['repos'])) * 100
            print(f"  • {pattern} ({percentage:.0f}%)")
        
        print(f"\nRecommendation:")
        if comparison['consensus_technologies']:
            print(f"  Use: {', '.join(comparison['consensus_technologies'][:3])}")
        else:
            print(f"  No strong consensus - multiple valid approaches")

# Usage
if __name__ == "__main__":
    comparator = PatternComparator()
    
    pattern = input("Pattern to compare (e.g., filesystem_browser): ").strip()
    comparison = comparator.compare_pattern_implementations(pattern)
```

**Success Criteria:**
- [ ] Compares implementations across repos
- [ ] Identifies consensus technologies
- [ ] Finds common code patterns
- [ ] Provides recommendations

**Time Estimate:** 4 hours  
**Cost:** $0 (free code search)

---

### Task 2.3: Enhanced Query Interface with Code Examples (Day 4-5 - Thursday-Friday)

**Objective:** Update query interface to return code examples

**File:** Update `pattern_extraction_pipeline/query_patterns.py`

**Add these methods:**

```python
def recommend_pattern_with_examples(self, requirements):
    """Enhanced recommendation with code examples."""
    
    with self.neo4j.session() as session:
        result = session.run("""
            MATCH (r:Requirement)
            WHERE r.type = $req_type
              AND r.domain = $req_domain
            MATCH (r)-[:SOLVED_BY]->(p:Pattern)
            MATCH (p)-[:REQUIRES]->(c:Constraint)
            OPTIONAL MATCH (p)-[:USES]->(t:Technology)
            OPTIONAL MATCH (p)-[:IMPLEMENTED_IN]->(ce:CodeExample)
            
            WITH p, 
                 collect(DISTINCT c.rule) AS constraints,
                 collect(DISTINCT t.name) AS technologies,
                 collect(DISTINCT {
                     file: ce.file_path,
                     language: ce.language,
                     snippet: ce.snippet,
                     url: ce.url
                 }) AS code_examples
            
            RETURN 
                p.name AS pattern,
                p.confidence AS confidence,
                p.source_repo AS source,
                p.stars AS stars,
                constraints,
                technologies,
                code_examples
            
            ORDER BY p.stars DESC
            LIMIT 5
        """,
            req_type=requirements['type'],
            req_domain=requirements['domain']
        )
        
        return [dict(record) for record in result]

def get_anti_patterns_with_code(self, requirements):
    """Get anti-patterns with code examples."""
    
    with self.neo4j.session() as session:
        result = session.run("""
            MATCH (r:Requirement)
            WHERE r.type = $req_type
              AND r.domain = $req_domain
            MATCH (r)-[:AVOID]->(ap:AntiPattern)
            OPTIONAL MATCH (ap)-[:FOUND_IN]->(ce:CodeExample)
            
            WITH ap,
                 collect({
                     file: ce.file_path,
                     snippet: ce.snippet,
                     line: ce.line,
                     repo: ce.repo
                 }) AS examples
            
            RETURN 
                ap.name AS anti_pattern,
                ap.why_fails AS reason,
                ap.frequency AS frequency,
                examples
            
            ORDER BY ap.frequency DESC
            LIMIT 5
        """,
            req_type=requirements['type'],
            req_domain=requirements['domain']
        )
        
        return [dict(record) for record in result]
```

**Success Criteria:**
- [ ] Returns patterns with code examples
- [ ] Shows anti-patterns with code evidence
- [ ] Formats examples for display
- [ ] Maintains backward compatibility

**Time Estimate:** 6 hours  
**Cost:** $0

---

## Testing & Validation

### Integration Tests

**File:** `pattern_extraction_pipeline/test_grep_integration.py`

```python
# test_grep_integration.py
# Integration tests for grep_app_mcp

import pytest
from grep_app_client import GrepAppClient
from code_enhanced_extractor import CodeEnhancedExtractor
from code_antipattern_detector import CodeAntiPatternDetector

def test_grep_client():
    """Test grep_app_mcp client."""
    client = GrepAppClient()
    
    # Health check
    assert client.health_check(), "Server not available"
    
    # Search
    results = client.search_code("fs.watch", lang_filter="JavaScript")
    assert len(results) > 0, "No search results"
    
    # File retrieval
    content = client.github_file("microsoft", "vscode", "README.md")
    assert content is not None, "File not retrieved"

def test_enhanced_extraction():
    """Test enhanced pattern extraction."""
    extractor = CodeEnhancedExtractor()
    
    pattern = extractor.analyze_single_repo_enhanced("microsoft/vscode")
    
    assert pattern['pattern_name'], "No pattern name"
    assert pattern['confidence'] in ['low', 'medium', 'high'], "Invalid confidence"
    
    if extractor.code_analysis_enabled:
        assert 'code_evidence' in pattern or 'implementations' in pattern, \
            "No code analysis performed"

def test_anti_pattern_detection():
    """Test anti-pattern detection."""
    detector = CodeAntiPatternDetector()
    
    evidence = detector.detect_anti_patterns_in_repo("test/repo")
    
    # Should complete without error
    assert isinstance(evidence, list), "Invalid result type"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

**Run tests:**
```powershell
pytest test_grep_integration.py -v
```

---

## Success Metrics

### Week 7 (High Priority) Targets:
- [ ] grep_app_mcp server running reliably
- [ ] Python client working with all core functions
- [ ] >50% of low-confidence patterns upgraded
- [ ] Code examples extracted for >70% of top 50 patterns
- [ ] <$1 total cost for validation

### Week 8 (Medium Priority) Targets:
- [ ] Anti-pattern signatures defined for 5+ patterns
- [ ] Cross-repo comparison working for common patterns
- [ ] Query interface enhanced with code examples
- [ ] All tests passing
- [ ] <$0.50 cost for anti-pattern detection

### Overall Success:
- [ ] Pattern confidence increased by >30% on average
- [ ] Code examples available for top 100 patterns
- [ ] Anti-pattern database has >100 code examples
- [ ] Integration complete and documented
- [ ] Total cost: <$2

---

## Rollout Schedule

| Day | Task | Hours | Cost |
|-----|------|-------|------|
| **Week 7** | | | |
| Mon | 1.1 Setup grep_app_mcp | 2 | $0 |
| Mon | 1.2 Create Python client | 3 | $0 |
| Tue-Wed | 1.3 Enhanced extractor | 8 | $0 |
| Thu | 1.4 Validate low-confidence | 4 | $0.40 |
| Fri | 1.5 Extract examples | 3 | $0.50 |
| **Week 8** | | | |
| Mon-Tue | 2.1 Anti-pattern detection | 8 | $0 |
| Wed | 2.2 Pattern comparison | 4 | $0 |
| Thu-Fri | 2.3 Enhanced queries | 6 | $0 |
| **Total** | | **38 hours** | **$0.90** |

---

## Troubleshooting

### grep_app_mcp server won't start
```powershell
cd C:\Users\Fab2\Desktop\AI\Specs\grep_app_mcp

# Check Node version
node --version  # Should be 18+

# Reinstall dependencies
Remove-Item node_modules -Recurse -Force
npm install

# Try dev mode
npm run dev
```

### Python client connection fails
```python
# Check server is running
curl http://localhost:8603/sse

# Try different port
client = GrepAppClient(base_url="http://localhost:8603")

# Check firewall
# Windows: Allow Node.js through firewall
```

### Search returns no results
```python
# Try simpler query first
results = client.search_code("function", lang_filter="JavaScript")

# Check repo filter syntax
results = client.search_code("test", repo_filter="microsoft/vscode")

# Verify grep.app API is working
# Visit: https://grep.app
```

### Neo4j connection issues
```powershell
# Check Neo4j is running
docker ps | Select-String "neo4j"

# Restart if needed
docker restart spec-engine-graph

# Test connection
python -c "from neo4j import GraphDatabase; print('OK')"
```

---

## Next Steps After Completion

1. **Week 9:** Integrate with SPEC_Engine Commander
2. **Week 10:** Add code examples to pre-flight validation
3. **Week 11:** Build code example search UI
4. **Week 12:** Document and deploy

---

## Appendix: File Checklist

### New Files to Create:
- [ ] `grep_app_client.py` - Python client
- [ ] `code_enhanced_extractor.py` - Enhanced extractor
- [ ] `validate_low_confidence.py` - Validation script
- [ ] `extract_code_examples.py` - Example extractor
- [ ] `code_antipattern_detector.py` - Anti-pattern detector
- [ ] `pattern_comparator.py` - Pattern comparison
- [ ] `test_grep_integration.py` - Integration tests

### Files to Update:
- [ ] `query_patterns.py` - Add code example queries
- [ ] `requirements.txt` - Add requests library
- [ ] `.env.template` - Add grep_app_mcp settings
- [ ] `README.md` - Document grep_app integration

### External Dependencies:
- [ ] grep_app_mcp server (separate repo)
- [ ] Node.js 18+ (for grep_app_mcp)
- [ ] requests library (Python)

---

**Ready to begin? Start with Task 1.1!**
