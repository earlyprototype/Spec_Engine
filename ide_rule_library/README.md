# IDE Rule Library - Enhanced Quality System

**A production-ready system for discovering, scoring, and serving high-quality IDE coding rules from vetted GitHub repositories.**

**Status:** Production Ready | Quality-Enabled  
**Version:** 2.0 (Enhanced)  
**Last Updated:** 8 January 2026

---

## What This System Does

Prevents **cargo culting** by filtering coding rules based on repo quality, not just popularity.

### The Problem
Popular repos (high stars) aren't always good sources:
- Abandoned projects with outdated patterns
- No tests, CI/CD, or production usage
- One-person hobby projects vs battle-tested codebases
- Marketing hype vs actual quality

### The Solution
**7-Factor Quality Scoring** that evaluates:
1. **Star Velocity** - Growth rate, not just total stars
2. **Freshness** - Active maintenance (updated recently)
3. **Issue Health** - Maintainer responsiveness
4. **Contributor Diversity** - Not a one-person show
5. **Production Signals** - CI/CD, Docker, tests, monitoring
6. **Documentation** - README, contributing guides, changelogs
7. **Usage Signal** - Fork ratio (actual usage)

**Result:** Query by quality, get rules from sources you can trust.

---

## Quick Start

### Prerequisites

```bash
pip install PyGithub neo4j python-dotenv google-generativeai tenacity pyyaml
```

### Environment Setup

Create `.env`:
```bash
# GitHub API (required for repo scanning)
GITHUB_TOKEN=ghp_your_token_here

# Neo4j Database (required)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# Gemini API (required for rule extraction)
GEMINI_API_KEY=your_gemini_key_here
```

### Database Setup

```bash
# Create indexes and schema
python setup_database_v2.py
```

### Validate System Health

```bash
# Check all connections and configuration
python validate_system.py
```

---

## Core Workflows

### 1. Scan & Extract Rules from GitHub

```bash
# Scan repositories for IDE rule files (28 formats)
python scan_existing_patterns.py

# Extract rules with Gemini analysis + embeddings
python scan_existing_patterns.py --extract

# Limit to first 50 repos for testing
python scan_existing_patterns.py --extract --max 50
```

**What gets extracted:**
- Rule content
- Gemini-powered analysis (purpose, categories, practices)
- Context metadata (tech stack, project type, team size)
- Semantic embeddings for similarity search

### 2. Calculate Quality Scores

```bash
# Migrate quality scores for all repos
python migrate_quality_scores.py

# Analyze quality score distribution
python quality_analysis.py

# Estimate API costs before migration
python estimate_costs.py
```

**Quality metrics fetched:**
- Stars, forks, contributors
- Creation & update timestamps
- Open/closed issues
- File tree (CI/CD, tests, Docker)
- README size

### 3. Generate Contextual Rules

```bash
# Generate .cursorrules for your project
python generate_cursorrules_v2.py "Build a Python FastAPI backend" \
  --tech python fastapi postgresql \
  --type api \
  --size medium \
  --team small \
  --output .cursorrules \
  --min-quality 60 \
  --min-confidence 3
```

**Smart features:**
- Semantic search (finds relevant rules by meaning)
- Quality filtering (only high-quality sources)
- Context matching (project size, team size, tech stack)
- Graceful degradation (relaxes filters if needed)
- Confidence disclaimers (warns about AI-inferred context)

---

## System Architecture

### Data Flow

```
GitHub Repos
    ↓ (scan_existing_patterns.py)
Rule Files Discovered
    ↓ (enhanced_rule_extractor.py + Gemini)
Analyzed Rules + Embeddings
    ↓ (neo4j_writer.py)
Neo4j Database (IDERule nodes)
    ↓ (migrate_quality_scores.py + GitHub API)
Quality Scores Added
    ↓ (enhanced_query_engine.py)
Semantic Search + Quality Filtering
    ↓ (generate_cursorrules_v2.py)
Contextual .cursorrules Generated
```

### Neo4j Schema

