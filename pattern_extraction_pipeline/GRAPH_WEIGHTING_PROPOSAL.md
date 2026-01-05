# Knowledge Graph Weighting & Quality Scoring

**Making the graph smarter through multi-dimensional weighting**

---

## Current State

### What We Have Now

**Node Properties:**
- `Pattern.stars` - GitHub stars (popularity)
- `Pattern.confidence` - LLM confidence (high/medium/low)

**Relationship Properties:**
- `USES.role` - Technology role (primary/cache/utility)

**Problems:**
- Stars don't measure quality (viral repos vs solid engineering)
- No recency weighting (5-year-old pattern vs fresh)
- No maintenance indicators (active vs abandoned)
- No technology compatibility scoring
- No constraint criticality levels
- All patterns treated equally regardless of production-readiness

---

## Proposed Enhancements

### 1. Pattern Quality Score (Composite Metric)

Instead of just stars, calculate a **quality score** from multiple signals:

```python
quality_score = (
    popularity_score * 0.30 +      # Stars, forks, watchers
    maintenance_score * 0.25 +     # Recent commits, issue response time
    maturity_score * 0.20 +        # Age, number of releases
    community_score * 0.15 +       # Contributors, documentation quality
    reliability_score * 0.10       # Test coverage, CI/CD presence
)
```

**Metrics to extract:**

```python
{
    # Popularity (30%)
    'stars': 8500,
    'forks': 1200,
    'watchers': 450,
    'downloads': 50000,  # from package manager if applicable
    
    # Maintenance (25%)
    'last_commit_days_ago': 7,
    'commit_frequency': 45,  # commits/month
    'open_issues': 23,
    'closed_issues': 450,
    'issue_response_time_hours': 12,
    
    # Maturity (20%)
    'repo_age_months': 36,
    'release_count': 24,
    'major_version': 3,
    'breaking_changes': 2,  # last year
    
    # Community (15%)
    'contributors': 45,
    'has_documentation': True,
    'has_contributing_guide': True,
    'has_license': 'MIT',
    
    # Reliability (10%)
    'has_tests': True,
    'has_ci': True,
    'test_coverage': 85,  # if available
    'has_security_policy': True
}
```

### 2. Recency/Freshness Score

Weight patterns by how recent they are:

```python
recency_score = {
    '0-6 months': 1.0,    # Fresh, likely using current best practices
    '6-12 months': 0.9,   # Recent
    '1-2 years': 0.75,    # Still relevant
    '2-3 years': 0.5,     # May be outdated
    '3+ years': 0.3       # Likely deprecated patterns
}
```

**Store in Pattern node:**
```cypher
CREATE (p:Pattern {
    created_at: date('2024-06-15'),
    last_updated: date('2026-01-05'),
    freshness_score: 0.95
})
```

### 3. Technology Relationship Weights

Instead of just `role`, add **criticality and compatibility**:

```cypher
(Pattern)-[u:USES {
    role: 'primary',              # existing
    criticality: 0.9,             # NEW: 0-1, how critical is this tech?
    can_substitute: ['vue', 'svelte'],  # NEW: alternative techs
    version_range: '^17.0.0',     # NEW: version compatibility
    adoption_confidence: 0.85     # NEW: how proven is this choice?
}]->(Technology)
```

**Example:**
```python
{
    'name': 'react',
    'role': 'primary',
    'criticality': 0.95,  # Core to the pattern
    'can_substitute': ['vue', 'preact'],  # Alternatives
    'version_range': '^18.0.0',
    'adoption_confidence': 0.95  # Very proven choice
}

{
    'name': 'lodash',
    'role': 'utility',
    'criticality': 0.3,  # Nice to have, not critical
    'can_substitute': ['ramda', 'native-es6'],
    'adoption_confidence': 0.7  # Could use alternatives
}
```

### 4. Constraint Criticality

Not all constraints are equally important:

```cypher
(Pattern)-[r:REQUIRES {
    criticality: 'must',          # must / should / nice-to-have
    enforcement: 'architectural', # architectural / implementation / style
    violation_impact: 'high'      # high / medium / low
}]->(Constraint)
```

**Example:**
```python
{
    'constraint': 'filesystem_is_source_of_truth',
    'criticality': 'must',        # Violating this breaks the pattern
    'enforcement': 'architectural',
    'violation_impact': 'high',
    'reasoning': 'Core architectural principle for data integrity'
}

{
    'constraint': 'use_typescript',
    'criticality': 'should',      # Recommended but not required
    'enforcement': 'implementation',
    'violation_impact': 'medium',
    'reasoning': 'Improves maintainability but JavaScript works'
}
```

