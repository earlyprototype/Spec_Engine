# Getting Started with the SPEC Engine

**Version:** 1.3  
**Last Updated:** 2025-11-03  
**Purpose:** Beginner-friendly tutorial for creating your first specification

---

## Welcome

This tutorial will walk you through creating your first SPEC from scratch. By the end, you'll understand how to transform a goal into an executable specification that an LLM can follow autonomously.

**Time required:** 30-45 minutes  
**Prerequisites:** None (we'll explain everything)

---

## What You'll Learn

1. What a SPEC is and why it's useful
2. How to set up a project (DNA profile - optional)
3. How to create your first SPEC
4. How to execute a SPEC
5. How to interpret the results

---

## Part 1: Understanding SPECs (5 minutes)

### What is a SPEC?

A SPEC is a structured set of instructions that guides an LLM to achieve a specific goal. Think of it as a recipe, but for AI:

- **Recipe:** Bake chocolate cake
- **SPEC:** Build a charity shop point-of-sale system

### The Three Files

Every SPEC consists of three files:

1. **spec_[name].md** - Human-readable story
   - What we're trying to achieve
   - Why we're doing each step
   - Examples and explanations

2. **parameters_[name].toml** - Machine-readable config
   - Same information, structured format
   - Easy for computers to validate
   - Settings and thresholds

3. **exe_[name].md** - Execution controller
   - How to interpret the spec
   - When to ask for help
   - How to handle failures

Plus one file created during execution:

4. **progress_[name].json** - Runtime log
   - What happened
   - What worked, what failed
   - Decision trail

### The Core Principle: One Goal

Every SPEC has exactly ONE goal. Not two, not three. One.

**Good goal:** "Create a user registration system"  
**Bad goal:** "Create registration and also build email templates and set up analytics"

Why? Because focus creates clarity. Clarity creates success.

---

## Part 2: Your First Decision - DNA Profile? (5 minutes)

### What is a DNA Profile?

A DNA profile is **optional** project-level configuration. It answers questions like:
- How cautious should the system be?
- What testing approach should we use?
- Are there specific tools we prefer?

### Should You Create One?

**Create a DNA profile if:**
- You'll create multiple SPECs for the same project
- You want consistent settings across SPECs
- You have specific requirements (risk level, custom tools)

**Skip DNA profile if:**
- This is a one-off task
- You're fine with system defaults
- You're just experimenting

**For this tutorial:** We'll skip the DNA profile to keep things simple. You can always create one later!

---

## Part 3: Creating Your First SPEC (20 minutes)

### Step 1: Choose a Goal

Let's use a simple, achievable goal for your first SPEC:

**Goal:** "Analyse the structure and quality of a Python module"

This is good because:
- Single focused objective
- Measurable outcome (analysis report)
- Achievable in reasonable time
- Requires multiple steps (perfect for learning)

### Step 2: Launch the Commander

The Commander is the SPEC-generating agent. It lives in:
```
__SPEC_Engine/_Commander_SPEC/Spec_Commander.md
```

**How to launch:** Provide this file to your LLM along with your goal.

**Example prompt:**
```
Use Spec_Commander.md to create a SPEC for this goal:
"Analyse the structure and quality of a Python module at /src/auth.py"
```

### Step 3: Commander Interview and Tool Selection (automated)

The Commander will:

1. **Detect DNA profile** (Step 0)
   - Scans for existing project configuration
   - If none found, offers to create one
   - For this tutorial, select [B] Skip

2. **Load constitution** (Step 1)
   - Reads system governance rules
   - Understands quality standards
   - No action required from you

3. **Draft high-level structure** (Step 2)
   - Commander proposes goal, tasks, completion criteria
   - Shows you something like:

4. **Analyse and recommend MCP tools** (Step 2.5 - NEW)
   - Commander reads MCP tools catalog (269 servers, 2900+ tools)
   - Analyses goal requirements autonomously
   - Recommends REQUIRED/RECOMMENDED/OPTIONAL tools
   - Adds tool recommendations to proposal

5. **Present complete proposal** (Step 3 becomes Step 3a)
   - Shows goal, tasks, AND toolset together
   - Combined structure looks like:

```markdown
# SPEC Proposal for Review

## Goal
Analyse the structure and quality of Python module /src/auth.py

## Definition of Complete
- [ ] Analysis report generated covering functions, classes, dependencies
- [ ] Code quality metrics calculated (complexity, maintainability)
- [ ] Report saved as auth_analysis.md

## Recommended MCP Toolset

### REQUIRED Tools (1)
- **filesystem** (★★★★★ | 11 tools)
  - Rationale: Must read Python file from local storage
  - Provides: File reading, directory operations
  - Install: `npm install @modelcontextprotocol/server-filesystem`

### RECOMMENDED Tools (1)
- **github** (★★★★★ | 26 tools)
  - Rationale: Version control context improves analysis quality
  - Alternative: Analyse file without repository history
  - Install: `npm install @modelcontextprotocol/server-github`

### OPTIONAL Tools (0)
- None recommended for this goal

## Tasks (High-Level)
1. **Parse and map module structure**
2. **Analyse code quality metrics**
3. **Generate comprehensive report**
```

6. **MANDATORY HUMAN REVIEW & TOOL INSTALLATION** (Step 3a - UPDATED)
   - This is now a **single pause point** for both review and tool installation
   - Commander will ask: [A] Approve, [R] Revise, [T] Modify tools, [C] Clarify

**Your action:** Review carefully! This is your chance to catch issues before detailed work begins.

Questions to ask yourself:
- Is the goal singular and clear?
- Are the recommended tools appropriate? (Do I need all REQUIRED ones? Want to add others?)
- Do the tasks collectively achieve the goal?
- Are completion criteria specific?

**If [A] Approve:**
- Commander shows installation commands
- You install REQUIRED tools now (using terminal)
- You configure MCP client and restart it
- You confirm [Y] when done
- Commander proceeds to generate detailed SPEC

**If [R] Revise or [T] Modify tools:**
- Make changes, Commander re-presents proposal
- Loop until you're satisfied, then [A] Approve

**If [C] Clarify:**
- Ask questions, Commander answers
- Re-presents proposal for your [A] Approval

### Step 4: Detailed Generation (automatic)

Once approved, Commander:

1. Breaks each task into 1-5 concrete steps
2. Identifies critical steps (failures block the goal)
3. Defines backup methods (alternative approaches)
4. Generates all three files simultaneously:
   - `spec_module_analysis.md`
   - `parameters_module_analysis.toml`
   - `exe_module_analysis.md`

5. Validates everything (constitutional compliance)

6. Shows you the output location:
```
SPECs/spec_module_analysis/
├── spec_module_analysis.md
├── parameters_module_analysis.toml
├── exe_module_analysis.md
└── (progress_module_analysis.json will be created at runtime)
```

### Step 5: Review Generated Files (5 minutes)

**Open `spec_module_analysis.md`** and look for:

- **Goal section:** Should match what you approved
- **Tasks and Steps:** Check they make sense
- **Critical flags:** Do critical steps really block the goal?
- **Backup methods:** Are they genuine alternatives (not just "try again")?

**Example task structure:**
```markdown
### Task [1]: Parse and map module structure

- **Step [1]:** Read source file and parse imports
  - **Primary method:** Use AST parser to extract imports
  - **Backup [1]:** If AST fails, use regex pattern matching
  - **Expected output:** List of imported modules
  - **Critical:** true

- **Step [2]:** Identify all functions and classes
  - **Primary method:** Parse function/class definitions with AST
  - **Expected output:** Structured list with names and line numbers
  - **Critical:** true
```

**Open `parameters_module_analysis.toml`** and verify:

- Matches the structure in spec.md
- Task IDs align (Task [1] in both files)
- Critical flags consistent
- Expected outputs defined

If something looks wrong, you can edit files before execution!

---

## Part 4: Executing Your SPEC (10 minutes)

### Step 1: Launch the Executor

The executor is `exe_module_analysis.md` (generated for your spec).

**How to launch:** Provide this file to your LLM.

**Example prompt:**
```
Execute exe_module_analysis.md
```

### Step 2: Initialisation

The executor will:

1. **Validate files** (Section 1.1)
   - Checks spec.md and parameters.toml exist
   - Verifies they're properly formatted

2. **Initialise progress log** (Section 1.2)
   - Creates progress_module_analysis.json
   - Records start time

3. **Mode selection** (Section 1.2a)
   - Prompts you:
```
Execution Mode Selection
========================

Default: Dynamic Mode (Recommended)

Options:
[1] Continue with Dynamic mode (recommended)
[2] Switch to Silent mode (fully autonomous)
[3] Switch to Collaborative mode (pause at decisions)

Press Enter to continue with Dynamic:
```

**For this tutorial:** Press Enter (accept Dynamic mode)

4. **Validate everything** (Section 1.3-1.10)
   - Parses both files
   - Checks goal is singular
   - Verifies tasks and steps exist
   - Confirms IDs match between files
   - Validates constitutional compliance

If validation passes, you'll see:
```
✅ Validation complete
✅ Ready for execution
```

### Step 3: Execution (automatic)

Now watch as the executor:

1. **Executes Task 1 steps sequentially**
   - Logs each step start
   - Attempts primary method
   - If failure, tries backups
   - Records outcomes

2. **Dynamic mode monitors for issues**
   - Tracks consecutive failures
   - Watches for backup depletion
   - Checks output quality

3. **Moves to Task 2, then Task 3**
   - Sequential execution
   - Each task builds on previous results

4. **Post-execution analysis** (Section 6)
   - What worked well?
   - What failed repeatedly?
   - Were backups effective?
   - Constitutional compliance score

### Step 4: Completion Verification

Before marking the goal as ACHIEVED, executor verifies:

- **Primary deliverable exists** (auth_analysis.md report)
- **Quality standards met** (all required sections present)
- **Verification method passed** (report contains expected analysis)

**Status options:**
- **ACHIEVED:** Everything complete
- **PARTIAL:** Core done but quality issues
- **NOT ACHIEVED:** Core deliverable missing

---

## Part 5: Interpreting Results (5 minutes)

### Reading progress.json

Open `progress_module_analysis.json` to see:

**Execution summary:**
```json
{
  "run_id": "2025-11-02T14:30:00Z",
  "status": "completed",
  "goal_achievement_status": "ACHIEVED",
  "execution_mode": "dynamic"
}
```

**Task outcomes:**
```json
{
  "tasks": [
    {
      "task_id": 1,
      "status": "completed",
      "steps_completed": 3,
      "steps_failed": 0,
      "backups_used": 0
    },
    ...
  ]
}
```

**Post-execution analysis:**
```json
{
  "post_execution_analysis": {
    "failure_patterns": {
      "overall_failure_rate": 0.08,
      "most_successful_backups": [
        {"description": "regex pattern matching", "success_rate": 1.0}
      ]
    },
    "constitutional_compliance_review": {
      "overall_compliance_score": 95
    },
    "recommendations": [
      "Current critical balance (60%) is appropriate",
      "All backup methods were genuine alternatives"
    ]
  }
}
```

### What to Look For

**Green flags:**
- Low failure rate (<20%)
- High compliance score (>90)
- Few mode escalations
- Recommendations say "appropriate"

**Red flags:**
- High failure rate (>40%)
- Many backups exhausted
- Compliance score <80
- Recommendations suggest major changes

---

## Common Questions

### Q: What if validation fails?

**A:** The executor will tell you exactly what's wrong:

```
❌ Validation Error: Task [2] missing in parameters.toml
❌ Validation Error: Step [1.3] has no expected output defined
```

Fix the issue in the appropriate file and re-run executor.

### Q: What if a step keeps failing?

**A:** Dynamic mode will escalate:

```
🚨 Dynamic Mode Escalation
Trigger: 3 consecutive failures
Task: 1, Step: 2
Methods attempted: primary, backup[1], backup[2]

OPTIONS:
[A] Skip this step (if non-critical)
[B] Provide alternative approach
[C] Halt execution for manual intervention
```

Choose based on whether the step is critical to your goal.

### Q: Can I edit the SPEC after it's generated?

**A:** Yes! Before execution:
- Edit spec.md for clarity
- Edit parameters.toml for settings
- Ensure IDs stay synchronised

After execution starts:
- Don't edit (it won't affect current run)
- Create a new SPEC version instead

