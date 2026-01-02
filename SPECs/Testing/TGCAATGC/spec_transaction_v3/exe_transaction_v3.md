# exe_transaction_v3.md
## C:/Users/Fab2/Desktop/AI/Specs/SPECs/Testing/TGCAATGC/spec_transaction_v3/

---

### [META]
- **File Role:** Execution controller — reads and interprets both `spec_transaction_v3.md` and `parameters_transaction_v3.toml` to coordinate task execution.  
- **Created by:** `commander-spec.md`  
- **Mode:** Default = `dynamic`  
- **Logging:** Writes to `progress_transaction_v3.json`  
- **Descriptor:** transaction_v3 (Charity Shop POS Complete System)

---

## 1. Initialization and Validation

### 1.1 File Presence Check
1. Confirm presence of required files:
   - `spec_transaction_v3.md`
   - `parameters_transaction_v3.toml`
2. If either file is missing:
   - Log critical error.
   - Halt execution and prompt in **collaborative** mode for resolution.

### 1.1a Software Stack Validation (MANDATORY for Build/Create/System Goals)

**Trigger: If goal description contains "build", "create", "develop", "system", "application", "app"**

1. **Read [software_stack] from parameters_[descriptor].toml**

2. **Verify MANDATORY fields are populated:**
   - `deployment_type` (cannot be empty string)
   - `primary_language` (cannot be empty string)
   - `packaging_method` (if deployment_type requires it)

3. **Validate [user_interface] section:**
   - If goal says "for [users]" (e.g., "for volunteers", "for doctors") → `user_interface.required` MUST be true
   - If `user_interface.required = true` → verify:
     - `interface_type` is defined
     - `target_users` is defined
     - `skill_level` is defined

4. **Validate [deployment] section:**
   - If deployment_type = "desktop_app" or "web_app" → verify:
     - `target_platform` defined
     - `installation_type` defined
     - `startup_method` defined

5. **Validate [completion_criteria] section:**
   - Verify section exists (MANDATORY for build/create goals)
   - Check that at least 3 criteria are defined as true or have acceptance_criteria list populated
   - If `user_interface.required = true` → `completion_criteria.interface_complete` MUST exist
   - If external APIs/services mentioned in goal → `completion_criteria.production_ready` MUST exist

**If ANY validation fails:**
```json
{
  "validation_error": "software_stack_incomplete",
  "missing_fields": ["deployment_type", "ui_library"],
  "reason": "Goal requires building a system but software stack undefined",
  "action": "HALT"
}
```
- HALT execution immediately
- Log critical validation failure
- Escalate to collaborative mode
- Display message: "Critical: Software stack undefined. Cannot determine what to build. Review spec_[descriptor].md Software Stack section and parameters_[descriptor].toml [software_stack] section."

**If validation passes:**
```json
{
  "software_stack_validation": {
    "deployment_type": "desktop_app",
    "primary_language": "python",
    "framework": "pyqt5",
    "ui_required": true,
    "target_users": "charity shop volunteers",
    "packaging_method": "pyinstaller",
    "completion_criteria_defined": true,
    "validation_status": "PASS"
  }
}
```

**Log to progress.json and proceed to Section 1.2**

### 1.2 Initialize Progress Log
1. Check if `progress_transaction_v3.json` exists.
2. If not, create with initial structure:
   ```json
   {
     "run_id": "[timestamp]",
     "descriptor": "transaction_v3",
     "start_time": "[ISO-8601]",
     "status": "initializing",
     "execution_mode": "dynamic",
     "tasks": []
   }
   ```
3. If resuming, validate log integrity and mark as `resumed`.
4. Record initialization metadata:
   - Start time
   - Default mode (dynamic)
   - Total number of tasks and steps

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

2. **Capture user input:**
   - If Enter/empty: use Dynamic (default)
   - If "1": use Dynamic
   - If "2": use Silent
   - If "3": use Collaborative
   - Invalid input: re-prompt

3. **Update progress.json with selected mode:**
   ```json
   {
     "execution_mode": "dynamic|silent|collaborative",
     "mode_selected_by": "user",
     "mode_selection_timestamp": "[ISO-8601]"
   }
   ```

