# Spec System Design Philosophy

**Version:** 1.3  
**Date:** 3 November 2025  
**Purpose:** Comprehensive guide to the design principles, rationale, and best practices underlying the Spec system

---

## Table of Contents

1. [Core Philosophy](#core-philosophy)
2. [Architectural Principles](#architectural-principles)
3. [Hierarchical Structure](#hierarchical-structure)
4. [Dual-File Architecture](#dual-file-architecture)
5. [Execution Modes](#execution-modes)
6. [Robustness Mechanisms](#robustness-mechanisms)
7. [Bridging & Synchronisation](#bridging--synchronisation)
8. [Error Propagation](#error-propagation)
9. [LLM Interpretation Principles](#llm-interpretation-principles)
10. [Quality Standards](#quality-standards)
11. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
12. [Design Evolution](#design-evolution)

---

## Core Philosophy

### The North Star Principle

**Every Spec must have exactly one goal**, which serves as the "North Star" guiding all decisions, tasks, steps, and backups. This singular focus prevents scope creep, maintains clarity, and ensures all elements serve a unified purpose.

**Rationale:** LLMs perform better when they have a clear, unambiguous objective. Multiple goals create competing priorities and dilute focus.

### Goal-Directed Behaviour

All components of a Spec must explicitly and demonstrably contribute to achieving the stated goal. This is not merely aspirational—it must be verifiable during validation (Section 1.8 of exe_[descriptor].md).

**Implementation:** 
- Every task must be a discrete objective that advances the goal
- Every step must be a concrete action that completes the task
- Every backup must provide an alternative path to step completion

---

## Architectural Principles

### 1. Separation of Concerns

The Spec system separates three distinct concerns into three files:

| File | Concern | Audience |
|------|---------|----------|
| `spec_[descriptor].md` | **Intent & Reasoning** | Human + LLM (semantic understanding) |
| `parameters_[descriptor].toml` | **Structure & Configuration** | Machine + LLM (deterministic parsing) |
| `exe_[descriptor].md` | **Execution Logic** | LLM executor (orchestration) |

**Rationale:** This separation allows humans to reason about intent (Markdown), machines to validate structure (TOML), and executors to operate deterministically (exe controller).

### 2. Explicit Over Implicit

The system favours explicit declarations over implicit assumptions:

- **Explicit cross-references** between files (e.g., "See `constraints.max_latency` in parameters_[descriptor].toml")
- **Explicit expected outputs** for every step
- **Explicit backup methods** rather than generic "retry" logic
- **Explicit mode declarations** per step

**Rationale:** LLMs benefit from explicitness. Implicit relationships create ambiguity, leading to incorrect inferences or "lazy" behaviour.

### 3. Validation Before Execution

The system enforces comprehensive validation before any execution begins (exe_[descriptor].md Section 1.1-1.10):

1. File presence checks
2. Parse both Markdown and TOML
3. Validate goal (one and only one)
4. Validate tasks, steps, and backups
5. Verify bridging (Markdown ↔ TOML synchronisation)
6. Check referential integrity

**Rationale:** Early validation prevents downstream errors and ensures the Spec is well-formed before committing resources to execution.

### 4. Progressive Disclosure

Information is presented in layers of increasing detail:

- **Goal** (highest level, most abstract)
  - **Task** (discrete objective)
    - **Step** (concrete action)
      - **Backup** (alternative method)
        - **Expected Output** (verification criteria)

**Rationale:** This mirrors how humans reason about complex tasks and provides LLMs with appropriate context at each decision point.

---

## Hierarchical Structure

### Goal → Task → Step → Backup (Simple Structure)

The fundamental hierarchy for straightforward goals:

```
GOAL (singular, North Star)
  ├── TASK [1] (discrete objective derived from goal)
  │     ├── STEP [1.1] (concrete action)
  │     │     ├── Primary Method
  │     │     ├── Backup [1] (alternative reasoning path)
  │     │     └── Backup [2] (second alternative)
  │     ├── STEP [1.2] (concrete action)
  │     └── STEP [1.3] (concrete action)
  ├── TASK [2] (discrete objective)
  │     └── ...
  └── TASK [3] (discrete objective)
        └── ...
```

### Goal → SPECLet → Task → Step → Backup (Complex Structure)

**Evolution (v1.3):** For complex multi-phase goals, an intermediate SPECLet layer was added:

```
GOAL (singular, North Star)
  ├── SPECLet [platform_foundation] (cohesive work package)
  │     ├── TASK [1] (discrete objective)
  │     │     ├── STEP [1.1] (concrete action)
  │     │     └── STEP [1.2] (concrete action)
  │     └── TASK [2] (discrete objective)
  │           └── ...
  ├── SPECLet [feature_development] (depends on platform_foundation)
  │     ├── TASK [3] (discrete objective)
  │     └── TASK [4] (discrete objective)
  └── SPECLet [testing] (depends on feature_development)
        └── TASK [5] (discrete objective)
```

**Rationale for SPECLets:**

The original 3-layer hierarchy (Goal → Task → Step) works excellently for straightforward goals but proved insufficient for complex multi-phase projects. Real-world feedback indicated:

1. **Context Management:** Goals requiring >5 tasks exceeded optimal cognitive chunking
2. **Dependency Tracking:** No explicit way to express "Task Group A must complete before Task Group B"
3. **Parallel Execution:** Independent work packages couldn't be identified for concurrent execution
4. **Forced Workarounds:** Users were creating multiple SPECs for a single goal (violating Article I)

**Design Decision:** Add an **optional** SPECLet layer that:
- Groups related tasks into cohesive work packages (2-5 tasks per SPECLet)
- Explicitly declares dependencies between work packages (`depends_on` arrays)
- Enables parallel execution of independent work packages
- Maintains backwards compatibility (simple goals skip SPECLets entirely)

**When to use SPECLets:**
- Multi-phase projects (setup → development → testing)
- Task count would exceed 5 without grouping
- Clear dependency chains between phases
- Parallel execution opportunities

**When to skip SPECLets:**
- Straightforward goals with 2-5 sequential tasks
- Single-phase work
- Simple analysis or reporting tasks

**Key principle:** SPECLets are complexity management, not complexity introduction. Most goals don't need them.

### Preventing Conflation

**Common mistake:** Treating tasks as steps, SPECLets as tasks, or goals as tasks.

**Correct understanding:**
- **Goal** = outcome you want to achieve ("Build Design Thinking Dashboard")
- **SPECLet** (optional) = cohesive work package ("Platform Foundation", "Discovery Stage")
- **Task** = objective that advances the goal or SPECLet ("Set up database schema")
- **Step** = action that completes the task ("Create users table with authentication fields")
- **Backup** = alternative method for step ("Use SQLite if PostgreSQL unavailable")

**Verification:** Every SPECLet must clearly group related tasks. Every task must clearly state how it advances the goal. Every step must clearly state how it completes the task.

---

## Dual-File Architecture

### Why Both Markdown and TOML?

The dual-file architecture emerged from deep analysis of how LLMs interpret different data formats:

#### Markdown: Semantic Richness

**Strengths:**
- Natural language embedding allows contextual reasoning
- Hierarchical headings create semantic scaffolding
- LLMs trained extensively on Markdown documentation
- Supports narrative coherence and intent expression
- Flexible for evolving specifications

**Use Cases:**
- Expressing "why" and "what" (goals, rationale, context)
- Describing task logic and step relationships
- Providing examples and clarifications
- Human review and collaborative editing

#### TOML: Structural Determinism

**Strengths:**
- Key-value structure enforces schema compliance
- Machine-parseable for validation and verification
- Explicit delineation of elements (no ambiguity)
- Supports numerical constraints and configuration
- Enables automated integrity checks

**Use Cases:**
- Encoding "how" numerically (max_retries, thresholds)
- Defining structural relationships (task/step IDs)
- Specifying constraints and configuration
- Enabling bridging verification

### The Hybrid Advantage

**Together, they provide:**
1. **Semantic bandwidth** (Markdown) + **Structural integrity** (TOML)
2. **Human readability** (Markdown) + **Machine verifiability** (TOML)
3. **Flexible iteration** (Markdown) + **Deterministic execution** (TOML)

**Critical insight:** LLMs interpret Markdown as *conversation* and TOML as *configuration*. Using both in tandem leverages the strengths of each mode.

---

## Execution Modes

### Three-Mode System

The system supports three execution modes, evaluated **per step** (not per task).

**Default Mode:** Dynamic (recommended for most use cases)

**Mode Selection:** At the start of execution, the exe controller prompts the user to confirm or change the mode:
- "Continue with Dynamic mode (recommended)?"
- "Switch to Silent mode (fully autonomous)?"
- "Switch to Collaborative mode (pause at each step)?"

#### 1. Silent Mode
**Behaviour:** Fully autonomous execution without human intervention.

**Use when:**
- Steps are well-defined and highly predictable
- Backup methods provide comprehensive alternatives
- Workflow is low-risk and failures are tolerable
- No critical decision points requiring human judgement

**Characteristics:**
- Never prompts for human input except on unrecoverable errors
- Relies entirely on backup methods and retry logic
- Only escalates when all methods exhausted on critical steps

**Escalation triggers:**
- Critical step failure after all backups exhausted
- Unrecoverable error (no backups defined for critical step)

#### 2. Collaborative Mode
**Behaviour:** Pause execution and request human guidance at every step or decision point.

**Use when:**
- High-stakes workflow requiring constant oversight
- Learning mode (training the spec with human feedback)
- Steps are exploratory or require frequent judgement calls
- Building confidence in a new spec before autonomous execution

**Characteristics:**
- Pauses before or after each step for human confirmation
- Presents options and recommendations for human selection
- Learns from human decisions to improve future runs

**Logging requirements:**
- All prompts and human responses
- Decision rationale captured
- Timestamp and step context
- Pattern tracking for future automation

#### 3. Dynamic Mode (Default, Recommended)
**Behaviour:** Intelligently switch between Silent and Collaborative based on runtime conditions.

**Why it's the default:**
- Balances autonomy with safety
- Escalates only when genuinely needed
- Learns failure patterns and adapts
- Maximises efficiency while preventing catastrophic failures

**Robustness of Dynamic Mode Decision-Making:**

Dynamic mode employs a multi-signal approach to determine when escalation is necessary:

**Signal 1: Consecutive Failure Pattern**
- Tracks sliding window of last N steps (default N=5)
- If 3+ consecutive failures detected: escalate
- Resets counter on successful step completion
- **Robustness:** Prevents accumulation of minor failures into major breakdown

**Signal 2: Backup Depletion Pattern**
- Tracks frequency of backup usage across steps
- If same backup used successfully 3+ times: suggests strategy review
- If backups consistently failing: escalates for reassessment
- **Robustness:** Detects when primary methods are systematically inadequate

**Signal 3: Confidence Degradation**
- Compares actual outputs against expected outputs over time
- Tracks verification check pass/fail rates
- Monitors retry frequency per step over sequence
- If output quality trending downward: escalate
- **Robustness:** Early detection of quality deterioration before critical failure

**Signal 4: Critical Failure Threshold**
- Absolute threshold from `error_propagation.failure_threshold` (TOML)
- Default: 3 consecutive failures triggers escalation
- Configurable per-spec based on risk tolerance
- **Robustness:** Guaranteed escalation point regardless of other signals

**Signal 5: Method Exhaustion**
- If critical step fails after primary + all backups attempted: immediate escalate
- Non-critical step failures logged but don't trigger escalation
- **Robustness:** Respects critical_flag settings and doesn't over-escalate

**Decision Algorithm:**
```
FOR each step:
  READ prior_steps FROM progress.json
  CALCULATE consecutive_failures
  CALCULATE backup_depletion_score
  CALCULATE confidence_score
  
  IF (consecutive_failures >= 3) THEN
    escalate_reason = "consecutive_failure_pattern"
    SWITCH_TO collaborative_mode
  
  ELSE IF (backup_depletion_detected) THEN
    escalate_reason = "backup_inadequacy_pattern"
    SWITCH_TO collaborative_mode
  
  ELSE IF (confidence_score < threshold) THEN
    escalate_reason = "output_quality_degradation"
    SWITCH_TO collaborative_mode
  
  ELSE IF (failure_count >= error_propagation.failure_threshold) THEN
    escalate_reason = "absolute_threshold_breach"
    SWITCH_TO collaborative_mode
  
  ELSE IF (critical_step_failed AND all_methods_exhausted) THEN
    escalate_reason = "critical_failure_unrecoverable"
    SWITCH_TO collaborative_mode
  
  ELSE
    CONTINUE in silent_mode
  
  LOG escalation_decision WITH reason AND signals
```

**Robustness Rating: High**
- Multiple independent signals prevent false positives/negatives
- Configurable thresholds allow tuning per-spec
- Absolute safety valve (critical failure threshold)
- Sliding window approach prevents overreaction to isolated failures
- Pattern detection identifies systemic vs transient issues

**Fallback behaviour:** If dynamic mode decision logic encounters errors, defaults to collaborative mode (safe failure mode).

### Per-Step Mode Evaluation

**Critical principle:** Mode is evaluated and logged **per step**, not per task.

**Rationale:** Tasks are composite objectives. Some steps within a task may be critical while others are not. Per-step evaluation provides finer control and better logging granularity.

**Task-level mode determination:** The mode for a task is determined by the highest severity of any step within it (most critical step determines overall task mode).

### Optional: Research-Enabled Tasks

**When to Use:**  
Knowledge-intensive tasks that require gathering external information (e.g., "Research distributed consensus protocols", "Review current PDF extraction tools").

**When NOT to Use:**  
Execution-intensive tasks that implement or transform existing information (e.g., "Refactor authentication module", "Optimise database queries").

**Configuration:**
```toml
[[tasks]]
id = 1
description = "Research current PDF extraction methods"
research_enabled = true
research_sources = ["web_search", "documentation", "github_repos"]
```

**How It Works:**
- Research tasks prioritise information gathering over implementation
- Steps focus on finding, evaluating, and synthesising information
- Expected outputs are typically summaries, comparisons, or recommendations
- Research results feed into subsequent implementation tasks

**Example Research Task:**
```markdown
### Task [1]: Research PDF Extraction Tools
**Research Enabled:** true

- **Step [1]:** Survey available PDF processing libraries
  - **Primary method:** Search documentation and GitHub
  - **Expected output:** List of 5-10 libraries with brief descriptions

- **Step [2]:** Compare library capabilities
  - **Primary method:** Create comparison matrix (features, performance, license)
  - **Expected output:** Markdown table comparing libraries

- **Step [3]:** Recommend optimal tool chain
  - **Primary method:** Analyse use cases and select 2-3 libraries for different scenarios
  - **Expected output:** Recommendation with rationale
```

**Integration with Implementation:**
Research task results become inputs for subsequent implementation tasks. The spec should show this dependency explicitly.

### Optional: User Stories

**When to Include:**  
User-facing features or workflows where connecting technical tasks to user intent adds valuable context.

**When to Skip:**  
- Technical refactoring (no user-visible changes)
- Infrastructure or optimisation work
- Internal tooling with no external users
- Backend-only modifications

**Format:**
```
As a [role], I want [capability] so that [benefit]
```

**Example:**
```markdown
## User Stories (Optional)

- As a developer, I want documentation automatically extracted so I can understand module behaviour
- As a QA engineer, I want edge cases identified so testing is comprehensive
- As a maintainer, I want bugs traced to specific functions so fixes are targeted
```

**How User Stories Help:**
1. **Design Guidance:** Clarify what "good" looks like from user perspective
2. **Scope Definition:** Make explicit what's in/out of scope
3. **Acceptance Criteria:** Define success conditions
4. **Task Prioritisation:** Focus on user-impacting tasks first

**Integration with Goal Hierarchy:**
```
USER STORIES (optional layer)
     ↓
  GOAL (singular, North Star)
     ↓
  TASKS (discrete objectives)
     ↓
  STEPS (concrete actions)
```

User stories sit above the goal, providing the "why" for the "what" (goal) and "how" (tasks/steps).

**Important:** User stories are **not** substitutes for goals. They provide additional context but the goal remains the primary North Star.

### Optional: Clarification Steps

**Philosophy:** Rather than adding a separate clarification phase before spec generation (which conflicts with autonomous execution), handle ambiguity through explicit clarification steps when needed.

**Two Approaches:**

#### Approach 1: Pre-Flight Clarification (Commander)
If goal description is inherently ambiguous during spec generation, Commander flags it immediately:

```markdown
## Commander Detects Ambiguity

**Goal Provided:** "Improve the authentication system"

**Ambiguities Detected:**
- What aspect of authentication? (performance, security, usability)
- What constitutes "improvement"? (measurable criteria unclear)
- Scope: entire system or specific components?

**Action:** Request clarification before generating spec files.
```

**When to Use:** During spec generation, if Commander cannot reasonably decompose goal into tasks.

#### Approach 2: Clarification as Step (Within Spec)
If goal inherently requires human input during execution, make clarification an explicit collaborative step:

```toml
[[tasks]]
id = 1
description = "Gather requirements"

  [[tasks.steps]]
  id = 1
  description = "Identify ambiguous requirements in project description"
  expected_output = "List of questions requiring human clarification"
  critical_flag = true
  mode = "collaborative"  # Force human input
  
  [[tasks.steps]]
  id = 2
  description = "Document clarified requirements"
  expected_output = "Structured requirements document with resolved ambiguities"
  critical_flag = true
  mode = "silent"  # Can proceed autonomously with clarified inputs
```

**When to Use:** When goal explicitly requires human judgment or domain knowledge that LLM cannot infer.

**Example Clarification Step:**
```markdown
### Task [1]: Gather Requirements

- **Step [1]:** Identify unclear requirements
  - **Primary method:** Analyse project description for ambiguous terms, undefined scope, or missing criteria
  - **Expected output:** List of 5-10 specific questions requiring human input
  - **Critical:** true
  - **Mode:** collaborative (forces pause for human response)
  
- **Step [2]:** Document resolved requirements
  - **Primary method:** Structure human responses into clear, testable requirements
  - **Expected output:** Requirements document with specific, measurable criteria
  - **Critical:** true
  - **Mode:** silent
```

**Key Principle:** Clarification steps preserve autonomous execution philosophy. The LLM identifies what it doesn't know (Step 1), pauses for human input (collaborative mode), then continues autonomously with clarified information (Step 2+).

**Contrast with GitHub Spec Kit:** Spec Kit has separate clarification workflows because it's human-supervised throughout. SPECS is autonomous by default, so clarification must be an explicit, mode-controlled step within the execution flow.

---

## Robustness Mechanisms

### 1. Critical Flags

**Purpose:** Identify steps whose failure requires escalation.

**Behaviour:**
- `critical_flag = true`: Failure triggers collaborative mode (after backup exhaustion)
- `critical_flag = false`: Failure logged as warning, execution continues

**Guidelines:**
- Mark steps as critical if failure blocks the goal
- Mark steps as non-critical if they're "nice to have" but not essential
- Typically 40-60% of steps should be critical (not all, not none)

### 2. Backup Methods

**Philosophy:** Backups are **alternative reasoning paths**, not simple retries.

**Bad backup:** "Try the same method again"  
**Good backup:** "If documentation incomplete, inspect source code directly"

**Types of Backups:**

#### A. Cognitive Alternative Backups
Alternative reasoning approaches or methods:
- Use different analysis technique
- Try alternative data source
- Apply different framework or model

#### B. Tool-Based Backups
User-provided scripts, tools, or external programs:
- Multiple PDF-to-Markdown converters (e.g., try pypdf2, then pdfplumber, then pdf2image+OCR)
- Different linters or analysis tools
- Alternative API endpoints or services
- Fallback toolchains or processing pipelines

**Structure:**
```toml
[[tasks.steps.backups]]
id = 1
description = "[Alternative cognitive approach or tool]"
trigger_condition = "primary_failure"
tool_path = "[Optional: path to script/tool]"  # For tool-based backups
tool_args = "[Optional: arguments to pass]"    # For tool-based backups
execution_method = "cognitive|tool|script"      # Specifies backup type
```

**Example: Multiple PDF Processing Tools**
```toml
[[tasks.steps]]
id = 1
description = "Convert PDF document to Markdown"
expected_output = "Markdown file with preserved formatting"

[[tasks.steps.backups]]
id = 1
description = "Use pypdf2 for text extraction"
tool_path = "scripts/convert_pdf_pypdf2.py"
tool_args = "--preserve-layout"
execution_method = "tool"
trigger_condition = "primary_failure"

[[tasks.steps.backups]]
id = 2
description = "Use pdfplumber if pypdf2 fails"
tool_path = "scripts/convert_pdf_pdfplumber.py"
tool_args = "--tables-extract"
execution_method = "tool"
trigger_condition = "backup_1_failure"

[[tasks.steps.backups]]
id = 3
description = "Use OCR as final fallback if text extraction fails"
tool_path = "scripts/convert_pdf_ocr.py"
tool_args = "--tesseract --lang=eng"
execution_method = "tool"
trigger_condition = "backup_2_failure"
```

**Execution order:**
1. Attempt primary method (LLM cognitive approach or default tool)
2. If failure, attempt backup[1] (first alternative: cognitive or tool)
3. If backup[1] fails, attempt backup[2] (second alternative)
4. If backup[2] fails, attempt backup[3] (if defined)
5. If all fail and critical=true, escalate to collaborative mode

**Tool-Based Backup Execution:**
- exe controller checks `execution_method` field
- If `execution_method = "tool"` or `"script"`:
  - Execute tool/script specified in `tool_path`
  - Pass arguments from `tool_args`
  - Capture output and errors
  - Validate against `expected_output`
  - Log tool execution result
- If `execution_method = "cognitive"`:
  - LLM attempts alternative reasoning approach
  - No external tool invocation

**Logging:** Each backup attempt is logged separately with:
- backup_id
- execution_method (cognitive/tool/script)
- tool_path (if applicable)
- trigger_condition
- outcome (success/failure)
- error_message (if tool/script failed)
- timestamp

**Rationale for Tool-Based Backups:**
- Different tools have different strengths (e.g., pypdf2 fast but limited, OCR slow but comprehensive)
- User may have domain-specific tools or proprietary scripts
- Tool chains can be tried sequentially without LLM hallucination risk
- Deterministic tool behaviour complements probabilistic LLM reasoning

### 3. Thoroughness Enforcement

**Principle:** The LLM must exhaust all available methods before escalating or giving up.

**Implementation:**
- Backups must be attempted in sequence
- Retries must reach max_retries threshold
- Escalation only after genuine exhaustion of options

**Rationale:** Prevents "lazy" LLM behaviour where it gives up prematurely. Forces exploration of alternatives.

### 4. Retry Logic

**Per-step retry configuration:**
```toml
max_retries = 2  # Primary method retry count
```

**Retry vs Backup distinction:**
- **Retry:** Attempt same method again (for transient failures)
- **Backup:** Attempt different method (for method inadequacy)

**Execution flow:**
1. Primary method (with max_retries)
2. If still failing, attempt backups
3. Each backup also respects its own retry logic if defined

### 5. Research-Enabled Mode

**Purpose:** Allows LLM to access external knowledge sources when internal knowledge is insufficient.

**When to Enable:**

`research_enabled = true` should be set at the **task level** for knowledge-intensive tasks where:

1. **Domain-Specific Knowledge Required:**
   - Task requires current information beyond LLM training data
   - Task deals with rapidly evolving domains (technology, regulations, APIs)
   - Task requires specialist knowledge LLM may not possess

2. **Verification Against External Sources:**
   - Task involves fact-checking or validation
   - Task requires comparing against current documentation
   - Task needs confirmation of API specifications or library versions

3. **Discovery Tasks:**
   - Finding current best practices
   - Identifying available tools or libraries
   - Exploring solution approaches in unfamiliar domains

**When NOT to Enable:**

- Tasks where LLM's existing knowledge is sufficient
- Tasks that are primarily implementation-focused (writing code based on known patterns)
- Tasks involving reasoning or analysis (not fact retrieval)
- When speed/cost optimization is prioritized over thoroughness

**Implementation:**

In `parameters_[descriptor].toml`:
```toml
[[tasks]]
id = 1
description = "Research current authentication best practices for healthcare APIs"
research_enabled = true  # Enables web search, documentation access
research_sources = ["web_search", "documentation", "technical_specs"]
```

In `spec_[descriptor].md`:
```markdown
### Task [1]: Research module functionality
**TOML Reference:** `tasks[id=1]` in parameters_[descriptor].toml  
**Research Enabled:** true (requires current API documentation)
```

**Available Research Sources:**

When `research_enabled = true`, the LLM executor may use:
- `web_search`: General web searches for current information
- `documentation`: Official documentation sites (if URLs provided)
- `technical_specs`: API specifications, RFC documents
- `github_repos`: Repository searches for implementation examples
- `academic`: Research papers (via arXiv, PubMed, etc., if MCP tools available)

**Execution Behaviour:**

When research is enabled, the executor:
1. Attempts primary method using existing knowledge first
2. If confidence is low or verification needed, triggers research phase:
   - Formulates specific search queries
   - Executes searches via available MCP tools
   - Synthesizes findings
   - Validates information against multiple sources
3. Proceeds with step using researched information
4. Logs research queries and sources used

**Logging:**

Research activities are logged in `progress_[descriptor].json`:
```json
{
  "task_id": "1",
  "step_id": "1",
  "research_performed": true,
  "research_queries": [
    "FHIR authentication OAuth 2.0 best practices 2025",
    "healthcare API security standards HIPAA"
  ],
  "sources_consulted": [
    "https://www.hl7.org/fhir/security.html",
    "https://oauth.net/2/"
  ],
  "confidence_improvement": "medium_to_high"
}
```

**Cost Considerations:**

Research-enabled mode:
- Increases execution time (external API calls)
- May incur additional costs (web search APIs, MCP services)
- Generates more token usage (processing search results)

**Best Practice:** Enable selectively for tasks where research genuinely adds value, not as a default.

**Constitutional Note:** Research-enabled mode is a **task-level feature**, not a step-level feature. This prevents excessive research overhead and maintains focus on execution efficiency.

---

## Bridging & Synchronisation

### The Bridging Concept

**Bridging** ensures perfect alignment between spec_[descriptor].md and parameters_[descriptor].toml.

### Bridging Requirements

1. **ID Synchronisation:** Every task and step ID must match exactly between files
2. **Structural Correspondence:** Task/step hierarchy must be identical
3. **Explicit Cross-References:** Markdown should reference TOML keys directly
4. **Backup Alignment:** Backups in Markdown must be represented in TOML

### Cross-Reference Examples

**In spec_[descriptor].md:**
```markdown
### Task [1]: Research module functionality
**TOML Reference:** `tasks[id=1]` in parameters_[descriptor].toml

- Verification: Must satisfy `constraints.coverage_required = true` in TOML
- Constraint: Maximum latency: See `constraints.latency_max_ms` in TOML
```

**In parameters_[descriptor].toml:**
```toml
[[tasks]]
id = 1  # Corresponds to Task [1] in spec.md
description = "Research module functionality"
```

### Bridging Verification (Section 1.8)

The exe_[descriptor].md controller performs comprehensive bridging verification:

1. Confirm every task in Markdown exists in TOML
2. Confirm every step in Markdown has TOML entry
3. Verify IDs match exactly
4. Check sequence order consistency
5. Generate detailed report of discrepancies

**Outcome:** Execution halts if critical bridging errors detected.

### Why Bridging Matters

**Without bridging:** Files can drift apart, causing:
- Execution of steps not defined in Markdown
- Skipping of steps defined in Markdown but not TOML
- Incorrect parameter application
- Human-LLM misalignment

**With bridging:** Perfect synchronisation ensures human intent (Markdown) is executed exactly as specified (TOML).

---

## Error Propagation

### Concept

**Error Propagation** means downstream steps read and respond to prior step failures.

### Implementation (Section 2.1)

Before executing each step:
1. **Read progress_[descriptor].json** for prior outcomes
2. Check if any prior critical steps failed
3. Evaluate impact on current step
4. Make propagation decision based on strategy

### Propagation Strategies

Defined in `error_propagation.propagation_strategy` (TOML):

#### 1. halt_on_critical (Strictest)
**Behaviour:** Immediately stop all execution when a critical step fails. No further steps are attempted.

**When it occurs:**
- Critical step fails (critical_flag = true)
- All backups exhausted
- Immediate, non-negotiable halt

**After halt:**
- Execution completely stopped
- Writes partial completion summary to progress.json
- If in Silent mode: switches to Collaborative for human intervention
- If in Collaborative mode: already paused, requests resolution
- If in Dynamic mode: escalates to Collaborative

**Use case:** High-stakes workflows where downstream steps cannot proceed without upstream success (e.g., authentication must succeed before any API calls).

**Difference from collaborative_review:** No option to continue—execution is blocked.

#### 2. continue_and_log (Most Permissive)
**Behaviour:** Proceed to next step despite prior failure, but log warning and flag dependency concern.

**When it occurs:**
- Non-critical step fails (critical_flag = false)
- Or configured explicitly for risk-tolerant workflows

**Characteristics:**
- Execution continues uninterrupted
- Downstream steps informed of upstream failure
- Warnings accumulate in progress.json
- Partial outputs still usable

**Use case:** Best-effort workflows where partial completion is valuable (e.g., documentation generation where some sections can fail).

**Difference from halt_on_critical:** Execution continues regardless of failure.

#### 3. collaborative_review (Balanced)
**Behaviour:** Pause execution and request human decision about how to proceed.

**When it occurs:**
- Critical step fails (critical_flag = true)
- All backups exhausted
- But unlike halt_on_critical, human can choose response

**Human options presented:**
1. **"Skip and continue"**: Mark step as failed, proceed with downstream steps (like continue_and_log)
2. **"Retry with modification"**: Human provides adjusted parameters/approach, re-attempt step
3. **"Provide manual output"**: Human supplies the expected output, mark step as complete
4. **"Halt execution"**: Stop completely (like halt_on_critical)
5. **"Switch to different backup"**: Human suggests alternative method not in original backups

**Use case:** Workflows requiring human judgement on failure impact (e.g., code review where human decides if linter failure is blocking).

**Key Differences Between halt_on_critical and collaborative_review:**

| Aspect | halt_on_critical | collaborative_review |
|--------|------------------|---------------------|
| **Execution** | Stops immediately | Pauses for decision |
| **Human choice** | No options | 5 response options |
| **Can continue?** | No, must restart | Yes, if human chooses |
| **Auto-resume** | Never | Possible after human input |
| **Logging** | Marks as "halted" | Marks as "paused_for_review" |
| **Use in Silent mode** | Forces switch to Collaborative | Forces switch to Collaborative |
| **Use in Dynamic mode** | Escalates to Collaborative, then halts | Escalates to Collaborative, then offers choices |

**Recommended strategy by execution mode:**
- **Silent mode:** Use halt_on_critical (failures are unrecoverable without human)
- **Collaborative mode:** Use collaborative_review (already in human-in-loop)
- **Dynamic mode (default):** Use collaborative_review (allows intelligent human decisions)

**Mode dependency:** The strategy interacts with execution mode:
- If mode = Silent and strategy = collaborative_review: forces mode switch to Collaborative
- If mode = Collaborative and strategy = halt_on_critical: still allows human to decide (mode overrides strategy strictness)
- If mode = Dynamic and strategy = collaborative_review: escalates on critical failure patterns, presents options

### Dependency Tracking

**Explicit dependencies:**
- Step references output of prior step
- Task depends on completion of prior task

**Implicit dependencies:**
- Critical step failure may affect downstream logic
- Configuration values from failed steps may be invalid

**Logging:** All propagation decisions are logged with:
- prior_step_dependencies (array of step IDs)
- error_propagation_decision (halt/continue/review)
- impact_assessment (how failure affects current step)

### Failure Threshold

**Configuration:**
```toml
[error_propagation]
failure_threshold = 3  # Escalate after N consecutive failures
```

**Behaviour:** If consecutive failures reach threshold, escalate to collaborative mode regardless of individual step criticality.

**Rationale:** Persistent failure patterns indicate systemic issues requiring human review, even if individual steps are marked non-critical.

---

## LLM Interpretation Principles

### How LLMs "See" Specs

#### Markdown Interpretation

LLMs treat Markdown as **semantic context**:
- Headings create hierarchical attention structures
- Prose activates discursive reasoning modes
- Examples provide pattern matching templates
- Natural language enables intent inference

**Implication:** Use Markdown to explain "why" and provide context.

#### TOML Interpretation

LLMs treat TOML as **configuration data**:
- Key-value pairs parsed deterministically
- Numbers and strings as literal values
- Structure as schema to follow
- Less semantic inference, more rule adherence

**Implication:** Use TOML to encode "how" and enforce constraints.

### Prompt Scaffolding

The Spec system provides **cognitive scaffolding** for LLMs:

1. **Goal** anchors all reasoning
2. **Tasks** break down the goal into manageable units
3. **Steps** provide concrete action points
4. **Backups** offer pre-planned alternatives
5. **Logging** creates memory across steps

**Effect:** LLMs operate more deterministically and reliably within this scaffolding.

### Preventing Lazy Behaviour

**Techniques:**
1. **Explicit expected outputs:** Forces LLM to produce specific results
2. **Verification checks:** Output compared against expectations
3. **Backup requirements:** Can't skip to collaborative mode without trying alternatives
4. **Validation gates:** Execution blocked if validation fails

### Encouraging Thoroughness

**Techniques:**
1. **Max retries enforcement:** Must attempt retries before giving up
2. **Sequential backup execution:** Must try all backups before escalating
3. **Failure threshold tracking:** Pattern detection prevents single-point surrenders
4. **Logging all attempts:** Accountability for method exhaustion

---

## Quality Standards

### Internal Consistency

**Definition:** All elements within and across files must align logically and structurally.

**Checks:**
- Task IDs match between Markdown and TOML
- Step IDs match between Markdown and TOML
- Backup references are valid
- Constraints referenced exist in definitions
- Expected outputs are defined for all steps

### Goal Alignment

**Definition:** Every task and step must demonstrably serve the goal.

**Validation questions:**
- Does this task advance the goal?
- Does this step complete the task?
- Could the goal be achieved without this element?

**If "no" to any question:** Remove or revise the element.

### Syntactic Validity

**Requirements:**
- Markdown must render correctly
- TOML must parse without errors
- JSON logging structure must be valid
- Cross-references must resolve

**Automated checks:** TOML parsers, Markdown linters, JSON validators.

### Human Readability

**Principle:** Despite being designed for LLMs, specs must remain human-readable.

**Guidelines:**
- Use clear, plain language
- Avoid excessive jargon
- Structure information hierarchically
- Provide examples where helpful
- Keep individual steps atomic and understandable

### Explicitness

**Principle:** Prefer explicit declarations over implicit assumptions.

**Examples:**
- ✅ "Expected output: List of 5 function names"
- ❌ "Expected output: Function names"
- ✅ "Backup [1]: Use linter tool X if manual inspection fails"
- ❌ "Backup [1]: Try alternative method"

---

## Anti-Patterns to Avoid

### 1. Goal Conflation

**Anti-pattern:** Defining multiple goals in one Spec.

**Problem:** Creates competing priorities, dilutes focus, complicates validation.

**Solution:** One Spec = One Goal. Create separate Specs for different goals.

### 2. Task-Step Confusion

**Anti-pattern:** Treating tasks as steps or vice versa.

**Problem:** Breaks hierarchical reasoning, makes verification impossible.

**Solution:** Tasks are objectives; steps are actions. Maintain clear distinction.

### 3. Backup-as-Retry

**Anti-pattern:** Defining backups as "try the same thing again".

**Problem:** Doesn't provide alternative reasoning path, wastes LLM effort.

**Solution:** Backups must be genuinely different approaches or methods.

### 4. Vague Expected Outputs

**Anti-pattern:** "Expected output: Results"

**Problem:** LLM cannot verify success, no accountability for output quality.

**Solution:** Be specific: "Expected output: Markdown table with 3 columns: function name, parameter count, return type"

### 5. Over-Criticality

**Anti-pattern:** Marking all steps as `critical_flag = true`.

**Problem:** Everything becomes an escalation, collaborative mode overused, workflow grinds to halt.

**Solution:** Reserve critical flags for genuinely goal-blocking steps.

### 6. Under-Criticality

**Anti-pattern:** Marking no steps as critical.

**Problem:** Failures accumulate silently, goal never achieved, no escalation when needed.

**Solution:** Identify genuinely critical steps (typically 40-60% of total).

### 7. Missing Bridging References

**Anti-pattern:** Markdown and TOML don't cross-reference each other.

**Problem:** Files drift apart, execution doesn't match intent, humans and LLMs misaligned.

**Solution:** Explicit cross-references in Markdown to TOML keys.

### 8. Insufficient Logging

**Anti-pattern:** Logging only success/failure status.

**Problem:** Can't debug, can't audit, can't learn from failures.

**Solution:** Log method_used, backup_attempts, error_propagation_decisions, constraint_status, etc.

### 9. Ignoring Error Propagation

**Anti-pattern:** Each step executes in isolation, unaware of prior failures.

**Problem:** Downstream steps attempt to use invalid outputs from failed steps.

**Solution:** Enable error_propagation, read progress.json before each step.

### 10. Generic Descriptions

**Anti-pattern:** "[Insert task description here]" left unchanged.

**Problem:** Spec is unusable, provides no guidance.

**Solution:** Replace all placeholders with specific, actionable descriptions.

---

## Design Evolution

### From Initial Concept to Current System

The Spec system evolved through multiple iterations:

#### Phase 1: Single-File Markdown
**Concept:** Everything in one Markdown file.  
**Problem:** Lack of machine-verifiable structure, LLM interpretation inconsistency.

#### Phase 2: Dual-File Introduction (Markdown + TOML)
**Concept:** Separate intent (Markdown) from structure (TOML).  
**Breakthrough:** Recognised LLMs interpret formats differently, leveraging both improves reliability.

#### Phase 3: Bridging Mechanism
**Concept:** Explicit synchronisation between files.  
**Innovation:** Cross-references and validation prevent drift.

#### Phase 4: Mode System
**Concept:** Silent, Collaborative, and Dynamic modes.  
**Insight:** Per-step mode evaluation provides finer control than task-level modes.

#### Phase 5: Error Propagation
**Concept:** Steps read prior results and adjust behaviour.  
**Sophistication:** Dependency tracking, propagation strategies, failure thresholds.

#### Phase 6: Backup-as-Alternative-Reasoning
**Concept:** Backups are cognitive alternatives, not retries.  
**Maturity:** Step-level backup structure, trigger conditions, sequential execution.

### Key Learnings

1. **Explicitness beats implicitness:** LLMs perform better with explicit instructions.
2. **Validation prevents problems:** Early, comprehensive validation catches issues before execution.
3. **Hierarchical structure aids reasoning:** Goal → Task → Step → Backup mirrors human cognition.
4. **Dual-file leverages LLM strengths:** Markdown for semantics, TOML for structure.
5. **Per-step granularity matters:** Step-level evaluation provides fine-grained control.
6. **Thoroughness must be enforced:** LLMs need structural encouragement to exhaust alternatives.
7. **Error propagation is essential:** Downstream steps must be aware of upstream failures.

### Design Principles Discovered Through Degradation

When LLM models degraded during ChatGPT development, these elements were lost:
- Sophisticated bridging verification logic
- Comprehensive validation checks
- Mode escalation sophistication
- Error propagation patterns
- Meta-cognitive scaffolding for self-correction

**Implication:** These elements are most valuable and must be preserved rigorously in templates.

---

## Using This Philosophy

### For Spec Authors

When creating a new Spec:
1. Start with a **singular, clear goal**
2. Decompose into **2-5 tasks** that collectively achieve the goal
3. Break each task into **1-5 concrete steps**
4. Define **0-2 backups** per step (alternative reasoning paths)
5. Add **explicit TOML cross-references** in Markdown
6. Ensure **task/step IDs match** between files
7. Define **expected outputs** for every step
8. Mark **critical steps** appropriately (40-60% of total)
9. Configure **error propagation** if steps have dependencies
10. **Validate thoroughly** before execution

### For LLM Executors

When executing a Spec:
1. **Validate before executing** (Section 1.1-1.10)
2. **Read progress.json** before each step (error propagation)
3. **Attempt primary method** first
4. **Try all backups** if primary fails
5. **Log comprehensively** (method_used, backup_attempts, etc.)
6. **Escalate appropriately** (collaborative mode when genuinely blocked)
7. **Track consecutive failures** (for dynamic mode)
8. **Verify outputs** against expected_output
9. **Check constraints** after each step
10. **Write final summary** on completion

### For System Designers

When extending the Spec system:
1. **Preserve the hierarchy:** Goal → Task → Step → Backup
2. **Maintain dual-file advantage:** Don't collapse into single format
3. **Enforce bridging:** New features must respect Markdown ↔ TOML sync
4. **Enhance logging:** More granular is better than less
5. **Keep validation rigorous:** Don't weaken pre-flight checks
6. **Respect per-step evaluation:** Don't move to task-level or goal-level modes
7. **Extend thoughtfully:** New features should align with core philosophy

---

## Conclusion

The Spec system is designed to evoke **goal-driven, agentic behaviour in LLMs** through:

- **Clear hierarchy:** Goal → Task → Step → Backup
- **Dual-file architecture:** Markdown (intent) + TOML (structure)
- **Bridging synchronisation:** Explicit alignment between files
- **Execution modes:** Silent, Collaborative, Dynamic (per-step evaluation)
- **Robustness mechanisms:** Critical flags, backups, thoroughness enforcement
- **Error propagation:** Downstream awareness of upstream failures
- **Comprehensive validation:** Early detection of issues
- **Detailed logging:** Auditability and learning

**Core principle:** Explicitness, validation, and cognitive scaffolding enable LLMs to execute complex, multi-step workflows reliably and deterministically.

**Design goal:** Not to restrict LLMs, but to **guide them** toward successful goal achievement through structured reasoning and fallback mechanisms.

---

**End of Design Philosophy Document**

*This document should be read in conjunction with the template files (Spec_template.md, parameters_template.toml, exe_template.md) and the Commander specification (Spec_Commander.md).*

**Maintenance:** Update this document when design principles evolve or new patterns emerge.

**Version History:**
- v1.0 (2025-11-02): Initial comprehensive philosophy document