### Q: What if I want to rerun the SPEC?

**A:** Delete (or archive) `progress_module_analysis.json` and relaunch `exe_module_analysis.md`. It will start fresh.

---

## Next Steps

### Congratulations

You've created and executed your first SPEC! You now understand:
- The three-file architecture
- Goal-driven decomposition
- Execution modes and validation
- Result interpretation

### Level Up

Ready for more? Try:

1. **Create a DNA profile**
   - Run `DNA_SPEC.md` interview
   - Create multiple SPECs in same project
   - See how project settings apply

2. **Build something**
   - Try a build goal: "Create a password strength checker CLI tool"
   - Notice how Article XIV enforces completeness
   - Experience software stack validation

3. **Experiment with modes**
   - Try Silent mode for routine tasks
   - Try Collaborative mode for complex decisions
   - Compare dynamic mode behaviour

4. **Read the philosophy**
   - `DESIGN_PHILOSOPHY.md` explains the "why"
   - `constitution.md` shows the rules
   - `WORKFLOW_DIAGRAM.md` shows complete lifecycle

### Get Help

**Stuck?**
- Re-read relevant sections of this guide
- Check `README.md` for document map
- Review example specs in `SPECs/Testing/`

**Want to contribute?**
- Follow constitutional amendment process (Article XIII)
- Test changes with example specs
- Document rationale for design decisions

