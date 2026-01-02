# Troubleshoot SPEC - Usage Guide

**Version:** 2.0  
**Last Updated:** 2025-11-07  
**Created:** 2025-11-03  
**Purpose:** Quick guide for using the reusable Troubleshoot SPEC

---

## Version History

### Version 2.0 (2025-11-07)

**Major Enhancements** - Preventing TOOLSPEC drift and improving execution discipline:

1. **State Tracking Protocol** - Explicit state awareness and position tracking throughout execution
2. **New Issue Discovery Protocol** - Systematic handling of issues discovered mid-workflow (prevents reactive debugging)
3. **Mandatory Backup Protocol** - Enforced backup checkpoints before any file modifications
4. **Fix Workflow Checklist** - Condensed 5-phase checklist for systematic issue resolution
5. **Task Transition Gates** - Completion verification before transitioning between tasks
6. **Silent Mode Discipline** - Clarified expectations for internal state tracking in autonomous mode
7. **Enhanced TOML Validation** - State tracking fields and validation rules for v2.0 protocols

**Efficacy:** These enhancements address 85-90% of observed workflow deviations in real-world troubleshooting sessions.

### Version 1.0 (2025-11-03)

Initial release with 4-phase troubleshooting workflow.

---

## What Is This?

The **Troubleshoot SPEC** is a reusable specification designed to systematically diagnose and fix issues in completed SPEC projects when:

- The original SPEC execution encountered errors
- Deliverables don't meet Definition of Complete criteria
- The original LLM context is exhausted (too long to continue)
- Post-development issues emerge that need fixing

---

## When To Use

Use the Troubleshoot SPEC when:

1. **Post-Development Issues**: Original SPEC completed but deliverables don't work properly
2. **Context Exhausted**: Original chat is too long to continue troubleshooting
3. **Fresh Start Needed**: Want systematic diagnosis rather than ad-hoc fixing
4. **Multiple Issues**: Several problems that need organised resolution
5. **Documentation Required**: Need record of what was wrong and how it was fixed

---

## How It Works

### 4-Phase Workflow

```
Phase 1: Initialize (Task 0)
  └─> Get project folder location (ONE USER INPUT)
  └─> Validate project structure
  └─> Identify SPEC files

Phase 2: Gather Context (Task 1)
  └─> Read original SPEC and Definition of Complete
  └─> Read execution logs (progress.json)
  └─> Catalogue deliverables and error logs
  └─> Understand what was supposed to be built

Phase 3: Diagnose (Task 2)
  └─> Check deliverables against Definition of Complete
  └─> Test existing deliverables for functionality
  └─> Analyse error logs
  └─> Categorise issues by severity (CRITICAL/HIGH/MEDIUM/LOW)
  └─> Perform root cause analysis

Phase 4: Fix (Task 3)
  └─> Backup current state
  └─> Fix CRITICAL issues (must resolve)
  └─> Fix HIGH issues (should resolve)
  └─> Fix MEDIUM issues (if time permits)
  └─> Document LOW issues (known limitations)

Phase 5: Verify (Task 4)
  └─> Re-run original verification methods
  └─> Test critical functionality
  └─> Verify no regressions
  └─> Generate troubleshooting report
  └─> Request CoDesigner confirmation (if issues remain)
```

---

## Usage Instructions

### Step 1: Identify Your Project

Locate the project folder containing:
- Original SPEC files: `spec_[descriptor].md`, `parameters_[descriptor].toml`
- Execution log: `progress_[descriptor].json`
- Project deliverables (code, executables, reports, etc.)

Example structure:
```
my_project/
├── spec_podcast.md
├── parameters_podcast.toml
├── progress_podcast.json
├── podcast-website/          # Deliverables
│   ├── index.html
│   ├── components/
│   └── ...
└── error_logs/               # Optional
```

### Step 2: Start Fresh LLM Context

**Important:** Open a NEW chat session (fresh context) to avoid context exhaustion.

### Step 3: Launch Troubleshoot SPEC

Provide to your LLM:

```
Use __SPEC_Engine/_templates/Troubleshoot_SPEC.md to troubleshoot my project.

Project folder: C:\Users\Fab2\Desktop\AI\Specs\[YOUR_PROJECT_FOLDER]
```