```cypher
// IDERule nodes with quality metadata
(r:IDERule {
    // Identity
    id: string,                    // "owner/repo:file_path"
    source_repo: string,           // GitHub URL
    file_path: string,             // Path in repo
    file_format: string,           // ".cursorrules", "CLAUDE.md", etc.
    content_hash: string,          // Deduplication
    
    // Content
    content: string,               // Full rule text
    
    // Gemini Analysis
    purpose: string,               // What these rules do
    categories: [string],          // ["testing", "architecture"]
    key_practices: [string],       // Main practices
    reasoning: string,             // Why follow these
    
    // Context (AI-inferred)
    technologies: [string],        // ["python", "fastapi"]
    project_types: [string],       // ["api", "web_app"]
    ide_types: [string],           // ["cursor", "vscode"]
    
    // Quality Metadata
    quality_score: float,          // 0-100 composite score
    quality_breakdown_json: string, // JSON of 7 factors
    confidence_level: int,         // 1-5 confidence
    
    // Production Signals
    has_ci_cd: boolean,
    has_deployment: boolean,
    has_tests: boolean,
    has_monitoring: boolean,
    has_security: boolean,
    
    // Timestamps
    extracted_date: datetime,
    quality_migrated_at: datetime,
    
    // Semantic Search
    embedding: list<float>         // 768-dim vector (Gemini)
})

// Vector index for similarity search
CREATE VECTOR INDEX ide_rule_embeddings 
FOR (r:IDERule) ON r.embedding
OPTIONS {indexConfig: {`vector.dimensions`: 768, `vector.similarity_function`: 'cosine'}}
```

---

## Core Components

### 1. Scanning & Extraction

**`scan_existing_patterns.py`**
- Scans GitHub repos for 28 rule file formats
- Uses tree API for efficiency (1 API call vs 100+)
- Handles rate limiting, retries, errors
- Checkpointing for resume capability

**`enhanced_rule_extractor.py`**
- Gemini-powered analysis of rule content
- Extracts context (tech, project type, team size)
- Adds confidence disclaimers for AI-inferred data
- Generates semantic embeddings
- Retry logic for API failures

**`neo4j_writer.py`**
- Writes to Neo4j with duplicate detection
- Content hashing for deduplication
- Batch processing for efficiency

### 2. Quality Scoring

**`quality_scorer.py`**
- 7-factor composite scoring (0-100)
- Defensive handling of missing data
- Normalized scores across factors
- Production signal detection

**`migrate_quality_scores.py`**
- Fetches fresh GitHub data for all repos
- Calculates quality scores
- Updates IDERule nodes in bulk
- Progress tracking + checkpointing

**`quality_analysis.py`**
- Analyzes quality score distribution
- Calculates percentile thresholds
- Generates statistics

### 3. Query & Generation

**`enhanced_query_engine.py`**
- Semantic search using vector embeddings
- Quality-based filtering
- Context matching (tech, type, size)
- Graceful degradation (relaxes filters)
- v1 fallback for backwards compatibility

**`generate_cursorrules_v2.py`**
- CLI for generating contextual rules
- Query with filters (quality, confidence, tech)
- Gemini-powered synthesis of multiple rules
- Adds disclaimers for AI-inferred context

### 4. Utilities

**`validate_system.py`**
- Health checks (Neo4j, Gemini, indexes)
- Configuration validation
- Quality data status check

**`estimate_costs.py`**
- Projects Gemini API costs
- Estimates GitHub API usage
- Cost breakdowns by operation

**`logger.py`**
- Structured JSON logging
- Correlation IDs for tracing
- Configurable log levels

**`retry_handler.py`**
- Exponential backoff for Gemini API
- Handles quota exceeded, timeouts
- Configurable retry strategies

**`exceptions.py`**
- Custom exception hierarchy
- Specific error types for better handling

---

## Rule File Formats Supported (28 Total)

### Priority 1 (Most Common)
- `.cursorrules` - Cursor IDE
- `.github/copilot-instructions.md` - GitHub Copilot
- `AGENTS.md` / `AGENT.md` - Emerging standard
- `AI.md` - Generic vendor-neutral
- `CLAUDE.md` - Anthropic Claude
- `GEMINI.md` - Google Gemini CLI
- `INSTRUCTIONS.md` - Generic
- `CODING.md` - Coding standards

