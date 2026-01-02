# Better SPEC

**Version:** 1.0  
**Last Updated:** 2025-11-03  
**Purpose:** Systematically improve SPEC_Engine through analysis of development reports, processing of improvement proposals, or implementing specific enhancement requests

---

## Goal

Improve the SPEC_Engine framework by processing development analysis reports, systematically working through improvement proposals, or implementing specific enhancement requests to strengthen constitutional principles, templates, and execution quality.

---

## Software Stack & Architecture

**Not Applicable** - This is an analytical and documentation improvement task, not a build goal.

---

## Definition of Complete

What must exist and be verified:
- [ ] **Primary deliverables:** 
  - Improvements implemented (constitutional amendments, template updates, documentation enhancements)
  - Changes documented with rationale and version tracking
  - Original documents backed up to @filing/ (if modified)
  - progress_Better_SPEC.json tracking all actions taken
- [ ] **Quality standards met:** 
  - Constitutional compliance maintained (no contradictions introduced)
  - All changes align with existing Design Philosophy
  - Bridging integrity preserved across affected files
  - Changes tested for coherence with existing SPECs
- [ ] **Verification method:** 
  - Modified files are syntactically valid (Markdown renders, TOML parses)
  - Cross-references updated where affected
  - Change log entries added to relevant files
  - User approval obtained for all changes (per COMM_PROTOCOL)

---

## Definitions

- **goal**: Improve SPEC_Engine through systematic processing of improvements
- **task[n]**: Discrete objectives for different operational modes
- **step[m]**: Concrete actions within each task
- **backup[p]**: Alternative approaches when primary method is blocked
- **critical_flag**: Boolean indicating whether step failure blocks goal achievement
- **mode**: Dynamic (auto-detects operational mode, escalates when appropriate)
- **progress.json**: Structured log tracking improvements, decisions, and changes made
- **operational mode**: A (Report Analysis), B (Proposal Processing), C (Single Request)

---

## Components

Analysis and improvement requires access to:
- **SPEC_Engine core files:** Constitution, templates, Commander, DNA_SPEC, workflow diagrams
- **Development reports:** Analysis outputs from Dev_Analysis_SPEC or similar
- **Proposal documents:** Files in @dev\_SPEC_dev_proposals/
- **Filing archive:** @filing/ for backing up modified documents
- **Progress tracking:** progress_Better_SPEC.json

**Deliverables Generated:**
- **Modified framework files:** Updated Constitution, templates, documentation
- **Backup copies:** Original versions saved to @filing/Better_SPEC_changes/[timestamp]/
- **Change documentation:** Amendments logged in version history
- **progress_Better_SPEC.json:** Complete action log

**Machine-Readable Components:**  
See `[components]` section in parameters_Better_SPEC.toml

---

## Constraints

- All changes must align with existing constitutional principles
- No deletion of development documentation (per user memory)
- User approval required before implementing changes (per COMM_PROTOCOL)
- One proposal at a time for Mode B (ADHD-friendly processing)
- Maintain backwards compatibility where possible
- Original documents must be backed up before modification

**Machine-Readable Constraints:**  
See `[constraints]` section in parameters_Better_SPEC.toml:
- `user_approval_required = true`
- `backup_originals = true`
- `one_proposal_at_a_time = true` (Mode B)
- `preserve_backwards_compatibility = true`

---

## User Stories

- As a **SPEC_Engine developer**, I want to systematically process improvement recommendations so framework quality continuously improves
- As a **SPEC author**, I want constitutional guidance to evolve based on real-world usage patterns
- As a **system maintainer**, I want to process proposals one at a time so I can focus without cognitive overload
- As a **researcher**, I want analysis reports to drive concrete improvements rather than sitting unused

---

## Operational Modes

This SPEC operates in **three distinct modes**, auto-detected based on inputs:

### Mode A: Report Analysis
**Trigger:** User provides path to analysis report (e.g., TGACGTCA_SPEC_Engine_Improvements.md)
**Purpose:** Extract and implement improvements from completed development analysis
**Tasks executed:** Tasks 0, 1-3, 9-10

### Mode B: Collaborative Proposal Processing
**Trigger:** User requests "work through proposals" or provides proposals folder path
**Purpose:** Systematically process improvement proposals one at a time
**Tasks executed:** Tasks 0, 4-6, 9-10
**Key feature:** Processes ONE proposal per execution (ADHD-friendly)

