# Pattern Query Interface Guide

**Making the Knowledge Graph Useful for LLM-Assisted SPEC Building**

---

## Overview

The `PatternQueryInterface` bridges the gap between your architectural pattern knowledge graph and the SPEC Engine. It provides LLM-friendly methods to:

1. Find relevant patterns when building a SPEC
2. Verify SPEC feasibility against proven patterns
3. Query patterns by technology, requirement, or natural language
4. Get recommendations during SPEC creation

---

## Quick Start

### Installation

```powershell
cd pattern_extraction_pipeline
python -m pip install google-generativeai neo4j python-dotenv
```

### Environment Setup

Ensure `.env` has:

```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
GEMINI_API_KEY=your_gemini_key
```

### Basic Usage

```python
from pattern_query_interface import PatternQueryInterface

interface = PatternQueryInterface()

# Example: Find patterns for a SPEC
spec = {
    'goal': 'Build a file browser with React',
    'tech_stack': {'frontend': 'react', 'backend': 'node'},
    'deployment_type': 'Web Application'
}

result = interface.find_patterns_for_spec(spec)

print(f"Recommended patterns: {len(result['recommended_patterns'])}")
for pattern in result['recommended_patterns']:
    print(f"  - {pattern['pattern_name']} ({pattern['stars']} stars)")

interface.close()
```

---

## Integration with SPEC Engine

### 1. During SPEC Creation

When an LLM is building a SPEC, it can query patterns to inform technology choices:

```python
# User provides: "Build an e-commerce dashboard"

spec_draft = {
    'goal': 'Build an e-commerce dashboard with real-time analytics',
    'deployment_type': 'Web Application',
    'user_type': 'shop managers'
}

# Query patterns
patterns = interface.find_patterns_for_spec(spec_draft, top_k=5)

# LLM uses patterns to suggest tech stack:
# "Based on 5 proven patterns with avg 8.5K stars, I recommend:
#  - Frontend: React (used in 4/5 patterns)
#  - Backend: Node.js + Express (3/5 patterns)
#  - Database: PostgreSQL (recommended for e-commerce domain)"
```

### 2. During SPEC Verification

After building a SPEC, verify it's feasible:

```python
verification = interface.verify_spec_feasibility(spec_dict)

if verification['feasibility_score'] < 0.5:
    print("Warning: Low feasibility score")
    print("Concerns:", verification['concerns'])
    print("Recommendations:", verification['recommendations'])
```

### 3. Technology Selection

Query patterns by specific technology:

```python
# User wants to use Flask
flask_patterns = interface.query_by_technology('flask', role='primary')

print(f"Found {len(flask_patterns)} patterns using Flask as primary framework")
for p in flask_patterns:
    print(f"  - {p['pattern_name']}: {p['reasoning']}")
```

---

## API Reference

### Primary Methods

#### `find_patterns_for_spec(spec_dict, top_k=5)`

**Purpose:** Main method for SPEC-to-Pattern matching

**Input:**
```python
spec_dict = {
    'goal': 'What you want to build',
    'tech_stack': {'language': 'python', 'framework': 'flask'},
    'deployment_type': 'Web Application',
    'user_type': 'developers'
}
```

**Output:**
```python
{
    'recommended_patterns': [
        {
            'pattern_name': 'flask_api_template',
            'confidence': 'high',
            'stars': 5000,
            'source_repo': 'https://github.com/...',
            'reasoning': 'Why this pattern matches',
            'technologies': [{'name': 'flask', 'role': 'primary'}],
            'constraints': ['stateless_api', 'jwt_authentication']
        }
    ],
    'alternative_patterns': [...],
    'technologies': {
        'flask': [pattern1, pattern2],
        'postgresql': [pattern1]
    },
    'constraints': {
        'stateless_api': [pattern1, pattern2]
    },
    'reasoning': 'Human-readable summary of why these patterns were selected'
}
```

---

#### `verify_spec_feasibility(spec_dict)`

**Purpose:** Check if SPEC is feasible based on existing patterns

