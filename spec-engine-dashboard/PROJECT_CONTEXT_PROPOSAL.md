# Project Context Layer Proposal
**Date:** 2 January 2026  
**Purpose:** Define the value-add tier above SPEC parameters

---

## The Discovery

**parameters_{descriptor}.toml IS the DNA** - it contains all SPEC-specific configuration.

**What's missing:** A layer for PROJECT-LEVEL operational context that ALL SPECs share.

---

## Project Context Layer

### What It Is

**Runtime environment and orchestration shared across ALL SPECs in a project.**

Stored in: `SPECs/{DNA_CODE}/project_context.toml`

### What It Contains

**1. Runtime Environment**
```toml
[runtime]
database_url = "postgresql://localhost:5432/myproject"
api_base_url = "https://api.myproject.com"
deployment_target = "production"  # or "staging", "dev"
environment = "production"
```

**2. Shared Resources**
```toml
[shared_resources]
artifact_storage = "s3://gcattagc-artifacts"
log_aggregation = "cloudwatch:gcattagc-logs"
monitoring_key = "${DATADOG_API_KEY}"
notification_webhook = "https://hooks.slack.com/..."
```

**3. SPEC Orchestration**
```toml
[orchestration]
# Execution order dependencies
execution_order = [
    ["database_migration"],           # Must run first
    ["auth_service", "api_gateway"],  # Can run in parallel
    ["frontend", "docs"]               # Run after APIs ready
]

# Default execution mode for all SPECs (can be overridden per-SPEC)
default_mode = "dynamic"
```

**4. Project Metadata**
```toml
[metadata]
project_name = "Innovation Consultancy Dashboard"
dna_code = "GCATTAGC"
created_date = "2025-11-03"
last_deployed = "2026-01-02T14:30:00Z"
version = "1.2.0"
```

**5. Integration Endpoints**
```toml
[integrations]
git_repo = "https://github.com/user/project"
ci_cd_pipeline = "https://jenkins.mycompany.com/job/gcattagc"
issue_tracker = "https://jira.mycompany.com/projects/GCAT"
```

---

## Value Proposition

### Problem It Solves

**Without Project Context:**
- Every SPEC duplicates database URL, API endpoints, deployment target
- No way to see project-level execution order
- Can't track which SPECs belong to which deployment
- No centralized place for shared secrets/resources

**With Project Context:**
- Single source of truth for runtime environment
- Clear orchestration rules
- Project-level view of all SPECs
- Shared resource management

---

## Use Cases

### Use Case 1: Multi-Environment Deployment

**Scenario:** Same SPECs deployed to dev/staging/production

```toml
# SPECs/GCATTAGC-PROD/project_context.toml
[runtime]
database_url = "postgresql://prod-db:5432/myproject"
deployment_target = "production"

# SPECs/GCATTAGC-DEV/project_context.toml
[runtime]
database_url = "postgresql://localhost:5432/myproject_dev"
deployment_target = "dev"
```

**Same SPEC files, different project context = different runtime behavior.**

---

### Use Case 2: SPEC Dependency Orchestration

**Scenario:** API service needs database migration to run first

```toml
[orchestration]
execution_order = [
    ["database_migration"],
    ["api_service"],
    ["frontend"]
]
```

**Dashboard enforces order:** Can't start `api_service` until `database_migration` completes.

---

### Use Case 3: Shared Resource Management

**Scenario:** All SPECs need to upload artifacts to same S3 bucket

```toml
[shared_resources]
artifact_storage = "s3://gcattagc-artifacts"
```

**Every SPEC execution automatically has access to this shared storage.**

---

### Use Case 4: Project Health Dashboard

**Dashboard shows:**
- Project name: "Innovation Dashboard"
- All SPECs: database_migration ✓, api_service ✓, frontend ⚠️
- Last deployment: 2 hours ago
- Environment: Production
- Dependencies: Visual graph showing SPEC relationships

---

## Semantic Clarity

### DNA Metaphor Alignment

**DNA = Blueprint for organism**
- `parameters_{descriptor}.toml` = DNA for individual SPEC
- Contains all genetic instructions for that SPEC

**Project Context = Environment/Ecosystem**
- `project_context.toml` = Shared environment where SPECs live
- Not part of SPEC DNA, but affects how DNA expresses

**Biological Analogy:**
- DNA (parameters): "How to build a liver cell"
- Environment (project_context): "Body temperature, blood pH, available nutrients"

---

## Implementation Design

### File Structure

```
SPECs/GCATTAGC/
├── project_context.toml          ← NEW: Project-level runtime context
├── project_constitution.toml     ← Existing: Constitutional rules
├── spec_database_migration/
│   ├── spec_database_migration.md
│   ├── parameters_database_migration.toml  ← SPEC DNA
│   └── progress_database_migration.json
├── spec_api_service/
│   ├── spec_api_service.md
│   ├── parameters_api_service.toml         ← SPEC DNA
│   └── progress_api_service.json
```

### Inheritance Model