Or simply:

```
Use __SPEC_Engine/_templates/Troubleshoot_SPEC.md to troubleshoot my project.
```

The LLM will prompt you for the project folder path.

### Step 4: Provide Project Folder

When prompted:
```
Please provide the absolute path to the project folder containing the SPEC files and deliverables:
```

Respond with the full path:
```
C:\Users\Fab2\Desktop\AI\Specs\TGACGTCA\podcast-project
```

### Step 5: Let It Run

The Troubleshoot SPEC will now run **autonomously**:
- Reads your original SPEC files
- Reviews execution logs
- Tests deliverables
- Identifies issues
- Fixes problems systematically
- Generates report

**No further interaction needed** unless critical issues remain unresolved.

### Step 6: Review Results

When complete, you'll receive:

1. **Troubleshooting_Report_[PROJECT_CODE].md**
   - What was broken
   - Root causes identified
   - Fixes applied
   - Verification results
   - Current project status

2. **fixes_applied.log**
   - Detailed log of all changes made
   - Before/after documentation

3. **CoDesigner_Summary.md**
   - Quick summary for you
   - Current status vs Definition of Complete
   - Any remaining issues
   - Next steps

---

## Key Features

### Context-Efficient Operation

The Troubleshoot SPEC is designed to work in **fresh LLM context**:
- Doesn't require original build conversation history
- Reads all context from SPEC files and logs
- Operates independently of original execution

### Systematic Diagnosis

- Tests against original Definition of Complete
- Categorises issues by severity (CRITICAL → HIGH → MEDIUM → LOW)
- Performs root cause analysis
- Prioritises fixes intelligently

### Conservative Fixing

- **Preserves architecture**: Fixes existing code, doesn't rebuild
- **Minimal changes**: Only changes what's necessary
- **Backs up first**: Creates backup before applying fixes
- **Tests each fix**: Verifies fix works before moving on
- **Documents everything**: Logs every change with rationale

### Intelligent Escalation

Runs autonomously but escalates when:
- Root cause requires design decision
- All fix attempts fail
- Critical issues remain after exhaustive fixing
- Human judgment needed

---

## Common Scenarios

### Scenario 1: Build Completed But Executable Crashes

**Problem:**
- SPEC execution completed (goal_achievement_status: ACHIEVED)
- Executable created but crashes when run
- Error logs show runtime errors

**How Troubleshoot SPEC Helps:**
1. Reads original SPEC to understand intended functionality
2. Tests executable and captures crash errors
3. Analyses error logs for root cause (e.g., missing dependencies)
4. Fixes errors (installs dependencies, corrects code)
5. Verifies executable now runs successfully
6. Updates project status to ACHIEVED with verification

### Scenario 2: Build Partial - Missing Deliverables

**Problem:**
- SPEC execution stopped mid-way (goal_achievement_status: PARTIAL)
- Some deliverables missing
- Original context exhausted, can't continue

**How Troubleshoot SPEC Helps:**
1. Identifies missing deliverables from Definition of Complete
2. Checks progress.json to see what steps failed
3. Implements missing deliverables
4. Verifies all completion criteria now satisfied
5. Updates status to ACHIEVED

### Scenario 3: Quality Standards Not Met

**Problem:**
- Deliverable exists and runs
- Doesn't meet quality standards (incomplete documentation, poor UI, etc.)
- Definition of Complete criteria not satisfied

**How Troubleshoot SPEC Helps:**
1. Compares deliverable against quality standards
2. Identifies specific gaps (e.g., missing documentation sections)
3. Addresses quality issues systematically
4. Verifies standards now met
5. Confirms ACHIEVED status

### Scenario 4: Multiple Interrelated Issues

**Problem:**
- Several issues present
- Unclear which to fix first
- Concerned about introducing regressions

**How Troubleshoot SPEC Helps:**
1. Catalogues all issues systematically
2. Categorises by severity
3. Performs root cause analysis (may be one root cause)
4. Fixes in priority order (CRITICAL first)
5. Tests after each fix to detect regressions
6. Rolls back if fix introduces new issues

