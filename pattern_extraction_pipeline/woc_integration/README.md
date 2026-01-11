# World of Code (WoC) Integration Plan

**Date:** January 2026  
**Purpose:** Leverage World of Code infrastructure to enhance pattern extraction pipeline

---

## What is World of Code?

World of Code is a large-scale infrastructure for mining and analyzing the entire open-source software ecosystem.

**Scale:**
- 173 million Git repositories
- 3.1 billion commits
- 12.6 billion trees
- 12.5 billion blobs
- 250+ terabytes of data
- Monthly updates

**Sources:** GitHub, GitLab, Bitbucket, and other public VCS platforms

---

## Why WoC Matters for Your Pipeline

### Current State
You analyze ~250 repositories at a time, extracting architectural patterns from current code state.

### WoC Adds Three Critical Dimensions

1. **Historical Depth** - See how patterns evolved over time
2. **Dependency Data** - Pre-extracted imports/dependencies from all code
3. **Ecosystem Context** - Cross-repository relationships and code sharing

---

## Key WoC Capabilities Relevant to Pattern Extraction

### 1. Commit History Access (HIGHEST PRIORITY)

**What:** Complete commit history for all 173M repositories

**WoC Maps:**
- `c2dat` - Commit to full data (tree, parent, author, timestamp, message)
- `c2ta` - Commit to timestamp + author
- `p2c` / `c2p` - Project ↔ Commit mappings
- `c2b` - Commit to blobs (files changed)

**Your Use Case:**
```
For repo: HKUDS/LightRAG
→ Get all commits from WoC
→ Filter commits touching architectural files
→ Track when GraphRAG pattern elements appeared
→ Build evolution timeline
→ Store in Neo4j with temporal relationships
```

**Answers:**
- When did this pattern first appear?
- How has the pattern evolved?
- What was the pattern before GraphRAG?
- When did key dependencies get added?

---

### 2. Dependency Data (HIGH PRIORITY)

**What:** Pre-extracted imports/dependencies from all source code files

**WoC Files:**
- `c2PtAbflPkg` - Commit → Project → Time → Author → Blob → Filename → Language → Packages
- Format: `commit;repo;timestamp;author;blob;file;language;module1;module2;...`

**Example:**
```
000005efe300482514d70d44c5fa922b34ff79a5;Rayhane-mamah_Tacotron-2;1557284915;qq443452099;...;tacotron/synthesizer.py;PY;tensorflow;numpy;librosa.effects;wave;datetime.datetime
```

**Your Use Case:**
```
Query: "What packages do GraphRAG repositories import?"
Result: LangChain, LlamaIndex, Neo4j, OpenAI, Anthropic, etc.

Query: "When did Neo4j adoption spike in knowledge-graph repos?"
Result: Timeline of Neo4j import frequency

Query: "What's the common dependency pattern for RAG systems?"
Result: Vector DB + LLM + Graph DB = standard stack
```

**Answers:**
- What technologies define each architectural pattern?
- When did key frameworks get adopted?
- What's the typical tech stack for GraphRAG?
- Which dependencies correlate with quality?

---

### 3. Cross-Repository Code Sharing (MEDIUM PRIORITY)

**What:** Track exact code sharing between repositories

**WoC Maps:**
- `b2tac` - Blob to time/author/commit (all repos using this blob)
- `Ptb2Pt` - Project/time/blob to Project/time (copy-based reuse)
- `b2P` - Blob to projects (where does this code appear?)

**Your Use Case:**
```
For pattern implementation code:
→ Find which blob contains core pattern code
→ Query WoC: where else does this blob appear?
→ Identify pattern spread (who copied from whom)
→ Build diffusion network
```

**Answers:**
- How do patterns spread between repos?
- Who are the pattern innovators vs adopters?
- Which patterns get copied most?
- What's the pattern adoption network?

---

### 4. Author Networks (MEDIUM PRIORITY)

**What:** Track developer activity and contributions

**WoC Maps:**
- `a2c` - Author to commits
- `a2f` - Author to files
- `A2c` - Aliased author (consolidated identities)
- `A2P` - Aliased author to projects

**Your Use Case:**
```
For influential patterns:
→ Identify key authors who created the pattern
→ Track their other contributions
→ Build social network of pattern creators
→ Understand knowledge flow
```

**Answers:**
- Who creates influential patterns?
- How do patterns spread through developer networks?
- Which communities drive architectural innovation?

---

### 5. File-Level Evolution (LOW PRIORITY)

**What:** Track changes to specific files over time

**WoC Maps:**
- `f2c` - File to commits
- `c2f` - Commit to files
- `b2f` - Blob to filename

