# World of Code - Data Maps Quick Reference

**Purpose:** Quick lookup for WoC data maps relevant to pattern extraction

---

## Map Naming Convention

Format: `source2destination`

- Lowercase = Raw data
- **Uppercase = Cleaned/Aliased data** (use these when possible)

**Example:**
- `a2c` = Raw author to commits
- `A2c` = **Aliased author** to commits (duplicates merged, bots removed)

---

## Core Object Types

| Letter | Object | Example |
|--------|--------|---------|
| **a** | Author | `John Doe <john@example.com>` |
| **A** | Aliased Author | Consolidated identity (use this) |
| **b** | Blob | SHA1 of file content |
| **c** | Commit | SHA1 of commit |
| **cc** | Child Commit | Commits that follow |
| **pc** | Parent Commit | Commits that precede |
| **f** | File | Filename/path |
| **p** | Project | Repository (owner_repo format) |
| **P** | Deforked Project | Root project (use this) |
| **t** | Time | Unix timestamp |
| **tk** | Tokens | ctags output |

---

## Priority Maps for Pattern Extraction

### HIGHEST PRIORITY: Commit History

| Map | Format | Use Case |
|-----|--------|----------|
| **`p2c`** | project;commit1;commit2;... | Get all commits for repo |
| **`c2dat`** | commit;tree;parent;time;author;message | Full commit metadata |
| **`c2ta`** | commit;timestamp;author | Quick timestamp lookup |
| **`c2f`** | commit;file1;file2;... | Files changed in commit |
| **`c2b`** | commit;blob1;blob2;... | Blobs (file versions) in commit |

**Your Use:**
- Track pattern evolution
- Identify when pattern emerged
- Build architectural timelines

---

### HIGH PRIORITY: Dependencies

| Map | Format | Use Case |
|-----|--------|----------|
| **`c2PtAbflPkg`** | commit;project;time;author;blob;file;lang;dep1;dep2;... | All dependencies |
| **`c2PtAbflDef`** | Same format, but deps → definitions | What package is defined |

**Your Use:**
- Extract tech stack patterns
- Track framework adoption
- Identify common dependency combinations
- Correlate dependencies with quality

**Files:** 128 split files (`c2PtAbflPkgFullU0.s` to `...U127.s`)

---

### MEDIUM PRIORITY: Code Sharing

| Map | Format | Use Case |
|-----|--------|----------|
| **`b2tac`** | blob;time1;author1;commit1;time2;author2;commit2;... | All commits using blob |
| **`b2fa`** | blob;timestamp;author;commit | First appearance of blob |
| **`Ptb2Pt`** | project1;time1;blob;project2;time2 | Copy-based reuse |
| **`b2P`** | blob;project1;project2;... | Projects using blob |

**Your Use:**
- Track pattern code sharing
- Identify pattern originators
- Build diffusion networks
- Find copied implementations

---

### MEDIUM PRIORITY: Author Networks

| Map | Format | Use Case |
|-----|--------|----------|
| **`A2c`** | aliased_author;commit1;commit2;... | All commits by author |
| **`A2P`** | aliased_author;project1;project2;... | Projects by author |
| **`P2a`** | project;author1;author2;... | Authors in project |
| **`a2A`** | raw_author;aliased_author | Identity consolidation |

**Your Use:**
- Identify pattern creators
- Build author influence networks
- Track knowledge flow
- Find key contributors

---

### LOW PRIORITY: Repository Metadata

| Map | Format | Use Case |
|-----|--------|----------|
| **`P2core`** | project;author1;author2;... | Core contributors (80%+ commits) |
| **`lc2Pdat`** | last_commit;project;time;author;tree | Latest project state |
| **`P2g`** | project;language1;language2;... | Languages used |

**Your Use:**
- Validate project characteristics
- Filter by language
- Identify core maintainers

---

## Special Maps

### License Detection

**`P2Lt`**: project;license;timestamp  
**Example:** `HKUDS_LightRAG;MIT;2024-03`

### First Blob Appearance

**`b2fa`**: blob;timestamp;author;commit  
**Use:** Find who originally created code

### Last Blob to File

**`lb2f`**: blob;filename  
**Use:** Map blob to current filename

---

## Data Access Methods

### 1. Random Access (Fast for Few Keys)

**Command:** `~/lookup/getValues mapname`

```bash
# Get commits for one project
echo "HKUDS_LightRAG" | ~/lookup/getValues p2c

# Get commit metadata
echo "abc123..." | ~/lookup/getValues c2dat
```

**When to Use:**
- Querying <1000 items
- Interactive exploration
- Testing queries

---

### 2. Sweep/Grep (Fast for Pattern Matching)

**Command:** `zcat /da?_data/basemaps/gz/mapnameFullUX.s | grep pattern`

```bash
# Find all repos using Neo4j
zcat /da?_data/basemaps/gz/c2PtAbflPkgFullU*.s | grep -i "neo4j"

# Find all Python files
zcat /da?_data/basemaps/gz/b2fFullU*.s | grep '\.py;'
```

**When to Use:**
- Searching entire dataset
- Pattern matching
- Filtering large results

---

### 3. Python API (Convenient)

**Command:** `oscar.py` classes

```python
from oscar import Project, Commit, Author, Blob

# Object-oriented access
project = Project('HKUDS_LightRAG')
commits = project.commit_shas

commit = Commit('abc123...')
files = commit.changed_file_names
```

**When to Use:**
- Python scripts
- Interactive analysis
- Complex logic

---

## File Locations on da Servers