### Priority 2 (Specialized)
- `.cursor/rules/*.mdc` - Cursor project rules
- `.windsurfrules` - Windsurf/Codeium
- `.agent/rules/*.md` - Google Antigravity
- `.vscode/settings.json` - VS Code AI
- `.ai/` - Centralized AI instructions
- `.ai-rulez/` - Multi-tool config

### Priority 3 (Contextual)
- `.aider.conf.yml` - Aider CLI
- `.sourcegraph/**/*.rule.md` - Sourcegraph
- `.clinerules/project.md` - Cline
- `.aiconfig` - AIConfig framework
- `.idea/workspace.xml` - JetBrains

---

## Quality Scoring Details

### 7 Factors (0-100 Scale)

1. **Star Velocity** (20 points)
   - `stars_per_year / 1000 * 20`
   - Measures growth, not just popularity
   - 1000 stars/year = full score

2. **Freshness** (20 points)
   - Updated in last 30 days: 20
   - Last 90 days: 15
   - Last 180 days: 10
   - Last 365 days: 5
   - Older: 0

3. **Issue Health** (15 points)
   - `closed_issues / total_issues * 15`
   - Shows maintainer responsiveness
   - 100% closed = full score

4. **Contributor Diversity** (15 points)
   - 50+ contributors: 15
   - 20-49: 12
   - 10-19: 9
   - 5-9: 6
   - 2-4: 3
   - 1: 0.75

5. **Production Readiness** (20 points)
   - Detects: CI/CD, Docker, tests, monitoring, security
   - 5 points per category detected
   - Max 20 points

6. **Documentation** (5 points)
   - README, CONTRIBUTING, CHANGELOG, docs/
   - 1 point per indicator

7. **Usage Signal** (5 points)
   - `(forks / stars * 100) / 200 * 5`
   - High fork ratio = people use it

### Confidence Levels (1-5)

- **5** - Perfect data, production signals, high activity
- **4** - Good data, some signals (default for quality > 1000 stars)
- **3** - Decent data, basic metrics
- **2** - Limited data, estimates used
- **1** - Minimal data, low confidence

---

## API Usage & Rate Limits

### GitHub API

**Without Token:** 60 requests/hour  
**With Token:** 5,000 requests/hour

**Per-repo costs:**
- Basic scan: 1 call (tree API)
- Quality scoring: 4 calls (repo, contributors, tree, readme)

**Example:**
- Scan 72 repos: 72 calls (~1 minute)
- Quality score 72 repos: 288 calls (~3 minutes)

### Gemini API

**Embedding model:** `text-embedding-004`  
**Cost:** $0.00001 per 1000 tokens

**Per-rule costs:**
- Extraction: ~$0.001 per rule
- Synthesis: ~$0.01 per query

**Example:**
- Extract 100 rules: ~$0.10
- Generate 1000 .cursorrules: ~$10

---

## Configuration

### `config.yaml`

```yaml
# Gemini API Settings
gemini:
  model: gemini-2.0-flash-exp
  embedding_model: models/text-embedding-004
  temperature: 0.7
  max_tokens: 2000

# Neo4j Settings
neo4j:
  vector_index_name: ide_rule_embeddings
  batch_size: 100

# Logging
logging:
  level: INFO
  format: json
  output: logs/

# Query Defaults
query:
  default_top_k: 15
  min_quality_score: 60.0
  min_confidence: 3
  max_days_since_update: 180

# Rule File Priorities
rule_formats:
  priority_1: [.cursorrules, CLAUDE.md, AGENTS.md]
  priority_2: [.cursor/rules/*.mdc, .windsurfrules]
  priority_3: [.aider.conf.yml, .aiconfig]
```

---

## Testing & Validation

### System Health Check

```bash
python validate_system.py
```

Checks:
- Neo4j connectivity
- Database indexes
- Gemini API access
- Quality data status
- Configuration validity

### Integration Tests

```bash
cd tests
python test_integration_enhanced.py
python test_real_integration.py
```

