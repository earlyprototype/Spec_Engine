# Awesome List Parser - Usage Guide

**Purpose:** Extract high-quality GitHub repositories from awesome lists to feed into the pattern extraction pipeline.

---

## Why Use This?

**Problem:** Awesome lists are just markdown files with links - analyzing them directly produces useless "Curated List" patterns.

**Solution:** Parse awesome lists to extract the **linked repositories**, then analyze those.

**Benefit:** Leverage community curation to discover high-quality repositories without manual searching.

---

## Installation

```bash
cd pattern_extraction_pipeline

# Install PyGithub if not already installed
pip install PyGithub
```

---

## Quick Start

### Example 1: Extract NLP Libraries from awesome-nlp

```bash
python awesome_list_parser.py \
    --list keon/awesome-nlp \
    --min-stars 1000 \
    --output nlp_repos.json
```

**Output:** `nlp_repos.json` with full metadata for 50+ NLP libraries (spaCy, Transformers, AllenNLP, etc.)

---

### Example 2: Get URLs only (for manual review)

```bash
python awesome_list_parser.py \
    --list keon/awesome-nlp \
    --min-stars 500 \
    --format urls \
    --output nlp_urls.txt
```

**Output:** `nlp_urls.txt` with one URL per line:
```
https://github.com/explosion/spaCy
https://github.com/huggingface/transformers
https://github.com/allenai/allennlp
...
```

---

### Example 3: Generate domain queries for pattern extractor

```bash
python awesome_list_parser.py \
    --list keon/awesome-nlp \
    --min-stars 1000 \
    --format domains \
    --output domains_to_extract.txt
```

**Output:** `domains_to_extract.txt` with repo queries:
```
repo:explosion/spaCy
repo:huggingface/transformers
repo:allenai/allennlp
...
```

You can then feed these to your pattern extractor!

---

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--list` | Awesome list repo (e.g., `keon/awesome-nlp`) | **Required** |
| `--min-stars` | Minimum star count for included repos | `100` |
| `--max-stars` | Maximum star count (for filtering popular repos) | `None` |
| `--output` | Output file path | `awesome_repos.json` |
| `--format` | Output format: `json`, `urls`, or `domains` | `json` |

---

## Output Formats

### Format: `json` (Default)

Full repository metadata:

```json
[
  {
    "full_name": "explosion/spaCy",
    "name": "spaCy",
    "owner": "explosion",
    "html_url": "https://github.com/explosion/spaCy",
    "description": "Industrial-strength NLP",
    "stars": 30245,
    "forks": 4321,
    "language": "Python",
    "topics": ["nlp", "natural-language-processing", "machine-learning"],
    "created_at": "2015-03-02T12:34:56Z",
    "updated_at": "2026-01-06T10:20:30Z",
    "archived": false,
    "fork": false
  },
  ...
]
```

**Use case:** Detailed analysis, filtering, reporting

---

### Format: `urls`

Simple list of URLs:

```
https://github.com/explosion/spaCy
https://github.com/huggingface/transformers
...
```

**Use case:** Manual review, sharing with team

---

### Format: `domains`

Repository queries for pattern extractor:

```
repo:explosion/spaCy
repo:huggingface/transformers
...
```

**Use case:** Direct input to pattern extraction pipeline

---

## Popular Awesome Lists to Try

### AI/ML/NLP:
- `keon/awesome-nlp` - Natural Language Processing
- `josephmisiti/awesome-machine-learning` - Machine Learning
- `academic/awesome-datascience` - Data Science
- `ChristosChristofidis/awesome-deep-learning` - Deep Learning
- `dair-ai/ML-YouTube-Courses` - ML courses and tutorials

### Frameworks:
- `vinta/awesome-python` - Python packages
- `sindresorhus/awesome-nodejs` - Node.js packages
- `enaqx/awesome-react` - React ecosystem
- `vuejs/awesome-vue` - Vue.js ecosystem

### Databases:
- `sindresorhus/awesome-nodejs#databases` - Database tools
- `numetriclabz/awesome-db` - Database systems

### Knowledge Graphs (Highly Relevant!):
- Search GitHub for `awesome knowledge graph` or `awesome semantic web`

---

## Integration with Pattern Extractor

### Step 1: Extract repos from awesome list

```bash
python awesome_list_parser.py \
    --list keon/awesome-nlp \
    --min-stars 1000 \
    --format json \
    --output awesome_nlp_repos.json
```

### Step 2: Review and filter the JSON

Open `awesome_nlp_repos.json`, review the repos, filter by language/topics if needed.

### Step 3A: Manual addition to domain_selector_server.py

Add repos to your domain queries:

```python
domains = [
    # ... existing domains ...
    {
        'name': 'awesome_nlp_spacy',
        'query': 'repo:explosion/spaCy',
        'max_repos': 1
    },
    {
        'name': 'awesome_nlp_transformers',
        'query': 'repo:huggingface/transformers',
        'max_repos': 1
    },
    # ... more repos ...
]
```

### Step 3B: Automated batch extraction

Or create a script to batch-extract all repos:

```python
import json

# Load awesome list repos
with open('awesome_nlp_repos.json') as f:
    repos = json.load(f)

# Create domain queries
domains = []
for repo in repos[:50]:  # Top 50 repos
    domains.append({
        'name': f"awesome_{repo['name'].lower()}",
        'query': f"repo:{repo['full_name']}",
        'max_repos': 1
    })

# Add to your extraction pipeline
```

