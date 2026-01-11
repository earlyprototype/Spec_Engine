# Issue Mining Extension: Troubleshooting & Pattern Validation

**Status:** PROPOSAL - Enhancement to Pattern Extraction Pipeline  
**Date:** 3 January 2026  
**Parent:** Pattern Extraction Pipeline v1.0

---

## Executive Summary

**Current limitation:** Pattern extraction only analyses successful implementations (code + README). Missing critical data: **why implementations fail, common pitfalls, and real-world troubleshooting.**

**This extension:** Mine GitHub Issues, Pull Requests, and Discussions to extract:
1. **Troubleshooting knowledge** - Common problems and their solutions
2. **Anti-patterns** - What fails and why (from bug reports)
3. **Pattern validation** - Increase confidence for low-confidence patterns
4. **Evolution tracking** - How patterns change over time

**Value proposition:**
- When SPEC diverges: Query similar issues and proven solutions
- When confidence is low: Validate pattern against community discussions
- When implementation fails: Access troubleshooting database
- Continuous improvement: Patterns learn from real failures

## The Problem

### Current State: Success-Only Learning

Our pattern extraction pipeline learns from **successful implementations**:
- ✓ What architectures work
- ✓ What technologies are used
- ✓ What constraints apply

But it **misses failure modes**:
- ✗ Why patterns fail in specific contexts
- ✗ Common implementation mistakes
- ✗ Edge cases and gotchas
- ✗ Migration challenges
- ✗ Performance bottlenecks

### Real Example: Dashboard SPEC Divergence

**What happened:**
- Pattern: `database_primary_storage` (database-centric file management)
- Result: Failed (filesystem was actually primary)

**What we learned from code:** Database pattern works for CRUD apps

**What we'd learn from issues:**
- Issue #342: "Database sync with filesystem causes data loss"
- Issue #891: "Performance degradation when filesystem changes"
- Issue #1204: "Race conditions between DB and file updates"
- **Solution:** Use `filesystem_browser` pattern instead

## The Extension: Issue Mining Pipeline

### Three-Layer Architecture (Extended)

```
Layer 1: GitHub API
  ├─ Repositories (existing)
  ├─ Issues (NEW)
  ├─ Pull Requests (NEW)
  └─ Discussions (NEW)
         ↓
Layer 2: LLM Analysis
  ├─ Pattern extraction (existing)
  ├─ Issue analysis (NEW)
  ├─ Solution extraction (NEW)
  └─ Anti-pattern detection (NEW)
         ↓
Layer 3: Neo4j Graph
  ├─ Patterns (existing)
  ├─ Requirements (existing)
  ├─ Technologies (existing)
  ├─ Constraints (existing)
  ├─ Issues (NEW)
  ├─ Solutions (NEW)
  ├─ AntiPatterns (NEW)
  └─ Evolution (NEW)
```

### New Node Types

```cypher
// Issue node
(Issue {
    id: "repo/issue/123",
    title: "Database sync causes data loss",
    description: "When filesystem changes...",
    labels: ["bug", "data-loss"],
    created: datetime(),
    closed: datetime(),
    resolution: "use filesystem_browser instead"
})

// Solution node
(Solution {
    id: "solution_123",
    approach: "Switch to filesystem_browser pattern",
    reasoning: "Database cannot be source of truth for files",
    source: "repo/issue/123",
    upvotes: 42
})

// AntiPattern node (enhanced)
(AntiPattern {
    name: "database_primary_file_storage",
    why_fails: "Cannot sync filesystem changes reliably",
    evidence: ["issue/123", "issue/342", "issue/891"],
    frequency: 47,  // How many times reported
    severity: "high"
})

// Evolution node
(Evolution {
    pattern_name: "filesystem_browser",
    version: "2.0",
    change: "Added real-time watch support",
    reason: "Performance issues in v1.0",
    source: "PR/456",
    date: datetime()
})
```

### New Relationships