**Your Use Case:**
- Track changes to README.md (pattern documentation evolution)
- Monitor architectural file changes (e.g., /src/graph/index.ts)
- Understand refactoring patterns

---

## Integration Strategy

### Phase 1: Proof of Concept (Start Here)

**Scope:** ONE repository, commit history only

**Steps:**
1. Request WoC access (registration form)
2. Get SSH access to da servers
3. Query commit history for `HKUDS/LightRAG`
4. Extract architectural commit timestamps
5. Build simple timeline
6. Validate data quality

**Time:** 1-2 days  
**Risk:** Low  
**Value:** Proves feasibility

---

### Phase 2: Batch Historical Analysis

**Scope:** All 228 analyzed repositories, commit history

**Steps:**
1. Query WoC for commit history of all analyzed repos
2. Filter commits touching architectural files (README, /src/, /lib/, setup.py, package.json)
3. Extract pattern emergence timestamps
4. Store in Neo4j as temporal properties
5. Enable queries like "show pattern evolution timeline"

**Time:** 1 week  
**Risk:** Medium (data processing complexity)  
**Value:** High (enables temporal analysis)

---

### Phase 3: Dependency Pattern Mining

**Scope:** Extract dependency patterns from WoC

**Steps:**
1. Query `c2PtAbflPkg` files for your 228 repos
2. Extract dependency lists per repo
3. Identify common stacks (e.g., Neo4j + LangChain + OpenAI)
4. Store as pattern relationships in Neo4j
5. Enable queries like "what dependencies define GraphRAG pattern?"

**Time:** 2 weeks  
**Risk:** Medium (large data volume)  
**Value:** Very High (reveals tech stack patterns)

---

### Phase 4: Ecosystem Analysis

**Scope:** Pattern diffusion and code sharing

**Steps:**
1. Identify key pattern implementation files
2. Query WoC for where those blobs appear
3. Build pattern spread network
4. Track adoption timeline
5. Identify pattern innovators vs adopters

**Time:** 2-3 weeks  
**Risk:** High (complex analysis)  
**Value:** High (research-grade insights)

---

## Immediate Action Items

### 1. Request WoC Access (Optional)
**Form:** https://worldofcode.org/ registration
- Provide SSH public key
- GitHub/Bitbucket handles
- Research purpose: "Mining architectural patterns from GraphRAG/knowledge graph repositories"

**Access Granted:** Usually same day, max 1 day

---

### 2. Install oscar.py (Python API)
```bash
git clone https://github.com/ssc-oscar/oscar.py
cd oscar.py
pip install clickhouse-driver
```

**Key Classes:**
- `Author('...')` - Author analysis
- `Commit('...')` - Commit analysis
- `Project('...')` - Project analysis
- `Blob('...')` - Blob/file analysis

---

### 3. Test Query (No Access Needed Yet)
Review WoC tutorial to understand data structure:
- https://github.com/woc-hack/tutorial

**Key Concepts:**
- Maps are split into 32 or 128 parts (for parallel processing)
- Shell API (fast) vs Python API (convenient)
- `.tch` files for random access, `.s/.gz` files for sweeps

---

## Data You Can Extract from WoC

### For Each of Your 228 Analyzed Repos:

| Data Type | WoC Source | Your Benefit |
|-----------|-----------|--------------|
| Commit history | `p2c` | Pattern evolution timeline |
| Timestamps | `c2ta` | When pattern emerged |
| Dependencies | `c2PtAbflPkg` | Tech stack patterns |
| Authors | `p2a` | Pattern creator networks |
| File changes | `c2f` | Architectural evolution |
| Code sharing | `b2tac` | Pattern diffusion |
| First appearance | `b2fa` | Pattern origin tracking |

---

## Quick Win Examples

### Example 1: Pattern First Appearance

**Goal:** When did GraphRAG pattern first appear?

**WoC Query:**
```python
from oscar import Project, Commit

# Get all commits for LightRAG repo
commits = Project('HKUDS_LightRAG').commit_shas

# Sort by timestamp
sorted_commits = sorted(commits, key=lambda c: Commit(c).attributes[0])

# First commit = pattern origin
first_commit = Commit(sorted_commits[0])
print(f"Pattern emerged: {first_commit.attributes[0]}")  # timestamp
```

---

### Example 2: Dependency Timeline

**Goal:** When did repos start using Neo4j?

**WoC Query:**
```bash
# Search dependency data for Neo4j imports
zcat /da?_data/basemaps/gz/c2PtAbflPkgFullU*.s | grep -i 'neo4j' | sort -t';' -k3 -n > neo4j_timeline.csv
```

