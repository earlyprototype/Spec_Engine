# SPECS System - Future Development Roadmap

**Version:** 1.0  
**Date:** 2 November 2025  
**Purpose:** Track potential future enhancements and experimental features

---

## Status Legend
- 🎯 **Planned:** Approved for development, design in progress
- 🔬 **Experimental:** Concept stage, needs validation
- 💭 **Idea:** Proposed, needs design work
- ✅ **Completed:** Implemented and merged
- ❌ **Rejected:** Evaluated but not proceeding

---

## Parallel Execution Support

**Status:** 🔬 Experimental  
**Complexity:** High  
**Priority:** Low (stretch goal)  
**Dependencies:** None (optional enhancement)

### Problem Statement

Currently, SPECS enforces **strictly sequential execution**:
- Task [1] completes fully before Task [2] begins
- Step [1.1] completes before Step [1.2] begins
- No concurrent execution of independent steps

**Limitation:** Steps that have no dependencies could theoretically run in parallel for faster execution.

**Example:**
```
Task 1: Analyse codebase
  Step 1.1: Analyse module A  (independent)
  Step 1.2: Analyse module B  (independent)
  Step 1.3: Analyse module C  (independent)
  Step 1.4: Synthesise findings (depends on 1.1, 1.2, 1.3)
```

Steps 1.1, 1.2, 1.3 could run in parallel, then 1.4 waits for all three.

### Proposed Solution

#### A. Dependency Declaration in TOML

```toml
[[tasks.steps]]
id = 1
description = "Analyse module A"
expected_output = "Analysis document for module A"
parallel_enabled = true
parallel_group = "analysis_group_1"
depends_on = []  # No dependencies

[[tasks.steps]]
id = 2
description = "Analyse module B"
expected_output = "Analysis document for module B"
parallel_enabled = true
parallel_group = "analysis_group_1"
depends_on = []  # No dependencies

[[tasks.steps]]
id = 3
description = "Analyse module C"
expected_output = "Analysis document for module C"
parallel_enabled = true
parallel_group = "analysis_group_1"
depends_on = []  # No dependencies

[[tasks.steps]]
id = 4
description = "Synthesise findings from modules A, B, C"
expected_output = "Combined analysis document"
parallel_enabled = false
depends_on = [1, 2, 3]  # Waits for steps 1, 2, 3 to complete
```

#### B. Parallel Execution Logic (exe_template enhancement)

```markdown
## 2. Execution Flow (Enhanced for Parallel Support)

For each **Task**:
  
  ### 2.0 Build Dependency Graph
  - Parse all steps and their `depends_on` arrays
  - Create dependency graph: which steps can run when
  - Identify parallel groups: steps with no dependencies in same group
  
  ### 2.1 Identify Parallel-Executable Steps
  - Steps with `parallel_enabled = true` AND `depends_on = []` can start immediately
  - Steps in same `parallel_group` can run concurrently
  - Steps with `depends_on = [...]` wait for dependencies
  
  ### 2.2 Spawn Parallel Executions
  - For each parallel group:
    - Spawn concurrent execution threads/processes
    - Each thread follows standard step execution (2.2-2.3)
    - Maintain separate progress logs per thread
  
  ### 2.3 Synchronisation Point
  - When dependent step encountered (e.g., step 4 depends on [1,2,3]):
    - Wait for all dependency steps to complete
    - Check success status of dependencies
    - Proceed only if dependencies succeeded (or handle failures per strategy)
  
  ### 2.4 Continue Sequential or Parallel
  - After synchronisation, continue with next step(s)
  - Can spawn new parallel group if dependencies satisfied
```

#### C. Progress Logging for Parallel Execution

```json
{
  "run_id": "20251102-143022",
  "descriptor": "research_parallel",
  "execution_mode": "parallel_enabled",
  
  "tasks": [
    {
      "task_id": "task1",
      "step_id": "step1",
      "parallel_group": "analysis_group_1",
      "thread_id": "thread_1",
      "status": "in_progress",
      "started_at": "2025-11-02T14:31:15Z"
    },
    {
      "task_id": "task1",
      "step_id": "step2",
      "parallel_group": "analysis_group_1",
      "thread_id": "thread_2",
      "status": "in_progress",
      "started_at": "2025-11-02T14:31:16Z"  // Started 1 second after step1
    },
    {
      "task_id": "task1",
      "step_id": "step3",
      "parallel_group": "analysis_group_1",
      "thread_id": "thread_3",
      "status": "in_progress",
      "started_at": "2025-11-02T14:31:17Z"  // Started 2 seconds after step1
    }
  ],
  
  "parallel_execution_summary": {
    "concurrent_steps": 3,
    "time_saved": "estimated 5.2 minutes",
    "synchronisation_points": 1
  }
}
```

### Design Challenges

#### 1. LLM Context Limitations
**Problem:** Most LLMs can't truly execute in parallel - they process sequentially.

**Workarounds:**
- **Simulated parallelism:** LLM tracks multiple "threads" conceptually, executes sequentially but logs as if parallel
- **Multi-agent system:** Spawn separate LLM instances (expensive, complex)
- **Hybrid approach:** LLM plans parallel execution, delegates to external tools/scripts that CAN run parallel

#### 2. Error Propagation Complexity
**Problem:** If step 1.1 fails while 1.2 is running, what happens?

**Strategies:**
- **Pessimistic:** Cancel all parallel steps in group if one fails
- **Optimistic:** Let all parallel steps complete, aggregate failures at sync point
- **Configurable:** Per-spec setting for failure handling in parallel contexts