---

## Quick Reference

### Essential Files

| File | Purpose | When to Use |
|------|---------|-------------|
| `Spec_Commander.md` | Generate new SPEC | Starting a new goal |
| `exe_[descriptor].md` | Execute SPEC | Running the spec |
| `DNA_SPEC.md` | Project config | Multi-spec projects |
| `constitution.md` | System rules | Understanding principles |

### Common Commands

**Generate SPEC:**
```
Use Spec_Commander.md to create SPEC for goal: "[your goal]"
```

**Execute SPEC:**
```
Execute exe_[descriptor].md
```

**Check progress:**
```
Read progress_[descriptor].json
```

### File Locations

```
__SPEC_Engine/          Framework (read-only)
SPECs/[DNA]/spec_[]/    Your generated specs
```

---

## Troubleshooting

### "File not found" errors

**Problem:** Executor can't find spec.md or parameters.toml  
**Solution:** Check you're in correct directory. Files should be in `SPECs/[DNA]/spec_[descriptor]/`

### "Validation failed: IDs don't match"

**Problem:** Task/step IDs differ between spec.md and parameters.toml  
**Solution:** Edit files so IDs match exactly (e.g., Task [1] in both, Step [2] in both)

### "No expected output defined"

**Problem:** Step missing expected_output field  
**Solution:** Add specific, measurable output to each step in both files

