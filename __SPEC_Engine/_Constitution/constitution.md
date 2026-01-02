# Constitution SPEC

**Version:** 1.3  
**Date:** 3 November 2025  
**Status:** Immutable Foundation  
**Purpose:** Define the governing principles for all Specs in this system

---

## Context

**What This Is:**  
This document establishes a constitutional foundation for the SPECS system

**Why It Exists:**  
- Consistency across specs created by different users or at different times
- Quality gates that prevent common anti-patterns
- Clear rules for LLM executors to follow
- Architectural integrity as the system scales


**Integration Points:**
- Referenced by `Spec_Commander.md` Step 5 (validation)
- Enforced by `exe_template.md` Section 1.1-1.10 (pre-flight checks)
- Used by spec authors as quality checklist

---

## Introduction
This Constitution establishes the foundational principles that govern all Spec creation, validation, and execution within the SPECS system. These principles are immutable and must be respected by all Specs, regardless of domain or descriptor.

**Rationale:** Consistency across Specs enables reliable LLM behaviour, predictable validation, and maintainable workflows.

---

## Article I: The North Star Principle

### Section 1.1: Singular Goal Requirement
Every Spec MUST define exactly **one goal**. Multiple goals require separate Specs.

### Section 1.2: Goal Characteristics
The goal MUST be:
- **Singular:** One outcome, not multiple competing objectives
- **Clear:** Unambiguous and understandable by both humans and LLMs
- **Measurable:** Success or failure must be determinable
- **Explicit:** No implied or unstated objectives

### Section 1.3: Goal-Directed Behaviour
Every task, step, and backup within a Spec MUST demonstrably contribute to achieving the stated goal.

**Validation Question:** "If this element were removed, could the goal still be achieved?"
- If YES → element is optional or redundant
- If NO → element is essential and properly aligned

---

## Article II: Hierarchical Structure

### Section 2.1: The Inviolable Hierarchy
All Specs MUST adhere to one of two hierarchical structures:

#### Simple Spec Structure (for straightforward goals):
```
GOAL (singular, North Star)
  └── TASK [n] (discrete objective, 2-5 per Spec)
      └── STEP [m] (concrete action, 1-5 per task)
          └── BACKUP [p] (alternative method, 0-2 per step)
```

#### Complex Spec Structure (for multi-phase or large goals):
```
GOAL (singular, North Star)
  └── SPECLet [s] (work package, 1-n per Spec, optional)
      └── TASK [n] (discrete objective, 2-5 per SPECLet)
          └── STEP [m] (concrete action, 1-5 per task)
              └── BACKUP [p] (alternative method, 0-2 per step)
```

**When to use SPECLets:**
- Goal requires multiple distinct phases or work packages
- Different task groups have dependencies on each other
- Parallel execution would benefit the workflow
- Task count would exceed 5 without grouping

**When to skip SPECLets:**
- Goal is straightforward with 2-5 cohesive tasks
- No clear phase boundaries or dependencies
- Sequential execution is optimal

### Section 2.2: Preventing Conflation
- **Goals** are outcomes to achieve
- **SPECLets** (optional) are cohesive work packages that group related tasks
- **Tasks** are objectives that advance the goal (or SPECLet)
- **Steps** are actions that complete the task
- **Backups** are alternative methods for steps

These distinctions MUST be maintained. Treating tasks as steps, goals as tasks, or SPECLets as tasks violates this Article.

### Section 2.3: Quantitative Constraints

#### Simple Spec Structure:
- Goals per Spec: **1**
- Tasks per goal: **2-5** (fewer than 2 is under-decomposed; more than 5 suggests need for SPECLets)
- Steps per task: **1-5** (maintain atomic actions)
- Backups per step: **0-2** (more than 2 indicates poor primary method selection)

#### Complex Spec Structure (with SPECLets):
- Goals per Spec: **1**
- SPECLets per goal: **1-n** (no upper limit, but typically 2-8 for practical projects)
- Tasks per SPECLet: **2-5** (maintain cohesion within work packages)
- Steps per task: **1-5** (maintain atomic actions)
- Backups per step: **0-2** (more than 2 indicates poor primary method selection)

