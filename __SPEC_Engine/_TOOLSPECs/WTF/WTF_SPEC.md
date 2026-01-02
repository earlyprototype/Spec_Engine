# WTF SPEC (What's This Feature)

**Version:** 1.0  
**Last Updated:** 2 January 2026  
**Purpose:** Feature archaeology - systematically understand mysterious, undocumented, or legacy code

---

## Goal

Reverse-engineer and document the purpose, behaviour, and dependencies of an unknown code feature or module, producing comprehensive documentation that enables maintenance and extension.

---

## Knowledge Capture (Notepad)

**Purpose:** Capture insights, observations, and learnings during execution.

This notepad will be populated during execution with:
- Key insights and aha moments
- Technical discoveries and decisions
- Ideas for future enhancements
- Cross-system connections and patterns
- Observations from both AI executor and human user

**File:** `notepad_WTF.md` (automatically created during execution)

**Update Frequency:** Configured in parameters.toml (per_task by default)

---

## Software Stack & Architecture

**Not Applicable** - This is a code analysis/documentation task, not a build goal.

---

## Definition of Complete

What must exist and be verified:
- [ ] **Primary deliverable:** Comprehensive feature documentation including:
  - Feature purpose statement (1-2 sentences)
  - User stories ("As a [role], I want [capability] so that [benefit]")
  - Code flow diagram (visual representation of execution paths)
  - Dependencies map (upstream and downstream)
  - Edge cases and failure modes documented
  - Usage examples (code snippets showing how to use the feature)
  - Integration points (how feature connects to rest of system)
- [ ] **Quality standards met:**
  - Documentation is accurate (verified against actual code behaviour)
  - Examples are executable and produce expected results
  - Dependencies are complete (no undocumented dependencies discovered later)
  - Coverage is complete (all entry points documented)
- [ ] **Verification method:**
  - Documentation reviewed by someone unfamiliar with the code
  - Examples execute successfully
  - Integration points verified by inspection
  - Human CoDesigner confirms documentation enables understanding

---

## Troubleshooting Ecosystem

This TOOLSPEC is part of a three-spec troubleshooting ecosystem:

| TOOLSPEC | When to Use | Output |
|----------|-------------|--------|
| **Troubleshoot** | Post-development issues blocking goal | Fixed deliverables |
| **WTF** | Mysterious/legacy code needs understanding | Documentation |
| **Forensic** | Critical failure needs root cause | Investigation report |

**Decision Tree:**
1. Is this a production incident with data loss/security breach? → Use **Forensic**
2. Is the code mysterious/undocumented and you need to understand it? → Use **WTF** (this spec)
3. Is something broken and needs fixing? → Use **Troubleshoot**

**When to use WTF:**
- You've inherited legacy code with no documentation
- Code behaviour is unexpected or confusing
- You need to modify code but don't understand its purpose
- Preparing to refactor or replace mysterious code
- Building knowledge base for team onboarding

---

## MCP Toolset

### Installed Tools (Verified During SPEC Creation)

**REQUIRED Tools:**
- **filesystem**: Read code files, navigate directory structure
  - Rationale: Essential for code inspection
  - Install command: Built-in (no installation required)

**RECOMMENDED Tools:**
- **git**: Access commit history, blame information, branch analysis
  - Rationale: Understanding code evolution aids comprehension
  - Alternative: Manual inspection only
  - Install command: `npx @modelcontextprotocol/server-git`

- **github**: Search for similar patterns, API documentation, issue history
  - Rationale: External context helps understand design decisions
  - Alternative: Manual web search
  - Install command: `npx @modelcontextprotocol/server-github`

**OPTIONAL Tools:**
- **browser**: Access web documentation, Stack Overflow, language specs
  - Use case: Researching unfamiliar libraries or patterns
  - Install command: Browser extension MCP

### Tool Verification

The executor will verify tool availability during initialisation (Section 1.11) as a safety check.

---

## Definitions

