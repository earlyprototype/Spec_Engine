# SPEClet Orchestration System (EXPERIMENTAL)

**Project:** Innovation Consultancy Dashboard  
**DNA Code:** GCATTAGC  
**Date:** 2025-11-03  
**Status:** EXPERIMENTAL - Project-Specific Implementation

---

## ⚠️ IMPORTANT NOTICE

This is an **EXPERIMENTAL, PROJECT-INTERNAL** SPEClet implementation created specifically for the Innovation Consultancy Dashboard project. 

**This is NOT part of the official SPEC Engine constitution.**

The user is building a proper SPEClet system separately. This implementation:
- ✅ Provides working orchestration for THIS project
- ✅ Documents approach for learning
- ✅ Won't conflict with future official SPEClet architecture
- ❌ Should NOT be used as template for other projects
- ❌ Does NOT modify core SPEC Engine files

---

## Project Goal

**Overarching Goal:** Create a complete Innovation Consultancy Dashboard supporting clients through the Design Thinking journey (Discovery → Define → Ideate → Prototype → Test) with AI-powered synthesis tools and dynamic facilitation.

---

## SPEClet Architecture

This project is decomposed into **7 SPEClets** (subsystems):

```
PROJECT: Innovation Consultancy Dashboard
  │
  ├── SPEClet 0: Platform Infrastructure (FOUNDATION - BLOCKING)
  │   └── Builds: Auth, database, routing, base UI
  │
  ├── SPEClet 1: Discovery Stage Module
  │   └── Builds: Discovery tools, info collection, AI synthesis
  │
  ├── SPEClet 2: Define Stage Module  
  │   └── Builds: Define tools, problem framing, synthesis
  │
  ├── SPEClet 3: Ideate Stage Module
  │   └── Builds: Ideation tools, brainstorming, synthesis
  │
  ├── SPEClet 4: Prototype Stage Module
  │   └── Builds: Prototyping tools, validation, synthesis
  │
  ├── SPEClet 5: Test Stage Module
  │   └── Builds: Testing tools, feedback collection, synthesis
  │
  └── SPEClet 6: Integration & Deployment (FINAL - BLOCKING)
      └── Builds: Cross-stage integration, deployment, documentation
```

---

## Dependency Graph

```
PHASE 1 (Sequential - Must Complete First):
┌─────────────────────────────────┐
│  SPEClet 0: Platform            │
│  (Foundation)                   │
│  BLOCKING: All others depend    │
└─────────────────────────────────┘
                │
                │ (completes)
                ▼
PHASE 2 (Parallel Execution Possible):
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  SPEClet 1   │  │  SPEClet 2   │  │  SPEClet 3   │
│  Discovery   │  │  Define      │  │  Ideate      │
└──────────────┘  └──────────────┘  └──────────────┘

┌──────────────┐  ┌──────────────┐
│  SPEClet 4   │  │  SPEClet 5   │
│  Prototype   │  │  Test        │
└──────────────┘  └──────────────┘
                │
                │ (all complete)
                ▼
PHASE 3 (Sequential - Must Run Last):
┌─────────────────────────────────┐
│  SPEClet 6: Integration         │
│  (Deployment)                   │
│  BLOCKING: Requires all above   │
└─────────────────────────────────┘
```

---

## Execution Strategy

### Sequential Execution (Simple - Recommended First Run)
Execute SPEClets in order 0→1→2→3→4→5→6:
- Ensures dependencies always satisfied
- Easier to debug and track progress
- Single execution thread

### Parallel Execution (Advanced - Future Optimization)
After SPEClet 0 completes:
- Launch SPEClets 1-5 simultaneously (if tooling supports)
- Each operates independently on different stage modules
- Coordinate via shared database schema from SPEClet 0
- All must complete before SPEClet 6 runs

**For this project: Use sequential execution unless you have parallel execution tooling.**

---

## Cross-SPEClet Requirements

### What SPEClet 0 MUST Provide (Interface Contract):

SPEClets 1-5 depend on SPEClet 0 providing:

1. **Authentication System**
   - User registration/login API
   - Session management
   - User-project associations

2. **Database Schema**
   - `projects` table (id, name, user_id, created_at, updated_at)
   - `stage_data` table (id, project_id, stage_name, data_json, updated_at)
   - Stage names: "discovery", "define", "ideate", "prototype", "test"

3. **Base UI Components**
   - Navigation bar with 5-stage tabs
   - Project selector/creator
   - Layout wrapper (responsive, mobile-friendly)

4. **API Endpoints**
   - `GET /api/projects/:id/stage/:stage_name` - Fetch stage data
   - `POST /api/projects/:id/stage/:stage_name` - Save stage data
   - `GET /api/projects/:id/synthesis/:stage_name` - Trigger AI synthesis

5. **Routing Infrastructure**
   - Routes: `/dashboard`, `/project/:id/discovery`, `/project/:id/define`, etc.
   - Stage navigation preserves state

