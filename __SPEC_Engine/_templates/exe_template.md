# exe_template.md

**Version:** 1.3  
**Last Updated:** 2025-11-03  
**Purpose:** Execution controller template for interpreting and executing specs

---

## [root]/Specs/[descriptor]/

---

### [META]
- **File Role:** Execution controller — reads and interprets both `spec_[descriptor].md` and `parameters_[descriptor].toml` to coordinate task execution.  
- **Created by:** `commander-spec.md`  
- **Mode:** Default = `silent`  
- **Logging:** Writes to `progress_[descriptor].json`  
- **Descriptor Example:** research, debug, prototype, test, etc.

---

## 1. Initialization and Validation

### 1.1 File Presence Check
1. Confirm presence of required files:
   - `spec_[descriptor].md`
   - `parameters_[descriptor].toml`
2. If either file is missing:
   - Log critical error.
   - Halt execution and prompt in **collaborative** mode for resolution.

### 1.1a Software Stack Validation (MANDATORY for Build/Create/System Goals)

**Trigger: If goal description relates to or requires software development**

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
1. Check if `progress_[descriptor].json` exists.
2. If not, create with initial structure:
   ```json
   {
     "run_id": "[timestamp]",
     "descriptor": "[descriptor]",
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
1. Read and parse `spec_[descriptor].md`:
   - Extract goal description
   - Extract all tasks with IDs and descriptions
   - Extract all steps within each task
   - Extract any backups, components, constraints
2. Read and parse `parameters_[descriptor].toml`:
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

### 1.8a SPECLet Validation (if applicable)

**Trigger:** If `[[speclets]]` array exists in parameters_[descriptor].toml

**Purpose:** Validate SPECLet structure, dependencies, and prevent circular dependencies

**Process:**

1. **Parse SPECLet structure from both files:**
   - Extract all SPECLets from Markdown (sections like "### SPECLet [id]: Description")
   - Extract all SPECLets from TOML (`[[speclets]]` entries)
   - Store in memory for validation

2. **Verify Markdown ↔ TOML synchronisation for SPECLets:**
   - Confirm every SPECLet in Markdown has corresponding TOML entry
   - Confirm every SPECLet in TOML has corresponding Markdown section
   - Verify SPECLet IDs match exactly between files
   - Check that SPECLet descriptions are consistent
   - Verify `depends_on` arrays match between files
   - Confirm `tasks` arrays reference valid task IDs

3. **Validate dependency relationships:**
   
   a. **Check dependency references:**
   - For each SPECLet's `depends_on` array, verify all referenced SPECLet IDs exist
   - Example: If `discovery_stage.depends_on = ["platform_foundation"]`, confirm `platform_foundation` SPECLet exists
   
   b. **Detect circular dependencies:**
   - Build dependency graph
   - Perform cycle detection using depth-first search
   - Example of PROHIBITED circular dependency:
     ```
     platform_foundation → depends_on: ["test_stage"]
     test_stage → depends_on: ["discovery_stage"]
     discovery_stage → depends_on: ["platform_foundation"]
     ```
   - If cycle detected: CRITICAL ERROR, HALT execution
   
   c. **Validate dependency feasibility:**
   - Ensure no SPECLet depends on itself
   - Verify dependency chains are finite and resolvable
   - Check for orphaned SPECLets (not part of any valid execution path)

4. **Validate task assignments:**
   - Confirm each task ID appears in exactly ONE SPECLet's `tasks` array
   - Verify all task IDs are assigned to a SPECLet
   - Flag duplicate task assignments (CRITICAL ERROR)
   - Flag unassigned tasks (CRITICAL ERROR)

5. **Verify parallel execution flags:**
   - Check that `parallel_allowed` is boolean (true/false)
   - Validate that SPECLets marked parallel_allowed=true have no conflicting dependencies
   - Warn if all SPECLets have parallel_allowed=false (suggests unnecessary SPECLet complexity)

6. **Build execution order graph:**
   - Create topological sort of SPECLets based on dependencies
   - Identify which SPECLets can execute in parallel at each stage
   - Store execution plan in progress.json for reference during execution
   
   **Example execution plan:**
   ```json
   {
     "speclet_execution_plan": {
       "stage_1": {
         "speclets": ["platform_foundation"],
         "parallel": false,
         "description": "Initial stage - no dependencies"
       },
       "stage_2": {
         "speclets": ["discovery_stage", "define_stage"],
         "parallel": true,
         "description": "Both depend only on platform_foundation"
       },
       "stage_3": {
         "speclets": ["ideate_stage"],
         "parallel": false,
         "description": "Depends on define_stage from stage 2"
       },
       "stage_4": {
         "speclets": ["test_stage"],
         "parallel": false,
         "description": "Final validation stage"
       }
     }
   }
   ```

7. **Generate SPECLet validation report:**
   - Total SPECLets defined
   - Dependency relationships validated
   - Circular dependency check: PASS/FAIL
   - Task assignment check: PASS/FAIL
   - Execution stages identified
   - Parallel execution opportunities

8. **Handle validation failures:**
   
   **CRITICAL ERRORS (HALT execution):**
   - Circular dependency detected
   - SPECLet referenced in `depends_on` doesn't exist
   - Task assigned to multiple SPECLets
   - Tasks exist without SPECLet assignment
   - SPECLet exists in TOML but not Markdown (or vice versa)
   
   **WARNINGS (log but continue):**
   - All SPECLets marked parallel_allowed=false (suboptimal)
   - Complex dependency chains (>4 levels deep)
   - Single SPECLet defined (suggests simple spec structure would suffice)

9. **Log validation results:**
   ```json
   {
     "speclet_validation": {
       "speclets_defined": 6,
       "dependency_graph_valid": true,
       "circular_dependencies_detected": false,
       "task_assignment_valid": true,
       "execution_stages": 4,
       "parallel_opportunities": 1,
       "validation_status": "PASS"
     }
   }
   ```

10. **If validation passes:**
    - Log successful SPECLet validation
    - Store execution plan in progress.json
    - Proceed to Section 1.9
    
**If validation fails:**
- Log all critical errors
- Display detailed error messages with SPECLet IDs and specific issues
- Switch to collaborative mode
- HALT execution until resolved

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
   - Proceed to MCP Tool Verification (Section 1.11).

---

### 1.11 MCP Tool Verification (Safety Check)

**Purpose:** Verify that MCP tools installed during SPEC creation (Step 3a) are still available.

**Expected outcome:** All checks should PASS (tools were already installed during creation).

**Process:**

1. **Read tool configuration from parameters_[descriptor].toml**
   ```
   required_tools = parameters.toml["mcp_tools"]["required"]
   recommended_tools = parameters.toml["mcp_tools"]["recommended"]
   optional_tools = parameters.toml["mcp_tools"]["optional"]
   verification_settings = parameters.toml["mcp_tools"]["verification"]
   ```

2. **Check if tool verification is enabled**
   - If `verification_settings.check_on_startup = false`:
     - Log: "MCP tool verification disabled in configuration"
     - Skip verification, proceed to Section 2
   - If `verification_settings.check_on_startup = true`:
     - Continue to step 3

3. **Verify REQUIRED tools**
   
   For each tool in `required_tools` list:
   - Attempt to detect MCP server availability
     - Method: Check if MCP server responds/is configured
     - Platform-specific: Verify MCP client configuration
   
   **If tool is AVAILABLE:**
   - Log success: `"✅ REQUIRED tool '{tool_name}' verified"`
   - Add to verified list in progress.json
   
   **If tool is MISSING:**
   - Log error: `"❌ REQUIRED MCP server '{tool_name}' not available"`
   - Check spec_[descriptor].md for installation command
   - Display detailed error message:
     ```
     ═══════════════════════════════════════════════════════════════
     ❌ REQUIRED TOOL MISSING
     ═══════════════════════════════════════════════════════════════
     
     Tool: {tool_name}
     Status: Not detected
     
     This tool was marked as REQUIRED during SPEC creation but is
     not currently available.
     
     Possible causes:
     - Tool was not installed during Step 3a
     - MCP client configuration is missing this server
     - MCP client was not restarted after installation
     - Tool was uninstalled since SPEC creation
     
     Installation command:
     {install_command from spec.md}
     
     Configuration location:
     - Windows: %APPDATA%\Claude\claude_desktop_config.json
     - macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
     - Linux: ~/.config/Claude/claude_desktop_config.json
     
     ACTION REQUIRED:
     1. Install the tool using the command above
     2. Add server configuration to your MCP client config
     3. Restart your MCP client
     4. Re-run this executor
     
     ═══════════════════════════════════════════════════════════════
     ```
   - If `verification_settings.halt_if_required_missing = true`:
     - **HALT execution immediately**
     - Do NOT proceed to Section 2
     - Exit with error status
   - If `verification_settings.halt_if_required_missing = false`:
     - Log warning but continue (not recommended)

4. **Verify RECOMMENDED tools**
   
   For each tool in `recommended_tools` list:
   - Attempt to detect MCP server availability
   
   **If tool is AVAILABLE:**
   - Log success: `"✅ RECOMMENDED tool '{tool_name}' verified"`
   - Add to verified list in progress.json
   
   **If tool is MISSING:**
   - If `verification_settings.warn_if_recommended_missing = true`:
       - Log warning: `"⚠️ RECOMMENDED MCP server '{tool_name}' not available"`
       - Display installation information:
         ```
         ⚠️ RECOMMENDED TOOL MISSING: {tool_name}
         
         This tool was recommended during SPEC creation but is not available.
         Execution will continue, but efficiency may be reduced.
         
         Install: {install_command from spec.md}
         Rationale: {rationale from spec.md}
         Alternative: {alternative approach from spec.md}
         ```
   - **Continue execution** (do not halt)
   - Add to missing_recommended list in progress.json

5. **Log OPTIONAL tools** (informational only, no verification required)
   
   For each tool in `optional_tools` list:
   - Log info: `"ℹ️ OPTIONAL tool '{tool_name}' listed (not verified)"`
   - Do NOT attempt detection
   - Do NOT warn if missing

6. **Update progress_[descriptor].json with verification results**
   ```json
   {
     "mcp_tools_verification": {
       "verification_enabled": true,
       "verification_timestamp": "2025-11-03T12:00:00Z",
       "required_tools": {
         "total": 2,
         "verified": ["postgres", "github"],
         "missing": []
       },
       "recommended_tools": {
         "total": 1,
         "verified": ["playwright"],
         "missing": []
       },
       "optional_tools": {
         "total": 1,
         "listed": ["notion"]
       },
       "verification_status": "PASS"
     }
   }
   ```

7. **Determine overall verification status**
   
   **PASS:** All required tools verified
   - Display: `"✅ All required MCP tools verified"`
   - Display: `"✅ Proceeding to execution (Section 2)"`
   - Proceed to Section 2
   
   **FAIL:** One or more required tools missing
   - Display: `"❌ MCP tool verification failed"`
   - Display: `"❌ {n} required tool(s) missing"`
   - If halt_if_required_missing = true: **HALT execution**
   - If halt_if_required_missing = false: Log warning and continue

**Note:** This is a safety check, not initial installation. Tools should have been installed during SPEC creation Step 3a. If verification fails, it indicates a configuration problem, not a spec problem.

**Example Output (Success):**

```
Section 1.11: MCP Tool Verification (Safety Check)
═══════════════════════════════════════════════════

