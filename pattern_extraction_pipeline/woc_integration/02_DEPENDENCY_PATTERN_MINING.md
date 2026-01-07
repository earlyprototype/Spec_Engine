# WoC Integration: Dependency Pattern Mining

**Priority:** HIGH  
**Impact:** Understand tech stack patterns across GraphRAG ecosystem  
**Complexity:** Medium-High

---

## Overview

World of Code has **pre-extracted** all imports and dependencies from billions of source files. This enables immediate analysis of technology stack patterns without parsing any code yourself.

---

## What WoC Provides

### Pre-Extracted Dependencies

**WoC Files:** `c2PtAbflPkg` (128 files, split by commit SHA)

**Format:**
```
commit;deforked_repo;timestamp;aliased_author;blob;filename;language;module1;module2;...
```

**Real Example:**
```
000005efe300482514d70d44c5fa922b34ff79a5;Rayhane-mamah_Tacotron-2;1557284915;qq443452099 <47710489+qq443452099@users.noreply.github.com>;05604b3f...;tacotron/synthesizer.py;PY;tensorflow;numpy;librosa.effects;wave;datetime.datetime;io
```

**Languages Covered:**
- Python (PY)
- JavaScript/TypeScript (JS)
- Java
- C/C++
- Ruby
- Go
- Rust
- And many more

---

## Use Cases for Your Pipeline

### 1. Tech Stack Pattern Discovery

**Question:** "What's the typical tech stack for GraphRAG systems?"

**WoC Query:**
```bash
# Extract all dependencies from GraphRAG repos
for repo in HKUDS_LightRAG memvid_memvid topoteretes_cognee; do
    zcat /da?_data/basemaps/gz/c2PtAbflPkgFullU*.s | grep "$repo" | cut -d';' -f8- | tr ';' '\n' | sort | uniq -c
done
```

**Expected Output:**
```
  25 langchain
  18 neo4j
  15 openai
  12 faiss
  10 numpy
   8 anthropic
   5 redis
```

**Insight:** "GraphRAG systems typically use: LangChain (orchestration), Neo4j (graph), OpenAI/Anthropic (LLM), FAISS (vector search)"

---

### 2. Framework Adoption Timeline

**Question:** "When did GraphRAG repos start adopting Neo4j?"

**WoC Query:**
```bash
# Find first Neo4j imports in your analyzed repos
zcat /da?_data/basemaps/gz/c2PtAbflPkgFullU*.s | \
  grep -E "(HKUDS_LightRAG|memvid_memvid|topoteretes_cognee)" | \
  grep -i "neo4j" | \
  cut -d';' -f2,3 | \  # repo, timestamp
  sort -t';' -k2 -n | \  # sort by timestamp
  awk -F';' '{print strftime("%Y-%m-%d", $2), $1}' | \
  head -20
```

**Expected Output:**
```
2023-05-12 topoteretes_cognee
2023-08-20 HKUDS_LightRAG
2024-01-15 memvid_memvid
```

**Insight:** "Neo4j adoption in GraphRAG space spiked in mid-2023"

---

### 3. Dependency Correlation with Quality

**Question:** "Do high-quality patterns use specific dependencies?"

**Analysis:**
```python
from collections import Counter

def analyze_dependency_quality_correlation(patterns):
    """
    Correlate dependencies with pattern quality scores
    """
    high_quality = []  # quality > 0.85
    low_quality = []   # quality < 0.70
    
    for pattern in patterns:
        deps = get_woc_dependencies(pattern['source_repo'])
        
        if pattern['quality_score'] > 0.85:
            high_quality.extend(deps)
        elif pattern['quality_score'] < 0.70:
            low_quality.extend(deps)
    
    high_deps = Counter(high_quality).most_common(10)
    low_deps = Counter(low_quality).most_common(10)
    
    return {
        'high_quality_deps': high_deps,
        'low_quality_deps': low_deps
    }
```

**Potential Insight:**
- High-quality repos use: LangChain, Neo4j, FastAPI
- Low-quality repos use: outdated frameworks, fewer modern tools

---

### 4. Dependency Evolution Tracking

**Question:** "How did a repository's dependencies change over time?"