4. **Log mode selection:**
   - Record which mode was chosen
   - Note if default was accepted or explicitly changed
   - Timestamp the selection

5. **Proceed to validation** (Section 1.3)

### 1.3 Parse Specification Files
1. Read and parse `spec_transaction_v3.md`:
   - Extract goal description
   - Extract all tasks with IDs and descriptions
   - Extract all steps within each task
   - Extract any backups, components, constraints
2. Read and parse `parameters_transaction_v3.toml`:
   - Extract goal description
   - Extract tasks array with all parameters
   - Extract steps with actions, expected outputs
   - Extract logging and verification configuration
3. Store parsed content in memory for validation.

### 1.4 Validate Goal
1. Check that **one and only one goal** exists in both files.
2. Ensure goal description is non-empty and meaningful.
3. Verify goal descriptions match between Markdown and TOML.
4. Warn if goal is excessively vague or ambiguous.

### 1.5 Validate Tasks
1. Ensure at least one task is defined in both files.
2. For each task, verify presence of:
   - Unique task ID `[n]`
   - Non-empty name/description
   - At least one step
   - Valid `critical` flag (true/false)
   - Valid `mode` setting (silent/collaborative)
   - Defined `max_retries` value (≥ 0)
3. Check for duplicate task IDs.
4. Warn if task count is unusually small (< 1) or large (> 20).

### 1.6 Validate Steps
1. For each step within each task, verify:
   - Unique step ID `[m]` within that task
   - Non-empty action description
   - Expected output defined
2. Check for duplicate step IDs within the same task.
3. Warn if any step lacks clear expected output.
4. Flag steps with ambiguous or incomplete instructions.

### 1.7 Validate Backups (if applicable)
1. Check that backups exist for critical steps or where flagged.
2. Ensure backup descriptions are non-empty.
3. Warn if a critical step has no backup defined.
4. Verify backup IDs are unique and properly referenced.

### 1.8 Bridging Verification (Markdown ↔ TOML)
1. Confirm every task in `spec_[descriptor].md` exists in `parameters_[descriptor].toml`.
2. Confirm every step in Markdown has a corresponding TOML entry.
3. Verify task and step IDs match exactly between files.
4. Check that task sequence order is consistent.
5. If backups exist, confirm they are represented in both files.
6. Generate detailed report listing any:
   - Missing tasks or steps
   - Mismatched IDs
   - Inconsistent descriptions or parameters

### 1.9 Validate Components and Constraints (if applicable)
1. Ensure all components referenced in steps exist in components section.
2. Ensure all constraints referenced are properly defined.
3. Check for unused components or constraints (optional warning).
4. Verify referential integrity across the specification.

### 1.10 Validation Summary and Pre-Flight Check
1. Compile all validation findings into human-readable report:
   - Critical errors (block execution)
   - Warnings (proceed with caution)
   - Information (non-blocking notices)
2. Categories to report:
   - Missing or mismatched tasks/steps
   - Structural inconsistencies between Markdown and TOML
   - Missing or unused components/constraints
   - Ambiguous instructions or descriptions
3. If **critical errors** detected:
   - Log all errors to progress file.
   - Switch to **collaborative** mode.
   - Halt execution and prompt for resolution.
4. If **only warnings** detected:
   - Log warnings to progress file.
   - Optionally prompt in collaborative mode for acknowledgement.
   - Proceed if user confirms or system configured to continue.
5. If **validation passes**:
   - Log successful validation.
   - Mark progress log status as `ready_for_execution`.
   - Proceed to Execution Flow (Section 2).

---

**Initialization Complete**: All files validated, log initialized, ready for sequential task execution.

---

## 2. Execution Flow

### 2.0 Constitutional Compliance Check (Per Task)

**Before executing each task**, verify ongoing constitutional compliance per `commander_SPEC/constitution.md`:

#### Article IV Check: Error Propagation Functioning
1. Verify `error_propagation.enabled = true` in TOML
2. Check that `read_prior_steps = true`
3. Confirm dependency_tracking is active
4. **If disabled:** Log constitutional violation (Article VIII), escalate to collaborative