### "Goal not singular"

**Problem:** SPEC tries to achieve multiple goals  
**Solution:** Split into separate SPECs (one goal per spec)

### "Over-criticality detected (100%)"

**Problem:** All steps marked critical  
**Solution:** Review which steps truly block the goal. Mark others non-critical.

---

## Appendix: Complete Example Walkthrough

### Real Example: "Validate CSV Data Quality"

Let's walk through a complete, realistic example from start to finish.

#### The Goal

You have a CSV file with customer data and need to validate its quality:
- Check for missing required fields
- Validate email formats
- Detect duplicate entries
- Generate a quality report

**Goal statement:** "Validate data quality of customers.csv and generate quality report"

#### Step 1: Run Commander

Provide to LLM:
```
Use __SPEC_Engine/_Commander_SPEC/Spec_Commander.md to create a SPEC for:
"Validate data quality of customers.csv and generate quality report"
```

#### Step 2: Commander Generates Draft

Commander analyses and proposes:

```markdown
# SPEC Proposal for Review

## Goal
Validate data quality of customers.csv and generate quality report

## Definition of Complete
- [ ] Quality report generated (validation_report.md)
- [ ] All validation checks performed (missing fields, format, duplicates)
- [ ] Report includes statistics and specific issues found
- [ ] Report saved to output folder

## Software Stack
- Deployment type: Command-line tool
- Language: Python
- Framework: None (script-based)
- Target users: Data analysts
- Packaging: Standalone Python script

## Tasks (High-Level)
1. **Load and parse CSV data**
2. **Perform validation checks**
3. **Generate comprehensive report**

## Estimated Complexity
- Total steps: 9-12
- Critical steps: 6-7 (60%)
- No GUI required (CLI tool)
```

#### Step 3: Review and Approve