```cypher
// Issues
(Pattern)-[:HAS_ISSUE]->(Issue)
(Issue)-[:SOLVED_BY]->(Solution)
(Issue)-[:INDICATES]->(AntiPattern)
(Solution)-[:RECOMMENDS]->(Pattern)

// Evolution
(Pattern)-[:EVOLVED_TO]->(Pattern)
(Evolution)-[:ADDRESSED]->(Issue)

// Troubleshooting
(Requirement)-[:COMMON_ISSUES]->(Issue)
(Constraint)-[:VIOLATED_IN]->(Issue)
```

## Use Cases

### Use Case 1: Low Confidence Pattern Validation

**Scenario:** LLM extracts pattern with "low" confidence

**Current behavior:**
```python
pattern = {
    'pattern_name': 'hybrid_sync_manager',
    'confidence': 'low',  # Unclear from README
    'reasoning': 'Architecture not well documented'
}
```

**Enhanced behavior:**

```python
# After extraction, validate against issues
issues = github.search_issues(
    repo=pattern['source_repo'],
    labels=['architecture', 'design']
)

# Analyze discussions
discussions = analyze_architecture_discussions(issues)

# Update confidence
if discussions['confirms_pattern']:
    pattern['confidence'] = 'medium'
    pattern['reasoning'] += f" (validated by {len(issues)} discussions)"
    pattern['validation_source'] = [i.url for i in issues]
```

**Result:** Confidence increased from "low" to "medium" with evidence

---

### Use Case 2: SPEC Divergence Troubleshooting

**Scenario:** Dashboard SPEC diverges (database-centric instead of filesystem-centric)

**Current behavior:**
```
⚠ ARCHITECTURAL DIVERGENCE DETECTED
  Selected: database_primary_storage
  Recommended: filesystem_browser
Continue anyway? (yes/no)
```

**Enhanced behavior:**

```python
# Query for similar issues
issues = query.find_related_issues({
    'attempted_pattern': 'database_primary_storage',
    'context': 'file_system',
    'problem': 'data_management'
})

# Display troubleshooting
print("⚠ ARCHITECTURAL DIVERGENCE DETECTED")
print("  Selected: database_primary_storage")
print("  Recommended: filesystem_browser")
print()
print("Common issues with database_primary_storage for files:")
for issue in issues[:3]:
    print(f"  • {issue['title']}")
    print(f"    Problem: {issue['problem']}")
    print(f"    Solution: {issue['solution']}")
    print(f"    Source: {issue['source']}")
    print()

# Example output:
# • Database sync causes data loss (47 occurrences)
#   Problem: Filesystem changes not reflected in DB
#   Solution: Use filesystem_browser pattern
#   Source: https://github.com/example/repo/issues/123
```

**Result:** User sees **why** the divergence is problematic with real evidence

---

### Use Case 3: Implementation Troubleshooting

**Scenario:** SPEC execution fails during implementation

**Current behavior:**
```python
# SPECLet 3 failed: File synchronization error
# (no additional guidance)
```

**Enhanced behavior:**

```python
# Extract error details
error_context = {
    'pattern': 'database_primary_storage',
    'error_type': 'synchronization_error',
    'component': 'file_watcher'
}

# Query troubleshooting database
solutions = query.find_solutions(error_context)

print("=== Troubleshooting Suggestions ===")
print(f"Error: {error_context['error_type']}")
print(f"Pattern: {error_context['pattern']}")
print()
print("Found 3 similar issues with solutions:")

for sol in solutions[:3]:
    print(f"\n{sol['issue_title']}")
    print(f"  Frequency: Reported {sol['frequency']} times")
    print(f"  Solution: {sol['solution']}")
    print(f"  Alternative pattern: {sol['recommended_pattern']}")
    print(f"  Source: {sol['source_url']}")
```

**Result:** Actionable troubleshooting from real-world failures

---

### Use Case 4: Anti-Pattern Detection

**Scenario:** User attempts known anti-pattern

**Current behavior:**
```python
# No anti-pattern detection (only pattern recommendations)
```

**Enhanced behavior:**

