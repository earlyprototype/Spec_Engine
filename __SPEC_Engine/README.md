# SPEC Engine Documentation

**Version:** 1.3  
**Last Updated:** 2025-11-03  
**Purpose:** Structured workflow system for LLM-driven goal achievement

---

## What Is This?

The SPEC Engine is a constitutional framework that transforms high-level goals into structured, executable specifications for LLMs. It provides:

- **Goal-driven architecture:** Every element serves a singular North Star goal
- **Constitutional governance:** 14 Articles ensure quality and consistency
- **Three-file architecture:** Human-readable + Machine-readable + Execution controller
- **Project-level configuration:** Optional DNA profiles for per-project preferences
- **Built-in validation:** Pre-flight, runtime, and post-execution quality checks

---

## Quick Start: First Time Here?

**Step 1: Read This Overview** (you are here)  
**Step 2: Read `WORKFLOW_DIAGRAM.md`** - See the complete lifecycle  
**Step 3: Read `_Constitution/constitution.md`** - Understand governing principles  
**Step 4: Try creating a spec with `_Commander_SPEC/Spec_Commander.md`**

**For Beginners:** Start with `GETTING_STARTED.md` (beginner-friendly tutorial)

---

## Document Map

### Core Governance
```
_Constitution/
├── constitution.md          ⭐ START HERE - 14 immutable Articles
└── DESIGN_PHILOSOPHY.md     WHY decisions were made this way
```

**Read these first** to understand the system's foundations.

### Spec Generation
```
_Commander_SPEC/
└── Spec_Commander.md        🤖 Master coordinator for generating specs
```

**Use this** to create new specifications from goals.

### Project Configuration (Optional)
```
_DNA/
└── DNA_SPEC.md              🧬 Project-level preferences interview
```

**Use this** to configure project-wide settings (testing, risk, autonomy).

### Templates
```
_templates/
├── Spec_template.md         📄 Human-readable spec structure
├── parameters_template.toml ⚙️  Machine-readable parameters
└── exe_template.md          🚀 Execution controller logic
```

**These are templates** - don't edit directly. Commander generates from these.

### Meta-Documentation
```
WORKFLOW_DIAGRAM.md          Complete lifecycle from goal → execution → completion
COHERENCE_REVIEW.md          System-wide consistency validation (2025-11-02)
README.md                    This file
GETTING_STARTED.md           Beginner tutorial (coming soon)
```

---

## System Architecture

### Three Layers

```
┌─────────────────────────────────────────────────────┐
│  SYSTEM CONSTITUTION (immutable)                    │
│  Articles I-XIV                                     │
│  _Constitution/constitution.md                      │
└──────────────────┬──────────────────────────────────┘
                   │ governs
            ┌──────▼──────────────────────────────┐
            │  PROJECT CONSTITUTION (optional)    │
            │  Per-project preferences            │
            │  Specs/[DNA_CODE]/                  │
            │  project_constitution.toml          │
            └──────┬──────────────────────────────┘
                   │ configures
            ┌──────▼──────────────────────────────┐
            │  INDIVIDUAL SPEC (goal-specific)    │
            │  3 files per goal:                  │
            │  • spec_[descriptor].md             │
            │  • parameters_[descriptor].toml     │
            │  • exe_[descriptor].md              │
            └─────────────────────────────────────┘
```

### Three-File Specification

Every goal becomes a **SPEC** consisting of:

1. **spec_[descriptor].md** - Human-readable narrative
   - Goal, tasks, steps, backups
   - Software stack (for build goals)
   - Definition of complete
   - Cross-references to TOML

2. **parameters_[descriptor].toml** - Machine-readable config
   - Identical structure to markdown
   - Enables automated validation
   - Logging and error handling config

3. **exe_[descriptor].md** - Execution controller
   - Validation logic (Section 1)
   - Execution flow (Section 2)
   - Mode control (Section 3)
   - Post-execution analysis (Section 6)

4. **progress_[descriptor].json** - Runtime log (auto-generated)
   - Step outcomes
   - Retry counts
   - Mode switches
   - Constitutional compliance tracking

---

## Key Concepts

### The North Star Principle (Article I)
Every spec has **exactly one goal**. Multiple goals require separate specs.