### Section 2.4: SPECLet Dependencies and Parallel Execution

When using SPECLets, dependency relationships MUST be explicitly declared:

**Dependency Declaration:**
- Each SPECLet MUST declare which other SPECLets (if any) it depends on
- Dependencies use SPECLet IDs: `depends_on = ["speclet_id_1", "speclet_id_2"]`
- Empty dependency array indicates no dependencies: `depends_on = []`

**Execution Rules:**
- SPECLets with no dependencies CAN execute in parallel
- SPECLets with dependencies MUST wait for prerequisite SPECLets to complete
- Circular dependencies are PROHIBITED
- The executor MUST validate dependency graph for cycles during initialisation

**Parallel Execution:**
- SPECLets marked with `parallel_allowed = true` MAY execute concurrently if dependencies satisfied
- Tasks within a SPECLet execute sequentially (no intra-SPECLet parallelism)
- Progress tracking MUST capture SPECLet-level status (not_started, in_progress, completed, blocked)

**Example Dependency Structure:**
```
SPEC: "Build Design Thinking Dashboard"
  ├─ SPECLet A: "platform_foundation" [depends_on: []]
  ├─ SPECLet B: "discovery_stage" [depends_on: ["platform_foundation"]]
  ├─ SPECLet C: "define_stage" [depends_on: ["platform_foundation"]]
  ├─ SPECLet D: "ideate_stage" [depends_on: ["define_stage"]]
  ├─ SPECLet E: "prototype_stage" [depends_on: ["ideate_stage"]]
  └─ SPECLet F: "test_stage" [depends_on: ["prototype_stage"]]

Execution Flow:
- A executes first (no dependencies)
- B and C can execute in parallel once A completes
- D waits for C
- E waits for D
- F waits for E
```

---

## Article III: Dual-File Mandate

### Section 3.1: The Two Artefacts
Every Spec MUST consist of:
1. **spec_[descriptor].md** - Human-readable intent and reasoning
2. **parameters_[descriptor].toml** - Machine-readable structure and configuration

### Section 3.2: Bridging Requirement
The two files MUST maintain perfect synchronisation:
- Every task in Markdown MUST have corresponding TOML entry
- Every step in Markdown MUST have corresponding TOML entry
- Task and step IDs MUST match exactly
- Sequence order MUST be identical

### Section 3.3: Cross-Reference Requirement
Markdown files MUST contain explicit references to TOML keys:
- `"See constraints.max_latency in parameters_[descriptor].toml"`
- `"TOML Reference: tasks[id=1]"`

**Rationale:** Explicit bridging prevents file drift and maintains human-LLM alignment.

---

## Article IV: Validation Before Execution

### Section 4.1: Mandatory Pre-Flight Validation
NO Spec execution may begin without successful completion of validation (exe_[descriptor].md Section 1.1-1.10):

1. **File Presence Check** (Section 1.1)
2. **Progress Log Initialisation** (Section 1.2)
3. **Parse Specification Files** (Section 1.3)
4. **Validate Goal** (Section 1.4)
5. **Validate Tasks** (Section 1.5)
6. **Validate Steps** (Section 1.6)
7. **Validate Backups** (Section 1.7)
8. **Bridging Verification** (Section 1.8)
9. **Validate Components and Constraints** (Section 1.9)
10. **Validation Summary and Pre-Flight Check** (Section 1.10)

### Section 4.2: Halt on Critical Validation Errors
If validation detects critical errors, execution MUST NOT proceed until errors are resolved.

**Critical Errors Include:**
- Missing goal or multiple goals
- Task/step ID mismatches between Markdown and TOML
- Missing expected outputs for steps
- Duplicate IDs
- Invalid file syntax (unparseable TOML, malformed Markdown)

---

## Article V: Explicitness Over Implicitness

### Section 5.1: Explicit Declarations
The system MUST favour explicit declarations over implicit assumptions in all contexts:

- **Expected outputs:** Specific and measurable, not vague
  - ✅ "Markdown table with 3 columns: function name, parameter count, return type"
  - ❌ "Some results"