#### 3. Resource Contention
**Problem:** Parallel steps might compete for resources (files, APIs, memory).

**Mitigations:**
- Declare resource requirements in TOML: `resources_required = ["file_system", "api_key"]`
- Exe controller allocates resources, prevents conflicts
- Steps with conflicting resources forced to run sequentially

#### 4. Debugging Difficulty
**Problem:** Parallel execution harder to debug than sequential.

**Solutions:**
- Detailed thread-level logging
- Timeline visualisation: "Step 1.1 started at T+0s, step 1.2 at T+1s, both finished at T+45s"
- "Replay mode": Re-run in strictly sequential mode for debugging

### Benefits

✅ **Faster execution:** Independent steps run concurrently  
✅ **Better resource utilisation:** CPU/IO overlap  
✅ **Scalability:** Large specs with many independent steps benefit  

### Costs

❌ **Increased complexity:** Dependency management, synchronisation  
❌ **Harder debugging:** Parallel failures more complex  
❌ **LLM limitations:** Most LLMs can't truly parallelise  
❌ **Error handling complexity:** Failure propagation in parallel contexts  

### Implementation Phases

#### Phase 1: Design & Validation (3-4 weeks)
- Design dependency declaration syntax
- Design synchronisation logic
- Prototype with simple example spec
- Validate concept with actual LLM execution

#### Phase 2: Core Implementation (4-6 weeks)
- Implement dependency graph builder
- Implement parallel execution logic in exe_template
- Enhanced progress logging for parallel contexts
- Error handling for parallel failures

#### Phase 3: Testing & Refinement (2-3 weeks)
- Test with various specs (IO-bound, CPU-bound, API-bound)
- Measure actual speedup vs overhead
- Refine synchronisation logic
- Handle edge cases

#### Phase 4: Documentation (1 week)
- Update Constitution with parallel execution rules
- Update templates with parallel examples
- Create parallel execution best practices guide

**Total Effort:** 10-14 weeks for full implementation

### Decision Criteria

**Proceed if:**
- Use cases demonstrate clear need (e.g., analysis of 50+ modules)
- LLM parallelism workarounds proven viable
- Resources available for 3+ month development
- Benefits outweigh complexity costs

**Defer if:**
- Most specs are naturally sequential
- Current performance is acceptable
- Higher-priority features exist
- Complexity not justified by use cases

### Alternative Approaches

#### Option A: Manual Parallel Specs
Instead of automatic parallelism, create multiple specs:
- `research_module_a.md` (executes independently)
- `research_module_b.md` (executes independently)
- `research_synthesis.md` (waits for A and B, manual trigger)

**Pros:** Simple, uses existing system  
**Cons:** Manual coordination, no built-in dependency management

#### Option B: External Orchestration
Use external tool (Airflow, Prefect) to orchestrate parallel spec execution:
- SPECS remains sequential internally
- Orchestrator handles parallelism
- SPECS provides integration hooks

**Pros:** Mature orchestration, proven patterns  
**Cons:** External dependency, additional complexity

#### Option C: Subset Parallelism (Compromise)
Allow parallel execution **only** within specific task types:
- "Analysis tasks" can have parallel steps
- "Synthesis tasks" must be sequential
- Limited use cases, constrained complexity

**Pros:** Addresses 80% of use cases with 20% of complexity  
**Cons:** Not fully general-purpose

### Recommendation

**Current Recommendation:** 💭 **Defer**

**Rationale:**
1. **No immediate need:** Most specs naturally sequential
2. **High complexity:** Significant engineering effort
3. **LLM limitations:** True parallelism difficult with current LLMs
4. **Workarounds exist:** Manual parallel specs or external orchestration

**Revisit when:**
- Accumulate 10+ specs with clear parallel opportunities
- LLM capabilities improve (multi-agent systems become standard)
- Community requests emerge (if shared publicly)
- Performance becomes bottleneck

**Alternative:** Implement Option C (Subset Parallelism) if specific use case emerges that justifies limited parallel support.

---

## Other Future Ideas

### 2. Conditional Execution

**Status:** 💭 Idea  
**Description:** Steps that execute conditionally based on prior outcomes

```toml
[[tasks.steps]]
id = 3
description = "Optimise performance"
condition = "IF step2_output.performance_score < 0.8"
```

### 3. Spec Composition

**Status:** 💭 Idea  
**Description:** Compose larger specs from smaller, reusable spec modules

```toml
[composition]
includes = ["spec_analysis.md", "spec_testing.md"]
```

### 4. Real-Time Monitoring Dashboard

**Status:** 💭 Idea  
**Description:** Web UI showing live progress of spec execution

**Features:**
- Real-time step progress
- Backup usage visualisation
- Mode escalation alerts
- Performance metrics

### 5. Spec Templates Library

**Status:** 💭 Idea  
**Description:** Pre-built spec templates for common tasks

**Examples:**
- `template_code_review.md`
- `template_bug_fix.md`
- `template_feature_implementation.md`
- `template_research.md`

### 6. Adaptive Learning

**Status:** 💭 Idea  
**Description:** System learns from execution patterns to suggest improvements

**Features:**
- "Backup[1] always succeeds → promote to primary?"
- "Step 2.3 always fails → redesign suggestion"
- "80% of specs use these 3 tasks → template suggestion"

---

## Version History

- v1.0 (2025-11-02): Initial future development roadmap with parallel execution design

---

**End of Future Development Document**

*This document tracks potential enhancements. Items move from Idea → Experimental → Planned → Completed as they mature.*

**Maintenance:** Review quarterly to assess priority and feasibility of proposed features.