### Goal → Task → Step → Backup Hierarchy (Article II)

#### Simple Spec Structure:
```
GOAL (singular outcome)
  └── TASK [n] (discrete objective, 2-5 per spec)
      └── STEP [m] (concrete action, 1-5 per task)
          └── BACKUP [p] (alternative method, 0-2 per step)
```

#### Complex Spec Structure (with SPECLets):
```
GOAL (singular outcome)
  └── SPECLet [s] (work package, 1-n per spec, optional)
      └── TASK [n] (discrete objective, 2-5 per SPECLet)
          └── STEP [m] (concrete action, 1-5 per task)
              └── BACKUP [p] (alternative method, 0-2 per step)
```

**Use SPECLets when:** Multi-phase goals, >5 tasks, or parallel execution beneficial  
**Skip SPECLets for:** Straightforward goals with 2-5 sequential tasks

### Execution Modes (Article IX)
- **Silent:** Fully autonomous
- **Collaborative:** Human-in-loop
- **Dynamic (default):** Autonomous with intelligent escalation

### Critical Flags (Article VI)
- `critical = true`: Failure blocks goal, escalate after exhaustion
- `critical = false`: Log failure, continue execution
- **Balance:** 40-60% of steps should be critical

### Backups as Alternatives (Article VII)
Backups must be **alternative reasoning paths**, not simple retries.

**Invalid:** "Try again"  
**Valid:** "If documentation incomplete, inspect source code directly"

### Constitutional Enforcement (Articles I-XIV)
Three checkpoints:
1. **Pre-flight:** Commander validates before generation
2. **Runtime:** Exe checks compliance during execution
3. **Post-execution:** Analysis reviews adherence

---

## MCP Tool Integration (NEW - 2025-11-03)

The SPEC Engine now integrates MCP (Model Context Protocol) tool selection into the workflow:

- **Step 2.5:** Commander analyses goals and autonomously recommends relevant MCP servers
- **Step 3a:** Combined human review + tool installation (single pause point)  
- **Section 1.11:** Executor verifies tools before execution as safety check

**Tool Catalog:** `__SPEC_Engine/_tools/mcp_tools_catalog.yaml`
- 269 MCP servers
- 2900+ individual tools
- 24 categories (Databases, Cloud, AI/ML, Search, etc.)

**Benefits:**
- LLM autonomously selects tools based on goal requirements
- Human approves and installs in one workflow step
- Execution validates availability before proceeding
- Prevents tool-related execution failures

**See:** `GETTING_STARTED.md` for tutorial, `WORKFLOW_DIAGRAM.md` for complete flow

---

## Typical Workflow

### Phase 1: Project Setup (Optional, ~3 minutes)
```
Run DNA_SPEC.md interview
  ↓
Answer 5 questions about project
  ↓
Generate DNA code (e.g., ATGCTCGA)
  ↓
Create Specs/ATGCTCGA/project_constitution.toml
```

**When to use DNA profiles:**
- Multiple specs for same project
- Want consistent testing/risk preferences
- Custom tooling or constraints

**When to skip:**
- One-off goal
- Flexible about configuration
- Want system defaults

### Phase 2: Spec Generation (~20 minutes)
```
Launch Spec_Commander.md with goal
  ↓
Commander drafts high-level structure
  ↓
MANDATORY HUMAN REVIEW (approve/revise/clarify)
  ↓
Commander generates detailed steps
  ↓
Pre-flight validation (constitutional compliance)
  ↓
3 files created in Specs/[DNA_CODE]/spec_[descriptor]/
```

### Phase 3: Execution (Variable)
```
Launch exe_[descriptor].md
  ↓
Initialization & validation (Section 1)
  ↓
User selects mode (Dynamic/Silent/Collaborative)
  ↓
Execute tasks sequentially (Section 2)
  - Try primary method
  - Try backups if failure
  - Escalate if critical + exhausted
  - Log everything to progress.json
  ↓
Post-execution analysis (Section 6)
  - Failure patterns
  - Backup effectiveness
  - Constitutional compliance review
  - Completion verification
  ↓
Goal ACHIEVED / PARTIAL / NOT ACHIEVED
```

---

## When To Use Each Document

