# Data Quality & Normalization

## Problem

Knowledge graphs are susceptible to duplicate nodes due to:
- **Case sensitivity**: `SQlite` vs `sqlite`
- **Whitespace**: `react ` vs `react`
- **Formatting**: `filesystem is source of truth` vs `filesystem_is_source_of_truth`

These duplicates fragment the graph and reduce pattern matching accuracy.

## Solution

### 1. Normalization Layer

All data is normalized **before** storage:

```python
# Technology names -> lowercase
"SQlite" -> "sqlite"
"React" -> "react"
"TypeScript" -> "typescript"

# Constraint rules -> lowercase_snake_case
"Filesystem is source of truth" -> "filesystem_is_source_of_truth"
"Database for metadata only" -> "database_for_metadata_only"

# Role names -> lowercase
"Primary" -> "primary"
"Cache" -> "cache"
```

### 2. Unique Constraints

Neo4j constraints prevent duplicates at the database level:

```cypher
CREATE CONSTRAINT tech_unique FOR (t:Technology) REQUIRE t.name IS UNIQUE;
CREATE CONSTRAINT constraint_unique FOR (c:Constraint) REQUIRE c.rule IS UNIQUE;
```

If you try to create a duplicate, Neo4j will error or merge automatically (depending on MERGE vs CREATE).

### 3. Relationship Deduplication

`MERGE` without properties prevents duplicate relationships:

```cypher
// Before: Creates 4 relationships if called 4 times
CREATE (p)-[:USES {role: "primary"}]->(t)

// After: Creates 1 relationship, updates role if called again
MERGE (p)-[u:USES]->(t)
ON CREATE SET u.role = "primary"
ON MATCH SET u.role = "primary"
```

## Setup

### Initial Setup (Run Once)

```powershell
# Run data quality setup
python pattern_extraction_pipeline\setup_data_quality.py
```

This will:
1. Create unique constraints
2. Find and report duplicates
3. Merge duplicate nodes
4. Normalize existing data
5. Remove duplicate relationships

### Verify Cleanup

```cypher
// Check for duplicate technologies
MATCH (t:Technology)
WITH toLower(t.name) AS normalized_name, collect(t.name) AS names
WHERE size(names) > 1
RETURN normalized_name, names, size(names) AS count

// Check for duplicate constraints
MATCH (c:Constraint)
WITH toLower(c.rule) AS normalized_rule, collect(c.rule) AS rules
WHERE size(rules) > 1
RETURN normalized_rule, rules, size(rules) AS count

// Check for duplicate relationships
MATCH (p:Pattern)-[r:USES]->(t:Technology)
WITH p, t, count(r) AS rel_count
WHERE rel_count > 1
RETURN p.name, t.name, rel_count
```

All queries should return **0 results** after cleanup.

## How It Works

### Pattern Extractor

`pattern_extractor.py` now includes normalization methods:

```python
class PatternExtractor:
    @staticmethod
    def normalize_technology_name(name):
        """Normalize technology names to prevent duplicates."""
        return name.strip().lower()
    
    @staticmethod
    def normalize_constraint(constraint):
        """Normalize constraint rules."""
        return constraint.strip().lower().replace(' ', '_')
```

These are called automatically in `_store_pattern()` before data reaches Neo4j.

### LLM Output

The LLM may return inconsistent casing:

```json
{
  "technologies": [
    {"name": "TypeScript", "role": "Primary"},
    {"name": "SQLite", "role": "CACHE"}
  ]
}
```

The normalization layer converts this to:

```json
{
  "technologies": [
    {"name": "typescript", "role": "primary"},
    {"name": "sqlite", "role": "cache"}
  ]
}
```

## Benefits

1. **Consistency**: All data stored in uniform format
2. **Deduplication**: No duplicate nodes or relationships
3. **Accuracy**: Better pattern matching and queries
4. **Maintainability**: Easier to manage and query graph

## Testing

After running setup, extract a new pattern:

```powershell
python pattern_extraction_pipeline\test_pattern_extraction.py
```

Verify in Neo4j Browser:

```cypher
// All technologies should be lowercase
MATCH (t:Technology)
RETURN t.name
ORDER BY t.name

// All constraints should be lowercase_snake_case
MATCH (c:Constraint)
RETURN c.rule
ORDER BY c.rule

// No pattern should have >1 relationship to same technology
MATCH (p:Pattern)-[r:USES]->(t:Technology)
WITH p, t, count(r) AS rel_count
WHERE rel_count > 1
RETURN p.name, t.name, rel_count
LIMIT 5
```

## Research Sources

Best practices based on:
- [Biotech Knowledge Graphs: Architecture for Data Integration](https://intuitionlabs.ai/articles/biotech-knowledge-graph-architecture)
  - "This normalization is essential to avoid duplicate nodes"
  - Emphasis on global identifiers and semantic harmonization
- [User-Demand-Driven Framework (Nature)](https://www.nature.com/articles/s40494-025-02188-7)
  - Global ID binding for cross-media entities
  - Semantic equivalence via unified identifiers

## Future Enhancements

### Add More Normalization

```python
@staticmethod
def normalize_pattern_name(name):
    """Normalize pattern names."""
    return name.strip().lower().replace('-', '_')

@staticmethod
def normalize_domain(domain):
    """Normalize requirement domains."""
    return domain.strip().lower()
```

### LLM Prompt Engineering

Add to prompt template:

```
IMPORTANT: Return all technology names in lowercase:
- Correct: "react", "typescript", "sqlite"
- Incorrect: "React", "TypeScript", "SQLite"

Return all constraint rules in lowercase snake_case:
- Correct: "filesystem_is_source_of_truth"
- Incorrect: "Filesystem is source of truth"
```

This reduces post-processing but normalization layer still needed as fallback.

## Maintenance

Run `setup_data_quality.py` periodically to:
- Detect new duplicates
- Normalize new data
- Verify constraints are active

```powershell
# Run weekly
python pattern_extraction_pipeline\setup_data_quality.py
```