```python
# During pre-flight check
anti_patterns = query.find_anti_patterns({
    'type': 'data_management',
    'domain': 'file_system',
    'selected_pattern': 'database_primary_storage'
})

if anti_patterns:
    print("⚠ ANTI-PATTERN DETECTED")
    for ap in anti_patterns:
        print(f"\nPattern: {ap['name']}")
        print(f"Why it fails: {ap['why_fails']}")
        print(f"Reported: {ap['frequency']} times across {len(ap['evidence'])} repos")
        print(f"Severity: {ap['severity']}")
        print(f"\nEvidence:")
        for evidence in ap['evidence'][:3]:
            print(f"  • {evidence['title']} ({evidence['repo']})")
        print(f"\nRecommended instead: {ap['alternative']}")
```

**Result:** User sees concrete evidence of why approach will fail

---

## Implementation

### Phase 1: Issue Mining (Week 7)

**New file:** `issue_miner.py`

```python
# issue_miner.py
# Mine GitHub Issues for troubleshooting knowledge

from github import Github
from openai import OpenAI
from neo4j import GraphDatabase
import os

class IssueMiner:
    def __init__(self):
        self.github = Github(os.getenv("GITHUB_TOKEN"))
        self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.neo4j = GraphDatabase.driver(
            os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            auth=(os.getenv("NEO4J_USER", "neo4j"), 
                  os.getenv("NEO4J_PASSWORD", "password"))
        )
    
    def mine_issues(self, repo_name, pattern_name):
        """
        Mine issues for a specific repository and pattern.
        
        Args:
            repo_name: Full repo name (e.g., "microsoft/vscode")
            pattern_name: Pattern to validate (e.g., "filesystem_browser")
        
        Returns:
            Dict with issues, solutions, anti-patterns
        """
        repo = self.github.get_repo(repo_name)
        
        # Get closed issues (they have solutions)
        issues = repo.get_issues(
            state='closed',
            labels=['bug', 'architecture', 'design']
        )
        
        results = {
            'anti_patterns': [],
            'solutions': [],
            'validations': []
        }
        
        for issue in list(issues)[:50]:  # Limit to 50 most relevant
            # Analyze with LLM
            analysis = self._analyze_issue(
                issue=issue,
                pattern_name=pattern_name,
                repo_name=repo_name
            )
            
            if analysis:
                # Categorize
                if analysis['type'] == 'anti_pattern':
                    results['anti_patterns'].append(analysis)
                elif analysis['type'] == 'solution':
                    results['solutions'].append(analysis)
                elif analysis['type'] == 'validation':
                    results['validations'].append(analysis)
                
                # Store in graph
                self._store_issue(analysis)
        
        return results
    
    def _analyze_issue(self, issue, pattern_name, repo_name):
        """Use LLM to analyze issue."""
        
        # Get issue content
        title = issue.title
        body = issue.body[:2000] if issue.body else ""
        comments = [c.body[:500] for c in list(issue.get_comments())[:5]]
        labels = [l.name for l in issue.labels]
        
        # LLM analysis
        prompt = f"""
        Analyze this GitHub issue in context of architectural pattern.
        
        Repository: {repo_name}
        Pattern: {pattern_name}
        
        Issue #{issue.number}: {title}
        Labels: {labels}
        
        Body:
        {body}
        
        Comments:
        {' '.join(comments)}
        
        Determine:
        1. Does this indicate an anti-pattern? (pattern that fails)
        2. Does this provide a solution to a problem?
        3. Does this validate/invalidate the pattern?
        
        Extract in JSON format:
        {{
            "type": "anti_pattern" | "solution" | "validation" | "irrelevant",
            "pattern_affected": "{pattern_name}",
            "problem": "Brief description of problem",
            "solution": "Brief description of solution",
            "why_fails": "Why pattern fails (if anti-pattern)",
            "recommended_instead": "Better pattern",
            "confidence": "high" | "medium" | "low",
            "severity": "high" | "medium" | "low"
        }}
        
        If irrelevant to architecture, return {{"type": "irrelevant"}}.
        """
        
        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        analysis = json.loads(response.choices[0].message.content)
        
        if analysis['type'] == 'irrelevant':
            return None
        
        # Add metadata
        analysis['issue_id'] = f"{repo_name}/issues/{issue.number}"
        analysis['issue_url'] = issue.html_url
        analysis['issue_title'] = title
        analysis['created'] = issue.created_at
        analysis['closed'] = issue.closed_at
        
        return analysis
    
    def _store_issue(self, analysis):
        """Store issue analysis in Neo4j."""
        
        with self.neo4j.session() as session:
            if analysis['type'] == 'anti_pattern':
                # Create or update anti-pattern
                session.run("""
                    MERGE (ap:AntiPattern {name: $name})
                    ON CREATE SET
                        ap.why_fails = $why_fails,
                        ap.severity = $severity,
                        ap.frequency = 1,
                        ap.evidence = [$issue_url]
                    ON MATCH SET
                        ap.frequency = ap.frequency + 1,
                        ap.evidence = ap.evidence + $issue_url
                    
                    // Link to pattern it affects
                    WITH ap
                    MATCH (p:Pattern {name: $pattern})
                    MERGE (p)-[:HAS_ANTI_PATTERN]->(ap)
                    
                    // Create issue node
                    CREATE (i:Issue {
                        id: $issue_id,
                        title: $title,
                        url: $issue_url,
                        type: 'anti_pattern',
                        problem: $problem,
                        severity: $severity
                    })
                    
                    CREATE (i)-[:INDICATES]->(ap)
                """,
                    name=analysis['pattern_affected'] + "_anti",
                    why_fails=analysis['why_fails'],
                    severity=analysis['severity'],
                    issue_url=analysis['issue_url'],
                    pattern=analysis['pattern_affected'],
                    issue_id=analysis['issue_id'],
                    title=analysis['issue_title'],
                    problem=analysis['problem']
                )
            
            elif analysis['type'] == 'solution':
                # Create solution node
                session.run("""
                    CREATE (s:Solution {
                        id: $issue_id + '_solution',
                        approach: $solution,
                        problem: $problem,
                        source: $issue_url,
                        confidence: $confidence
                    })
                    
                    // Link to pattern
                    WITH s
                    MATCH (p:Pattern {name: $pattern})
                    MERGE (s)-[:SOLVES_ISSUE_WITH]->(p)
                    
                    // Create issue node
                    CREATE (i:Issue {
                        id: $issue_id,
                        title: $title,
                        url: $issue_url,
                        type: 'solution',
                        problem: $problem
                    })
                    
                    CREATE (i)-[:SOLVED_BY]->(s)
                """,
                    issue_id=analysis['issue_id'],
                    solution=analysis['solution'],
                    problem=analysis['problem'],
                    issue_url=analysis['issue_url'],
                    confidence=analysis['confidence'],
                    pattern=analysis.get('recommended_instead', analysis['pattern_affected']),
                    title=analysis['issue_title']
                )

# Usage
if __name__ == "__main__":
    miner = IssueMiner()
    
    # Mine issues for a repo
    results = miner.mine_issues(
        repo_name="microsoft/vscode",
        pattern_name="filesystem_browser"
    )
    
    print(f"Found {len(results['anti_patterns'])} anti-patterns")
    print(f"Found {len(results['solutions'])} solutions")
    print(f"Found {len(results['validations'])} validations")
```

