# Knowledge Graph Viewing Guide

Quick reference for viewing and exploring the architectural pattern knowledge graph in Neo4j.

## Access

**Neo4j Browser:** http://localhost:7474

**Credentials:**
- Username: `neo4j`
- Password: `password`

---

## Essential Queries

### 1. View Everything

```cypher
MATCH (n)
RETURN n
LIMIT 50
```

Shows all nodes and their connections. Adjust `LIMIT` to see more/less.

---

### 2. View Complete Pattern Graph

```cypher
MATCH (r:Requirement)-[:SOLVED_BY]->(p:Pattern)
OPTIONAL MATCH (p)-[:REQUIRES]->(c:Constraint)
OPTIONAL MATCH (p)-[:USES]->(t:Technology)
RETURN r, p, c, t
LIMIT 50
```

Shows the full pattern architecture: Requirements -> Patterns -> Technologies/Constraints

---

### 3. Pattern Summary Table

```cypher
MATCH (p:Pattern)
RETURN p.name AS Pattern, 
       p.confidence AS Confidence,
       p.stars AS Stars,
       p.source_repo AS Source
ORDER BY p.stars DESC
```

Text-based table of all patterns with metadata.

---

### 4. View Specific Pattern

```cypher
MATCH (p:Pattern {name: 'microkernel_architecture'})
OPTIONAL MATCH (p)-[r1:REQUIRES]->(c:Constraint)
OPTIONAL MATCH (p)-[r2:USES]->(t:Technology)
RETURN p, r1, c, r2, t
```

Replace `'microkernel_architecture'` with any pattern name.

**Available patterns:**
- `microkernel_architecture`
- `filesystem_browser`
- `distributed_system`
- `web_scraping_framework`
- `cli_tool`
- `desktop_application`

---

### 5. Technology Usage Statistics

```cypher
MATCH (t:Technology)<-[r:USES]-(p:Pattern)
RETURN t.name AS Technology, 
       count(p) AS UsedByPatterns,
       collect(p.name) AS Patterns
ORDER BY UsedByPatterns DESC
```

Shows which technologies are most commonly used across patterns.

---

### 6. Constraint Usage Statistics

```cypher
MATCH (c:Constraint)<-[r:REQUIRES]-(p:Pattern)
RETURN c.rule AS Constraint, 
       count(p) AS UsedByPatterns,
       collect(p.name) AS Patterns
ORDER BY UsedByPatterns DESC
```

Shows which architectural constraints are most common.

---

### 7. Find Patterns by Technology

```cypher
MATCH (p:Pattern)-[:USES]->(t:Technology {name: 'typescript'})
RETURN p.name AS Pattern,
       p.confidence AS Confidence,
       p.stars AS Stars
ORDER BY p.stars DESC
```

Replace `'typescript'` with any technology (lowercase): `react`, `electron`, `sqlite`, `rust`, `go`, etc.

---

### 8. Find Patterns by Requirement Type

```cypher
MATCH (r:Requirement {type: 'data_management'})-[:SOLVED_BY]->(p:Pattern)
RETURN r.domain AS Domain,
       p.name AS Pattern,
       p.confidence AS Confidence,
       p.stars AS Stars
ORDER BY p.stars DESC
```

**Available requirement types:**
- `data_management`
- `system_architecture`
- `integration`
- `user_interface`

---

### 9. Find Similar Patterns (by shared technologies)

```cypher
MATCH (p1:Pattern {name: 'filesystem_browser'})-[:USES]->(t:Technology)<-[:USES]-(p2:Pattern)
WHERE p1 <> p2
RETURN DISTINCT p2.name AS SimilarPattern,
       collect(DISTINCT t.name) AS SharedTechnologies,
       p2.stars AS Stars
ORDER BY size(SharedTechnologies) DESC, Stars DESC
```

Replace `'filesystem_browser'` with any pattern to find similar ones.

---

### 10. Patterns with High Confidence

