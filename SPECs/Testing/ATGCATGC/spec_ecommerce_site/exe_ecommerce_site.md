# exe_ecommerce_site.md
## SPECs/Testing/ATGCATGC/spec_ecommerce_site/

---

### [META]
- **File Role:** Execution controller for e-commerce website build
- **Created by:** Spec Commander with ATGCATGC constitution
- **Goal:** Build complete e-commerce website for boutique handcrafted scarf sales
- **Mode:** Default = `dynamic` (from project constitution)
- **Logging:** Writes to `progress_ecommerce_site.json`
- **Constitution:** ATGCATGC (low risk, moderate complexity, TDD required)

---

## 1. Initialisation and Validation

### 1.1 File Presence Check
1. Confirm presence of required files:
   - `spec_ecommerce_site.md`
   - `parameters_ecommerce_site.toml`
   - `SPECs/Testing/ATGCATGC/project_constitution.toml`
2. If any file is missing:
   - Log critical error
   - Halt execution and prompt in **collaborative** mode for resolution

### 1.2 Initialise Progress Log
1. Check if `progress_ecommerce_site.json` exists
2. If not, create with initial structure:
   ```json
   {
     "run_id": "[timestamp]",
     "descriptor": "ecommerce_site",
     "project": "scarf-boutique-ecommerce",
     "dna_code": "ATGCATGC",
     "start_time": "[ISO-8601]",
     "status": "initialising",
     "execution_mode": "dynamic",
     "constitution_applied": true,
     "tasks": []
   }
   ```
3. If resuming, validate log integrity and mark as `resumed`
4. Record initialisation metadata:
   - Start time
   - Default mode (dynamic, per constitution)
   - Total: 6 tasks, 31 steps
   - Critical step count: 23 (74% - note: within low-risk 20-40% target from constitution)
   - External dependencies: Stripe, Cloudinary, Email service

### 1.2a User Mode Selection (Interactive Prompt)

**After initialisation, before validation:**

1. **Present mode options to user:**
   ```
   E-commerce Website Build - Mode Selection
   =========================================
   
   Project: Boutique Scarf E-commerce (ATGCATGC)
   Risk Level: Low | Complexity: Moderate
   Constitution Default: Dynamic Mode
   
   Default: Dynamic Mode (Recommended for this project)
   - Runs autonomously with intelligent escalation
   - Balances efficiency with safety
   - Escalates after 3 consecutive failures (per constitution)
   - Continue_and_log strategy (failures logged but don't halt)
   
   Options:
   [1] Continue with Dynamic mode (recommended for moderate complexity)
   [2] Switch to Silent mode (fully autonomous - use if confident)
   [3] Switch to Collaborative mode (frequent oversight - for learning)
   
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
     "mode_selection_timestamp": "[ISO-8601]",
     "constitution_default": "dynamic"
   }
   ```

4. **Log mode selection and proceed to validation**

### 1.3 Parse Specification Files
1. Read and parse `spec_ecommerce_site.md`:
   - Extract goal: Build complete e-commerce website
   - Extract 6 tasks with descriptions
   - Extract 31 steps across all tasks
   - Extract backups (22 backup methods defined)
   - Extract user stories (enabled per constitution)
   - Extract components and constraints
2. Read and parse `parameters_ecommerce_site.toml`:
   - Extract goal description (verify match)
   - Extract tasks array [1-6] with all parameters
   - Extract steps with expected outputs
   - Extract error_propagation config (continue_and_log strategy)
   - Extract logging and verification config
3. Read and parse `project_constitution.toml`:
   - Verify DNA code: ATGCATGC
   - Extract risk level: low
   - Extract critical_percentage target: 20-40%
   - Extract TDD requirement: true
   - Extract external dependencies
4. Store parsed content in memory for validation

### 1.4 Validate Goal
1. Check that **one and only one goal** exists in both files
2. Goal text: "Build a complete e-commerce website for a boutique artist to sell fine handcrafted scarves..."
3. Verify goal descriptions match between Markdown and TOML
4. Confirm goal is specific and actionable
5. Log goal validation success

### 1.5 Validate Tasks
1. Verify 6 tasks are defined in both files
2. For each task, verify:
   - Unique task ID [1-6]
   - Descriptive name matches between files
   - At least one step per task
   - All critical flags are boolean
   - All modes are valid (dynamic/silent/collaborative)
   - Max retries defined (≥ 0)