- **Backup methods:** Alternative approaches, not generic retries
  - ✅ "Use linter tool X if manual inspection fails"
  - ❌ "Try alternative method"

- **Cross-references:** Direct key references
  - ✅ "See `constraints.coverage_required` in TOML"
  - ❌ "Check constraints"

### Section 5.2: No Placeholder Ambiguity
Template placeholders like `[Insert description here]` MUST be replaced with specific content before execution.

---

## Article VI: Critical Flag Discipline

### Section 6.1: Critical Flag Purpose
The `critical_flag` identifies steps whose failure requires escalation.

### Section 6.2: Critical Flag Guidelines
- **critical_flag = true:** Failure blocks goal achievement; escalate after backup exhaustion
- **critical_flag = false:** Failure logged as warning; execution continues

### Section 6.3: Criticality Balance
Typically **40-60% of steps** should be critical:
- **Over-criticality** (>80%): Everything escalates; workflow grinds to halt
- **Under-criticality** (<20%): Failures accumulate silently; goal unachievable

### Section 6.4: Validation Requirement
Spec authors MUST justify why each step is marked critical or non-critical during validation.

---

## Article VII: Backup Methods as Alternative Reasoning

### Section 7.1: Backup Philosophy
Backups MUST be **alternative reasoning paths or methods**, NOT simple retries of the same approach.

**Invalid Backup:** "Try again"  
**Valid Backup:** "If documentation incomplete, inspect source code directly"

### Section 7.2: Backup Types
Two categories of backups are permitted:

#### A. Cognitive Alternative Backups
- Alternative analysis techniques
- Different data sources
- Alternative frameworks or models

#### B. Tool-Based Backups
- User-provided scripts or external programs
- Alternative tools for the same purpose (e.g., multiple PDF converters)
- Fallback toolchains or processing pipelines

### Section 7.3: Sequential Exhaustion
Backups MUST be attempted sequentially (backup[1], then backup[2]) before escalation.

### Section 7.4: Thoroughness Enforcement
LLMs MUST exhaust all methods (primary + all backups + max retries) before escalating.

**Rationale:** Prevents "lazy" behaviour where LLM gives up prematurely.

---

## Article VIII: Error Propagation

### Section 8.1: Awareness of Prior Failures
Downstream steps MUST read `progress_[descriptor].json` before executing to check for prior failures.

### Section 8.2: Propagation Strategies
Three strategies are permitted:

1. **halt_on_critical:** Stop immediately on critical failure
2. **continue_and_log:** Proceed with warning on failure
3. **collaborative_review:** Pause for human decision

### Section 8.3: Dependency Tracking
Steps that depend on outputs from prior steps MUST:
- Explicitly declare dependencies
- Check prior step success status
- Handle propagated errors appropriately

### Section 8.4: Failure Threshold
If consecutive failures reach `error_propagation.failure_threshold`, escalation MUST occur regardless of individual step criticality.

**Rationale:** Persistent failure patterns indicate systemic issues requiring human review.

---

## Article IX: Execution Mode Discipline

### Section 9.1: Three-Mode System
The system supports three execution modes:

1. **Silent Mode:** Fully autonomous
2. **Collaborative Mode:** Human-in-loop
3. **Dynamic Mode (Default):** Intelligent escalation

### Section 9.2: Per-Step Mode Evaluation
Mode MUST be evaluated **per step**, not per task or goal.

### Section 9.3: Dynamic Mode as Default
**Dynamic mode is the recommended default** because it:
- Balances autonomy with safety
- Escalates only when genuinely needed
- Learns failure patterns and adapts

### Section 9.4: Mode Escalation Triggers
Dynamic mode MUST escalate to Collaborative when:
- 3+ consecutive failures detected
- Backup depletion pattern observed
- Confidence degradation detected
- Critical failure threshold breached
- Critical step fails with all methods exhausted

---

## Article X: Comprehensive Logging

### Section 10.1: Logging Requirements
ALL execution activity MUST be recorded in `progress_[descriptor].json` with entries for:
- task_id and step_id
- status (started, completed, retried, failed)
- retry_count and backup_attempts
- method_used (primary, backup[1], backup[2])
- timestamp
- mode (silent, collaborative, dynamic)
- error_propagation_decisions
- constraint_status