**Implementation:**
```python
def track_dependency_evolution(repo_name):
    """
    Track how dependencies changed across commits
    """
    commits = get_architectural_commits_from_woc(repo_name)
    
    evolution = []
    for commit in sorted(commits, key=lambda x: x['time']):
        deps = get_dependencies_for_commit(commit['sha'])
        evolution.append({
            'timestamp': commit['time'],
            'date': datetime.fromtimestamp(commit['time']),
            'dependencies': deps,
            'deps_added': deps - previous_deps if previous_deps else deps,
            'deps_removed': previous_deps - deps if previous_deps else set()
        })
        previous_deps = deps
    
    return evolution

# Example
evo = track_dependency_evolution('HKUDS_LightRAG')
for milestone in evo:
    if milestone['deps_added']:
        print(f"{milestone['date']}: Added {milestone['deps_added']}")
```

**Output:**
```
2024-03-15: Added {'langchain', 'neo4j-driver'}
2024-05-10: Added {'faiss-cpu', 'sentence-transformers'}
2024-07-20: Added {'anthropic'}
2024-09-01: Removed {'openai'} (switched to Anthropic)
```

---

### 5. Common Stack Patterns

**Question:** "What dependency combinations are common in GraphRAG repos?"

**Analysis:**
```python
from itertools import combinations
from collections import Counter

def find_common_stacks(repos):
    """
    Identify frequently co-occurring dependencies
    """
    stack_patterns = []
    
    for repo in repos:
        deps = get_woc_dependencies(repo)
        
        # Find all 3-dependency combinations
        for combo in combinations(deps, 3):
            stack_patterns.append(frozenset(combo))
    
    # Count frequency
    common_stacks = Counter(stack_patterns).most_common(10)
    
    return common_stacks

# Result
common = find_common_stacks(graphrag_repos)
# Output:
# 1. (LangChain, Neo4j, OpenAI) - 45 repos
# 2. (LangChain, FAISS, Anthropic) - 38 repos
# 3. (LlamaIndex, Neo4j, OpenAI) - 32 repos
```

---

## Integration with Existing Pipeline

### Enhance Pattern Storage

**Current Pattern Node:**
```cypher
(p:Pattern {
  name: "GraphRAG Implementation",
  source_repo: "https://github.com/HKUDS/LightRAG",
  quality_score: 0.92,
  extracted_at: datetime("2026-01-06")
})
```

**Enhanced with WoC Dependency Data:**
```cypher
(p:Pattern {
  name: "GraphRAG Implementation",
  source_repo: "https://github.com/HKUDS/LightRAG",
  quality_score: 0.92,
  extracted_at: datetime("2026-01-06"),
  // NEW: Dependency data from WoC
  core_dependencies: ['langchain', 'neo4j-driver', 'openai', 'faiss'],
  dependency_count: 15,
  first_neo4j_commit: datetime("2024-05-12"),
  first_langchain_commit: datetime("2024-03-15")
})

// Relationships to Technology nodes
(p)-[:USES {since: datetime("2024-03-15")}]->(t:Technology {name: "LangChain"})
(p)-[:USES {since: datetime("2024-05-12")}]->(t:Technology {name: "Neo4j"})
```

---

## Implementation Script

### Complete Dependency Extraction Script

**File:** `extract_woc_dependencies.py`