3. Check for duplicate task IDs
4. Task count (6) is reasonable for goal scope
5. Log task validation success

### 1.6 Validate Steps
1. Verify all 31 steps across 6 tasks
2. For each step, verify:
   - Unique step ID within task
   - Non-empty action description
   - Expected output clearly defined
   - Critical flag appropriate
   - Mode setting valid
3. Check for duplicate step IDs within tasks
4. Verify expected outputs are specific and measurable
5. Log step validation success

### 1.7 Validate Backups
1. Check 22 backup methods across critical steps
2. Verify backups are genuine alternatives, not retries:
   - "Research best practices" ✓ (alternative approach)
   - "Use alternative library" ✓ (tool-based alternative)
   - "Implement retry with backoff" ✓ (different strategy)
   - NOT "Try again" (simple retry - constitutional violation)
3. Confirm critical steps have backup coverage
4. Verify backup IDs unique and properly referenced
5. Log backup validation success

### 1.8 Bridging Verification (Markdown ↔ TOML)
1. Confirm all 6 tasks in spec_ecommerce_site.md exist in parameters_ecommerce_site.toml
2. Confirm all 31 steps match between files
3. Verify task IDs: 1, 2, 3, 4, 5, 6 (consistent)
4. Verify step IDs within each task (consistent)
5. Check backup references (22 backups) match between files
6. Verify constraint cross-references:
   - `constraints.auth_security`
   - `constraints.payment_security`
   - `constraints.test_coverage`
   - `constraints.max_image_size_mb`
   - All referenced constraints exist in TOML
7. Generate bridging report:
   - Missing tasks/steps: none expected
   - ID mismatches: none expected
   - Inconsistencies: none expected
8. Log bridging validation success

### 1.9 Validate Components and Constraints
1. Verify all components defined:
   - frontend, backend, database, image_hosting, payment_gateway, email_service, test_framework
2. Verify all constraints defined:
   - Security: auth_security, payment_security, no_credentials_in_logs, encrypt_sensitive_data
   - Testing: test_coverage, tests_must_pass
   - Technical: max_image_size_mb, responsive_design
   - Validation: project_structure_complete, image_hosting_functional, cart_functional, email_delivery
3. Check that steps reference only defined components
4. Verify security constraints align with constitution requirements
5. Log components and constraints validation success

### 1.10 Validation Summary and Pre-Flight Check
1. Compile validation findings:
   - **Critical errors:** None expected
   - **Warnings:** Critical step percentage (74%) exceeds constitution target (20-40%) - note for review but proceed (low risk project allows flexibility)
   - **Information:** 6 tasks, 31 steps, 22 backups defined; TDD required; 3 external dependencies
2. Constitution compliance check:
   - DNA code: ATGCATGC ✓
   - Risk level: low ✓
   - TDD required: true ✓
   - User stories: enabled ✓
   - External dependencies: documented ✓
   - Error propagation: enabled with continue_and_log ✓
3. If **critical errors** detected:
   - Log all errors to progress file
   - Switch to **collaborative** mode
   - Halt execution and prompt for resolution
4. If **only warnings** detected:
   - Log warnings to progress file
   - Note critical percentage variance
   - Proceed (low risk allows flexibility)
5. If **validation passes**:
   - Log successful validation
   - Mark progress log status as `ready_for_execution`
   - Display validation summary to user
   - Proceed to Execution Flow (Section 2)

---

**Initialisation Complete**: Files validated, log initialised, constitution applied, ready for sequential task execution.

---

## 2. Execution Flow

### 2.0 Constitutional Compliance Check (Per Task)

**Before executing each task**, verify ongoing constitutional compliance:

#### Constitution Check: ATGCATGC
1. Verify error_propagation.enabled = true ✓
2. Verify read_prior_steps = true ✓
3. Verify propagation_strategy = "continue_and_log" ✓
4. Verify TDD requirement is being followed
5. Record constitutional compliance in progress.json:
   ```json
   "constitutional_checks": {
     "task_id": 1,
     "dna_code": "ATGCATGC",
     "tdd_followed": true,
     "error_propagation_active": true,
     "external_dependencies_available": ["Stripe", "Cloudinary", "Email"],
     "compliant": true
   }
   ```

