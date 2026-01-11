# Integration Guide: Using the Knowledge Graph as a Tool

How to integrate the architectural pattern knowledge graph into your SPEC_Engine workflow.

---

## 🔥 NEW: Semantic Vector Search (2026-01-07)

**The knowledge graph now supports natural language pattern discovery via semantic search!**

### What's New

- **Semantic Search:** Find patterns using natural language goal descriptions
- **Hybrid Queries:** Combine semantic similarity with technical constraints  
- **Confidence Scoring:** Patterns ranked by composite score (semantic + metadata + stars)
- **Cross-Pattern Discovery:** Find conceptually similar patterns with different tech stacks
- **Pattern-Informed SPEC Generation:** Commander queries patterns BEFORE generating SPECs

### Quick Start with Semantic Search

```python
from pattern_query_interface_semantic import PatternQueryInterfaceSemantic

interface = PatternQueryInterfaceSemantic()

# Hybrid search (semantic + structural) - RECOMMENDED
result = interface.find_patterns_hybrid(
    goal="Build a file manager for volunteers",
    constraints={
        'technologies': ['typescript', 'react'],
        'min_stars': 5000
    },
    top_k=5
)

# Present top patterns to user for review
print(result['user_review_text'])

interface.close()
```

### Documentation

- **Architecture:** See `VECTOR_ARCHITECTURE.md` for complete technical specification
- **Implementation Status:** See `IMPLEMENTATION_STATUS_VECTOR_KG.md` for what's built
- **Testing:** Run `python test_vector_search.py` and `python test_hybrid_queries.py`

### Setup Required

1. **Generate Embeddings:**
   ```bash
   python generate_pattern_embeddings.py
   ```

2. **Create Vector Index:**
   ```bash
   cypher-shell -u neo4j -p password < vector_index_setup.cypher
   ```

3. **Verify Setup:**
   ```bash
   python test_vector_search.py
   ```

### Migration Path

The semantic interface **extends** the original interface - all existing code continues to work:

```python
# Old way (still works)
from pattern_query_interface import PatternQueryInterface
interface = PatternQueryInterface()

# New way (recommended)
from pattern_query_interface_semantic import PatternQueryInterfaceSemantic
interface = PatternQueryInterfaceSemantic()  # Includes all old methods + semantic
```

---

## Overview

You have a working knowledge graph with architectural patterns extracted from proven GitHub repositories. Now let's make it **useful** for actual SPEC development.

---

## Table of Contents

