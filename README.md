# Spec System: Goal-Driven Agentic Behaviour for LLMs

A structured framework for creating execution specifications that evoke reliable, goal-directed behaviour in Large Language Models.

---

## What is a Spec?

A **Spec** is a self-contained folder containing three coordinated files that work together to guide LLM execution:

```
/Specs/[descriptor]/
    ├── spec_[descriptor].md           # Human-readable intent & reasoning
    ├── parameters_[descriptor].toml   # Machine-readable structure & config
    ├── exe_[descriptor].md            # Execution controller & orchestration
    └── progress_[descriptor].json     # Runtime logging (created during execution)
```

Each Spec defines:
- **One goal** (North Star objective)
- **Multiple tasks** (discrete objectives advancing the goal)
- **Sequential steps** (concrete actions completing tasks)
- **Backup methods** (alternative approaches when primary methods fail)
- **Execution modes** (silent, collaborative, or dynamic)
- **Error propagation** (how failures affect downstream steps)

---

## Quick Start

### 1. Generate a New Spec

Use the Commander to generate a Spec from a goal description:

```
1. Open: commander_SPEC/Spec_Commander.md
2. Provide your goal/behaviour description
3. Commander generates all three files in /Specs/[descriptor]/
```

**Example goal:** "Conduct a literature review on decentralised mesh networking protocols"

**Resulting Spec:** `/Specs/research/` with spec_research.md, parameters_research.toml, exe_research.md

### 2. Execute the Spec

```
1. Open: /Specs/[descriptor]/exe_[descriptor].md
2. LLM reads and executes according to the controller logic
3. Progress tracked in progress_[descriptor].json
```

### 3. Review Results

Check `progress_[descriptor].json` for:
- Completed tasks and steps
- Backup methods used
- Mode switches
- Error propagation events
- Final summary

---

## Core Concepts

### Goal → Task → Step → Backup Hierarchy

```
GOAL (singular, North Star)
  ├── TASK [1] (discrete objective)
  │     ├── STEP [1.1] (concrete action)
  │     │     ├── Primary Method
  │     │     ├── Backup [1] (alternative approach)
  │     │     └── Backup [2] (second alternative)
  │     └── STEP [1.2]
  ├── TASK [2]
  └── TASK [3]
```

**Every element must serve the goal.** This prevents scope creep and ensures focused execution.

### Dual-File Architecture

**Why both Markdown and TOML?**

| File | Purpose | LLM Interpretation |
|------|---------|-------------------|
| **spec.md** | Intent, reasoning, context | Semantic understanding (conversation mode) |
| **parameters.toml** | Structure, configuration | Deterministic parsing (configuration mode) |

**Together:** Semantic richness + Structural integrity = Reliable execution

### Execution Modes

**Default: Dynamic Mode (Recommended)**

Balances autonomy with safety using multi-signal decision-making:

| Mode | Behaviour | When to Use |
|------|-----------|-------------|
| **Dynamic** | Autonomous with intelligent escalation | Most workflows (default) |
| **Silent** | Fully autonomous, minimal interruption | Well-defined, low-risk workflows |
| **Collaborative** | Pause at each critical decision | High-stakes or learning workflows |

At runtime, you'll be prompted to confirm or change the mode.

### Backup Methods

**Two types of backups:**

#### 1. Cognitive Backups
Alternative reasoning approaches by the LLM:
- "If documentation incomplete, inspect source code directly"
- "Try alternative analysis framework"

#### 2. Tool-Based Backups
User-provided scripts, programs, or tool chains:
- Multiple PDF converters (pypdf2 → pdfplumber → OCR)
- Different linters or analysis tools
- Alternative API endpoints

**Example:**
```toml
[[tasks.steps.backups]]
id = 1
description = "Use pypdf2 for PDF conversion"
execution_method = "tool"
tool_path = "scripts/convert_pdf_pypdf2.py"
tool_args = "--preserve-layout"
trigger_condition = "primary_failure"
```

### Error Propagation

Downstream steps read prior step results and adapt behaviour.

**Three strategies:**

1. **halt_on_critical** - Stop immediately on critical failure
2. **continue_and_log** - Proceed despite failures, log warnings
3. **collaborative_review** - Pause and request human decision (default for dynamic mode)