#### Article VI Check: Critical Flag Balance
1. Count critical vs non-critical steps in upcoming task
2. Calculate criticality ratio for this task
3. **If all steps critical (100%):** Log warning (Article VI - over-criticality)
4. **If no steps critical (0%):** Log warning (Article VI - under-criticality), unless single-step task
5. Record in progress.json:
   ```json
   "constitutional_checks": {
     "task_id": 1,
     "critical_balance": {
       "critical_count": 3,
       "total_count": 5,
       "ratio": 0.60,
       "compliant": true
     }
   }
   ```

#### Article VIII Check: Prior Step Outcomes Read
1. Before executing Step 1 of any task (except Task 1):
   - Verify prior task's final step outcome was read
   - Check for critical failures in prior tasks
   - **If not read:** Log constitutional violation (Article VIII)
   - Halt and request corrective action

#### Article X Check: Comprehensive Logging Active
1. Verify last step recorded all required fields:
   - task_id, step_id, status, method_used
   - backup_attempts (if backups attempted)
   - timestamp, mode
2. **If incomplete:** Log constitutional violation (Article X)
3. Continue but flag for post-execution review

#### Constitutional Violation Logging
Track violations in progress.json:
```json
"constitutional_compliance": {
  "violations_detected": [
    {
      "article": "VI",
      "section": "6.3",
      "description": "Task 2 has 100% critical steps (over-criticality)",
      "task_id": 2,
      "severity": "warning",
      "timestamp": "[ISO-8601]",
      "corrective_action": "Continue with warning logged"
    }
  ],
  "checks_performed": 4,
  "violations_critical": 0,
  "violations_warning": 1
}
```

**Enforcement Decision:**
- **Critical violations:** Halt task, escalate to collaborative mode
- **Warning violations:** Log and continue, include in post-execution review

---

### 2.1 Task Iteration

1. For each **Task** in `parameters_[descriptor].toml` (ordered by `id`):
   - Perform Constitutional Compliance Check (Section 2.0)
   - Log Task start event  
   - Read its description and mode

2. For each **Step** within that Task:
   
   ### 2.2 Pre-Step Error Propagation Check
   - **Read `progress_[descriptor].json`** for prior step outcomes
   - Check if any prior **critical steps** in this or previous tasks failed
   - If critical failure detected:
     - Evaluate impact on current step (dependency analysis)
     - Options based on `error_propagation.propagation_strategy`:
       - `halt_on_critical`: Stop execution, escalate to collaborative mode
       - `continue_and_log`: Proceed with warning flag, log dependency concern
       - `collaborative_review`: Pause and request human decision
   - Log propagation decision in progress file
   
   ### 2.3 Step Execution with Backup Selection
   - Log `start` event with timestamp
   - **Attempt primary method** as defined by `action`
   - If successful:
     - Log `step_complete` with expected output summary
     - Verify output matches `expected_output` definition
     - Proceed to next step
   
   - If failure detected:
     - Increment retry count for primary method
     - **Attempt Backup Method Selection (Section 2.5)**
     - Log each backup attempt with method ID
   
   ### 2.4 Retry and Mode Escalation Logic
   - If primary method fails and backups exist:
     - Execute backups in sequence (backup[1], then backup[2])
     - Log each backup attempt separately
   - If all methods exhausted (primary + all backups):
     - Check `critical_flag`:
       - If `critical = true`:
         - Increment consecutive failure counter
         - Switch to **collaborative mode**
         - Prompt for human instruction
         - Log mode switch, attempted methods, and user response
       - If `critical = false`:
         - Log failure as warning
         - Continue to next step
   - If consecutive failures reach `error_propagation.failure_threshold`:
     - Escalate to collaborative mode regardless of individual step criticality

3. When all Steps complete:
   - Mark Task as `complete`.
   - Log task summary (steps succeeded, retries, mode switches, backups used).
   - Reset consecutive failure counter for next task.

4. Continue sequentially to next Task.
   - Parallel execution is **not** supported.

---

## 2.6 Backup Method Selection

When a step's primary method fails:

1. **Check if backups are defined** for this step in `parameters_[descriptor].toml`
   - Look for `[[tasks.steps.backups]]` entries

2. **Execute backups sequentially:**
   - Attempt `backup[id=1]` (first alternative approach)
   - If `backup[1]` fails, attempt `backup[id=2]` (second alternative)
   - Log each backup attempt with:
     - backup_id
     - trigger_condition
     - outcome (success/failure)
     - timestamp

