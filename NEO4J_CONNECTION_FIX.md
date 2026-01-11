# Neo4j Connection Issue - Root Cause & Prevention

**Date:** 2026-01-11  
**Issue:** UI failed to connect to Neo4j with "Timed out trying to establish connection to localhost:7687"  
**Status:** FIXED

---

## Root Cause

The system was trying to connect to the **wrong Neo4j instance** due to **multiple hardcoded defaults** that overrode the `.env` file configuration.

### Configuration Hierarchy (What We Had)

1. **`.env` file**: `NEO4J_URI=bolt://localhost:7688` (CORRECT - spec-engine-neo4j)
2. **`config.yaml`**: `uri: bolt://localhost:7687` (WRONG - plasticflower-neo4j)
3. **Python defaults**: `os.getenv("NEO4J_URI", "bolt://localhost:7687")` (WRONG)
4. **Pydantic defaults**: `uri: str = "bolt://localhost:7687"` (WRONG)

**Result:** config.yaml and Python defaults **overrode** the .env file, connecting to port 7687 (wrong database) instead of 7688 (correct database).

---

## Two Neo4j Databases

We have **two Neo4j instances** running:

| Container | Port | Purpose | Status |
|-----------|------|---------|--------|
| `plasticflower-neo4j` | 7687 | Other project | Running |
| `spec-engine-neo4j` | 7688 | Pattern extraction | Running (5,020 nodes) |

The pattern extraction UI should **only** connect to `spec-engine-neo4j` on port **7688**.

---

## Files Fixed

### 1. `config.yaml` (Line 25)
```yaml
# BEFORE
neo4j:
  uri: bolt://localhost:7687  # Wrong

# AFTER
neo4j:
  uri: bolt://localhost:7688  # spec-engine-neo4j (pattern extraction database)
```

### 2. `config_validator.py` (Line 47 + new __init__)
```python
# BEFORE
class Neo4jConfig(BaseModel):
    uri: str = "bolt://localhost:7687"  # Wrong default

# AFTER
class Neo4jConfig(BaseModel):
    uri: str = "bolt://localhost:7688"  # Correct default
    
    def __init__(self, **data):
        """Override URI from environment variable if set"""
        import os
        env_uri = os.getenv('NEO4J_URI')
        if env_uri:
            data['uri'] = env_uri  # Respect .env file
        super().__init__(**data)
```

### 3. `domain_selector_server.py` (Line 176)
```python
# BEFORE
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI", "bolt://localhost:7687"),  # Wrong

# AFTER
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI", "bolt://localhost:7688"),  # spec-engine-neo4j
```

### 4. `pattern_query_interface.py` (Line 21)
```python
# BEFORE
neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")  # Wrong

# AFTER
neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7688")  # spec-engine-neo4j
```

### 5. `health_check.py` (Line 26)
```python
# BEFORE
uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")  # Wrong

# AFTER
uri = os.getenv("NEO4J_URI", "bolt://localhost:7688")  # spec-engine-neo4j
```

### 6. `diagnose_neo4j.py` (Line 19)
```python
# BEFORE
uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")  # Wrong

# AFTER
uri = os.getenv("NEO4J_URI", "bolt://localhost:7688")  # spec-engine-neo4j
```

---

## Prevention Strategy

### 1. Environment Variables Take Priority

The config validator now checks `os.getenv('NEO4J_URI')` **first**, before using any YAML or hardcoded defaults.

**Priority order (now):**
1. Environment variable `NEO4J_URI` (from `.env`) - **HIGHEST PRIORITY**
2. `config.yaml` value
3. Pydantic default in `config_validator.py`
4. Python `os.getenv()` fallback - **LOWEST PRIORITY**

### 2. All Defaults Point to Correct Database

Changed all hardcoded defaults from `7687` to `7688` so even if `.env` is missing, it connects to the correct database.

### 3. Diagnostic Tool

Created `diagnose_neo4j.py` to quickly identify connection issues:

```bash
cd pattern_extraction_pipeline
python diagnose_neo4j.py
```

Outputs:
- Which URI is being used
- Whether NEO4J_PASSWORD is set
- Connection status
- Node count
- Troubleshooting steps if connection fails

---

## How To Verify Fix

```powershell
# 1. Check .env file
Get-Content pattern_extraction_pipeline\.env | Select-String "NEO4J_URI"
# Should show: NEO4J_URI=bolt://localhost:7688

# 2. Run diagnostic
cd pattern_extraction_pipeline
python diagnose_neo4j.py
# Should connect successfully to port 7688

# 3. Restart Flask server (if running)
# Stop with Ctrl+C, then:
python domain_selector_server.py
# Server will now connect to correct database

# 4. Test UI extraction
# Open http://localhost:8000/
# Run an extraction - should work without connection errors
```

---

## Summary

**Problem:** Multiple configuration sources with wrong defaults overrode the correct `.env` setting.

**Solution:** 
1. Fixed all hardcoded defaults (7687 → 7688)
2. Made environment variables take priority over config files
3. Added diagnostic tool for future debugging

**Result:** System now correctly connects to `spec-engine-neo4j` on port 7688.

**Prevention:** Environment variables (`NEO4J_URI` in `.env`) now have highest priority. All fallback defaults point to the correct database.

DONE.
