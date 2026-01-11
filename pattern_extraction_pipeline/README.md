# Pattern Extraction Pipeline

LLM-powered tool for extracting architectural patterns from GitHub repositories and storing them in a Neo4j knowledge graph.

## Quick Start

### Launch the Web UI (Easiest)

**Windows:**
```powershell
./launch_selector.bat
```

**PowerShell:**
```powershell
./launch_selector.ps1
```

This will:
1. Start the Flask server on http://localhost:8000
2. Open the UI in your browser automatically

### Use the UI

1. **Describe your project** in natural language
2. **Add technologies** (optional)
3. **Click "Analyse Requirements"** - AI suggests topics and domains
4. **Click "Run Extraction Now"** - extracts patterns with live progress!

## What You Get

- AI-powered GitHub topic recommendations
- Domain organisation suggestions
- Ready-to-use search queries
- Technology stack recommendations
- One-click pattern extraction with real-time progress
- **Multi-dimensional quality scoring** (popularity, maintenance, maturity, community, freshness)
- **Technology criticality weights** (know which techs are critical vs optional)
- **Constraint enforcement levels** (must/should/nice-to-have)
- Auto-generated batch scripts for manual use

## Using the Pattern Extractor Programmatically

### Recommended: Context Manager (Automatic Resource Cleanup)

```python
from pattern_extraction_pipeline import PatternExtractor

# Use context manager for automatic resource cleanup
with PatternExtractor() as extractor:
    pattern = extractor.analyze_single_repo('anthropics/anthropic-sdk-python')
    print(f"Extracted: {pattern['pattern_name']}")
# Resources (Neo4j driver, executors) automatically cleaned up here
```

**Note:** PatternExtractor will issue a deprecation warning if not used as a context manager. This encourages proper resource cleanup and prevents memory leaks.

## Using Patterns for SPEC Building

### 🔥 NEW: Semantic Search (Recommended)

The knowledge graph now supports **natural language pattern discovery**!

```python
from pattern_query_interface_semantic import PatternQueryInterfaceSemantic

with PatternQueryInterfaceSemantic() as interface:
    # Hybrid search: semantic + structural (RECOMMENDED)
    result = interface.find_patterns_hybrid(
        goal="Build a file browser for volunteers",  # Natural language!
        constraints={
            'technologies': ['typescript', 'react'],
            'min_stars': 5000
        },
        top_k=5
    )
    
    # Present options to user
    print(result['user_review_text'])
    
    # Verify feasibility with semantic search
    verification = interface.verify_spec_feasibility(
        {'goal': 'Build a file browser'},
        use_semantic=True
    )
    print(f"Feasibility: {verification['feasibility_score']}")
```

### Traditional Structural Queries (Still Supported)

```python
from pattern_query_interface import PatternQueryInterface

with PatternQueryInterface() as interface:
    # Find patterns by exact criteria
    spec = {'goal': 'Build a file browser', 'deployment_type': 'Web Application'}
    patterns = interface.find_patterns_for_spec(spec)
    
    print(f"Found {len(patterns['recommended_patterns'])} relevant patterns")
```

**Documentation:**
- `VECTOR_ARCHITECTURE.md` - Complete technical specification
- `PATTERN_QUERY_GUIDE.md` - Full API documentation
- `IMPLEMENTATION_STATUS_VECTOR_KG.md` - What's been built

## Files

### Pattern Extraction
- `launch_selector.bat` - Quick launcher (Windows)
- `launch_selector.ps1` - Quick launcher (PowerShell)
- `domain_selector_ui.html` - Web interface for extraction
- `domain_selector_server.py` - Flask API server
- `domain_topic_selector.py` - CLI tool (alternative)
- `pattern_extractor.py` - Core extraction engine

### Pattern Querying
- `pattern_query_interface.py` - **LLM-friendly query interface for SPEC building**
- `example_spec_builder.py` - Example: LLM building a SPEC with pattern guidance
- `PATTERN_QUERY_GUIDE.md` - Complete query API documentation

### Documentation
- `_KG_SPEC_INTEGRATION_GUIDE.md` - Complete integration guide

## Requirements

```powershell
python -m pip install google-generativeai flask flask-cors toml python-dotenv neo4j
```

Set `GEMINI_API_KEY` in `.env` file.

## Stop Server

```powershell
Stop-Process -Name python -Force
```

Or press Ctrl+C in the terminal where the server is running.

---

**See `_KG_SPEC_INTEGRATION_GUIDE.md` for complete documentation.**
