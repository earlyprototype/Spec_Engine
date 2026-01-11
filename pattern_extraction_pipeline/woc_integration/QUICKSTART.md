# World of Code - Quick Start Guide

**For:** Pattern Extraction Pipeline Enhancement  
**Goal:** Add historical depth to pattern analysis

---

## Step-by-Step: First 48 Hours

### Day 1: Setup & Access

**Morning (2 hours)**

**1. Generate SSH Key (if needed)**
```bash
ssh-keygen -t rsa -b 4096
cat ~/.ssh/id_rsa.pub
# Copy this public key
```

**2. Request WoC Access**
- Visit: https://worldofcode.org/
- Fill registration form with:
  - Your SSH public key
  - GitHub handle
  - Purpose: "Mining architectural patterns from GraphRAG repositories"
- Wait for confirmation email (same day, usually <4 hours)

**3. Test Connection (once approved)**
```bash
# Add to ~/.ssh/config
Host da0
    Hostname da0.eecs.utk.edu
    Port 443
    User YOUR_USERNAME
    IdentityFile ~/.ssh/id_rsa

# Test login
ssh da0
```

**Afternoon (2 hours)**

**4. Clone oscar.py**
```bash
# On da0 server
ssh da0
git clone https://github.com/ssc-oscar/oscar.py
cd oscar.py

# Install dependencies
pip install --user clickhouse-driver
```

**5. Test Basic Query**
```bash
# Get commits for a project
cd ~/oscar.py
python3
>>> from oscar import Project
>>> p = Project('torvalds_linux')
>>> commits = p.commit_shas
>>> print(f"Linux has {len(commits)} commits")
```

**Evening (1 hour)**

**6. Review Your Analyzed Repos**
```bash
# On your local machine
# Get list of repos you've analyzed
cypher-shell -u neo4j -p password -a bolt://localhost:7688 \
  "MATCH (p:Pattern) RETURN DISTINCT p.source_repo" > my_repos.txt

# Format for WoC (convert URLs to WoC format)
# https://github.com/HKUDS/LightRAG → HKUDS_LightRAG
```

---

### Day 2: First Real Query

**Morning (3 hours)**

**7. Query ONE Repository's History**
```python
#!/usr/bin/env python3
# test_woc_query.py

from oscar import Project, Commit
from datetime import datetime

repo_name = "HKUDS_LightRAG"  # Replace with your repo
print(f"Analyzing {repo_name}...")

# Get all commits
project = Project(repo_name)
commits = list(project.commit_shas)
print(f"Total commits: {len(commits)}")

# Analyze first 10 commits
for i, commit_sha in enumerate(commits[:10]):
    try:
        commit = Commit(commit_sha)
        timestamp, tz, author = commit.attributes[:3]
        date = datetime.fromtimestamp(timestamp)
        files = commit.changed_file_names
        
        print(f"\n[{i+1}] {date.strftime('%Y-%m-%d')}")
        print(f"    Author: {author}")
        print(f"    Files: {len(files)}")
        
        # Look for architectural files
        arch_files = [f for f in files if 'graph' in f.lower() or 'rag' in f.lower()]
        if arch_files:
            print(f"    Architectural: {arch_files[:3]}")
            
    except Exception as e:
        print(f"    Error: {e}")
        continue

print("\n[SUCCESS] WoC query working!")
```

**Run it:**
```bash
ssh da0
cd ~/
python3 test_woc_query.py
```

**Afternoon (2 hours)**

**8. Build Simple Timeline**
```python
#!/usr/bin/env python3
# build_timeline.py

from oscar import Project, Commit
from datetime import datetime
from collections import defaultdict

def build_pattern_timeline(repo_name):
    """
    Build timeline of architectural changes
    """
    project = Project(repo_name)
    commits = project.commit_shas
    
    timeline = []
    
    for commit_sha in commits:
        try:
            commit = Commit(commit_sha)
            timestamp = commit.attributes[0]
            files = commit.changed_file_names
            
            # Filter for architectural files
            arch_files = [f for f in files if (
                'graph' in f.lower() or
                'rag' in f.lower() or
                f.endswith('README.md') or
                f.endswith('requirements.txt') or
                '/src/' in f or
                '/lib/' in f
            )]
            
            if arch_files:
                timeline.append({
                    'timestamp': timestamp,
                    'date': datetime.fromtimestamp(timestamp),
                    'commit': commit_sha,
                    'files': arch_files
                })
        except:
            continue
    
    # Sort by timestamp
    timeline.sort(key=lambda x: x['timestamp'])
    
    return timeline


# Test
timeline = build_pattern_timeline('HKUDS_LightRAG')

print(f"Architectural evolution: {len(timeline)} key commits\n")
for i, event in enumerate(timeline[:10]):
    print(f"[{i+1}] {event['date'].strftime('%Y-%m-%d')}: {len(event['files'])} files")
    print(f"    {event['files'][:2]}")

# Save
import json
with open('lightrag_timeline.json', 'w') as f:
    json.dump(timeline, f, default=str, indent=2)

print(f"\n[SAVED] lightrag_timeline.json")
```

**Evening (1 hour)**

**9. Validate Results**
```bash
# Compare WoC timeline with GitHub
# Visit: https://github.com/HKUDS/LightRAG/commits
# Spot check: Do dates match? Do files match?
```

**10. Decision Point**

If timeline looks good:
- ✅ Proceed to batch processing (Phase 2)

If timeline has issues:
- Debug data quality
- Adjust filtering
- Or consider this isn't worth it