### Mode C: Single Request Handler
**Trigger:** User provides specific improvement request
**Purpose:** Implement a specific one-off enhancement
**Tasks executed:** Tasks 0, 7-8, 9-10

---

## Task [0]: Initialise and Determine Operational Mode

**TOML Reference:** `tasks[id=0]` in parameters_Better_SPEC.toml  
**Purpose:** Understand what the user wants to improve and select appropriate operational mode

- **Step [0]:** Receive user input and context
  - **Primary method:** Analyse user query to identify what they're providing (report path, proposal request, specific improvement)
  - **Expected output:** User input captured and categorised
  - **Critical:** true
  - **Mode:** collaborative

- **Step [1]:** Detect operational mode
  - **Primary method:** Determine mode based on input:
    - If report file path provided → Mode A (Report Analysis)
    - If "proposals" or folder path mentioned → Mode B (Proposal Processing)
    - If specific improvement described → Mode C (Single Request)
  - **Backup [1]:** If ambiguous, ask user to clarify which mode they intend
  - **Expected output:** Operational mode clearly identified (A, B, or C)
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Validate inputs based on mode
  - **Primary method:** For Mode A: Verify report file exists; Mode B: Verify proposals folder exists; Mode C: Verify request is specific and actionable
  - **Backup [1]:** If inputs missing or invalid, escalate to collaborative mode to gather required information
  - **Expected output:** Required inputs validated and accessible
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Scan SPEC_Engine current state
  - **Primary method:** Read current versions of Constitution, templates, Commander, workflow docs to establish baseline
  - **Expected output:** Current framework state documented with version numbers
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Route to appropriate task set
  - **Primary method:** Based on detected mode, proceed to relevant tasks (1-3 for A, 4-6 for B, 7-8 for C)
  - **Expected output:** Mode-specific tasks initiated
  - **Critical:** true
  - **Mode:** silent

- **Verification:** Operational mode clearly identified, inputs validated, framework baseline established
- **Logging:** Record mode selection and routing decision in progress_Better_SPEC.json

---

## Task [1]: Analyse Development Report (Mode A)

**TOML Reference:** `tasks[id=1]` in parameters_Better_SPEC.toml  
**Purpose:** Extract actionable recommendations from analysis report

- **Step [1]:** Read and parse analysis report
  - **Primary method:** Read provided report file, identify structure, extract all sections
  - **Expected output:** Complete report contents loaded into context
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Extract improvement recommendations
  - **Primary method:** Parse recommendations section, identify all proposed improvements with priority levels
  - **Expected output:** Structured list of recommendations with priorities (P1, P2, P3), impact, effort
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Categorise recommendations by target component
  - **Primary method:** Group recommendations by target: Constitution articles, template updates, Commander changes, workflow docs, new SPECs
  - **Expected output:** Recommendations categorised by affected component
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Identify quick wins
  - **Primary method:** Filter for P1 priority + Low effort recommendations
  - **Expected output:** List of high-impact, low-effort improvements
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Identify critical issues
  - **Primary method:** Extract all CRITICAL severity issues from report
  - **Expected output:** List of critical problems requiring immediate attention
  - **Critical:** true
  - **Mode:** silent

- **Verification:** All recommendations extracted, categorised, and prioritised
- **Logging:** Record extracted recommendations in progress_Better_SPEC.json

---

## Task [2]: Prioritise and Present Recommendations (Mode A)

**TOML Reference:** `tasks[id=2]` in parameters_Better_SPEC.toml  
**Purpose:** Present recommendations to user for approval

- **Step [1]:** Generate prioritised improvement plan
  - **Primary method:** Create ordered list: Critical issues first, then P1 quick wins, then P1 high-effort, then P2
  - **Expected output:** Prioritised implementation plan with rationale for ordering
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Present plan to user
  - **Primary method:** Display prioritised recommendations with clear structure:
    - Recommendation title and description
    - Target component
    - Expected benefit
    - Implementation effort
    - Proposed order
  - **Expected output:** User presented with clear, structured plan
  - **Critical:** true
  - **Mode:** collaborative

- **Step [3]:** Capture user decisions
  - **Primary method:** For each recommendation, get user decision: Approve/Reject/Modify/Defer
  - **Backup [1]:** If user wants to discuss, engage in collaborative dialogue to refine approach
  - **Expected output:** User approval status for each recommendation
  - **Critical:** true
  - **Mode:** collaborative

