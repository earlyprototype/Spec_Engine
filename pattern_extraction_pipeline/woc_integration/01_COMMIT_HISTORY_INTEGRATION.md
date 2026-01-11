# WoC Integration: Commit History for Pattern Evolution

**Priority:** HIGHEST  
**Impact:** Track how architectural patterns evolved over time  
**Complexity:** Medium

---

## Overview

Use World of Code's complete commit history (3.1B commits) to understand when and how architectural patterns emerged in your analyzed repositories.

---

## What You Get

### Historical Depth

For each of your 228+ analyzed repositories:
- Complete commit history since repo creation
- Every file change with timestamp
- Author information for each change
- Commit messages with context

### Pattern Evolution Insights

**Questions You Can Answer:**
1. When did this pattern first appear in the codebase?
2. How has the pattern evolved over time?
3. What triggered pattern adoption (new framework? refactor?)
4. How quickly did pattern mature?
5. What was the architecture before this pattern?

---

## WoC Data Sources

### Primary Maps

**1. Project to Commits (`p2c`)**
```
Format: project;commit1;commit2;...;commitN
Example: HKUDS_LightRAG;abc123...;def456...;...
```

**2. Commit to Data (`c2dat`)**
```
Format: commit;tree;parent;time;timezone;author;committer;message
Example: abc123;tree_sha;parent_sha;1640000000;+0000;Author <email>;...;Added GraphRAG implementation
```

**3. Commit to Files (`c2f`)**
```
Format: commit;file1;file2;...;fileN
Example: abc123;src/graph/index.ts;src/rag/query.py;README.md
```

**4. Blob Content (`showCnt blob`)**
```
Get actual file content for any blob SHA
```

---

## Implementation Plan

### Step 1: Query Commit History

**Goal:** Get all commits for an analyzed repository

**Using oscar.py:**
```python
from oscar import Project, Commit

# Get project commits
repo_name = "HKUDS_LightRAG"
project = Project(repo_name)

# All commits
commits = project.commit_shas

print(f"Total commits: {len(commits)}")
```

**Using Shell API:**
```bash
# Query p2c map
echo "HKUDS_LightRAG" | ~/lookup/getValues p2c
```

---

### Step 2: Filter Architectural Commits

**Goal:** Find commits that touched architectural files

**Architectural Files (Examples):**
- README.md, ARCHITECTURE.md
- /src/graph/, /src/rag/, /lib/
- package.json, requirements.txt, setup.py
- docker-compose.yml, Dockerfile
- Configuration files

**Using oscar.py:**
```python
architectural_commits = []

for commit_sha in commits:
    commit = Commit(commit_sha)
    files = commit.changed_file_names
    
    # Filter for architectural files
    arch_files = [f for f in files if (
        'graph' in f.lower() or
        'rag' in f.lower() or
        f.endswith('README.md') or
        f.endswith('package.json') or
        f.endswith('requirements.txt') or
        '/src/' in f or
        '/lib/' in f
    )]
    
    if arch_files:
        timestamp, author = commit.attributes[0], commit.attributes[3]
        architectural_commits.append({
            'sha': commit_sha,
            'time': timestamp,
            'author': author,
            'files': arch_files
        })

# Sort by timestamp
architectural_commits.sort(key=lambda x: x['time'])
```

---

### Step 3: Build Pattern Timeline

**Goal:** Identify when pattern elements first appeared

**Example Analysis:**
```python
def build_pattern_timeline(repo_name, pattern_name):
    """
    Track when a pattern emerged in a repository
    """
    timeline = {
        'pattern': pattern_name,
        'repo': repo_name,
        'emergence': None,
        'milestones': []
    }
    
    # Get architectural commits
    commits = get_architectural_commits(repo_name)
    
    for commit in commits:
        # Check if pattern keywords in files/message
        if pattern_in_commit(commit, pattern_name):
            if not timeline['emergence']:
                timeline['emergence'] = commit['time']
            
            timeline['milestones'].append({
                'time': commit['time'],
                'sha': commit['sha'],
                'files': commit['files'],
                'author': commit['author']
            })
    
    return timeline

# Example: Track GraphRAG pattern in LightRAG
timeline = build_pattern_timeline('HKUDS_LightRAG', 'GraphRAG')
print(f"Pattern emerged: {timeline['emergence']}")
print(f"Key milestones: {len(timeline['milestones'])}")
```

---

### Step 4: Store in Neo4j

**Goal:** Add temporal relationships to existing pattern data

**Neo4j Schema Addition:**
```cypher
// Pattern emergence
MERGE (p:Pattern {name: "GraphRAG Implementation"})
MERGE (r:Repository {url: "https://github.com/HKUDS/LightRAG"})
MERGE (c:Commit {sha: "abc123...", timestamp: 1640000000})
MERGE (p)-[:EMERGED_IN]->(c)
MERGE (c)-[:BELONGS_TO]->(r)

// Pattern evolution
MERGE (c2:Commit {sha: "def456...", timestamp: 1650000000})
MERGE (p)-[:EVOLVED_IN]->(c2)

// Temporal query
MATCH (p:Pattern)-[e:EMERGED_IN]->(c:Commit)
RETURN p.name, c.timestamp
ORDER BY c.timestamp ASC
```

---

### Step 5: Enable Temporal Queries

**New Capabilities:**

**1. Pattern Age:**
```cypher
// How old is this pattern?
MATCH (p:Pattern {name: "GraphRAG"})-[:EMERGED_IN]->(c:Commit)
WITH p, c.timestamp as emergence
WITH p, (datetime().epochSeconds - emergence) / 86400 as days_old
RETURN p.name, days_old
```