- **goal**: Document mysterious code feature completely for maintenance and extension
- **task[n]**: Discrete archaeology objectives (survey, behaviour analysis, dependency mapping, documentation)
- **step[m]**: Concrete inspection or documentation actions within each task
- **backup[p]**: Alternative analysis method when primary approach fails
- **critical_flag**: Boolean indicating whether step failure blocks archaeology goal
- **mode**: Execution mode per step - `collaborative` (initial setup), then `dynamic` (autonomous with escalation)
- **progress.json**: Structured log tracking archaeology execution and outcomes
- **target_code**: The mysterious code feature/module being analysed
- **feature_boundary**: Where the feature starts/ends (entry points, interfaces)

---

## Components

Feature archaeology requires access to:
- **Source code files:** The mysterious feature and surrounding context
- **Version control history:** Git logs, commits, blame information
- **Existing documentation:** READMEs, comments, API docs (if any)
- **Test files:** Unit tests, integration tests (if they exist)
- **Configuration files:** Settings, environment variables affecting behaviour
- **Related features:** Code that calls or is called by target feature
- **Project context:** Overall architecture, tech stack, design patterns

---

## Constraints

- MUST use actual code behaviour as source of truth (not assumptions)
- MUST verify all hypotheses with code inspection
- MUST document ALL discovered entry points
- MUST NOT modify code during analysis (read-only archaeology)
- SHOULD use git history to understand evolution
- SHOULD identify original author if possible
- MAY use external research (Stack Overflow, docs) for library understanding

---

## Tasks

### Task [1]: Initial Code Survey

**Purpose:** Map the feature's structure and identify key components.

#### Step [1.1]: Identify entry points (public APIs, main functions)
- **Primary method:** Search for public functions, exported classes, API routes
- **Expected output:** List of 3-10 entry points with signatures and file locations
- **Critical:** true
- **Backup [1]:** If no clear public API, identify all function definitions and filter by naming conventions (public vs private)

#### Step [1.2]: Map data structures and types
- **Primary method:** Extract class definitions, type annotations, interfaces, structs
- **Expected output:** Data model diagram or structured list showing relationships
- **Critical:** true
- **Backup [1]:** If no explicit types, infer from usage patterns and variable names

#### Step [1.3]: Extract comments and documentation fragments
- **Primary method:** Collect all docstrings, comments, README sections mentioning feature
- **Expected output:** Consolidated documentation fragments with source references
- **Critical:** false
- **Backup [1]:** If no comments exist, note this absence (indicates documentation need)

---

### Task [2]: Behaviour Analysis

**Purpose:** Understand what the feature actually does at runtime.

#### Step [2.1]: Trace execution paths for common scenarios
- **Primary method:** Follow code flow from entry point through typical use cases
- **Expected output:** Flowchart or step-by-step execution description for 2-3 scenarios
- **Critical:** true
- **Backup [1]:** If code is too complex, identify branching points and document decision logic

#### Step [2.2]: Identify side effects (I/O, state changes, external calls)
- **Primary method:** Search for file operations, database calls, API requests, global state modifications
- **Expected output:** List of all side effects with triggering conditions
- **Critical:** true
- **Backup [1]:** If side effects are implicit, trace function calls to external libraries and document