### Phase 2: Query Enhancement (Week 7)

**Update:** `query_patterns.py`

```python
# Add to PatternQuery class

def find_related_issues(self, context):
    """
    Find issues related to a pattern/context.
    
    Args:
        context: dict with pattern, problem, domain
    
    Returns:
        List of related issues with solutions
    """
    with self.neo4j.session() as session:
        result = session.run("""
            MATCH (p:Pattern {name: $pattern})
            MATCH (p)-[:HAS_ISSUE]->(i:Issue)
            MATCH (i)-[:SOLVED_BY]->(s:Solution)
            
            RETURN 
                i.title AS issue_title,
                i.problem AS problem,
                i.url AS source_url,
                s.approach AS solution,
                s.confidence AS confidence
            
            ORDER BY s.confidence DESC
            LIMIT 10
        """,
            pattern=context['attempted_pattern']
        )
        
        return [dict(record) for record in result]

def find_anti_patterns_with_evidence(self, requirements):
    """
    Enhanced anti-pattern detection with evidence.
    
    Args:
        requirements: dict with type, domain, selected_pattern
    
    Returns:
        List of anti-patterns with issue evidence
    """
    with self.neo4j.session() as session:
        result = session.run("""
            MATCH (p:Pattern {name: $selected_pattern})
            MATCH (p)-[:HAS_ANTI_PATTERN]->(ap:AntiPattern)
            MATCH (i:Issue)-[:INDICATES]->(ap)
            
            WITH ap, collect({
                title: i.title,
                url: i.url,
                problem: i.problem,
                severity: i.severity
            }) as evidence
            
            RETURN 
                ap.name AS name,
                ap.why_fails AS why_fails,
                ap.frequency AS frequency,
                ap.severity AS severity,
                ap.alternative AS alternative,
                evidence
            
            ORDER BY ap.frequency DESC
        """,
            selected_pattern=requirements['selected_pattern']
        )
        
        return [dict(record) for record in result]

def validate_low_confidence_pattern(self, pattern_name):
    """
    Validate a low-confidence pattern using issue analysis.
    
    Args:
        pattern_name: Name of pattern to validate
    
    Returns:
        Dict with validation result and updated confidence
    """
    with self.neo4j.session() as session:
        result = session.run("""
            MATCH (p:Pattern {name: $pattern_name})
            MATCH (i:Issue {type: 'validation'})-[:VALIDATES]->(p)
            
            WITH p, count(i) as validation_count
            
            RETURN 
                p.confidence AS original_confidence,
                validation_count,
                CASE 
                    WHEN validation_count > 10 THEN 'high'
                    WHEN validation_count > 5 THEN 'medium'
                    ELSE p.confidence
                END AS updated_confidence
        """,
            pattern_name=pattern_name
        )
        
        record = result.single()
        return dict(record) if record else None
```