You review:
- Goal is singular: ✅
- Tasks achieve goal: ✅
- Completion criteria specific: ✅

**You select: [A] APPROVE**

#### Step 4: Commander Generates Detailed SPEC

Commander generates three files with detailed tasks:

**Task [1]: Load and parse CSV data**
- Step [1]: Read CSV file using pandas
  - Backup [1]: If pandas unavailable, use csv module
  - Critical: true
- Step [2]: Validate file structure (headers present)
  - Critical: true
- Step [3]: Convert to dataframe for analysis
  - Critical: true

**Task [2]: Perform validation checks**
- Step [1]: Check for missing required fields
  - Primary: Identify null values in required columns
  - Backup [1]: Manual iteration if vectorized check fails
  - Critical: true
- Step [2]: Validate email format using regex
  - Primary: Apply email regex pattern to email column
  - Backup [1]: Use simple @ check if regex fails
  - Critical: false (quality, not blocking)
- Step [3]: Detect duplicate entries
  - Primary: Use pandas.duplicated() on unique identifiers
  - Critical: true
- Step [4]: Calculate completeness percentage
  - Critical: false (reporting metric)

**Task [3]: Generate comprehensive report**
- Step [1]: Structure findings into sections
  - Critical: false
- Step [2]: Write report to markdown file
  - Primary: Use file operations to write
  - Backup [1]: Print to console if file write fails
  - Critical: true
- Step [3]: Include summary statistics
  - Critical: false

Files created:
```
SPECs/spec_csv_validation/
├── spec_csv_validation.md
├── parameters_csv_validation.toml
├── exe_csv_validation.md
└── (progress_csv_validation.json - created at runtime)
```

#### Step 5: Execute the SPEC

Provide to LLM:
```
Execute SPECs/spec_csv_validation/exe_csv_validation.md
```

**Execution Flow:**

1. **Initialisation:**
```
✅ Files validated
✅ Progress log initialized
✅ Mode selection: Dynamic (default accepted)
✅ Validation complete - 3 tasks, 10 steps
```

2. **Task 1 Execution:**
```
Starting Task [1]: Load and parse CSV data

Step [1.1]: Read CSV file using pandas
  → Attempting primary method...
  → ✅ Success: Loaded 1,247 rows
  
Step [1.2]: Validate file structure
  → Attempting primary method...
  → ✅ Success: 5 columns detected [id, name, email, phone, address]
  
Step [1.3]: Convert to dataframe
  → Attempting primary method...
  → ✅ Success: DataFrame created

Task [1] complete: 3/3 steps succeeded
```

3. **Task 2 Execution:**
```
Starting Task [2]: Perform validation checks

Step [2.1]: Check for missing required fields
  → Attempting primary method...
  → ✅ Success: Found 23 missing emails, 7 missing phones
  
Step [2.2]: Validate email format
  → Attempting primary method...
  → ✅ Success: 1,189 valid emails, 35 invalid formats
  
Step [2.3]: Detect duplicate entries
  → Attempting primary method...
  → ✅ Success: Found 12 duplicate customer IDs
  
Step [2.4]: Calculate completeness
  → Attempting primary method...
  → ✅ Success: Overall completeness: 94.2%

Task [2] complete: 4/4 steps succeeded
```

4. **Task 3 Execution:**
```
Starting Task [3]: Generate comprehensive report

Step [3.1]: Structure findings into sections
  → Attempting primary method...
  → ✅ Success: Report structure created
  
Step [3.2]: Write report to file
  → Attempting primary method...
  → ✅ Success: validation_report.md created
  
Step [3.3]: Include summary statistics
  → Attempting primary method...
  → ✅ Success: Statistics section added

Task [3] complete: 3/3 steps succeeded
```

5. **Post-Execution Analysis:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXECUTION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Failure Pattern Analysis:
  • Overall failure rate: 0% (0/10 steps)
  • No backups required
  • No mode escalations

Constitutional Compliance:
  • Article VI (Critical balance): 60% - PASS
  • Article VII (Backup quality): All genuine alternatives - PASS
  • Article X (Logging): Complete - PASS
  • Overall compliance score: 100

Recommendations:
  • SPEC structure is optimal
  • Primary methods highly effective
  • No changes recommended
```

6. **Completion Verification:**
```
Verifying goal achievement...

