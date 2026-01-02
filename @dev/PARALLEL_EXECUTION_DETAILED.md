# Parallel Execution Support: Detailed Design & Risk Analysis

**Version:** 1.0  
**Date:** 2 November 2025  
**Purpose:** Complete technical specification for Enhancement #6 with risk mitigation strategies

---

## Executive Summary

**Status:** OUTLINE REQUESTED + EXAMPLE CODE  
**User Concern:** "Seems risky"  
**Recommendation:** IMPLEMENT WITH STRICT SAFEGUARDS

### The Core Idea

Allow independent steps within a task to execute simultaneously rather than sequentially, reducing total execution time whilst maintaining correctness.

### Why It's Risky (And How We Mitigate)

| Risk | Mitigation |
|------|------------|
| Race conditions (steps modify same output) | Explicit dependency declarations prevent this |
| Resource exhaustion (too many parallel LLM calls) | Configurable parallelism limits |
| Error cascade (one failure affects many) | Parallel groups fail independently |
| Debugging complexity (harder to trace) | Enhanced logging with parallel execution IDs |
| Synchronisation bugs (wrong execution order) | Barrier synchronisation between phases |

---

## Current State: Sequential Execution

### Example Spec (Sequential)

```markdown
### Task [1]: Research module functionality

- Step [1]: Extract specifications from documentation
- Step [2]: Analyse module dependencies  
- Step [3]: Summarise intended behaviour
```

**Execution timeline:**
```
[Step 1] -----> [Step 2] -----> [Step 3] -----> Complete
   60s            45s             30s           (Total: 135s)
```

