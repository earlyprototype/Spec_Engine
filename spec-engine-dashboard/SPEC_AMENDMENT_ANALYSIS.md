# SPEC Amendment Analysis
**Date:** 2 January 2026  
**Purpose:** How to update the Dashboard SPEC to reflect Project Context architecture

---

## Current SPEC Issues

### Line 119: "DNA Profile Manager (create, edit, view profiles)"

**Current interpretation:** Form-based CRUD to create new DNA profiles

**Should be:** 
- "Project Browser (browse, view projects)"
- "Project Detail (view project context, list SPECs, show dependencies)"

**Amendment:**
```markdown
- Project Browser (browse existing projects from SPECs/ directory)
- Project Detail Viewer (runtime context, SPEC list, dependency graph)
- Project Context Editor (edit project_context.toml)
```

---

### Line 136: "DNA profiles table (dna_code, settings, created_at)"

**Current:** Database-first approach storing DNA profile data

**Should be:** 
- Database only caches metadata for UI performance
- File system (`SPECs/*/project_context.toml`) is source of truth

**Amendment:**
```markdown
- Projects cache table (dna_code, project_name, last_scanned, spec_count)
- SPECs table (spec_id, dna_code, descriptor, status)
- Executions table (execution_id, spec_id, status, started_at, completed_at)
- Progress logs table (execution_id, task_id, step_id, status, timestamp)
```

**Note:** Projects table is a CACHE, not primary storage

---

### SPECLet 3: "DNA Profile Management"

**Current focus:**
- Task [3.1]: Build DNA profile list view
- Task [3.2]: Implement DNA creation form
- Task [3.3]: Add DNA editing and viewing capabilities

**Should be:**
- Task [3.1]: Build Project Browser (scan `SPECs/*/` directories)
- Task [3.2]: Implement Project Detail Page (show project context + SPECs list)
- Task [3.3]: Add Project Context Editor (edit `project_context.toml`)

**Key change:** Read from file system, not create through forms

---

## Recommended SPEC Amendments

### 1. Rename Throughout

**Find/Replace:**
- "DNA Profile" → "Project"
- "DNA Profile Management" → "Project Management"
- "DNA profile table" → "Projects cache table"

**Keep "DNA" only in biological/metaphor contexts:**
- "parameters_{descriptor}.toml = SPEC DNA" ✓
- "DNA code (GCATTAGC)" ✓

---

### 2. Update Component Descriptions

**Old (Line 119):**
```markdown
- DNA Profile Manager (create, edit, view profiles)
```

**New:**
```markdown
- Project Browser (browse projects from SPECs/ directory)
- Project Detail Viewer (context, SPECs, dependencies, execution history)
- Project Context Editor (Monaco editor for project_context.toml)
```

---

### 3. Clarify Database Role

**Add to Constraints (after Line 159):**
```markdown
- Database is a CACHE for UI performance only
- File system (SPECs/ directory) is the source of truth
- On startup, scan SPECs/ and sync database cache
- Never store SPEC content or parameters in database
```

---

### 4. Add Project Context Definition

**Add new section after Line 100:**

```markdown
## Project Context

**Definition:** Operational runtime environment shared across all SPECs in a project.

**File:** `SPECs/{DNA_CODE}/project_context.toml`

**Contents:**
- Runtime environment (database URL, API endpoints, deployment target)
- Shared resources (artifact storage, monitoring keys, webhooks)
- SPEC orchestration (execution order, dependencies)
- Project metadata (name, version, last deployed)

**Purpose:**
- Provide project-level view of all related SPECs
- Manage shared operational context
- Enforce SPEC execution dependencies
- Track project-level deployment history

**Not a cascade:** Project context is read ALONGSIDE SPEC parameters, not merged.
```

---

### 5. Update SPECLet 3 Tasks

**Old:**
```markdown
### SPECLet [3]: DNA Profile Management
Tasks:
- Task [3.1]: Build DNA profile list view
- Task [3.2]: Implement DNA creation form
- Task [3.3]: Add DNA editing and viewing capabilities
```