#### Step [2.3]: Document error handling patterns
- **Primary method:** Identify try-catch blocks, error returns, validation checks
- **Expected output:** Error taxonomy (what can go wrong, how it's handled)
- **Critical:** false
- **Backup [1]:** If no explicit error handling, document failure modes and risks

---

### Task [3]: Dependency Mapping

**Purpose:** Understand what this feature depends on and what depends on it.

#### Step [3.1]: Identify upstream dependencies (what this code relies on)
- **Primary method:** Extract imports, requires, includes; categorize as internal vs external
- **Expected output:** Dependency tree showing all upstream dependencies with purposes
- **Critical:** true
- **Backup [1]:** If dependencies are complex, focus on direct dependencies only, defer transitive

#### Step [3.2]: Identify downstream dependents (what relies on this code)
- **Primary method:** Search codebase for imports/calls to this feature
- **Expected output:** List of all calling code with usage context
- **Critical:** true
- **Backup [1]:** Use git grep or IDE search if code navigation is unavailable

#### Step [3.3]: Map external integrations (APIs, databases, services)
- **Primary method:** Identify all external system connections (databases, APIs, message queues)
- **Expected output:** Integration diagram showing external touchpoints
- **Critical:** true
- **Backup [1]:** If integrations are hidden, trace network/IO calls to infer connections

---

### Task [4]: Documentation Generation

**Purpose:** Create comprehensive, maintainable documentation.

#### Step [4.1]: Write "What It Does" summary (plain English)
- **Primary method:** Synthesize analysis into 3-5 paragraph explanation suitable for non-experts
- **Expected output:** Feature overview document including purpose, key concepts, architecture
- **Critical:** true
- **Backup [1]:** If feature is complex, write multiple summaries at different technical levels

#### Step [4.2]: Create usage examples
- **Primary method:** Write 3-5 code examples showing common use cases with expected outputs
- **Expected output:** Runnable example snippets with comments explaining each step
- **Critical:** true
- **Backup [1]:** If examples can't run standalone, provide pseudocode with detailed explanations

#### Step [4.3]: Document known issues and workarounds
- **Primary method:** Review git issues, TODO comments, bug reports; extract known problems
- **Expected output:** Issues list with workarounds and links to related tickets/PRs
- **Critical:** false
- **Backup [1]:** If no formal issue tracking, search comments for "FIXME", "HACK", "TODO"

#### Step [4.4]: Create integration guide
- **Primary method:** Document how to safely integrate with or modify this feature
- **Expected output:** Integration guide with do's/don'ts, gotchas, and extension points
- **Critical:** false
- **Backup [1]:** If extension points aren't clear, document current integration patterns from dependents

---

## Bridging (Markdown ↔ TOML)

**All task and step IDs in this markdown MUST match corresponding entries in `parameters_WTF.toml`.**

**Cross-References:**
- Task [1] → `tasks[id=1]` in TOML
- Step [1.1] → `tasks[id=1].steps[id=1]` in TOML
- Task [2] → `tasks[id=2]` in TOML
- Constraints → `constraints.*` in TOML

**Validation:** `exe_WTF.md` Section 1.8 verifies this synchronisation before execution.

---

## Instructions for LLM Executor

### Execution Philosophy

WTF is a **code archaeology** TOOLSPEC. Your goal is understanding, not modification:

1. **Read-only operation:** Never modify the target code during analysis
2. **Evidence-based:** All claims must be verified against actual code
3. **Comprehensive coverage:** Document ALL entry points, not just obvious ones
4. **Plain English:** Write for humans who will maintain this code, not other LLMs
5. **Visual aids:** Diagrams are worth a thousand words for complex flows

### Target Code Specification

**Before starting Task 1, you MUST establish:**
- Which file(s) or module(s) are being analysed?
- What are the boundaries of the "feature"?
- Are there test files or documentation to reference?

**If unclear, escalate to collaborative mode and ask:**
```
[WTF SETUP - Target Identification]
I need to identify the mysterious code you want documented.

Please provide:
1. File path(s) or module name(s)
2. Specific function/class if known
3. Context: Why is this mysterious? What are you trying to do?

Example: "lib/auth/session_manager.py - not sure how session expiry works"
```

### Analysis Depth

Balance thoroughness with practicality:
- **Small feature (<500 lines):** Deep analysis, every path documented
- **Medium feature (500-2000 lines):** Focus on main paths, note areas requiring deeper investigation
- **Large feature (>2000 lines):** Modular approach, document subsystems separately

### Verification Requirements

**After each task, verify:**
- Task [1]: Can you explain the feature's structure to a colleague?
- Task [2]: Can you predict the feature's behaviour for new inputs?
- Task [3]: Do you know what would break if this feature changed?
- Task [4]: Could someone maintain this feature using your documentation?

**If NO to any:** Return to that task with more thorough analysis before proceeding.

### Documentation Quality Standards

**Your documentation MUST:**
- Use concrete examples (not "handles data" but "transforms JSON user objects to database rows")
- Include actual code snippets where helpful
- Highlight surprising or non-obvious behaviour
- Warn about gotchas and footguns
- Provide rationale where evident ("uses X because Y wasn't available in version Z")

**Your documentation MUST NOT:**
- Guess or assume behaviour without verification
- Use jargon without definition
- Omit error cases or edge conditions
- Leave integration points vague

---

**End of WTF SPEC**

*This TOOLSPEC implements Lia Workflow Specs' "wtf.toml" concept within SPEC Engine's constitutional framework. For related troubleshooting workflows, see Troubleshoot_SPEC.md and Forensic_SPEC.md.*