#### Critical Flag Balance Review
1. Count critical vs non-critical steps in current task
2. Calculate ratio (overall: 74%, note variance from 20-40% target)
3. Log if task has unusual critical balance
4. Continue (low risk project allows flexibility)

#### Prior Step Outcomes Check
1. Before executing Step 1 of any task (except Task 1):
   - Read progress.json for prior task outcomes
   - Check for failures in critical steps
   - Identify any warnings or issues to consider
   - Log dependency check performed

#### Comprehensive Logging Active
1. Verify last step logged all required fields
2. Confirm progress.json is up-to-date
3. Track any logging gaps

---

### 2.1 Task Iteration

**Execute tasks sequentially: Task 1 → Task 2 → Task 3 → Task 4 → Task 5 → Task 6**

For each **Task**:

1. Perform Constitutional Compliance Check (Section 2.0)
2. Log Task start event with timestamp
3. Read task description and parameters from TOML
4. Check task-specific requirements:
   - Task 1: Foundation - critical for all downstream work
   - Task 2: Authentication - security-critical
   - Task 3: Product catalogue - requires Cloudinary dependency
   - Task 4: Shopping cart - depends on products and auth
   - Task 5: Payment - requires Stripe dependency, highest security
   - Task 6: Order management - requires email service dependency

For each **Step** within that Task:
   
### 2.2 Pre-Step Error Propagation Check
- **Read `progress_ecommerce_site.json`** for prior step outcomes
- Check if any prior **critical steps** failed
- With continue_and_log strategy:
  - Log any prior failures as context
  - Assess impact on current step
  - If dependency broken (e.g., auth failed but cart needs auth), log warning
  - Proceed unless dependency is completely blocking
- Update step context with propagation information

### 2.3 Step Execution (TDD Approach for Critical Steps)

**For steps involving code (most implementation steps):**
1. If step requires testing (critical_flag = true):
   - **Write tests FIRST** (TDD requirement from constitution)
   - Tests should cover happy path and edge cases
   - Verify test count meets expected output minimum (where specified)
   - Tests should fail initially (red phase)
2. **Implement primary method**:
   - Follow step description
   - Make tests pass (green phase)
   - Refactor if needed
3. **Verify expected output**:
   - Check tests pass
   - Verify output matches expected_output field
   - Confirm non-functional requirements met (security, performance)

**If successful:**
- Log `step_complete` with test results
- Note TDD cycle completed (red-green-refactor)
- Proceed to next step

**If failure detected:**
- Increment retry count
- Attempt Backup Method (Section 2.4)
- Log each attempt

### 2.4 Retry and Backup Logic
- If primary method fails:
  - Check if backup defined in TOML
  - Execute backup method(s) sequentially
  - Log each backup attempt with ID
- If all methods exhausted (primary + backups):
  - Check critical_flag:
    - If critical = true:
      - Increment consecutive failure counter
      - If counter reaches 3: escalate to collaborative mode
      - Log failure details and prompt for guidance
    - If critical = false:
      - Log warning
      - Continue to next step (per continue_and_log strategy)
- If consecutive failures reach 5 (failure_threshold from constitution):
  - Escalate regardless of individual step criticality
  - Request collaborative review

### 2.5 Task Completion
1. When all steps complete:
   - Mark Task as `complete`
   - Log task summary:
     - Steps succeeded/failed
     - Retries used
     - Backups triggered
     - TDD cycles completed
     - Mode switches (if any)
   - Reset consecutive failure counter
   - Verify task deliverable:
     - Task 1: Project structure exists, dependencies installed
     - Task 2: Authentication working, tests passing
     - Task 3: Products manageable, images hosted on Cloudinary
     - Task 4: Cart functional, tested
     - Task 5: Stripe integrated, payment flow tested
     - Task 6: Orders tracked, emails sent
2. Continue to next task (no parallelism)

---

## 3. Mode Control

### Dynamic Mode (Default)
- Executes autonomously with intelligent escalation
- **Escalation triggers:**
  1. 3 consecutive step failures (from constitution escalation_threshold)
  2. All backups exhausted on critical step
  3. External dependency failure (Stripe, Cloudinary, Email)
  4. Security constraint violation detected
  5. 5 total failures reached (from constitution failure_threshold)