**New:**
```markdown
### SPECLet [3]: Project Management
Tasks:
- Task [3.1]: Build Project Browser (scan SPECs/ directories, list existing projects)
- Task [3.2]: Implement Project Detail Page (show context, list SPECs, visualize dependencies)
- Task [3.3]: Add Project Context Editor (Monaco editor for project_context.toml with validation)
```

---

### 6. Update User Stories

**Old (Line 176):**
```markdown
- As a **project manager**, I want to manage multiple DNA profiles through a dashboard so I can organise projects efficiently
```

**New:**
```markdown
- As a **project manager**, I want to browse all projects and view their SPECs so I can organise work efficiently
- As a **operator**, I want to see SPEC dependencies within a project so I know which must run first
- As a **developer**, I want to manage project-level runtime context so all SPECs share the same environment
```

---

### 7. Clarify File Structure in Definitions

**Add to Definitions section (after Line 110):**

```markdown
**File Structure:**
```
SPECs/
├── GCATTAGC/                           # DNA code = Project
│   ├── project_context.toml            # Runtime context (NEW)
│   ├── project_constitution.toml       # Constitutional rules
│   ├── spec_database_migration/
│   │   ├── spec_database_migration.md
│   │   ├── parameters_database_migration.toml  # SPEC DNA
│   │   ├── progress_database_migration.json    # Execution progress
│   │   ├── test_results_database_migration.json    # Test metrics (NEW)
│   │   ├── build_status_database_migration.json    # Build status (NEW)
│   │   ├── quality_metrics_database_migration.json # Code quality (NEW)
│   │   └── validation_status_database_migration.json # Validation (NEW)
│   └── spec_api_service/
│       ├── spec_api_service.md
│       ├── parameters_api_service.toml         # SPEC DNA
│       ├── progress_api_service.json
│       ├── test_results_api_service.json       # Test metrics (NEW)
│       ├── build_status_api_service.json       # Build status (NEW)
│       ├── quality_metrics_api_service.json    # Code quality (NEW)
│       └── validation_status_api_service.json  # Validation (NEW)
```
```

---

### 8. Add Development Progress Tracking

**Add new section:**

```markdown
## Development Progress Tracking

The dashboard displays comprehensive development progress for each SPEC:

**Per-SPEC Metrics:**
- Execution progress (status, tasks/steps completed, duration)
- Test results (passed/failed, coverage, failing test details)
- Build status (success/failed, errors, warnings, build time)
- Code quality (linting, complexity, technical debt, security)
- Validation status (SPEC, parameters, dependencies, constitutional compliance)
- Documentation status (README, goal, parameters, examples)
- Git metrics (commits, last commit, branch, uncommitted changes)
- Dependency status (blocked by, blocking, dependencies met)
- SPECLet breakdown (if applicable)

**Project-Level Aggregate:**
- Overall progress (% complete, SPECs done/total)
- Test summary (total tests, passing/failing, coverage)
- Quality gates (validation, security, coverage targets)
- Velocity metrics (SPECs completed, average time, sprint progress)
- Blockers (list of blocked SPECs with reasons)
- Technical debt (critical/high/medium issues)

**Data Sources:**
New JSON files per SPEC:
- `test_results_{descriptor}.json` - Test execution results
- `build_status_{descriptor}.json` - Build success/failure
- `quality_metrics_{descriptor}.json` - Linting, complexity, security
- `validation_status_{descriptor}.json` - Validation checks

**Dashboard Features:**
- Real-time WebSocket updates
- Filter/sort by status, test results, coverage
- Visual indicators (✓ Green, ⚠️ Amber, ✗ Red, → Grey)
- Drill-down views for detailed metrics
- Trend analysis charts
- Notification system for failures/completions
```

---

## Implementation Strategy

### Option 1: Minimal Change (Recommended)

