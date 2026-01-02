# Better SPEC - SPEC_Engine Improvement System

**Version:** 1.0  
**Purpose:** Reusable SPEC for systematically improving the SPEC_Engine framework

---

## What Is This?

Better_SPEC is a reusable SPEC designed to process SPEC_Engine improvements in three distinct ways:

### Mode A: Report Analysis
Process completed development analysis reports (like those from Dev_Analysis_SPEC) to extract and implement improvement recommendations.

**When to use:** You have a completed analysis report with recommendations
**Example:** "Analyse @dev/_ANALYSIS/TGACGTCA_SPEC_Engine_Improvements.md"

### Mode B: Proposal Processing
Systematically work through improvement proposals in the `@dev/_SPEC_dev_proposals/` folder, **one at a time** (ADHD-friendly).

**When to use:** You want to process pending proposals systematically
**Example:** "Work through proposals in @dev/_SPEC_dev_proposals/"

### Mode C: Single Request
Handle a specific one-off improvement request.

**When to use:** You have a specific enhancement idea
**Example:** "Add verification requirements to Constitution Article IX"

---

## How To Use

### Basic Usage

```
Execute Better_SPEC with [your request]
```

The SPEC will **automatically detect** which mode to use based on your input:
- Report file path → Mode A
- Proposals folder / "work through proposals" → Mode B  
- Specific improvement description → Mode C

### Example Invocations

**Mode A Example:**
```
I need to process the improvement recommendations from 
C:\Users\Fab2\Desktop\AI\Specs\@dev\_ANALYSIS\TGACGTCA_SPEC_Engine_Improvements.md
```

**Mode B Example:**
```
Let's work through the proposals in @dev\_SPEC_dev_proposals/ systematically
```

**Mode C Example:**
```
I want to add a verification requirement to Article IX that forces agents 
to verify fixes before claiming completion
```

---

## Key Features

### ADHD-Friendly Design
- **One thing at a time** (Mode B processes ONE proposal per execution)
- **Clear progress tracking** (always know where you are)
- **Resumable** (can stop and continue later)
- **Structured presentation** (not overwhelming)

### Safety First
- **Always backs up originals** to `@filing/Better_SPEC_changes/`
- **Seeks approval before changes** (shows before/after)
- **Never deletes dev docs** (per user preferences)
- **Validates all changes** (syntax, coherence, constitutional alignment)

### Intelligent Operation
- **Auto-detects mode** (no need to specify)
- **Dynamic escalation** (collaborative when needed, silent when possible)
- **Constitutional enforcement** (all changes respect existing principles)
- **Cross-reference maintenance** (updates affected references automatically)

---

## What It Does

### Mode A Workflow
1. Reads analysis report
2. Extracts all recommendations
3. Presents them prioritised (Critical → Quick Wins → High Impact)
4. Gets your approval for each
5. Implements approved changes
6. Documents outcomes

### Mode B Workflow
1. Scans proposals folder
2. Inventories all proposals with impact/effort assessment
3. Shows you the list and recommends next proposal
4. Processes ONE proposal with you
5. Asks if you want to do another
6. Implements approved changes when you're done

### Mode C Workflow
1. Understands your specific request
2. Assesses feasibility and impact
3. Designs implementation approach
4. Shows you the plan
5. Gets approval
6. Implements changes

---

## Files Structure

```
Better_SPEC/
├── spec_Better_SPEC.md           Human-readable specification
├── parameters_Better_SPEC.toml   Machine-readable parameters
├── README.md                      This file
└── progress_Better_SPEC.json     (Generated during execution)
```

---

## Where Changes Go

### Backups
All original files are backed up before modification to:
```
@filing/Better_SPEC_changes/[timestamp]/originals/
```

### Session Documentation
Session summaries are saved to:
```
@filing/Better_SPEC_sessions/[timestamp]_[mode]_summary.md
```

### Modified Files
Changes are made directly to SPEC_Engine files:
- `__SPEC_Engine/_Constitution/constitution.md`
- `__SPEC_Engine/_templates/*.md`
- `__SPEC_Engine/_Commander_SPEC/Spec_Commander.md`
- `__SPEC_Engine/WORKFLOW_DIAGRAM.md`
- etc.

---

## Constitutional Compliance

This SPEC fully complies with all Constitutional Articles:

- **Article I:** Singular goal (improve SPEC_Engine)
- **Article II:** Proper hierarchy (Goal → Tasks → Steps → Backups)
- **Article III:** Dual-file mandate (spec + parameters)
- **Article VI:** Critical balance 40-50% (appropriate for meta-improvement work)
- **Article IX:** Dynamic mode with intelligent escalation
- **Article X:** Comprehensive logging to progress.json

---

## Critical Balance: 47% Overall

Breakdown by task:
- Task 0: 80% (mode detection critical)
- Task 1: 60% (report parsing critical)
- Task 2: 100% (user approval critical)
- Task 3: 0% (documentation only)
- Task 4: 60% (proposal inventory critical)
- Task 5: 86% (proposal processing critical)
- Task 6: 33% (continuation optional)
- Task 7: 87% (request handling critical)
- Task 8: 0% (documentation only)
- Task 9: 86% (implementation critical)
- Task 10: 40% (completion critical)

**Overall:** 47% critical (within 40-60% constitutional guideline)

---

## User Preferences Respected

This SPEC is designed with your specific preferences in mind:

- **One recommendation at a time** (per memory)
- **Seek approval before changes** (per COMM_PROTOCOL)
- **UK English throughout** (per user rules)
- **No dev doc deletion** (per memory)
- **Backs up to @filing/** (per memory)
- **ADHD-friendly** (per memory: chunks, structure, progress tracking)

---

## Next Steps

1. **To start using:** Simply provide input matching one of the three modes
2. **Mode A:** Give it a report path
3. **Mode B:** Ask to "work through proposals"
4. **Mode C:** Describe a specific improvement

The SPEC will handle the rest, working with you collaboratively to improve the SPEC_Engine framework.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-03 | Initial creation with three operational modes |

---

**Questions?** This SPEC is self-documenting. Read `spec_Better_SPEC.md` for complete detail on all tasks and steps.

