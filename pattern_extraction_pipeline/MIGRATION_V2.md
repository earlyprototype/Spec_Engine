# Migration Guide: Pattern-Rule Integration V2

## Overview

This guide covers upgrading to the refactored Pattern-Rule Integration V2, which addresses critical production issues and adds proper package management, error handling, observability, and testing infrastructure.

## What Changed

### Major Improvements

1. **Proper Package Structure** - No more sys.path hacks, proper `setup.py` installation
2. **Config Validation** - Pydantic validation catches errors before runtime
3. **Error Handling** - Specific exceptions, rate limiting, graceful degradation
4. **Real Tests** - Integration tests with real APIs, not just mocks
5. **Observability** - Metrics collection, structured logging, health checks
6. **Resource Management** - Fixed Neo4j stream leaks
7. **Backwards Compatibility** - Feature flags for gradual rollout

## Breaking Changes

### 1. Import Paths

**Before (V1):**
```python
# sys.path hacking
sys.path.append('../ide_rule_library')
from enhanced_rule_extractor import EnhancedRuleExtractor
```

**After (V2):**
```python
# Proper package imports
from ide_rule_library.enhanced_rule_extractor import EnhancedRuleExtractor
```

**Action Required:** Update all imports to use full package paths.

### 2. Configuration

**Before (V1):**
```python
# Raw dict, no validation
with open('config.yaml') as f:
    config = yaml.safe_load(f)
```

**After (V2):**
```python
# Validated with Pydantic
from pattern_extraction_pipeline.config_validator import validate_config_file
config = validate_config_file('config.yaml')
```

**Action Required:** Configuration will now fail fast on errors. Fix any invalid config values.

### 3. Model Name Configuration

**Before (V1):**
```python
# Hardcoded in multiple places
self.llm = genai.GenerativeModel('gemini-2.5-flash')
```

**After (V2):**
```python
# Centralized in config.yaml
self.llm = genai.GenerativeModel(self.config.gemini.model_name)
```

**Action Required:** Ensure `config.yaml` has `gemini.model_name` set.

## Migration Steps

### Step 1: Install as Package

**Option A: Development Mode (Recommended)**
```bash
# From project root
pip install -e .
```

**Option B: Regular Installation**
```bash
pip install .
```

**Verify:**
```bash
python -c "from pattern_extraction_pipeline import PatternExtractor; print('OK')"
python -c "from ide_rule_library import EnhancedRuleExtractor; print('OK')"
```

### Step 2: Update Configuration

Ensure your `config.yaml` includes all required fields:

```yaml
rule_extraction:
  enabled: true
  max_file_size: 100000
  file_patterns:
    - .cursorrules
    - .aiderules
    - CLAUDE.md

gemini:
  api_key_env: GEMINI_API_KEY
  model_name: gemini-2.5-flash  # REQUIRED
  max_retries: 3

neo4j:
  uri: bolt://localhost:7687
  user: neo4j
  password_env: NEO4J_PASSWORD

github:
  token_env: GITHUB_TOKEN
  max_repos_per_query: 100
  rate_limit_pause: 60
```

**Validate:**
```bash
python -c "from pattern_extraction_pipeline.config_validator import validate_config_file; validate_config_file('pattern_extraction_pipeline/config.yaml'); print('Config valid')"
```

### Step 3: Health Check

Run the health check to verify all services:

```bash
cd pattern_extraction_pipeline
python health_check.py
```

Expected output:
```
[+] neo4j              : Connected to bolt://localhost:7687
[+] gemini_api         : API key valid, model responsive
[+] github_api         : Authenticated as yourusername, rate limit: 4998 requests remaining
[+] ide_rule_library   : IDE Rule Library available and importable

Status: HEALTHY - All core services operational
```

### Step 4: Update Code

Update any custom scripts that import or use the pipeline:

**Before:**
```python
from pattern_extractor import PatternExtractor

extractor = PatternExtractor()
```

**After:**
```python
from pattern_extraction_pipeline import PatternExtractor

extractor = PatternExtractor(config_path='config.yaml')
# Config is now automatically validated
```

### Step 5: Test Integration

Run the real integration tests:

```bash
cd pattern_extraction_pipeline/tests
pytest test_real_integration.py -v
```