```python
#!/usr/bin/env python3
"""
Extract dependency data from World of Code for analyzed repositories
"""

import subprocess
from collections import defaultdict
from datetime import datetime

def get_repo_dependencies_from_woc(repo_name, woc_data_path="/da?_data/basemaps/gz/"):
    """
    Query WoC for all dependencies used by a repository
    
    Args:
        repo_name: Repository name (e.g., "HKUDS_LightRAG")
        woc_data_path: Path to WoC data files
    
    Returns:
        Dict with dependency timeline
    """
    dependencies = defaultdict(list)
    
    # Query all c2PtAbflPkg files for this repo
    cmd = f"zcat {woc_data_path}c2PtAbflPkgFullU*.s | grep '{repo_name}'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    for line in result.stdout.splitlines():
        parts = line.split(';')
        if len(parts) < 8:
            continue
        
        commit = parts[0]
        timestamp = int(parts[2])
        language = parts[6]
        deps = parts[7:]  # All dependencies
        
        for dep in deps:
            if dep:  # Skip empty
                dependencies[dep].append({
                    'timestamp': timestamp,
                    'commit': commit,
                    'language': language
                })
    
    # Sort each dependency by first appearance
    for dep in dependencies:
        dependencies[dep].sort(key=lambda x: x['timestamp'])
    
    return dict(dependencies)


def extract_core_stack(dependencies, min_occurrences=3):
    """
    Identify core dependencies (used consistently)
    
    Args:
        dependencies: Output from get_repo_dependencies_from_woc()
        min_occurrences: Minimum commits using dependency
    
    Returns:
        List of core dependencies with first appearance
    """
    core_stack = []
    
    for dep, commits in dependencies.items():
        if len(commits) >= min_occurrences:
            first_use = commits[0]
            core_stack.append({
                'name': dep,
                'first_used': datetime.fromtimestamp(first_use['timestamp']),
                'commit_count': len(commits),
                'language': first_use['language']
            })
    
    return sorted(core_stack, key=lambda x: x['first_used'])


def store_dependencies_in_neo4j(pattern, dependencies):
    """
    Store dependency data in Neo4j
    """
    from neo4j import GraphDatabase
    
    driver = GraphDatabase.driver(
        "bolt://localhost:7688",
        auth=("neo4j", "password")
    )
    
    with driver.session() as session:
        # Create Technology nodes and relationships
        for dep in dependencies:
            session.run("""
                MATCH (p:Pattern {source_repo: $repo})
                MERGE (t:Technology {name: $dep_name})
                MERGE (p)-[r:USES]->(t)
                ON CREATE SET
                    r.since = datetime($first_used),
                    r.commit_count = $count
                ON MATCH SET
                    r.commit_count = $count
            """, 
            repo=pattern['source_repo'],
            dep_name=dep['name'],
            first_used=dep['first_used'].isoformat(),
            count=dep['commit_count']
            )
    
    driver.close()


# Main execution
if __name__ == "__main__":
    # Example: Process one repository
    repo_name = "HKUDS_LightRAG"
    
    print(f"Extracting dependencies for {repo_name}...")
    deps = get_repo_dependencies_from_woc(repo_name)
    
    print(f"Found {len(deps)} unique dependencies")
    
    core = extract_core_stack(deps, min_occurrences=3)
    print(f"\nCore stack ({len(core)} dependencies):")
    for dep in core:
        print(f"  - {dep['name']}: first used {dep['first_used'].strftime('%Y-%m-%d')} ({dep['commit_count']} commits)")
    
    # Store in Neo4j
    pattern = {'source_repo': f"https://github.com/{repo_name.replace('_', '/')}"}
    store_dependencies_in_neo4j(pattern, core)
    print("\nStored in Neo4j!")
```

---

## Query Examples After Integration

### 1. Find Patterns by Technology

```cypher
// All patterns using Neo4j
MATCH (p:Pattern)-[:USES]->(t:Technology {name: "neo4j"})
RETURN p.name, p.quality_score, p.source_repo
ORDER BY p.quality_score DESC
```

### 2. Technology Adoption Timeline

```cypher
// When did repos adopt LangChain?
MATCH (p:Pattern)-[u:USES]->(t:Technology {name: "langchain"})
RETURN p.name, u.since
ORDER BY u.since ASC
```

### 3. Common Tech Stacks

```cypher
// Find repos using both Neo4j and LangChain
MATCH (p:Pattern)-[:USES]->(t1:Technology {name: "neo4j"})
MATCH (p)-[:USES]->(t2:Technology {name: "langchain"})
RETURN p.name, p.quality_score
ORDER BY p.quality_score DESC
```

### 4. Technology Popularity

```cypher
// Most popular technologies in GraphRAG space
MATCH (t:Technology)<-[:USES]-(p:Pattern)
WITH t, count(p) as usage_count
RETURN t.name, usage_count
ORDER BY usage_count DESC
LIMIT 10
```

---

## Expected Insights

### Stack Patterns You'll Discover