**Coverage:**
- Rule extraction
- Quality scoring
- Query engine
- Graceful degradation
- Backwards compatibility

---

## Current Status (8 Jan 2026)

### Database Stats
- **Repositories**: 72 unique repos scanned
- **Rules**: 171 IDERule nodes
- **Quality Scores**: 100% coverage
- **Score Range**: 22.0 - 56.2 / 100
- **Average Quality**: 43.1 / 100

### System Features
- ✅ Rule extraction with Gemini analysis
- ✅ Quality scoring (7 factors)
- ✅ Semantic search (vector embeddings)
- ✅ Quality-based filtering
- ✅ Graceful degradation
- ✅ Context matching
- ✅ Cost estimation
- ✅ System validation
- ✅ Migration tools
- ✅ Integration tests

### What Works
1. **Discovery** - Scans 28 rule formats across GitHub
2. **Extraction** - Gemini analysis + embeddings
3. **Scoring** - Real GitHub metrics → quality scores
4. **Filtering** - Query by quality, tech, context
5. **Generation** - Synthesize contextual .cursorrules
6. **Validation** - Health checks, cost estimates

---

## Documentation

- **`README.md`** (this file) - Complete system overview
- **`QUICKSTART.md`** - Step-by-step guide
- **`ENHANCED_SYSTEM_GUIDE.md`** - Deep dive into enhanced features
- **`MIGRATION_GUIDE.md`** - Upgrading from v1 to v2
- **`QUICK_REFERENCE.md`** - Common commands
- **`METRICS_EXPLAINED.md`** - Quality scoring details
- **`FINAL_TEST_RESULTS.md`** - Test results and proof
- **`RESEARCH_REPORT_JAN_2026.md`** - Market research

---

## Files Overview

### Core System (11 files)
- `enhanced_query_engine.py` - Semantic search + quality filtering
- `enhanced_rule_extractor.py` - Gemini analysis + embeddings
- `generate_cursorrules_v2.py` - Rule generation CLI
- `quality_scorer.py` - 7-factor scoring system
- `migrate_quality_scores.py` - Quality data migration
- `quality_analysis.py` - Score distribution analysis
- `estimate_costs.py` - API cost projection
- `validate_system.py` - Health checks
- `retry_handler.py` - API retry logic
- `exceptions.py` - Custom error types
- `setup_database_v2.py` - Database schema

### Scanning & Ingestion (5 files)
- `scan_existing_patterns.py` - GitHub scanner
- `neo4j_writer.py` - Database writer
- `rate_limiter.py` - Rate limit handling
- `monitor.py` - Progress monitoring
- `progress_tracker.py` - Checkpointing

### Configuration (3 files)
- `config.yaml` - System configuration
- `logger.py` - Structured logging
- `.env` - Environment variables (you create this)

---

## Next Steps

### For Production Use

1. **Expand Coverage**
   - Scan more repos (currently 72)
   - Add file scanning for production signals (+20-25 pts)
   - Track usage patterns

2. **Improve Filtering**
   - Lower default thresholds (quality >= 30)
   - Better technology tagging
   - Project size inference

3. **Add Intelligence**
   - Track which rules get queried
   - Learn from user feedback
   - Auto-update quality scores (weekly)

4. **Scale**
   - Background workers for scanning
   - Cache layer for expensive ops
   - Analytics dashboard

### For Research

See the comprehensive strategy above for:
- Multi-dimensional scoring
- Smart prioritization
- Continuous maintenance
- Metrics tracking

---

## Support & Issues

**GitHub Rate Limits:** Use `GITHUB_TOKEN` for 5000/hour  
**Gemini API:** Get key from https://aistudio.google.com/  
**Neo4j:** Install from https://neo4j.com/download/

**Common Issues:**
- "No quality data" → Run `migrate_quality_scores.py`
- "Vector index missing" → Run `setup_database_v2.py`
- "No results found" → Lower quality thresholds or use fallback

---

**Created:** 7 January 2026  
**Enhanced:** 8 January 2026  
**Status:** Production Ready  
**Anti-Cargo-Culting:** Operational ✓