Checking 2 required tools...
  ✅ REQUIRED tool 'postgres' verified
  ✅ REQUIRED tool 'github' verified

Checking 1 recommended tool...
  ✅ RECOMMENDED tool 'playwright' verified

Optional tools (1 listed, no verification required):
  ℹ️ OPTIONAL tool 'notion' listed

═══════════════════════════════════════════════════
✅ All required MCP tools verified
✅ Proceeding to execution (Section 2)
═══════════════════════════════════════════════════
```

**Example Output (Failure):**

```
Section 1.11: MCP Tool Verification (Safety Check)
═══════════════════════════════════════════════════

Checking 2 required tools...
  ✅ REQUIRED tool 'postgres' verified
  ❌ REQUIRED tool 'github' not available

[Detailed error message displayed - see step 3 above]

═══════════════════════════════════════════════════
❌ MCP tool verification failed
❌ 1 required tool missing: github
❌ HALTING EXECUTION
═══════════════════════════════════════════════════
```

---

**Initialization Complete**: All files validated, MCP tools verified, log initialized, ready for sequential task execution.

---

## 2. Execution Flow

### 2.0 Constitutional Compliance Check (Per Task)

**Before executing each task**, verify ongoing constitutional compliance per `__SPEC_Engine/_Constitution/constitution.md`:

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

### 2.0a Pattern-Informed Feasibility Check (if pattern selected)

**Purpose:** Validate implementation approach against selected pattern knowledge

**Trigger:** If pattern was selected during SPEC generation (check for pattern metadata in spec file)

#### Process

1. **Load Pattern Context**
   - Check if spec file contains pattern metadata (usually in header or metadata section)
   - Fields to look for:
     - `pattern_name`: Name of selected pattern
     - `pattern_confidence`: HIGH/MEDIUM/LOW
     - `pattern_technologies`: Recommended technology stack
     - `pattern_reference`: GitHub URL
     - `risk_assessment`: Pattern-based risk level

2. **Verify Technology Alignment**
   - Compare selected software stack with pattern recommendations
   - Check if chosen technologies match pattern.technologies
   - **If mismatch detected:**
     ```
     WARNING: Technology deviation from pattern recommendation
     Pattern recommended: [pattern_technologies]
     Spec specifies: [actual_technologies]
     
     Pattern confidence was: [confidence]
     Risk assessment: Increased from [original_risk] to MEDIUM
     
     OPTIONS:
     [A] Continue anyway (log deviation)
     [B] Escalate to collaborative mode for review
     [C] Suggest alternative patterns with matching tech
     ```

3. **Assess Implementation Risk**
   - Use pattern confidence score to inform risk assessment
   - Calculate composite risk:
     ```
     risk_level = pattern_risk + technology_deviation_penalty + complexity_factor
     
     If risk_level > MEDIUM_THRESHOLD:
       Log warning and suggest backup patterns
     ```

4. **Query Backup Patterns (if needed)**
   - If primary pattern confidence is MEDIUM or LOW
   - Or if technology deviation detected
   - Query knowledge graph for similar patterns:
     ```python
     from pattern_extraction_pipeline.commander_integration import CommanderPatternInterface
     interface = CommanderPatternInterface()
     
     backups = interface.get_backup_suggestions(
         pattern_name=primary_pattern_name,
         top_k=3
     )
     ```
   - Log backup patterns in progress.json:
     ```json
     "pattern_feasibility": {
       "primary_pattern": "...",
       "primary_confidence": "MEDIUM",
       "technology_alignment": "partial",
       "backup_patterns_available": [
         {"name": "...", "confidence": "HIGH", "similarity": 0.82},
         {"name": "...", "confidence": "HIGH", "similarity": 0.78}
       ],
       "risk_assessment": "MEDIUM",
       "recommendation": "Proceed with caution, consider backups if primary fails"
     }
     ```

5. **Pattern-Informed Error Recovery**
   - When step failures occur, check if backup patterns suggest alternative approaches
   - Before attempting generic backup methods, consult pattern backups:
     ```python
     if step_failed and pattern_backups_available:
         alternative_approaches = [
             backup['name'] + ": " + backup['reasoning']
             for backup in pattern_backups[:2]
         ]
         log_message("Pattern-informed alternatives available: " + str(alternative_approaches))
     ```

6. **Log Pattern Feasibility Check**
   ```json
   "constitutional_compliance": {
     "pattern_feasibility_check": {
       "performed": true,
       "pattern_name": "electron_desktop_app",
       "pattern_confidence": "HIGH",
       "technology_alignment": "full",
       "risk_level": "LOW",
       "backup_patterns_loaded": true,
       "timestamp": "[ISO-8601]"
     }
   }
   ```

#### No Pattern Selected (Fallback)

If no pattern was selected during generation:
- Log: "No pattern guidance - using general feasibility assessment"
- Skip this section
- Proceed to Section 2.0b (SPECLet Orchestration)

---

### 2.0b SPECLet Orchestration (if applicable)

**Trigger:** If `speclet_execution_plan` exists in progress.json (created during Section 1.8a validation)

**Purpose:** Coordinate parallel execution of SPECLets according to dependency graph

**Orchestration Logic:**

1. **Load execution plan from progress.json:**
   ```javascript
   execution_plan = progress.json["speclet_execution_plan"]
   stages = execution_plan.stages (stage_1, stage_2, ...)
   ```

2. **For each execution stage (sequential):**
   
   a. **Identify SPECLets for this stage:**
   - Extract `stage.speclets` array
   - Check `stage.parallel` flag
   - Load task IDs for each SPECLet
   
   b. **Check dependency satisfaction:**
   - For each SPECLet in this stage:
     - Verify all SPECLets in `depends_on` array have status = "completed"
     - If any dependency not satisfied: mark SPECLet as "blocked"
     - If all dependencies satisfied: mark SPECLet as "ready"
   
   c. **Execute SPECLets:**
   
   **If stage.parallel = true AND multiple SPECLets ready:**
   - Log: "Stage {n}: Executing {count} SPECLets in parallel"
   - For each ready SPECLet:
     - Update status to "in_progress"
     - Execute all tasks within SPECLet sequentially (Section 2.1)
     - Track completion per SPECLet
     - Update status to "completed" when all tasks finish
   - Wait for all SPECLets in stage to complete before proceeding to next stage
   
   **If stage.parallel = false OR single SPECLet:**
   - Log: "Stage {n}: Executing SPECLet {id} sequentially"
   - Execute SPECLet tasks sequentially (Section 2.1)
   - Update SPECLet status to "completed"
   - Proceed to next stage
   
   d. **Handle failures during parallel execution:**
   - If critical failure in one parallel SPECLet:
     - Continue other parallel SPECLets to completion
     - After stage completes, escalate failure
     - Mark dependent SPECLets in future stages as "blocked"
     - User decision: Skip blocked SPECLets or halt execution?
   
   e. **Update SPECLet status tracking:**
   ```json
   {
     "speclet_progress": {
       "platform_foundation": {
         "status": "completed",
         "started_at": "2025-11-03T12:00:00Z",
         "completed_at": "2025-11-03T12:15:00Z",
         "tasks_completed": [1, 2, 3],
         "tasks_failed": [],
         "execution_time_seconds": 900
       },
       "discovery_stage": {
         "status": "in_progress",
         "started_at": "2025-11-03T12:15:00Z",
         "tasks_completed": [4],
         "tasks_in_progress": [5]
       },
       "test_stage": {
         "status": "not_started",
         "depends_on_status": {
           "discovery_stage": "in_progress",
           "define_stage": "not_started"
         },
         "blocked": true,
         "blocked_reason": "waiting_for_dependencies"
       }
     }
   }
   ```

3. **Dependency status monitoring:**
   - Before starting each SPECLet, verify dependency satisfaction
   - Check `speclet.depends_on` array against `speclet_progress`
   - **Required status:** All dependencies must be "completed"
   - **If blocked:** Log reason and wait or skip based on error propagation strategy

4. **Progress visualization (optional):**
   - Display current stage and SPECLet status
   - Example output:
   ```
   ═══════════════════════════════════════════════════
   SPECLet Execution Progress
   ═══════════════════════════════════════════════════
   
   Stage 1: Initial Setup
     ✅ platform_foundation (completed in 15m)
   
   Stage 2: Core Features (parallel execution)
     🔄 discovery_stage (in progress - Task 4/5)
     🔄 define_stage (in progress - Task 7/8)
   
   Stage 3: Advanced Features
     ⏸️ ideate_stage (blocked - waiting for define_stage)
   
   Stage 4: Final Validation
     ⏸️ test_stage (blocked - waiting for ideate_stage)
   
   Overall: Stage 2 of 4 (50%)
   ═══════════════════════════════════════════════════
   ```

5. **Parallel execution coordination:**
   - If LLM supports concurrent execution: Execute parallel SPECLets simultaneously
   - If LLM requires sequential processing: Execute parallel SPECLets in sequence but track as "could have been parallel"
   - Log execution model used: `"parallel_execution_model": "concurrent"` or `"sequential"`

6. **Error handling across SPECLets:**
   
   **Scenario A: Critical failure in SPECLet with dependencies**
   - Example: `platform_foundation` fails
   - Impact: All dependent SPECLets (`discovery_stage`, `define_stage`, etc.) blocked
   - Action: Mark blocked SPECLets, escalate to user, offer options:
     - [A] Fix platform_foundation and retry
     - [B] Skip blocked SPECLets and continue with independent ones
     - [C] Halt execution entirely
   
   **Scenario B: Critical failure in independent parallel SPECLet**
   - Example: `discovery_stage` fails, `define_stage` succeeds
   - Impact: Only `discovery_stage` and its dependents affected
   - Action: Continue with `define_stage` branch, mark `discovery_stage` branch blocked
   
   **Scenario C: Non-critical failure**
   - Log failure, continue all SPECLets
   - Note partial completion in final report

7. **Post-stage validation:**
   - After each stage completes, verify:
     - All SPECLets in stage reached terminal status (completed/failed)
     - No SPECLets left in "in_progress" state
     - Dependency graph still valid for remaining stages
   - Update overall progress percentage

8. **Completion criteria:**
   - All stages executed
   - All SPECLets either "completed" or explicitly "skipped"
   - No SPECLets left in "blocked" state without user decision
   - Final status logged: ACHIEVED / PARTIAL / NOT_ACHIEVED

**Note:** If NO SPECLets defined (simple spec structure), skip this section entirely and proceed directly to Section 2.1 for sequential task execution.

---

### 2.1 Task Iteration

1. For each **Task** in `parameters_[descriptor].toml` (ordered by `id`):
   - Perform Constitutional Compliance Check (Section 2.0)
   - Log Task start event  
   - Read its description and mode
   - **Check research_enabled flag** (Section 2.1a)

### 2.1a Research-Enabled Mode (if flag set)

**Trigger:** If task has `research_enabled = true` in TOML

**Purpose:** Access external knowledge when LLM's internal knowledge insufficient

**When activated:**
```json
{
  "task_id": "1",
  "research_enabled": true,
  "research_sources": ["web_search", "documentation", "technical_specs"]
}
```

**Execution behaviour:**

1. **Pre-Task Research Phase** (before step execution):
   - Review task description and expected outcomes
   - Identify knowledge gaps (unfamiliar APIs, current standards, domain-specific info)
   - Formulate specific research queries
   - Log research intent

2. **Research Execution:**
   - Execute queries via available MCP tools:
     - `web_search`: Current information, best practices
     - `documentation`: Official docs (if URLs provided in task)
     - `technical_specs`: API specs, RFCs
     - `github_repos`: Implementation examples
     - `academic`: Papers (arXiv, PubMed if available)
   - Synthesize findings from multiple sources
   - Validate information consistency
   - Extract actionable insights

3. **Research Logging:**
   ```json
   {
     "task_id": "1",
     "research_phase": {
       "triggered": true,
       "timestamp_start": "2025-11-02T14:30:00Z",
       "timestamp_end": "2025-11-02T14:32:15Z",
       "queries_performed": [
         "FastAPI authentication best practices 2025",
         "OAuth2 implementation patterns Python"
       ],
       "sources_consulted": [
         "https://fastapi.tiangolo.com/tutorial/security/",
         "https://oauth.net/2/"
       ],
       "key_findings": [
         "OAuth2 with Password flow recommended for internal APIs",
         "JWT tokens standard for stateless auth"
       ],
       "confidence_level": "high"
     }
   }
   ```

4. **Apply Research to Steps:**
   - Steps within task now execute with researched context
   - Primary methods informed by current best practices
   - Expected outputs adjusted if research reveals better approach
   - Backup methods may reference alternative approaches found

5. **Research Cost Tracking:**
   ```json
   {
     "research_cost": {
       "time_seconds": 135,
       "api_calls": 3,
       "tokens_used": 4500
     }
   }
   ```

**When NOT to trigger research:**
- Task has `research_enabled = false` or field missing
- LLM confidence high for task domain
- Speed/cost optimization prioritized
- Task is implementation (not discovery/learning)

**Fallback:** If research tools unavailable, log warning and proceed with existing knowledge

---

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

0. **Pattern-Informed Backup Suggestion (if pattern selected)**
   
   **Before attempting defined backups**, check if pattern knowledge can suggest alternatives:
   
   a. **Check for pattern backups in progress.json:**
   ```json
   "pattern_feasibility": {
     "backup_patterns_available": [
       {"name": "alternative_pattern", "reasoning": "...", "technologies": [...]}
     ]
   }
   ```
   
   b. **If pattern backups exist, evaluate relevance:**
   - Does the backup pattern address the same failure type?
   - Are the technologies compatible with current stack?
   - What is the confidence level of the backup pattern?
   
   c. **Present pattern backup options (if relevant):**
   ```
   PRIMARY METHOD FAILED: [step description]
   
   PATTERN-INFORMED ALTERNATIVES AVAILABLE:
   
   From knowledge graph backup patterns:
   
   1. [backup_pattern_name] (confidence: HIGH, similarity: 0.82)
      Approach: [backup_pattern_reasoning]
      Technologies: [backup_pattern_technologies]
      Reference: [github_url]
   
   2. [backup_pattern_name_2] (confidence: MEDIUM, similarity: 0.75)
      Approach: [backup_pattern_reasoning]
      Technologies: [backup_pattern_technologies]
      
   OPTIONS:
   [A] Try pattern-informed alternative 1
   [B] Try pattern-informed alternative 2
   [C] Use defined backup methods from spec
   [D] Escalate to collaborative mode
   ```
   
   d. **If user selects pattern alternative:**
   - Log the pattern backup selection
   - Adapt the step execution to use the pattern's approach
   - Record success/failure for learning
   
   e. **If pattern alternatives not relevant or user chooses [C]:**
   - Proceed to Step 1 below (use defined backups)
   
   **Note:** Pattern backups represent **proven alternative implementations** from the knowledge graph, distinct from spec-defined cognitive/tool backups.

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

## 2.7 Notepad Update (Knowledge Capture)

After completing each task (or per configured frequency), update the knowledge capture notepad:

### When to Update
Check `[knowledge_capture].update_frequency` in parameters_[descriptor].toml:
- **per_task** (default): Update after each task completion
- **per_step**: Update after each step completion (detailed, verbose)
- **end_only**: Update only at spec completion (minimal)

### Update Process

1. **Reflect on execution outcomes:**
   - What was learned during this task/step?
   - What technical decisions were made and why?
   - Were there any surprises or unexpected challenges?
   - What patterns or connections emerged?

2. **Identify key insights:**
   - **Key Insights:** Discoveries, aha moments, important realizations
   - **Technical Notes:** Implementation details, architectural decisions, trade-offs made
   - **Ideas for Enhancement:** Future improvements, features, optimizations identified
   - **Cross-System Connections:** Links to other projects, reusable patterns, shared components
   - **AI Observations:** What the LLM executor learned from this execution
   - **Human Observations:** Any user feedback or notes (if in collaborative mode)

3. **Format the update:**
   ```markdown
   ### [Task X or Step X.Y] - [Timestamp]
   
   **Insight:** [Key discovery or learning]
   
   **Technical Decision:** [Decision made and rationale]
   
   **Connection:** [Related pattern or project, if any]
   ```

4. **Append to notepad_[descriptor].md:**
   - Open notepad file (create if doesn't exist using notepad_template.md)
   - Append under appropriate section (Key Insights, Technical Notes, etc.)
   - Add entry to Execution Timeline table
   - Save file

5. **Log to progress.json:**
   ```json
   {
     "task_id": "2",
     "notepad_update": {
       "timestamp": "[ISO-8601]",
       "insights_captured": 2,
       "technical_notes": 1,
       "ideas": 1
     }
   }
   ```

### Example Notepad Entry

```markdown
## Key Insights