**1. The "Full GraphRAG Stack":**
- LLM Provider (OpenAI/Anthropic)
- LLM Framework (LangChain/LlamaIndex)
- Graph Database (Neo4j/FalkorDB)
- Vector Store (FAISS/Pinecone/Weaviate)
- Embeddings (sentence-transformers)

**2. The "Lightweight RAG Stack":**
- LLM only (OpenAI)
- Simple vector store (ChromaDB)
- No graph database

**3. The "Research Stack":**
- PyTorch/TensorFlow
- NetworkX (graph algorithms)
- Custom implementations
- Academic libraries

### Dependency Trends

**Likely Findings:**
- Neo4j adoption increased 2023-2024
- LangChain dominates orchestration
- OpenAI → Anthropic migration trend
- FAISS common for vector search

---

## Data Volume Considerations

### Challenge

128 files × ~500MB each = ~64GB compressed data

Processing all files takes hours. Need smart filtering.

### Optimization Strategies

**1. Filter by Repository First**
```bash
# Create filtered dataset (once)
for i in {0..127}; do
    zcat /da?_data/basemaps/gz/c2PtAbflPkgFullU$i.s | \
      grep -f your_repos.txt >> filtered_deps.txt
done
```

**2. Process in Parallel**
```python
from multiprocessing import Pool

def process_file(i):
    return extract_deps_from_file(i)

with Pool(10) as pool:
    results = pool.map(process_file, range(128))
```

**3. Use Incremental Processing**
```python
# Process new repos only
new_repos = get_repos_since_last_run()
for repo in new_repos:
    extract_and_store_dependencies(repo)
```

---

## Integration Timeline

**Day 1:** Request WoC access, setup oscar.py  
**Days 2-3:** Test query for 1-5 repos, validate data  
**Days 4-5:** Write extraction script for all 228 repos  
**Days 6-8:** Process all repos, extract dependencies  
**Day 9:** Store in Neo4j with relationships  
**Day 10:** Build query interface, validate insights

**Total:** 10 days

---

## Success Criteria

**Phase 1 Success:**
- ✅ Can extract dependencies for one repo from WoC
- ✅ Dependencies match actual repo (spot check)
- ✅ Can identify first use timestamps
- ✅ Processing time reasonable (<10 min per repo)

**Phase 2 Success:**
- ✅ All 228 repos processed
- ✅ Dependencies stored in Neo4j
- ✅ Technology nodes created
- ✅ Queries working (find patterns by tech)
- ✅ Insights are actionable

---

## Alternative: GitHub API Fallback

If WoC seems too complex:

**Use GitHub GraphQL to get dependency files:**
```graphql
query {
  repository(owner: "HKUDS", name: "LightRAG") {
    object(expression: "HEAD:requirements.txt") {
      ... on Blob {
        text
      }
    }
  }
}
```

**Pros:**
- Simpler (familiar API)
- No WoC access needed

**Cons:**
- Manual parsing (requirements.txt, package.json, etc.)
- Current state only (no history)
- Rate limits
- Missing transitive dependencies

---

## Value Proposition

### Why This Matters

**Current State:**
- You know repos use Neo4j (you see it in README)
- You don't know WHEN they adopted it
- You don't know WHAT ELSE they use
- You don't know COMMON PATTERNS

**With WoC Dependency Data:**
- Complete tech stack for every repo
- Adoption timeline for each dependency
- Common stack patterns identified
- Tech correlation with quality

**Research Value:**
- Publishable insights on tech stack trends
- GraphRAG ecosystem tech analysis
- Framework adoption patterns
- Quality predictors (does Neo4j + LangChain = higher quality?)

---

## Recommendation

**High value but significant effort.** Consider this AFTER:
1. ✅ Duplicate detection complete
2. ✅ Current extraction tested
3. ⏳ Commit history integration (Phase 1 of WoC)

**Rationale:** Commit history is simpler and higher immediate value. Get that working first, then add dependency mining.

---

## Bottom Line

WoC's pre-extracted dependency data is a goldmine for understanding tech stack patterns in the GraphRAG ecosystem. It answers questions impossible to answer from current-state code analysis alone.

**Value:** Very High  
**Effort:** Medium-High (10 days)  
**Timing:** Do AFTER commit history integration proves valuable
