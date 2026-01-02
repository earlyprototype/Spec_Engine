# exe_podcast.md

**Version:** 1.0  
**Last Updated:** 2025-11-03  
**Purpose:** Execution controller for podcast website deployment spec

---

## [root]/Specs/TGACGTCA/spec_podcast/

---

### [META]
- **File Role:** Execution controller — reads and interprets both `spec_podcast.md` and `parameters_podcast.toml` to coordinate task execution
- **Created by:** `commander-spec.md`
- **Mode:** Default = `dynamic` (autonomous with intelligent escalation)
- **Logging:** Writes to `progress_podcast.json`
- **Descriptor:** podcast
- **MCP Integration:** shadcn/ui MCP server available for component discovery and installation
- **Component Library:** shadcn/ui (Radix UI primitives + Tailwind CSS)

---

## 1. Initialization and Validation

### 1.1 File Presence Check
1. Confirm presence of required files:
   - `spec_podcast.md`
   - `parameters_podcast.toml`
2. If either file is missing:
   - Log critical error
   - Halt execution and prompt in **collaborative** mode for resolution

### 1.1a Software Stack Validation (MANDATORY for Build/Create/System Goals)

**Trigger: This is a build goal (web application deployment)**

1. **Read [software_stack] from parameters_podcast.toml**

2. **Verify MANDATORY fields are populated:**
   - ✅ `deployment_type = "web_app"`
   - ✅ `primary_language = "javascript"`
   - ✅ `packaging_method = "vercel_netlify_static"`

3. **Validate [user_interface] section:**
   - ✅ Goal says "for podcast listeners and administrators" → `user_interface.required = true`
   - ✅ `interface_type = "web"`
   - ✅ `target_users = "podcast_listeners_and_administrators"`
   - ✅ `skill_level = "none"`

4. **Validate [deployment] section:**
   - ✅ `target_platform = "web"`
   - ✅ `installation_type = "web_url"`
   - ✅ `startup_method = "open_url"`

5. **Validate [completion_criteria] section:**
   - ✅ Section exists with 10 specific acceptance criteria
   - ✅ All completion flags present (functional_complete, interface_complete, deployment_complete, production_ready, user_tested, documentation_complete)
   - ✅ User interface completion required (interface_complete = true)
   - ✅ Production readiness required (production_ready = true)

**Validation Status: PASS**

```json
{
  "software_stack_validation": {
    "deployment_type": "web_app",
    "primary_language": "javascript",
    "framework": "nextjs",
    "ui_required": true,
    "target_users": "podcast_listeners_and_administrators",
    "packaging_method": "vercel_netlify_static",
    "completion_criteria_defined": true,
    "acceptance_criteria_count": 10,
    "validation_status": "PASS"
  }
}
```

**shadcn/ui MCP Integration Note:**
- MCP server available for autonomous component discovery
- Use MCP tools to: list components, search components, get component details, install components
- Steps marked with `mcp_tools_available = true` can leverage MCP for shadcn/ui operations
- Components needed are specified in `shadcn_components_needed` arrays in TOML

**Log to progress_podcast.json and proceed to Section 1.2**

### 1.2 Initialize Progress Log
1. Check if `progress_podcast.json` exists
2. If not, create with initial structure:
   ```json
   {
     "run_id": "[timestamp]",
     "descriptor": "podcast",
     "start_time": "[ISO-8601]",
     "status": "initializing",
     "execution_mode": "dynamic",
     "tasks": []
   }
   ```
3. If resuming, validate log integrity and mark as `resumed`
4. Record initialization metadata:
   - Start time
   - Default mode (dynamic)
   - Total: 5 tasks, 20 steps

### 1.2a User Mode Selection (Interactive Prompt)

**After initialization, before validation:**

1. **Present mode options to user:**
   ```
   Execution Mode Selection
   ========================
   
   Default: Dynamic Mode (Recommended)
   - Runs autonomously but escalates intelligently when needed
   - Balances efficiency with safety
   - Uses multi-signal decision-making for escalation
   
   Options:
   [1] Continue with Dynamic mode (recommended)
   [2] Switch to Silent mode (fully autonomous, minimal interruption)
   [3] Switch to Collaborative mode (pause at each critical decision)
   
   Current selection: Dynamic
   
   Press Enter to continue with Dynamic, or enter 1/2/3 to select:
   ```

