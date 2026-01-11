# Integration Testing Guide for Duplicate Detection

## Overview

This guide provides step-by-step instructions for testing the duplicate detection functionality in the pattern extraction pipeline.

## Prerequisites

1. Neo4j container running (`docker ps` should show `spec-engine-neo4j` as healthy)
2. Valid `.env` file with GitHub and Gemini API keys
3. Python environment with dependencies installed

## Test Scenarios

### Scenario 1: Fresh Extraction (Baseline)

**Purpose:** Verify normal extraction works without duplicates

**Steps:**
```powershell
cd pattern_extraction_pipeline

# Extract 3 repos from a small query
python -c "
from pattern_extractor import PatternExtractor
extractor = PatternExtractor()
patterns = extractor.extract_patterns(
    'topic:markdown-parser stars:>1000',
    limit=3,
    validate=False,
    force_reanalyse=False
)
print(f'\nExtracted {len(patterns)} patterns')
"
```

**Expected Output:**
- Total: 3
- Successful: 3 (or partial, depending on data availability)
- Failed: 0
- Skipped: 0

### Scenario 2: Duplicate Detection

**Purpose:** Verify repositories are skipped on re-extraction

**Steps:**
```powershell
# Run the SAME query again
python -c "
from pattern_extractor import PatternExtractor
extractor = PatternExtractor()
patterns = extractor.extract_patterns(
    'topic:markdown-parser stars:>1000',
    limit=3,
    validate=False,
    force_reanalyse=False
)
print(f'\nExtracted {len(patterns)} patterns')
"
```

**Expected Output:**
- Total: 3
- Successful: 0
- Failed: 0
- Skipped: 3 (all repositories should be skipped)
- Console should show `[SKIP] Already analyzed on YYYY-MM-DD`

### Scenario 3: Force Re-analysis

**Purpose:** Verify force flag overrides skip logic

**Steps:**
```powershell
# Run with force_reanalyse=True
python -c "
from pattern_extractor import PatternExtractor
extractor = PatternExtractor()
patterns = extractor.extract_patterns(
    'topic:markdown-parser stars:>1000',
    limit=3,
    validate=False,
    force_reanalyse=True
)
print(f'\nExtracted {len(patterns)} patterns')
"
```

**Expected Output:**
- Total: 3
- Successful: 3 (patterns re-analyzed and updated)
- Failed: 0
- Skipped: 0
- Console should NOT show skip messages

### Scenario 4: MERGE Validation

**Purpose:** Verify MERGE preserves validation scores while updating extraction data

**Steps:**

1. Extract a pattern and get it validated:
```powershell
# Extract and wait for validation
python -c "
from pattern_extractor import PatternExtractor
extractor = PatternExtractor()
patterns = extractor.extract_patterns(
    'topic:json-parser stars:>5000',
    limit=1,
    validate=False
)
print('Pattern extracted, waiting 10 seconds for validation...')
import time
time.sleep(10)
"
```

2. Check validation scores:
```cypher
// In Neo4j Browser
MATCH (p:Pattern)
WHERE p.source_repo CONTAINS 'json-parser'
RETURN p.name, p.validation_score, p.quality_score, p.extracted_at
ORDER BY p.extracted_at DESC
LIMIT 1
```

3. Force re-extract:
```powershell
python -c "
from pattern_extractor import PatternExtractor
extractor = PatternExtractor()
patterns = extractor.extract_patterns(
    'topic:json-parser stars:>5000',
    limit=1,
    validate=False,
    force_reanalyse=True
)
"
```

4. Check scores again:
```cypher
// In Neo4j Browser - same query as step 2
MATCH (p:Pattern)
WHERE p.source_repo CONTAINS 'json-parser'
RETURN p.name, p.validation_score, p.quality_score, p.extracted_at
ORDER BY p.extracted_at DESC
LIMIT 1
```

**Expected:**
- `extracted_at` should be updated (recent timestamp)
- `quality_score` should be updated (may differ slightly)
- `validation_score` should be PRESERVED (same value as before)
- `judge_score` should be PRESERVED if it was set

### Scenario 5: Uniqueness Constraint

**Purpose:** Verify constraint prevents manual duplicate creation

**Steps:**

1. Try to create a duplicate pattern manually:
```cypher
// In Neo4j Browser
// First, get an existing pattern's source_repo
MATCH (p:Pattern)
RETURN p.source_repo
LIMIT 1

// Try to create a duplicate (replace URL with actual pattern URL)
CREATE (p:Pattern {
    source_repo: "https://github.com/existing/repo",
    name: "duplicate_test"
})
```

**Expected:**
- Should fail with constraint violation error
- Error message should mention `pattern_repo_unique` constraint

### Scenario 6: Trajectory Logging

**Purpose:** Verify skipped repositories are logged

**Steps:**

1. Run extraction with some duplicates:
```powershell
python -c "
from pattern_extractor import PatternExtractor
extractor = PatternExtractor()
patterns = extractor.extract_patterns(
    'topic:markdown-parser stars:>1000',
    limit=5,
    validate=False,
    domain='test_trajectory'
)
"
```

2. Check trajectory log:
```powershell
# Find the latest trajectory file
Get-ChildItem pattern_extraction_pipeline\logs\trajectories\test_trajectory_*.json |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1 |
    ForEach-Object { Get-Content $_.FullName | ConvertFrom-Json }
```

**Expected:**
- `skipped_repositories` array should contain skipped repos
- Each entry should have: repo name, reason, previous_extraction date, quality_score
- `summary.skipped` count should match array length

### Scenario 7: Backend API Integration

**Purpose:** Verify force flag passes through backend

**Steps:**

