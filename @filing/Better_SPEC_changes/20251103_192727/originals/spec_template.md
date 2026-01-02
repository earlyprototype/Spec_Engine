# Spec Template (Goal-First)

**Version:** 1.0  
**Last Updated:** 2025-11-02  
**Purpose:** Human-readable specification template for goal-driven LLM execution

---

## Goal
[Insert single overarching goal here]

---

## Software Stack & Architecture

**MANDATORY for goals containing: "build", "create", "system", "application", "app", "develop"**

### Deployment Type
Select ONE:
- [ ] Web Application (browser-based)
- [ ] Desktop Application (installable exe/app)
- [ ] Command-line Tool (terminal-based, for technical users)
- [ ] Mobile Application
- [ ] API Service
- [ ] Library/Module (for developers)

### Technology Stack
- **Language:** [Python/JavaScript/TypeScript/Go/Rust/etc.]
- **Framework:** [Flask/Django/Electron/Qt/React/Next.js/etc.]
- **Database:** [SQLite/PostgreSQL/MongoDB/None/etc.]
- **UI Library:** [PyQt/Tkinter/HTML+CSS/React/None/etc.]
- **Packaging:** [PyInstaller/Electron Builder/Docker/npm package/etc.]

### User Interface Requirements
- **Primary users:** [Who will use this system? Be specific: "developers", "shop volunteers", "medical staff"]
- **Interaction method:** [GUI buttons/CLI commands/Web browser/Touch screen/API calls]
- **Technical skill level:** [None/Basic/Advanced]
- **Accessibility requirements:** [Large buttons/Screen reader support/High contrast/Simple language/etc.]

### Deployment Requirements
- **Target environment:** [Windows 10+/macOS/Linux/Cloud/Docker/Browser/etc.]
- **Installation method:** [Double-click installer/Portable .exe/npm install/Docker compose/Web URL/etc.]
- **Configuration needed:** [API keys/Database credentials/Printer setup/None/etc.]
- **Startup process:** [Click desktop icon/Run command/Open URL/etc.]

---

## Definition of Complete

**MANDATORY: Define specific, measurable criteria for when this goal is ACHIEVED.**

What must exist and be verified:
- [ ] Primary deliverable (report, executable, test suite, documentation, etc.)
- [ ] Quality standards met (specific, measurable)
- [ ] Verification method defined (how to objectively confirm completion)

For build/create/system goals, see Software Stack section above.  
Validation logic in `exe_template.md` Section 6.4.

---

## MCP Toolset

### Installed Tools (Verified During SPEC Creation)

The following MCP servers were approved and installed during SPEC creation (Step 3a).