---

## Filtering Strategy

### Conservative (High Quality Only):
```bash
--min-stars 5000
```
Result: ~10-20 repos per awesome list (very high quality)

### Balanced (Recommended):
```bash
--min-stars 1000
```
Result: ~50-100 repos per awesome list (good quality)

### Comprehensive (More Coverage):
```bash
--min-stars 100
```
Result: ~200-500 repos per awesome list (includes smaller projects)

---

## Example Workflow

### Discover NLP Libraries via Awesome Lists

**Goal:** Find high-quality NLP libraries beyond basic GitHub search

**Steps:**

1. **Parse awesome-nlp:**
   ```bash
   python awesome_list_parser.py \
       --list keon/awesome-nlp \
       --min-stars 1000 \
       --output nlp_libs.json
   ```

2. **Parse awesome-python (NLP section):**
   ```bash
   python awesome_list_parser.py \
       --list vinta/awesome-python \
       --min-stars 5000 \
       --output python_libs.json
   ```

3. **Combine and deduplicate:**
   ```python
   import json
   
   nlp = json.load(open('nlp_libs.json'))
   python = json.load(open('python_libs.json'))
   
   # Combine and deduplicate by full_name
   all_repos = {r['full_name']: r for r in nlp + python}
   
   # Filter for NLP-related
   nlp_repos = [
       r for r in all_repos.values()
       if any(topic in r['topics'] for topic in ['nlp', 'natural-language-processing'])
   ]
   
   json.dump(nlp_repos, open('final_nlp_repos.json', 'w'), indent=2)
   ```

4. **Extract patterns:**
   Feed `final_nlp_repos.json` to your pattern extractor!

---

## Rate Limiting

**GitHub API limits:** 5000 requests/hour with authentication

**This script uses:** ~1 request per repository + 1 for README

**Example:** Parsing awesome-nlp with 200 repos = ~201 requests

**Impact:** Well within limits for normal use

**Tip:** If parsing multiple large awesome lists, add a delay:
```python
import time
time.sleep(1)  # Between repos
```

---

## Troubleshooting

### Error: "GITHUB_TOKEN not found"

**Solution:** Make sure `.env` file contains:
```
GITHUB_TOKEN=ghp_yourtoken...
```

### Error: "Failed to fetch README"

**Cause:** Repository may be private, deleted, or renamed

**Solution:** Script will skip and continue with other repos

### Too many repos returned

**Solution:** Increase `--min-stars` threshold

### Not enough repos returned

**Solution:** Decrease `--min-stars` or try a different awesome list

---

## Advanced Usage

### Filter by Language

Modify the script to filter by programming language:

```python
filtered_repos = parser_instance.filter_repos(
    repos_with_metadata,
    min_stars=args.min_stars,
    languages=['Python', 'TypeScript']  # Add this
)
```

### Filter by Topics

```python
filtered_repos = parser_instance.filter_repos(
    repos_with_metadata,
    min_stars=args.min_stars,
    required_topics=['machine-learning', 'nlp']  # Add this
)
```

### Exclude Archived/Forks

Already enabled by default! Script excludes:
- Archived repositories (no longer maintained)
- Forked repositories (not original work)

---

## Best Practices

1. **Start with high-quality awesome lists** (check star count of the list itself)
2. **Use conservative star thresholds** (1000+ for production analysis)
3. **Review output before feeding to pattern extractor** (spot-check quality)
4. **Deduplicate across multiple lists** (same repo may appear in multiple awesome lists)
5. **Prioritize active repos** (check `updated_at` timestamp)

---

## Example Output

### Running the script:

```bash
$ python awesome_list_parser.py --list keon/awesome-nlp --min-stars 1000

[START] Parsing awesome list: keon/awesome-nlp
[CONFIG] Min stars: 1000
[OK] Fetched README from keon/awesome-nlp
[FOUND] 247 unique GitHub repositories

[FETCHING] Repository metadata...
  [1/247] Fetching explosion/spaCy... (30245 stars)
  [2/247] Fetching huggingface/transformers... (142532 stars)
  [3/247] Fetching facebookresearch/fairseq... (31234 stars)
  ...
  [247/247] Fetching someuser/small-repo... (45 stars)

[FILTERED] 52 repositories meet criteria

[SAVED] Output written to awesome_repos.json

[SUMMARY]
  Total repos extracted: 52
  Star range: 1023 - 142532
  Top 5 repos:
    - huggingface/transformers: 142532 stars (Python)
    - explosion/spaCy: 30245 stars (Python)
    - facebookresearch/fairseq: 31234 stars (Python)
    - stanfordnlp/CoreNLP: 9532 stars (Java)
    - pytorch/fairseq: 30123 stars (Python)
```

---

## Next Steps

After parsing awesome lists:

1. **Review the JSON output** - Check quality and relevance
2. **Feed to pattern extractor** - Add repos to your domain queries
3. **Analyze patterns** - Extract architectural patterns from discovered repos
4. **Compare results** - See if awesome-list repos produce different patterns than GitHub search

**Expected benefit:** Higher-quality patterns from curated, well-maintained repositories.

---

## Bottom Line

Awesome lists are **gold mines** for discovering high-quality repositories. This parser lets you leverage that curation without polluting your pattern database with "list" patterns.

**Use it to bootstrap your pattern extraction with community-validated, production-quality code.**
