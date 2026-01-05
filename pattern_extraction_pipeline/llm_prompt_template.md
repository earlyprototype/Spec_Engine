# LLM Prompt Template

This file contains the prompt template used for extracting architectural patterns from GitHub repositories. You can customize this prompt to improve extraction quality or focus on specific aspects.

## Current Prompt Template

```
Analyze this GitHub repository and extract architectural pattern.

Repository: {repo_name}
Stars: {stars}
URL: {repo_url}

README:
{readme}

Structure:
{structure}

Dependencies:
{dependencies}

Extract in JSON format:
{
    "pattern_name": "filesystem_browser",
    "confidence": "high",
    "requirements": {
        "type": "data_management",
        "domain": "file_system",
        "context": ["existing_files", "web_ui"]
    },
    "constraints": [
        "filesystem_is_source_of_truth",
        "database_for_metadata_only"
    ],
    "technologies": [
        {"name": "react", "role": "primary"},
        {"name": "sqlite", "role": "cache"}
    ],
    "reasoning": "Brief explanation..."
}

Be specific. If unclear, set confidence to "low".
```

## Field Descriptions

### pattern_name
- Short, descriptive name for the architectural pattern
- Examples: `filesystem_browser`, `crud_application`, `api_gateway`
- Use snake_case

### confidence
- `high`: Clear, well-documented pattern
- `medium`: Pattern identifiable but with some ambiguity
- `low`: Pattern unclear or insufficient information

### requirements.type
Common types:
- `data_management`: Managing, storing, retrieving data
- `integration`: Connecting systems/services
- `visualization`: Displaying data/dashboards
- `processing`: Data transformation/computation
- `authentication`: User identity/access
- `communication`: Messaging, real-time updates

### requirements.domain
Specific domain within the type:
- For data_management: `file_system`, `database`, `cache`, `search`
- For integration: `api`, `webhook`, `event_bus`, `etl`
- For visualization: `dashboard`, `chart`, `report`, `monitor`

### requirements.context
Array of contextual requirements:
- `existing_files`: Works with pre-existing data
- `new_data`: Creates new data
- `web_ui`: Has web interface
- `cli`: Command-line interface
- `real_time`: Real-time updates
- `batch`: Batch processing

### constraints
Rules/principles the pattern follows:
- `filesystem_is_source_of_truth`
- `database_is_primary_storage`
- `stateless_design`
- `horizontal_scalability`
- `eventual_consistency`
- `idempotent_operations`

### technologies
Array of key technologies:
- `name`: Technology name (lowercase)
- `role`: `primary`, `cache`, `queue`, `runtime`, `framework`, `library`

### reasoning
Brief explanation (2-3 sentences) of why this pattern was identified:
- What problem does it solve?
- What are the key architectural decisions?
- What makes this pattern suitable for this use case?

## Customization Tips

### Focus on Specific Patterns

If you want to extract only specific types of patterns, modify the prompt:

```
Analyze this GitHub repository and determine if it implements a {specific_pattern} pattern.

Focus on:
- {aspect_1}
- {aspect_2}
- {aspect_3}

If it matches, extract details. If not, return null.
```

### Increase Detail

For more detailed extraction:

```
Extract in JSON format with additional fields:
{
    ...existing fields...
    "scalability": "horizontal" | "vertical" | "both",
    "data_flow": "request_response" | "event_driven" | "batch",
    "deployment": "monolith" | "microservices" | "serverless",
    "testing_approach": "unit" | "integration" | "e2e" | "all"
}
```

### Domain-Specific Focus

For specific domains (e.g., web applications):

```
Focus on web application architecture:
- Frontend framework and architecture
- Backend API design
- State management approach
- Authentication/authorization pattern
- Database design pattern
```

### Quality Filtering

To improve quality:

```
Before extracting, verify:
1. Repository has clear documentation (README)
2. Active maintenance (commits in last 6 months)
3. Production-ready (stars > 5000)
4. Clear architectural decisions

If any criteria fail, set confidence to "low" and note why.
```

## Usage in Code

To use a custom prompt in `pattern_extractor.py`:

```python
def _extract_with_llm(self, **kwargs):
    """Use LLM to extract pattern from repo."""
    
    # Load custom prompt template
    with open('llm_prompt_template.md', 'r') as f:
        # Parse and extract the template section
        # (implement your own parser)
        prompt_template = parse_template(f.read())
    
    # Format with actual data
    prompt = prompt_template.format(**kwargs)
    
    # Call LLM
    response = self.llm.chat.completions.create(...)
```

## Testing Prompts

To test prompt modifications:

```python
# test_prompt.py
from pattern_extractor import PatternExtractor

extractor = PatternExtractor()

# Test on known repository
pattern = extractor.analyze_single_repo("microsoft/vscode")

# Verify output quality
print("Pattern:", pattern['pattern_name'])
print("Confidence:", pattern['confidence'])
print("Reasoning:", pattern['reasoning'])

# Expected: filesystem_browser, high confidence
```

## Best Practices

1. **Be Specific:** Clear field definitions reduce hallucination
2. **Use Examples:** Show desired output format
3. **Set Confidence Levels:** Allow LLM to express uncertainty
4. **Request Reasoning:** Forces LLM to explain its analysis
5. **Structured Output:** JSON ensures consistent parsing
6. **Validate Results:** Spot-check 10% of extractions

## Common Issues

### Pattern Name Too Generic

**Problem:** Pattern names like "web_app" are too broad

**Fix:** Add constraint to prompt:
```
Pattern name must be specific (e.g., "crud_admin_panel" not "web_app")
```

### Hallucinated Technologies

**Problem:** LLM invents technologies not in dependencies

**Fix:** Add instruction:
```
Only extract technologies explicitly mentioned in dependencies or README.
If unclear, omit rather than guess.
```

### Inconsistent Confidence

**Problem:** All patterns marked "high" confidence

**Fix:** Add criteria:
```
Confidence criteria:
- high: Clear architecture, good documentation, >10k stars
- medium: Architecture identifiable, some documentation, >5k stars
- low: Architecture unclear, poor docs, or <5k stars
```

## Version History

- **v1.0** (2026-01-02): Initial prompt template
- Future versions will be tracked here
