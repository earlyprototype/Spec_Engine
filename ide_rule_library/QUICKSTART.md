# Quick Start: IDE Rule Library Scanner

**Ready to scan your 534 Pattern repositories for IDE rule files!**

---

## Step 1: Test Connections

```powershell
cd ide_rule_library
python test_connection.py
```

**Expected output:**
```
✓ Connected to Neo4j
✓ Found 534 Pattern nodes
✓ Authenticated with GitHub
✓ API calls remaining: 5000/5000
```

---

## Step 2: Quick Test (First 10 Repos)

```powershell
python scan_existing_patterns.py --max 10
```

**This will:**
- Scan first 10 high-star repositories
- Show which rule files are found
- Take ~1 minute
- Save results to `scan_results.json`

**Example output:**
```
[1/10] electron_desktop_app
  Repo: https://github.com/electron/electron
  Stars: 113,000
  ✓ Found 2 rule file(s):
    - .cursorrules (P1)
    - .vscode/settings.json (P2)

[2/10] react_dashboard_pattern
  Repo: https://github.com/facebook/react
  Stars: 220,000
  ✓ Found 1 rule file(s):
    - .github/copilot-instructions.md (P1)

...

SCAN SUMMARY
====================
Total patterns scanned:     10
Repos with IDE rule files:  3
Success rate:               30.0%
Total rule files found:     5

Most Common Formats:
  .cursorrules: 2 repos
  .github/copilot-instructions.md: 1 repo
  .vscode/settings.json: 1 repo
```

---

## Step 3: Full Scan (All 534 Repos)

```powershell
python scan_existing_patterns.py
```

**This will:**
- Scan all 534 Pattern repositories
- Find repos with IDE rule files (statistics determined by scan)
- Take ~10-15 minutes with GitHub token
- Save complete results to `scan_results.json`

**Example output:**
```
Total patterns scanned:     534
Repos with IDE rule files:  [Determined by scan]
Total rule files found:     [Determined by scan]
Success rate:               [Calculated after scan]

Most Common Formats:
  [Statistics generated from actual scan results]
```

---

## Step 4: Review Results

```powershell
# View scan results
code scan_results.json

# Or read in terminal
python -m json.tool scan_results.json | more
```

**Results include:**
- Total statistics
- Format breakdown
- Priority distribution
- List of all repos with rules found
- Specific file paths discovered

---

## What Happens Next

After scanning, you can:

1. **Extraction (Now Available):**
   ```powershell
   python scan_existing_patterns.py --extract
   ```
   - Fetches actual file content
   - Analyzes with Gemini
   - Stores as IDERule nodes in Neo4j
   - Generates embeddings for semantic search

2. **Rule Generation (Now Available):**
   ```powershell
   python generate_cursorrules.py "Build a dashboard" --tech typescript react --type web_app
   ```
   - Queries IDERule nodes semantically
   - Synthesizes tailored `.cursorrules` for your project
   - Based on proven patterns from high-star repos

3. **SPEC Integration (Future):**
   - Commander queries IDE rules during SPEC generation
   - Auto-generates `.cursorrules` for new projects
   - Pattern + IDE rules = complete project setup

---

## Troubleshooting

### Connection Test Fails

**Neo4j not found:**
```powershell
docker ps | grep neo4j
# Should show spec-engine-neo4j running
```

**GitHub token missing:**
- Get token: https://github.com/settings/tokens
- Add to `.env`: `GITHUB_TOKEN=ghp_your_token_here`
- Scope needed: `repo:public_repo`

### Scan Errors

**"Repository not found"**
- Repo is private or deleted
- Scanner continues to next repo
- Normal - some patterns may reference old repos

**"API rate limit exceeded"**
- Without token: 60/hour limit
- With token: 5000/hour limit
- Wait 1 hour or add GitHub token

---

## Files Created

After running scanner:

```
ide_rule_library/
├── scan_results.json          ← Scan results
├── scan_existing_patterns.py  ← Scanner script
├── test_connection.py         ← Connection tester
├── README.md                  ← Full documentation
├── QUICKSTART.md              ← This file
└── RESEARCH_REPORT_JAN_2026.md ← Complete research
```

---

## Ready to Go!

```powershell
# 1. Test connections
python test_connection.py

# 2. Quick test (10 repos)
python scan_existing_patterns.py --max 10

# 3. Full scan (534 repos)
python scan_existing_patterns.py
```

**Time investment:** ~15 minutes total  
**Result:** Know exactly which of your 534 repos have IDE rule files!

---

**Questions?** See README.md for detailed documentation.