---

## Success Checklist

**After 48 Hours, You Should Have:**

- [  ] WoC access granted
- [  ] Can SSH to da0
- [  ] oscar.py installed and working
- [  ] Successfully queried ONE repo
- [  ] Built pattern timeline for one repo
- [  ] Timeline validated against GitHub
- [  ] Decision made: proceed or defer?

---

## If Proceeding to Batch Processing

### Week 1: Process All Repos

**Script:** `batch_extract_timelines.py`

```python
#!/usr/bin/env python3
"""
Process all analyzed repositories
"""

from oscar import Project, Commit
from multiprocessing import Pool
import json

# Load your repo list
with open('my_repos.txt') as f:
    repos = [line.strip() for line in f]

def process_repo(repo_name):
    try:
        timeline = build_pattern_timeline(repo_name)
        return {
            'repo': repo_name,
            'timeline': timeline,
            'status': 'success'
        }
    except Exception as e:
        return {
            'repo': repo_name,
            'error': str(e),
            'status': 'failed'
        }

# Process 10 repos in parallel
with Pool(10) as pool:
    results = pool.map(process_repo, repos)

# Save results
with open('all_timelines.json', 'w') as f:
    json.dump(results, f, default=str, indent=2)

# Summary
successful = len([r for r in results if r['status'] == 'success'])
print(f"Processed: {successful}/{len(repos)} repos")
```

**Run:**
```bash
ssh da0
python3 batch_extract_timelines.py
# Wait ~2-4 hours for 228 repos
```

---

### Week 2: Integrate with Neo4j

**Script:** `load_timelines_to_neo4j.py`

```python
#!/usr/bin/env python3
"""
Load WoC timelines into Neo4j
"""

from neo4j import GraphDatabase
import json

driver = GraphDatabase.driver(
    "bolt://localhost:7688",
    auth=("neo4j", "password")
)

# Load timeline data
with open('all_timelines.json') as f:
    timelines = json.load(f)

with driver.session() as session:
    for result in timelines:
        if result['status'] != 'success':
            continue
        
        repo_url = result['repo'].replace('_', '/')
        timeline = result['timeline']
        
        # Store pattern emergence
        if timeline:
            first_commit = timeline[0]
            session.run("""
                MATCH (p:Pattern {source_repo: $repo})
                SET p.pattern_emerged = datetime($emerged)
                SET p.first_arch_commit = $commit
                SET p.evolution_commits = $count
            """,
            repo=f"https://github.com/{repo_url}",
            emerged=first_commit['date'].isoformat(),
            commit=first_commit['commit'],
            count=len(timeline)
            )

print("[DONE] Timelines loaded into Neo4j!")
driver.close()
```

---

## Common Issues & Solutions

### Issue 1: SSH Connection Timeout
**Symptom:** `Connection timed out` or `No route to host`  
**Fix:** Check VPN if required, verify port 443 open, try da1/da2/da3 instead

### Issue 2: oscar.py Import Errors
**Symptom:** `ModuleNotFoundError: clickhouse-driver`  
**Fix:** `pip install --user clickhouse-driver`

### Issue 3: Repository Not Found
**Symptom:** `Project('HKUDS_LightRAG')` returns empty  
**Fix:** Check WoC naming convention:
- GitHub: `owner_repo` (underscore, not slash)
- Lowercase recommended
- Try variations: `hkuds_lightrag`

### Issue 4: Slow Queries
**Symptom:** Queries take >10 minutes  
**Fix:** Use shell API with grep for filtering first, then Python for processing

### Issue 5: Data Quality Issues
**Symptom:** Commits with future dates or missing data  
**Fix:** Filter invalid timestamps:
```python
if not (1262304000 < timestamp < time.time()):
    continue  # Skip invalid timestamps
```

---

## Quick Reference: WoC Naming

### Map Naming Convention

Format: `source2destination`

**Examples:**
- `a2c` = Author to Commits
- `c2p` = Commit to Project
- `b2f` = Blob to File
- `p2a` = Project to Authors

**Capital letters = Cleaned/Aliased:**
- `A2c` = Aliased Author to Commits (duplicates merged)
- `P2c` = Deforked Project to Commits (forks merged)

---

## When to Ask for Help

**WoC Community Support:**
- Discord: WoC community server
- GitHub Issues: https://github.com/woc-hack/tutorial/issues
- Email: Via registration contact

**Common Questions:**
- "How do I query for X?"
- "My query is slow, how to optimize?"
- "Data format clarification?"
- "Repository name format?"

---

## Next Steps After Quick Start

1. **Validate:** Timelines match reality?
2. **Analyze:** What insights do timelines reveal?
3. **Decide:** Worth continuing to dependency mining?
4. **Scale:** Process all repos or subset?
5. **Integrate:** Add to production pipeline or one-time analysis?

---

## Resources

**Essential Reading:**
- Tutorial: https://github.com/woc-hack/tutorial
- oscar.py docs: In repository
- WoC site: https://worldofcode.org/docs/#/

**Your Integration Docs:**
- `01_COMMIT_HISTORY_INTEGRATION.md` - Detailed implementation
- `02_DEPENDENCY_PATTERN_MINING.md` - Tech stack analysis
- `README.md` - Overview and strategy

---

## Bottom Line

**48 hours from zero to validated timeline for ONE repo.**

If successful, you've proven WoC can add historical depth to your pattern extraction. Then decide: batch process all repos or defer?

**Don't overthink it. Just request access and run the Day 1 test query. You'll know immediately if it's valuable.**