### Task 2: Database Schema Design - 2026-01-02 14:30

**Insight:** Using JSONB for flexible attributes avoids schema migrations but requires careful indexing strategy.

**Technical Decision:** Chose PostgreSQL JSONB over separate EAV tables because query performance is acceptable for <10k records and schema flexibility is critical for evolving requirements.

**Connection:** This pattern mirrors the approach used in [related_project] - could extract to shared library.
```

### Constitutional Requirement

Per Article XV, Section 15.3:
- Knowledge capture is **MANDATORY** for all spec executions
- Both machine-readable (progress.json) and human-readable (notepad.md) logs must be generated
- Notepad provides cumulative learning across executions and sessions

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

#### 1. Consecutive Failures Pattern (EXPLICIT)
- **Tracking window:** Last N steps (configurable via `escalation_threshold` in TOML, default N=3 for dynamic mode)
- **Trigger condition:** N consecutive step failures (primary + all backups exhausted)
- **Measurement:** Count steps where `status = "failed"` and all backup attempts logged
- **Reset condition:** Any step with `status = "completed"` resets counter to 0
- **Example:** Steps 2.1 (failed), 2.2 (failed), 2.3 (failed) → escalate before 2.4

#### 2. Backup Depletion Pattern (EXPLICIT)
**Definition:** Pattern indicating primary methods are systematically failing, forcing reliance on backups.

**Trigger conditions (any of):**
- **Same backup succeeds repeatedly:** If same backup method used successfully ≥3 times in last 5 steps
  - Measurement: Count `method_used = "backup[1]"` or `"backup[2]"` with same description
  - Reason: Primary method consistently wrong, backup should become primary
  
- **Backup exhaustion rate:** If ≥60% of last 5 steps required backups
  - Measurement: Count steps where `backup_attempts > 0` / total steps in window
  - Reason: Primary methods unreliable across multiple steps
  
- **Backups consistently failing:** If ≥3 consecutive steps exhausted all backups without success
  - Measurement: Count steps where all backups attempted but `status = "failed"`
  - Reason: Alternative reasoning paths not working, need human strategy review

**Example backup depletion:**
```json
{
  "steps_analysed": [
    {"id": "1.1", "method_used": "backup[1]", "status": "completed"},
    {"id": "1.2", "method_used": "backup[1]", "status": "completed"},
    {"id": "1.3", "method_used": "backup[1]", "status": "completed"}
  ],
  "backup_depletion_detected": true,
  "reason": "backup[1] 'inspect source code' used 3 times, primary method 'parse documentation' never succeeds",
  "recommendation": "Escalate for strategy review - consider promoting backup to primary"
}
```

#### 3. Confidence Degradation (EXPLICIT)
**Definition:** Step output quality declining over time, indicating LLM uncertainty or accumulating errors.

**Trigger conditions (any of):**
- **Expected output mismatch rate:** If ≥50% of last 5 steps have `expected_output_match = false`
  - Measurement: Count steps where verification shows output doesn't match spec
  - Reason: LLM producing incorrect outputs repeatedly
  
- **Retry escalation pattern:** If average retries per step increases by ≥50% over 5-step window
  - Measurement: Compare average retries in steps 1-5 vs steps 6-10
  - Example: Steps 1-5 avg 0.4 retries, steps 6-10 avg 0.8 retries → degradation detected
  
- **Constraint violation rate:** If ≥40% of last 5 steps have constraint violations logged
  - Measurement: Count steps with `constraint_status` showing failures
  - Reason: LLM not adhering to specifications consistently

**Example confidence degradation:**
```json
{
  "confidence_analysis": {
    "window": "last_5_steps",
    "expected_output_match_rate": 0.4,  // 2 of 5 matched
    "avg_retries_current": 1.2,
    "avg_retries_previous": 0.6,
    "retry_increase_pct": 100,
    "confidence_degradation_detected": true,
    "trigger": "expected_output_mismatch_rate_above_50_pct"
  }
}
```

#### 4. Critical Failure Threshold (EXPLICIT)
- **Source:** `error_propagation.failure_threshold` in parameters_[descriptor].toml
- **Trigger condition:** Total failures (critical OR non-critical) reaches threshold within task
- **Measurement:** Count all steps with `status = "failed"` in current task
- **Typical values:** 3 for dynamic mode, 5 for silent mode, 2 for high-risk projects
- **Reason:** Absolute safety valve regardless of individual step settings

**Dynamic Mode Escalation Logic:**
```
// Check each trigger with explicit measurements above