**Configuration:**
```toml
[error_propagation]
enabled = true
propagation_strategy = "collaborative_review"
failure_threshold = 3  # Escalate after N consecutive failures
```

---

## Project Structure

```
/Specs/
    ├── README.md                       # This file
    ├── _templates/                     # Template files for new Specs
    │   ├── Spec_template.md
    │   ├── parameters_template.toml
    │   ├── exe_template.md
    │   └── DESIGN_PHILOSOPHY.md        # Comprehensive design rationale
    ├── commander_SPEC/
    │   └── Spec_Commander.md           # Spec generation controller
    ├── _filing/                        # Reference documents
    │   └── chatgpt_design_evolution.md
    └── [descriptor]/                   # Individual Specs
        ├── spec_[descriptor].md
        ├── parameters_[descriptor].toml
        ├── exe_[descriptor].md
        └── progress_[descriptor].json
```

---

## Key Files Explained

### Spec_template.md

Human-readable specification template showing:
- Goal definition
- Task breakdown with TOML cross-references
- Step structure with primary methods and backups
- Expected outputs and verification criteria
- Bridging examples (Markdown ↔ TOML synchronisation)

**Key sections:**
- Definitions (goal, task, step, backup, critical_flag, mode)
- Components and Constraints
- Task examples with full structure
- Bridging requirements
- Instructions for LLM

### parameters_template.toml

Machine-readable configuration template containing:
- Metadata and file relationships
- Execution mode configuration (default: dynamic)
- Goal description
- Tasks array with steps and backups
- Error propagation settings
- Logging and verification configuration
- Progress tracking fields

**Key sections:**
```toml
[execution]
default_mode = "dynamic"

[error_propagation]
propagation_strategy = "collaborative_review"

[[tasks.steps.backups]]
execution_method = "cognitive|tool|script"
```

### exe_template.md

Execution controller template defining:
- Comprehensive validation (10 validation steps before execution)
- Mode selection (user prompted at runtime)
- Execution flow with error propagation
- Backup selection logic
- Dynamic mode decision algorithm
- Verification layers
- Enhanced logging

**Critical sections:**
- 1.1-1.10: Initialization and Validation
- 1.2a: User Mode Selection
- 2.1: Pre-Step Error Propagation Check
- 2.5: Backup Method Selection
- 3: Mode Control with Dynamic Mode robustness details

### DESIGN_PHILOSOPHY.md

Comprehensive design document (750+ lines) covering:
- Core philosophy (North Star principle)
- Architectural principles
- Execution mode definitions and robustness analysis
- Backup method types and examples
- Error propagation strategies with mode dependency
- LLM interpretation principles
- Quality standards
- Anti-patterns to avoid
- Design evolution history

**Read this document before creating your first Spec.**

### Spec_Commander.md

Meta-specification for generating new Specs. Instructs LLMs on:
- Reading design philosophy first
- Goal interpretation
- File generation from templates
- Content guidelines (2-5 tasks, 1-5 steps per task)
- Alignment checks
- Quality standards

**Usage:** Provide a goal description, Commander generates complete Spec.

---

## Creating a New Spec

### Step-by-Step Process

1. **Read Design Philosophy**
   ```
   Open: _templates/DESIGN_PHILOSOPHY.md
   Understand: Core principles, modes, backups, error propagation
   ```

2. **Define Your Goal**
   - One clear, singular objective
   - Specific enough to be actionable
   - Broad enough to decompose into multiple tasks
   - Example: "Generate comprehensive API documentation from source code"

3. **Use Commander to Generate Spec**
   ```
   Open: commander_SPEC/Spec_Commander.md
   Provide: Your goal description
   Commander creates: /Specs/[descriptor]/ with all three files
   ```

4. **Review Generated Files**
   - Check goal is singular and clear
   - Verify tasks advance the goal
   - Ensure steps are concrete and actionable
   - Confirm backups provide genuine alternatives
   - Validate Markdown ↔ TOML synchronisation

5. **Customise if Needed**
   - Add tool-based backups if you have specific scripts
   - Adjust critical_flag settings (40-60% of steps should be critical)
   - Configure error_propagation strategy for your use case
   - Add constraints or components specific to your domain