2. **Capture user input and update progress_podcast.json**

3. **Proceed to validation** (Section 1.3)

### 1.3 Parse Specification Files
1. Read and parse `spec_podcast.md`:
   - Extract goal: Deploy production podcast website
   - Extract 5 tasks with descriptions
   - Extract all 20 steps across tasks
   - Extract backups, components, constraints
2. Read and parse `parameters_podcast.toml`:
   - Extract goal description
   - Extract tasks array with all parameters
   - Extract steps with actions, expected outputs
   - Extract logging and verification configuration
3. Store parsed content in memory for validation

### 1.4 Validate Goal
1. ✅ Check that **one and only one goal** exists in both files
2. ✅ Goal description is clear and measurable
3. ✅ Goal descriptions match between Markdown and TOML
4. ✅ Goal is specific (not vague or ambiguous)

**Status:** PASS

### 1.5 Validate Tasks
1. ✅ 5 tasks defined in both files (within 2-5 range per Constitution Article II)
2. For each task, verify:
   - ✅ Unique task ID [1-5]
   - ✅ Non-empty description
   - ✅ At least one step per task
   - ✅ Valid mode settings
   - ✅ Defined max_retries values
3. ✅ No duplicate task IDs
4. ✅ Task count appropriate (5 is within optimal range)

**Status:** PASS

### 1.6 Validate Steps
1. For each step within each task, verify:
   - ✅ Unique step ID within that task
   - ✅ Non-empty action description
   - ✅ Expected output defined for all 20 steps
2. ✅ No duplicate step IDs within tasks
3. ✅ All expected outputs are specific and measurable

**Step count per task:** 4, 4, 4, 4, 4 (all within 1-5 range)

**Status:** PASS

### 1.7 Validate Backups
1. ✅ Backups exist for critical steps where appropriate
2. ✅ All backup descriptions are specific alternative methods (not simple retries)
3. ✅ Backup IDs are unique and properly referenced
4. ⚠️ Some critical steps have no backups (acceptable per Constitution - 0-2 backups permitted)

**Backup coverage:** 12 backups across 20 steps

**Status:** PASS with minor warning

### 1.8 Bridging Verification (Markdown ↔ TOML)
1. ✅ Every task in `spec_podcast.md` exists in `parameters_podcast.toml`
2. ✅ Every step in Markdown has corresponding TOML entry
3. ✅ Task IDs match: [1, 2, 3, 4, 5]
4. ✅ Step IDs match within each task: [1, 2, 3, 4]
5. ✅ Backups represented in both files
6. ✅ Task sequence order consistent

**Bridging Status:** SYNCHRONIZED

### 1.9 Validate Components and Constraints
1. ✅ Components referenced in steps exist in spec
2. ✅ Constraints properly defined in TOML
3. ✅ Cross-browser compatibility constraints specified
4. ✅ Pagination and email deliverability constraints defined

**Status:** PASS

### 1.10 Validation Summary and Pre-Flight Check

**Validation Report:**

✅ **PASS**: Goal is singular and clear  
✅ **PASS**: 5 tasks defined (within 2-5 range)  
✅ **PASS**: Step counts are [4, 4, 4, 4, 4] (within 1-5 range)  
✅ **PASS**: 14 of 20 steps marked critical (70%, within acceptable range for production deployment)  
✅ **PASS**: All expected outputs are specific and measurable  
✅ **PASS**: Software stack fully defined for web application  
✅ **PASS**: Completion criteria comprehensive (10 acceptance criteria)  
✅ **PASS**: Bridging verification successful - files synchronized  
⚠️ **INFO**: Critical percentage slightly high (70%) but appropriate for production goal  
⚠️ **INFO**: Task 1 has research_enabled = true (will use web search for design research)

**Critical Errors:** None  
**Warnings:** None (info notes only)