### Section 10.2: Accountability Through Logging
Logging serves as:
- **Audit trail:** What was attempted, when, and why
- **Learning mechanism:** Pattern detection for future runs
- **Debugging aid:** Trace failures to specific methods
- **Progress tracking:** Where execution stands

### Section 10.3: Immutability
Once written, log entries MUST NOT be modified. Append-only logging ensures integrity.

### Section 10.4: Constitutional Violation Tracking
The progress log MUST include a `constitutional_compliance` section tracking:
- violations_detected (array of violation records)
- articles_violated (which constitutional articles)
- violation_severity (warning, critical)
- corrective_actions_taken
- compliance_score (0-100)

**Example Structure:**
```json
"constitutional_compliance": {
  "violations_detected": [
    {
      "article": "VII",
      "section": "7.1",
      "description": "Backup method was simple retry, not alternative reasoning",
      "step_id": "2.3",
      "severity": "warning",
      "timestamp": "2025-11-02T14:23:45Z"
    }
  ],
  "compliance_score": 92,
  "violations_by_severity": {
    "critical": 0,
    "warning": 2
  }
}
```

---

## Article XI: Quality Standards

### Section 11.1: Internal Consistency
All elements within and across files MUST align logically and structurally.

### Section 11.2: Goal Alignment
Every task and step MUST demonstrably serve the goal.

### Section 11.3: Syntactic Validity
- Markdown MUST render correctly
- TOML MUST parse without errors
- JSON logging MUST be valid

### Section 11.4: Human Readability
Despite being designed for LLMs, Specs MUST remain human-readable:
- Use clear, plain language
- Avoid excessive jargon
- Structure information hierarchically
- Provide examples where helpful

---

## Article XII: Anti-Patterns Prohibition

The following anti-patterns are PROHIBITED:

### Section 12.1: Goal Conflation
NO Spec may define multiple goals.

### Section 12.2: Task-Step Confusion
Tasks and steps MUST NOT be conflated.

### Section 12.3: Backup-as-Retry
Backups MUST NOT be simple retries.

### Section 12.4: Vague Expected Outputs
Expected outputs MUST be specific and measurable.

### Section 12.5: Over-Criticality
NO Spec may mark all steps as critical.

### Section 12.6: Under-Criticality
NO Spec may mark zero steps as critical (unless single-step task).

### Section 12.7: Missing Bridging
Markdown and TOML MUST cross-reference each other.

### Section 12.8: Insufficient Logging
Logging MUST capture method_used, backups, errors, and decisions.

### Section 12.9: Ignoring Error Propagation
Steps MUST read progress.json before executing.

### Section 12.10: Generic Descriptions
Template placeholders MUST be replaced with specific content.

---

## Article XIII: Amendment Process

### Section 13.1: Constitution Stability
This Constitution is designed to be **stable and long-lived**. Changes should be rare and carefully considered.

### Section 13.2: Amendment Requirements
Modifications to this Constitution require:
1. Explicit documentation of rationale for change
2. Review and approval by system maintainers
3. Backwards compatibility assessment
4. Version increment and changelog entry

### Section 13.3: Design Learning
Amendments should reflect **learnings from execution**, not convenience:
- Patterns that repeatedly improve Spec quality
- Failure modes that require structural prevention
- LLM behaviour insights that warrant codification

---

## Article XIV: Complete Systems Require Deployable Artifacts

### Section 14.1: Definition of "Complete System"
When a goal contains the keywords **"build"**, **"create"**, **"develop"**, **"system"**, **"application"**, or **"app"**, the Spec MUST produce a **runnable, deployable, usable system** — not just backend logic.

**Complete system means:**
- Can be launched/started by target users
- Has appropriate user interface for intended audience
- Configured for production use (or configuration wizard provided)
- Includes deployment artifacts (executables, installers, Docker images, etc.)
- Documented for end users (not just developers)

### Section 14.2: Mandatory Sections
Specs for build/create/system goals MUST include:

