# Quality Scoring Metrics - What We Actually Measure

## 7-Factor Composite Score (0-100)

### 1. Star Velocity (20 points max)
**What it measures:** Stars gained per year, not just total stars
**Why it matters:** A repo with 1000 stars in 6 months is more active than one with 1000 stars in 10 years
**GitHub data needed:**
- `stargazers_count` (stars)
- `created_at` (repo creation date)
**Formula:** `stars_per_year / 1000 * 20` (capped at 20)

### 2. Freshness (20 points max)
**What it measures:** How recently the repo was updated
**Why it matters:** Abandoned repos shouldn't be recommended
**GitHub data needed:**
- `updated_at` (last update timestamp)
**Scoring:**
- Updated in last 30 days: 20 points
- Last 90 days: 15 points
- Last 180 days: 10 points
- Last 365 days: 5 points
- Older: 0 points

### 3. Issue Health (15 points max)
**What it measures:** Ratio of closed to total issues
**Why it matters:** Shows maintainer responsiveness
**GitHub data needed:**
- `open_issues_count`
- `closed_issues` (estimated from search if not available)
**Formula:** `closed_issues / total_issues * 15`

### 4. Contributor Diversity (15 points max)
**What it measures:** Number of contributors
**Why it matters:** Single-maintainer repos are riskier
**GitHub data needed:**
- Contributors count (from `/contributors` API endpoint)
**Scoring:**
- 50+ contributors: 15 points
- 20-49: 12 points
- 10-19: 9 points
- 5-9: 6 points
- 2-4: 3 points
- 1: 0.75 points

### 5. Production Readiness (20 points max)
**What it measures:** Presence of production infrastructure files
**Why it matters:** Real production usage > hobby projects
**GitHub data needed:**
- File list from repo (tree API)
**Signals detected:**
- CI/CD: `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, etc.
- Deployment: `Dockerfile`, `kubernetes/`, `terraform/`, etc.
- Testing: `pytest.ini`, `tests/`, `.coveragerc`, etc.
- Monitoring: `prometheus.yml`, `grafana/`, etc.
- Security: `.snyk`, `dependabot.yml`, `SECURITY.md`, etc.
- Quality tools: `.pre-commit-config.yaml`, `mypy.ini`, etc.
**Scoring:** 5 points per category detected (max 20)

### 6. Documentation (5 points max)
**What it measures:** Quality of docs and readme
**Why it matters:** Good docs indicate serious projects
**GitHub data needed:**
- README length
- Presence of docs files: `CONTRIBUTING.md`, `CHANGELOG.md`, `docs/`, etc.
**Scoring:** 1 point per indicator (max 5)

### 7. Usage Signal (5 points max)
**What it measures:** Fork ratio (forks per 1000 stars)
**Why it matters:** High fork ratio = people actually use it
**GitHub data needed:**
- `stargazers_count`
- `forks_count`
**Formula:** `(forks / stars * 100) / 200 * 5` (capped at 5)

---

## What We're Currently Getting from GitHub API

### Basic Repo Data (1 API call per repo)
- ✅ `stargazers_count` (stars)
- ✅ `forks_count` (forks)
- ✅ `created_at` (creation date)
- ✅ `updated_at` (last update)
- ✅ `open_issues_count` (open issues)
- ✅ Default branch name

### Contributors (1 API call per repo)
- ✅ Contributor count (from pagination headers)

### What We're MISSING
- ❌ **File list** (production signals) - Requires `/repos/{owner}/{repo}/git/trees/{sha}?recursive=1`
- ❌ **README length** - Could get from `/repos/{owner}/{repo}/readme`
- ❌ **Closed issues count** - Would need `/repos/{owner}/{repo}/issues?state=closed&per_page=1` and parse headers

## Current Score Breakdown

With our current data (no file scanning):
- Star velocity: 0-20 points ✅
- Freshness: 0-20 points ✅
- Issue health: 0-7.5 points (partial, assuming 50% close rate)
- Diversity: 0-15 points ✅
- Production readiness: 0 points ❌ (no file data)
- Documentation: 0 points ❌ (no file data)
- Usage signal: 0-5 points ✅

**Maximum possible score with current data: ~68/100**

## To Get Full 100-Point Scoring

We need to add these API calls per repo:
1. `/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1` - Get all files
2. `/repos/{owner}/{repo}/readme` - Get README for length/quality

This would add 2 more API calls per repo (144 total for 72 repos).