**Note:** These tests use real APIs and Neo4j. Ensure you have:
- `TEST_NEO4J_URI` set (or uses default: `bolt://localhost:7688`)
- Valid API keys in `.env`

### Step 6: Gradual Feature Rollout

If upgrading production, use feature flags for gradual rollout:

```yaml
# Start with rule extraction disabled
rule_extraction:
  enabled: false  # <-- Set to false initially

# Enable on a subset of extractions first
# Monitor metrics and logs
# Then set to true when confident
```

Check feature flags programmatically:

```python
from pattern_extraction_pipeline.feature_flags import is_feature_enabled

if is_feature_enabled(config, 'rule_extraction.enabled', default=False):
    # Extract rules
    pass
```

## New Features

### Metrics Collection

Track extraction performance:

```python
extractor = PatternExtractor()
# After extraction
report = extractor.metrics.get_report()
print(f"Rules extracted: {report['counters']['rules_extracted']}")
print(f"Average extraction time: {report['timers']['rule_extraction']['avg_seconds']:.2f}s")
```

### Rate Limiting

Automatic rate limiting prevents quota exhaustion:

```python
# Rate limiter is automatically initialized
# Default: 15 calls per minute for Gemini free tier

# Check stats
stats = extractor.gemini_rate_limiter.get_stats()
print(f"Total waits: {stats['total_waits']}")
print(f"Total wait time: {stats['total_wait_time_seconds']}s")
```

### Health Checks

Programmatic health checks:

```python
from pattern_extraction_pipeline.health_check import check_health

health = check_health(verbose=True)
if not health['healthy']:
    print("System unhealthy:")
    for name, check in health['checks'].items():
        if not check['ok']:
            print(f"  - {name}: {check['message']}")
```

## Rollback Procedure

If you encounter issues, rollback to V1:

### 1. Revert Code Changes
```bash
git checkout <previous-commit>
```

### 2. Uninstall Package
```bash
pip uninstall ai-specs
```

### 3. Reinstall Dependencies
```bash
pip install -r pattern_extraction_pipeline/requirements.txt
pip install -r ide_rule_library/requirements.txt
```

### 4. Restore sys.path hacks (if needed)
```python
import sys
sys.path.append('../ide_rule_library')
```

## Testing Checklist

Before deploying to production:

- [ ] All imports work without sys.path modifications
- [ ] Health check passes
- [ ] Config validation passes
- [ ] Integration tests pass
- [ ] Metrics are being collected
- [ ] Rate limiter prevents quota exhaustion
- [ ] No Neo4j resource leaks (check `SHOW TRANSACTIONS`)
- [ ] Feature flags can enable/disable rule extraction
- [ ] Logs show structured output with proper error messages

## Troubleshooting

### "Module not found" errors

**Problem:** Can't import `pattern_extraction_pipeline` or `ide_rule_library`

**Solution:**
```bash
# Install as editable package
pip install -e .

# Or add to PYTHONPATH (temporary)
export PYTHONPATH="${PYTHONPATH}:/path/to/project"
```

### Config validation fails

**Problem:** `ValidationError` when loading config

**Solution:**
- Check all required fields are present
- Validate YAML syntax (use `yamllint`)
- Check data types (e.g., `max_file_size` should be int, not string)
- Review error message for specific field causing issue

### Health check fails

**Problem:** Health check reports unhealthy services

**Solution:**
- **Neo4j:** Check Neo4j is running (`systemctl status neo4j` or Docker)
- **Gemini:** Verify `GEMINI_API_KEY` in `.env`, check quota on [Google AI Studio](https://aistudio.google.com/)
- **GitHub:** Verify `GITHUB_TOKEN` in `.env`, check token has required scopes

### Tests fail

**Problem:** Integration tests fail

**Solution:**
- Ensure test Neo4j instance is running (separate from production)
- Check test API keys are valid
- Review test output for specific assertion failures
- Check if rate limits were hit (tests use real APIs)

## Support

For issues or questions:
1. Check [PATTERN_RULE_INTEGRATION_COMPLETE.md](./PATTERN_RULE_INTEGRATION_COMPLETE.md) for design details
2. Review test files in `tests/` for usage examples
3. Run health check and share output
4. Check logs for detailed error messages

## Version History

- **V2.0** - Production-ready refactor (this version)
- **V1.0** - Initial pattern-rule integration (deprecated)