**Output:**
```python
{
    'feasibility_score': 0.75,  # 0.0-1.0
    'confidence': 'high',       # high/medium/low
    'supporting_patterns': [list of patterns],
    'concerns': [
        'Limited patterns found for real-time WebSocket with Flask',
        'Consider Socket.IO or alternative framework'
    ],
    'recommendations': [
        'Use proven Flask-SocketIO library',
        'Add Redis for pub/sub scaling'
    ]
}
```

---

#### `natural_language_query(query, top_k=5)`

**Purpose:** Natural language interface for exploration

**Examples:**
```python
# Query: "Find patterns for building a file browser with React"
result = interface.natural_language_query("file browser with React")

# Query: "Show me authentication patterns using JWT"
result = interface.natural_language_query("authentication JWT")

# Output:
{
    'patterns': [list of matching patterns],
    'interpretation': 'Looking for file management patterns using React',
    'suggestions': [
        'Try: "file upload patterns"',
        'Try: "React component libraries for file management"'
    ]
}
```

---

### Direct Query Methods

#### `query_by_technology(tech_name, role=None)`

Find patterns using specific technology:

```python
# All React patterns
react_patterns = interface.query_by_technology('react')

# Patterns using SQLite as cache
cache_patterns = interface.query_by_technology('sqlite', role='cache')
```

---

#### `query_by_requirement(req_type, req_domain=None)`

Find patterns by requirement type/domain:

```python
# All data management patterns
data_patterns = interface.query_by_requirement('data_management')

# File system specific
fs_patterns = interface.query_by_requirement('data_management', 'file_system')
```

**Common requirement types:**
- `data_management`
- `ui_component`
- `api_service`
- `cli_tool`
- `real_time`
- `authentication`

**Common domains:**
- `file_system`
- `e-commerce`
- `authentication`
- `media`
- `analytics`

---

#### `query_by_constraint(constraint)`

Find patterns with specific constraints:

```python
# Patterns that follow "filesystem is source of truth"
patterns = interface.query_by_constraint('filesystem_is_source_of_truth')

# Patterns requiring JWT authentication
patterns = interface.query_by_constraint('jwt_authentication')
```

---

## Command-Line Interface

```powershell
# Query by technology
python pattern_query_interface.py --tech react

# Query by requirement
python pattern_query_interface.py --requirement data_management --domain file_system

# Natural language query
python pattern_query_interface.py --query "Find patterns for real-time chat applications"

# Verify SPEC feasibility
python pattern_query_interface.py --spec-file my_spec.json
```

---

## Integration Patterns

### Pattern 1: LLM Prompt Enhancement

**Before:**
```
User: Build me a file manager

LLM: I'll use React and Node.js. [generic response]
```

**After (with Pattern Query):**
```python
# In LLM system prompt or tool call:
patterns = interface.find_patterns_for_spec({
    'goal': 'Build a file manager',
    'deployment_type': 'Web Application'
})

# LLM response now informed by real patterns:
"Based on 3 proven patterns (avg 7K stars), I recommend:
 - Frontend: React with react-virtualized for large file lists
 - Backend: Node.js with Express
 - File handling: Use streams for large files (pattern: github.com/...)
 - Database: SQLite for metadata caching (pattern: github.com/...)"
```

---

### Pattern 2: SPEC Template Auto-Fill

When starting a new SPEC:

```python
# User provides minimal input
user_input = {
    'goal': 'Build a podcast website with audio playback'
}

# Query patterns
patterns = interface.find_patterns_for_spec(user_input, top_k=3)

# Auto-suggest SPEC fields:
suggested_spec = {
    'goal': user_input['goal'],
    'deployment_type': 'Web Application',  # inferred from patterns
    'tech_stack': {
        'language': 'TypeScript',  # most common in patterns
        'framework': 'Next.js',    # most common in patterns
        'database': 'PostgreSQL'   # recommended for media domain
    },
    'reasoning': patterns['reasoning']
}
```

---

### Pattern 3: Constraint Validation

Check if SPEC violates known constraints:

```python
spec = {
    'goal': 'Build file browser',
    'tech_stack': {'database': 'mongodb'},
    'constraints': ['filesystem_is_source_of_truth']
}

patterns = interface.find_patterns_for_spec(spec)

# If patterns suggest SQLite for metadata but user chose MongoDB:
verification = interface.verify_spec_feasibility(spec)
# Returns concern: "Proven patterns typically use SQLite for file metadata caching"
```

