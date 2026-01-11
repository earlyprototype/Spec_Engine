# Migration Guide: Enhanced Quality System

**Date:** 8 January 2026  
**Version:** 2.0  
**Status:** Production Ready (requires migration)

---

## Overview

The enhanced quality system is production-ready but requires a one-time migration to backfill quality scores for existing rules.

## Breaking Changes

### 1. Quality Scores Required

**Change:** Enhanced query engine expects `quality_score` property on IDERule nodes.

**Impact:** Queries will fall back to v1 (no quality filtering) if quality data missing.

**Fix:** Run migration script (see below).

### 2. New Query Parameters

**Change:** `query_rules()` now accepts quality filter parameters.

**Old:**
```python
rules = engine.query_rules(query="Python API", top_k=15)
```

**New (with defaults):**
```python
rules = engine.query_rules(
    query="Python API",
    min_quality_score=60.0,      # Optional, defaults to 60
    min_confidence=3,             # Optional, defaults to 3
    require_production_signals=True,  # Optional, defaults to True
    top_k=15
)
```

**Backwards Compatible:** All quality parameters are optional. If omitted and no quality data exists, system falls back to v1 behaviour.

### 3. Context Inference Disclaimers

**Change:** Context fields (project_sizes, team_sizes) now marked as AI-inferred.

**Impact:** Generated .cursorrules files include disclaimers that context is best guess, not validated.

**No Action Required:** Automatic in v2 generator.

---

## Migration Steps

### Step 1: Validate System Health

Check that all components are working:

```powershell
python validate_system.py
```

Expected output:
```
[OK] Environment Variables: All required environment variables present
[OK] Config File: Config file valid
[OK] Required Files: All 10 required files present
[OK] Neo4j Connection: Neo4j connection successful
[OK] Neo4j Indexes: Found X indexes including vector index
[OK] Database Content: Found 171 rules (0 with quality scores)
[WARNING] No rules have quality scores (run migrate_quality_scores.py)
[OK] Gemini API: Gemini API working

STATUS: System is ready for production use
```

### Step 2: Estimate Migration Cost

Check what the migration will cost:

```powershell
python estimate_costs.py --operation migration
```

Expected output:
```
MIGRATION ESTIMATE
Rules to migrate: 171
API calls: 0 (uses cached data)
Gemini cost: $0.00
Estimated time: 8.6 minutes

Migration uses cached repo data from Neo4j (no API calls, no cost)
```

### Step 3: Dry Run Migration

Test migration on first 3 rules:

```powershell
python migrate_quality_scores.py --dry-run
```

Review output to ensure quality scores are calculated correctly.

### Step 4: Run Full Migration

Migrate all 171 rules:

```powershell
python migrate_quality_scores.py --batch-size 10
```

Progress will be checkpointed every 10 rules. If interrupted, re-run the same command to resume.

Expected output:
```
[1/171] Processing repo1:file1...
  Migrated: quality=68.3, confidence=4
[2/171] Processing repo2:file2...
  Migrated: quality=72.1, confidence=4
...
Checkpoint saved at 10 rules
...

MIGRATION SUMMARY
Total rules: 171
Migrated: 171
Skipped: 0
Errors: 0
Duration: 512.3s
```

### Step 5: Verify Migration

Confirm all rules have quality scores:

```powershell
python migrate_quality_scores.py --verify-only
```

Expected output:
```
VERIFICATION RESULTS
Total rules: 171
With quality scores: 171
Average quality: 65.4/100
Quality range: 32.5 - 89.2

SUCCESS: All rules have quality scores
```

### Step 6: Analyze Distribution

Generate quality distribution report:

```powershell
python quality_analysis.py
```

This will show:
- Quality score percentiles (P10, P25, P50, P75, P90, P95)
- Confidence level distribution
- Production signal statistics
- Recommended thresholds for different use cases

### Step 7: Test Enhanced Generation

Generate a .cursorrules file using the enhanced system:

```powershell
python generate_cursorrules_v2.py "Build a Python FastAPI backend" `
  --tech python fastapi `
  --type api `
  --size medium `
  --team small `
  --min-quality 60 `
  --min-confidence 3
```

Verify output includes:
- Quality scores for each example
- Production signals
- Context disclaimers
- Trade-offs

---

## Rollback Plan