### Phase 3: Integration (Week 8)

**Update pre-flight validation** in `exe_template.md`:

```python
# Enhanced pre-flight with issue mining

def enhanced_validation(spec_descriptor):
    """Validate with anti-pattern detection."""
    
    params = load_toml(f'parameters_{spec_descriptor}.toml')
    arch = params.get('architecture_validation', {})
    
    # Standard pattern query
    query = PatternQuery()
    recommendations = query.recommend_pattern(params['requirements'])
    
    # NEW: Check for anti-patterns with evidence
    anti_patterns = query.find_anti_patterns_with_evidence({
        'selected_pattern': arch['selected_pattern'],
        'type': params['requirements']['type'],
        'domain': params['requirements']['domain']
    })
    
    if anti_patterns:
        print("⚠ ANTI-PATTERN DETECTED")
        for ap in anti_patterns[:1]:  # Show top anti-pattern
            print(f"\nPattern: {ap['name']}")
            print(f"Why it fails: {ap['why_fails']}")
            print(f"Reported: {ap['frequency']} times")
            print(f"Severity: {ap['severity']}")
            print(f"\nEvidence from real issues:")
            for ev in ap['evidence'][:3]:
                print(f"  • {ev['title']}")
                print(f"    {ev['problem']}")
                print(f"    Source: {ev['url']}")
            print(f"\nRecommended alternative: {ap['alternative']}")
        
        proceed = input("\nThis pattern has known issues. Continue? (yes/no): ")
        if proceed.lower() != 'yes':
            return False
    
    # NEW: If low confidence, try to validate
    if arch.get('pattern_confidence') == 'low':
        validation = query.validate_low_confidence_pattern(arch['selected_pattern'])
        if validation:
            print(f"Pattern validated by {validation['validation_count']} community discussions")
            print(f"Confidence updated: {validation['original_confidence']} → {validation['updated_confidence']}")
            arch['pattern_confidence'] = validation['updated_confidence']
            save_toml(f'parameters_{spec_descriptor}.toml', params)
    
    return True
```

## Cost & Performance

### Additional Costs

**Issue mining (per repo):**
- Fetch 50 issues: Free (GitHub API)
- LLM analysis: 50 issues × $0.01 = **$0.50 per repo**

**Full corpus (400 repos):**
- Pattern extraction: $4 (existing)
- Issue mining: 400 × $0.50 = **$200**
- **Total: $204**

### Optimization Strategies

