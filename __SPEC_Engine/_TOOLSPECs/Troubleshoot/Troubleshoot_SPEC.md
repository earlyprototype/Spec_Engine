# Troubleshoot SPEC

**Version:** 2.0  
**Last Updated:** 2025-11-07  
**Purpose:** Systematically diagnose and resolve issues in a recently completed SPEC project with fresh LLM context

---

## Goal

Systematically diagnose and resolve post-development issues in a completed SPEC project, producing a fully functional deliverable that meets all Definition of Complete criteria.

---

## Software Stack & Architecture

**Not Applicable** - This is a troubleshooting/remediation task, not a build goal.

---

## Definition of Complete

What must exist and be verified:
- [ ] **Primary deliverables:** 
  - All issues identified and categorised by severity and type
  - Fixes implemented for all critical and high-priority issues
  - Troubleshooting report documenting: issues found, root causes, fixes applied, verification results
  - Original project deliverables now meet Definition of Complete criteria from original SPEC
- [ ] **Quality standards met:** 
  - All critical issues resolved (blocking issues that prevent goal achievement)
  - High-priority issues resolved or documented with workarounds
  - Original SPEC's primary deliverable exists and is functional
  - Original SPEC's quality standards now satisfied
  - Verification methods from original SPEC now pass
- [ ] **Verification method:** 
  - Run original SPEC's verification methods - all must pass
  - Execute functional tests on fixed deliverables - all critical paths work
  - Review troubleshooting report - all critical issues have status "RESOLVED"
  - Human CoDesigner confirms project now meets original intent

---

## Definitions

- **goal**: Diagnose and fix issues in completed SPEC project to achieve original goal
- **task[n]**: Discrete troubleshooting objectives (gather context, diagnose, fix, verify)
- **step[m]**: Concrete diagnostic or remediation actions within each task
- **backup[p]**: Alternative troubleshooting or fixing method when primary approach fails
- **critical_flag**: Boolean indicating whether step failure blocks troubleshooting goal
- **mode**: Execution mode per step - `collaborative` (initial setup), then `silent` (autonomous troubleshooting)
- **progress.json**: Structured log tracking troubleshooting execution and outcomes
- **project_folder**: Target project folder path (ONLY required user input)
- **original_spec**: The SPEC that was executed to create the project being troubleshot

---

## State Tracking Protocol

**MANDATORY for LLM Executor:**

Before ANY action during troubleshooting, maintain explicit state awareness.

### Internal State Variables

The LLM executor must maintain these variables throughout execution:

```json
{
  "current_task": 3,
  "current_step": 2,
  "task_name": "Implement Fixes for Identified Issues",
  "step_name": "Fix critical issues",
  "current_issue_id": "C-3",
  "mode": "silent",
  "next_action": "Apply fix and document",
  "backup_created": true,
  "documented": false
}
```

### State Checkpoint Format

**BEFORE each action, internally verify:**

```
[STATE CHECKPOINT - Internal]
Current Task: 3.2
Task Name: Fix CRITICAL issues
Issue ID: C-3 (SDK Mismatch)
Action: Installing @insforge/sdk package
Pre-checks:
  □ Backup created: YES
  □ Fix documented: NO (will do after)
  □ Previous fix verified: YES
Next Action: Document in fixes_applied.log
```

### State Transitions

Valid transitions between tasks:

| From | To | Condition |
|------|-----|-----------|
| Task 1 | Task 2 | All context gathered |
| Task 2 | Task 3 | All issues categorised by severity |
| Task 3 | Task 4 | All CRITICAL issues fixed |
| Task 4 | Task 3 | New issue discovered (via New Issue Protocol) |
| Task 3 | Task 2 | Root cause unclear, needs more diagnosis |
| Any | Collaborative | Escalation criteria met |

**INVALID Transition:** Jumping from Task 4 (Verification) directly to applying fixes without documenting new issue in registry.

### progress_Troubleshoot.json Enhancement

Add mandatory `current_state` object:

```json
{
  "troubleshooting_session": {...},
  "current_state": {
    "task": 3,
    "step": 2,
    "issue_in_progress": "C-3",
    "mode": "silent",
    "last_action": "Applied fix to lib/supabase.ts",
    "awaiting": "user_verification",
    "backup_location": "troubleshooting_2025-11-07/backups/",
    "fixes_count": 2,
    "issues_remaining": 1
  },
  "tasks_completed": [...]
}
```

**Implementation Notes:**
- LLM should update `current_state` after EVERY action
- State must be saved before any file modification
- State checkpoints are internal (not shown to user) unless in collaborative mode

---

## Components

Troubleshooting requires access to:
- **Original SPEC files:** spec_[descriptor].md, parameters_[descriptor].toml, exe_[descriptor].md
- **Execution logs:** progress_[descriptor].json from original build
- **Project deliverables:** Code files, executables, documentation, outputs
- **Error logs:** Any error logs, crash reports, validation failures
- **Definition of Complete:** Original completion criteria to verify against
- **Test artefacts:** Test results, validation reports, user feedback