3. **Backup success:**
   - If any backup succeeds:
     - Log successful backup method
     - Mark step as complete via backup
     - Note which backup was used in progress.json
     - Continue to next step

4. **All backups exhausted:**
   - If all backups fail and `critical_flag = true`:
     - Log all attempted methods (primary + all backups)
     - Switch to collaborative mode
     - Present summary of attempts to human
     - Request guidance or alternative approach
   - If all backups fail and `critical_flag = false`:
     - Log warning with all attempts
     - Continue execution (step marked as failed but non-blocking)

5. **No backups defined:**
   - If step has no backups and `critical_flag = true`:
     - Escalate immediately to collaborative mode
   - If step has no backups and `critical_flag = false`:
     - Log failure and continue

**Note:** Backups represent **alternative reasoning paths or methods**, not simple retries of the same approach.

---

## 3. Mode Control

### Silent Mode
- Executes all instructions autonomously.
- Only raises alerts if a critical failure persists beyond retries.

### Collaborative Mode
- Prompts for human input before proceeding after persistent failure or ambiguity.
- Records both prompt and response in log.

### Dynamic Mode
Adaptive switching between Silent and Collaborative based on failure patterns and confidence signals.

**When to Enable:** Set explicitly in parameters_[descriptor].toml if workflow requires intelligent escalation.

**Triggers for Mode Escalation:**
1. **Consecutive Failures Pattern:**
   - Track last N steps (configurable, default N=5)
   - If 3+ consecutive step failures (regardless of backups): escalate to collaborative
   - Reset counter on successful step completion

2. **Backup Depletion Pattern:**
   - If same backup method used successfully 3+ times: suggest collaborative review of approach
   - If backups consistently failing: escalate for strategy reassessment

3. **Confidence Degradation:**
   - If step output quality decreases (based on verification checks)
   - If expected outputs increasingly mismatched
   - If retries increasing per step over time

4. **Critical Failure Threshold:**
   - From `error_propagation.failure_threshold` in TOML
   - Absolute escalation point regardless of individual step settings

**Dynamic Mode Logic:**
```
IF consecutive_failures >= 3 OR 
   backup_depletion_detected OR 
   failure_count >= error_propagation.failure_threshold OR
   confidence_score < threshold:
   
   THEN switch_to_collaborative_mode()
   LOG escalation_reason
   REQUEST human_guidance
```

Mode changes are always logged with:
- timestamp  
- originating task and step  
- cause of switch (failure pattern, confidence drop, threshold breach)
- attempted methods summary
- current consecutive failure count

---

## 4. Verification Layer

### 4.1 Per-Step Verification
After each step execution:
1. **Verify expected output:**
   - Compare actual output against `expected_output` field in TOML
   - Log verification outcome (match/mismatch)
   
2. **Check constraint satisfaction:**
   - Validate against constraints defined in parameters_[descriptor].toml
   - Log any constraint violations
   
3. **Validate backup usage:**
   - If backup was used, confirm it's properly documented
   - Verify backup trigger conditions were met

### 4.2 Per-Task Verification
After each Task:
1. Confirm all Steps marked complete or appropriately failed.
2. Cross-check task and step IDs against TOML definitions.
3. Verify error propagation was handled correctly:
   - Check that dependent steps acknowledged prior failures
   - Confirm propagation decisions were logged
4. If discrepancies found:
   - Log verification failure with details
   - Attempt automated resolution (e.g., realignment by ID)
   - If unresolved, trigger collaborative review

### 4.3 Error Propagation Verification
Before marking task complete:
1. **Review propagation decisions:**
   - Confirm all critical failures were properly escalated
   - Verify non-critical failures were logged appropriately
   
2. **Check dependency chain:**
   - Ensure downstream steps that depended on failed steps handled the failure
   - Validate propagation_strategy was followed consistently
   
3. **Validate failure threshold tracking:**
   - Confirm consecutive failure counter is accurate
   - Verify escalations occurred at correct thresholds