---

## Advanced: Custom Prompt Templates

### For SPEC Creation

```python
def build_spec_with_patterns(user_goal: str) -> dict:
    """Build a SPEC informed by proven patterns."""
    
    # Step 1: Query patterns
    patterns = interface.find_patterns_for_spec({'goal': user_goal}, top_k=5)
    
    # Step 2: Build LLM prompt
    prompt = f"""Build a SPEC for: {user_goal}

PROVEN PATTERNS (from knowledge graph):
{json.dumps(patterns['recommended_patterns'], indent=2)}

Based on these {len(patterns['recommended_patterns'])} proven patterns:
1. Suggest appropriate tech stack
2. Identify key constraints
3. Estimate feasibility

Return SPEC in standard format.
"""
    
    # Step 3: LLM generates SPEC
    spec = llm.generate_content(prompt)
    
    return spec
```

---

### For SPEC Verification

```python
def verify_and_improve_spec(spec_dict: dict) -> dict:
    """Verify SPEC and suggest improvements."""
    
    verification = interface.verify_spec_feasibility(spec_dict)
    
    if verification['feasibility_score'] < 0.7:
        prompt = f"""This SPEC has feasibility concerns:

SPEC:
{json.dumps(spec_dict, indent=2)}

FEASIBILITY ANALYSIS:
- Score: {verification['feasibility_score']}
- Concerns: {verification['concerns']}
- Recommendations: {verification['recommendations']}

SUPPORTING PATTERNS:
{json.dumps(verification['supporting_patterns'][:3], indent=2)}

Suggest specific improvements to the SPEC based on proven patterns.
"""
        
        improvements = llm.generate_content(prompt)
        return improvements
    
    return {"status": "SPEC looks good!"}
```

---

## Best Practices

### 1. Always Close Connections

```python
interface = PatternQueryInterface()
try:
    result = interface.find_patterns_for_spec(spec)
    # ... use result ...
finally:
    interface.close()
```

### 2. Handle Empty Results

```python
patterns = interface.find_patterns_for_spec(spec)

if len(patterns['recommended_patterns']) == 0:
    print("No similar patterns found - this might be a novel architecture")
    print("Consider: simpler technologies, different approach, or expand pattern corpus")
```

### 3. Use Feasibility Scores as Guidance, Not Rules

- **Score > 0.7:** High confidence, proven approach
- **Score 0.4-0.7:** Moderate confidence, consider adjustments
- **Score < 0.4:** Low confidence, significant risk or novel architecture

### 4. Expand Pattern Corpus for Better Results

The more patterns in your knowledge graph, the better recommendations:

```powershell
# Current: ~6 patterns (testing)
# Target: 100-500 patterns (production)

# Use domain_topic_selector to expand:
python domain_selector_server.py
# Then use Web UI to extract more patterns
```

---

## Troubleshooting

### "No patterns found"

**Cause:** Knowledge graph is empty or connection failed

**Solution:**
```powershell
# Check Neo4j is running
# Extract patterns first:
cd pattern_extraction_pipeline
.\launch_selector.ps1
# Use UI to extract patterns
```

### "LLM not configured"

**Cause:** Missing `GEMINI_API_KEY` in `.env`

**Solution:**
```powershell
# Add to .env:
echo "GEMINI_API_KEY=your_key_here" >> .env
```

### Low feasibility scores for valid SPECs

**Cause:** Insufficient patterns in knowledge graph for that domain

**Solution:**
1. Extract more patterns in that domain
2. Use broader requirement types
3. Check if it's genuinely a novel architecture

---

## Next Steps

1. **Expand Pattern Corpus:** Use the Web UI to extract 100+ patterns
2. **Integrate into SPEC Engine:** Add pattern query as a tool for LLMs
3. **Build SPEC Validator:** Automated feasibility checker before execution
4. **Create Pattern Browser:** Web UI to explore knowledge graph

---

**Version:** 1.0  
**Last Updated:** 2026-01-05  
**Related:** `_KG_SPEC_INTEGRATION_GUIDE.md`, `pattern_extractor.py`