- **Step [4]:** Create implementation queue
  - **Primary method:** Build ordered queue of approved recommendations
  - **Expected output:** Final implementation queue with user-approved items
  - **Critical:** true
  - **Mode:** silent

- **Verification:** User has reviewed and approved/rejected all recommendations, implementation queue is ready
- **Logging:** Record user decisions in progress_Better_SPEC.json

---

## Task [3]: Document Report Processing (Mode A)

**TOML Reference:** `tasks[id=3]` in parameters_Better_SPEC.toml  
**Purpose:** Track which report was processed and outcomes

- **Step [1]:** Create processing summary
  - **Primary method:** Document: report source, date processed, recommendations extracted, user decisions, queued implementations
  - **Expected output:** Processing summary markdown file
  - **Critical:** false
  - **Mode:** silent

- **Step [2]:** Save summary to filing
  - **Primary method:** Save summary to @filing/Better_SPEC_sessions/[timestamp]_report_analysis.md
  - **Expected output:** Summary filed for future reference
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Report processing documented
- **Logging:** Record summary file path in progress_Better_SPEC.json

---

## Task [4]: Scan and Inventory Proposals (Mode B)

**TOML Reference:** `tasks[id=4]` in parameters_Better_SPEC.toml  
**Purpose:** Identify all improvement proposals in the proposals folder

- **Step [1]:** Scan proposals folder
  - **Primary method:** List all files in @dev\_SPEC_dev_proposals/, recursively include subdirectories
  - **Expected output:** Complete inventory of proposal files with paths
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Read and parse each proposal
  - **Primary method:** For each file, read contents, extract: title, summary, proposed changes, rationale
  - **Backup [1]:** If file format unclear, attempt to extract key information from available structure
  - **Expected output:** Structured data for each proposal
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Categorise proposals
  - **Primary method:** Group by category: Constitutional amendments, Template updates, Commander enhancements, New features, Documentation improvements
  - **Expected output:** Proposals categorised by type
  - **Critical:** false
  - **Mode:** silent

- **Step [4]:** Assess impact and effort for each proposal
  - **Primary method:** Analyse each proposal to estimate: Impact (High/Medium/Low), Effort (High/Medium/Low), Urgency (Critical/High/Medium/Low)
  - **Expected output:** Impact/effort/urgency assessment for all proposals
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Check for already-processed proposals
  - **Primary method:** Review progress_Better_SPEC.json for previously processed proposals
  - **Expected output:** List of new proposals and previously processed proposals
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All proposals inventoried, parsed, categorised, and assessed
- **Logging:** Record proposal inventory in progress_Better_SPEC.json

---

## Task [5]: Select and Process Single Proposal (Mode B)

**TOML Reference:** `tasks[id=5]` in parameters_Better_SPEC.toml  
**Purpose:** Work through ONE proposal with user

- **Step [1]:** Present proposal inventory to user
  - **Primary method:** Display all proposals with: title, category, impact/effort/urgency, processing status (new/processed)
  - **Expected output:** User sees complete proposal landscape
  - **Critical:** true
  - **Mode:** collaborative

- **Step [2]:** Let user select proposal OR recommend next
  - **Primary method:** Ask user: "Which proposal would you like to work on?" Also provide recommendation based on: Critical urgency → High impact/Low effort → High impact/Medium effort
  - **Backup [1]:** If user unsure, provide detailed rationale for recommended proposal
  - **Expected output:** Specific proposal selected for processing
  - **Critical:** true
  - **Mode:** collaborative

- **Step [3]:** Present selected proposal in detail
  - **Primary method:** Display full proposal contents:
    - Title and rationale
    - Proposed changes with specifics
    - Expected benefits
    - Potential risks or considerations
    - Affected components
  - **Expected output:** User has complete understanding of proposal
  - **Critical:** true
  - **Mode:** collaborative

- **Step [4]:** Discuss and refine with user
  - **Primary method:** Engage in dialogue:
    - "Do you agree with this approach?"
    - "Should we modify anything?"
    - "Are there concerns about implementation?"
  - **Expected output:** User feedback captured, proposal refined if needed
  - **Critical:** true
  - **Mode:** collaborative

- **Step [5]:** Get approval decision
  - **Primary method:** Ask user: "Should we implement this proposal? (Approve/Modify/Reject/Defer)"
  - **Expected output:** Clear approval status
  - **Critical:** true
  - **Mode:** collaborative