### 4.4 Run End Verification
At run end:
- Validate all Tasks in `parameters_[descriptor].toml` are marked as complete in `progress_[descriptor].json`
- Check for orphaned or skipped steps
- Verify all error propagation events were properly handled
- Confirm all mode switches were logged
- If incomplete:
  - Summarize pending tasks and steps
  - List all critical failures that blocked completion
  - Flag as partial completion with reason codes

---

## 5. Logging and Reporting

All activity is recorded in `progress_[descriptor].json` with entries for:
- task_id  
- step_id  
- status (started, completed, retried, failed, skipped)  
- retry_count  
- timestamp  
- mode (current execution mode for this step)
- method_used (primary, backup_1, backup_2, etc.)
- backup_attempts (array of attempted backup IDs)
- error_propagation_decision (if applicable)
- prior_step_dependencies (array of step IDs this step read)
- constraint_status (pass/fail for each constraint)
- expected_output_match (boolean)
- message or error detail  
- consecutive_failure_count (for dynamic mode tracking)

**Enhanced Logging for Error Propagation:**
- Log whenever a step reads progress.json for prior results
- Log propagation decisions (halt, continue, escalate)
- Track dependency chains between steps
- Record impact assessments when critical failures occur

**Enhanced Logging for Backup Usage:**
- Log each backup attempt separately
- Record trigger conditions for backup activation
- Track which backup method succeeded (if any)
- Note if all backups exhausted before escalation

At completion:
1. Write final summary:
   - Total tasks completed / attempted
   - Steps succeeded / failed / skipped
   - Total retries across all steps
   - Backup methods used (count per backup type)
   - Critical errors encountered with step locations
   - Mode switches with reasons and timestamps
   - Error propagation events and decisions
   - Runtime duration
   - Final consecutive failure count
2. Mark log as `run_complete = true`.
3. Add completion metadata:
   - Overall success status
   - Partial completion flags if applicable
   - List of unmet dependencies or blocked steps

---

## 6. Finalization

- Print or return summary report.
- Optionally archive the Spec folder for audit (`/Specs/[descriptor]/archive_[date]/`).
- Ensure all logs are time-stamped and immutable post-completion.

---

## 6. Post-Execution Analysis

**After completing all tasks OR on critical halt**, perform comprehensive analysis:

### 6.1 Failure Pattern Analysis

Analyse execution history from progress.json to identify patterns and learnings:

#### Step 1: Identify Failure Patterns
1. **Scan all step outcomes** for failures
2. **Count failure frequency** per step:
   - Which steps failed most often?
   - Were failures isolated or clustered in specific tasks?
3. **Track retry patterns:**
   - How many retries were needed per step?
   - Did retries succeed or did backups resolve failures?
4. **Calculate failure rates:**
   - Overall: `failed_steps / total_steps`
   - Per task: `failed_steps_in_task / total_steps_in_task`

#### Step 2: Analyse Backup Effectiveness
1. **Identify successful backups:**
   - Which backup methods succeeded?
   - How often did backup[1] vs backup[2] resolve failures?
2. **Track backup usage frequency:**
   - Which steps used backups most?
   - Were backups genuine alternatives or just retries? (Constitutional Article VII check)
3. **Calculate backup success rate:**
   - `successful_backups / total_backup_attempts`
4. **Recommend backup improvements:**
   - If backup[1] always fails but backup[2] succeeds → promote backup[2] to primary
   - If no backups succeeded → suggest new alternative approaches

#### Step 3: Mode Escalation Analysis
1. **Count mode switches:**
   - How many times did dynamic mode escalate to collaborative?
   - What triggered escalations? (consecutive failures, backup depletion, confidence degradation)
2. **Evaluate escalation appropriateness:**
   - Were escalations justified? (critical failures, method exhaustion)
   - Were there false escalations? (over-cautious thresholds)
3. **Track escalation triggers:**
   ```json
   "escalation_analysis": {
     "total_escalations": 2,
     "triggers": {
       "consecutive_failures": 1,
       "backup_depletion": 0,
       "confidence_degradation": 0,
       "critical_failure": 1
     }
   }
   ```

#### Step 4: Dependency and Error Propagation Analysis
1. **Verify error propagation functioned correctly:**
   - Did downstream steps read prior step outcomes?
   - Were critical failures properly halted or escalated?