6. **Execute**
   ```
   Open: /Specs/[descriptor]/exe_[descriptor].md
   Follow: Controller instructions
   Select: Execution mode when prompted (default: dynamic)
   ```

7. **Monitor Progress**
   ```
   Review: progress_[descriptor].json during execution
   Track: Step completions, backup usage, mode switches
   ```

8. **Review Results**
   ```
   Check: Final summary in progress.json
   Verify: Goal achievement
   Learn: Which backups were useful, where failures occurred
   ```

---

## Execution Mode Decision Guide

### When to Use Dynamic Mode (Default)

**Characteristics:**
- Runs autonomously most of the time
- Escalates intelligently based on 5 signals
- Balances efficiency with safety

**Use for:**
- Most workflows
- New Specs you're testing
- Workflows with some uncertainty
- When you want intelligent escalation

**Robustness:** High - uses multiple independent signals to prevent false positives/negatives

### When to Use Silent Mode

**Characteristics:**
- Fully autonomous
- Never prompts except on unrecoverable errors
- Only escalates when all methods exhausted

**Use for:**
- Well-tested Specs with proven reliability
- Low-risk workflows
- Workflows with comprehensive backup coverage
- Batch processing

**Warning:** No safety net - ensure backups are comprehensive

### When to Use Collaborative Mode

**Characteristics:**
- Pauses at each critical decision
- Requests human input frequently
- Learns from human decisions

**Use for:**
- High-stakes workflows
- Training new Specs
- Exploratory work
- Building confidence before autonomous execution

**Note:** Time-intensive but provides maximum oversight

---

## Best Practices

### Goal Definition
- One goal per Spec (no exceptions)
- Clear, explicit, singular objective
- Verifiable outcome
- Example: "Produce a code review report" (not "improve code quality")

### Task Breakdown
- 2-5 tasks per Spec (typical)
- Each task is a discrete objective
- Tasks execute sequentially (no parallelism)
- Every task must advance the goal

### Step Design
- 1-5 steps per task (typical)
- Steps are atomic, actionable units
- Define expected output for every step
- 40-60% of steps should be critical
- Clear verification criteria

### Backup Strategy
- 0-2 backups per step
- Backups are genuine alternatives, not retries
- Critical steps should have at least one backup
- Consider tool-based backups for deterministic tasks
- Test tool-based backups before adding to Spec

### Bridging
- Every task/step ID must match between Markdown and TOML
- Use explicit cross-references: "See `constraints.x` in TOML"
- Validate synchronisation before execution
- Keep descriptions consistent across files

### Logging
- Log comprehensively (method_used, backup_attempts, error_propagation_decisions)
- Review progress.json regularly
- Learn from failures and backup usage patterns
- Use logs to refine future Specs

---

## Troubleshooting

### "Bridging validation failed"

**Cause:** Mismatch between spec.md and parameters.toml

**Fix:**
1. Check task IDs match exactly
2. Check step IDs match within each task
3. Verify backup references exist in both files
4. Ensure constraint references are valid

### "All backups exhausted, escalating"

**Cause:** Primary method and all backups failed

**If expected:**
- Review backup methods for inadequacy
- Add more comprehensive backups
- Consider tool-based alternatives

**If unexpected:**
- Check if step definition is ambiguous
- Verify expected outputs are realistic
- Review logs for pattern in failures

### "Consecutive failure threshold reached"

**Cause:** 3+ consecutive step failures (dynamic mode)

**Action:**
- Review recent step definitions for quality
- Check if constraints are too strict
- Consider if goal decomposition needs revision
- Switch to collaborative mode to diagnose

### "Mode switch not logged"

**Cause:** Execution may not be following exe controller logic

**Fix:**
- Verify exe_[descriptor].md is being used
- Check progress.json structure is valid
- Ensure mode changes trigger logging code

---

## Advanced Features

### Custom Failure Thresholds

Adjust when dynamic mode escalates:

```toml
[error_propagation]
failure_threshold = 5  # More permissive (default: 3)
```

### Tool Chain Backups

Sequential tool fallbacks:

```toml
[[tasks.steps.backups]]
id = 1
execution_method = "tool"
tool_path = "tools/fast_converter.py"

[[tasks.steps.backups]]
id = 2
execution_method = "tool"
tool_path = "tools/robust_converter.py"

[[tasks.steps.backups]]
id = 3
execution_method = "tool"
tool_path = "tools/slow_but_comprehensive_converter.py"
```

### Resumable Execution

If execution halts, resume from progress.json:

```
1. Check progress.json for last completed step
2. Modify exe_[descriptor].md to skip completed tasks
3. Re-run from interruption point
```

### Spec Archiving

Preserve completed Specs:

```
/Specs/[descriptor]/archive_[date]/
    ├── spec_[descriptor].md
    ├── parameters_[descriptor].toml
    ├── exe_[descriptor].md
    └── progress_[descriptor].json
```

---

## Anti-Patterns to Avoid

1. **Multiple goals in one Spec**
   - Creates competing priorities
   - Solution: One Spec per goal

2. **Vague expected outputs**
   - "Expected output: Results"
   - Solution: Be specific: "Markdown table with 3 columns: name, count, status"

3. **All steps marked critical**
   - Causes excessive escalation
   - Solution: Reserve critical for genuinely goal-blocking steps

4. **Backups that are just retries**
   - "Try the same thing again"
   - Solution: Genuine alternatives: "If X fails, try Y approach"

5. **Missing bridging references**
   - Files drift apart
   - Solution: Explicit cross-references between Markdown and TOML

6. **Ignoring error propagation**
   - Downstream steps unaware of failures
   - Solution: Enable error_propagation, read progress.json

---

## FAQ

**Q: Can I run multiple Specs simultaneously?**
A: Yes, each Spec is independent. Run in separate processes.

**Q: Can tasks execute in parallel?**
A: No, tasks execute sequentially by design. This ensures error propagation and dependency tracking work correctly.

**Q: Can I modify a Spec during execution?**
A: Not recommended. Finish execution, review results, then modify for next run.

**Q: What happens if I abort execution?**
A: Progress.json contains partial results. Review for last completed step. Can resume manually.

**Q: Can I use this system with different LLMs?**
A: Yes, the Spec format is LLM-agnostic. However, behaviour may vary based on LLM capabilities.

**Q: How do I test tool-based backups?**
A: Test tools/scripts independently before adding to Spec. Verify they handle expected inputs and produce expected outputs.

**Q: What if my goal needs more than 5 tasks?**
A: You can expand, but consider if your goal might actually be multiple goals. Breaking into separate Specs may be cleaner.

**Q: Can I nest Specs (Spec calls another Spec)?**
A: Not directly supported. However, you can create a task that invokes another Spec's exe controller.

---

## Version History

- **v1.0** (2025-11-02): Initial release with comprehensive templates, design philosophy, and dynamic mode as default

---

## Contributing

When extending this system:

1. **Preserve the hierarchy** - Goal → Task → Step → Backup
2. **Maintain dual-file advantage** - Keep Markdown and TOML separate
3. **Enforce bridging** - New features must respect synchronisation
4. **Enhance logging** - More granular is better
5. **Keep validation rigorous** - Don't weaken pre-flight checks
6. **Document in DESIGN_PHILOSOPHY.md** - Explain rationale for changes

---

## Support

For issues, questions, or suggestions:

1. Review DESIGN_PHILOSOPHY.md for design rationale
2. Check templates for examples
3. Examine chatgpt_design_evolution.md for historical context
4. Review progress.json logs for debugging information

---

## License

This framework is designed to improve LLM reliability and goal-directed behaviour. Use freely, extend thoughtfully.

---

**Core Principle:** Explicitness, validation, and cognitive scaffolding enable LLMs to execute complex, multi-step workflows reliably and deterministically.

**Design Goal:** Not to restrict LLMs, but to guide them toward successful goal achievement through structured reasoning and fallback mechanisms.

**North Star:** Every element must serve the goal.

---

*For comprehensive design rationale, read: `commander_SPEC/DESIGN_PHILOSOPHY.md`*
*For Spec generation: `commander_SPEC/Spec_Commander.md`*