**Result:** CSV with: commit, repo, timestamp, author, file, language, neo4j + other deps

---

### Example 3: Code Sharing Detection

**Goal:** Which repos share GraphRAG implementation code?

**WoC Query:**
```bash
# Find all repos using specific blob (e.g., GraphRAG core algorithm file)
echo "<blob_sha>" | ~/lookup/getValues b2P
```

**Result:** List of all projects with that exact code

---

## Integration Architecture

### Current Pipeline (You Have This)
```
GitHub API → PatternExtractor → Neo4j
     ↓
Current code snapshot
```

### Enhanced with WoC
```
GitHub API → PatternExtractor → Neo4j
     ↓              ↑
Current snapshot   WoC Historical Data
                    ↓
           Commit history
           Dependencies
           Code sharing
           Author networks
```

### Neo4j Schema Enhancement

**Add Temporal Relationships:**
```cypher
// Pattern evolution
(Pattern)-[:EMERGED_AT {timestamp}]->(Commit)
(Pattern)-[:EVOLVED_IN {timestamp}]->(Commit)

// Dependency timeline
(Pattern)-[:ADOPTED_TECH {timestamp}]->(Technology)
(Technology)-[:USED_BY {timestamp}]->(Pattern)

// Pattern diffusion
(Pattern)-[:SPREAD_TO {timestamp}]->(Repository)
(Repository)-[:COPIED_FROM {timestamp}]->(Repository)

// Author influence
(Author)-[:CREATED]->(Pattern)
(Author)-[:INFLUENCED]->(Author)
```

---

## Cost-Benefit Analysis

### Benefits of WoC Integration

**High-Impact Benefits:**
1. Pattern evolution tracking (Research-grade insight)
2. Dependency pattern mining (Tech stack understanding)
3. Temporal analysis (When patterns emerged/adopted)
4. Pattern diffusion networks (How patterns spread)

**Research Opportunities:**
- Publish papers on pattern evolution
- Track architectural trends over time
- Identify pattern innovation sources
- Understand ecosystem dynamics

### Costs

**Time Investment:**
- Initial setup: 1-2 days (registration, learning API)
- Phase 1 POC: 1-2 days (one repo test)
- Phase 2 batch: 1 week (all 228 repos)
- Phase 3+ advanced: 2-4 weeks each

**Complexity:**
- Learning WoC data structures
- Processing large datasets (TB scale if doing sweeps)
- Integrating temporal data into Neo4j

**Infrastructure:**
- SSH access to da servers (free)
- Processing scripts (Python/Perl)
- Increased Neo4j storage (minimal)

---

## Decision Framework

### When to Use WoC

**Use WoC When:**
- You want pattern evolution timelines
- You need dependency/tech stack analysis
- You're researching pattern diffusion
- You want to publish research papers
- You need historical depth beyond current code state

**Don't Use WoC When:**
- Just need current architecture patterns (GitHub API sufficient)
- Time constraints (adds complexity)
- Single snapshot analysis adequate
- Research depth not required

---

## Recommendation

### For Your Current Phase
**Complete duplicate detection testing first!** (You're at 80%)

### After Current Feature is Complete
**Start with WoC Phase 1 POC:**
1. Request access (1 day)
2. Test commit history for ONE repo (1 day)
3. Evaluate if insights justify complexity
4. Decision point: proceed or defer

**If POC successful:**
- Implement Phase 2 (batch commit history)
- Consider Phase 3+ for research publications

**If POC shows limited value:**
- Defer WoC integration
- Focus on current pipeline scale/quality
- Revisit later when publishing research

---

## Resources

**WoC Documentation:**
- Main Site: https://worldofcode.org/docs/#/
- Tutorial: https://github.com/woc-hack/tutorial
- Registration: https://worldofcode.org/ (form)

**APIs:**
- oscar.py (Python): https://github.com/ssc-oscar/oscar.py
- Shell API: https://bitbucket.org/swsc/lookup

**Support:**
- Discord: WoC community
- Email: Support via registration

---

## Next Steps

1. **Finish current duplicate detection testing** ← DO THIS FIRST
2. Review WoC tutorial (30 minutes)
3. Decide if historical/dependency analysis valuable
4. If yes: Request WoC access
5. If yes: Run Phase 1 POC
6. Evaluate and decide on Phase 2+

---

## Bottom Line

World of Code is **incredibly powerful** but adds significant complexity. The key question: **Do you need historical depth and ecosystem analysis, or is current-state pattern extraction sufficient?**

For research publications: WoC is essential.  
For production pattern database: Current approach may be adequate.

**Recommendation:** Complete current work, then run WoC Phase 1 POC to evaluate value.