- **Step [6]:** If approved, add to implementation queue
  - **Primary method:** Add approved proposal to implementation queue for Task 9
  - **Expected output:** Proposal queued for implementation
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Mark proposal as processed
  - **Primary method:** Update progress_Better_SPEC.json to record: proposal processed, decision made, timestamp
  - **Expected output:** Proposal tracking updated
  - **Critical:** false
  - **Mode:** silent

- **Verification:** One proposal fully processed, user decision captured, tracking updated
- **Logging:** Record proposal processing in progress_Better_SPEC.json with full detail

---

## Task [6]: Check for More Proposals (Mode B)

**TOML Reference:** `tasks[id=6]` in parameters_Better_SPEC.toml  
**Purpose:** Determine if user wants to process another proposal (ONE AT A TIME)

- **Step [1]:** Ask if user wants to continue
  - **Primary method:** Ask: "Would you like to process another proposal now, or stop here?"
  - **Expected output:** User decision (continue or stop)
  - **Critical:** false
  - **Mode:** collaborative

- **Step [2]:** If continue, return to Task 5
  - **Primary method:** Loop back to Task 5 Step 1 to select next proposal
  - **Expected output:** Next proposal processing initiated
  - **Critical:** false
  - **Mode:** silent

- **Step [3]:** If stop, proceed to implementation
  - **Primary method:** Continue to Task 9 to implement queued approvals
  - **Expected output:** Implementation phase initiated
  - **Critical:** true
  - **Mode:** silent

- **Verification:** User decision captured, appropriate routing executed
- **Logging:** Record continuation decision in progress_Better_SPEC.json

---

## Task [7]: Process Single Improvement Request (Mode C)

**TOML Reference:** `tasks[id=7]` in parameters_Better_SPEC.toml  
**Purpose:** Handle specific one-off improvement request

- **Step [1]:** Parse user request
  - **Primary method:** Extract from user input: what they want to improve, why, target component
  - **Expected output:** Request clearly understood and structured
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Assess request feasibility and impact
  - **Primary method:** Analyse: Is request constitutional? Does it contradict existing principles? What files need modification? What's the implementation complexity?
  - **Expected output:** Feasibility assessment with affected components identified
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Identify potential conflicts or issues
  - **Primary method:** Check if request conflicts with: existing constitutional articles, design philosophy, current templates, other recent changes
  - **Backup [1]:** If conflicts found, identify ways to resolve or accommodate
  - **Expected output:** Conflict analysis with resolution suggestions if applicable
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Design implementation approach
  - **Primary method:** Create specific implementation plan: which files to modify, exact changes needed, order of operations
  - **Expected output:** Detailed implementation plan
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Present proposal to user
  - **Primary method:** Show user:
    - Their original request (restated)
    - Proposed implementation approach
    - Files that will be modified
    - Expected benefits
    - Potential risks or considerations
    - Any conflicts or trade-offs
  - **Expected output:** User has complete picture of implementation
  - **Critical:** true
  - **Mode:** collaborative

- **Step [6]:** Discuss and refine
  - **Primary method:** Engage with user to refine approach based on their feedback
  - **Expected output:** Implementation approach refined and approved
  - **Critical:** true
  - **Mode:** collaborative

- **Step [7]:** Get approval
  - **Primary method:** Ask: "Should we proceed with this implementation?"
  - **Expected output:** Clear approval or rejection
  - **Critical:** true
  - **Mode:** collaborative

- **Step [8]:** If approved, add to implementation queue
  - **Primary method:** Queue approved changes for Task 9
  - **Expected output:** Changes queued for implementation
  - **Critical:** true
  - **Mode:** silent

- **Verification:** Request understood, implementation designed, user approval obtained
- **Logging:** Record request processing in progress_Better_SPEC.json

---

## Task [8]: Document Request Processing (Mode C)

**TOML Reference:** `tasks[id=8]` in parameters_Better_SPEC.toml  
**Purpose:** Track the single request and decision

- **Step [1]:** Create request summary
  - **Primary method:** Document: original request, implementation approach, user decision, timestamp
  - **Expected output:** Request summary markdown
  - **Critical:** false
  - **Mode:** silent

- **Step [2]:** Save to filing
  - **Primary method:** Save to @filing/Better_SPEC_sessions/[timestamp]_single_request.md
  - **Expected output:** Summary filed
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Request documented
- **Logging:** Record summary path in progress_Better_SPEC.json

---

## Task [9]: Implement Approved Changes