**Validation Status: READY FOR EXECUTION**

Mark progress log status as `ready_for_execution`

Proceed to Execution Flow (Section 2)

---

## 2. Execution Flow

### 2.0 Constitutional Compliance Check (Per Task)

**Before executing each task**, verify ongoing constitutional compliance per `__SPEC_Engine/_Constitution/constitution.md`:

#### Article IV Check: Error Propagation Functioning
1. ✅ Verify `error_propagation.enabled = true` in TOML
2. ✅ Check that `read_prior_steps = true`
3. ✅ Confirm dependency_tracking is active
4. **Status:** Compliant

#### Article VI Check: Critical Flag Balance
1. Count critical vs non-critical steps in upcoming task
2. Calculate criticality ratio for this task
3. Record in progress.json:
   ```json
   "constitutional_checks": {
     "task_id": 1,
     "critical_balance": {
       "critical_count": 3,
       "total_count": 4,
       "ratio": 0.75,
       "compliant": true,
       "note": "Slightly high but acceptable for foundation task"
     }
   }
   ```

#### Article VIII Check: Prior Step Outcomes Read
1. Before executing Step 1 of any task (except Task 1):
   - Verify prior task's final step outcome was read
   - Check for critical failures in prior tasks
   - **If not read:** Log constitutional violation

#### Article X Check: Comprehensive Logging Active
1. Verify last step recorded all required fields
2. **If incomplete:** Log constitutional violation
3. Continue but flag for post-execution review

**Proceed with task execution**

---

### 2.1 Task Iteration

1. For each **Task** in `parameters_podcast.toml` (ordered by `id`):
   - Perform Constitutional Compliance Check (Section 2.0)
   - Log Task start event
   - Read task description and mode
   - **Check research_enabled flag** (Section 2.1a)

### 2.1a Research-Enabled Mode (Task 1 Only)

**Trigger:** Task 1 has `research_enabled = true`

**Purpose:** Gather current mindfulness web design trends and colour psychology

**Execution behaviour:**

1. **Pre-Task Research Phase:**
   - Review task description: "Research mindfulness web design patterns and colour schemes"
   - Identify knowledge gaps: Current 2025 design trends, mindfulness colour palettes
   - Formulate research queries:
     - "Mindfulness website design trends 2025"
     - "Calming colour palettes for meditation apps"
     - "Modern podcast website layouts"
     - "Colour psychology for wellness websites"

2. **Research Execution:**
   - Execute queries via available MCP tools (web_search, documentation)
   - Synthesize findings from multiple sources
   - Extract actionable design insights

3. **Research Logging:**
   ```json
   {
     "task_id": "1",
     "research_phase": {
       "triggered": true,
       "timestamp_start": "[ISO-8601]",
       "timestamp_end": "[ISO-8601]",
       "queries_performed": [
         "Mindfulness website design trends 2025",
         "Calming colour palettes for meditation apps"
       ],
       "sources_consulted": ["..."],
       "key_findings": ["..."],
       "confidence_level": "high"
     }
   }
   ```

4. **Apply Research to Steps:**
   - Step 1 executes with researched design trends context
   - Step 2 uses colour palette findings

---

2. For each **Step** within that Task:

   ### 2.2 Pre-Step Error Propagation Check
   - **Read `progress_podcast.json`** for prior step outcomes
   - Check if any prior **critical steps** failed
   - If critical failure detected:
     - Evaluate impact on current step
     - Apply `propagation_strategy = "collaborative_review"`
     - Pause and request human decision
   - Log propagation decision

   ### 2.3 Step Execution with Backup Selection
   - Log `start` event with timestamp
   - **Attempt primary method** as defined
   - If successful:
     - Log `step_complete` with expected output summary
     - Verify output matches `expected_output`
     - Proceed to next step
   - If failure detected:
     - Increment retry count
     - **Attempt Backup Method Selection (Section 2.6)**
     - Log each backup attempt

   ### 2.4 Retry and Mode Escalation Logic
   - If primary method fails and backups exist:
     - Execute backups in sequence
     - Log each backup attempt separately
   - If all methods exhausted:
     - Check `critical_flag`:
       - If `critical = true`:
         - Increment consecutive failure counter
         - Switch to **collaborative mode**
         - Prompt for human instruction
       - If `critical = false`:
         - Log failure as warning
         - Continue to next step
   - If consecutive failures reach `failure_threshold = 3`:
     - Escalate to collaborative mode