If you need to rollback to v1:

### Option 1: Use v1 Generator

Continue using `generate_cursorrules.py` (v1) instead of `generate_cursorrules_v2.py`:

```powershell
python generate_cursorrules.py "Build a Python FastAPI backend" `
  --tech python fastapi `
  --type api
```

### Option 2: Remove Quality Scores

Remove quality scores from database (forces v2 to use v1 fallback):

```cypher
MATCH (r:IDERule)
REMOVE r.quality_score, r.quality_breakdown, r.confidence_level,
       r.has_ci_cd, r.has_deployment, r.has_tests, r.has_monitoring,
       r.has_security, r.production_signals, r.repo_age_days,
       r.days_since_update, r.contributor_count, r.quality_migrated_at
```

---

## Troubleshooting

### Issue: Migration fails with "No Pattern node found"

**Cause:** IDERule node has no parent Pattern node.

**Fix:** These rules will be skipped automatically. Check logs for skipped rule IDs.

### Issue: Migration very slow

**Cause:** GitHub API rate limiting.

**Fix:** Migration includes automatic rate limiting. Wait for completion or reduce batch size:

```powershell
python migrate_quality_scores.py --batch-size 5
```

### Issue: "No quality data available" warning

**Cause:** Migration not run or incomplete.

**Fix:** Run migration script. System will fall back to v1 query (no quality filtering).

### Issue: All rules filtered out by quality thresholds

**Cause:** Quality thresholds too strict for your database.

**Fix:** Use recommended thresholds from `quality_analysis.py` or enable graceful degradation:

```python
# Use fallback query that relaxes filters automatically
rules = engine.query_rules_with_fallback(
    query="Python API",
    min_quality_score=60,
    min_results=5  # Relax if fewer than 5 results
)
```

---

## New Features Available After Migration

### 1. Quality-Filtered Queries

```python
# Strict: High quality only
rules = engine.query_rules(
    query="Python API",
    min_quality_score=75,
    min_confidence=4,
    require_production_signals=True
)

# Balanced: Good quality
rules = engine.query_rules(
    query="Python API",
    min_quality_score=60,
    min_confidence=3
)

# Permissive: Acceptable quality
rules = engine.query_rules(
    query="Python API",
    min_quality_score=40,
    min_confidence=2,
    require_production_signals=False
)
```

### 2. Smart Thresholds

```python
from quality_analysis import QualityAnalyzer

analyzer = QualityAnalyzer(driver, logger)

# Get threshold at median (50th percentile)
threshold = analyzer.get_smart_threshold(percentile=50)

# Use in query
rules = engine.query_rules(
    query="Python API",
    min_quality_score=threshold
)
```

### 3. Graceful Degradation

```python
# Automatically relaxes filters if too few results
rules = engine.query_rules_with_fallback(
    query="Python API",
    min_quality_score=60,
    min_results=5  # Trigger fallback if < 5 results
)
```

### 4. Quality Statistics

```python
# Get database quality stats
stats = engine.get_quality_stats()

print(f"Total rules: {stats['total']}")
print(f"Average quality: {stats['avg_quality']:.1f}")
print(f"With CI/CD: {stats['with_ci_cd']}")
print(f"With tests: {stats['with_tests']}")
```

---

## Support

If you encounter issues:

1. Check logs: `logs/enhanced_quality.log`
2. Run validation: `python validate_system.py`
3. Check migration checkpoint: `migration_checkpoint.json`
4. Review this guide's troubleshooting section

---

## Summary

| Step | Command | Time | Required |
|------|---------|------|----------|
| 1. Validate | `python validate_system.py` | 10s | Yes |
| 2. Estimate | `python estimate_costs.py --operation migration` | 5s | Recommended |
| 3. Dry Run | `python migrate_quality_scores.py --dry-run` | 10s | Recommended |
| 4. Migrate | `python migrate_quality_scores.py` | 8-10min | Yes |
| 5. Verify | `python migrate_quality_scores.py --verify-only` | 5s | Yes |
| 6. Analyze | `python quality_analysis.py` | 5s | Recommended |
| 7. Test | `python generate_cursorrules_v2.py ...` | 15s | Recommended |

**Total time:** ~10-15 minutes

---

**Version:** 2.0  
**Last Updated:** 8 January 2026