**2. Pattern Evolution Speed:**
```cypher
// How fast did pattern mature?
MATCH (p:Pattern)-[:EMERGED_IN]->(first:Commit)
MATCH (p)-[:EVOLVED_IN]->(commits:Commit)
WITH p, first.timestamp as start, max(commits.timestamp) as latest, count(commits) as evolution_count
WITH p, (latest - start) / 86400 as evolution_days, evolution_count
RETURN p.name, evolution_days, evolution_count
```

**3. Pattern Timeline:**
```cypher
// Show pattern evolution over time
MATCH (p:Pattern {name: "GraphRAG"})-[:EVOLVED_IN]->(c:Commit)
RETURN c.timestamp, c.sha, c.message
ORDER BY c.timestamp ASC
```

---

## Example Output

### Pattern Evolution Timeline for LightRAG

```
Pattern: GraphRAG Implementation
Repository: HKUDS/LightRAG
Emerged: 2024-03-15 (commit abc123)

Milestones:
  2024-03-15 [abc123] - Initial GraphRAG structure (Author: HKUDS)
  2024-04-02 [def456] - Added Neo4j integration (Author: HKUDS)
  2024-05-10 [ghi789] - LLM integration via LangChain (Author: Contributor1)
  2024-06-20 [jkl012] - Community detection algorithm (Author: HKUDS)
  2024-08-15 [mno345] - Vector search enhancement (Author: Contributor2)

Evolution Speed: 153 days, 47 architectural commits
Pattern Maturity: Mature (active development)
```

---

## Data Quality Considerations

### WoC Data Characteristics

**Strengths:**
- Complete history (all commits preserved)
- Timestamp accuracy (from git metadata)
- Cross-repository coverage

**Limitations:**
- Commit messages vary in quality
- Some commits incorrectly timestamped (future dates)
- Fork commits may duplicate history
- Bot commits may pollute data

### Filtering Strategy

**Filter Out:**
```python
def is_valid_commit(commit):
    timestamp = commit['time']
    author = commit['author']
    
    # Exclude future commits (incorrect timestamps)
    if timestamp > time.time():
        return False
    
    # Exclude very old commits (pre-pattern era)
    if timestamp < 1262304000:  # Before 2010
        return False
    
    # Exclude bot commits
    bot_indicators = ['bot', 'dependabot', '[bot]', 'automated']
    if any(indicator in author.lower() for indicator in bot_indicators):
        return False
    
    return True
```

---

## Performance Optimization

### Challenge
Querying 228 repos × average 1000 commits = 228K commits to process

### Optimization Strategies

**1. Parallel Processing**
```python
from multiprocessing import Pool

def process_repo(repo_name):
    return extract_pattern_timeline(repo_name)

# Process 10 repos in parallel
with Pool(10) as pool:
    timelines = pool.map(process_repo, repo_list)
```

**2. Cache WoC Queries**
```python
# Cache commit data locally
@lru_cache(maxsize=10000)
def get_commit_data(commit_sha):
    return Commit(commit_sha).attributes
```

**3. Batch Queries**
```bash
# Query multiple repos at once via shell
for repo in $(cat repo_list.txt); do
    echo $repo | ~/lookup/getValues p2c >> all_commits.txt
done
```

---

## Success Metrics

### Validation Criteria

**Phase 1 POC Success:**
- ✅ Can extract commit history for one repo
- ✅ Can identify architectural commits
- ✅ Can build pattern timeline
- ✅ Timeline makes sense (validates actual pattern emergence)
- ✅ Processing time < 5 minutes per repo

**Phase 2 Batch Success:**
- ✅ All 228 repos processed
- ✅ Pattern timelines stored in Neo4j
- ✅ Temporal queries working
- ✅ Insights are actionable

---

## Expected Timeline

**Phase 1 POC:**
- Day 1: Request access, setup oscar.py
- Day 2: Query one repo, build timeline, validate
- **Decision Point:** Proceed or defer?

**Phase 2 Batch (if proceeding):**
- Days 3-4: Write batch processing script
- Days 5-7: Process all 228 repos
- Day 8: Store in Neo4j
- Days 9-10: Build query interface, validate

**Total:** 10 days from access to production

---

## Risk Assessment

**Low Risk:**
- WoC access is free
- oscar.py is mature
- Commit history data is high quality
- Processing is parallelizable

**Medium Risk:**
- Learning curve for WoC APIs
- Data volume (processing time)
- Integration with existing Neo4j schema

**Mitigation:**
- Start with Phase 1 POC (low commitment)
- Only proceed if clear value
- Can defer if time-constrained

---

## Alternative: Lightweight Approach

**If WoC seems too heavy, alternative:**

Use GitHub GraphQL API for commit history:
```graphql
query {
  repository(owner: "HKUDS", name: "LightRAG") {
    defaultBranchRef {
      target {
        ... on Commit {
          history(first: 100) {
            nodes {
              committedDate
              message
              author { name email }
              changedFiles
            }
          }
        }
      }
    }
  }
}
```

**Pros:**
- No WoC access needed
- Simpler integration
- GitHub API already familiar

**Cons:**
- Limited to 100 commits per query (pagination needed)
- Rate limits (5000 requests/hour)
- Only GitHub (WoC includes GitLab, Bitbucket)
- No cross-repository analysis

---

## Bottom Line

**Commit history integration via WoC:**
- **Value:** Very High (enables temporal pattern analysis)
- **Complexity:** Medium (new API to learn)
- **Time:** 10 days from start to production
- **Risk:** Low (POC validates before full commitment)

**Recommendation:** Run Phase 1 POC after duplicate detection is complete. WoC's 3.1B commits could transform your pattern extraction from static snapshots to dynamic evolution tracking.
