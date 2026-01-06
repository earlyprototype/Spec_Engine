# Smart Duplicate Detection - Integration Test Guide

## Prerequisites

Database is ready:
- [x] 228 unique patterns in Neo4j
- [x] No duplicates remain  
- [x] Uniqueness constraint active on `Pattern.source_repo`
- [x] All code changes implemented

## Test 1: Unit Tests (Database Queries)

**Run manually:**
```cmd
cd pattern_extraction_pipeline
RUN_TESTS.bat
```

**Expected Output:**
```
=== Test 1: Duplicate Check Query ===
   [PASS] Correctly returned None for non-existent repo

=== Test 2: Check Existing Repository ===
   Testing with: https://github.com/...
   [PASS] Found pattern: ...

=== Test 3: Uniqueness Constraint ===
   [PASS] Constraint found: pattern_repo_unique

=== Test 4: No Duplicate Patterns ===
   [PASS] No duplicate patterns found

=== Test 5: Pattern Statistics ===
   Total patterns: 228
   With source_repo: 228
   [PASS] Database statistics collected

Passed: 5/5
[SUCCESS] All unit tests passed!
```

---

## Test 2: Integration Test - Skip Logic

**Objective:** Verify that re-analyzing an existing repository is SKIPPED

### Steps:

1. **Start the Flask server:**
   ```cmd
   cd pattern_extraction_pipeline
   python domain_selector_server.py
   ```

2. **Open UI:** http://localhost:8000

3. **Create test query for EXISTING repository:**
   - Query: `repo:medusajs/medusa`
   - Limit: 10
   - Force Re-analyze: **UNCHECKED** ✗

4. **Click "Generate Batch Script"**

5. **Run extraction**

6. **Expected Console Output:**
   ```
   [21:50:00] Analyzing https://github.com/medusajs/medusa...
     [SKIP] Already analyzed on 2026-01-06
            Quality: 0.80, Stars: 25000
   ```

7. **Check Statistics:**
   ```
   Extraction Statistics:
     Total repositories: 1
     Skipped (duplicates): 1
     Successful: 0
   ```

8. **Check Trajectory Log:**
   ```json
   {
     "skipped_repositories": [
       {
         "repo": "medusajs/medusa",
         "reason": "already_analyzed",
         "previous_extraction": "2026-01-06T...",
         "quality_score": 0.799
       }
     ],
     "summary": {
       "skipped": 1,
       "total_repos": 1
     }
   }
   ```

**Result:** ✅ **PASS** if repo was skipped

---

## Test 3: Integration Test - Force Re-analyze

**Objective:** Verify that force flag OVERRIDES skip logic

### Steps:

1. **Same query as Test 2**
2. **Force Re-analyze: CHECKED** ✓
3. **Run extraction**

4. **Expected Console Output:**
   ```
   [21:52:00] Analyzing https://github.com/medusajs/medusa...
     [INFO] Force re-analyze enabled
     [ANALYZING] Fetching repository...
     [LLM] Extracting patterns...
     [OK] Pattern updated (quality: 0.XX)
   ```

5. **Check Statistics:**
   ```
   Extraction Statistics:
     Total repositories: 1
     Skipped (duplicates): 0
     Successful: 1
   ```

**Result:** ✅ **PASS** if repo was re-analyzed despite existing

---

## Test 4: Integration Test - New Repository

**Objective:** Verify normal extraction still works

### Steps:

1. **Query for UNKNOWN repository:**
   - Query: `repo:newrepo/never-analyzed`
   - Limit: 5

2. **Run extraction**

3. **Expected Behavior:**
   - No skip message
   - Normal analysis proceeds
   - Pattern created with MERGE (not CREATE)
   - Statistics show successful: 1, skipped: 0

**Result:** ✅ **PASS** if new repo is analyzed normally

---

## Test 5: MERGE Behavior Verification

**Objective:** Verify MERGE preserves validation scores

### Steps:

1. **Find a pattern with validation score:**
   ```cypher
   MATCH (p:Pattern)
   WHERE p.validation_score IS NOT NULL
   RETURN p.name, p.source_repo, p.validation_score, p.quality_score
   LIMIT 1
   ```

2. **Note the validation_score value**

3. **Force re-analyze that repository**

4. **Query again and verify:**
   - `validation_score` unchanged
   - `quality_score` updated (if different)
   - `extracted_at` updated to new timestamp

**Expected Neo4j Query Result:**
```
Before:  validation_score: 0.85, quality_score: 0.80, extracted_at: 2026-01-05
After:   validation_score: 0.85, quality_score: 0.82, extracted_at: 2026-01-06
```

**Result:** ✅ **PASS** if validation score preserved

---

## Test 6: Performance Benchmark

**Objective:** Measure skip check overhead

### Steps:

1. **Run extraction on 50 EXISTING repositories**
2. **Time the execution**

**Expected:**
- Skip check: <100ms per repo
- Total time: ~5 seconds for 50 repos
- No LLM calls made
- API rate limit NOT hit

**Result:** ✅ **PASS** if skip is fast (<100ms/repo)

---

## Success Criteria

All tests must pass:
- [  ] Unit Tests (5/5 passed)
- [  ] Skip Logic Works
- [  ] Force Override Works  
- [  ] New Repos Analyzed
- [  ] MERGE Preserves Scores
- [  ] Performance Acceptable

---

## Troubleshooting

### Issue: Tests timeout
**Fix:** Run `RUN_TESTS.bat` manually in separate terminal

### Issue: Skip logic not working
**Check:**
1. Constraint exists: `SHOW CONSTRAINTS`
2. Code deployed: Check `pattern_extractor.py` line 322
3. Database has patterns: `MATCH (p:Pattern) RETURN count(p)`

### Issue: Force flag not working
**Check:**
1. UI checkbox value in browser console
2. Backend receives flag: Check server logs
3. Code passes flag: `domain_selector_server.py` line 293

---

**Test Date:** 6 January 2026  
**Database:** spec-engine-neo4j (port 7688)  
**Status:** Ready for Testing