Universal Checks:
  ✅ Primary deliverable exists: validation_report.md
  ✅ Quality standards met: All validation checks performed
  ✅ Verification passed: Report contains required sections

Goal Achievement Status: ACHIEVED
```

#### Step 6: Review Results

**Check validation_report.md:**
```markdown
# Data Quality Report: customers.csv

## Summary Statistics
- Total rows: 1,247
- Columns analyzed: 5
- Overall completeness: 94.2%
- Validation date: 2025-11-02

## Missing Data Analysis
- Missing emails: 23 records (1.8%)
- Missing phone numbers: 7 records (0.6%)

## Format Validation
- Valid email formats: 1,189 (95.3%)
- Invalid email formats: 35 (2.8%)
  Example issues:
    - Row 234: "john.doe@"
    - Row 567: "invalid.email"

## Duplicate Detection
- Duplicate customer IDs: 12 occurrences
  Affected IDs: [123, 456, 789...]

## Recommendations
1. Contact data entry team about email validation
2. Investigate duplicate ID source
3. Consider required field enforcement
```

**Check progress_csv_validation.json:**

All 10 steps logged with:
- Outcomes (all successful)
- Methods used (all primary)
- Timestamps
- Expected outputs matched

**Goal ACHIEVED ✅**

#### What Made This Successful?

1. **Clear goal:** Single, measurable objective
2. **Appropriate critical flags:** 60% critical (data loading, report writing)
3. **Effective backups:** Genuine alternatives (csv module vs pandas)
4. **Good decomposition:** 3 tasks, 10 steps - manageable scope
5. **Specific outputs:** "List of missing fields" not "some results"

#### What Could Have Gone Wrong?

**Scenario 1: Pandas not installed**
```
Step [1.1]: Read CSV using pandas
  → ❌ Failed: ModuleNotFoundError: No module named 'pandas'
  → Attempting Backup [1]: Use csv module
  → ✅ Success: Loaded using csv.DictReader

Method updated: backup[1] used
```

**Scenario 2: Invalid CSV format**
```
Step [1.2]: Validate file structure
  → ❌ Failed: No header row detected
  → Step marked CRITICAL
  → No backup defined for this failure mode

Dynamic Mode Escalation:
  Trigger: Critical step failed with no backup
  
OPTIONS:
  [A] Provide CSV file location for header definition
  [B] Skip validation (mark as PARTIAL)
  [C] Halt execution

User selected [A]: Provided header definition
  → Manual header: ['id', 'name', 'email', 'phone', 'address']
  → ✅ Continuing with provided headers
```

**Scenario 3: Multiple failures**
```
Task [2]: Perform validation checks
  Step [2.1]: ❌ Failed (primary)
  Step [2.2]: ❌ Failed (primary + backup[1])
  Step [2.3]: ❌ Failed (primary)

Dynamic Mode Escalation:
  Trigger: 3 consecutive failures (threshold reached)
  Backup depletion detected
  
Escalating to collaborative mode...

Human guidance requested:
  "Validation steps failing due to unexpected data format.
   Current approach assumes standard CSV structure.
   Recommend reviewing file format before continuing."
```

---

### Key Takeaways from Example

1. **SPECs work for diverse goals:** This example showed data validation, not code generation
2. **Backups prevent failures:** csv module backup avoided pandas dependency issue
3. **Critical flags matter:** Data loading critical, formatting validation non-critical
4. **Dynamic mode adapts:** Would escalate if multiple failures occurred
5. **Results are verifiable:** Clear deliverable (report) with measurable completion

---

**You're ready to start! Choose a goal and launch `Spec_Commander.md`.**

---

## Advanced: Complex SPECs with SPECLets

###When You Need SPECLets

For most goals, the simple structure (SPEC → TASK → Step) works perfectly. But for complex multi-phase projects, SPECLets provide an intermediate grouping layer.

**Use SPECLets when:**
- Goal has multiple distinct phases (setup → features → testing)
- You'd need >5 tasks without grouping
- Some work depends on other work completing first
- Independent work could run in parallel

**Example: Design Thinking Innovation Dashboard**

This is a complex project requiring:
- Platform foundation (database, API, auth)
- Multiple stages (discovery, define, ideate, prototype, test)
- Sequential dependencies (can't test before building)
- Parallel opportunities (discovery + define can run together)

**Simple approach (doesn't work well):**
- Forces 6 separate SPECs or violates "2-5 tasks" rule
- Manual dependency tracking
- No parallel execution

**SPECLet approach:**
```
SPEC: "Build Design Thinking Dashboard"
  ├─ SPECLet: platform_foundation [no deps, 3 tasks]
  ├─ SPECLet: discovery_stage [depends: platform, 2 tasks]
  ├─ SPECLet: define_stage [depends: platform, 3 tasks]
  ├─ SPECLet: ideate_stage [depends: define, 2 tasks]
  ├─ SPECLet: prototype_stage [depends: ideate, 3 tasks]
  └─ SPECLet: test_stage [depends: prototype, 2 tasks]