#### In spec_[descriptor].md:
1. **Software Stack & Architecture** section defining:
   - Deployment type (web app, desktop app, CLI, mobile, API, library)
   - Technology stack (language, framework, database, UI library, packaging method)
   - User interface requirements (if user-facing)
   - Deployment requirements (target platform, installation method, startup process)

2. **Definition of Complete** section specifying:
   - Functional Completeness criteria
   - Deployment Completeness criteria
   - User Acceptance criteria (if user-facing)
   - Production Readiness criteria (if applicable)

#### In parameters_[descriptor].toml:
1. **[software_stack]** section with populated fields
2. **[user_interface]** section (required = true if user-facing)
3. **[deployment]** section with target platform and installation method
4. **[completion_criteria]** section with testable acceptance criteria

### Section 14.3: User-Facing Systems
If goal says **"for [users]"** (e.g., "for volunteers", "for doctors", "for customers"):
- `user_interface.required` MUST be true
- `interface_type` MUST be appropriate for skill_level
- User Acceptance section MUST exist in Definition of Complete
- User stories SHOULD be included for design context

**Rationale:** "For volunteers" implies volunteers will use the system, requiring a volunteer-appropriate interface, not developer-only tools.

### Section 14.4: Production Readiness Requirement
If the goal implies production use or mentions external services (APIs, databases, payment processors):
- `completion_criteria.production_ready` MUST be true
- Real API connections MUST be implemented (not just test mode simulators)
- Configuration MUST be user-accessible (wizard, settings file, or environment variables)
- Error recovery for external dependencies MUST be implemented

**Anti-Pattern:** Building a payment processing system where the payment API is hardcoded to test mode only.

### Section 14.5: Validation Enforcement
This Article is enforced at THREE checkpoints:

#### Checkpoint 1: Spec Commander (Step 5.1a)
Before generating spec files, Commander MUST validate:
- Software stack sections exist and are populated
- Definition of Complete is specific and testable
- User interface requirements match goal ("for [users]" → UI required)

**Failure Action:** HALT spec generation, request clarification

#### Checkpoint 2: Exe Pre-Flight (Section 1.1a)
Before execution begins, exe controller MUST validate:
- [software_stack] section exists in TOML with non-empty required fields
- [completion_criteria] section exists with defined criteria
- If UI required, UI fields are populated

**Failure Action:** HALT execution, log validation error

#### Checkpoint 3: Exe Post-Execution (Section 6.4)
After tasks complete, BEFORE marking goal ACHIEVED:
- Verify runnable system exists (executable, installer, or deployed service)
- Verify user interface exists (if required)
- Verify production APIs configured (if required)
- Verify user documentation exists

**Failure Action:** Mark goal as PARTIAL (not ACHIEVED), log specific gaps

### Section 14.6: Goal Achievement Status
Three statuses are possible:

1. **ACHIEVED:** All completion criteria met, deployment verification passed
   - Runnable system exists
   - User interface implemented (if required)
   - Production ready (if required)
   - User documentation present

2. **PARTIAL:** Core logic works but deployment incomplete
   - Backend functions exist but no executable
   - No user interface for user-facing system
   - APIs in test mode only
   - Missing user documentation

3. **NOT ACHIEVED:** Core logic broken or critical gaps
   - Primary functionality doesn't work
   - Critical steps failed
   - Goal fundamentally not met

**Critical Rule:** Backend-only solutions for user-facing goals MUST be marked PARTIAL, never ACHIEVED.

### Section 14.7: Rationale
This Article exists because:

**Problem Identified:** Specs were satisfied by building backend modules without user interfaces, deployment packages, or production configurations — technically meeting step requirements but failing the actual goal.

**Example Failure:** 
- Goal: "Build a charity shop POS system for volunteers"
- What was delivered: Python scripts requiring command-line and technical knowledge
- What was missing: GUI, executable, volunteer usability, production Square API

**Solution:** Enforce that "build a system" means "build a complete, deployable, usable system," not "write some code."

**Constitutional Principle:** The goal is the North Star (Article I). Satisfying technical steps while missing the goal's intent violates the fundamental principle. This Article makes that enforcement explicit for build/create goals.