IF consecutive_failures >= escalation_threshold OR 
   backup_depletion_detected (as defined in §2 above) OR 
   confidence_degradation_detected (as defined in §3 above) OR
   failure_count >= error_propagation.failure_threshold:
   
   THEN switch_to_collaborative_mode()
   LOG {
     escalation_reason: [which trigger(s) activated],
     measurements: [specific metrics that triggered],
     attempted_methods: [all methods tried],
     recommendation: [suggested action]
   }
   REQUEST human_guidance
```

**All trigger conditions above are measurable** from `progress_[descriptor].json` entries.

Mode changes are always logged with:
- timestamp  
- originating task and step  
- cause of switch (failure pattern, confidence drop, threshold breach)
- attempted methods summary
- current consecutive failure count

### Education Mode

**Behaviour:** Autonomous execution with enhanced learning opportunities and approval gates.

**Philosophy:** Per Article XV (The Slow-Code Principle), understanding over speed when learning matters.

**When to Use:**
- Learning new frameworks or patterns
- Training on project-specific workflows
- Building understanding before autonomous execution
- Onboarding new team members to codebase

**Execution Flow:**

When `execution.default_mode = "education"` or mode switches to education:

1. **Execute step autonomously** (like silent mode initially)

2. **At critical steps or key decisions:**
   - PAUSE execution
   - PRESENT education checkpoint
   - EXPLAIN situation and available approaches
   - COMPARE alternatives with pros/cons
   - RECOMMEND approach with rationale
   - REQUEST human review
   - EXECUTE approved approach
   - EXPLAIN outcome and lessons learned

3. **Education Checkpoint Format:**

```
[EDUCATION CHECKPOINT - Step X.Y]