2. **Identify dependency issues:**
   - Did any step depend on failed upstream step?
   - How was the dependency handled?
3. **Track propagation decisions:**
   - How many times was `halt_on_critical` invoked?
   - How many times did `continue_and_log` proceed despite failures?

#### Step 5: Generate Recommendations
Based on patterns identified, generate actionable recommendations:

**Critical Flag Adjustments:**
- "Consider marking Step 2.3 as non-critical (failed 3 times but goal still achievable)"
- "Consider marking Step 1.1 as critical (failure blocked downstream steps)"

**Backup Improvements:**
- "Backup method 'inspect source code' succeeded 100% of the time, prioritise it"
- "Primary method for Step 3.2 failed consistently, replace with current backup[1]"

**Mode Configuration:**
- "3 consecutive failures triggered escalation twice, consider increasing threshold to 4"
- "Backup depletion never triggered escalation, current coverage is good"

**Spec Structure:**
- "Task 2 had 5 steps, 4 failed - consider breaking into smaller sub-tasks"
- "Overall critical flag balance: 58% (within 40-60% guideline, compliant)"

### 6.2 Constitutional Compliance Review

Review constitutional adherence per `commander_SPEC/constitution.md`:

#### Article VI Review: Critical Flag Balance
1. **Calculate overall critical balance:**
   - Total critical steps / Total steps
   - Per-task critical ratios