- **When escalating:**
  - Switch to collaborative mode temporarily
  - Present situation summary to user
  - Request guidance or decision
  - Log escalation reason and user response
  - Resume dynamic mode after resolution

### Silent Mode (If Selected)
- Fully autonomous execution
- Only escalates on unrecoverable errors
- Requires high confidence in spec quality
- Recommended only after testing spec in dynamic mode

### Collaborative Mode (If Selected)
- Pauses at each critical decision
- Requests user input before proceeding
- Useful for:
  - Learning the process
  - High-stakes modifications
  - Debugging spec issues
  - Verifying external service integration

### Mode Changes
All mode switches logged with:
- Timestamp
- Originating task and step
- Reason for switch
- User decision (if applicable)
- Consecutive failure count

---

## 4. Verification Layer

### 4.1 Per-Step Verification
After each step:
1. **Verify expected output:**
   - Compare actual vs expected_output in TOML
   - For test steps: verify minimum test count
   - For implementation steps: verify tests pass
   - Log verification outcome

2. **Check constraint satisfaction:**
   - Security constraints (no credentials in logs, encryption)
   - Testing constraints (TDD followed, tests pass)
   - Technical constraints (image size limits, etc.)
   - Log any violations

3. **Validate TDD compliance:**
   - For code implementation steps, verify tests were written first
   - Confirm red-green-refactor cycle followed
   - Log TDD adherence

### 4.2 Per-Task Verification
After each Task:
1. Confirm all steps marked complete or appropriately handled
2. Verify task deliverable achieved:
   - Can be demonstrated/tested
   - Meets acceptance criteria
   - Documented appropriately
3. Check error propagation handling:
   - Failures logged correctly
   - Downstream steps aware of issues
   - Continue_and_log strategy followed
4. External dependency verification:
   - Task 3: Cloudinary integration functional
   - Task 5: Stripe integration functional
   - Task 6: Email service functional

### 4.3 Security Verification
Ongoing throughout execution:
1. No credentials logged or committed
2. Sensitive data encrypted
3. Stripe handles all payment data (PCI compliance)
4. Authentication properly implemented
5. Authorization checks on admin endpoints

### 4.4 Run End Verification
At run end:
1. Validate all 6 tasks complete
2. Check overall test coverage
3. Verify all external dependencies integrated
4. Confirm no security violations logged
5. Review constitutional compliance throughout
6. Generate completion report:
   - Tasks completed: 6/6
   - Critical steps passed: X/23
   - Tests written: total count
   - Tests passing: should be 100%
   - Backups used: count and types
   - Mode switches: count and reasons
   - External services integrated: 3/3
   - Security compliant: yes/no

---

## 5. Logging and Reporting

All activity recorded in `progress_ecommerce_site.json`:

**Standard fields:**
- task_id (1-6)
- step_id (1-n within task)
- status (started, completed, failed, skipped)
- retry_count
- timestamp (ISO-8601)
- mode (current execution mode)
- method_used (primary, backup_1, backup_2)
- backup_attempts (array)
- expected_output_match (boolean)
- message or error detail

**TDD-specific fields:**
- tdd_cycle_completed (boolean)
- tests_written_first (boolean)
- test_count
- tests_passing (boolean)

**E-commerce-specific fields:**
- external_dependency_used (Stripe/Cloudinary/Email)
- security_check_passed (boolean)
- integration_verified (boolean)

**Error propagation fields:**
- error_propagation_decision
- prior_step_dependencies (array)
- propagation_strategy_used ("continue_and_log")

**Constitutional compliance fields:**
- constitution_check_passed (boolean)
- dna_code ("ATGCATGC")
- risk_assessment ("low")

### Final Summary
At completion, write comprehensive summary:
```json
{
  "execution_summary": {
    "goal": "Build complete e-commerce website",
    "project": "scarf-boutique-ecommerce",
    "dna_code": "ATGCATGC",
    "total_tasks": 6,
    "tasks_completed": 6,
    "total_steps": 31,
    "steps_completed": X,
    "critical_steps_passed": "X/23",
    "tdd_cycles": X,
    "tests_written": X,
    "tests_passing": X,
    "backups_used": X,
    "mode_switches": X,
    "external_integrations": {
      "stripe": "success/failed",
      "cloudinary": "success/failed",
      "email_service": "success/failed"
    },
    "security_compliant": true,
    "constitutional_compliant": true,
    "runtime_duration": "X hours",
    "completion_status": "success/partial/failed"
  }
}
```