Situation: [What we're about to do and why]

Available Approaches:
  A. [Primary method]
     Pros: [Advantages, when to use]
     Cons: [Disadvantages, risks]
     
  B. [Backup 1]
     Pros: [Advantages, when to use]
     Cons: [Disadvantages, risks]

Recommendation: [Approach A]
Rationale: [Why this approach is best for current situation]

Continue with recommended approach? [Y/n/explain more/try different]
```

4. **User Response Handling:**
   - **Y or Enter:** Execute recommended approach
   - **n:** Present alternative approaches again
   - **explain more:** Provide deeper technical explanation
   - **try different:** Allow user to select specific approach

5. **After Execution:**
```
[EDUCATION OUTCOME - Step X.Y]

Approach Used: [Which method was executed]
Result: [What happened]
Lesson Learned: [Key takeaway for future similar situations]
Alternative Would Have: [Brief note on what other approaches would have done differently]

Proceeding to next step...
```

6. **Learning Log to Notepad:**
   - All education checkpoints logged to notepad
   - Decisions made with rationale
   - Outcomes and lessons learned
   - Cumulative knowledge building

**Configuration (from parameters.toml):**

```toml
[education]
enabled = true
approval_gates = "increased"        # How many checkpoints
rationale_required = true           # Always explain why
alternatives_shown = true           # Always show options
comparison_depth = "detailed"       # How deep to compare
learning_pace = "moderate"          # How often to pause
```

**Learning Pace:**
- **slow:** Pause at every critical step and many non-critical steps (thorough but time-intensive)
- **moderate:** Pause at critical steps and key decision points (balanced, recommended)
- **fast:** Pause only at major decisions (minimal overhead)

**Comparison Depth:**
- **brief:** Simple pros/cons lists
- **moderate:** Pros/cons with examples
- **detailed:** Comprehensive trade-off analysis with code examples

**When NOT to Use Education Mode:**
- Routine workflows you understand well
- Time-critical troubleshooting
- Production incidents requiring speed
- Workflows with no novel learning value

**Education Mode vs Collaborative Mode:**

| Aspect | Education | Collaborative |
|--------|-----------|---------------|
| **Goal** | Learning & understanding | Control & oversight |
| **Pauses** | Key decisions + explanation | Every critical step |
| **Information** | Teaches alternatives & rationale | Confirms approach |
| **Outcome** | Knowledge accumulation | Task completion |
| **Best For** | Learning new patterns | High-stakes execution |

**Logging:**

Education mode adds to progress.json:
```json
{
  "step_id": "2.3",
  "mode": "education",
  "education_checkpoint": {
    "approaches_presented": 2,
    "recommended": "primary",
    "user_selected": "primary",
    "rationale_provided": true,
    "lesson_logged": true
  }
}
```

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
- **research_phase** (if research_enabled for task):
  - triggered (boolean)
  - timestamp_start, timestamp_end
  - queries_performed (array of search queries)
  - sources_consulted (array of URLs)
  - key_findings (array of insights)
  - confidence_level (low/medium/high)
  - research_cost (time, API calls, tokens)

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

Review constitutional adherence per `__SPEC_Engine/_Constitution/constitution.md`:

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

### 6.4 Completion Verification (MANDATORY)

**Execute BEFORE marking goal as ACHIEVED**

Read "Definition of Complete" from `spec_[descriptor].md` and verify each criterion:

#### Universal Checks (All Goals)

1. **Primary Deliverable Exists**
   - Check that the specified deliverable actually exists
   - Examples: report file, executable, test suite, documentation, analysis results

2. **Quality Standards Met**
   - Verify measurable quality criteria from spec
   - Examples: test coverage ≥95%, all functions documented, performance targets met

3. **Verification Method Passed**
   - Execute the verification method defined in spec
   - Examples: run test suite, execute analysis on dataset, test deployment

#### Additional Checks for Build/Create/System Goals

**Trigger:** If goal contains "build", "create", "develop", "system", "application", "app"

4. **Deployment Artifact Exists**
   - `desktop_app`: Check for `.exe`, `.app`, or installer
   - `web_app`: Check server can start, URL accessible
   - `cli`: Check executable/package exists
   - `library`: Check package published/installable

5. **User Interface (if user_interface.required = true)**
   - GUI/web interface implemented (not just backend)
   - Target users can use without technical knowledge

6. **Production Ready (if completion_criteria.production_ready = true)**
   - Real APIs configured (search for `test_mode` flags)
   - Production endpoints used, not mocks
   - Credentials configurable (not hardcoded)

7. **User Documentation**
   - If "for [users]" in goal: user guide exists
   - Installation/configuration guide if needed

#### Status Assignment

```json
{
  "completion_verification": {
    "primary_deliverable_exists": true/false,
    "quality_standards_met": true/false,
    "verification_passed": true/false,
    "deployment_artifact_exists": true/false,  // if applicable
    "user_interface_implemented": true/false,  // if applicable
    "production_ready": true/false,            // if applicable
    "user_documentation_exists": true/false,   // if applicable
    
    "overall_status": "PASS|FAIL",
    "goal_achievement_status": "ACHIEVED|PARTIAL|NOT_ACHIEVED",
    "gaps": ["list any missing elements"],
    "timestamp": "[ISO-8601]"
  }
}
```

**Status Rules:**
- **ACHIEVED:** All applicable checks PASS
- **PARTIAL:** Core deliverable exists but quality/deployment incomplete
- **NOT ACHIEVED:** Core deliverable missing or broken

**Log to progress.json**

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