---

## Article XI: Method Execution Order and Backup Justification

### Section 11.1: Primary Method Primacy
The primary method MUST be attempted before any backup method is considered.

**Rationale:** Primary methods represent the intended, optimal solution. Backups exist only for contingency, not convenience.

### Section 11.2: Backup Progression
Backup methods MUST be attempted in sequence (backup[1], then backup[2]) and ONLY after:
1. Primary method has been attempted
2. Primary method has demonstrably failed
3. Failure has been logged with specific reason

### Section 11.3: Backup Justification Requirement
Every use of a backup method MUST be accompanied by:
- Explicit log entry stating why primary failed
- Description of what was attempted
- Reason the backup was deemed necessary

**Format in progress.json:**
```json
{
  "step_id": "5.1",
  "method_used": "backup_2",
  "primary_failure_reason": "Tkinter GUI development blocked by [specific issue]",
  "backup_1_failure_reason": "Flask web interface blocked by [specific issue]",
  "backup_justification": "CLI provides basic functionality to meet deadline"
}
```

### Section 11.4: Prohibited Backup Patterns
The following are CONSTITUTIONAL VIOLATIONS:
- Skipping primary method due to perceived complexity
- Using backup method for speed or convenience
- Selecting backup method without attempting primary
- Failing to log backup justification

### Section 11.5: Enforcement
**Pre-execution:** Executor MUST declare intention to attempt primary method

**During execution:** If switching to backup, MUST log:
1. What was attempted (code, approach, tools)
2. Specific failure encountered
3. Why backup is more viable

**Post-execution:** Verification MUST check `method_used` matches progression:
- If `method_used = "backup_1"` → verify primary failure logged
- If `method_used = "backup_2"` → verify both primary and backup_1 failures logged

### Section 11.6: Dynamic Mode Escalation
If executor encounters difficulty with primary method:
1. Log the challenge
2. Escalate to collaborative mode
3. Discuss backup options with user
4. Document decision

**Critical Rule:** DO NOT silently switch to backup method without escalation.

### Section 11.7: Rationale
This Article exists because:

**Problem Identified:** Executors were selecting easier backup methods (e.g., CLI) without attempting primary methods (e.g., GUI), resulting in deliverables that technically satisfied steps but failed user requirements.

**Example Violation:**
- Step: "Implement user interface"
- Primary: Tkinter GUI
- Backup 1: Flask web interface
- Backup 2: CLI interface
- What happened: CLI implemented without attempting GUI or web interface
- Why wrong: User stories required "point-and-click" operation (CLI cannot satisfy)

**Solution:** Enforce method execution order and require documented justification for all backup usage.

**Constitutional Principle:** Backups are contingency plans, not convenience shortcuts. Primary methods represent best practice; using backups without attempting primary undermines spec quality and goal achievement.

---

## Article XV: The Slow-Code Principle (Lia Integration)

### Section 15.1: Understanding Over Speed
Specs MUST prioritise human understanding over rapid execution when appropriate.

**Rationale:** While automation and speed are valuable, they must not come at the cost of human comprehension. The "Troubleshooting Cliff" phenomenon demonstrates that AI tools achieve near-perfect creation success but fail catastrophically during debugging when developers don't understand the code.

**Requirement:** When education or understanding is a goal component, specs MUST include mechanisms for knowledge transfer, not just task completion.

### Section 15.2: Education Mode
When `education_mode = true` in execution configuration:
- Approval gates MUST increase at critical decision points
- Rationale explanations are MANDATORY for each approach selected
- Alternative approaches MUST be presented for learning comparison
- Pros/cons analysis MUST be provided before human selection
- Learning checkpoints MUST be logged to notepad

**Behaviour Pattern:**
```
1. PAUSE before critical step
2. EXPLAIN current situation and objective
3. PRESENT alternative approaches with trade-offs
4. RECOMMEND approach with detailed rationale
5. REQUEST human review and decision
6. EXECUTE approved approach
7. EXPLAIN outcome and lessons learned
```

