# Test Suite

## Quick Start

Run all tests with Docker Compose (recommended):

```bash
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

This automatically starts Neo4j, runs all tests, and cleans up.

## Test Categories

### Unit Tests (Mocked, Fast)
- `test_unit_integration.py` - Pattern-IDERule integration logic (9 tests)
- `test_config_validation.py` - Pydantic config validators (11 tests)
- `test_resource_cleanup.py` - Resource management (7 tests)

**Run locally:**
```bash
pytest pattern_extraction_pipeline/tests/ -v
```

**Requirements:** None (fully mocked)

### Integration Tests (Real APIs, Slow)
- `test_integration_scenarios.py` - Tests against real Neo4j, Gemini, GitHub
- `test_e2e.py` - Full end-to-end workflow

**Requirements:**
- Neo4j running (Docker Compose handles this)
- `GEMINI_API_KEY` in `.env`
- `GITHUB_TOKEN` in `.env`

## Manual Setup (Without Docker)

If you can't use Docker Compose:

```bash
# Start Neo4j
docker run -d --name neo4j-test -p 7687:7687 -p 7474:7474 \
  -e NEO4J_AUTH=neo4j/testpassword neo4j:5.15

# Set environment
export NEO4J_PASSWORD=testpassword
export GEMINI_API_KEY=your_key
export GITHUB_TOKEN=your_token

# Run tests
pytest pattern_extraction_pipeline/tests/ -v

# Cleanup
docker stop neo4j-test && docker rm neo4j-test
```

## Coverage Report

```bash
pytest pattern_extraction_pipeline/tests/ \
  --cov=pattern_extraction_pipeline \
  --cov-report=term-missing \
  --cov-report=html

# View report
start htmlcov/index.html  # Windows
open htmlcov/index.html   # macOS/Linux
```

**Current Coverage:** 35% (target: 45%+)

## Test Status

| Test File | Tests | Status | Speed |
|-----------|-------|--------|-------|
| test_unit_integration.py | 9 | PASSING | <1s |
| test_config_validation.py | 11 | PASSING | <1s |
| test_resource_cleanup.py | 7 | PASSING | <1s |
| test_integration_scenarios.py | TBD | Manual | 60s |
| test_e2e.py | TBD | Manual | 120s |
| **Total Unit Tests** | **27** | **ALL PASS** | **<2s** |

## Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| NEO4J_PASSWORD | Yes | - | Neo4j authentication |
| GEMINI_API_KEY | Yes | - | Gemini API access |
| GITHUB_TOKEN | Yes | - | GitHub API access |
| NEO4J_URI | No | bolt://localhost:7687 | Neo4j connection |
| NEO4J_USER | No | neo4j | Neo4j username |

## Common Issues

| Error | Solution |
|-------|----------|
| Module not found | Run `pip install -e .` from project root |
| Neo4j connection failed | Check NEO4J_PASSWORD is set |
| API quota exceeded | Wait for quota reset (24h) |
| Rate limit exceeded | Set GITHUB_TOKEN for 5000/hr limit |

---

Last updated: 2026-01-11 (trimmed from 321 to 95 lines)