**Deliverables Generated:**
- **Troubleshooting_Report_[PROJECT_CODE].md:** Comprehensive troubleshooting documentation (issues, fixes, verification)
- **fixes_applied.log:** Structured log of all changes made during troubleshooting
- **progress_Troubleshoot.json:** Troubleshooting execution log
- **Updated project deliverables:** Fixed/corrected versions of original outputs

**Machine-Readable Components:**  
See `[components]` section in parameters_Troubleshoot.toml

---

## Constraints

- Troubleshooting must not introduce new issues or regressions
- All fixes must be documented with clear rationale
- Original project structure and architecture should be preserved unless fundamentally flawed
- Changes must be traceable (before/after documentation)
- Critical issues must be resolved; non-critical issues may be documented as known limitations
- Must operate within fresh LLM context (context-efficient approach)

**Machine-Readable Constraints:**  
See `[constraints]` section in parameters_Troubleshoot.toml:
- `preserve_architecture = true` (don't rebuild from scratch unless necessary)
- `document_all_changes = true` (every fix must be logged)
- `critical_issues_required = true` (critical issues must be resolved for completion)

---

## User Stories

- As a **Human CoDesigner**, I want systematic issue diagnosis so I don't waste time on trial-and-error debugging
- As a **project stakeholder**, I want issues fixed efficiently so the project delivers value quickly
- As a **future maintainer**, I want troubleshooting documented so I understand what went wrong and how it was fixed
- As a **SPEC Engine user**, I want fresh-context troubleshooting so I can fix projects even when original context is exhausted

---

## Troubleshooting Framework

This SPEC operates in **post-development** mode, designed to:
1. Work with **fresh LLM context** (doesn't require original build conversation)
2. **Read original SPEC** to understand intent
3. **Assess current state** against original Definition of Complete
4. **Diagnose systematically** using error logs and testing
5. **Fix efficiently** with minimal rework
6. **Verify thoroughly** against original criteria

### Issue Severity Classification

Issues are classified by impact:

- **CRITICAL:** Blocks original goal achievement, prevents core functionality
- **HIGH:** Major functionality impaired, significant quality degradation
- **MEDIUM:** Minor functionality issues, quality below standards but usable
- **LOW:** Cosmetic issues, edge cases, nice-to-haves

### Troubleshooting Workflow

```
Initialize Context
      ↓
Gather Project Metadata
      ↓
Read Original SPEC & Logs
      ↓
Assess Current State vs Definition of Complete
      ↓
Identify All Issues (error logs, testing, validation)
      ↓
Categorise by Severity
      ↓
Fix Critical Issues (must resolve)
      ↓
Fix High-Priority Issues (should resolve)
      ↓
Verify Fixes (re-run original verification)
      ↓
Document & Report
```

---

## New Issue Discovery Protocol

### Handling Issues Discovered During Execution

**CRITICAL RULE:** Issues discovered during Tasks 3 (Fixing) or 4 (Verification) MUST NOT be fixed reactively. Follow this protocol.

#### When New Issues Are Discovered

**Triggers:**
- User reports error during testing
- Error appears in logs during verification
- Fix introduces regression
- New symptom observed during testing

#### Mandatory Protocol

**Step 1: PAUSE Current Task**

```
[PAUSE TRIGGERED]
Current Task: 4 (Verification)
Current Step: 2 (Test critical functionality)
Trigger: User reported 404 error on registration
Action: PAUSE verification workflow
```

**Do NOT:**
- ❌ Immediately diagnose the error
- ❌ Install packages or modify code
- ❌ Continue with reactive debugging

**Step 2: Document in ISSUE_REGISTRY.md**

Before ANY diagnosis or fixing:

```markdown
#### Issue C-X: [Short Title] ⏳ **DISCOVERED**
- **Severity:** [TBD - requires classification]
- **Component:** [Affected file/system]
- **Description:** [Observable problem]
- **Root Cause:** [UNKNOWN - requires diagnosis]
- **Discovered During:** Task X, Step Y
- **Status:** ⏳ **DISCOVERED**
```

**Step 3: Classify Severity**

- **CRITICAL:** Blocks goal achievement or core functionality
- **HIGH:** Major functionality impaired
- **MEDIUM:** Minor functionality issues
- **LOW:** Cosmetic issues

**Step 4: Determine Workflow Path**

| Scenario | Required Action |
|----------|-----------------|
| Root cause clear + CRITICAL | Proceed to Task 3 (Fix) |
| Root cause unclear | Return to Task 2 (Diagnosis) |
| NON-CRITICAL | Document for later |
| Requires user input | Escalate to collaborative mode |

**Step 5: Execute Appropriate Workflow**

**Path A: CRITICAL + Clear Root Cause**
1. Return to Task 3, Step 2 (Fix CRITICAL issues)
2. Create backup before modifying files
3. Apply fix using standard workflow
4. Document in fixes_applied.log
5. Test fix immediately
6. Return to Task 4 to resume verification

**Path B: Root Cause Unclear**
1. Return to Task 2 (Diagnose)
2. Identify root cause
3. Proceed to Task 3 to fix
4. Return to Task 4 to resume verification

**Path C: Non-Critical**
1. Document in known_issues.md
2. Continue current task

#### Verification Interruption Handling

If new issue discovered during Task 4:
1. Mark current verification as INCOMPLETE
2. Follow New Issue Protocol
3. Fix the issue
4. Restart verification from beginning

---

## Task [0]: Initialize Troubleshooting Context

**TOML Reference:** `tasks[id=0]` in parameters_Troubleshoot.toml  
**Purpose:** Gather project location and establish context for troubleshooting

- **Step [0]:** Receive project folder location (ONLY USER INPUT REQUIRED)
  - **Primary method:** Prompt for project folder path containing SPEC and deliverables
  - **Expected output:** Absolute path to project folder
  - **Critical:** true
  - **Mode:** collaborative (ONE TIME ONLY - for folder path input)

- **Step [1]:** Validate project folder structure
  - **Primary method:** Check for presence of: SPEC files (spec_*.md, parameters_*.toml), progress_*.json, deliverable files/folders
  - **Backup [1]:** If standard structure not found, scan for SPEC files recursively in subdirectories
  - **Expected output:** List of key project files found with paths
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify project code/descriptor
  - **Primary method:** Extract descriptor from SPEC filenames (e.g., "podcast" from spec_podcast.md)
  - **Backup [1]:** If multiple SPECs found, prompt user to select which SPEC is being troubleshot
  - **Expected output:** Project descriptor string (e.g., "podcast", "pos_system", "analysis")
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Initialize troubleshooting progress log
  - **Primary method:** Create progress_Troubleshoot.json with metadata: timestamp, project_folder, project_descriptor, troubleshooting_session_id
  - **Expected output:** progress_Troubleshoot.json created with initialized structure
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Create troubleshooting workspace
  - **Primary method:** Create troubleshooting folder within project: [project_folder]/troubleshooting_[timestamp]/
  - **Backup [1]:** If folder creation fails, use project root directly
  - **Expected output:** Workspace path for troubleshooting artefacts
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Project folder validated, descriptor identified, progress log initialized
- **Logging:** Record initialization in progress_Troubleshoot.json

---

## Task [1]: Gather Project Context and Metadata

**TOML Reference:** `tasks[id=1]` in parameters_Troubleshoot.toml  
**Purpose:** Collect comprehensive information about the project, original SPEC, and current state

- **Step [1]:** Read original SPEC files
  - **Primary method:** Read spec_[descriptor].md to extract: Goal, Definition of Complete, Tasks, Software Stack (if build goal)
  - **Backup [1]:** If spec.md corrupt or missing, attempt to reconstruct from parameters.toml
  - **Expected output:** Original goal text, Definition of Complete criteria list, task/step count
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Read original execution log
  - **Primary method:** Parse progress_[descriptor].json to extract: execution status, completion status, step outcomes, errors logged
  - **Backup [1]:** If progress.json missing or incomplete, scan for any log files in project
  - **Expected output:** Execution summary: total steps, success rate, errors encountered, completion status
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Catalogue project deliverables
  - **Primary method:** Scan project folder for deliverables (code files, executables, reports, documentation, test results)
  - **Expected output:** Complete inventory of deliverables with file paths and sizes
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Locate and read error logs
  - **Primary method:** Search for error log files (error_logs/, *.log, *_errors.txt), read and parse contents
  - **Backup [1]:** If no dedicated error logs, extract error messages from progress.json
  - **Expected output:** Consolidated error inventory with messages, timestamps, contexts
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Read troubleshooting trigger context (if provided)
  - **Primary method:** Check for troubleshooting_context.txt or similar file documenting why troubleshooting was initiated
  - **Backup [1]:** If no context file, check latest chat logs or project notes
  - **Expected output:** List of issues that triggered troubleshooting session (user-reported problems)
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Extract original Definition of Complete criteria
  - **Primary method:** Parse Definition of Complete section from spec.md into discrete checkable criteria
  - **Expected output:** Numbered list of completion criteria with verification methods
  - **Critical:** true
  - **Mode:** silent

- **Verification:** Original SPEC understood, execution history known, deliverables inventoried, errors catalogued
- **Logging:** Record all gathered context in progress_Troubleshoot.json

---

## Task [2]: Diagnose Issues Systematically

**TOML Reference:** `tasks[id=2]` in parameters_Troubleshoot.toml  
**Purpose:** Identify all issues preventing goal achievement, categorise by severity and root cause

- **Step [1]:** Assess against Definition of Complete
  - **Primary method:** For each criterion in Definition of Complete, check: Does deliverable exist? Does it meet quality standards? Does verification method pass?
  - **Expected output:** Completion criteria assessment table with status: MET/NOT_MET/PARTIAL for each criterion
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify missing deliverables
  - **Primary method:** Compare Definition of Complete against deliverable inventory, note what's missing
  - **Expected output:** List of missing deliverables with severity (CRITICAL if primary deliverable missing)
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Test existing deliverables
  - **Primary method:** Based on deliverable type, execute functional tests:
    - For executables: attempt to run/launch, test core functionality
    - For code: check for syntax errors, import errors, runtime errors
    - For reports: validate structure, completeness, formatting
    - For systems: test critical user workflows
  - **Backup [1]:** If automated testing not possible, perform manual inspection against requirements
  - **Expected output:** Test results table with pass/fail status and error details for each deliverable tested
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse error logs and failure patterns
  - **Primary method:** Categorise errors from logs by type: syntax errors, import errors, logic errors, missing dependencies, configuration issues
  - **Backup [1]:** Use error message patterns to infer root causes if logs are incomplete
  - **Expected output:** Error analysis table with error types, frequencies, affected components
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify quality standard violations
  - **Primary method:** Review deliverables against quality standards from Definition of Complete (e.g., code standards, documentation completeness, UI requirements)
  - **Expected output:** Quality violation list with specific issues and standard violated
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Perform root cause analysis
  - **Primary method:** For each identified issue, trace to root cause: SPEC design flaw, implementation error, missing dependency, environmental issue, requirement misunderstanding
  - **Backup [1]:** If root cause unclear, categorise as "unclear - requires investigation" and flag for collaborative review
  - **Expected output:** Root cause mapping for all issues with confidence level (HIGH/MEDIUM/LOW)
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Categorise issues by severity
  - **Primary method:** Classify each issue using severity framework:
    - CRITICAL: Blocks goal achievement or core functionality
    - HIGH: Major functionality impaired, significant quality degradation
    - MEDIUM: Minor functionality issues, quality below standards
    - LOW: Cosmetic issues, edge cases
  - **Expected output:** Issue registry with all issues categorised by severity, including root causes and affected components
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Prioritise fix order
  - **Primary method:** Order issues by: CRITICAL first (all), then HIGH (all), then MEDIUM (time permitting), then LOW (document only)
  - **Expected output:** Prioritised fix list with estimated complexity per issue
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All issues identified, categorised, prioritised; root causes documented
- **Logging:** Record complete issue registry in progress_Troubleshoot.json

### Task 2 Completion Gate

Before proceeding to Task 3, verify:

```
TASK 2 COMPLETION GATE
□ All issues identified and documented
□ Issue registry complete with severities
□ Root causes documented (or marked as "unclear")
□ Prioritised fix list created
□ Total issues categorised:
  - CRITICAL: [count]
  - HIGH: [count]
  - MEDIUM: [count]
  - LOW: [count]
□ Ready to proceed to Task 3 (Fix issues): YES/NO

IF NO: Complete pending items before transition
IF YES: Document transition in progress_Troubleshoot.json
```

---

## Task [3]: Implement Fixes for Identified Issues

**TOML Reference:** `tasks[id=3]` in parameters_Troubleshoot.toml  
**Purpose:** Systematically resolve issues starting with highest priority, applying fixes with verification

- **Step [1]:** Create backup of current state (MANDATORY BEFORE ANY MODIFICATIONS)
  - **Primary method:** Copy all deliverables to backup folder: [project_folder]/troubleshooting_[timestamp]/backups/
  - **Backup [1]:** If full copy fails, create list of file checksums for rollback capability
  - **Expected output:** Backup folder path or checksum manifest file
  - **Critical:** true
  - **Mode:** silent
  
  **⚠️ MANDATORY CHECKPOINT:**
  
  Before modifying ANY file in Task 3:
  1. Check if file backup exists
  2. If not, create: `[filename].backup-[timestamp]`
  3. Document backup location in fixes_applied.log
  4. Verify backup was created successfully
  5. ONLY THEN proceed with modification
  
  **No exceptions.** If backup fails, escalate to collaborative mode.
  
  **Backup Manifest Format:**
  ```json
  {
    "backup_created": "2025-11-07T14:30:22Z",
    "files_backed_up": [
      {
        "original": "frontend/src/lib/supabase.ts",
        "backup": "troubleshooting_2025-11-07/backups/lib/supabase.ts.backup-20251107-143022",
        "checksum": "abc123...",
        "reason": "Fix C-3: SDK mismatch"
      }
    ]
  }
  ```

- **Step [2]:** Fix critical issues (blocking goal achievement)
  - **Primary method:** For each CRITICAL issue in priority order:
    1. Identify fix approach (implement missing deliverable, correct error, add dependency)
    2. Apply fix with minimal changes
    3. Document change in fixes_applied.log
    4. Test fix immediately
  - **Backup [1]:** If automated fix fails, generate detailed fix instructions for collaborative implementation
  - **Backup [2]:** If issue is architectural, flag for collaborative redesign discussion
  - **Expected output:** All CRITICAL issues resolved OR escalated with clear collaborative action required
  - **Critical:** true
  - **Mode:** silent
  
  **Per-Issue Fix Checklist (Execute for EACH issue):**
  
  ```
  ISSUE [ID]: [Title]
  
  □ Pre-Fix
    - Issue documented in ISSUE_REGISTRY.md
    - Root cause identified
    - Fix approach determined
  
  □ Backup
    - Files to modify have backups
    - Backup locations documented
  
  □ Apply Fix
    - Minimal changes only
    - Fix aligns with root cause
    - No scope creep
  
  □ Document (DURING fix, not after)
    - fixes_applied.log updated
    - Before/after code documented
    - ISSUE_REGISTRY.md status updated
  
  □ Verify
    - Fix tested immediately
    - No regressions introduced
    - Mark RESOLVED if PASS
  ```

- **Step [3]:** Fix high-priority issues (major functionality)
  - **Primary method:** For each HIGH severity issue:
    1. Apply fix using same systematic approach as Step 2
    2. Verify no regressions introduced
    3. Document changes
  - **Backup [1]:** If fix introduces new issues, rollback and document as "requires alternative approach"
  - **Expected output:** HIGH issues resolved or documented with workaround approaches
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Address medium-priority issues (quality improvements)
  - **Primary method:** Fix MEDIUM issues if time/context permits, following same systematic approach
  - **Expected output:** MEDIUM issues resolved OR documented for future iteration
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Document low-priority issues
  - **Primary method:** Create known_issues.md documenting LOW severity issues with workarounds if available
  - **Expected output:** known_issues.md file with LOW severity issue documentation
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Update project documentation
  - **Primary method:** Update README, user guides, or technical docs to reflect fixes, changes, new requirements discovered
  - **Backup [1]:** If no existing documentation, create basic usage documentation
  - **Expected output:** Updated documentation reflecting current project state
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Create fixes summary log
  - **Primary method:** Compile fixes_applied.log with structure: Issue ID, Severity, Root Cause, Fix Applied, Files Changed, Verification Status
  - **Expected output:** Comprehensive fixes_applied.log with all changes documented
  - **Critical:** true
  - **Mode:** silent

- **Verification:** All CRITICAL issues resolved, HIGH issues resolved or documented, changes logged
- **Logging:** Record all fixes and verification results in progress_Troubleshoot.json

### Task 3 Completion Gate

Before proceeding to Task 4, verify:

```
TASK 3 COMPLETION GATE
□ All CRITICAL issues resolved OR escalated
□ All HIGH issues resolved OR documented with workarounds
□ fixes_applied.log complete
□ All modifications backed up
□ Each fix tested and verified
□ No pending fixes for CRITICAL issues
□ Ready to proceed to Task 4 (Verification): YES/NO

IF NO: Complete pending fixes before transition
IF YES: Document transition in progress_Troubleshoot.json
```

---

## Task [4]: Verify Resolution and Generate Report

**TOML Reference:** `tasks[id=4]` in parameters_Troubleshoot.toml  
**Purpose:** Confirm fixes work, original Definition of Complete is now satisfied, document troubleshooting

- **Step [1]:** Re-run original verification methods
  - **Primary method:** Execute verification methods from original Definition of Complete section
  - **Backup [1]:** If automated verification not possible, perform manual verification against criteria
  - **Expected output:** Verification results table showing status (PASS/FAIL) for each Definition of Complete criterion
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Test all critical functionality
  - **Primary method:** Execute functional tests covering all critical user workflows/features from original SPEC
  - **Backup [1]:** If formal test suite doesn't exist, create and execute ad-hoc tests for critical paths
  - **Expected output:** Functional test results with pass/fail status for each critical feature
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Verify no regressions introduced
  - **Primary method:** Compare working functionality from pre-troubleshooting state, ensure nothing broke
  - **Backup [1]:** If pre-troubleshooting baseline unclear, test basic functionality end-to-end
  - **Expected output:** Regression test results confirming no new issues introduced
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Generate troubleshooting report
  - **Primary method:** Create Troubleshooting_Report_[PROJECT_CODE].md with sections:
    - Executive Summary (what was broken, what was fixed, current status)
    - Original Goal and Definition of Complete
    - Issues Found (complete registry with severity)
    - Root Cause Analysis
    - Fixes Applied (detailed with before/after)
    - Verification Results
    - Outstanding Issues (if any)
    - Recommendations for future prevention
  - **Expected output:** Complete Troubleshooting_Report_[PROJECT_CODE].md with all sections
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Update original project status
  - **Primary method:** Update progress_[descriptor].json to reflect new completion status: ACHIEVED/PARTIAL/NOT_ACHIEVED based on verification
  - **Expected output:** Updated progress_[descriptor].json with current goal_achievement_status
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Generate completion summary for Human CoDesigner
  - **Primary method:** Create concise summary (2-3 paragraphs) for CoDesigner:
    - What was fixed
    - Current project status vs Definition of Complete
    - Any remaining issues requiring human decision
    - Next steps (if any)
  - **Expected output:** CoDesigner_Summary.md with clear status and next actions
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Request Human CoDesigner confirmation (if required)
  - **Primary method:** If any CRITICAL or HIGH issues remain unresolved, or if goal_achievement_status is PARTIAL:
    - Present current status
    - Explain remaining issues
    - Request decision: [A] Accept current state, [B] Provide guidance for remaining issues, [C] Escalate for collaborative resolution
  - **Backup [1]:** If all CRITICAL issues resolved, mark troubleshooting as complete without escalation
  - **Expected output:** Human confirmation of project status OR guidance for remaining work
  - **Critical:** false
  - **Mode:** collaborative (conditional - only if issues remain)

- **Verification:** All verification methods pass OR remaining issues documented and approved by Human CoDesigner
- **Logging:** Record final status and verification results in progress_Troubleshoot.json

---

## Bridging: Markdown ↔ TOML Synchronisation

This spec file (Troubleshoot_SPEC.md) must maintain perfect alignment with its companion file (parameters_Troubleshoot.toml).

**Bridging Requirements:**
1. Each task in this file must have corresponding `[[tasks]]` entry in TOML with matching ID (0-4)
2. Each step within a task must have corresponding `[[tasks.steps]]` entry with matching ID
3. Expected outputs in this file must match `expected_output` fields in TOML
4. Critical flags must be synchronised between files
5. Constraints referenced must exist in TOML `[constraints]` section

**Example Cross-References:**
- "See `constraints.preserve_architecture` in parameters_Troubleshoot.toml" (Task 3 context)
- "As defined in `tasks[id=2]` in TOML" (Task 2 reference)
- "Must satisfy TOML verification requirements" (All task verifications)

The exe_Troubleshoot.md controller will validate this synchronisation during initialisation (Section 1.8).

---

## Instructions for LLM Executor

### ⚠️ LARGE CONTEXT LLM STRONGLY RECOMMENDED

**IMPORTANT: Before executing this TOOLSPEC, share this recommendation with the Human CoDesigner:**

```
⚠️ LARGE CONTEXT LLM RECOMMENDATION

This Troubleshoot TOOLSPEC is designed for complex projects and requires:
- Reading multiple SPEC files, progress logs, and deliverables
- Maintaining comprehensive issue tracking across long sessions
- Holding project state throughout troubleshooting (100+ actions)
- Generating detailed reports without context loss

RECOMMENDED LLM MODELS:
✅ Gemini 2.5 Pro (2M token context) - OPTIMAL
✅ Other 1M+ context token LLMs

SMALL CONTEXT LLMs:
❌ Risk losing track of earlier issues
❌ May need to re-read files multiple times
❌ Possible incomplete troubleshooting
❌ NOT RECOMMENDED for projects > 50 files

If using a small-context LLM, you may need to:
- Provide reminders about previously identified issues
- Re-supply earlier diagnostic findings  
- Track current task/step position manually
- Review files already modified

For best results, use Gemini 2.5 Pro or similar large-context model.
```

**After sharing this message with the user, proceed with troubleshooting.**

---

### Execution Mode: MOSTLY AUTONOMOUS (COLLABORATIVE ONLY FOR INITIALIZATION)

This SPEC requires **ONE MANDATORY USER INTERACTION**:
1. Project folder path (Task 0, Step 0)

Plus **ONE CONDITIONAL INTERACTION**:
2. Human CoDesigner confirmation (Task 4, Step 7) - ONLY if critical issues remain unresolved

All diagnostic and fixing tasks execute autonomously in silent mode.

#### Silent Mode Discipline

**Silent mode means:**
- ✅ Don't report every micro-action to user
- ✅ Work autonomously without asking permission
- ✅ Batch-report progress at logical checkpoints

**Silent mode does NOT mean:**
- ❌ Don't track state internally
- ❌ Skip documentation steps
- ❌ Work without systematic process
- ❌ Ignore workflow checkpoints

**Internal State Tracking in Silent Mode:**

Even when not communicating with user, maintain internal checkpoints:

```
[INTERNAL STATE - Silent Mode]
Time: 14:30:22
Task: 3.2 (Fix CRITICAL issues)
Issue: C-3 (SDK Mismatch)
Action: Installing @insforge/sdk
Backup: ✅ Created
Documentation: ⏳ Next step
Test Plan: Restart dev server, user tests registration
```

**When to Break Silence:**

Communicate with user when:
1. Task completes (e.g., "Task 2 complete: 6 issues identified")
2. CRITICAL issue requires user verification
3. Need user input to proceed
4. Escalation criteria met
5. Final report generation

**State Tracking Requirements:**
- Update progress_Troubleshoot.json after each major action
- Maintain current_state object at all times
- Use internal checkpoints before file modifications
- Follow all protocols even without user communication

### Backup Discipline

**NEVER modify a file without backup.**

Before each file modification:

```
[BACKUP CHECKPOINT]
File to modify: frontend/src/lib/supabase.ts
Backup exists: NO
Action: Creating backup...
Backup location: troubleshooting_2025-11-07/backups/lib/supabase.ts.backup-20251107-143022
Backup verified: YES
Proceeding with modification: YES
```

If you find yourself typing file modification commands without having created a backup:
1. STOP immediately
2. Create backup first
3. Document backup in fixes_applied.log
4. Then proceed

### Execution Guidelines

1. **Start with project location**: Prompt user for project folder path (Task 0, Step 0), then proceed autonomously
2. **Operate in fresh context**: Don't assume knowledge from original build - read all SPEC files and logs
3. **Be systematic**: Follow diagnostic workflow - don't jump to fixes without understanding root causes
4. **Fix conservatively**: Minimal changes to resolve issues, preserve original architecture
5. **Document everything**: Every fix must be logged with rationale, files changed, verification
6. **Test after each fix**: Verify fix works before moving to next issue
7. **Prioritise ruthlessly**: CRITICAL issues must be resolved; LOW issues can be documented
8. **Read original SPEC carefully**: Understand original goal and intent to guide fixes
9. **Check Definition of Complete**: This is the success criteria - all verification must reference this
10. **Use backup methods**: If primary fix approach fails, try alternatives before escalating
11. **Escalate intelligently**: Only escalate for genuinely ambiguous decisions or unresolvable issues
12. **Think like a debugger**: Isolate issues, test hypotheses, verify fixes systematically
13. **Maintain traceability**: Before/after documentation for every change
14. **Avoid scope creep**: Fix issues, don't rebuild or add new features
15. **Generate useful reports**: Documentation should help future troubleshooting and learning

### Context-Efficient Operation

Since this SPEC operates in **fresh LLM context** separate from original build:

- **Don't assume context**: Read original SPEC files completely
- **Rely on logs**: progress.json is your history of what happened
- **Be efficient**: Gather all context upfront in Task 1 before diagnosing
- **Summarise effectively**: Extract key information, don't re-read entire files multiple times
- **Focus on current state**: What exists now vs what should exist (Definition of Complete)

### Diagnostic Priorities

When diagnosing issues, check in this order:
1. **Deliverable existence**: Does primary deliverable exist?
2. **Syntax/Import errors**: Can code be executed at all?
3. **Core functionality**: Do critical features work?
4. **Quality standards**: Does output meet quality requirements?
5. **Edge cases**: Do non-critical paths work?
6. **Cosmetic issues**: Is presentation/formatting acceptable?

### Fix Implementation Priorities

When implementing fixes:
1. **CRITICAL issues first**: Must resolve to achieve goal
2. **HIGH issues second**: Major functionality improvements
3. **MEDIUM if time permits**: Quality improvements
4. **LOW document only**: Known limitations

### Escalation Criteria

Escalate to collaborative mode when:
- Root cause requires design decision (not just implementation)
- Fix would fundamentally change architecture
- Multiple fix approaches have tradeoffs requiring human judgment
- All fix attempts fail and no clear alternative exists
- Remaining issues require scope/requirement clarification

**Don't escalate for**: Straightforward implementation issues, missing dependencies, simple bugs, quality improvements.

---

## Expected Troubleshooting Report Structure

The final report should follow this structure:

```markdown
# Troubleshooting Report: [Project Name]

**Project Code:** [PROJECT_CODE]  
**Troubleshooting Date:** [DATE]  
**Troubleshooting Session:** [SESSION_ID]  
**Project Folder:** [PATH]

---

## Executive Summary

[2-3 paragraphs covering:]
- What the original goal was
- What issues were preventing goal achievement
- What was fixed
- Current project status (ACHIEVED/PARTIAL/NOT_ACHIEVED)

---

## Original Goal and Definition of Complete

### Original Goal
[Quote from original SPEC]

### Definition of Complete (Original Criteria)
[List all criteria from original SPEC with current status]

- [ ] Criterion 1 - Status: MET/NOT_MET/PARTIAL
- [ ] Criterion 2 - Status: MET/NOT_MET/PARTIAL
- [ ] ...

---

## Pre-Troubleshooting Assessment

### Project State Before Troubleshooting
- Deliverables found: [list with status]
- Completion status from original execution: [ACHIEVED/PARTIAL/NOT_ACHIEVED]
- Primary issues observed: [high-level summary]

### Errors Identified
[Table of errors from logs]

| Error Type | Count | Severity | Component |
|------------|-------|----------|-----------|
| Import errors | 3 | HIGH | main.py |
| ... | ... | ... | ... |

---

## Issue Registry

### CRITICAL Issues (Blocking Goal Achievement)

#### Issue C-1: [Title]
- **Severity:** CRITICAL
- **Component:** [File/module affected]
- **Description:** [What's broken]
- **Root Cause:** [Why it's broken]
- **Impact:** [How it blocks goal]
- **Status:** RESOLVED/UNRESOLVED

[Repeat for all CRITICAL issues]

### HIGH Priority Issues (Major Functionality)

[Same structure as CRITICAL issues]

### MEDIUM Priority Issues (Quality/Minor Functionality)

[Same structure]

### LOW Priority Issues (Cosmetic/Edge Cases)

[Same structure]

---

## Root Cause Analysis

### Primary Root Causes Identified

1. **[Root Cause Category]** (e.g., Missing Dependencies)
   - Issues attributed: C-1, H-2, M-3
   - Underlying reason: [Explanation]
   - Prevention recommendation: [How to avoid in future]

[Repeat for each root cause category]

---

## Fixes Applied

### Critical Fixes

#### Fix C-1: [Issue Title]
- **Issue:** [Brief description]
- **Fix Applied:** [What was done]
- **Files Modified:** [List of files]
- **Changes Made:** 
  ```
  [Before/after code snippets or descriptions]
  ```
- **Verification:** [How fix was tested]
- **Status:** VERIFIED WORKING

[Repeat for all critical fixes]

### High-Priority Fixes

[Same structure as Critical Fixes]

### Medium-Priority Fixes

[Same structure]

---

## Verification Results

### Definition of Complete Re-Assessment

| Criterion | Status Before | Status After | Notes |
|-----------|---------------|--------------|-------|
| Primary deliverable exists | NOT_MET | MET | [Deliverable] now present |
| Quality standards met | PARTIAL | MET | All quality checks pass |
| ... | ... | ... | ... |

### Functional Testing Results

| Test | Status | Notes |
|------|--------|-------|
| Core workflow A | PASS | Tested successfully |
| Core workflow B | PASS | Fixed in C-1 |
| ... | ... | ... |

### Regression Testing

[Confirm no new issues introduced]

---

## Outstanding Issues

### Unresolved Issues (if any)

[List any issues that remain, with explanation why and recommended next steps]

### Known Limitations

[Document LOW priority issues or intentional limitations]

---

## Recommendations

### For This Project
1. [Specific recommendation for remaining work or improvements]
2. [Testing recommendations]
3. [Deployment recommendations]

### For Future SPEC Development
1. [How to prevent similar issues]
2. [SPEC improvement suggestions]
3. [Validation improvements]

---

## Files Modified

Complete list of files changed during troubleshooting:

- `[filepath]` - [Description of changes]
- `[filepath]` - [Description of changes]
- ...

---

## Final Status

**Goal Achievement Status:** ACHIEVED / PARTIAL / NOT_ACHIEVED

**Rationale:** [Explanation of status based on Definition of Complete]

**Human CoDesigner Action Required:** YES / NO

[If YES, explain what decision/action is needed]

---

## Appendices

### A. Complete fixes_applied.log
[Full log of all changes]

### B. Verification Test Details
[Detailed test results]

### C. Error Logs (Original)
[Original error logs for reference]

### D. Backup Location
[Path to pre-troubleshooting backup]

```

---

## Common Troubleshooting Scenarios

### Scenario 1: Missing Primary Deliverable

**Symptoms:**
- CRITICAL: Primary deliverable from Definition of Complete does not exist
- progress.json shows goal_achievement_status: NOT_ACHIEVED or PARTIAL

**Diagnostic Steps:**
1. Check if deliverable was attempted but failed (check progress.json steps)
2. Identify which task/step was supposed to create deliverable
3. Check error logs for failure reason
4. Determine if issue was implementation or original SPEC design

**Fix Approaches:**
- **Primary:** Implement the missing deliverable following original SPEC intent
- **Backup [1]:** If original approach failed, use alternative method to create deliverable
- **Backup [2]:** If requirements were unclear, create minimal viable deliverable and escalate for CoDesigner approval

### Scenario 2: Deliverable Exists But Doesn't Work

**Symptoms:**
- Deliverable file exists but has errors when executed/used
- Error logs show runtime errors, crashes, or functional failures

**Diagnostic Steps:**
1. Attempt to execute/use the deliverable
2. Collect error messages and identify error types
3. Check for: syntax errors, import errors, logic errors, missing dependencies
4. Test core functionality vs edge cases to assess severity

**Fix Approaches:**
- **Primary:** Fix identified errors directly in deliverable
- **Backup [1]:** If errors are extensive, refactor problematic component
- **Backup [2]:** If deliverable is fundamentally flawed, regenerate using alternative approach

### Scenario 3: Quality Standards Not Met

**Symptoms:**
- Deliverable exists and runs but doesn't meet quality criteria from Definition of Complete
- Examples: Missing documentation, incomplete test coverage, UI not implemented, poor code quality

**Diagnostic Steps:**
1. Extract specific quality standards from Definition of Complete
2. Test deliverable against each standard
3. Identify gaps between current state and required standards
4. Categorise gaps by severity (CRITICAL if standard is mandatory, MEDIUM if nice-to-have)

**Fix Approaches:**
- **Primary:** Address each quality gap systematically (add documentation, implement tests, improve code)
- **Backup [1]:** If comprehensive quality fix is extensive, address CRITICAL quality issues only
- **Backup [2]:** Document quality gaps as known limitations if fixing would require rebuild

### Scenario 4: Multiple Interrelated Issues

**Symptoms:**
- Several issues present that may be related
- Fixing one issue might affect others
- Root cause unclear with multiple symptoms

**Diagnostic Steps:**
1. List all observed issues
2. Map dependencies between issues
3. Identify common root cause (e.g., all issues trace to missing configuration file)
4. Prioritise by impact on goal achievement

**Fix Approaches:**
- **Primary:** Fix root cause first, then verify if dependent issues resolve automatically
- **Backup [1]:** Fix issues individually in priority order if root cause unclear
- **Backup [2]:** Create fix plan and escalate for CoDesigner review if issue complexity is high

### Scenario 5: Ambiguous Requirements

**Symptoms:**
- Definition of Complete criteria unclear or subjective
- Original SPEC has vague expected outputs
- Unclear whether deliverable meets intent

**Diagnostic Steps:**
1. Document ambiguity specifically (what is unclear?)
2. Check original chat logs or context for clarification (if available)
3. Assess deliverable against most reasonable interpretation
4. Flag ambiguity for CoDesigner clarification

**Fix Approaches:**
- **Primary:** Implement most reasonable interpretation based on goal intent
- **Backup [1]:** Implement minimal viable solution that arguably satisfies criteria
- **Backup [2]:** ESCALATE to collaborative mode for CoDesigner clarification before proceeding

---

**End of Troubleshoot_SPEC.md**

This SPEC is designed to be reusable across any post-development troubleshooting scenario, enabling efficient issue resolution with fresh LLM context.

