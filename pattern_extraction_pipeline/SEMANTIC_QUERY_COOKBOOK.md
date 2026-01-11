# Semantic Query Cookbook

Quick reference for common semantic search patterns and use cases.

**Version:** 1.0  
**Date:** 2026-01-07

---

## Table of Contents

1. [Basic Queries](#basic-queries)
2. [Advanced Queries](#advanced-queries)
3. [Constraint Patterns](#constraint-patterns)
4. [Discovery Patterns](#discovery-patterns)
5. [Integration Patterns](#integration-patterns)
6. [Performance Tips](#performance-tips)
7. [Troubleshooting](#troubleshooting)

---

## Basic Queries

### Pattern 1: Simple Semantic Search

**Use Case:** Quick pattern discovery with natural language

```python
from pattern_query_interface_semantic import PatternQueryInterfaceSemantic

interface = PatternQueryInterfaceSemantic()

result = interface.find_patterns_semantic(
    goal="Build a desktop file manager",
    top_k=5
)

for p in result['patterns']:
    print(f"{p['name']}: {p['composite_score']:.2f}")
```

**When to use:** Exploratory searches, getting quick recommendations

### Pattern 2: Hybrid Search (Recommended Default)

**Use Case:** Natural language + technical requirements

```python
result = interface.find_patterns_hybrid(
    goal="Real-time chat application with message persistence",
    constraints={
        'technologies': ['nodejs', 'websocket', 'redis'],
        'min_stars': 10000
    },
    top_k=5
)

# Present to user for review
print(result['user_review_text'])
```

**When to use:** Production SPEC generation, when you know tech requirements

### Pattern 3: Feasibility Check

**Use Case:** Validate SPEC before implementation

```python
spec = {
    'goal': 'Build an e-commerce platform with real-time inventory',
    'tech_stack': {'languages': ['typescript', 'python']},
    'deployment_type': 'web'
}

verification = interface.verify_spec_feasibility(spec, use_semantic=True)

print(f"Feasibility: {verification['feasibility_score']}")
print(f"Confidence: {verification['confidence']}")
if verification['concerns']:
    print(f"Concerns: {', '.join(verification['concerns'])}")
```

**When to use:** Pre-flight SPEC validation, risk assessment

---

## Advanced Queries

### Pattern 4: Cross-Pattern Discovery

**Use Case:** Find alternative architectural approaches

```python
result = interface.discover_alternatives(
    goal="Event-driven file processing system",
    include_different_tech=True,
    min_similarity=0.7,
    top_k=15
)

# Group by architectural approach
for approach, patterns in result['approaches'].items():
    print(f"\n{approach} ({len(patterns)} patterns):")
    for p in patterns[:3]:
        techs = ', '.join(p['tech_stack'][:3])
        print(f"  - {p['name']} ({techs})")
```

**When to use:** Exploring design options, comparing architectures

### Pattern 5: Similar Pattern Search

**Use Case:** Find backup approaches when primary pattern fails

```python
# During execution, if primary pattern fails
current_pattern = "electron_desktop_app"

result = interface.find_similar_patterns(
    pattern_name=current_pattern,
    top_k=3,
    min_similarity=0.6
)

print(f"Backup options for {current_pattern}:")
for p in result['similar_patterns']:
    shared = ', '.join(p['shared_technologies'][:3])
    print(f"  {p['name']} (similarity: {p['similarity']:.2f})")
    print(f"    Shared tech: {shared}")
    print(f"    Reasoning: {p['reasoning'][:80]}...")
```

**When to use:** Runtime backup suggestions, pattern exploration

---

## Constraint Patterns

### Pattern 6: Technology-Focused Search

**Use Case:** Find patterns using specific technologies

```python
result = interface.find_patterns_hybrid(
    goal="Data visualization dashboard",
    constraints={
        'technologies': ['d3js', 'typescript', 'react'],
        'min_stars': 5000,
        'min_confidence': 'high'
    },
    semantic_top_k=30,  # Cast wider net for semantic
    top_k=10
)
```

**Constraint options:**
- `technologies`: List[str] - Required technologies
- `deployment_type`: str - 'web', 'desktop', 'mobile', 'cli', 'api'
- `min_stars`: int - Minimum GitHub stars
- `min_confidence`: str - 'high', 'medium', or 'low'
- `domains`: List[str] - Domain filters

### Pattern 7: Deployment-Specific Search

**Use Case:** Filter by deployment type

```python
# Find web application patterns
result = interface.find_patterns_hybrid(
    goal="User management system",
    constraints={
        'deployment_type': 'web',
        'min_stars': 10000
    }
)

# Find CLI tool patterns
result = interface.find_patterns_hybrid(
    goal="File processing utility",
    constraints={
        'deployment_type': 'cli',
        'technologies': ['python'],
        'min_stars': 5000
    }
)
```

### Pattern 8: High-Confidence Only

**Use Case:** Production-ready patterns only

```python
result = interface.find_patterns_hybrid(
    goal="Payment processing system",
    constraints={
        'min_confidence': 'high',
        'min_stars': 20000  # Well-proven patterns
    },
    top_k=3  # Top 3 only
)
```

**Confidence levels:**
- `high`: Well-documented, clear architecture, established pattern
- `medium`: Proven but less documentation
- `low`: Experimental or niche patterns

---

## Discovery Patterns

### Pattern 9: Explore by Domain

**Use Case:** Survey patterns in a specific domain

```python
# First, semantic search to get candidates
result = interface.find_patterns_semantic(
    goal="e-commerce product catalog",
    top_k=20
)

# Group by domain
domains = {}
for p in result['patterns']:
    for domain in p.get('domains', ['unknown']):
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(p['name'])

for domain, patterns in domains.items():
    print(f"{domain}: {len(patterns)} patterns")
```

### Pattern 10: Technology Popularity Analysis

**Use Case:** See which technologies are most common for a goal

```python
result = interface.find_patterns_semantic(
    goal="Real-time data streaming",
    top_k=30
)

# Aggregate technologies
tech_counts = {}
for p in result['patterns']:
    for tech in p.get('technologies', []):
        tech_counts[tech] = tech_counts.get(tech, 0) + 1

# Sort by popularity
popular = sorted(tech_counts.items(), key=lambda x: x[1], reverse=True)
print("Most common technologies for 'Real-time data streaming':")
for tech, count in popular[:10]:
    print(f"  {tech}: {count} patterns")
```

---

## Integration Patterns

### Pattern 11: Commander Integration (Future)

**Use Case:** Pattern-informed SPEC generation

```python
def generate_spec_from_pattern(user_goal, user_constraints):
    """Commander workflow with pattern selection."""
    
    # Step 1: Query patterns
    interface = PatternQueryInterfaceSemantic()
    result = interface.find_patterns_hybrid(
        goal=user_goal,
        constraints=user_constraints,
        top_k=10
    )
    
    # Step 2: Present to user
    print(result['user_review_text'])
    print("\nSelect a pattern (1-10): ")
    selection = int(input())
    
    selected_pattern = result['patterns'][selection - 1]
    
    # Step 3: Generate SPEC using pattern
    spec_template = {
        'goal': user_goal,
        'recommended_tech_stack': selected_pattern['technologies'],
        'architectural_approach': selected_pattern['reasoning'],
        'proven_success': f"{selected_pattern['stars']:,} stars",
        'confidence': selected_pattern['recommendation'],
        'source_repo': selected_pattern['source_repo']
    }
    
    interface.close()
    return spec_template, selected_pattern
```

### Pattern 12: Executor Backup Suggestions

**Use Case:** Runtime backup method discovery

```python
def suggest_backups_for_failed_step(current_pattern, failed_step):
    """Find alternative approaches when step fails."""
    
    interface = PatternQueryInterfaceSemantic()
    
    # Find similar patterns
    similar = interface.find_similar_patterns(
        pattern_name=current_pattern,
        top_k=5
    )
    
    backups = []
    for pattern in similar['similar_patterns']:
        backup = {
            'pattern': pattern['name'],
            'approach': pattern['reasoning'],
            'similarity': pattern['similarity'],
            'shared_tech': pattern['shared_technologies'],
            'rationale': f"Similar to {current_pattern}, proven with {pattern['stars']:,} stars"
        }
        backups.append(backup)
    
    interface.close()
    return backups
```

---

## Performance Tips

### Tip 1: Use Caching

Embeddings are cached automatically by filename hash. Reusing queries is very fast:

```python
# First call: generates embedding (30-80ms)
result1 = interface.find_patterns_semantic(goal="File manager", top_k=5)

# Second call with same goal: uses cache (5-15ms)
result2 = interface.find_patterns_semantic(goal="File manager", top_k=10)
```

### Tip 2: Adjust semantic_top_k for Speed

```python
# Faster: narrow semantic search
result = interface.find_patterns_hybrid(
    goal="...",
    constraints={...},
    semantic_top_k=10,  # Only search top 10 semantic matches
    top_k=5
)

# More thorough: wider semantic search
result = interface.find_patterns_hybrid(
    goal="...",
    constraints={...},
    semantic_top_k=30,  # Search top 30 semantic matches
    top_k=5
)
```

**Trade-off:** Lower semantic_top_k is faster but might miss relevant patterns

### Tip 3: Batch Queries

If you need multiple queries, batch them:

```python
goals = [
    "File manager application",
    "Real-time chat system",
    "Data visualization dashboard"
]

results = []
for goal in goals:
    result = interface.find_patterns_semantic(goal, top_k=3)
    results.append(result)
# Embeddings cached after first, subsequent queries very fast
```

### Tip 4: Use Semantic for Discovery, Hybrid for Precision

```python
# Phase 1: Discovery (fast, exploratory)
candidates = interface.find_patterns_semantic(
    goal="distributed system",
    top_k=20
)

# Analyze candidates...

# Phase 2: Precision (with constraints)
final = interface.find_patterns_hybrid(
    goal="distributed message queue system",
    constraints={
        'technologies': ['kafka', 'redis'],
        'min_stars': 10000
    },
    top_k=5
)
```

---

## Troubleshooting

### Issue: No patterns returned

**Symptoms:**
```python
result['patterns'] == []
```

**Diagnosis:**
1. Check if patterns have embeddings:
   ```bash
   python test_vector_search.py
   ```
2. Lower similarity threshold:
   ```python
   result = interface.find_patterns_semantic(
       goal="...",
       min_similarity=0.3  # Lower from default 0.5
   )
   ```
3. Check pattern count in database:
   ```cypher
   MATCH (p:Pattern) RETURN count(p)
   ```

### Issue: Irrelevant results

**Symptoms:** Top patterns don't match goal intent

**Solutions:**
1. **Add constraints:**
   ```python
   # Instead of semantic-only
   result = interface.find_patterns_hybrid(
       goal="file manager",
       constraints={
           'deployment_type': 'desktop',
           'technologies': ['electron', 'typescript']
       }
   )
   ```

2. **Adjust scoring weights:**
   ```python
   from confidence_scorer import ConfidenceScorer, ConfidenceWeights
   
   # Emphasize semantic match more
   weights = ConfidenceWeights(
       semantic=0.6,  # Increased from 0.4
       confidence=0.2,
       stars=0.2
   )
   
   scorer = ConfidenceScorer(weights)
   interface.confidence_scorer = scorer
   ```

3. **Use more specific goal descriptions:**
   ```python
   # Vague
   goal = "application"
   
   # Specific
   goal = "desktop file browser application with tree view and preview pane"
   ```

### Issue: Slow queries (>500ms)

**Diagnosis:**
1. Check index status:
   ```cypher
   SHOW INDEXES YIELD name, state WHERE name = 'pattern_embeddings'
   ```
2. Check pattern count:
   ```cypher
   MATCH (p:Pattern) RETURN count(p)
   ```

**Solutions:**
1. **If >1000 patterns, enable quantization:**
   ```cypher
   DROP INDEX pattern_embeddings IF EXISTS;
   CREATE VECTOR INDEX pattern_embeddings FOR (p:Pattern) ON p.embedding
   OPTIONS {
       indexConfig: {
           `vector.dimensions`: 768,
           `vector.similarity_function`: 'cosine',
           `vector.quantization.enabled`: true,
           `vector.quantization.type`: 'bit'
       }
   }
   ```

2. **Reduce semantic_top_k:**
   ```python
   result = interface.find_patterns_hybrid(
       goal="...",
       semantic_top_k=10,  # Reduced from 20
       top_k=5
   )
   ```

### Issue: Missing embeddings

**Symptoms:**
```
Pattern X found but no embedding property
```

**Solution:**
```bash
# Regenerate embeddings for all patterns
python generate_pattern_embeddings.py --force

# Or for specific patterns only
python generate_pattern_embeddings.py
```

---

## Best Practices

1. **Always use hybrid for production:** Semantic-only is for exploration
2. **Present top 5-10 to users:** Don't auto-select, let humans choose
3. **Check confidence scores:** High-confidence patterns are safer
4. **Use cross-pattern discovery for innovation:** Find new approaches
5. **Cache is your friend:** Reuse queries when possible
6. **Specific goals = better results:** "Desktop file manager" > "application"
7. **Monitor performance:** Keep queries under 200ms
8. **Update embeddings weekly:** When adding new patterns
9. **Test constraints independently:** Verify tech filters work
10. **Log user selections:** Learn which patterns users prefer

---

## Quick Reference

```python
# Import
from pattern_query_interface_semantic import PatternQueryInterfaceSemantic
interface = PatternQueryInterfaceSemantic()

# Semantic search
interface.find_patterns_semantic(goal, top_k, min_similarity)

# Hybrid search (RECOMMENDED)
interface.find_patterns_hybrid(goal, constraints, top_k, semantic_top_k)

# Cross-pattern discovery
interface.discover_alternatives(goal, include_different_tech, min_similarity, top_k)

# Similar patterns
interface.find_similar_patterns(pattern_name, top_k, min_similarity)

# Feasibility check
interface.verify_spec_feasibility(spec_dict, use_semantic)

# Always close
interface.close()
```

---

**Version:** 1.0  
**Last Updated:** 2026-01-07  
**See Also:** `VECTOR_ARCHITECTURE.md`, `PATTERN_QUERY_GUIDE.md`
