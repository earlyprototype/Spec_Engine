# Quick Start: Semantic Pattern Search

Get semantic pattern search up and running in 5 minutes.

---

## Prerequisites

- Neo4j 5.22 running (from docker-compose.yml)
- Patterns extracted in knowledge graph
- Gemini API key in `.env`

---

## Step 1: Generate Embeddings (2-5 minutes)

```powershell
# Navigate to directory
cd c:\Users\Fab2\Desktop\AI\Specs\pattern_extraction_pipeline

# Generate embeddings for all patterns
python generate_pattern_embeddings.py
```

**Expected output:**
```
PatternEmbeddingPipeline initialized
Initial Status:
  Total patterns: 50
  Without embeddings: 50

Processing 50 patterns...
Batch 1: Processing patterns 1-50...
  ✓ pattern1 (45ms)
  ✓ pattern2 (12ms) [cached]
  ...
✓ Pipeline complete!
Final Status:
  Total patterns: 50
  With embeddings: 50
```

**Time:** ~2-5 minutes depending on pattern count and cache hits

---

## Step 2: Create Vector Index (30 seconds)

```powershell
# Run Cypher setup script
cypher-shell -u neo4j -p specengine123 < vector_index_setup.cypher
```

**Or via Neo4j Browser** (http://localhost:7475):
```cypher
CREATE VECTOR INDEX pattern_embeddings IF NOT EXISTS
FOR (p:Pattern) ON p.embedding
OPTIONS {
    indexConfig: {
        `vector.dimensions`: 768,
        `vector.similarity_function`: 'cosine'
    }
};

CALL db.awaitIndexes(300);
```

**Verify:**
```cypher
SHOW INDEXES YIELD name, state WHERE name = 'pattern_embeddings';
```

Should return: `state = 'ONLINE'`

---

## Step 3: Test Semantic Search (1 minute)

```powershell
# Run test suite
python test_vector_search.py
```

**Expected:**
```
TEST 1: Vector Index Status
✓ PASSED: Vector index is online and ready

TEST 2: Embedding Coverage
✓ PASSED: All patterns have embeddings

TEST 3: Embedding Dimensions
✓ PASSED: All embeddings have correct dimensions (768)

TEST 4: Vector Search Queries
✓ PASSED: All vector searches executed successfully

TEST 5: Query Performance
✓ PASSED: Performance within targets

Overall: 5/5 tests passed (100%)
✓ SUCCESS: All tests passed!
```

---

## Step 4: Try It Out! (Interactive)

```powershell
# Start Python interactive shell
python
```

```python
from pattern_query_interface_semantic import PatternQueryInterfaceSemantic

# Initialize interface
interface = PatternQueryInterfaceSemantic()

# Test 1: Simple semantic search
result = interface.find_patterns_semantic(
    goal="Build a desktop file manager application",
    top_k=5
)

print(f"Found {len(result['patterns'])} patterns:\n")
for i, p in enumerate(result['patterns'], 1):
    print(f"{i}. {p['name']} (score: {p['composite_score']:.2f})")
    print(f"   {p['explanation']}\n")

# Test 2: Hybrid search with constraints
result = interface.find_patterns_hybrid(
    goal="Real-time chat application with message history",
    constraints={
        'technologies': ['nodejs', 'websocket'],
        'min_stars': 5000
    },
    top_k=5
)

# Present to user
print(result['user_review_text'])

# Close
interface.close()
```

**Expected:** Relevant patterns with confidence scores

---

## Step 5: Run Hybrid Query Tests (Optional)

```powershell
python test_hybrid_queries.py
```

**Expected:**
```
TEST 1: Semantic Search (No Constraints)
✓ PASSED

TEST 2: Hybrid Search with Technology Constraints
✓ PASSED

TEST 3: Confidence Scoring
✓ PASSED

TEST 4: Cross-Pattern Discovery
✓ PASSED

TEST 5: Similar Pattern Search
✓ PASSED

TEST 6: Enhanced SPEC Verification
✓ PASSED

Overall: 6/6 tests passed (100%)
✓ SUCCESS: All hybrid query tests passed!
```

---

## Common Issues

### Issue: "NEO4J_PASSWORD not found"

**Solution:**
```powershell
# Check .env file
cat .env | Select-String "NEO4J_PASSWORD"

# If missing, add it
echo "NEO4J_PASSWORD=specengine123" >> .env
```

### Issue: "GEMINI_API_KEY not found"

**Solution:**
```powershell
# Add to .env
echo "GEMINI_API_KEY=your_key_here" >> .env
```

### Issue: "No patterns have embeddings"

**Solution:**
```powershell
# Force regenerate
python generate_pattern_embeddings.py --force
```

### Issue: Vector index not found

**Solution:**
```powershell
# Re-run index setup
cypher-shell -u neo4j -p specengine123 < vector_index_setup.cypher
```

---

## What's Next?

1. **Explore the API:**
   - Read `SEMANTIC_QUERY_COOKBOOK.md` for common patterns
   - Check `VECTOR_ARCHITECTURE.md` for technical details

2. **Integrate with SPEC Commander:**
   - Use patterns to inform SPEC generation
   - Implement user pattern selection workflow

3. **Customize Scoring:**
   - Adjust confidence weights if needed
   - Tune for your use case

4. **Add More Patterns:**
   - Extract additional patterns
   - Re-run `generate_pattern_embeddings.py`
   - Patterns auto-indexed

---

## Quick Command Reference

```powershell
# Setup
python generate_pattern_embeddings.py
cypher-shell -u neo4j -p specengine123 < vector_index_setup.cypher

# Test
python test_vector_search.py
python test_hybrid_queries.py

# Usage
python  # Then import PatternQueryInterfaceSemantic

# Regenerate (after adding patterns)
python generate_pattern_embeddings.py
```

---

**Time to Complete:** ~5-10 minutes  
**Result:** Semantic pattern search fully functional

**Next:** See `SEMANTIC_QUERY_COOKBOOK.md` for usage patterns