### Section 15.3: Knowledge Capture Requirement
Every spec execution MUST generate both:
- Machine-readable progress log (`progress_[descriptor].json`)
- Human-readable knowledge capture (`notepad_[descriptor].md`)

**Notepad Requirements:**
The notepad MUST capture across execution:
- Key insights and discoveries
- Technical decisions with rationale
- Ideas for future enhancement
- Cross-system connections and patterns
- Observations from both AI executor and human user

**Update Frequency:** Configurable per spec (per_step, per_task, or end_only), default is per_task.

### Section 15.4: Troubleshooting Ecosystem Parity
Problem diagnosis and resolution MUST be given equal weight to creation workflows.

**Requirements:**
- System MUST provide dedicated troubleshooting TOOLSPECs equivalent to creation TOOLSPECs
- Troubleshooting workflows MUST be systematic, not ad-hoc
- Three troubleshooting modes MUST be supported:
  - **Diagnostic:** Fix broken functionality (Troubleshoot TOOLSPEC)
  - **Archaeological:** Understand mysterious code (WTF TOOLSPEC)
  - **Forensic:** Investigate critical failures (Forensic TOOLSPEC)

**Rationale:** The "Troubleshooting Cliff" is a real failure mode where AI excels at creation but fails at debugging. Constitutional parity ensures troubleshooting receives systematic support.

### Section 15.5: Pre-built Workflow Library
The system MUST maintain a curated library of reusable TOOLSPECs for common workflows, organised by category:
- Development (feature implementation, testing, specification)
- Quality (review, architecture, security, optimisation)
- Problem Solving (troubleshoot, archaeology, forensics)
- Research & Learning (research, learning, paper analysis)
- Knowledge (documentation, standards)
- Strategy (innovation, integration)

**Purpose:** Reduce time-to-value for common tasks while maintaining flexibility for novel goals.

### Section 15.6: MCP Protocol Integration
The framework MUST expose capabilities via Model Context Protocol for external integration:
- **Resources:** Constitution, TOOLSPECs, templates accessible as MCP resources
- **Tools:** Spec generation, validation, TOOLSPEC recommendation exposed as MCP tools
- **Prompts:** Workflow starters available as MCP prompts

**Rationale:** Enable use of SPEC Engine within other AI tools and workflows, not just standalone.

### Section 15.7: Enforcement
This Article is enforced through:

**Template-Level:**
- Notepad template MUST exist in `_templates/notepad_template.md`
- All spec templates MUST include notepad section
- Parameters template MUST include `[knowledge_capture]` configuration
- Exe template MUST include notepad update logic (Section 2.7)

**Execution-Level:**
- Executor MUST create notepad file at spec start
- Executor MUST update notepad per configured frequency
- Education mode checkpoints MUST log to both progress.json and notepad
- TOOLSPEC library MUST be maintained and indexed

**Documentation-Level:**
- README MUST highlight troubleshooting ecosystem as key feature
- Workflow selection guide MUST be provided
- Education mode usage MUST be documented

### Section 15.8: Rationale
This Article integrates Lia Workflow Specs' "slow-code" philosophy with SPEC Engine's structural rigour:

**Problem Identified:** Pure speed-focused AI coding creates technical debt and comprehension gaps. Developers ship fast but debug poorly because they don't understand generated code.

**Solution:** Constitutional requirement for understanding-focused features (education mode, notepad) alongside execution-focused features (dynamic mode, validation).

**Core Principle:** "Understanding over speed, when understanding matters." Not all tasks require learning, but when they do, the system must support it constitutionally, not as an afterthought.

---

## Enforcement

### Three-Layer Enforcement System

The Constitution is enforced through three integrated layers:

#### Layer 1: Pre-Flight Enforcement (Commander & Validation)
**When:** Before spec generation and before first execution  
**Who:** `Spec_Commander.md` Step 5 and `exe_[descriptor].md` Section 1.1-1.10  
**Action:** Validate constitutional compliance, halt on violations

**Checks:**
- Article I: Single goal validation
- Article II: Hierarchical structure and quantitative constraints
- Article III: Dual-file synchronisation and bridging
- Article V: Explicitness of outputs and backups
- Article VI: Critical flag balance (40-60%)
- Article XI: Backup method structure and scope coherence
- Article XII: Anti-pattern detection