```cypher
MATCH (p:Pattern)
WHERE p.confidence = 'high'
RETURN p.name AS Pattern,
       p.stars AS Stars,
       p.reasoning AS Reasoning
ORDER BY p.stars DESC
```

Shows only high-confidence patterns (well-documented, clear architecture).

---

## Quick Filters

### By Star Count

```cypher
MATCH (p:Pattern)
WHERE p.stars > 10000
RETURN p.name, p.stars
ORDER BY p.stars DESC
```

### By Confidence Level

```cypher
MATCH (p:Pattern)
WHERE p.confidence IN ['high', 'medium']
RETURN p.name, p.confidence, p.stars
ORDER BY p.stars DESC
```

---

## Graph Visualization Tips

### Navigation
- **Click and drag** - Move nodes around
- **Mouse wheel** - Zoom in/out
- **Click node** - View properties in sidebar
- **Double-click node** - Expand/collapse connections
- **Right-click node** - Additional options (expand, collapse, dismiss)

### Customization
- **Click legend** (bottom) - Change node colours
- **Click relationship type** - Highlight specific connections
- **Settings (gear icon)** - Adjust visualization preferences

### Layout Options
- **Click layout icon** (top) - Choose different graph layouts:
  - Force-directed (default)
  - Hierarchical
  - Circular

---

## Node Types

| Node Type | Colour | Description |
|-----------|--------|-------------|
| **Pattern** | Purple | Architectural pattern extracted from GitHub repos |
| **Technology** | Blue | Technologies/frameworks used (react, typescript, etc.) |
| **Constraint** | Orange | Architectural constraints/rules |
| **Requirement** | Red | Problem types that patterns solve |

---

## Relationship Types

| Relationship | Direction | Meaning |
|--------------|-----------|---------|
| **SOLVED_BY** | Requirement -> Pattern | Pattern solves this requirement |
| **USES** | Pattern -> Technology | Pattern uses this technology |
| **REQUIRES** | Pattern -> Constraint | Pattern requires this constraint |

---

## Common Tasks

### 1. Explore a Requirement Domain

```cypher
MATCH path = (r:Requirement {domain: 'file_system'})-[:SOLVED_BY]->(p:Pattern)-[:USES]->(t:Technology)
RETURN path
```

### 2. Find Patterns Using Multiple Technologies

```cypher
MATCH (p:Pattern)-[:USES]->(t1:Technology {name: 'react'})
MATCH (p)-[:USES]->(t2:Technology {name: 'typescript'})
RETURN p.name AS Pattern,
       p.stars AS Stars,
       p.source_repo AS Source
```

### 3. Technology Stack for a Pattern

```cypher
MATCH (p:Pattern {name: 'desktop_application'})-[:USES]->(t:Technology)
RETURN p.name AS Pattern,
       collect({tech: t.name, role: null}) AS TechStack
```

### 4. Export Pattern Details

```cypher
MATCH (p:Pattern {name: 'microkernel_architecture'})
OPTIONAL MATCH (p)-[:USES]->(t:Technology)
OPTIONAL MATCH (p)-[:REQUIRES]->(c:Constraint)
RETURN p.name AS Pattern,
       p.confidence AS Confidence,
       p.stars AS Stars,
       p.reasoning AS Reasoning,
       collect(DISTINCT t.name) AS Technologies,
       collect(DISTINCT c.rule) AS Constraints
```

---

## Graph Statistics

### Overall Stats

```cypher
MATCH (p:Pattern) WITH count(p) AS patterns
MATCH (t:Technology) WITH patterns, count(t) AS techs
MATCH (c:Constraint) WITH patterns, techs, count(c) AS constraints
MATCH (r:Requirement) WITH patterns, techs, constraints, count(r) AS reqs
RETURN patterns AS Patterns,
       techs AS Technologies,
       constraints AS Constraints,
       reqs AS Requirements
```

### Relationship Counts