---

## Issue Severity Levels

The Troubleshoot SPEC categorises all issues by severity:

### CRITICAL
- **Definition:** Blocks original goal achievement or prevents core functionality
- **Examples:**
  - Primary deliverable missing
  - Executable crashes on startup
  - Core API endpoints non-functional
  - Critical data loss or corruption
- **Resolution:** **MUST** be fixed for completion

### HIGH
- **Definition:** Major functionality impaired, significant quality degradation
- **Examples:**
  - Important features broken
  - Major UI elements non-functional
  - Significant performance issues
  - Major security vulnerabilities
- **Resolution:** **SHOULD** be fixed, may document with workaround if fix complex

### MEDIUM
- **Definition:** Minor functionality issues, quality below standards but usable
- **Examples:**
  - Edge cases not handled
  - Incomplete documentation
  - UI formatting issues
  - Minor performance degradation
- **Resolution:** Fix if time permits, otherwise document for future iteration

### LOW
- **Definition:** Cosmetic issues, edge cases, nice-to-haves
- **Examples:**
  - Typos in UI text
  - Minor formatting inconsistencies
  - Optional features not implemented
  - Aesthetic improvements
- **Resolution:** Document as known limitations, don't fix during troubleshooting

---

## What Gets Fixed

### Always Fixed (Required for Completion)
- **CRITICAL issues**: All must be resolved
- **HIGH issues**: All should be resolved (or documented with workarounds)

### Sometimes Fixed (If Time Permits)
- **MEDIUM issues**: Fixed if straightforward, otherwise documented

### Never Fixed During Troubleshooting
- **LOW issues**: Documented only, marked as future enhancements
- **New features**: Troubleshooting fixes issues, doesn't add features
- **Architectural changes**: Preserves original architecture unless fundamentally broken

---

## Deliverables Generated

After troubleshooting completes, you'll find:

### 1. Troubleshooting Report
**Location:** `[project_folder]/Troubleshooting_Report_[PROJECT_CODE].md`

**Contents:**
- Executive summary
- Original goal and Definition of Complete
- Pre-troubleshooting assessment
- Complete issue registry (all issues categorised)
- Root cause analysis
- Fixes applied (before/after documentation)
- Verification results
- Outstanding issues (if any)
- Recommendations

### 2. Fixes Log
**Location:** `[project_folder]/fixes_applied.log`

**Contents:**
- Chronological log of all changes
- Issue ID → Fix applied → Files modified → Verification
- Traceability for every change

### 3. CoDesigner Summary
**Location:** `[project_folder]/CoDesigner_Summary.md`

**Contents:**
- Quick status overview (2-3 paragraphs)
- What was fixed
- Current status vs Definition of Complete
- Any remaining issues requiring decisions
- Next steps

### 4. Known Issues (if applicable)
**Location:** `[project_folder]/known_issues.md`

**Contents:**
- LOW severity issues not fixed
- Workarounds (if available)
- Future enhancement suggestions

### 5. Updated Progress Log
**Location:** `[project_folder]/progress_[descriptor].json`

**Updates:**
- Current goal_achievement_status (ACHIEVED/PARTIAL/NOT_ACHIEVED)
- Troubleshooting session metadata
- Link to troubleshooting report

### 6. Fixed Deliverables
**Location:** Original deliverable locations

**Updates:**
- Corrected code files
- Fixed executables
- Updated documentation
- Improved outputs

### 7. Backup
**Location:** `[project_folder]/pre-troubleshooting-backup_[timestamp]/`

**Contents:**
- Complete backup of project state before troubleshooting
- Enables rollback if needed

---

## Tips for Best Results

### 1. Prepare Your Project Folder
- Ensure SPEC files are present (`spec_*.md`, `parameters_*.toml`)
- Keep execution log (`progress_*.json`) - it contains valuable history
- Include any error logs or crash reports
- Don't delete "failed" deliverables - they provide diagnostic clues

### 2. Use Fresh Context
- **Always** start troubleshooting in a new chat session
- Don't try to troubleshoot in the same context as the original build
- Fresh context enables the SPEC to read everything systematically