**REQUIRED Tools:**
{{#each mcp_tools.required}}
- **{{this.name}}**
  - Rationale: {{this.rationale}}
  - Install command: `{{this.install_command}}`
{{/each}}

**RECOMMENDED Tools:**
{{#each mcp_tools.recommended}}
- **{{this.name}}**
  - Rationale: {{this.rationale}}
  - Alternative: {{this.alternative}}
  - Install command: `{{this.install_command}}`
{{/each}}

**OPTIONAL Tools:**
{{#each mcp_tools.optional}}
- **{{this.name}}**
  - Use case: {{this.use_case}}
  - Install command: `{{this.install_command}}`
{{/each}}

### Tool Verification

The executor will verify tool availability during initialisation (Section 1.11) as a **safety check**.

These tools were installed during SPEC creation (Step 3a), so verification should pass automatically.

**If verification fails**, it indicates:
- MCP configuration changed since SPEC creation
- MCP client was not properly restarted after installation
- Installation was incomplete or tools were uninstalled

Refer to installation commands above if re-installation is needed.

---

**Example (populated):**

## MCP Toolset

### Installed Tools (Verified During SPEC Creation)

The following MCP servers were approved and installed during SPEC creation (Step 3a).

**REQUIRED Tools:**
- **postgres**
  - Rationale: Core database operations essential for data management goal
  - Install command: `npm install @modelcontextprotocol/server-postgres`

- **github**
  - Rationale: Version control and file operations required for code management
  - Install command: `npm install @modelcontextprotocol/server-github`

**RECOMMENDED Tools:**
- **playwright**
  - Rationale: Browser automation improves testing workflow efficiency
  - Alternative: Manual browser testing via UI
  - Install command: `npm install @modelcontextprotocol/server-playwright`

**OPTIONAL Tools:**
- **notion**
  - Use case: Documentation publishing if project uses Notion workspace
  - Install command: `npm install @modelcontextprotocol/server-notion`

### Tool Verification

The executor will verify tool availability during initialisation (Section 1.11) as a **safety check**.

These tools were installed during SPEC creation (Step 3a), so verification should pass automatically.

**If verification fails**, it indicates:
- MCP configuration changed since SPEC creation
- MCP client was not properly restarted after installation
- Installation was incomplete or tools were uninstalled

Refer to installation commands above if re-installation is needed.

---

## Definitions
- goal: The overarching objective the agent must achieve.
- task[n]: Discrete objectives derived from the goal. `[n]` denotes task number.
- step[m]: Concrete actions or reasoning sub-unit within a task. `[m]` denotes step number.
- backup[p]: Alternative method or reasoning path for step[m]. `[p]` denotes backup number.
- critical_flag: Boolean indicating whether a step is critical.
- mode: Execution mode per step[m]: `silent` or `collaborative`.
- progress.json: Structured log tracking execution, retries, outputs, and flags.

## Components
- Codebase  
- Test framework  
- Documentation sources

**Machine-Readable Components (Optional):**  
For specs that need to validate component references, define them in the `[components]` section of parameters_[descriptor].toml:
- `codebase = "Main source repository at /src"`
- `test_framework = "PyTest testing suite v7.0"`
- `api_endpoint = "Production API at https://api.example.com"`

This enables exe Section 1.9 to verify that steps only reference defined components.  

## Constraints
- All critical functionality must be tested  
- Steps must be goal-directed  
- Logging must be completed for every step

**Machine-Readable Constraints (Optional):**  
For automated validation of numeric/boolean constraints, define them in the `[constraints]` section of parameters_[descriptor].toml:
- `max_latency_ms = 200` (numeric threshold - exe controller can validate)
- `coverage_required = true` (boolean requirement - exe controller can check)
- `output_format = "markdown"` (string requirement - exe controller can verify)

**Freeform Constraints:**  
Narrative constraints can remain in Markdown only without TOML definition. Use machine-readable constraints when you need the exe controller to automatically validate thresholds.

**Bridging Note:** When using machine-readable constraints, reference them explicitly:  
Example: "Maximum latency: See `constraints.max_latency_ms` in parameters_[descriptor].toml (must be ≤ 200ms)"  

---

## User Stories (Optional)

**When to Use:** User-facing features or workflows where linking technical implementation to user intent provides valuable context.

**When to Skip:** Technical tasks with no direct user impact (e.g., refactoring, optimisation, infrastructure work).

User stories follow the format:
- As a [role], I want [capability] so that [benefit]

**Example:**
- As a developer, I want documentation automatically extracted so I can understand module behaviour without reading code
- As a QA engineer, I want edge cases identified so testing is comprehensive
- As a maintainer, I want bugs traced to functions so fixes are targeted

**Purpose:** User stories bridge abstract goals and technical tasks, providing design insights that guide task-level decisions.

---

## Clarification Steps (Optional)

**When to Use:** Goals that inherently require human judgment or domain knowledge that the LLM cannot infer.

**How to Implement:** Create an explicit collaborative step that pauses for human input:

```markdown
### Task [1]: Gather Requirements

- **Step [1]:** Identify ambiguous requirements
  - **Primary method:** Analyse goal description for undefined terms, unclear scope, missing criteria
  - **Expected output:** List of specific questions requiring human clarification
  - **Critical:** true
  - **Mode:** collaborative (pauses execution for human response)

- **Step [2]:** Document clarified requirements
  - **Primary method:** Structure human responses into testable requirements
  - **Expected output:** Requirements document with specific, measurable criteria
  - **Critical:** true
  - **Mode:** silent (proceeds autonomously with clarified inputs)
```

**Key Principle:** Clarification is a step within the spec, not a separate phase. This preserves autonomous execution while handling ambiguity explicitly.

---

## Goal Example

**Goal:** Perform a comprehensive review and testing of a software module.

### Task [1]: Research module functionality
**TOML Reference:** `tasks[id=1]` in parameters_[descriptor].toml  
**Research Enabled:** Optional (`research_enabled = true` for knowledge-intensive tasks)

- **Step [1]:** Extract specifications from documentation  
  - **Primary method:** Parse documentation files systematically  
  - **Backup [1]:** If documentation incomplete, inspect source code directly  
  - **Backup [2]:** If source unclear, reference similar module implementations  
  - **Expected output:** Structured summary of module functions and dependencies  
  - **Critical:** true  
  - **Mode:** silent  

- **Step [2]:** Analyse module dependencies and function signatures  
  - **Primary method:** Map import statements and function declarations  
  - **Expected output:** Dependency graph and signature list  
  - **Critical:** true  
  - **Mode:** silent  

- **Step [3]:** Summarise intended behaviour  
  - **Primary method:** Synthesise findings into coherent summary  
  - **Backup [1]:** If synthesis unclear, request collaborative review  
  - **Expected output:** Behaviour description document  
  - **Critical:** false  
  - **Mode:** silent  

- **Verification:** All functions documented or inferred; TOML constraint `coverage_required = true` satisfied  
- **Logging:** Append structured entry to progress_[descriptor].json for each step  

### Task [2]: Create automated tests
**TOML Reference:** `tasks[id=2]` in parameters_[descriptor].toml

- **Step [1]:** Identify core functions  
  - **Primary method:** Extract public API functions from module  
  - **Expected output:** List of functions requiring tests  
  - **Critical:** true  
  - **Mode:** silent  

- **Step [2]:** Determine edge cases  
  - **Primary method:** Analyse function parameters and boundary conditions  
  - **Backup [1]:** Reference previous modules for common edge case patterns  
  - **Expected output:** Edge case matrix  
  - **Critical:** true  
  - **Mode:** silent  

- **Step [3]:** Draft test scenarios  
  - **Primary method:** Create test case specifications for each function  
  - **Expected output:** Test scenario documentation  
  - **Critical:** false  
  - **Mode:** silent  

- **Step [4]:** Implement initial test suite  
  - **Primary method:** Write test code using project testing framework  
  - **Backup [1]:** If framework unclear, reference testing templates  
  - **Expected output:** Executable test suite  
  - **Critical:** true  
  - **Mode:** silent  

- **Verification:** Test coverage includes core and edge functions; meets `constraints.min_coverage` in TOML  
- **Logging:** Append structured entry to progress_[descriptor].json for each step  

### Task [3]: Debug and verify module behaviour
**TOML Reference:** `tasks[id=3]` in parameters_[descriptor].toml

- **Step [1]:** Run test suite and record failures  
  - **Primary method:** Execute test suite and capture failure logs  
  - **Expected output:** Failure report with stack traces  
  - **Critical:** true  
  - **Mode:** silent  

- **Step [2]:** Trace errors to specific functions  
  - **Primary method:** Analyse stack traces and debug logs  
  - **Backup [1]:** Use debugger for step-through analysis  
  - **Expected output:** Root cause identification  
  - **Critical:** true  
  - **Mode:** silent  

- **Step [3]:** Apply fixes  
  - **Primary method:** Implement corrections based on root cause  
  - **Expected output:** Modified source code  
  - **Critical:** true  
  - **Mode:** silent  

- **Step [4]:** Re-run tests and verify pass/fail status  
  - **Primary method:** Execute full test suite again  
  - **Backup [1]:** Manual verification if automated tests inconclusive  
  - **Expected output:** Test results showing all passes  
  - **Critical:** true  
  - **Mode:** silent  

- **Step [5]:** Document fixes and update test coverage  
  - **Primary method:** Update documentation with fix descriptions  
  - **Expected output:** Updated documentation and coverage report  
  - **Critical:** false  
  - **Mode:** silent  

- **Verification:** Test suite passes; meets `constraints.pass_rate = 100%` in TOML; documentation updated  
- **Logging:** Append structured entry to progress_[descriptor].json for each step  

### JSON Log Example
````json
{
  "task_id": "task1",
  "step_id": "step2",
  "attempt_number": 1,
  "method_used": "primary",
  "constraint_status": {
      "coverage": "pass",
      "alignment_with_goal": "pass"
  },
  "mode": "silent",
  "critical_flag": true,
  "timestamp": "2025-11-01T12:00Z"
}

---

## Bridging: Markdown ↔ TOML Synchronisation

This spec file (spec_[descriptor].md) must maintain perfect alignment with its companion file (parameters_[descriptor].toml).

**Bridging Requirements:**
1. Each task in this file must have a corresponding `[[tasks]]` entry in TOML with matching ID
2. Each step within a task must have a corresponding `[[tasks.steps]]` entry with matching ID
3. Each backup method must be referenced in TOML structure
4. Constraints and components should cross-reference TOML keys explicitly
5. Expected outputs in this file should match `expected_output` fields in TOML

**Example Cross-References:**
- "See `constraints.max_latency` in parameters_[descriptor].toml"
- "As defined in `tasks[id=2].steps[id=3]` in TOML"
- "Must satisfy TOML verification requirements"

The exe_[descriptor].md controller validates this synchronisation during initialisation (Section 1.8).

---

### Instructions for LLM
1. Start with the **goal** (singular, clear, North Star).  
2. Break the goal into **tasks `[n]`** (discrete objectives).  
3. For each task, define **steps `[m]`** needed to achieve it (concrete actions).  
4. Include **backup `[p]`** methods where appropriate (alternative reasoning paths, not just retries).  
5. Ensure **bridging alignment**: every task/step ID must match between this file and parameters_[descriptor].toml.  
6. Add explicit **TOML cross-references** for constraints and configuration values.  
7. Log each step in **progress_[descriptor].json**, including mode, retries, and critical flags.  
8. Verify outputs and constraints after each step.  
9. Read prior step results from progress.json before executing dependent steps (error propagation).  