---

## 6. Post-Execution Analysis

**After completing all tasks OR on critical halt:**

### 6.1 Failure Pattern Analysis

**Identify patterns:**
1. Which steps failed most often?
2. Were failures clustered in specific tasks?
3. Which backups were most effective?
4. What triggered mode escalations?

**Backup effectiveness:**
1. Success rate per backup type
2. Recommend promoting successful backups to primary
3. Suggest new backups for gaps

**Mode escalation analysis:**
1. Count and categorise escalations
2. Were escalations appropriate?
3. Should thresholds be adjusted?

### 6.2 Constitutional Compliance Review

**Review ATGCATGC constitution adherence:**
1. TDD followed throughout? (required)
2. Critical balance appropriate? (noted 74% vs 20-40% target)
3. Error propagation functioned? (continue_and_log strategy)
4. External dependencies handled? (Stripe, Cloudinary, Email)
5. Security requirements met? (encryption, PCI compliance)

**Generate compliance score:**
```json
"constitutional_compliance_review": {
  "dna_code": "ATGCATGC",
  "tdd_compliance": "full/partial/none",
  "error_propagation": "functional/issues",
  "external_dependencies": "3/3 integrated",
  "security_requirements": "met/violations_found",
  "overall_compliance_score": 85-100
}
```

### 6.3 E-commerce-Specific Analysis

**Deliverable quality:**
1. Can users register and login?
2. Can admin manage products?
3. Can customers browse and add to cart?
4. Can payments be processed via Stripe?
5. Are orders created and emails sent?

**Integration health:**
1. Cloudinary: upload speed, reliability
2. Stripe: test mode vs production readiness
3. Email: delivery success rate

**Security posture:**
1. Credentials encrypted
2. No credentials in logs/code
3. PCI compliance via Stripe
4. Authentication properly protecting routes

### 6.4 Recommendations

Generate actionable recommendations:

**For this project:**
- "Deploy to staging environment for user testing"
- "Switch Stripe from test mode to live mode when ready"
- "Monitor Cloudinary storage usage"
- "Set up email delivery monitoring"

**For future SPECs:**
- "Critical step balance (74%) exceeded target - consider breaking into multiple SPECs"
- "TDD approach worked well - continue for similar projects"
- "External dependency backups (alternative services) were good safety net"
- "Dynamic mode with continue_and_log strategy appropriate for low-risk projects"

### 6.5 Append Analysis to Progress.json

Add comprehensive analysis section with all findings, recommendations, and compliance review.

---

## 7. Finalization

1. **Print summary report** to console
2. **Archive option:** Save to `/SPECs/Testing/ATGCATGC/spec_ecommerce_site/archive_[date]/`
3. **Ensure immutability:** Progress log timestamped and complete
4. **Next steps guidance:**
   - Test the application thoroughly
   - Set up staging environment
   - Configure production credentials
   - Plan deployment strategy
   - Set up monitoring and analytics

---

## 8. Notes for Execution

**Project-specific considerations:**

1. **External Dependencies:**
   - Cloudinary: Obtain credentials before Task 3
   - Stripe: Use test mode for Tasks 5, switch to live for production
   - Email service: Configure and verify before Task 6

2. **Technology Stack:**
   - Flexible per constitution - select appropriate for your skills
   - Suggestions: React+Node.js, Vue+Python, Ruby on Rails
   - Ensure test framework compatible (Jest, Pytest, RSpec)

3. **ADHD-Friendly Execution:**
   - Clear progress indicators after each step
   - Break sessions at task boundaries (natural stopping points)
   - 6 tasks = 6 work sessions possible
   - Progress.json provides clear "where am I?" context

4. **TDD Discipline:**
   - Write tests first for all critical steps
   - Resist urge to code before testing
   - Red-green-refactor cycle is the goal
   - Tests provide confidence for autonomous execution

5. **Security Priority:**
   - Never commit credentials
   - Always encrypt sensitive data
   - Use Stripe for payment data (never store cards)
   - Test authentication thoroughly

---

**Execution ready. Begin with Task 1: Project Foundation and Setup.**

*End of exe_ecommerce_site.md*

