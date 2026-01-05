# Pattern Extraction Pipeline - File Index

Complete reference to all files in this directory.

## Core Implementation

### `pattern_extractor.py`
**Purpose:** Main extraction pipeline (GitHub → LLM → Neo4j)  
**Usage:** `python pattern_extractor.py`  
**Key Classes:**
- `PatternExtractor` - Main extraction class
  - `extract_patterns(query, limit)` - Batch extraction
  - `analyze_single_repo(repo_name)` - Single repo extraction
  - `store_pattern(pattern)` - Store in Neo4j

**Dependencies:** PyGithub, OpenAI, Neo4j

---

### `query_patterns.py`
**Purpose:** Query interface for pattern graph  
**Usage:** `python query_patterns.py`  
**Key Classes:**
- `PatternQuery` - Query class
  - `recommend_pattern(requirements)` - Get recommendations
  - `search_by_technology(tech_name)` - Find patterns by tech
  - `get_pattern_details(pattern_name)` - Full pattern info
  - `get_statistics()` - Graph stats

**Dependencies:** Neo4j

---

### `batch_extract.py`
**Purpose:** Extract 400+ patterns across multiple domains  
**Usage:** `python batch_extract.py`  
**Features:**
- Extract all domains (file managers, dashboards, APIs, data tools)
- Custom domain extraction
- Quick test mode (10 patterns per domain)
- Cost tracking and progress reporting

**Estimated Time:** 30-60 minutes for full corpus  
**Estimated Cost:** ~$4 for 400 patterns

---

## Testing

### `test_extraction.py`
**Purpose:** Test extraction pipeline  
**Usage:** `python test_extraction.py`  
**Options:**
1. Single repository extraction (microsoft/vscode)
2. Multiple repositories extraction (5 file managers)

**Use Case:** Validate extraction works before running batch

---

### `test_query.py`
**Purpose:** Test graph queries  
**Usage:** `python test_query.py`  
**Options:**
1. Dashboard requirements query (validates divergence detection)
2. Technology search (find patterns using specific tech)
3. Pattern details (full information about a pattern)
4. Graph statistics (check graph health)
5. Run all tests

**Use Case:** Validate graph is populated and queries work

---

## Setup & Configuration

### `setup.ps1`
**Purpose:** Automated setup for Windows (PowerShell)  
**Usage:** `.\setup.ps1`  
**Actions:**
- Checks Docker and Python installation
- Starts Neo4j container
- Installs Python dependencies
- Creates .env from template
- Provides next steps

**Time:** ~2 minutes

---

### `setup.sh`
**Purpose:** Automated setup for Linux/macOS (Bash)  
**Usage:** `./setup.sh`  
**Actions:** Same as setup.ps1

**Time:** ~2 minutes

---

### `requirements.txt`
**Purpose:** Python dependencies  
**Usage:** `pip install -r requirements.txt`  
**Packages:**
- PyGithub==2.1.1
- openai==1.12.0
- neo4j==5.16.0
- python-dotenv==1.0.1

---

### `env.template`
**Purpose:** Environment variable template  
**Usage:** Copy to `.env` and fill in credentials  
**Required Variables:**
- `GITHUB_TOKEN` - Get from https://github.com/settings/tokens
- `OPENAI_API_KEY` - Get from https://platform.openai.com/api-keys
- `NEO4J_URI` - Default: bolt://localhost:7687
- `NEO4J_USER` - Default: neo4j
- `NEO4J_PASSWORD` - Default: password

---

### `docker-compose.yml`
**Purpose:** Docker Compose configuration for Neo4j  
**Usage:** `docker-compose up -d`  
**Features:**
- Neo4j with APOC plugins
- Persistent volumes (data, logs, imports, plugins)
- Memory configuration (2GB heap, 1GB page cache)
- Auto-restart

**Alternative to:** `docker run` command in setup scripts

---

### `.gitignore`
**Purpose:** Ignore files for Git  
**Ignores:**
- Python cache files
- Virtual environments
- .env files (keep credentials secret!)
- IDE files
- Neo4j data directories
- Log files

---

## Documentation

### `README.md`
**Purpose:** Complete documentation  
**Contents:**
- Overview and architecture
- Cost and performance
- Requirements
- Quick start (Windows & Linux)
- Manual setup
- Usage examples
- Graph schema
- Advanced queries
- Troubleshooting
- Cost breakdown
- Roadmap
- Contributing