### 5. Pattern Similarity Scores

Create relationships between similar patterns:

```cypher
(Pattern1)-[s:SIMILAR_TO {
    similarity_score: 0.85,       # 0-1 based on tech/constraint overlap
    shared_technologies: 4,
    shared_constraints: 2,
    use_case_overlap: 'high'
}]->(Pattern2)
```

**Use case:** "If this pattern doesn't work, try these similar ones"

### 6. Domain Authority Score

Weight requirement domains by how well-represented they are:

```cypher
(Requirement {
    type: 'data_management',
    domain: 'file_system',
    pattern_count: 12,            # How many patterns solve this?
    avg_quality_score: 0.78,      # Average quality of solutions
    domain_maturity: 'established' # established / emerging / experimental
})
```

### 7. Technology Popularity Trends

Track technology usage across patterns:

```cypher
(Technology {
    name: 'react',
    pattern_count: 45,            # Used in 45 patterns
    avg_pattern_quality: 0.82,    # Quality of patterns using this
    trend: 'stable',              # growing / stable / declining
    first_seen: date('2023-01-15'),
    last_seen: date('2026-01-05'),
    ecosystem_maturity: 'mature'  # mature / developing / experimental
})
```

---

## Implementation: Enhanced Extraction

### Update Pattern Extractor

```python
def _extract_with_llm(self, repo, **kwargs):
    """Enhanced extraction with quality metrics."""
    
    # Get additional GitHub metrics
    quality_metrics = self._calculate_quality_metrics(repo)
    
    prompt = f"""
    Analyze this repository and extract architectural pattern with WEIGHTS.
    
    Repository: {repo.full_name}
    Quality Metrics:
    - Stars: {repo.stargazers_count}
    - Last updated: {repo.updated_at}
    - Open issues: {repo.open_issues_count}
    - Contributors: {repo.get_contributors().totalCount}
    
    Extract in JSON with CRITICALITY SCORES:
    {{
        "pattern_name": "filesystem_browser",
        "confidence": "high",
        
        "technologies": [
            {{
                "name": "react",
                "role": "primary",
                "criticality": 0.95,  # 0-1: how critical is this tech?
                "can_substitute": ["vue", "preact"],
                "adoption_confidence": 0.9  # how proven is this choice?
            }}
        ],
        
        "constraints": [
            {{
                "rule": "filesystem_is_source_of_truth",
                "criticality": "must",  # must / should / nice-to-have
                "enforcement": "architectural",
                "violation_impact": "high",
                "reasoning": "why this constraint matters"
            }}
        ]
    }}
    """
    
    # ... LLM extraction ...
    
    # Add calculated metrics
    pattern['quality_score'] = quality_metrics['composite_score']
    pattern['freshness_score'] = quality_metrics['freshness_score']
    pattern['maintenance_score'] = quality_metrics['maintenance_score']
    
    return pattern
```

### Store Enhanced Data

```python
def _store_pattern(self, pattern):
    """Store pattern with full weighting."""
    
    with self.neo4j.session() as session:
        session.run("""
            CREATE (p:Pattern {
                name: $pattern_name,
                confidence: $confidence,
                source_repo: $source_repo,
                
                // Enhanced metrics
                stars: $stars,
                quality_score: $quality_score,
                freshness_score: $freshness_score,
                maintenance_score: $maintenance_score,
                
                // Timestamps
                extracted_at: datetime(),
                repo_last_updated: $repo_last_updated,
                
                // Metadata
                repo_age_months: $repo_age_months,
                contributor_count: $contributor_count
            })
            
            // Technologies with weights
            WITH p
            UNWIND $technologies AS tech
            MERGE (t:Technology {name: tech.name})
            MERGE (p)-[u:USES]->(t)
            SET u.role = tech.role,
                u.criticality = tech.criticality,
                u.adoption_confidence = tech.adoption_confidence,
                u.can_substitute = tech.can_substitute
            
            // Constraints with criticality
            WITH p
            UNWIND $constraints AS constraint
            MERGE (c:Constraint {rule: constraint.rule})
            MERGE (p)-[r:REQUIRES]->(c)
            SET r.criticality = constraint.criticality,
                r.enforcement = constraint.enforcement,
                r.violation_impact = constraint.violation_impact,
                r.reasoning = constraint.reasoning
        """, ...)
```

---

## Query Interface Enhancements

### Weighted Pattern Ranking