1. Start the backend server:
```powershell
cd pattern_extraction_pipeline
python domain_selector_server.py
```

2. In another terminal, send test request:
```powershell
$body = @{
    queries = @(
        @{
            query = "topic:json-parser stars:>5000"
            limit = 2
            force_reanalyse = $false
        }
    )
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/extract" -Method POST -Body $body -ContentType "application/json"
```

3. Check extraction status:
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/extract/status" -Method GET
```

4. Repeat with force_reanalyse = $true and verify different behavior

**Expected:**
- First run: Repos processed
- Second run (force=false): Repos skipped
- Third run (force=true): Repos re-processed

### Scenario 8: UI Integration

**Purpose:** Verify UI checkbox controls force flag

**Steps:**

1. Start backend server (if not running):
```powershell
cd pattern_extraction_pipeline
python domain_selector_server.py
```

2. Open UI in browser:
```
http://localhost:8000
```

3. Enter project description and analyze

4. Observe query results with:
   - Checkbox labeled "Force Re-analyze"
   - Limit input field

5. Check/uncheck the Force Re-analyze checkbox

6. Click "Extract Patterns" button

**Expected:**
- Checkbox visible for each query
- Checking box sets `force_reanalyse: true` in request
- Console shows force flag status
- Extraction behavior changes based on checkbox state

## Performance Validation

### Test Skip Performance

**Purpose:** Verify skip check is fast (<10ms per repo)

**Steps:**
```powershell
python -c "
from pattern_extractor import PatternExtractor
import time

extractor = PatternExtractor()

# Time multiple checks
times = []
for i in range(10):
    start = time.time()
    result = extractor._check_if_repo_exists('https://github.com/test/repo-' + str(i))
    elapsed = time.time() - start
    times.append(elapsed)

avg_time = sum(times) / len(times)
print(f'Average check time: {avg_time*1000:.2f}ms')
print(f'Max check time: {max(times)*1000:.2f}ms')

if avg_time < 0.01:
    print('[PASS] Average time < 10ms')
else:
    print('[FAIL] Average time >= 10ms')
"
```

**Expected:**
- Average time < 10ms
- Max time < 50ms (with network variance)

## Post-Implementation Checklist

Run these checks after all tests pass:

### Database Verification

```cypher
// 1. Verify constraint exists
SHOW CONSTRAINTS

// Should show: pattern_repo_unique

// 2. Check for duplicates
MATCH (p:Pattern)
WITH p.source_repo as repo, count(*) as cnt
WHERE cnt > 1
RETURN repo, cnt

// Should return: (no rows)

// 3. Count patterns
MATCH (p:Pattern)
RETURN count(p) as total_patterns

// 4. Check extraction metadata
MATCH (p:Pattern)
RETURN 
    count(p) as total,
    sum(CASE WHEN p.has_readme THEN 1 ELSE 0 END) as with_readme,
    sum(CASE WHEN p.extracted_at IS NOT NULL THEN 1 ELSE 0 END) as with_timestamp
```

### Code Verification

```powershell
# 1. Check method exists
Select-String -Path "pattern_extraction_pipeline\pattern_extractor.py" -Pattern "_check_if_repo_exists"

# 2. Check force parameter
Select-String -Path "pattern_extraction_pipeline\pattern_extractor.py" -Pattern "force_reanalyse"

# 3. Check MERGE usage
Select-String -Path "pattern_extraction_pipeline\pattern_extractor.py" -Pattern "MERGE.*Pattern"

# 4. Check trajectory logging
Select-String -Path "pattern_extraction_pipeline\trajectory_logger.py" -Pattern "log_repository_skipped"

# 5. Check UI checkbox
Select-String -Path "pattern_extraction_pipeline\domain_selector_ui.html" -Pattern "Force Re-analyze"
```

## Troubleshooting

### Issue: Neo4j Connection Timeout

**Solution:**
```powershell
# Check Neo4j container status
docker ps -a | Select-String "neo4j"

# Restart if needed
docker restart spec-engine-neo4j

# Wait for health check
Start-Sleep -Seconds 10
```

### Issue: Constraint Creation Fails

**Solution:**
```powershell
# Clean up duplicates first
cd pattern_extraction_pipeline
python setup_data_quality.py
```

### Issue: Patterns Not Being Skipped

**Check:**
1. Verify `force_reanalyse=False` in call
2. Check repository URL matches exactly
3. Verify pattern exists in database:
```cypher
MATCH (p:Pattern {source_repo: "URL_HERE"})
RETURN p
```

### Issue: UI Checkbox Not Working

**Check:**
1. Browser console for JavaScript errors
2. Network tab to verify request includes `force_reanalyse` field
3. Backend logs for force flag value

## Success Criteria

All tests pass when:

- [ ] Fresh extraction processes all repos
- [ ] Re-extraction skips all previously analyzed repos
- [ ] Force flag bypasses skip logic
- [ ] MERGE preserves validation scores
- [ ] Uniqueness constraint prevents duplicates
- [ ] Trajectory logs include skipped repos
- [ ] Backend passes force flag correctly
- [ ] UI checkbox controls force flag
- [ ] Skip check performance < 10ms
- [ ] No duplicate patterns in database

## Monitoring First Production Run

After tests pass, monitor a production extraction:

```powershell
# Start extraction with monitoring
cd pattern_extraction_pipeline
python domain_selector_server.py

# In another terminal, watch logs
Get-Content logs\trajectories\*.json -Wait | ConvertFrom-Json
```

**Watch for:**
- Skip rate on repeat queries (should be 50-80%)
- No constraint violation errors
- Extraction time improvements
- Correct statistics in trajectory logs