**Keep 80% of existing code, rebrand and redirect:**

1. Rename frontend routes: `/dna-profiles` → `/projects`
2. Update backend to scan `SPECs/*/` instead of database queries
3. Project detail page shows:
   - Project name from `project_constitution.toml`
   - List of SPECs under that DNA code (scan `spec_*/` directories)
   - Option to edit `project_context.toml` (if exists)

**Changes needed:**
- Frontend: 3 files (rename, update API calls)
- Backend: 2 files (dna.routes.ts → projects.routes.ts, scan file system)
- Database: No schema change needed (just rename table)

**Effort:** 2-3 hours

---

### Option 2: Full Rebuild

**Scrap DNA management, rebuild as Projects:**

1. Delete DNA profile CRUD code
2. Build file-based project scanner
3. Add project_context.toml editor
4. Add SPEC dependency visualization

**Changes needed:**
- Frontend: Rebuild 5 pages
- Backend: Rebuild 3 services
- Database: Simplify schema

**Effort:** 2-3 days

---

### Option 3: Document Vision, Minimal MVP

**Keep current broken state, just document the correct approach:**

1. Write SPEC amendment document
2. Note divergences in current implementation
3. Provide roadmap for future fixes
4. Focus on getting Parameter Editor + Execution working first

**Changes needed:**
- Documentation only
- Mark "Projects" as "partial implementation"

**Effort:** 30 minutes

---

## Recommended Path Forward

**Phase 1: Quick Win (Now)**
1. Fix execution page (already done)
2. Get Parameter Editor loading `parameters_{descriptor}.toml` correctly
3. Document the Project Context vision

**Phase 2: Rebrand (Next)**
1. Rename "DNA Profiles" → "Projects"
2. Make it file-based (scan `SPECs/*/`)
3. Show list of SPECs under each project

**Phase 3: Enhance (Later)**
1. Add `project_context.toml` editor
2. Add SPEC dependency graph
3. Project-level execution history
4. Development progress tracking dashboard
5. Test results visualization
6. Quality metrics and trend analysis

---

## Key Insights for SPEC Amendment

### 1. The SPEC Was Ambiguous

**"DNA Profile Management" could mean:**
- Create new DNA profiles (wrong interpretation)
- Manage existing project files (correct interpretation)

**Amendment should clarify:**
- "Browse existing projects from file system"
- "View project-level operational context"
- "Edit project_context.toml for runtime environment"

---

### 2. Database Role Unclear

**SPEC says:**
- "SQLite for execution history and metadata"
- "DNA profiles table"

**This led to:**
- Storing DNA profiles IN database (wrong)
- Database as primary storage (wrong)

**Amendment should clarify:**
- "Database CACHES file system for UI performance"
- "File system is source of truth"
- "Database stores: execution history, progress logs, UI state ONLY"

---

### 3. Missing Architecture Diagram

**SPEC should include:**

```
┌─────────────┐
│ File System │  ← SOURCE OF TRUTH
│ SPECs/*     │
└──────┬──────┘
       │ scan/watch
       ↓
┌─────────────┐
│  Backend    │
│  Services   │
└──────┬──────┘
       │ cache
       ↓
┌─────────────┐
│  Database   │  ← CACHE + Execution History
│  (SQLite)   │
└──────┬──────┘
       │ query
       ↓
┌─────────────┐
│  Dashboard  │
│  Frontend   │
└─────────────┘
```

---

## Conclusion

**Most effective amendment approach:**

1. **Clarify semantics:** "DNA Profile" → "Project", make file-based explicit
2. **Add Project Context definition** as new concept
3. **Update SPECLet 3** to focus on browsing/viewing, not creating
4. **Add architecture diagram** showing file system → backend → database → UI flow
5. **Specify database as cache**, not primary storage

**Implementation:** Option 1 (Minimal Change) - rename and redirect existing code to file system.

**Effort:** Small SPEC changes, medium code changes (2-3 hours), maintains 80% of existing work.