**NO CASCADE** - Project Context is read alongside SPEC parameters, not merged.

**At execution time:**
```javascript
// Read both independently
const projectContext = readFile('SPECs/GCATTAGC/project_context.toml');
const specParams = readFile('SPECs/GCATTAGC/spec_api/parameters_api.toml');

// Use together
const execution = {
  spec: specParams,           // SPEC-specific config
  runtime: projectContext.runtime,  // Shared runtime
  resources: projectContext.shared_resources
};
```

---

## Dashboard Integration

### Projects Page (Renamed from "DNA Profiles")

**Shows:** List of all project DNA codes
```
GCATTAGC - Innovation Consultancy Dashboard
ATGCATGC - Client Portal
TGCATGCA - Analytics Engine
```

### Project Detail Page

**Tabs:**
1. **Overview**
   - Project metadata
   - Runtime environment
   - Last deployment info

2. **SPECs**
   - List all SPECs under this project
   - Show execution status
   - Dependency graph visualization
   - **Development progress per SPEC** (see Development Progress section below)

3. **Runtime Context**
   - Edit project_context.toml
   - Manage shared resources
   - Configure orchestration

4. **Execution History**
   - Project-level execution timeline
   - Which SPECs ran when
   - Overall project health

5. **Development Dashboard**
   - Aggregate test results across all SPECs
   - Project-wide health metrics
   - Quality gate status
   - Trend analysis (velocity, quality over time)

---

## Development Progress Tracking

### Per-SPEC Progress Metrics

**Displayed for each SPEC in the project:**

**1. Execution Progress**
- Current status: Not Started | In Progress | Completed | Failed | Blocked
- Progress percentage: 0-100%
- Current task/step being executed
- Tasks completed: 12/20
- Steps completed: 45/60
- Execution duration: 2h 34m
- Estimated time remaining: 45m

**2. Test Results**
- Tests passed: 127 ✓
- Tests failed: 3 ✗
- Test coverage: 87%
- Last test run: 5 minutes ago
- Failing test details (expandable)

**3. Build Status**
- Build status: Success | Failed | In Progress
- Compilation errors: 0
- Warnings: 3
- Build time: 45s
- Last build: 10 minutes ago

**4. Code Quality Metrics**
- Linting errors: 0
- Linting warnings: 5
- Code complexity: Low | Medium | High
- Technical debt score: 2.3/10
- Security vulnerabilities: 0 critical, 1 medium

**5. Validation Status**
- SPEC validated: ✓
- Parameters validated: ✓
- Dependencies resolved: ✓
- Constitutional compliance: ✓

**6. Documentation Status**
- README present: ✓
- Goal defined: ✓
- Parameters documented: ✓
- Execution instructions: ✓
- Examples provided: ✓

**7. Git Metrics**
- Commits: 47
- Last commit: 2 hours ago
- Branch: feature/api-integration
- Uncommitted changes: 3 files

**8. Dependency Status**
- Blocked by: spec_database_migration (in progress)
- Blocking: spec_frontend (waiting)
- Dependencies met: 2/3

**9. SPECLet Breakdown** (if SPEC has SPECLets)
- SPECLet 1: Platform Foundation ✓ (100%)
- SPECLet 2: API Layer ⚠️ (65%, 2 tests failing)
- SPECLet 3: Integration → (0%, blocked)

---

### Project-Level Aggregate Metrics

**Dashboard shows overall project health:**

**1. Overall Progress**
```
Project: GCATTAGC - Innovation Dashboard
Progress: 67% complete (4/6 SPECs done)
Status: ⚠️ 2 SPECs failing tests

SPECs Status:
✓ database_migration    100% | 45 tests | 0 errors
✓ auth_service          100% | 89 tests | 0 errors  
⚠️ api_gateway          85%  | 67 tests | 3 failed
⚠️ frontend             72%  | 103 tests | 5 failed
→ docs                  40%  | 12 tests | 0 errors
→ deployment            0%   | pending
```

**2. Test Summary**
- Total tests: 316
- Passing: 308 (97.5%)
- Failing: 8 (2.5%)
- Coverage: 84% (project average)
- Trend: ↑ +2% from last week

**3. Quality Gates**
```
✓ All SPECs validated
✓ No critical security issues
✗ Test coverage below 85% target
✗ 2 SPECs with failing tests
✓ All constitutional rules met
```

**4. Velocity Metrics**
- SPECs completed this week: 2
- Average SPEC completion time: 3.5 days
- Current sprint progress: 67% (on track)

**5. Blockers**
- api_gateway: 3 integration tests failing (needs database_migration schema update)
- frontend: 5 UI tests failing (API contract changes)
- docs: Blocked waiting for api_gateway to stabilize

**6. Technical Debt**
- Critical issues: 0
- High priority: 2
- Medium priority: 7
- Code smells: 23

---

### Progress Data Sources

**Read from file system:**