**1. Selective Mining**
- Only mine issues for patterns with confidence < 0.8
- Reduces cost: 400 → ~80 repos = **$40** (saving $160)

**2. Cached Mining**
- Mine once, cache results
- Only update monthly
- Incremental cost: ~$10/month

**3. Community Contributions**
- Users can submit issue analyses
- Reduces automated mining needs

### Performance

**Issue mining:** ~30 seconds per repo (50 issues)  
**Full corpus:** 400 repos × 30s = **3.3 hours**

**Parallel processing:** Can reduce to ~1 hour

## Success Metrics

### Confidence Improvement
- **Target:** 80% of low-confidence patterns validated to medium/high
- **Measure:** Compare confidence before/after issue mining

### Divergence Prevention
- **Target:** 90% of anti-patterns caught before execution
- **Measure:** Pre-flight warnings vs actual divergences

### Troubleshooting Effectiveness
- **Target:** 70% of failures have relevant solution suggestions
- **Measure:** User feedback on solution relevance

### Community Validation
- **Target:** 50+ patterns validated by issue evidence
- **Measure:** Patterns with >5 validation issues

## Rollout Plan

### Week 7: Core Implementation
- Day 1-2: Build `issue_miner.py`
- Day 3: Test on 10 repos
- Day 4: Integrate with graph
- Day 5: Update query methods

### Week 8: Integration
- Day 1-2: Enhanced pre-flight validation
- Day 3: Troubleshooting query interface
- Day 4: Documentation
- Day 5: Testing with Dashboard SPEC

### Week 9: Batch Mining
- Mine issues for full 400-pattern corpus
- Validate low-confidence patterns
- Build anti-pattern database
- Generate troubleshooting guides

### Week 10: Continuous Updates
- Automated weekly issue mining
- Community contribution workflow
- Feedback integration
- Metrics dashboard

## Example Queries

### Find Solutions for Error

```python
from query_patterns import PatternQuery

query = PatternQuery()

solutions = query.find_related_issues({
    'attempted_pattern': 'database_primary_storage',
    'problem': 'synchronization_error',
    'domain': 'file_system'
})

for sol in solutions:
    print(f"{sol['issue_title']}")
    print(f"  Solution: {sol['solution']}")
    print(f"  Confidence: {sol['confidence']}")
    print(f"  Source: {sol['source_url']}")
```

### Detect Anti-Patterns

```python
anti_patterns = query.find_anti_patterns_with_evidence({
    'selected_pattern': 'database_primary_storage',
    'type': 'data_management',
    'domain': 'file_system'
})

for ap in anti_patterns:
    print(f"Anti-pattern: {ap['name']}")
    print(f"Frequency: {ap['frequency']} reports")
    print(f"Evidence: {len(ap['evidence'])} issues")
    for ev in ap['evidence'][:3]:
        print(f"  • {ev['title']}")
```

### Validate Low Confidence

```python
validation = query.validate_low_confidence_pattern('hybrid_sync_manager')

print(f"Validated by {validation['validation_count']} discussions")
print(f"Confidence: {validation['original_confidence']} → {validation['updated_confidence']}")
```

## Next Steps

1. **Approve extension** - Decision: Add issue mining to pipeline?
2. **Optimize costs** - Use selective mining strategy ($40 vs $200)
3. **Implement Week 7** - Build `issue_miner.py`
4. **Test on 10 repos** - Validate approach
5. **Full integration** - Weeks 8-10

## Open Questions

1. **Cost optimization:** Selective mining (80 repos, $40) vs full mining (400 repos, $200)?
2. **Mining frequency:** One-time, weekly, or monthly updates?
3. **Quality control:** Human review of issue analyses?
4. **Community:** Allow user-submitted issue analyses?

## Decision Required

**Extend pattern pipeline with issue mining?**

- **Option A:** Full extension (all 400 repos, $204 total)
- **Option B:** Selective extension (low-confidence only, $44 total)
- **Option C:** POC first (10 repos, $5, validate approach)
- **Option D:** Defer (focus on core pattern library first)

---

**Recommendation:** Option C (POC) → validate value → Option B (selective)

**Rationale:** Prove value on small scale, then optimize costs with selective mining.
