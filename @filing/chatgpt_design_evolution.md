# ChatGPT Spec Development - Design Evolution Reference

**Date Saved:** 2 November 2025  
**Purpose:** Archive of high-value design ideas and strategic philosophy from ChatGPT development sessions

## Source
Original conversation: `c:\Users\Fab2\Desktop\AI\Specs\chat\chatgpt_dev.md`

## Context
This document captures the iterative development of a dual-file specification system (Markdown + TOML) designed to evoke goal-driven agentic behaviour in LLMs. The system evolved through multiple model deprecations, with significant design philosophy and implementation details developed across the conversation.

## Key Design Concepts Developed

### 1. Hybrid Dual-File Architecture
- **Markdown** for semantic richness, intent, and reasoning context
- **TOML** for deterministic parameters, constraints, and machine-readable structure
- **Bridging mechanism** to maintain synchronisation between files

### 2. Hierarchical Structure
- **Goal** (singular, North Star) → **Tasks** (objectives) → **Steps** (concrete actions) → **Backups** (alternative methods)
- Clear definitional boundaries prevent conflation

### 3. Execution Modes
- **Silent mode**: Autonomous execution, only flags critical failures
- **Collaborative mode**: Pauses for human input at decision points
- **Dynamic mode**: Adaptive switching based on failure patterns
- Mode evaluation occurs **per step**, not per task

### 4. Robustness Mechanisms
- **Critical flags**: Identify steps whose failure requires escalation
- **Backup methods**: Alternative reasoning paths when primary methods fail
- **Retry logic**: Attempt backups before escalating to collaborative mode
- **Thoroughness enforcement**: LLM must attempt alternatives before giving up

### 5. Progress Tracking & Verification
- **progress.json**: Structured logging of execution, retries, mode switches
- **Bridging verification**: Cross-file validation of task/step IDs
- **Error propagation**: Downstream steps read prior results to inform execution

### 6. File Organisation
- **[descriptor] convention**: All files postpended with descriptor (e.g., `_research`)
- **Folder structure**: `[root]/Specs/[descriptor]/`
- **File relationships**: Explicit cross-references between spec.md, parameters.toml, and exe.md

### 7. Meta-Specification Layer
- **Commander files**: Meta-instructions for generating and executing specs
- **Preparation phase**: How to construct the dual-file spec
- **Production phase**: How to interpret and execute the spec

## Design Philosophy

### LLM Interpretation Principles
1. **Semantic bandwidth**: Markdown carries intent; TOML carries structure
2. **Contextual reasoning**: LLMs treat Markdown as narrative; TOML as configuration
3. **Cognitive grounding**: Each file "knows" about the others through explicit references
4. **Traceability**: Meta sections and progress logs enable context reconstruction

### Validation Approach
1. **One goal only**: Prevents scope creep and maintains focus
2. **Typically 2-5 tasks**: Soft guidance, expandable if justified
3. **1-5 steps per task**: Atomic, actionable units
4. **0-2 backups per step**: Alternative methods without overwhelming complexity

### Quality Standards
- Internal consistency across all files
- Every element must serve the goal
- Syntactically valid and human-readable
- Explicit instructions (avoid vague placeholders)
- LLM-oriented tone (instructional, not descriptive)

## Evolution Notes

The system evolved from:
- Single-file specs → dual-file hybrid system
- Generic project workflows → refined agent-like command sets
- Task-focused → goal-directed with explicit task/step hierarchy
- Simple retries → sophisticated backup methods and mode escalation
- Basic logging → comprehensive progress tracking with error propagation

## Key Insights from Degradation

When LLM models degraded, the following were lost/compromised:
1. Sophisticated bridging verification logic
2. Comprehensive validation checks (detailed in exe.md initialization)
3. Mode escalation sophistication
4. Error propagation patterns between steps
5. Meta-cognitive scaffolding for LLM self-correction

These elements should be prioritised in template preservation and enhancement.

---

*This document serves as a reference for maintaining design integrity across future iterations.*