Execution Flow:
- Stage 1: platform_foundation runs
- Stage 2: discovery_stage + define_stage run in PARALLEL
- Stage 3: ideate_stage waits for define_stage
- Stage 4: prototype_stage waits for ideate_stage  
- Stage 5: test_stage runs final validation
```

### Creating a SPECLet-Based SPEC

When you run `Spec_Commander.md` with a complex goal:

**Step 1: Commander Detects Complexity**
```
Analyzing goal: "Build Design Thinking Innovation Dashboard"

Complexity Assessment:
- Multi-phase nature: YES (6 distinct stages)
- Task count would exceed 5: YES (15+ tasks needed)
- Dependency chains: YES (stages must be sequential)
- Parallel opportunities: YES (some stages independent)

Recommendation: Use SPECLets
```

**Step 2: Commander Proposes SPECLet Structure**
```markdown
## Structure Assessment
**Complexity:** Complex
**SPECLets needed:** Yes - Multi-stage platform with sequential dependencies

## SPECLet Structure
### SPECLet 1: platform_foundation - Core Infrastructure
- **Depends on:** None
- **Parallel allowed:** Yes
- **Tasks:**
  1. Task 1.1: Set up database schema
  2. Task 1.2: Create API framework
  3. Task 1.3: Configure authentication

### SPECLet 2: discovery_stage - Discovery Phase
- **Depends on:** platform_foundation
- **Parallel allowed:** Yes (can run with define_stage)
- **Tasks:**
  1. Task 2.1: Build discovery interface
  2. Task 2.2: Implement journey mapping tools

[... more SPECLets ...]

## Dependency Flow
```
platform_foundation
  ├─> discovery_stage (parallel)
  └─> define_stage (parallel)
      └─> ideate_stage
          └─> prototype_stage
              └─> test_stage
```
```

**Step 3: You Review and Approve**
- Check SPECLet groupings make sense
- Verify dependencies are correct
- Confirm parallel execution opportunities identified

**Step 4: Commander Generates Files**
Both `spec_[descriptor].md` and `parameters_[descriptor].toml` include:
- [[speclets]] array with dependencies
- Tasks grouped under SPECLets
- Execution plan for orchestration

**Step 5: Execute with Orchestration**
When you run `exe_[descriptor].md`:
- Validates SPECLet dependencies (no circular refs)
- Creates execution plan (topological sort)
- Executes SPECLets in stages
- Tracks per-SPECLet progress
- Handles failures without blocking independent branches

### SPECLet Progress Tracking

During execution, you'll see:
```
═══════════════════════════════════════════════════
SPECLet Execution Progress
═══════════════════════════════════════════════════

Stage 1: Foundation
  ✅ platform_foundation (completed in 15m)

Stage 2: Core Features (parallel execution)
  🔄 discovery_stage (in progress - Task 2/2)
  🔄 define_stage (in progress - Task 3/3)

Stage 3: Advanced Features
  ⏸️ ideate_stage (blocked - waiting for define_stage)

Overall: Stage 2 of 5 (40%)
═══════════════════════════════════════════════════
```

### When to Keep It Simple

Most goals DON'T need SPECLets. Use the simple structure for:
- "Analyse code quality of module.py"
- "Generate test coverage report"
- "Debug authentication issue"
- "Create documentation for API"
- "Optimize database queries"

These are straightforward, sequential, and fit within 2-5 tasks naturally.

---

**You're ready to start! Choose a goal and launch `Spec_Commander.md`.**