1. [Expand the Corpus](#1-expand-the-corpus)
2. [Query Interface Setup](#2-query-interface-setup)
3. [SPEC_Engine Integration](#3-spec_engine-integration)
4. [API Endpoint (Optional)](#4-api-endpoint-optional)
5. [Maintenance & Updates](#5-maintenance--updates)
6. [Production Deployment](#6-production-deployment)

---

## 1. Expand the Corpus

### Currently: 6 patterns (testing)

### Goal: 100-500 patterns (production-ready corpus)

### Strategy: Extract by Domain and Topic

#### Option 1: Manual Selection (Traditional)

Create domain-specific extraction scripts:

```powershell
# File management patterns (10-20 patterns)
python -c "from pattern_extractor import PatternExtractor; e = PatternExtractor(); e.extract_patterns('topic:file-manager stars:>5000', limit=20)"

# Dashboard patterns (20-30 patterns)
python -c "from pattern_extractor import PatternExtractor; e = PatternExtractor(); e.extract_patterns('topic:dashboard stars:>5000', limit=30)"

# CLI tool patterns (10-20 patterns)
python -c "from pattern_extractor import PatternExtractor; e = PatternExtractor(); e.extract_patterns('topic:cli stars:>5000', limit=20)"

# API/Backend patterns (30-50 patterns)
python -c "from pattern_extractor import PatternExtractor; e = PatternExtractor(); e.extract_patterns('topic:api OR topic:backend stars:>5000', limit=50)"

# Real-time/WebSocket patterns (10-20 patterns)
python -c "from pattern_extractor import PatternExtractor; e = PatternExtractor(); e.extract_patterns('topic:websocket OR topic:realtime stars:>5000', limit=20)"
```

#### Option 2: LLM-Assisted Selection (Recommended)

**Web UI (Easiest):**

```powershell
# Start the server
python domain_selector_server.py

# Then open domain_selector_ui.html in your browser
# Or use the quick launcher:
./launch_selector.ps1
```

The web UI provides:
1. Simple form for project description
2. AI-powered topic and domain recommendations
3. **One-click extraction** - runs patterns extraction directly from the browser
4. Real-time progress monitoring with live logs
5. Auto-generated batch script as fallback

**CLI (Alternative):**

```powershell
# Interactive mode
python domain_topic_selector.py

# Or provide project description directly
python domain_topic_selector.py --description "Building a real-time collaborative text editor"

# Batch mode with file input
python domain_topic_selector.py --from-constitution project_constitution.toml
```

Both tools will:
1. Analyse your project requirements
2. Suggest relevant GitHub topics (e.g., `topic:editor`, `topic:websocket`, `topic:collaboration`)
3. Recommend appropriate domains (e.g., `realtime_apps`, `text_editing`, `collaboration`)
4. Generate optimised search queries
5. Estimate pattern counts and extraction time

### Using the Web UI (Recommended)

**Quick Start:**

```powershell
# Option 1: Use launcher script
./launch_selector.bat

# Option 2: Use PowerShell launcher
./launch_selector.ps1

# Option 3: Manual start
python domain_selector_server.py
# Then open domain_selector_ui.html in browser
```

**Web UI Features:**

1. **Simple Form Interface**
   - Enter project description in natural language
   - Optionally add existing technologies
   - Click "Analyse Requirements"

2. **AI-Powered Recommendations**
   - Primary topics (3-5 most relevant)
   - Secondary topics (broader coverage)
   - Domain organisation suggestions
   - Ready-to-use search queries
   - Technology stack recommendations
   - Confidence score and time estimates

3. **One-Click Extraction** (NEW!)
   - Click "Run Extraction Now" button
   - Real-time progress bar
   - Live logs showing extraction status
   - Pattern count updates
   - No need to copy/paste scripts!

4. **Fallback Batch Script**
   - Auto-generated Python script
   - Available if you prefer manual execution
   - Can be saved and customised

**Using the UI:**

1. **Start the server** (runs on http://localhost:8000)
2. **Open the HTML file** in your browser
3. **Describe your project**: "Building a secure note-taking app for counsellors with GDPR compliance"
4. **Add technologies** (optional): "nodejs, postgresql, react"
5. **Click "Analyse Requirements"** - wait 5-10 seconds
6. **Review recommendations** - topics, domains, queries
7. **Click "Run Extraction Now"** - watch patterns being extracted in real-time!

**Example Workflow:**

```
Input: "Building a real-time chat application with WebSocket support"
Technologies: nodejs, socketio

Output:
- Confidence: HIGH
- Est. Time: 2-3 hours
- Topics: realtime, chat, websocket, nodejs
- Domains: realtime_collaboration, websocket_infrastructure, chat_systems
- 4 optimised queries ready to extract

Click "Run Extraction Now":
[===================] 100% - 85 patterns extracted in 45 minutes
```

### Using the CLI (Alternative)

The CLI tool provides three modes if you prefer terminal:

**Interactive Mode:**

```powershell
python domain_topic_selector.py
```

Follow the prompts to describe your project and get instant recommendations.

**Command-Line Mode:**

```powershell
# Analyse a specific project
python domain_topic_selector.py --description "Building a real-time collaborative text editor" --technologies "typescript,websocket"

# Save recommendations to file
python domain_topic_selector.py --description "E-commerce platform with inventory management" --output recommendations.json

# Generate batch script automatically
python domain_topic_selector.py --description "Dashboard for monitoring IoT devices" --generate-script
```

**Constitution Mode (Integrated with SPEC):**

```powershell
# Analyse from existing project constitution
python domain_topic_selector.py --from-constitution ../TGACGTCA/project_constitution.toml --generate-script
```

### Batch Extraction Script

Create `batch_extract_domains.py` (or use the auto-generated one):

```python
# batch_extract_domains.py
from pattern_extractor import PatternExtractor

extractor = PatternExtractor()

domains = [
    ("topic:file-manager stars:>5000", 20, "file_management"),
    ("topic:dashboard stars:>5000", 30, "dashboards"),
    ("topic:cli stars:>5000", 20, "cli_tools"),
    ("topic:api OR topic:backend stars:>5000", 50, "backend_api"),
    ("topic:websocket OR topic:realtime stars:>5000", 20, "realtime"),
    ("topic:database stars:>5000", 30, "databases"),
    ("topic:authentication stars:>5000", 20, "auth"),
    ("topic:monitoring stars:>5000", 20, "monitoring"),
    ("topic:testing stars:>5000", 20, "testing"),
    ("topic:devops stars:>5000", 30, "devops"),
]

total_extracted = 0

for query, limit, domain_name in domains:
    print(f"\n{'='*60}")
    print(f"Extracting {domain_name} patterns...")
    print(f"{'='*60}")
    
    patterns = extractor.extract_patterns(query, limit=limit)
    total_extracted += len(patterns)
    
    print(f"✓ {len(patterns)} patterns extracted for {domain_name}")

print(f"\n{'='*60}")
print(f"Total patterns extracted: {total_extracted}")
print(f"{'='*60}")
```

Run it:

```powershell
python batch_extract_domains.py
```

**Expected time:** 2-4 hours for ~260 patterns (FREE with Gemini)

### Why Use the Web UI?

**Traditional Approach (Manual):**
- Write GitHub search queries by hand
- Guess relevant topics without reasoning
- No validation of query quality
- Run Python scripts in terminal
- No visibility into extraction progress
- Hard to share or reproduce

**Web UI Benefits:**
- ✓ Natural language input (just describe your project)
- ✓ AI-powered topic recommendations with reasoning
- ✓ Domain suggestions tailored to your needs
- ✓ Estimated repo counts and extraction time
- ✓ Tech stack recommendations from similar projects
- ✓ **One-click extraction with live progress**
- ✓ Real-time logs and pattern counts
- ✓ No terminal or scripting required

**Real Example:**

```
Traditional (15+ minutes of work):
1. Research GitHub topics for "secure note-taking with GDPR"
2. Write 5+ search queries manually
3. Create batch_extract.py script
4. Run script in terminal
5. Wait with no progress feedback
6. Check logs after completion

Web UI (30 seconds):
1. Type: "secure note-taking app for counsellors with GDPR compliance"
2. Click "Analyse Requirements" (10 seconds)
3. Click "Run Extraction Now"
4. Watch real-time progress with live logs
✓ Done! 85 patterns extracted
```

### Recommended Workflow: From SPEC to Patterns

**Step 1: Create Project Constitution**

```powershell
# Create your project constitution as usual
cd SPECs/MYPROJECT
# Edit project_constitution.toml
```

**Step 2: Get Domain & Topic Recommendations**

```powershell
python ../../pattern_extraction_pipeline/domain_topic_selector.py \
  --from-constitution project_constitution.toml \
  --generate-script
```

This generates `batch_extract_custom.py` tailored to your project.

**Step 3: Extract Relevant Patterns**

```powershell
cd ../../pattern_extraction_pipeline
python batch_extract_custom.py
```

**Step 4: Validate Your SPEC**

```powershell
python spec_validator.py --constitution ../SPECs/MYPROJECT/project_constitution.toml
```

Now you have a knowledge graph populated with patterns specifically relevant to your project!

---

## 2. Query Interface Setup

**UPDATE:** We now have a production-ready, LLM-optimized query interface!

### Use the Pattern Query Interface

The `PatternQueryInterface` is specifically designed for LLM-assisted SPEC building. See `PATTERN_QUERY_GUIDE.md` for full documentation.

**Quick Start:**

```powershell
# Install dependencies
python -m pip install google-generativeai

# Run the example
python example_spec_builder.py
```

**Key Features:**
- SPEC-to-Pattern matching with semantic ranking
- Feasibility verification for SPECs
- Natural language query support
- Technology/requirement/constraint queries
- LLM-friendly response formats

**Example Usage:**

```python
from pattern_query_interface import PatternQueryInterface

interface = PatternQueryInterface()

# Find patterns for your SPEC
spec = {
    'goal': 'Build a file browser application',
    'deployment_type': 'Web Application',
    'tech_stack': {'frontend': 'react'}
}

result = interface.find_patterns_for_spec(spec, top_k=5)

print(f"Recommended: {len(result['recommended_patterns'])} patterns")
print(f"Reasoning: {result['reasoning']}")

# Verify feasibility
verification = interface.verify_spec_feasibility(spec)
print(f"Feasibility: {verification['feasibility_score']}")

interface.close()
```

See `PATTERN_QUERY_GUIDE.md` for complete API documentation and integration patterns.

---

### Legacy: Create a Basic Python Query Library (Optional)

If you need direct Neo4j access without LLM features, create `pattern_query.py`:

```python
# pattern_query.py
# Python interface for querying the knowledge graph

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from typing import List, Dict, Optional

load_dotenv()

class PatternQuery:
    """Query interface for architectural pattern knowledge graph."""
    
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            auth=(os.getenv("NEO4J_USER", "neo4j"), 
                  os.getenv("NEO4J_PASSWORD", "password"))
        )
    
    def close(self):
        """Close database connection."""
        self.driver.close()
    
    def recommend_patterns(
        self,
        requirement_type: str,
        domain: Optional[str] = None,
        technologies: Optional[List[str]] = None,
        min_stars: int = 1000,
        confidence: str = "high"
    ) -> List[Dict]:
        """
        Get pattern recommendations based on requirements.
        
        Args:
            requirement_type: Type of requirement (e.g., 'data_management')
            domain: Specific domain (e.g., 'file_system')
            technologies: List of preferred technologies (e.g., ['typescript', 'react'])
            min_stars: Minimum GitHub stars
            confidence: Pattern confidence ('high', 'medium', 'low')
        
        Returns:
            List of recommended patterns with metadata
        """
        with self.driver.session() as session:
            query = """
                MATCH (r:Requirement {type: $req_type})-[:SOLVED_BY]->(p:Pattern)
                WHERE p.stars >= $min_stars
                  AND p.confidence = $confidence
            """
            
            if domain:
                query += " AND r.domain = $domain"
            
            query += """
                OPTIONAL MATCH (p)-[:USES]->(t:Technology)
                OPTIONAL MATCH (p)-[:REQUIRES]->(c:Constraint)
            """
            
            if technologies:
                query += """
                WITH p, r, collect(DISTINCT t.name) AS all_techs, 
                     collect(DISTINCT c.rule) AS constraints
                WHERE any(tech IN $technologies WHERE tech IN all_techs)
                """
            else:
                query += """
                WITH p, r, collect(DISTINCT t.name) AS all_techs,
                     collect(DISTINCT c.rule) AS constraints
                """
            
            query += """
                RETURN p.name AS pattern,
                       p.confidence AS confidence,
                       p.stars AS stars,
                       p.source_repo AS source,
                       p.reasoning AS reasoning,
                       all_techs AS technologies,
                       constraints
                ORDER BY p.stars DESC
                LIMIT 10
            """
            
            params = {
                "req_type": requirement_type,
                "min_stars": min_stars,
                "confidence": confidence
            }
            
            if domain:
                params["domain"] = domain
            
            if technologies:
                params["technologies"] = technologies
            
            result = session.run(query, params)
            
            return [dict(record) for record in result]
    
    def get_pattern_details(self, pattern_name: str) -> Dict:
        """Get complete details for a specific pattern."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Pattern {name: $pattern_name})
                OPTIONAL MATCH (p)-[:USES]->(t:Technology)
                OPTIONAL MATCH (p)-[:REQUIRES]->(c:Constraint)
                OPTIONAL MATCH (r:Requirement)-[:SOLVED_BY]->(p)
                RETURN p.name AS pattern,
                       p.confidence AS confidence,
                       p.stars AS stars,
                       p.source_repo AS source,
                       p.reasoning AS reasoning,
                       collect(DISTINCT {name: t.name}) AS technologies,
                       collect(DISTINCT c.rule) AS constraints,
                       r.type AS requirement_type,
                       r.domain AS requirement_domain
            """, pattern_name=pattern_name)
            
            record = result.single()
            return dict(record) if record else None
    
    def find_similar_patterns(
        self,
        pattern_name: str,
        limit: int = 5
    ) -> List[Dict]:
        """Find patterns similar to a given pattern (by shared technologies)."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p1:Pattern {name: $pattern_name})-[:USES]->(t:Technology)<-[:USES]-(p2:Pattern)
                WHERE p1 <> p2
                WITH p2, collect(DISTINCT t.name) AS shared_techs
                RETURN p2.name AS pattern,
                       p2.confidence AS confidence,
                       p2.stars AS stars,
                       shared_techs AS shared_technologies,
                       size(shared_techs) AS similarity_score
                ORDER BY similarity_score DESC, p2.stars DESC
                LIMIT $limit
            """, pattern_name=pattern_name, limit=limit)
            
            return [dict(record) for record in result]
    
    def get_technology_stack(self, pattern_name: str) -> List[Dict]:
        """Get the complete technology stack for a pattern."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Pattern {name: $pattern_name})-[r:USES]->(t:Technology)
                RETURN t.name AS technology,
                       r.role AS role
                ORDER BY 
                    CASE r.role
                        WHEN 'primary' THEN 1
                        WHEN 'framework' THEN 2
                        WHEN 'runtime' THEN 3
                        WHEN 'library' THEN 4
                        WHEN 'cache' THEN 5
                        WHEN 'queue' THEN 6
                        ELSE 7
                    END
            """, pattern_name=pattern_name)
            
            return [dict(record) for record in result]
    
    def validate_spec_requirements(
        self,
        requirement_type: str,
        domain: str,
        technologies: List[str]
    ) -> Dict:
        """
        Validate SPEC requirements against known patterns.
        
        Returns confidence score and recommendations.
        """
        patterns = self.recommend_patterns(
            requirement_type=requirement_type,
            domain=domain,
            technologies=technologies,
            min_stars=5000
        )
        
        if not patterns:
            return {
                "confidence": "low",
                "message": "No established patterns found for this combination",
                "recommendation": "Consider reviewing requirements or exploring alternative approaches"
            }
        
        top_pattern = patterns[0]
        
        # Calculate confidence based on star count and pattern confidence
        if top_pattern['stars'] > 20000 and top_pattern['confidence'] == 'high':
            confidence = "high"
        elif top_pattern['stars'] > 10000:
            confidence = "medium"
        else:
            confidence = "low"
        
        return {
            "confidence": confidence,
            "validated_pattern": top_pattern['pattern'],
            "stars": top_pattern['stars'],
            "reasoning": top_pattern['reasoning'],
            "recommended_technologies": top_pattern['technologies'],
            "constraints": top_pattern['constraints'],
            "source": top_pattern['source']
        }

# Example usage
if __name__ == "__main__":
    query = PatternQuery()
    
    # Example 1: Recommend patterns for file management
    print("=== File Management Patterns ===")
    patterns = query.recommend_patterns(
        requirement_type="data_management",
        domain="file_system",
        technologies=["typescript", "sqlite"]
    )
    
    for p in patterns:
        print(f"\n{p['pattern']} ({p['stars']} stars)")
        print(f"  Technologies: {', '.join(p['technologies'])}")
        print(f"  Source: {p['source']}")
    
    # Example 2: Get pattern details
    print("\n=== Pattern Details ===")
    details = query.get_pattern_details("filesystem_browser")
    if details:
        print(f"Pattern: {details['pattern']}")
        print(f"Reasoning: {details['reasoning']}")
    
    # Example 3: Validate SPEC requirements
    print("\n=== Validate SPEC Requirements ===")
    validation = query.validate_spec_requirements(
        requirement_type="data_management",
        domain="file_system",
        technologies=["typescript", "react", "sqlite"]
    )
    
    print(f"Confidence: {validation['confidence']}")
    print(f"Validated Pattern: {validation['validated_pattern']}")
    print(f"Recommended Technologies: {', '.join(validation['recommended_technologies'])}")
    
    query.close()
```

### Test the Query Interface

```powershell
python pattern_query.py
```

---

## 3. SPEC_Engine Integration

### Option A: Pre-SPEC Validation

Before starting a SPEC, validate the requirements against the knowledge graph.

Create `spec_validator.py`:

```python
# spec_validator.py
# Validate SPEC requirements against knowledge graph before starting

from pattern_query import PatternQuery
import toml
from pathlib import Path

class SpecValidator:
    """Validate SPEC requirements using knowledge graph."""
    
    def __init__(self):
        self.query = PatternQuery()
    
    def validate_from_constitution(self, constitution_path: str) -> dict:
        """
        Validate SPEC requirements from project_constitution.toml
        
        Returns validation report with recommendations.
        """
        const = toml.load(constitution_path)
        
        # Extract requirements from constitution
        req_type = const.get('requirement_type', 'data_management')
        domain = const.get('domain', None)
        technologies = const.get('preferred_technologies', [])
        
        # Query knowledge graph
        validation = self.query.validate_spec_requirements(
            requirement_type=req_type,
            domain=domain,
            technologies=technologies
        )
        
        # Get recommended patterns
        patterns = self.query.recommend_patterns(
            requirement_type=req_type,
            domain=domain,
            technologies=technologies,
            min_stars=5000
        )
        
        return {
            "validation": validation,
            "recommended_patterns": patterns[:3],
            "similar_implementations": [p['source'] for p in patterns[:5]]
        }
    
    def generate_validation_report(self, constitution_path: str) -> str:
        """Generate markdown validation report."""
        result = self.validate_from_constitution(constitution_path)
        
        report = f"""# SPEC Validation Report

## Validation Result

**Confidence:** {result['validation']['confidence']}

**Validated Pattern:** {result['validation'].get('validated_pattern', 'N/A')}

**Reasoning:** {result['validation'].get('reasoning', 'No matching patterns found')}

## Recommended Patterns

"""
        
        for i, pattern in enumerate(result['recommended_patterns'], 1):
            report += f"""
### {i}. {pattern['pattern']}

- **Stars:** {pattern['stars']}
- **Confidence:** {pattern['confidence']}
- **Technologies:** {', '.join(pattern['technologies'])}
- **Source:** {pattern['source']}
- **Reasoning:** {pattern['reasoning']}

"""
        
        report += """
## Similar Real-World Implementations

"""
        for impl in result['similar_implementations']:
            report += f"- {impl}\n"
        
        report += """
## Recommended Next Steps

1. Review the top recommended pattern
2. Examine the source repositories for implementation details
3. Adapt the pattern to your specific requirements
4. Document any deviations from the recommended pattern

"""
        
        return report
    
    def close(self):
        self.query.close()

# Example usage
if __name__ == "__main__":
    validator = SpecValidator()
    
    # Validate from project constitution
    report = validator.generate_validation_report("../project_constitution.toml")
    
    # Save report
    Path("VALIDATION_REPORT.md").write_text(report)
    
    print(report)
    
    validator.close()
```

### Add to SPEC Workflow

Update `__SPEC_Engine/_Constitution/ARTICLE_I.md` to include validation step:

```markdown
## Step 0: Validate Requirements (New)

Before creating a SPEC, validate your requirements against the knowledge graph:

```powershell
python pattern_extraction_pipeline/spec_validator.py
```

Review the generated `VALIDATION_REPORT.md` for:
- Confidence level (high/medium/low)
- Recommended architectural patterns
- Similar real-world implementations
- Technology stack recommendations
```

---

### Option B: In-SPEC Recommendations

During SPEC creation, query the graph for specific guidance.

Create `spec_assistant.py`:

```python
# spec_assistant.py
# Real-time SPEC assistance using knowledge graph

from pattern_query import PatternQuery

class SpecAssistant:
    """Real-time assistant for SPEC development."""
    
    def __init__(self):
        self.query = PatternQuery()
    
    def recommend_tech_stack(
        self,
        requirement_type: str,
        domain: str,
        existing_techs: list = None
    ) -> dict:
        """Recommend technology stack for requirements."""
        patterns = self.query.recommend_patterns(
            requirement_type=requirement_type,
            domain=domain,
            technologies=existing_techs
        )
        
        if not patterns:
            return {"recommendation": "No established patterns found"}
        
        # Aggregate technologies from top patterns
        tech_counts = {}
        for pattern in patterns[:5]:
            for tech in pattern['technologies']:
                tech_counts[tech] = tech_counts.get(tech, 0) + 1
        
        # Sort by frequency
        recommended = sorted(tech_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "primary_stack": [t[0] for t in recommended[:3]],
            "additional_options": [t[0] for t in recommended[3:6]],
            "based_on_patterns": [p['pattern'] for p in patterns[:3]],
            "confidence": patterns[0]['confidence']
        }
    
    def suggest_constraints(self, pattern_name: str) -> list:
        """Suggest architectural constraints based on pattern."""
        details = self.query.get_pattern_details(pattern_name)
        if details:
            return details.get('constraints', [])
        return []
    
    def find_examples(self, requirement_type: str, domain: str) -> list:
        """Find example implementations."""
        patterns = self.query.recommend_patterns(
            requirement_type=requirement_type,
            domain=domain,
            min_stars=10000
        )
        
        return [
            {
                "pattern": p['pattern'],
                "source": p['source'],
                "stars": p['stars']
            }
            for p in patterns
        ]
    
    def close(self):
        self.query.close()

# CLI interface
if __name__ == "__main__":
    import sys
    
    assistant = SpecAssistant()
    
    if len(sys.argv) < 3:
        print("Usage: python spec_assistant.py <command> <args>")
        print("\nCommands:")
        print("  tech-stack <type> <domain>  - Recommend technology stack")
        print("  constraints <pattern>        - Get architectural constraints")
        print("  examples <type> <domain>     - Find example implementations")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "tech-stack":
        req_type = sys.argv[2]
        domain = sys.argv[3]
        result = assistant.recommend_tech_stack(req_type, domain)
        print(f"Primary Stack: {', '.join(result['primary_stack'])}")
        print(f"Based on: {', '.join(result['based_on_patterns'])}")
    
    elif command == "constraints":
        pattern = sys.argv[2]
        constraints = assistant.suggest_constraints(pattern)
        print(f"Constraints for {pattern}:")
        for c in constraints:
            print(f"  - {c}")
    
    elif command == "examples":
        req_type = sys.argv[2]
        domain = sys.argv[3]
        examples = assistant.find_examples(req_type, domain)
        print(f"Example implementations:")
        for ex in examples:
            print(f"  - {ex['pattern']} ({ex['stars']} stars): {ex['source']}")
    
    assistant.close()
```

### Use During SPEC Creation

```powershell
# Recommend tech stack
python spec_assistant.py tech-stack data_management file_system

# Get constraints for a pattern
python spec_assistant.py constraints filesystem_browser

# Find example implementations
python spec_assistant.py examples data_management file_system
```

---

## 4. API Endpoint (Optional)

For dashboard/web interface integration, create a REST API.

Create `api_server.py`:

```python
# api_server.py
# REST API for knowledge graph queries

from flask import Flask, jsonify, request
from pattern_query import PatternQuery
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

query = PatternQuery()

@app.route('/api/patterns/recommend', methods=['POST'])
def recommend_patterns():
    """Recommend patterns based on requirements."""
    data = request.json
    
    patterns = query.recommend_patterns(
        requirement_type=data.get('requirement_type'),
        domain=data.get('domain'),
        technologies=data.get('technologies', []),
        min_stars=data.get('min_stars', 1000),
        confidence=data.get('confidence', 'high')
    )
    
    return jsonify(patterns)

@app.route('/api/patterns/<pattern_name>', methods=['GET'])
def get_pattern(pattern_name):
    """Get pattern details."""
    details = query.get_pattern_details(pattern_name)
    return jsonify(details) if details else ('Not found', 404)

@app.route('/api/patterns/<pattern_name>/similar', methods=['GET'])
def get_similar_patterns(pattern_name):
    """Get similar patterns."""
    limit = request.args.get('limit', 5, type=int)
    similar = query.find_similar_patterns(pattern_name, limit)
    return jsonify(similar)

@app.route('/api/validate', methods=['POST'])
def validate_requirements():
    """Validate SPEC requirements."""
    data = request.json
    
    validation = query.validate_spec_requirements(
        requirement_type=data.get('requirement_type'),
        domain=data.get('domain'),
        technologies=data.get('technologies', [])
    )
    
    return jsonify(validation)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
```

### Install Dependencies

```powershell
pip install flask flask-cors
```

### Run API Server

```powershell
python api_server.py
```

### Test API

```powershell
# Recommend patterns
curl -X POST http://localhost:5001/api/patterns/recommend `
  -H "Content-Type: application/json" `
  -d '{\"requirement_type\": \"data_management\", \"domain\": \"file_system\"}'

# Validate requirements
curl -X POST http://localhost:5001/api/validate `
  -H "Content-Type: application/json" `
  -d '{\"requirement_type\": \"data_management\", \"domain\": \"file_system\", \"technologies\": [\"typescript\"]}'
```

---

## 5. Maintenance & Updates

### Weekly: Add New Patterns

```powershell
# Add 10-20 new patterns weekly
python -c "from pattern_extractor import PatternExtractor; e = PatternExtractor(); e.extract_patterns('stars:>5000 pushed:>2025-01-01', limit=20)"
```

### Monthly: Clean Up Data Quality

```powershell
python setup_data_quality.py
python verify_data_quality.py
```

### Quarterly: Refresh Stale Patterns

```cypher
// Find patterns older than 3 months
MATCH (p:Pattern)
WHERE p.extracted_date < date() - duration('P3M')
RETURN p.name, p.source_repo
```

Re-extract these to get updated star counts and activity.

---

## 6. Production Deployment

### Docker Deployment

Create `docker-compose.production.yml`:

```yaml
version: '3.8'

services:
  neo4j:
    image: neo4j:latest
    container_name: spec-patterns-graph
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/your-production-password
      - NEO4J_dbms_memory_heap_max__size=2G
    volumes:
      - neo4j-data:/data
      - neo4j-logs:/logs
    restart: unless-stopped
  
  api:
    build: .
    container_name: spec-patterns-api
    ports:
      - "5001:5001"
    environment:
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=your-production-password
    depends_on:
      - neo4j
    restart: unless-stopped

volumes:
  neo4j-data:
  neo4j-logs:
```

### Backup Strategy

```powershell
# Backup Neo4j database
docker exec spec-patterns-graph neo4j-admin dump --to=/backups/neo4j-$(date +%Y%m%d).dump

# Restore from backup
docker exec spec-patterns-graph neo4j-admin load --from=/backups/neo4j-20260102.dump
```

---

## Quick Start Checklist

- [ ] Expand corpus to 100+ patterns (`batch_extract_domains.py`)
- [ ] Test query interface (`python pattern_query.py`)
- [ ] Integrate validation into SPEC workflow (`spec_validator.py`)
- [ ] (Optional) Set up API server for dashboard integration
- [ ] Schedule weekly pattern additions
- [ ] Document your specific use cases

---

## Real-World Usage Examples

### Example 1: Starting a New SPEC

```powershell
# 1. Validate requirements
python spec_validator.py --constitution project_constitution.toml

# 2. Review VALIDATION_REPORT.md

# 3. Get tech stack recommendations
python spec_assistant.py tech-stack data_management file_system

# 4. Proceed with SPEC creation using recommended pattern
```

### Example 2: Mid-SPEC Architecture Decision

```powershell
# Should we use SQLite or PostgreSQL for caching?
python pattern_query.py --query "
  MATCH (p:Pattern)-[:USES]->(t:Technology)
  WHERE t.name IN ['sqlite', 'postgresql']
  RETURN t.name, count(p) AS pattern_count
  ORDER BY pattern_count DESC
"
```

### Example 3: Finding Reference Implementations

```python
from pattern_query import PatternQuery

query = PatternQuery()
examples = query.find_similar_patterns("your_current_spec_pattern")

print("Reference implementations:")
for ex in examples:
    print(f"- {ex['pattern']}: {ex['source']}")
```

---

## Next Steps

1. **Expand corpus** - Extract 100+ patterns across your common domains
2. **Integrate validation** - Add pre-SPEC validation step
3. **Use during SPECs** - Query graph when making architecture decisions
4. **Monitor effectiveness** - Track how often recommendations are followed
5. **Refine queries** - Customize `pattern_query.py` for your specific needs

---

## Advanced Usage: Domain & Topic Selector

### Custom LLM Models

Edit `domain_topic_selector.py` to use different models:

```python
# Line 28: Change the model
self.model = genai.GenerativeModel('gemini-2.0-flash-exp')  # Default
# self.model = genai.GenerativeModel('gemini-1.5-pro')      # More thorough
# self.model = genai.GenerativeModel('gemini-1.5-flash')    # Faster
```

### Refining Recommendations

If the initial recommendations aren't quite right:

```powershell
# Be more specific in your description
python domain_topic_selector.py --description "Building a Python-based CLI tool for managing Docker containers with interactive TUI, similar to lazydocker"

# Add technology constraints
python domain_topic_selector.py \
  --description "Real-time chat application" \
  --technologies "nodejs,socketio,redis" \
  --generate-script
```

### Iterative Refinement

```powershell
# 1. Get initial recommendations
python domain_topic_selector.py --description "Project X" --output recommendations_v1.json

# 2. Review, then refine
python domain_topic_selector.py \
  --description "Project X - specifically focusing on real-time features and scalability" \
  --output recommendations_v2.json

# 3. Compare recommendations
diff recommendations_v1.json recommendations_v2.json
```

### Integration with Existing Knowledge Graph

```powershell
# 1. Check current pattern count
python -c "from pattern_query import PatternQuery; q = PatternQuery(); print('Current patterns:', len(q.get_all_patterns()))"

# 2. Get recommendations for gaps
python domain_topic_selector.py --description "Areas we're missing coverage in: authentication, caching, monitoring"

# 3. Extract targeted patterns
python batch_extract_custom.py
```

### Troubleshooting

**Issue: LLM returns no recommendations**
```powershell
# Check API key
echo $env:GEMINI_API_KEY

# Test API connection
python -c "import google.generativeai as genai; genai.configure(api_key='YOUR_KEY'); print('Connected')"
```

**Issue: Topics not returning enough repos**
- Reduce minimum star count in generated queries
- Broaden topic selection (use secondary topics)
- Check GitHub topic exists: `https://github.com/topics/YOUR-TOPIC`

**Issue: Extraction takes too long**
- Reduce `limit` values in batch script
- Focus on primary topics only
- Increase `stars:>X` threshold

### Best Practices

1. **Start Specific, Then Broaden**
   - First run: Use very specific description
   - Second run: Broaden if not enough patterns found

2. **Validate Topics on GitHub**
   - Check suggested topics exist on GitHub
   - Verify repo counts match estimates

3. **Iterate on Domain Names**
   - Use clear, descriptive domain names
   - Group related patterns together
   - Avoid overly broad domains

4. **Monitor Extraction Quality**
   - Check pattern confidence scores
   - Review reasoning for extracted patterns
   - Remove low-quality patterns

5. **Update Regularly**
   - Re-run selector every 3-6 months
   - Update to capture new GitHub trends
   - Refine based on actual SPEC usage

### Example: Complete Workflow

```powershell
# Start new SPEC project
cd SPECs/NEWPROJECT

# Describe the project
python ../../pattern_extraction_pipeline/domain_topic_selector.py \
  --description "Building a Python web scraper with async requests, rate limiting, and data export to CSV/JSON. Needs to handle authentication and proxy rotation." \
  --technologies "python,asyncio" \
  --generate-script \
  --output extraction_plan.json

# Review the plan
cat extraction_plan.json

# Execute extraction
cd ../../pattern_extraction_pipeline
python batch_extract_custom.py

# Validate against extracted patterns
python spec_validator.py --constitution ../SPECs/NEWPROJECT/project_constitution.toml

# Start building with confidence
```

---

## Quick Reference

### Launch Web UI

```powershell
# Easiest - use launcher
./launch_selector.bat

# Or PowerShell
./launch_selector.ps1

# Or manual
python domain_selector_server.py
# Then open domain_selector_ui.html
```

### Stop Server

```powershell
# Find and kill Python processes
Stop-Process -Name python -Force

# Or use Ctrl+C in the terminal where server is running
```

### File Locations

- **Web UI**: `pattern_extraction_pipeline/domain_selector_ui.html`
- **Server**: `pattern_extraction_pipeline/domain_selector_server.py`
- **CLI Tool**: `pattern_extraction_pipeline/domain_topic_selector.py`
- **Launchers**: 
  - `pattern_extraction_pipeline/launch_selector.bat` (Windows)
  - `pattern_extraction_pipeline/launch_selector.ps1` (PowerShell)

### Common Workflows

**Start a new project:**
```powershell
./launch_selector.bat
# 1. Describe project
# 2. Click "Analyse Requirements"
# 3. Click "Run Extraction Now"
# 4. Wait for patterns to extract
```

**From existing SPEC constitution:**
```powershell
python domain_topic_selector.py --from-constitution ../SPECs/MYPROJECT/project_constitution.toml --generate-script
python batch_extract_custom.py
```

**Check extracted patterns:**
```powershell
# Neo4j Browser
http://localhost:7474

# Query: How many patterns?
MATCH (p:Pattern) RETURN count(p)
```

---

**Version:** 2.0  
**Last Updated:** 2026-01-05
**New in v2.0:** 
- LLM-assisted domain and topic selection
- Web UI with one-click extraction
- Real-time progress monitoring
- Quick launcher scripts