3. When all Steps complete:
   - Mark Task as `complete`
   - Log task summary
   - Reset consecutive failure counter

4. Continue sequentially to next Task

---

## 2.6 Backup Method Selection

When a step's primary method fails:

1. **Check if backups are defined** for this step
2. **Execute backups sequentially** (backup[1], then backup[2])
3. **Log each backup attempt** with:
   - backup_id
   - trigger_condition
   - outcome (success/failure)
   - timestamp
4. **If backup succeeds:**
   - Log successful backup method
   - Mark step as complete
   - Continue to next step
5. **If all backups exhausted:**
   - If `critical_flag = true`:
     - Log all attempted methods
     - Switch to collaborative mode
     - Request human guidance
   - If `critical_flag = false`:
     - Log warning
     - Continue execution

---

## 3. Mode Control

### Silent Mode
- Executes autonomously
- Only raises alerts on critical failures beyond retries

### Collaborative Mode
- Prompts for human input on persistent failure or ambiguity
- Records prompt and response in log

### Dynamic Mode (Default for Podcast Spec)

**Triggers for Mode Escalation:**

#### 1. Consecutive Failures Pattern
- Window: Last 3 steps (threshold = 3 per TOML)
- Trigger: 3 consecutive step failures
- Reset: Any successful step completion

#### 2. Backup Depletion Pattern
- Same backup succeeds ≥3 times in last 5 steps
- ≥60% of last 5 steps required backups
- ≥3 consecutive steps exhausted all backups

#### 3. Confidence Degradation
- ≥50% of last 5 steps have expected_output mismatch
- Average retries increase ≥50% over 5-step window
- ≥40% of last 5 steps have constraint violations

#### 4. Critical Failure Threshold
- Total failures reach `failure_threshold = 3`

**Dynamic Mode Escalation Logic:**
```
IF consecutive_failures >= 3 OR 
   backup_depletion_detected OR 
   confidence_degradation_detected OR
   failure_count >= 3:
   
   THEN switch_to_collaborative_mode()
   LOG escalation_reason
   REQUEST human_guidance
```

All mode changes logged with timestamp, task, step, cause, and attempted methods

---

## 4. Verification Layer

### 4.1 Per-Step Verification
After each step:
1. **Verify expected output** against TOML definition
2. **Check constraint satisfaction** (cross-browser compatibility, responsiveness, etc.)
3. **Validate backup usage** properly documented

### 4.2 Per-Task Verification
After each Task:
1. Confirm all Steps marked complete or appropriately failed
2. Cross-check task and step IDs against TOML
3. Verify error propagation handled correctly
4. If discrepancies found, trigger collaborative review

### 4.3 Error Propagation Verification
Before marking task complete:
1. Review propagation decisions
2. Check dependency chain
3. Validate failure threshold tracking

### 4.4 Run End Verification
At run end:
- Validate all 5 Tasks marked complete
- Check for orphaned or skipped steps
- Verify all error propagation events handled
- Confirm all mode switches logged
- If incomplete: Summarize pending tasks and critical failures

---

## 5. Logging and Reporting

All activity recorded in `progress_podcast.json` with entries for:
- task_id
- step_id
- status (started, completed, retried, failed, skipped)
- retry_count
- timestamp
- mode
- method_used (primary, backup_1, backup_2)
- backup_attempts
- error_propagation_decision
- prior_step_dependencies
- constraint_status
- expected_output_match
- message or error detail
- consecutive_failure_count
- **research_phase** (for Task 1):
  - triggered, timestamp_start, timestamp_end
  - queries_performed, sources_consulted
  - key_findings, confidence_level