2. **Evaluate appropriateness:**
   - Was 40-60% guideline met?
   - Were critical steps appropriately designated? (failures actually blocked goal)
   - Were non-critical steps appropriately designated? (failures didn't block goal)
3. **Recommendation:** Adjust critical flags based on actual execution outcomes

#### Article VII Review: Backup Quality
1. **Review each backup used:**
   - Was it a genuine alternative reasoning path?
   - Or was it just a retry? (Constitutional violation)
2. **Scan backup descriptions:**
   - "Try again" → violation
   - "Use alternative tool X" → compliant
3. **Log violations:**
   ```json
   "constitutional_violations": {
     "article": "VII",
     "description": "Step 2.3 backup[1] was simple retry, not alternative method",
     "severity": "warning"
   }
   ```

#### Article VIII Review: Error Propagation
1. **Verify prior step outcomes were read:**
   - Did each step check progress.json before executing?
   - Were dependencies handled correctly?
2. **Check propagation strategy effectiveness:**
   - Did chosen strategy (halt_on_critical, continue_and_log, collaborative_review) work well?
   - Should strategy be changed for future runs?

#### Article IX Review: Mode Escalation
1. **Evaluate dynamic mode performance:**
   - Were escalations appropriate and timely?
   - Were there missed escalations (should have escalated but didn't)?
   - Were there false escalations (escalated unnecessarily)?
2. **Review escalation thresholds:**
   - Was consecutive_failure_threshold appropriate?
   - Was backup_depletion_threshold appropriate?

#### Article X Review: Logging Completeness
1. **Verify all required fields logged:**
   - task_id, step_id, status, method_used
   - backup_attempts, timestamp, mode
   - error_propagation_decisions
2. **Check for gaps or incomplete entries**
3. **Confirm immutability** (no entries modified post-write)

### 6.3 Append Analysis to Progress.json

Add comprehensive analysis section to progress.json:

```json
"post_execution_analysis": {
  "timestamp": "[ISO-8601]",
  "failure_patterns": {
    "steps_that_frequently_fail": [
      {"step_id": "2.3", "failure_count": 3, "retry_count": 6}
    ],
    "overall_failure_rate": 0.17,
    "most_successful_backups": [
      {"backup_description": "inspect source code", "success_rate": 1.0},
      {"backup_description": "use alternative linter", "success_rate": 0.67}
    ],
    "backup_success_rate": 0.75
  },
  "mode_escalation_analysis": {
    "total_escalations": 2,
    "escalation_triggers": {
      "consecutive_failures": 1,
      "critical_failure": 1
    },
    "false_escalations": 0,
    "missed_escalations": 0
  },
  "constitutional_compliance_review": {
    "article_vi_critical_balance": {
      "overall_ratio": 0.58,
      "compliant": true,
      "recommendation": "Balance is appropriate"
    },
    "article_vii_backup_quality": {
      "violations": 1,
      "description": "Step 2.3 backup was simple retry"
    },
    "article_viii_error_propagation": {
      "functioning_correctly": true
    },
    "article_ix_mode_escalation": {
      "appropriate_escalations": 2,
      "threshold_adjustment_needed": false
    },
    "article_x_logging": {
      "complete": true,
      "immutable": true
    },
    "overall_compliance_score": 92
  },
  "recommendations": [
    "Consider marking Step 2.3 as non-critical",
    "Promote 'inspect source code' backup to primary method for Step 1.2",
    "Replace Step 2.3 backup[1] with genuine alternative (current backup is simple retry)",
    "Current mode escalation thresholds are appropriate, no adjustment needed"
  ]
}
```

### 6.4 Deployment Verification (MANDATORY for Build/Create/System Goals)

**Trigger: If goal contains "build", "create", "develop", "system", "application", "app"**

**Execute BEFORE marking goal as ACHIEVED or COMPLETE**

#### Check 1: Runnable System Exists

**For desktop_app:**
- [ ] Executable file exists (.exe for Windows, .app for macOS)
- [ ] OR installer package exists
- [ ] Can be launched by target user without terminal commands
- [ ] Configuration is accessible (wizard, settings file, or hardcoded defaults)

**Test:**
```bash
# Verify these artifacts exist:
ls dist/[app_name].exe         # Windows
ls dist/[app_name].app         # macOS
ls setup/installer.exe         # If installation_type = "installer"
ls config/settings.ini         # Or configuration wizard implemented
```

**For web_app:**
- [ ] Server can be started
- [ ] Application accessible via URL (not localhost-only if production)
- [ ] Deployment package exists (Docker image, zip, etc.)

**For cli:**
- [ ] Executable or package exists
- [ ] Can be run via startup_method defined in TOML
- [ ] Help/usage documentation accessible

**If check fails:**
```json
{
  "deployment_verification": {
    "runnable_system_exists": false,
    "reason": "No executable found, only Python source files",
    "expected": "dist/volunteers_pos.exe per packaging_method=pyinstaller",
    "found": "src/*.py files only",
    "status": "FAIL"
  }
}
```

#### Check 2: User Interface Exists (if user_interface.required = true)

- [ ] GUI/Web interface implemented (not just backend modules)
- [ ] All user stories can be tested through the interface
- [ ] Target users can interact without command-line knowledge
- [ ] No "edit config file manually" required for core workflows

**Verify:**
- Launch the system as target user would
- Complete primary task using only the interface
- Check that skill_level requirement is met (if "none", must be usable by non-technical person)

**If check fails:**
```json
{
  "deployment_verification": {
    "user_interface_implemented": false,
    "reason": "Backend functions exist but no GUI",
    "user_interface_required": true,
    "target_users": "charity shop volunteers",
    "skill_level_required": "none",
    "status": "FAIL"
  }
}
```

#### Check 3: Production Ready (if completion_criteria.production_ready = true)

- [ ] Real APIs configured (not test mode simulators)
- [ ] External services connected (databases, payment processors, hardware)
- [ ] Production credentials present OR configuration wizard implemented
- [ ] Error recovery for network/hardware failures implemented

**Verify:**
- Search code for test_mode flags → must be false or configurable
- Check API client initialization → must use production endpoints
- Verify fallback/retry logic exists for external dependencies

**Example validation:**
```python
# BAD - Test mode only:
if self.test_mode:
    return mock_response()

# GOOD - Production capable:
if self.api_key and self.production_endpoint:
    return real_api_call()
else:
    raise ConfigurationError("Production API not configured")
```

**If check fails:**
```json
{
  "deployment_verification": {
    "production_ready": false,
    "issues": [
      "Square API in test mode only (payment_processor.py:45)",
      "No production endpoint configured",
      "API key not configurable by user"
    ],
    "status": "FAIL"
  }
}
```

#### Check 4: User Documentation Exists

- [ ] Installation instructions for target users (not developers)
- [ ] Configuration guide (if configuration_required not empty)
- [ ] Usage instructions for primary workflows
- [ ] Troubleshooting common errors

**Required documents:**
- `README.md` or `USER_GUIDE.md` for end users
- `INSTALL.md` if installation steps needed
- In-app help or tooltips (if GUI)

**If check fails:**
```json
{
  "deployment_verification": {
    "user_documentation_exists": false,
    "found": ["README.md for developers", "API documentation"],
    "missing": ["User installation guide", "Volunteer workflow instructions"],
    "status": "FAIL"
  }
}
```

#### Final Deployment Verdict

**If ALL checks PASS:**
```json
{
  "deployment_verification": {
    "runnable_system_exists": true,
    "user_interface_implemented": true,
    "production_ready": true,
    "user_documentation_exists": true,
    "overall_status": "PASS",
    "goal_achievement_status": "ACHIEVED"
  }
}
```

**If ANY check FAILS:**
```json
{
  "deployment_verification": {
    "overall_status": "FAIL",
    "goal_achievement_status": "PARTIAL",
    "reason": "Core logic works but system not deployable",
    "gaps": [
      "No volunteers_pos.exe - Python scripts only",
      "No volunteer GUI - command-line only",
      "Square API in test mode",
      "No user installation guide"
    ],
    "recommendation": "Mark goal as PARTIAL. Backend complete but deployment incomplete."
  }
}
```

**Critical Rule:** 
- Goal status = ACHIEVED only if deployment_verification.overall_status = PASS
- Goal status = PARTIAL if deployment_verification.overall_status = FAIL but core logic works
- Goal status = NOT ACHIEVED if core logic broken

**Log to progress.json and include in post-execution analysis**

### 6.5 Learning for Future Specs

Document key learnings to inform future spec creation:

1. **Effective patterns identified:**
   - Backup methods that consistently worked
   - Step structures that completed without issues
   - Dependency patterns that propagated correctly

2. **Anti-patterns to avoid:**
   - Step structures that consistently failed
   - Backup methods that didn't provide genuine alternatives
   - Critical flag assignments that were inappropriate

3. **System tuning insights:**
   - Optimal consecutive_failure_threshold
   - Effective propagation_strategy for this domain
   - Appropriate critical flag balance for this type of goal

**Action:** Store learnings in `_filing/execution_learnings_[date].md` for reference

---

## 7. Notes for Adaptation

- Designed for sequential task execution only.
- Compatible with LLM collaborative workflows or automated interpreters.
- Extensible for continuous integration by linking `exe_[descriptor].md` calls to post-generation pipelines.
- Reuse by copying and renaming according to project descriptor (e.g., `exe_debug.md`).

---

## Sequential Multi-Task Workflow Reference
+------------------+
|      GOAL        |
| "Review & test   |
| module"          |
+--------+---------+
         |
         v
+------------------+
|   TASK [1]       |
| "Research        |
| functionality"   |
+--------+---------+
         |
         v
+-------------------------+
|      STEP [1.1]         |
| Extract specifications   |
| critical_flag?           |
| mode = silent            |
+--------+----------------+
         |
         v
+-------------------------+
|      BACKUP [1.1.1]     |
| Triggered if step fails |
| Alternative reasoning   |
+--------+----------------+
         |
         v
+-------------------------+
| LOGGING STEP [1.1]      |
| Append to progress.json |
+--------+----------------+
         |
         v
+-------------------------+
| DYNAMIC MODE EVAL [1.1] |
| Escalate if critical &  |
| failure                 |
+--------+----------------+
         |
         v
+-------------------------+
| ERROR PROPAGATION [1.1] |
| Update downstream steps |
+--------+----------------+
         |
         v
+-------------------------+
| Continue Steps 1.2–1.n  |
| Repeat backup, logging, |
| mode eval, error prop    |
+--------+-----------------+
         |
         v
+------------------+
|   TASK [2]       |
| "Create automated|
| tests"           |
+--------+---------+
         |
         v
+-------------------------+
| STEP [2.1] … STEP [2.n] |
| Handle sequentially with |
| backup, logging, mode,   |
| error propagation        |
+--------+----------------+
         |
         v
+------------------+
|   TASK [3]       |
| "Etc..."         |
+--------+---------+
         |
         v
+------------------+
| SPEC COMPLETED   |
| Goal achieved    |
+------------------+


*End of exe_template.md*