| Document | When To Use |
|----------|-------------|
| `constitution.md` | Before creating any spec (understand rules) |
| `DESIGN_PHILOSOPHY.md` | When you want to know WHY (rationale) |
| `WORKFLOW_DIAGRAM.md` | To see complete lifecycle flow |
| `Spec_Commander.md` | To CREATE a new spec from a goal |
| `DNA_SPEC.md` | To configure project-level preferences |
| `exe_[descriptor].md` | To EXECUTE an existing spec |
| `Spec_template.md` | Reference when writing custom specs |
| `parameters_template.toml` | Reference for TOML structure |
| `GETTING_STARTED.md` | First-time beginner tutorial |

---

## File System Requirements

### Expected Directory Structure
```
[Your Workspace Root]/
├── __SPEC_Engine/           # This directory (framework)
│   ├── README.md
│   ├── WORKFLOW_DIAGRAM.md
│   ├── COHERENCE_REVIEW.md
│   ├── _Constitution/
│   ├── _Commander_SPEC/
│   ├── _DNA/
│   └── _templates/
│
└── SPECs/                   # Generated specs live here
    ├── [DNA_CODE_1]/        # Project 1 (e.g., ATGCTCGA)
    │   ├── project_constitution.toml
    │   ├── spec_[descriptor_1]/
    │   │   ├── spec_[descriptor_1].md
    │   │   ├── parameters_[descriptor_1].toml
    │   │   ├── exe_[descriptor_1].md
    │   │   └── progress_[descriptor_1].json
    │   └── spec_[descriptor_2]/
    │
    └── [DNA_CODE_2]/        # Project 2 (e.g., TGCAATGC)
        └── ...
```

**Important:** 
- Framework files live in `__SPEC_Engine/`
- Generated specs live in `SPECs/[DNA_CODE]/spec_[descriptor]/`
- DNA codes are 8 characters using A, T, G, C only
- Each spec lives in its own folder

---

## Common Questions

### Q: Do I need a DNA profile?
**A:** No, it's optional. DNA profiles are useful when:
- Creating multiple specs for same project
- Want consistent testing/risk/autonomy settings
- Have custom tools or constraints

Without DNA, Commander uses system defaults.

### Q: Can I edit templates directly?
**A:** No. Templates in `_templates/` are blueprints. Commander generates from these. Edit generated files in `SPECs/[DNA_CODE]/spec_[descriptor]/` instead.

### Q: What if validation fails?
**A:** Exe will HALT and explain what's missing. Common issues:
- Goal not singular (Article I)
- Tasks/steps out of 2-5 / 1-5 range (Article II)
- Markdown ↔ TOML mismatch (Article III)
- Software stack undefined for build goals (Article XIV)

Fix the spec files and re-run.

### Q: Can I use this for non-coding goals?
**A:** Yes! SPECs work for any goal:
- Research and analysis
- Content creation
- Data processing
- Testing and QA
- System administration
- And yes, building software

### Q: How do I know if my goal is "complete"?
**A:** Exe Section 6.4 verifies completion criteria from your spec:
- Primary deliverable exists
- Quality standards met
- Verification method passed
- (For build goals) Deployment artifact exists, UI implemented, production-ready

Status: ACHIEVED (all pass) / PARTIAL (core works, deployment incomplete) / NOT ACHIEVED (broken)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.3 | 2025-11-03 | Added SPECLet abstraction layer for complex multi-phase goals with parallel execution support |
| 1.0 | 2025-11-02 | Initial README created during structural review |

---

## Getting Help

**Read first:**
1. This README (overview)
2. `WORKFLOW_DIAGRAM.md` (detailed workflow)
3. `_Constitution/constitution.md` (governing rules)

**Stuck?**
- Check `COHERENCE_REVIEW.md` for system health status
- Review example specs in `SPECs/Testing/`
- Consult `DESIGN_PHILOSOPHY.md` for design rationale

**Contributing:**
- Document must align with constitution.md
- Changes require constitutional amendment process (Article XIII)
- Test changes with example specs before committing

---

**Next Steps:** Read `WORKFLOW_DIAGRAM.md` to see the complete lifecycle, then try creating your first spec with `Spec_Commander.md`.