At completion:
1. Write final summary:
   - Total: 5 tasks, 20 steps
   - Steps succeeded / failed / skipped
   - Total retries
   - Backup methods used
   - Critical errors with locations
   - Mode switches with reasons
   - Error propagation events
   - Runtime duration
2. Mark log as `run_complete = true`
3. Add completion metadata

---

## 6. Post-Execution Analysis

**After completing all tasks OR on critical halt**, perform comprehensive analysis:

### 6.1 Failure Pattern Analysis

#### Step 1: Identify Failure Patterns
- Scan all 20 step outcomes for failures
- Count failure frequency per step
- Track retry patterns
- Calculate failure rates (overall and per-task)

#### Step 2: Analyse Backup Effectiveness
- Identify successful backups
- Track backup usage frequency
- Calculate backup success rate
- Recommend backup improvements

#### Step 3: Mode Escalation Analysis
- Count mode switches
- Evaluate escalation appropriateness
- Track escalation triggers

#### Step 4: Dependency and Error Propagation Analysis
- Verify error propagation functioned correctly
- Identify dependency issues
- Track propagation decisions

#### Step 5: Generate Recommendations
- Critical flag adjustments
- Backup improvements
- Mode configuration tuning
- Spec structure suggestions

### 6.2 Constitutional Compliance Review

#### Article VI Review: Critical Flag Balance
- Overall: 14/20 = 70%
- Evaluate if appropriate for production deployment
- Recommend adjustments based on actual execution

#### Article VII Review: Backup Quality
- Review each backup used
- Verify genuine alternative reasoning paths (not retries)
- Log violations if found

#### Article VIII Review: Error Propagation
- Verify prior step outcomes were read
- Check propagation strategy effectiveness

#### Article IX Review: Mode Escalation
- Evaluate dynamic mode performance
- Review escalation thresholds
- Assess appropriateness

#### Article X Review: Logging Completeness
- Verify all required fields logged
- Check for gaps or incomplete entries
- Confirm immutability

### 6.3 Append Analysis to progress_podcast.json

Add comprehensive analysis section with:
- Failure patterns
- Backup effectiveness
- Mode escalation analysis
- Constitutional compliance review
- Recommendations

### 6.4 Completion Verification (MANDATORY)

**Execute BEFORE marking goal as ACHIEVED**

Read "Definition of Complete" from `spec_podcast.md` and verify each criterion:

#### Universal Checks
1. ✅ **Primary Deliverable Exists:** Podcast website deployed and accessible
2. ✅ **Quality Standards Met:** Audio playback works, admin panel functional, responsive design verified
3. ✅ **Verification Method Passed:** Manual testing, device testing, admin testing completed

#### Build/System Goal Checks
4. ✅ **Deployment Artifact Exists:** Website deployed to production URL
5. ✅ **User Interface Implemented:** Web interface functional for listeners and admins
6. ✅ **Production Ready:** Insforge backend in production mode, email service configured with real APIs
7. ✅ **User Documentation:** Admin user guide created with screenshots

#### Status Assignment
```json
{
  "completion_verification": {
    "primary_deliverable_exists": true,
    "quality_standards_met": true,
    "verification_passed": true,
    "deployment_artifact_exists": true,
    "user_interface_implemented": true,
    "production_ready": true,
    "user_documentation_exists": true,
    
    "overall_status": "PASS",
    "goal_achievement_status": "ACHIEVED",
    "gaps": [],
    "timestamp": "[ISO-8601]"
  }
}
```

**Status Rules:**
- **ACHIEVED:** All applicable checks PASS
- **PARTIAL:** Core deliverable exists but deployment/production incomplete
- **NOT ACHIEVED:** Core deliverable missing or broken

### 6.5 Learning for Future Specs

Document key learnings:
- Effective patterns identified
- Anti-patterns to avoid
- System tuning insights

Store learnings in `@filing/execution_learnings_podcast_[date].md`

---

## 7. Notes for Adaptation

- Designed for sequential task execution only
- Compatible with LLM collaborative workflows
- Extensible for CI/CD pipelines
- Reusable template (copy and rename for other projects)

---

**End of exe_podcast.md**