**Problem:** Steps 1 and 2 are **independent** (don't depend on each other), yet they execute sequentially.

**Opportunity:** If Step 1 and Step 2 could run simultaneously:
```
[Step 1] -----> 
                 [Step 3] -----> Complete
[Step 2] ----->
   60s      45s     30s           (Total: 90s, 33% faster)
```

---

## Proposed State: Parallel Execution

### Same Spec (With Parallel Markers)

```markdown
### Task [1]: Research module functionality

- Step [1] [P]: Extract specifications from documentation
- Step [2] [P]: Analyse module dependencies  
- Step [3]: Summarise intended behaviour (depends on Steps 1 & 2)
```

**New notation:**
- `[P]` = Can execute in parallel with other `[P]` steps in same task
- No `[P]` = Must execute after all prior steps complete

### TOML Structure

```toml
[[tasks]]
id = 1
description = "Research module functionality"

[[tasks.steps]]
id = 1
description = "Extract specifications from documentation"
expected_output = "Structured summary of functions and dependencies"
parallel_safe = true  # NEW: Can run in parallel
parallel_group = "research"  # NEW: Group identifier
dependencies = []  # NEW: No dependencies on other steps
critical = true

[[tasks.steps]]
id = 2
description = "Analyse module dependencies"
expected_output = "Dependency graph and signature list"
parallel_safe = true  # NEW: Can run in parallel
parallel_group = "research"  # NEW: Same group as step 1
dependencies = []  # NEW: No dependencies
critical = true

[[tasks.steps]]
id = 3
description = "Summarise intended behaviour"
expected_output = "Behaviour description document"
parallel_safe = false  # NEW: Cannot run in parallel (needs prior results)
dependencies = [1, 2]  # NEW: Depends on steps 1 and 2
critical = false
```

---

## Execution Model

### Execution Phases

A task is divided into **phases** based on dependencies:

**Phase 1: Independent Steps (Parallel)**
- Steps with `dependencies = []`
- Marked `parallel_safe = true`
- Execute simultaneously

**Phase 2: Dependent Steps (Sequential)**
- Steps with `dependencies = [1, 2]`
- Wait for Phase 1 completion
- Execute sequentially or in new parallel group

### Barrier Synchronisation

Between phases, a **barrier** ensures all prior phase steps complete before next phase starts:

```
Phase 1:  [Step 1] [P]  }
          [Step 2] [P]  }  Execute in parallel
          
          -------- BARRIER --------  Wait for all Phase 1 steps
          
Phase 2:  [Step 3]       Single step (or new parallel group)
```

---

## Example Code: exe_template.md Enhancement

### Current Sequential Logic (Section 2)

```markdown
## 2. Execution Flow

1. For each Task in parameters_[descriptor].toml (ordered by id):
   - For each Step within that Task:
     - Execute step
     - Log result
     - Check error propagation
     - Proceed to next step
```

### Enhanced Parallel Logic (Section 2 - NEW)

```markdown
## 2. Execution Flow

1. For each Task in parameters_[descriptor].toml (ordered by id):
   
   ### 2.1 Phase Detection
   - Analyse all steps in task
   - Group steps by dependencies:
     - Phase 1: steps with dependencies = []
     - Phase 2: steps depending only on Phase 1
     - Phase 3: steps depending on Phase 1 or 2
     - ... (continue until all steps assigned)
   
   ### 2.2 Phase Execution
   For each Phase:
   
   #### 2.2.1 Identify Parallel Groups
   - Within phase, group steps by `parallel_group` field
   - Steps in same parallel_group can run simultaneously
   - Steps in different parallel_groups also run simultaneously
   - Steps with `parallel_safe = false` run sequentially
   
   #### 2.2.2 Launch Parallel Execution
   For each parallel group in phase:
   ```
   parallel_results = []
   
   FOR EACH step IN parallel_group:
     execution_id = generate_unique_id()
     launch_async_execution(step, execution_id)
     log(step_id, status="launched_parallel", execution_id, timestamp)
   
   WAIT_FOR_ALL parallel_group steps to complete
   
   FOR EACH step IN parallel_group:
     collect_result(step)
     log(step_id, status="complete_parallel", execution_id, timestamp, result)
     verify_expected_output(step)
   
   IF any_step_failed AND critical:
     handle_failure_with_backups(step)
   ```
   
   #### 2.2.3 Barrier Synchronisation
   - After all parallel groups in phase complete:
     - Verify all outputs present
     - Check error propagation
     - Log phase completion
     - Proceed to next phase (if any)
   
   ### 2.3 Fallback to Sequential
   If parallel execution not supported or disabled:
   - Execute all steps sequentially (current behaviour)
   - Log: "Parallel execution disabled, using sequential mode"
```

---

## Example: Complete Parallel Execution Scenario

### Spec Definition

```toml
[execution]
parallel_enabled = true  # NEW: Master switch
max_parallel_steps = 3   # NEW: Resource limit

[[tasks]]
id = 1
description = "Comprehensive module analysis"

# Phase 1: Independent research (can run in parallel)
[[tasks.steps]]
id = 1
description = "Extract API documentation"
parallel_safe = true
parallel_group = "research"
dependencies = []
critical = true

[[tasks.steps]]
id = 2
description = "Analyse dependency graph"
parallel_safe = true
parallel_group = "research"
dependencies = []
critical = true

[[tasks.steps]]
id = 3
description = "Review test coverage"
parallel_safe = true
parallel_group = "research"
dependencies = []
critical = false

# Phase 2: Synthesis (depends on Phase 1)
[[tasks.steps]]
id = 4
description = "Generate comprehensive report"
parallel_safe = false
dependencies = [1, 2, 3]
critical = true

# Phase 3: Validation (depends on Phase 2)
[[tasks.steps]]
id = 5
description = "Validate report completeness"
parallel_safe = false
dependencies = [4]
critical = true
```

### Execution Timeline

**Without Parallel Execution:**
```
[Step 1: 60s] → [Step 2: 45s] → [Step 3: 30s] → [Step 4: 50s] → [Step 5: 20s]
Total: 205 seconds
```

**With Parallel Execution:**
```
Phase 1 (Parallel):
  [Step 1: 60s]  }
  [Step 2: 45s]  }  Run simultaneously
  [Step 3: 30s]  }
  
  Duration: 60s (longest of the three)

Phase 2 (Sequential):
  [Step 4: 50s]

Phase 3 (Sequential):
  [Step 5: 20s]

Total: 130 seconds (36% faster)
```

### Enhanced progress.json Logging

```json
{
  "run_id": "2025-11-02T15:00:00Z",
  "execution_mode": "parallel",  // NEW
  "max_parallel_steps": 3,  // NEW
  "tasks": [
    {
      "task_id": "task1",
      "phases": [  // NEW: Phase tracking
        {
          "phase_id": 1,
          "parallel_groups": ["research"],
          "steps_in_phase": [1, 2, 3],
          "phase_start": "2025-11-02T15:00:05Z",
          "phase_end": "2025-11-02T15:01:05Z",
          "phase_duration_ms": 60000,
          "steps": [
            {
              "step_id": "step1",
              "execution_id": "exec_001",  // NEW: Unique parallel execution ID
              "status": "complete",
              "parallel_group": "research",
              "launched_at": "2025-11-02T15:00:05.100Z",
              "completed_at": "2025-11-02T15:01:05.100Z",
              "execution_time_ms": 60000,
              "parallel_execution": true  // NEW
            },
            {
              "step_id": "step2",
              "execution_id": "exec_002",
              "status": "complete",
              "parallel_group": "research",
              "launched_at": "2025-11-02T15:00:05.200Z",
              "completed_at": "2025-11-02T15:00:50.200Z",
              "execution_time_ms": 45000,
              "parallel_execution": true
            },
            {
              "step_id": "step3",
              "execution_id": "exec_003",
              "status": "complete",
              "parallel_group": "research",
              "launched_at": "2025-11-02T15:00:05.300Z",
              "completed_at": "2025-11-02T15:00:35.300Z",
              "execution_time_ms": 30000,
              "parallel_execution": true
            }
          ]
        },
        {
          "phase_id": 2,
          "steps_in_phase": [4],
          "phase_start": "2025-11-02T15:01:05Z",
          "phase_end": "2025-11-02T15:01:55Z",
          "phase_duration_ms": 50000,
          "steps": [
            {
              "step_id": "step4",
              "execution_id": "exec_004",
              "status": "complete",
              "dependencies_satisfied": [1, 2, 3],  // NEW
              "parallel_execution": false
            }
          ]
        }
      ]
    }
  ]
}
```

---

## Risk Analysis & Mitigation

### Risk 1: Race Conditions ⚠️ HIGH

**Scenario:** Two parallel steps modify the same output file.

**Example:**
- Step 1: Write to `output.md` (append documentation)
- Step 2: Write to `output.md` (append test results)
- **Problem:** Concurrent writes corrupt file

**Mitigation Strategy:**

1. **Explicit output declaration:**
   ```toml
   [[tasks.steps]]
   id = 1
   output_files = ["docs/api.md"]  # NEW: Declare outputs
   
   [[tasks.steps]]
   id = 2
   output_files = ["docs/tests.md"]  # NEW: Different output
   ```

2. **Validation during phase detection:**
   ```markdown
   ### 2.1.1 Output Conflict Detection
   
   For each parallel group:
     - Collect all output_files from steps
     - Check for overlapping outputs
     - IF overlap detected:
       - Log error: "Steps X and Y cannot run in parallel (shared output: file.md)"
       - FORCE sequential execution for conflicting steps
       - Continue with remaining parallel steps
   ```

3. **Runtime check:**
   ```markdown
   Before launching parallel execution:
     - Verify no output file conflicts
     - If conflict detected at runtime:
       - Fall back to sequential execution
       - Log warning
   ```

**Risk Level After Mitigation:** LOW

---

### Risk 2: Resource Exhaustion ⚠️ MEDIUM

**Scenario:** Too many parallel LLM calls overwhelm system or API rate limits.

**Example:**
- 10 steps marked parallel
- All launch simultaneously
- API rate limit: 5 requests/minute
- **Problem:** 5 steps succeed, 5 fail with rate limit errors

**Mitigation Strategy:**

1. **Configurable parallelism limit:**
   ```toml
   [execution]
   max_parallel_steps = 3  # NEW: Limit concurrent steps
   ```

2. **Semaphore-based execution:**
   ```markdown
   ### 2.2.2 Launch Parallel Execution with Semaphore
   
   semaphore = Semaphore(max_parallel_steps)
   
   FOR EACH step IN parallel_group:
     WAIT_FOR semaphore.acquire()
     launch_async_execution(step, execution_id)
     ON_COMPLETE: semaphore.release()
   ```

3. **Adaptive throttling:**
   ```markdown
   IF rate_limit_error detected:
     - Reduce max_parallel_steps by 1
     - Retry failed step
     - Log throttling adjustment
   ```

**Risk Level After Mitigation:** LOW

---

### Risk 3: Error Cascade ⚠️ HIGH

**Scenario:** One parallel step fails, but others continue and depend on its output.

**Example:**
- Phase 1: Steps 1, 2, 3 run in parallel
- Step 2 fails (critical)
- Steps 1 and 3 complete successfully
- Phase 2: Step 4 depends on outputs from Steps 1, 2, 3
- **Problem:** Step 4 proceeds with incomplete inputs

**Mitigation Strategy:**

1. **Immediate failure propagation:**
   ```markdown
   ### 2.2.4 Critical Failure Handling (NEW)
   
   During parallel execution:
     IF any_critical_step_fails:
       - Immediately signal all parallel steps to abort
       - Wait for clean shutdown of running steps
       - Log all step states (completed/aborted/failed)
       - Apply error propagation strategy
       - DO NOT proceed to next phase
   ```

2. **Phase-level dependency validation:**
   ```markdown
   ### 2.2.3 Barrier Synchronisation (Enhanced)
   
   After phase completion:
     - Verify ALL required outputs present
     - Check critical steps all passed
     - IF any critical failure:
       - Evaluate error_propagation strategy
       - halt_on_critical: STOP execution
       - collaborative_review: Request human guidance
       - continue_and_log: Proceed with warning
   ```

**Risk Level After Mitigation:** LOW

---

### Risk 4: Debugging Complexity ⚠️ MEDIUM

**Scenario:** Parallel execution makes it hard to trace what happened when.

**Example:**
- 5 steps run in parallel
- One fails
- **Problem:** Log entries interleaved, hard to reconstruct timeline

**Mitigation Strategy:**

1. **Enhanced logging with execution IDs:**
   ```json
   {
     "step_id": "step2",
     "execution_id": "exec_002",  // NEW: Unique per execution
     "parallel_group": "research",
     "launched_at": "2025-11-02T15:00:05.200Z",
     "events": [  // NEW: Event stream per step
       {
         "event": "launched",
         "timestamp": "2025-11-02T15:00:05.200Z"
       },
       {
         "event": "primary_method_started",
         "timestamp": "2025-11-02T15:00:05.250Z"
       },
       {
         "event": "primary_method_failed",
         "timestamp": "2025-11-02T15:00:30.000Z",
         "error": "Parse error"
       },
       {
         "event": "backup[1]_started",
         "timestamp": "2025-11-02T15:00:30.100Z"
       },
       {
         "event": "backup[1]_complete",
         "timestamp": "2025-11-02T15:00:50.200Z"
       }
     ]
   }
   ```

2. **Timeline visualisation tool:**
   ```markdown
   ### Post-Execution Analysis
   
   Generate timeline view from progress.json:
   
   Phase 1 (Parallel):
   15:00:05 [Step 1] ============================> Complete (60s)
   15:00:05 [Step 2] ===================> Complete (45s)
   15:00:05 [Step 3] ============> Complete (30s)
   
   Phase 2 (Sequential):
   15:01:05 [Step 4] =======> Complete (50s)
   ```

**Risk Level After Mitigation:** LOW

---

### Risk 5: Synchronisation Bugs ⚠️ HIGH

**Scenario:** Barrier logic has bug, phase proceeds before all steps complete.

**Example:**
- Phase 1: Steps 1, 2, 3 parallel
- Step 3 still running
- Barrier incorrectly reports "all complete"
- Phase 2 starts
- **Problem:** Step 4 uses incomplete outputs from Step 3

**Mitigation Strategy:**

1. **Explicit synchronisation contract:**
   ```markdown
   ### 2.2.3 Barrier Synchronisation (Strict)
   
   barrier_contract:
     PRECONDITION: All steps in phase launched
     POSTCONDITION: All steps in phase completed OR failed
   
   barrier_implementation:
     1. Count steps_launched in phase
     2. Wait until steps_completed + steps_failed = steps_launched
     3. Verify all expected outputs exist (if completed)
     4. Log barrier_passed event
     5. ONLY THEN proceed to next phase
   ```

2. **Timeout safety:**
   ```markdown
   barrier_timeout = phase_timeout * 1.5
   
   IF barrier_wait > barrier_timeout:
     - Log error: "Barrier timeout, some steps hung"
     - Mark hung steps as failed
     - Trigger collaborative mode
     - DO NOT proceed to next phase
   ```

3. **Comprehensive testing:**
   - Unit test barrier logic
   - Simulate hung steps
   - Simulate rapid completions
   - Verify barrier never passes early

**Risk Level After Mitigation:** LOW (with thorough testing)

---

## Implementation Phases

### Phase 0: Foundation (No Parallel Execution Yet)

**Goal:** Add infrastructure without changing behaviour

**Changes:**
1. Add `dependencies`, `parallel_safe`, `parallel_group` fields to TOML
2. Add `dependencies` validation to Commander
3. Add `parallel_enabled = false` flag to all specs
4. No execution logic changes

**Outcome:** Templates ready, but everything still sequential

**Duration:** 1 week

**Risk:** ZERO (no behaviour change)

---

### Phase 1: Dependency Analysis Only

**Goal:** Detect phases but don't execute in parallel yet

**Changes:**
1. Add phase detection logic to exe_template.md
2. Log detected phases to progress.json
3. Execute sequentially but log "would be parallel"
4. Validate dependency declarations

**Outcome:** Can see where parallelism would apply

**Duration:** 1 week

**Risk:** LOW (logging only)

---

### Phase 2: Controlled Parallel Execution

**Goal:** Enable parallel execution with strict limits

**Changes:**
1. Implement parallel execution for max_parallel_steps = 2
2. Add barrier synchronisation
3. Add output conflict detection
4. Add immediate critical failure handling

**Outcome:** Parallel execution works with safety limits

**Duration:** 2 weeks

**Risk:** MEDIUM (new execution path)

---

### Phase 3: Full Parallel Support

**Goal:** Production-ready parallel execution

**Changes:**
1. Increase parallelism limits
2. Add adaptive throttling
3. Add timeline visualisation
4. Comprehensive testing

**Outcome:** Robust parallel execution

**Duration:** 2 weeks

**Risk:** MEDIUM (requires extensive testing)

---

## Safety Checklist

Before enabling parallel execution for a spec:

- [ ] All steps have explicit `dependencies` declared
- [ ] All steps declare `output_files` if they write to files
- [ ] No output file conflicts detected
- [ ] `max_parallel_steps` configured appropriately
- [ ] Error propagation strategy chosen (recommend `halt_on_critical`)
- [ ] Critical steps identified correctly
- [ ] Backup methods defined for critical steps
- [ ] Tested sequentially first
- [ ] Progress logging verified
- [ ] Monitoring in place for failures

---

## Recommendation

### Short Term: DON'T IMPLEMENT YET

**Rationale:**
1. **High complexity:** Parallel execution adds significant complexity
2. **Marginal benefit:** Most specs have <10 steps, time savings minimal
3. **Risk:** Bugs in parallel logic could corrupt outputs
4. **Alternative:** Optimize sequential execution first (better backups, faster retries)

### Medium Term: FOUNDATION ONLY

**If pursuing parallel execution:**
1. Implement Phase 0 (add fields, no execution change)
2. Test dependency declarations with real specs
3. Validate use cases where parallelism helps
4. Defer Phase 1-3 until proven need

### Long Term: CONSIDER IF PROVEN NEED

**Proceed to full implementation only if:**
- You regularly have 5+ independent steps per task
- Sequential execution time is genuinely problematic (>10 minutes per spec)
- You've exhausted sequential optimisation approaches
- You have robust testing infrastructure
- You're comfortable with the added complexity

---

## Alternative: Pseudo-Parallel Execution

**Lower-risk approach that provides some benefits:**

**Instead of true parallelism:** Use **pre-fetching** and **result caching**

```markdown
### Pseudo-Parallel Approach

1. Analyse all steps in task
2. Identify independent steps (dependencies = [])
3. For each independent step:
   - Pre-fetch required inputs
   - Cache intermediate results
   - Execute sequentially but with optimised I/O
4. No true parallelism, no synchronisation bugs
5. Faster than naive sequential, safer than parallel
```

**Benefits:**
- Simpler implementation
- No race conditions
- No synchronisation bugs
- Still provides speedup (from optimised I/O)

**Drawbacks:**
- Not as fast as true parallelism
- Limited to I/O-bound steps

**Recommendation:** Consider this instead of full parallelism

---

## Conclusion

**Parallel execution is powerful but risky.** The risks can be mitigated with careful design, but the complexity cost is high.

**For SPECS system:**
- ❌ **Don't implement now** (marginal benefit, high risk)
- ⚠️ **Consider foundation later** (add fields, test dependency declarations)
- ✅ **Explore pseudo-parallel** (safer alternative with some benefits)

**If you proceed:**
1. Start with Phase 0 only
2. Test extensively
3. Use with max_parallel_steps = 2 initially
4. Monitor carefully for issues
5. Be prepared to revert to sequential if problems emerge

---

**End of Parallel Execution Detailed Design**

*Recommendation: Defer implementation until proven need. Focus on sequential optimisation first.*