#### Layer 2: Runtime Enforcement (During Execution)
**When:** Before each task execution  
**Who:** `exe_[descriptor].md` Section 2.0 (Constitutional Compliance Check)  
**Action:** Verify ongoing compliance, log violations, escalate if critical

**Checks:**
- Article IV: Error propagation enabled and functioning
- Article VII: Backup methods exhausted before escalation
- Article VIII: Prior step outcomes read from progress.json
- Article IX: Mode escalation triggers functioning correctly
- Article X: Comprehensive logging active
- Article XI: Method execution order and backup justification

**Enforcement Mechanism:**
- Non-critical violations: Log warning, continue execution
- Critical violations: Halt task, escalate to collaborative mode
- Pattern violations: Track in progress.json for post-execution review

#### Layer 3: Post-Execution Review (After Completion)
**When:** After all tasks complete or on critical halt  
**Who:** `exe_[descriptor].md` Section 6 (Post-Execution Analysis)  
**Action:** Analyse constitutional compliance patterns, generate recommendations

**Reviews:**
- Article VI: Was critical flag balance appropriate?
- Article VII: Were backups effective alternatives?
- Article VIII: Did error propagation function correctly?
- Article IX: Were mode escalations appropriate?
- Article X: Is logging complete and accurate?
- Article XI: Were primary methods attempted before backups?

**Outputs:**
- Constitutional compliance score
- Violation summary
- Recommendations for spec improvement
- Patterns for future spec design

### For Spec Authors
When creating a Spec, adherence to this Constitution is MANDATORY. The Commander (`Spec_Commander.md`) and validation process (`exe_[descriptor].md` Section 1.1-1.10) enforce these principles.

**Your Responsibility:**
- Read this Constitution before creating specs
- Ensure goal is singular and clear
- Balance critical flags appropriately
- Define explicit expected outputs
- Provide genuine backup alternatives

### For LLM Executors
When executing a Spec, this Constitution governs behaviour. Validation failures that violate Constitutional principles MUST halt execution.

**Your Responsibility:**
- Respect validation gates - do not bypass
- Exhaust backup methods before escalating
- Read progress.json before each step
- Log comprehensively and accurately
- Escalate appropriately based on Article IX

### For System Designers
When extending the SPECS system, new features MUST align with these principles. Features that violate the Constitution are prohibited.

**Your Responsibility:**
- Ensure new features respect the hierarchy (Article II)
- Maintain dual-file architecture (Article III)
- Enhance, don't dilute, constitutional enforcement
- Document constitutional implications of changes

---

## Conclusion

This Constitution establishes the **immutable foundation** for the SPECS system. It ensures:

- **Consistency:** All Specs follow the same principles
- **Quality:** Structural enforcement prevents common failures
- **Reliability:** LLMs behave predictably within these constraints
- **Maintainability:** Clear rules enable long-term system evolution

**Core Principle:** Structure enables freedom. By constraining LLM behaviour through explicit rules, we enable more reliable and powerful agentic workflows.

---

**End of Constitution**

*This document should be read before creating any Spec. It is referenced by `Spec_Commander.md` and enforced by `exe_[descriptor].md` validation routines.*

**Maintenance:** Amendments to this Constitution MUST be documented in version history below.

**Version History:**
- v1.4 (2026-01-02): Added Article XV (The Slow-Code Principle) integrating Lia Workflow Specs philosophy - education mode, knowledge capture, troubleshooting ecosystem parity, workflow library, MCP integration
- v1.3 (2025-11-03): Amended Article II to add SPECLet abstraction layer for complex multi-phase goals, enabling parallel execution with dependency management
- v1.2 (2025-11-02): Added Article XI (Method Execution Order and Backup Justification) to prevent premature backup usage
- v1.1 (2025-11-02): Added Article XIV (Complete Systems Require Deployable Artifacts) based on Charity Shop POS testing learnings
- v1.0 (2025-11-02): Initial Constitution based on Design Philosophy v1.0