**Length:** ~500 lines  
**Read Time:** ~15 minutes

---

### `QUICK_START.md`
**Purpose:** Get running in 5 minutes  
**Contents:**
- Prerequisites checklist
- 5-minute setup steps
- Test commands
- Next steps
- Commands cheatsheet
- Cost tracking

**Length:** ~150 lines  
**Read Time:** ~5 minutes

---

### `INTEGRATION_GUIDE.md`
**Purpose:** Integrate with SPEC_Engine  
**Contents:**
- Commander integration (SPEC creation)
- Parameters TOML integration
- Pre-flight integration (execution validation)
- Feedback loop (continuous learning)
- Implementation checklist
- Testing
- Migration plan
- Troubleshooting

**Length:** ~400 lines  
**Read Time:** ~20 minutes  
**Target Audience:** SPEC_Engine developers

---

### `llm_prompt_template.md`
**Purpose:** LLM prompt documentation and customization  
**Contents:**
- Current prompt template
- Field descriptions
- Customization tips
- Domain-specific focus
- Testing prompts
- Best practices
- Common issues

**Length:** ~300 lines  
**Use Case:** Customize extraction behavior

---

### `INDEX.md`
**Purpose:** This file - complete file reference  
**Contents:** Summary of every file in the pipeline

---

## Supporting Files

### `.env` (not included, created by you)
**Purpose:** Your actual credentials  
**Created By:** Copying env.template  
**Never Commit:** Listed in .gitignore  
**Keep Secret:** Contains API keys

---

## Quick Reference

### New User Path
1. `README.md` - Understand the system
2. `QUICK_START.md` - Get it running
3. `test_extraction.py` - Test extraction
4. `test_query.py` - Test queries
5. `batch_extract.py` - Extract full corpus

### Developer Path
1. `README.md` - System architecture
2. `pattern_extractor.py` - Core implementation
3. `query_patterns.py` - Query implementation
4. `llm_prompt_template.md` - Customize extraction
5. `INTEGRATION_GUIDE.md` - Integrate with SPEC_Engine

### Troubleshooting Path
1. `QUICK_START.md` - Common issues
2. `README.md` (Troubleshooting section)
3. `docker logs spec-engine-graph` - Check Neo4j
4. http://localhost:7474 - Neo4j Browser

## File Statistics

- **Total Files:** 15
- **Code Files:** 5 (pattern_extractor.py, query_patterns.py, batch_extract.py, test_extraction.py, test_query.py)
- **Setup Files:** 4 (setup.ps1, setup.sh, requirements.txt, env.template, docker-compose.yml)
- **Documentation Files:** 6 (README.md, QUICK_START.md, INTEGRATION_GUIDE.md, llm_prompt_template.md, INDEX.md, .gitignore)
- **Total Lines:** ~3000+

## Dependencies Summary

**External Services:**
- GitHub API (free with token)
- OpenAI API (~$4 for 400 patterns)
- Neo4j (free Community Edition)

**Python Packages:**
- PyGithub (GitHub API client)
- openai (OpenAI API client)
- neo4j (Neo4j driver)
- python-dotenv (environment variables)

**Infrastructure:**
- Docker (for Neo4j)
- Python 3.8+

## Next Steps After Setup

1. **Test Extraction** - Run `test_extraction.py` to verify setup
2. **Test Queries** - Run `test_query.py` to verify graph works
3. **Extract 10 Patterns** - Small test batch (~$0.10)
4. **Validate Quality** - Check pattern extraction accuracy
5. **Extract Full Corpus** - Run `batch_extract.py` (~$4)
6. **Integrate with SPEC_Engine** - Follow `INTEGRATION_GUIDE.md`

## Support Resources

- **Setup Issues:** `QUICK_START.md` + `README.md` (Troubleshooting)
- **Usage Examples:** `README.md` (Usage section)
- **Customization:** `llm_prompt_template.md`
- **Integration:** `INTEGRATION_GUIDE.md`
- **Neo4j Queries:** http://localhost:7474 (Neo4j Browser)
- **Proposal Background:** `../_structureNewProposal.md`

## Version

**Version:** 1.0.0  
**Date:** 2 January 2026  
**Status:** Production Ready (POC)

## Changelog

- **v1.0.0** (2026-01-02):
  - Initial release
  - Core extraction pipeline
  - Query interface
  - Test suite
  - Full documentation
  - Setup automation
  - Docker support

Future versions will be documented here.