**TOML Reference:** `tasks[id=9]` in parameters_Better_SPEC.toml  
**Purpose:** Execute all approved improvements

- **Step [1]:** Review implementation queue
  - **Primary method:** List all approved changes queued from previous tasks
  - **Expected output:** Complete list of changes to implement
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Create backup of original files
  - **Primary method:** For each file to be modified, copy current version to @filing/Better_SPEC_changes/[timestamp]/originals/
  - **Expected output:** All original files backed up
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Implement changes systematically
  - **Primary method:** For each change in queue:
    - Show user exactly what will be changed (before/after)
    - Get confirmation
    - Make the modification
    - Verify syntax validity
    - Document change in file's version history
  - **Backup [1]:** If user wants to modify the change, engage in refinement dialogue
  - **Expected output:** All approved changes implemented successfully
  - **Critical:** true
  - **Mode:** collaborative

- **Step [4]:** Update cross-references
  - **Primary method:** If changes affect cross-referenced sections (e.g., Constitution article numbers), update all references across affected files
  - **Expected output:** Cross-reference integrity maintained
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Verify file validity
  - **Primary method:** Check modified files: Markdown renders correctly, TOML parses without errors, JSON is valid
  - **Backup [1]:** If validation errors found, fix syntax issues
  - **Expected output:** All modified files syntactically valid
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Test for constitutional coherence
  - **Primary method:** Review modifications against constitutional principles to ensure no contradictions introduced
  - **Expected output:** Coherence verification passed
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Create change log
  - **Primary method:** Generate comprehensive change log listing: files modified, nature of changes, rationale, timestamp
  - **Expected output:** Detailed change log document
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All changes implemented, files valid, coherence maintained, backups created
- **Logging:** Record all implementations in progress_Better_SPEC.json with full detail

---

## Task [10]: Finalise and Document

**TOML Reference:** `tasks[id=10]` in parameters_Better_SPEC.toml  
**Purpose:** Complete the improvement cycle with documentation

- **Step [1]:** Generate session summary
  - **Primary method:** Create summary document:
    - Operational mode used
    - Changes implemented
    - Files modified
    - Backup locations
    - Outcomes and benefits
  - **Expected output:** Session summary markdown
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Save summary to filing
  - **Primary method:** Save to @filing/Better_SPEC_sessions/[timestamp]_session_summary.md
  - **Expected output:** Summary filed
  - **Critical:** false
  - **Mode:** silent

- **Step [3]:** Update SPEC_Engine documentation
  - **Primary method:** If changes warrant it, update WORKFLOW_DIAGRAM.md or README.md to reflect improvements
  - **Backup [1]:** Skip if changes are minor and don't affect user-facing documentation
  - **Expected output:** Framework documentation current (if applicable)
  - **Critical:** false
  - **Mode:** silent

- **Step [4]:** Present completion report to user
  - **Primary method:** Show user:
    - What was accomplished
    - Files modified (with paths)
    - Where backups are stored
    - Next recommended actions (if any)
  - **Expected output:** User informed of all outcomes
  - **Critical:** true
  - **Mode:** collaborative

- **Step [5]:** Clean up temporary files
  - **Primary method:** Remove any temporary analysis files created during execution
  - **Expected output:** Workspace clean
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Session documented, user informed, workspace clean
- **Logging:** Record completion in progress_Better_SPEC.json

---

## Bridging: Markdown ↔ TOML Synchronisation

This spec file (spec_Better_SPEC.md) must maintain perfect alignment with its companion file (parameters_Better_SPEC.toml).

**Bridging Requirements:**
1. Each task in this file must have corresponding `[[tasks]]` entry in TOML with matching ID (0-10)
2. Each step within a task must have corresponding `[[tasks.steps]]` entry with matching ID
3. Expected outputs in this file must match `expected_output` fields in TOML
4. Critical flags must be synchronised between files
5. Constraints referenced must exist in TOML `[constraints]` section

**Example Cross-References:**
- "See `constraints.user_approval_required` in parameters_Better_SPEC.toml" (Task 9)
- "As defined in `tasks[id=5]` in TOML" (Mode B proposal processing)
- "Must satisfy TOML verification requirements" (All task verifications)

The exe_Better_SPEC.md controller validates this synchronisation during initialisation (Section 1.8).

---

## Instructions for LLM Executor

### Execution Mode: DYNAMIC