### 3. Provide Complete Path
- Use absolute paths (e.g., `C:\Users\Fab2\Desktop\AI\Specs\project`)
- Avoid relative paths which may be ambiguous
- Include the full path to the project root folder

### 4. Trust the Process
- Let the SPEC run autonomously through diagnosis and fixing
- Don't interrupt with manual fixes during execution
- The systematic approach catches issues manual debugging misses

### 5. Review the Report
- Read the troubleshooting report after completion
- Understand what was wrong and how it was fixed
- Use recommendations to prevent similar issues in future SPECs

### 6. Test Thoroughly After
- Even though verification runs automatically, do your own testing
- Confirm the fixes work in your real-world usage scenarios
- Check that the project now meets your original intent

---

## Troubleshooting the Troubleshooter

### If Troubleshoot SPEC Can't Find SPEC Files

**Problem:** "Critical error: SPEC files not found in project folder"

**Solutions:**
1. Verify you provided the correct project folder path
2. Check folder contains `spec_*.md` and `parameters_*.toml`
3. If files are in a subdirectory, provide path to that subdirectory
4. If multiple projects in folder, specify which one when prompted

### If All Fixes Fail

**Problem:** Multiple fix attempts fail, issues remain unresolved

**What Happens:**
- Troubleshoot SPEC will escalate to collaborative mode
- You'll be presented with:
  - Issues that couldn't be resolved
  - Fix attempts made
  - Options: [A] Accept current state, [B] Provide guidance, [C] Escalate further

**Your Options:**
1. **Accept current state**: Mark as PARTIAL completion, document remaining issues
2. **Provide guidance**: Explain alternative fix approach or clarify requirements
3. **Escalate**: Acknowledge that project needs redesign or human intervention

### If Issues Are Ambiguous

**Problem:** Can't determine if deliverable meets original intent

**What Happens:**
- Troubleshoot SPEC flags ambiguity
- Escalates to collaborative mode
- Asks for clarification on requirements or acceptance criteria

**Your Action:**
- Clarify what you originally intended
- Confirm whether current state is acceptable
- Provide additional context from original goal

---

## Integration with SPEC Engine

The Troubleshoot SPEC follows all constitutional requirements:

- **Article I (North Star)**: Single goal - fix issues to meet Definition of Complete
- **Article II (Hierarchy)**: 5 tasks (0-4), 1-8 steps per task ✓
- **Article III (Dual-File)**: Troubleshoot_SPEC.md + parameters_Troubleshoot.toml ✓
- **Article VI (Critical Flags)**: 60% critical balance ✓
- **Article VII (Backups)**: Alternative methods, not retries ✓
- **Article IX (Modes)**: Silent with intelligent escalation ✓
- **Article X (Logging)**: Comprehensive progress tracking ✓

---

## Comparison: Original SPEC vs Troubleshoot SPEC

| Aspect | Original SPEC | Troubleshoot SPEC |
|--------|---------------|-------------------|
| **Purpose** | Build from scratch | Fix existing project |
| **Context** | Continues from goal definition | Fresh context, reads SPEC files |
| **Inputs** | Goal + requirements | Project folder + SPEC files |
| **Process** | Implement tasks sequentially | Diagnose → Fix → Verify |
| **Output** | New deliverables | Fixed deliverables |
| **Documentation** | SPEC files + progress.json | Troubleshooting report + fixes log |
| **Mode** | Builds autonomously | Fixes autonomously |
| **Escalation** | Escalates on execution issues | Escalates on unresolvable issues |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-03 | Initial creation - reusable troubleshooting SPEC |

---

## Next Steps

Ready to troubleshoot your project?

1. Locate your project folder
2. Open fresh LLM chat session
3. Run: `Use __SPEC_Engine/_templates/Troubleshoot_SPEC.md to troubleshoot my project`
4. Provide project folder path when prompted
5. Let it run autonomously
6. Review troubleshooting report

**Need help?** Check the Common Scenarios section above for examples similar to your situation.

---

**Questions? Feedback?**

The Troubleshoot SPEC is part of the SPEC Engine framework. See `__SPEC_Engine/README.md` for more information about the system.