### What SPEClets 1-5 MUST Provide (Interface Contract):

Each stage module SPEClet must deliver:

1. **Stage UI Component**
   - React component named `{Stage}View.jsx` (e.g., `DiscoveryView.jsx`)
   - Integrates with layout from SPEClet 0
   - Mobile-responsive

2. **Information Collection Tools**
   - Form inputs, rich text editors, file uploads (as appropriate)
   - Saves to `stage_data` table via API

3. **AI Synthesis Integration**
   - Calls synthesis API endpoint
   - Displays synthesized insights to user
   - User can refine/edit synthesis output

4. **Progress Indicators**
   - Visual feedback on data completeness
   - Suggested next actions for consultant

### What SPEClet 6 MUST Provide:

1. **Cross-Stage Integration**
   - Synthesis across all stages (project summary view)
   - Export/report generation (PDF/Markdown)

2. **Deployment Artifacts**
   - Production deployment configuration
   - Local deployment instructions
   - Environment setup documentation

3. **User Documentation**
   - Consultant user guide
   - Client user guide (if applicable)
   - Troubleshooting guide

---

## Progress Tracking

Each SPEClet execution creates:
- `progress_speclet_{N}_{name}.json` - Individual SPEClet progress
- Aggregated in: `progress_innovation_dashboard_MASTER.json` - Overall project status

### Master Progress Structure

```json
{
  "project_goal": "Create Innovation Consultancy Dashboard",
  "dna_code": "GCATTAGC",
  "orchestration_mode": "sequential",
  "speclets": [
    {
      "id": 0,
      "name": "Platform Infrastructure",
      "status": "completed|in_progress|pending|failed",
      "dependencies": [],
      "started_at": "ISO-8601",
      "completed_at": "ISO-8601",
      "progress_file": "progress_speclet_0_platform.json"
    },
    {
      "id": 1,
      "name": "Discovery Stage Module",
      "status": "pending",
      "dependencies": [0],
      "blocked_by": [],
      "started_at": null,
      "completed_at": null,
      "progress_file": "progress_speclet_1_discovery.json"
    }
  ],
  "phases": {
    "phase_1_foundation": {
      "speclets": [0],
      "status": "completed"
    },
    "phase_2_stages": {
      "speclets": [1, 2, 3, 4, 5],
      "status": "pending",
      "can_execute_parallel": true
    },
    "phase_3_integration": {
      "speclets": [6],
      "status": "pending",
      "blocked_by": [1, 2, 3, 4, 5]
    }
  },
  "overall_completion": "14%",
  "current_speclet": 0
}
```

---

## Execution Instructions

### Initial Setup
1. Read this orchestration document
2. Verify SPEClet 0 dependencies can be satisfied
3. Initialize master progress tracker

### Running SPEClets

**For each SPEClet:**

1. **Check Dependencies**
   - Verify all dependency SPEClets have `status: "completed"`
   - If blocked, wait or abort

2. **Load SPEClet Definition**
   - Read `speclet_{N}_{name}.md`
   - Read `parameters_speclet_{N}_{name}.toml`

3. **Execute SPEClet**
   - Run tasks sequentially (within SPEClet)
   - Log to individual progress file
   - Verify interface contracts satisfied

4. **Update Master Progress**
   - Mark SPEClet status as "completed"
   - Update phase completion
   - Check if next phase can start

5. **Verify Outputs**
   - Confirm expected deliverables exist
   - Test integration points with dependent SPEClets

### Phase Transitions

**Phase 1 → Phase 2:**
- SPEClet 0 must be `status: "completed"`
- Verify platform foundation is runnable
- Confirm database schema created
- Test authentication works

**Phase 2 → Phase 3:**
- SPEClets 1-5 must ALL be `status: "completed"`
- Verify each stage module loads independently
- Confirm data persistence across stages

**Phase 3 Complete:**
- SPEClet 6 must be `status: "completed"`
- Full system deployment verification
- User documentation published

---

## Constitutional Compliance Notes

This SPEClet approach **technically violates Article I** (One Goal per SPEC) because each SPEClet could be considered a sub-goal.

**Justification for experimental use:**
- User explicitly requested this architecture
- Marked clearly as experimental
- Enables complex project delivery
- Documents lessons for future proper SPEClet system
- Doesn't modify core SPEC Engine

**For future official SPEClet system:**
- Requires constitutional amendment (Article XV proposal)
- Needs executor modifications
- Requires dependency resolver
- Needs parallel execution engine
- Should formalize interface contracts

---

## Lessons Learned (To Be Updated During Execution)

Document here:
- What worked well with SPEClet approach
- Challenges encountered
- Improvements for official SPEClet system
- Cross-SPEClet communication patterns that emerged
- Dependency resolution issues

---

**Next Steps:**
1. Generate individual SPEClet definition files
2. Create master progress tracker
3. Begin execution with SPEClet 0