### Base Maps (Relationships)
```
/da[0-5]_data/basemaps/gz/
  - a2cFullU*.s      (Author to Commits)
  - c2pFullU*.s      (Commit to Project)
  - p2cFullU*.s      (Project to Commits)
  - b2facFullU*.s    (Blob to First Author/Commit)
  ...
```

### Dependencies
```
/da[0-5]_data/basemaps/gz/
  - c2PtAbflPkgFullU*.s   (Dependencies)
  - c2PtAbflDefFullU*.s   (Definitions)
```

### Blob Content
```
/da5_data/All.blobs/
  - Used by showCnt blob command
```

---

## Map Split Convention

Most maps split into **32** or **128** parts based on SHA1 hash:

**32-way split:** Based on first byte % 32
- Files: `mapname.0.tch` to `mapname.31.tch`
- Example: `a2cFullU.0.tch` to `a2cFullU.31.tch`

**128-way split:** Based on first 7 bits
- Files: `mapnameFullU0.s` to `mapnameFullU127.s`
- Example: `c2PtAbflPkgFullU0.s` to `c2PtAbflPkgFullU127.s`

**Why:** Enables parallel processing

---

## Quick Lookup Examples

### Example 1: Get Project Commits
```bash
echo "HKUDS_LightRAG" | ~/lookup/getValues p2c
```

### Example 2: Get Commit Details
```bash
echo "abc123def456..." | ~/lookup/getValues c2dat
```

### Example 3: Find All Neo4j Users
```bash
zcat /da?_data/basemaps/gz/c2PtAbflPkgFullU*.s | grep -i ";neo4j"
```

### Example 4: Get Blob Content
```bash
echo "blob_sha1..." | ~/lookup/showCnt blob
```

### Example 5: Find Author's Projects
```bash
echo "John Doe <john@example.com>" | ~/lookup/getValues a2P
```

---

## Data Quality Notes

### Use Aliased/Deforked Versions

**Raw versions (lowercase):**
- `a2c` - Contains duplicate authors, bots, invalid IDs
- `p2c` - Contains fork duplicates

**Cleaned versions (uppercase):**
- **`A2c`** - Duplicates merged, bots removed (USE THIS)
- **`P2c`** - Forks merged to root project (USE THIS)

### Invalid Data

**Watch Out For:**
- Timestamps in future (user system clock wrong)
- Timestamps before 1990 (invalid git data)
- Bot authors (`dependabot`, `[bot]`)
- Empty/null fields

**Filter:**
```python
# Validate timestamp
if not (1262304000 < timestamp < time.time()):
    continue  # Skip invalid (pre-2010 or future)

# Exclude bots
if '[bot]' in author.lower() or 'bot@' in author.lower():
    continue
```

---

## Performance Tips

### 1. Query Specific Files
```bash
# BAD: Query all 128 files
zcat /da?_data/basemaps/gz/c2PtAbflPkgFullU*.s | grep ...

# GOOD: Calculate which file based on SHA
# Then query only that file
```

### 2. Use Correct Server
- `da0-da4` have different data subsets
- Use `/da?_data/` wildcard to search all

### 3. Cache Locally
```bash
# Cache filtered data once
zcat /da?_data/basemaps/gz/c2PtAbflPkgFullU*.s | \
  grep -f my_repos.txt > local_deps_cache.txt

# Query local cache (much faster)
grep "specific_repo" local_deps_cache.txt
```

### 4. Use Parallel Processing
```bash
# Process 32 files in parallel
for i in {0..31}; do
    (zcat /da?_data/basemaps/gz/a2cFullU$i.s | grep PATTERN > output$i.txt) &
done
wait
cat output*.txt > combined.txt
```

---

## Common Queries Cheat Sheet

### Get Commits for Repository
```bash
echo "owner_repo" | ~/lookup/getValues P2c
```

### Get Repository Dependencies
```bash
zcat /da?_data/basemaps/gz/c2PtAbflPkgFullU*.s | grep "owner_repo" | cut -d';' -f8-
```

### Get Commit Timestamp
```bash
echo "commit_sha" | ~/lookup/getValues c2ta | cut -d';' -f2
```

### Get Blob Content
```bash
echo "blob_sha" | ~/lookup/showCnt blob
```

### Find Code Sharing
```bash
echo "blob_sha" | ~/lookup/getValues b2P
```

### Get Author's Aliases
```bash
echo "Author Name <email>" | ~/lookup/getValues a2A
```

---

## Data Freshness

**WoC Version:** Currently V (some data U, S, T)  
**Update Frequency:** Monthly (target <1 quarter lag)  
**Coverage:** As of collection date

**Check Current Version:**
```bash
ssh da0
ls /da?_data/basemaps/gz/ | grep FullU | head -1
# Shows latest version letter
```

---

## For More Information

**Detailed Tutorials:**
- WoC Tutorial: https://github.com/woc-hack/tutorial
- WoC Docs: https://worldofcode.org/docs/#/

**Your Integration Docs:**
- `01_COMMIT_HISTORY_INTEGRATION.md` - How to use commit maps
- `02_DEPENDENCY_PATTERN_MINING.md` - How to use dependency maps
- `QUICKSTART.md` - 48-hour getting started guide
- `INTEGRATION_ROADMAP.md` - Phased implementation plan

---

## Bottom Line

**For pattern extraction, prioritize:**
1. **`P2c`** / **`c2dat`** - Commit history (evolution tracking)
2. **`c2PtAbflPkg`** - Dependencies (tech stack patterns)
3. **`b2tac`** - Code sharing (pattern diffusion)
4. **`A2c`** - Author networks (influence mapping)

Everything else is secondary for your use case.

**Start simple:** Phase 1 POC with `P2c` and `c2dat` only. Then expand if valuable.
