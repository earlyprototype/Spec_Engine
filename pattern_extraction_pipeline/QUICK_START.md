# Quick Start Guide

Get the Pattern Extraction Pipeline running in 5 minutes.

## Prerequisites Checklist

- [ ] Docker installed and running
- [ ] Python 3.8+ installed
- [ ] GitHub account (for API token)
- [ ] Google Gemini API key (FREE)

## 5-Minute Setup

### Step 1: Start Neo4j (1 minute)

**Windows PowerShell:**
```powershell
docker run -d --name spec-engine-graph -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j
```

**Linux/macOS:**
```bash
docker run -d --name spec-engine-graph -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j
```

Verify: Open http://localhost:7474
- Username: `neo4j`
- Password: `password`

### Step 2: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment (2 minutes)

1. Copy template:
   ```bash
   cp env.template .env
   ```

2. Edit `.env`:
   - Get GitHub token: https://github.com/settings/tokens
   - Get Gemini key: https://aistudio.google.com/app/apikey
   - Paste into `.env`

### Step 4: Setup Data Quality (30 seconds)

```bash
python setup_data_quality.py
```

This creates unique constraints and normalization rules to prevent duplicate nodes.

**Expected output:**
```
[OK] Technology.name unique constraint created
[OK] Constraint.rule unique constraint created
[OK] Data Quality Setup Complete
```

### Step 5: Test Extraction (1 minute)

```bash
python test_extraction.py
```

Choose option 1 (single repo test).

**Expected output:**
```
✓ Extracted pattern: filesystem_browser
✓ Confidence: high
✓ Cost: ~$0.01
```

### Step 6: Test Query (30 seconds)

```bash
python test_query.py
```

Choose option 1 (Dashboard query).

**Expected output:**
```
Recommendations:
1. filesystem_browser (confidence: high)
   Stars: 50000+
   Source: https://github.com/microsoft/vscode
```

## You're Done!

Now you can:
- **Expand corpus:** `python batch_extract_domains.py` (extract 100+ patterns)
- **Query patterns:** `python pattern_query.py` (programmatic interface)
- **View graph:** See `GRAPH_VIEWING_GUIDE.md`
- **Integrate with SPECs:** See `INTEGRATION_GUIDE.md`

## Next Steps

### Extract 400 Patterns (30-60 minutes, $4)

```bash
python batch_extract.py
```

Choose option 1 (extract all domains).

### Query for Recommendations

```python
from query_patterns import PatternQuery

query = PatternQuery()

results = query.recommend_pattern({
    'type': 'data_management',
    'domain': 'file_system'
})

for r in results:
    print(f"{r['pattern']} - {r['stars']} stars")
    print(f"  {r['source']}")
```

### Custom Extraction

```python
from pattern_extractor import PatternExtractor

extractor = PatternExtractor()

# Extract authentication patterns
auth_patterns = extractor.extract_patterns(
    "topic:authentication stars:>5000",
    limit=50
)
```

## Troubleshooting

### "Docker not found"
- Install Docker Desktop: https://www.docker.com/products/docker-desktop
- Make sure Docker is running

### "Neo4j connection failed"
- Wait 30 seconds after starting Docker container
- Check: `docker ps | grep spec-engine-graph`
- Restart: `docker restart spec-engine-graph`

### "GitHub rate limit"
- Make sure GITHUB_TOKEN is in `.env`
- Check rate limit: https://github.com/settings/tokens

### "Gemini API error"
- Verify GEMINI_API_KEY in `.env`
- Check quota: https://aistudio.google.com/app/apikey
- Regenerate key if authentication fails

## Commands Cheatsheet

```bash
# Start Neo4j
docker start spec-engine-graph

# Stop Neo4j
docker stop spec-engine-graph

# View Neo4j logs
docker logs spec-engine-graph

# Neo4j Browser
# http://localhost:7474

# Test single extraction
python test_extraction.py

# Test queries
python test_query.py

# Batch extract (400 patterns)
python batch_extract.py

# Custom extraction
python pattern_extractor.py
```

## File Reference

- `pattern_extractor.py` - Main extraction pipeline (with normalization)
- `setup_data_quality.py` - Data quality setup & cleanup
- `query_patterns.py` - Query interface
- `test_extraction.py` - Test extraction
- `test_query.py` - Test queries
- `batch_extract.py` - Extract 400+ patterns
- `.env` - Your API keys (keep secret!)
- `README.md` - Full documentation
- `DATA_QUALITY.md` - Data quality documentation

## Cost Tracking

Using Google Gemini API (FREE tier):
- Single repo test: FREE
- 10 repos: FREE
- 100 repos: FREE
- 400 repos (full corpus): FREE

*Subject to Gemini's free tier rate limits*

## Support

Stuck? Check:
1. This file (common issues above)
2. `README.md` (full documentation)
3. `llm_prompt_template.md` (prompt customization)
4. Neo4j Browser (http://localhost:7474) for graph visualization