This SPEC uses **Dynamic mode** throughout:
- Silent execution where possible
- Collaborative escalation when user input required
- Intelligent mode switching based on context

### Key Operational Principles

1. **Mode auto-detection**: Don't ask user which mode - determine from their input
2. **One at a time (Mode B)**: Process only ONE proposal per execution in Mode B
3. **Always get approval**: Show changes before making them (per COMM_PROTOCOL)
4. **Back up originals**: Never modify without creating backup first
5. **UK English**: All communication and documentation in British English
6. **ADHD-friendly**: Clear structure, one thing at a time, progress visible

### Execution Guidelines

1. **Start by understanding context**: What is the user providing? (report, proposals folder, single request)
2. **Auto-detect mode silently**: Don't announce "I'm in Mode A" - just operate in that mode
3. **Present information clearly**: Use structured formatting, bullet points, clear headings
4. **One proposal at a time (Mode B)**: Never batch process - always do one, ask if they want another
5. **Seek approval before changes**: Show exact before/after, wait for confirmation
6. **Maintain constitutional alignment**: Every change must respect existing principles
7. **Track everything**: Log all decisions, changes, and outcomes in progress.json
8. **Back up religiously**: Original must be in @filing/ before any modification
9. **Communicate in UK English**: Realise, analyse, organise (not realize, analyze, organize)
10. **Be concise**: User prefers one recommendation at a time (per memory)

### Mode-Specific Guidance

**Mode A (Report Analysis):**
- Extract all recommendations efficiently
- Present in priority order (Critical → P1 Quick Wins → P1 High Effort → P2)
- Let user approve/reject each one
- Queue approved items for batch implementation

**Mode B (Proposal Processing):**
- Show full inventory first
- Recommend next proposal but let user choose
- Process ONLY ONE proposal
- Ask if they want to do another
- If yes, loop back; if no, implement what's been approved

**Mode C (Single Request):**
- Understand the specific ask
- Design implementation approach
- Show full impact assessment
- Get approval
- Implement

### Critical Success Factors

1. **User approval for all changes**: Never surprise the user with modifications
2. **One thing at a time**: Don't overwhelm with multiple simultaneous actions
3. **Backups always**: File protection is non-negotiable
4. **Clear communication**: Explain what you're doing and why
5. **Constitutional coherence**: Every change must strengthen, not weaken, the framework

### Escalation Triggers

Escalate to collaborative mode when:
- User input is ambiguous
- Implementation approach has multiple valid options
- Change might have unexpected consequences
- Constitutional conflict detected
- User seems uncertain or needs discussion

### Documentation Standards

All changes must include:
- Rationale (why this change?)
- Affected files (what's being modified?)
- Version increment (update version histories)
- Backup location (where's the original?)
- Testing notes (how to verify?)

---

## Expected Output Structure

Depending on mode, outputs will vary:

### Mode A Output
```markdown
# Better_SPEC Session Report: Report Analysis
**Date:** [timestamp]
**Report Analysed:** [path]

## Recommendations Extracted
[List all recommendations with priorities]

## User Decisions
[Approve/Reject/Modify for each]

## Implementations Completed
[List changes made]

## Files Modified
[Paths to modified files]

## Backups Location
[Path to backup folder]

## Next Steps
[Recommended follow-up actions]
```

### Mode B Output
```markdown
# Better_SPEC Session Report: Proposal Processing
**Date:** [timestamp]
**Proposals Processed:** [count]

## Proposals Reviewed
[List of proposals reviewed with decisions]

## Proposal Details
### [Proposal Title]
- **Decision:** Approved/Rejected/Deferred
- **Implementation:** [if approved, what was done]
- **Rationale:** [why]

## Files Modified
[Paths to modified files]

## Backups Location
[Path to backup folder]

## Remaining Proposals
[Count and categories of unprocessed proposals]

## Next Recommended Proposal
[Suggestion for next session]
```

### Mode C Output
```markdown
# Better_SPEC Session Report: Single Request
**Date:** [timestamp]

## Request
[Original user request restated]

## Implementation Approach
[What was designed]

## User Decision
[Approved/Rejected/Modified]

## Changes Made
[If approved, detailed change list]

## Files Modified
[Paths to modified files]

## Backups Location
[Path to backup folder]

## Verification
[How to verify change is working]
```

---

**End of spec_Better_SPEC.md**

This SPEC is designed to be reusable across all SPEC_Engine improvement activities, operating intelligently in three distinct modes based on user needs.