```python
def find_patterns_for_spec(self, spec_dict, top_k=5):
    """Find patterns with sophisticated scoring."""
    
    with self.neo4j.session() as session:
        result = session.run("""
            MATCH (r:Requirement)-[:SOLVED_BY]->(p:Pattern)
            OPTIONAL MATCH (p)-[u:USES]->(t:Technology)
            
            // Calculate composite relevance score
            WITH p, r,
                 // Quality component (40%)
                 p.quality_score * 0.4 AS quality_weight,
                 
                 // Freshness component (20%)
                 p.freshness_score * 0.2 AS freshness_weight,
                 
                 // Maintenance component (20%)
                 p.maintenance_score * 0.2 AS maintenance_weight,
                 
                 // Technology match component (20%)
                 CASE 
                   WHEN t.name IN $preferred_techs 
                   THEN 0.2 
                   ELSE 0.1 
                 END AS tech_match_weight
            
            WITH p, r,
                 (quality_weight + freshness_weight + 
                  maintenance_weight + tech_match_weight) AS relevance_score
            
            ORDER BY relevance_score DESC
            LIMIT $top_k
            
            RETURN p, r, relevance_score
        """, ...)
```

### Technology Recommendations

```python
def recommend_technologies(self, requirement_type, domain):
    """Recommend technologies with confidence scores."""
    
    with self.neo4j.session() as session:
        result = session.run("""
            MATCH (r:Requirement {type: $req_type, domain: $domain})
                  -[:SOLVED_BY]->(p:Pattern)
                  -[u:USES]->(t:Technology)
            
            // Weight by pattern quality and tech criticality
            WITH t,
                 AVG(p.quality_score * u.criticality) AS weighted_score,
                 COUNT(p) AS pattern_count,
                 AVG(u.adoption_confidence) AS avg_confidence,
                 COLLECT(DISTINCT p.name) AS patterns
            
            WHERE pattern_count >= 2  // At least 2 patterns use this
            
            RETURN t.name AS technology,
                   weighted_score,
                   pattern_count,
                   avg_confidence,
                   patterns
            ORDER BY weighted_score DESC
        """, ...)
```

---

## Benefits

### 1. Better Recommendations
- "React is used in 5 patterns, avg quality 0.85, high adoption confidence"
- vs just "React is used in 5 patterns"

### 2. Risk Assessment
- Patterns with low maintenance scores flagged as risky
- Fresh patterns preferred over stale ones
- Alternative technologies suggested if confidence is low

### 3. Nuanced Constraints
- "Must follow" vs "should follow" vs "nice to have"
- Impact assessment if violated
- Enforcement level guidance

### 4. Technology Substitution
- "Can't use React? Try Vue or Preact (used in similar patterns)"
- Confidence scores for alternatives

### 5. Pattern Evolution Tracking
- See how patterns age over time
- Identify emerging vs declining approaches
- Track technology trend shifts

---

## Implementation Priority

### Phase 1: Core Weights (Immediate)
1. Quality score calculation
2. Technology criticality
3. Constraint criticality
4. Freshness scoring

### Phase 2: Relationship Weights (Next)
5. Technology substitution suggestions
6. Constraint enforcement levels
7. Pattern similarity scores

### Phase 3: Advanced Analytics (Future)
8. Technology trend analysis
9. Domain authority scoring
10. Predictive maintenance warnings

---

## Example: Before vs After

### Before (Basic)

```
Pattern: filesystem_browser_react
Stars: 7500
Confidence: high
Technologies: react, sqlite
Constraints: filesystem_is_source_of_truth
```

### After (Weighted)

```
Pattern: filesystem_browser_react
Quality Score: 0.87 (excellent)
  - Stars: 7500
  - Freshness: 0.95 (updated 2 weeks ago)
  - Maintenance: 0.88 (active, 12hr issue response)
  - Maturity: 0.82 (3 years old, 24 releases)

Technologies:
  - react (primary)
    Criticality: 0.95 (core to pattern)
    Adoption confidence: 0.9 (very proven)
    Can substitute: vue, preact
    
  - sqlite (cache)
    Criticality: 0.6 (important but not critical)
    Adoption confidence: 0.85
    Can substitute: indexeddb, localstorage

Constraints:
  - filesystem_is_source_of_truth
    Criticality: MUST (architectural)
    Violation impact: HIGH
    Reasoning: Core data integrity principle
    
  - use_typescript
    Criticality: SHOULD (implementation)
    Violation impact: MEDIUM
    Reasoning: Improves maintainability
```

---

**Ready to implement:** Start with Phase 1 (quality + criticality scores)

**See:** `pattern_extractor_enhanced.py` (to be created)