```cypher
MATCH ()-[r:USES]->() WITH 'USES' AS type, count(r) AS count
UNION
MATCH ()-[r:REQUIRES]->() WITH 'REQUIRES' AS type, count(r) AS count
UNION
MATCH ()-[r:SOLVED_BY]->() WITH 'SOLVED_BY' AS type, count(r) AS count
RETURN type AS RelationshipType, count AS Count
ORDER BY count DESC
```

### Most Connected Nodes

```cypher
MATCH (n)
RETURN labels(n)[0] AS NodeType,
       CASE 
         WHEN 'Pattern' IN labels(n) THEN n.name
         WHEN 'Technology' IN labels(n) THEN n.name
         WHEN 'Constraint' IN labels(n) THEN n.rule
         ELSE toString(id(n))
       END AS Node,
       size((n)--()) AS Connections
ORDER BY Connections DESC
LIMIT 10
```

---

## Troubleshooting

### No Results?

```cypher
// Check if data exists
MATCH (n) RETURN count(n) AS total_nodes
```

If 0, run pattern extraction: `python pattern_extractor.py`

### Graph Too Cluttered?

Add `LIMIT` to queries:
```cypher
MATCH (n) RETURN n LIMIT 10
```

### Can't See Relationships?

Make sure you're returning both nodes AND relationships:
```cypher
// Good
MATCH (p:Pattern)-[r:USES]->(t:Technology)
RETURN p, r, t

// Bad - only returns nodes
MATCH (p:Pattern)-[:USES]->(t:Technology)
RETURN p, t
```

### Slow Query?

Use indexes (already created via constraints):
```cypher
// Check existing constraints/indexes
SHOW CONSTRAINTS
```

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl + Enter` | Run query |
| `Ctrl + Up/Down` | Navigate query history |
| `Esc` | Clear graph |
| `Ctrl + K` | Clear editor |

---

## Export Data

### Export as JSON

```cypher
MATCH (p:Pattern)
OPTIONAL MATCH (p)-[:USES]->(t:Technology)
OPTIONAL MATCH (p)-[:REQUIRES]->(c:Constraint)
RETURN {
  pattern: p.name,
  confidence: p.confidence,
  stars: p.stars,
  source: p.source_repo,
  technologies: collect(DISTINCT t.name),
  constraints: collect(DISTINCT c.rule)
} AS pattern_data
```

Click "Export" button (top right) -> "JSON"

### Export as CSV

Click "Export" button -> "CSV" after running any query.

---

## Advanced: Pathfinding

### Shortest Path Between Patterns

```cypher
MATCH (p1:Pattern {name: 'filesystem_browser'}),
      (p2:Pattern {name: 'desktop_application'}),
      path = shortestPath((p1)-[*]-(p2))
RETURN path
```

Shows how two patterns are connected (via shared technologies/constraints).

### All Paths from Requirement to Technologies

```cypher
MATCH path = (r:Requirement {type: 'data_management'})-[:SOLVED_BY]->(p:Pattern)-[:USES]->(t:Technology)
RETURN path
LIMIT 20
```

---

## Quick Reference Card

**Most Useful Queries:**

1. **See everything:** `MATCH (n) RETURN n LIMIT 50`
2. **Pattern list:** `MATCH (p:Pattern) RETURN p.name, p.stars ORDER BY p.stars DESC`
3. **View pattern:** `MATCH (p:Pattern {name: 'X'})-[r]->(n) RETURN p, r, n`
4. **Find by tech:** `MATCH (p:Pattern)-[:USES]->(:Technology {name: 'X'}) RETURN p.name, p.stars`
5. **Graph stats:** `MATCH (n) RETURN labels(n)[0] AS type, count(n) AS count`

---

## Need Help?

- **Neo4j Cypher Docs:** https://neo4j.com/docs/cypher-manual/current/
- **Pattern Extraction Pipeline:** See `README.md` in this directory
- **Data Quality Issues:** Run `python verify_data_quality.py`
- **Add More Patterns:** Run `python pattern_extractor.py`

---

**Version:** 1.0  
**Last Updated:** 2026-01-02