**1. progress_{descriptor}.json**
```json
{
  "status": "in_progress",
  "progress_percentage": 67,
  "tasks_completed": 12,
  "tasks_total": 20,
  "current_task": "Task [3]: Implement API endpoints",
  "started_at": "2026-01-02T08:00:00Z",
  "estimated_completion": "2026-01-02T14:30:00Z"
}
```

**2. test_results_{descriptor}.json** (NEW)
```json
{
  "timestamp": "2026-01-02T12:00:00Z",
  "total": 89,
  "passed": 86,
  "failed": 3,
  "coverage": 87.5,
  "duration_ms": 4523,
  "failing_tests": [
    {
      "name": "API authentication middleware",
      "error": "Expected 200, got 401",
      "file": "tests/auth.test.ts:45"
    }
  ]
}
```

**3. build_status_{descriptor}.json** (NEW)
```json
{
  "timestamp": "2026-01-02T11:55:00Z",
  "status": "success",
  "duration_ms": 45230,
  "errors": 0,
  "warnings": 3,
  "output_size_kb": 2340
}
```

**4. quality_metrics_{descriptor}.json** (NEW)
```json
{
  "timestamp": "2026-01-02T12:00:00Z",
  "lint_errors": 0,
  "lint_warnings": 5,
  "complexity_score": 2.3,
  "technical_debt_minutes": 140,
  "security_issues": {
    "critical": 0,
    "high": 0,
    "medium": 1
  }
}
```

**5. validation_status_{descriptor}.json** (NEW)
```json
{
  "spec_valid": true,
  "parameters_valid": true,
  "dependencies_resolved": true,
  "constitutional_compliance": true,
  "last_validated": "2026-01-02T08:00:00Z"
}
```

---

### Development Dashboard Features

**1. Real-time Updates**
- WebSocket pushes progress updates to dashboard
- Auto-refresh test results when tests run
- Live execution status changes

**2. Filtering & Sorting**
- Filter by: Status, Test results, Coverage threshold
- Sort by: Progress, Tests failing, Last updated
- Search by: SPEC name, descriptor, tags

**3. Visual Indicators**
```
✓ Green: All tests passing, 100% complete
⚠️ Amber: Tests failing OR in progress
✗ Red: Build failed OR critical errors
→ Grey: Not started OR blocked
```

**4. Drill-down Views**
- Click SPEC → See detailed progress
- Click test count → See failing test details
- Click coverage → See uncovered files
- Click blocker → See dependency graph

**5. Trend Analysis**
- Progress over time chart
- Test success rate trend
- Coverage trend
- Velocity chart (SPECs completed per week)

**6. Notifications**
- Alert when tests fail
- Alert when SPEC completes
- Alert when blockers resolved
- Daily digest of project health

---

## Comparison: Old vs New

### Old Interpretation (WRONG)

```
DNA Profile Form → Create new DNA → Store in database → Generate files
```

**Problems:**
- Creates new projects from scratch through UI
- Treats DNA as database records
- Ignores existing file structure

### New Interpretation (CORRECT)

```
Browse SPECs/ directory → Find GCATTAGC → Read project_context.toml → Display project dashboard
```

**Benefits:**
- File system is source of truth
- Shows existing projects
- Project context adds operational value

---

## What Changes in the Dashboard

### Before (Misguided)

1. **DNA Profiles page:** Form to create new DNA profiles
2. **Focus:** CRUD operations on DNA records

### After (Correct)

1. **Projects page:** Browse existing projects from `SPECs/*/`
2. **Project Detail:** 
   - Shows project_context.toml (runtime environment)
   - Lists all SPECs under this project
   - Displays SPEC dependencies
   - Shows execution history
3. **Focus:** View/manage project-level operational context

---

## Backward Compatibility

**Existing SPECs without project_context.toml work fine.**

If `project_context.toml` doesn't exist:
- Use sensible defaults
- Allow inline execution (no orchestration enforcement)
- Dashboard shows warning: "No project context configured"

---

## Next Steps

### Phase 1: Minimal Viable Change

1. Keep existing backend/frontend mostly intact
2. Rename "DNA Profiles" → "Projects"
3. Change GET /api/projects to scan `SPECs/*/` directories (file-based)
4. Show project names from existing `project_constitution.toml` files
5. Project detail shows: List of SPECs under that DNA code

### Phase 2: Add Project Context Support

1. Create `project_context.toml` schema
2. Add editor for project context
3. Backend reads project context during execution
4. Use orchestration rules to enforce SPEC order

### Phase 3: Dashboard Enhancements

1. SPEC dependency graph visualization
2. Project-level execution timeline
3. Environment selector (dev/staging/prod contexts)
4. Shared resource management UI

---

## Conclusion

**Project Context Layer has clear value:**
- Runtime environment shared across SPECs
- Orchestration rules for SPEC dependencies
- Project-level view of all related SPECs
- Shared resource management

**Not configuration cascade - it's operational context.**

**Semantically distinct from SPEC parameters (DNA):**
- parameters_{descriptor}.toml = SPEC DNA (what to build)
- project_context.toml = Environment (where it runs)

**This clarifies the architecture and adds genuine value above SPEC parameters.**
