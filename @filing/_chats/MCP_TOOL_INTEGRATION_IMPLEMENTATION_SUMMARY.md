# MCP Tool Integration - Implementation Summary

**Date:** 2025-11-03  
**Status:** Complete  
**Scope:** Integrate MCP tool selection into SPEC Engine workflow

---

## Overview

Successfully integrated MCP (Model Context Protocol) tool recommendation, human installation, and verification into the SPEC Engine workflow. This creates a smooth, human-in-the-loop process for identifying and installing relevant tools before SPEC execution.

---

## Changes Implemented

### A) Commander Workflow (`__SPEC_Engine/_Commander_SPEC/Spec_Commander.md`)

#### 1. Added Step 2.5: MCP Tool Analysis and Recommendation (NEW)

**Location:** Lines 190-276

**Purpose:** LLM analyses goal requirements and autonomously recommends MCP tools.

**Key Features:**
- Loads `mcp_tools_catalog.yaml` (269 servers, 2900+ tools, 24 categories)
- Analyses goal characteristics: activity type, resource access, outputs, scale, technologies
- Evaluates tool categories and individual servers autonomously
- Classifies tools into three tiers:
  - **REQUIRED:** Goal cannot be achieved without (conservative)
  - **RECOMMENDED:** Significantly improves efficiency
  - **OPTIONAL:** Nice to have, enhances workflow
- Documents rationale for each recommendation
- Non-prescriptive framework - LLM makes autonomous decisions (no rigid mappings)

**Quality Guidelines:**
- Don't over-specify tools
- Consider ecosystem (avoid redundancy)
- Balance coverage across lifecycle
- Respect DNA profile preferences
- Avoid: rigid rules, popularity bias, marking everything REQUIRED

#### 2. Updated Step 3 Output Format (REVISED)

**Location:** Lines 290-349

**Changes:**
- Draft Proposal Document now includes "Recommended MCP Toolset" section
- Shows REQUIRED, RECOMMENDED, and OPTIONAL tools with:
  - Tool name, popularity rating, tool count, category
  - Rationale (why relevant to THIS goal)
  - Provides/Alternative/Use case (context-dependent)
  - Installation command from catalog

**Example:**
```markdown
## Recommended MCP Toolset

### REQUIRED Tools (2 tools)
- **postgres** (★★★★★ | 15 tools | Databases)
  - Rationale: Core database operations essential for data management goal
  - Provides: Query execution, schema inspection, data migration
  - Install: `npm install @modelcontextprotocol/server-postgres`

### RECOMMENDED Tools (1 tool)
- **playwright** (★★★★☆ | 8 tools | Browser Automation)
  - Rationale: Browser automation improves testing workflow efficiency
  - Alternative: Manual browser testing via UI
  - Install: `npm install @modelcontextprotocol/server-playwright`
```

#### 3. Revised Step 3a: MANDATORY HUMAN REVIEW & TOOL INSTALLATION (MAJOR REVISION)

**Location:** Lines 351-511

**Changes:** Transformed from simple review to **combined 5-phase workflow**:

**Phase 1: Present Proposal**
- Shows complete proposal including MCP Toolset
- User options: [A] Approve, [R] Revise, [T] Modify tools, [C] Clarify
- Pause execution for user response

**Phase 2: Handle User Response**
- [R] REVISE: Apply changes to structure or toolset, loop to Phase 1
- [T] MODIFY tools: Adjust tool classifications only, loop to Phase 1
- [C] CLARIFY: Answer questions, re-present, loop to Phase 1
- [A] APPROVE: Proceed to Phase 3

**Phase 3: Tool Installation Instructions**
- Display installation commands for all REQUIRED tools
- Display installation commands for RECOMMENDED tools (optional)
- Display installation commands for OPTIONAL tools (if desired)
- Show OS-specific MCP config file locations
- Remind to restart MCP client
- Human installs tools NOW (in terminal, configures MCP client)

**Phase 4: Confirm Installation**
- User confirms: [Y] Installed, [N] Failed, [S] Skip
- [Y]: Log success, proceed to Step 4
- [N]: Troubleshoot, loop until [Y] or [S]
- [S]: Warning about Section 1.11 verification, confirm skip

**Phase 5: Exit Checkpoint**
- Single pause point complete
- Structure approved + tools installed
- Ready for detailed SPEC generation
- Proceed to Step 4

**Rationale:**
- Catch structural issues BEFORE detailed generation
- Ensure tools ready BEFORE execution
- Single pause = smoother workflow (not multiple pauses)
- Prevents tool-related execution failures

---

### B) Template Updates

#### 1. Spec Template (`__SPEC_Engine/_templates/Spec_template.md`)

**Added Section:** Lines 62-147

**New Section: "MCP Toolset"**

**Structure:**
```markdown
## MCP Toolset

### Installed Tools (Verified During SPEC Creation)

The following MCP servers were approved and installed during SPEC creation (Step 3a).

**REQUIRED Tools:**
{{#each mcp_tools.required}}
- **{{this.name}}**
  - Rationale: {{this.rationale}}
  - Install command: `{{this.install_command}}`
{{/each}}

**RECOMMENDED Tools:**
[similar structure]

**OPTIONAL Tools:**
[similar structure]

### Tool Verification

The executor will verify tool availability during initialisation (Section 1.11) as a **safety check**.

These tools were installed during SPEC creation (Step 3a), so verification should pass automatically.

**If verification fails**, it indicates:
- MCP configuration changed since SPEC creation
- MCP client was not properly restarted after installation
- Installation was incomplete or tools were uninstalled

Refer to installation commands above if re-installation is needed.
```

**Includes:** Full example with postgres, github, playwright, notion

**Purpose:**
- Document which tools were selected and why
- Provide re-installation instructions if verification fails
- Clarify that executor performs safety check, not initial installation

#### 2. Parameters Template (`__SPEC_Engine/_templates/parameters_template.toml`)

**Added Section:** Lines 67-106

**New Section: `[mcp_tools]`**

**Structure:**
```toml
[mcp_tools]
# List of MCP server names (strings) installed during Step 3a
required = []      # Must be installed - executor will HALT if missing
recommended = []   # Should be installed - executor will WARN if missing
optional = []      # Nice to have - no warning if missing

# Verification settings
[mcp_tools.verification]
check_on_startup = true                    # Verify tools before execution
halt_if_required_missing = true            # Stop execution if required tools absent
warn_if_recommended_missing = true         # Show warning for missing recommended
log_available_tools = true                 # Log which tools were detected

# Optional: Tool-specific configuration (add sections as needed)
# [mcp_tools.config.postgres]
# connection_string = "postgresql://localhost:5432/mydb"
# readonly = true
```

**Includes:** Complete example showing how to populate arrays and configuration

**Purpose:**
- Machine-readable tool lists for executor verification
- Configurable verification behaviour
- Optional tool-specific configuration (connection strings, credentials, etc.)

#### 3. Exe Template (`__SPEC_Engine/_templates/exe_template.md`)

**Added Section:** Lines 248-440

**New Section: 1.11 MCP Tool Verification (Safety Check)**

**Purpose:** Verify MCP tools installed during SPEC creation are still available.

**Expected Outcome:** All checks should PASS (tools already installed).

**Process:**

**Step 1:** Read tool configuration from `parameters_[descriptor].toml`
- Load required_tools, recommended_tools, optional_tools
- Load verification_settings

**Step 2:** Check if verification enabled
- If `check_on_startup = false`: Skip, proceed to Section 2
- If `check_on_startup = true`: Continue

**Step 3:** Verify REQUIRED tools
- For each tool: Attempt to detect MCP server availability
- If AVAILABLE: Log success, add to verified list
- If MISSING:
  - Log error with detailed message
  - Display installation command from spec.md
  - Display MCP config file locations (OS-specific)
  - Display troubleshooting steps
  - If `halt_if_required_missing = true`: **HALT execution**
  - If `halt_if_required_missing = false`: Log warning, continue

**Step 4:** Verify RECOMMENDED tools
- For each tool: Attempt to detect availability
- If AVAILABLE: Log success
- If MISSING:
  - If `warn_if_recommended_missing = true`: Display warning with installation info
  - **Continue execution** (do not halt)

**Step 5:** Log OPTIONAL tools
- Informational only, no verification
- Log: "OPTIONAL tool 'X' listed (not verified)"

**Step 6:** Update progress.json
- Record verification results
- Log verified/missing tools by classification
- Record overall verification status

**Step 7:** Determine overall status
- **PASS:** All required tools verified → Proceed to Section 2
- **FAIL:** Required tools missing → HALT (if configured)

**Includes:**
- Example success output
- Example failure output with detailed error messages
- JSON logging format

**Note:** This is a safety check, not initial installation. If verification fails, it indicates a configuration problem (tools removed, MCP not restarted, etc.).

---

### C) Documentation Updates

#### 1. Workflow Diagram (`__SPEC_Engine/WORKFLOW_DIAGRAM.md`)

**Added:** Lines 302-331 (Step 2.5)

**New Step 2.5: MCP Tool Analysis**

Visual representation showing:
- Loading catalog (269 servers, 2900+ tools)
- Analysing goal characteristics (activity, resources, outputs, scale)
- Identifying relevant categories
- Evaluating and classifying tools (REQUIRED/RECOMMENDED/OPTIONAL)
- Documenting rationale

**Revised:** Lines 332-414 (Step 3a)

**Updated Step 3a: Combined Review & Installation**

Visual representation showing:
- **Phase 1:** Present complete proposal (including MCP Toolset)
- User options: [A] Approve, [R] Revise, [T] Modify tools, [C] Clarify
- **Phase 2:** Installation (after [A] approval)
  - Display commands for REQUIRED/RECOMMENDED/OPTIONAL tools
  - Show installation instructions (terminal, config, restart)
  - Human installs tools NOW
- **Phase 3:** Confirm installation
  - [Y] Installed → Proceed to Step 4
  - [N] Failed → Troubleshoot
  - [S] Skip → Warning + proceed

**Rationale noted:**
- Catch issues at proposal level
- Ensure tools ready before execution
- Single pause = smoother workflow

#### 2. Getting Started (`__SPEC_Engine/GETTING_STARTED.md`)

**Updated:** Lines 128-216

**Changes:**
- Step 3 title updated to "Commander Interview and Tool Selection"
- Added Step 4: "Analyse and recommend MCP tools (Step 2.5 - NEW)"
- Updated Step 5: "Present complete proposal (Step 3 becomes Step 3a)"
- Updated proposal example to include MCP Toolset section with concrete example:
  - REQUIRED: filesystem (for reading Python file)
  - RECOMMENDED: github (for version control context)
- Step 6 updated to "MANDATORY HUMAN REVIEW & TOOL INSTALLATION (Step 3a - UPDATED)"
- Added detailed workflow explanation:
  - Questions to ask (including tool appropriateness)
  - What happens if [A] Approve (installation phase)
  - What happens if [R] Revise or [T] Modify tools (loop)
  - What happens if [C] Clarify (answer, re-present)

**Purpose:** Tutorial now guides users through new tool selection workflow with concrete examples.

#### 3. README (`__SPEC_Engine/README.md`)

**Added Section:** Lines 172-192

**New Section: "MCP Tool Integration (NEW - 2025-11-03)"**

**Content:**
- Brief overview of integration
- Key steps: Step 2.5, Step 3a, Section 1.11
- Tool Catalog details (269 servers, 2900+ tools, 24 categories)
- Benefits:
  - LLM autonomously selects tools
  - Human approves/installs in one step
  - Execution validates availability
  - Prevents tool-related failures
- References to GETTING_STARTED.md and WORKFLOW_DIAGRAM.md

**Purpose:** High-level introduction to new feature for users scanning README.

---

## Key Design Principles

### 1. Single Pause Workflow
- Combined structure review + tool installation into ONE pause point (Step 3a)
- Prevents workflow fragmentation
- Smoother user experience
- All approvals collected before proceeding

### 2. LLM Autonomous Reasoning
- Non-prescriptive framework for tool selection
- No rigid mappings (e.g., "if web app, always use X")
- LLM considers goal holistically and makes reasoned recommendations
- Quality guidelines (not rules) prevent over-specification

### 3. Human in the Loop
- LLM **recommends**, human **installs**
- Human can modify tool selections ([T] option)
- Human must confirm installation before proceeding
- Respects human's better context about project needs

### 4. Safety Check, Not Installation
- Executor Section 1.11 is a **verification** step
- Assumes tools already installed during Step 3a
- Failure indicates configuration problem (not spec problem)
- Provides detailed troubleshooting guidance

### 5. Three-Tier Classification
- **REQUIRED:** Conservative - only if goal fundamentally impossible without
- **RECOMMENDED:** Common practice, significant efficiency gain
- **OPTIONAL:** Nice to have, not essential
- Clear rationale for each tier

### 6. Rationale Documentation
- Every recommended tool includes WHY it's relevant to THIS goal
- References specific goal requirements
- Alternatives noted for RECOMMENDED/OPTIONAL
- Installation commands provided inline

---

## Workflow Summary

```
User provides goal
    ↓
Commander Step 0: DNA Profile Detection
    ↓
Commander Step 1: Load Constitution
    ↓
Commander Step 2: Draft High-Level Structure
    ↓
Commander Step 2.5: Analyse Goal & Recommend MCP Tools (NEW)
    ↓
Commander Step 3: Create Draft Proposal (includes MCP Toolset)
    ↓
Commander Step 3a: MANDATORY HUMAN REVIEW & TOOL INSTALLATION (REVISED)
    ├─→ Phase 1: Present Proposal (structure + toolset)
    │   └─→ User: [A] Approve | [R] Revise | [T] Modify tools | [C] Clarify
    │       (Loop until [A] approved)
    ├─→ Phase 2: Installation Instructions
    │   └─→ Human installs REQUIRED tools (terminal + config + restart)
    ├─→ Phase 3: Confirm Installation
    │   └─→ User: [Y] Installed | [N] Failed | [S] Skip
    │       (Loop until [Y] or [S])
    └─→ Phase 4: Exit (ready for detailed generation)
    ↓
Commander Step 4: Generate Detailed Steps and Files
    ↓
Commander Step 5: Pre-Flight Validation
    ↓
Commander Step 6: Output Check
    ↓
SPEC Files Generated:
    ├─→ spec_[descriptor].md (includes MCP Toolset section)
    ├─→ parameters_[descriptor].toml (includes [mcp_tools] section)
    └─→ exe_[descriptor].md (includes Section 1.11)
    ↓
User invokes exe_[descriptor].md
    ↓
Executor Section 1.1-1.10: Standard Validation
    ↓
Executor Section 1.11: MCP Tool Verification (NEW)
    ├─→ Read [mcp_tools] from parameters.toml
    ├─→ Verify REQUIRED tools (HALT if missing)
    ├─→ Verify RECOMMENDED tools (WARN if missing)
    ├─→ Log OPTIONAL tools (informational)
    ├─→ Update progress.json
    └─→ PASS: All required tools verified → Proceed to Section 2
        FAIL: Required tools missing → HALT with detailed error
    ↓
Executor Section 2: Execution Flow
    ↓
Executor Section 6: Post-Execution Analysis & Verification
    ↓
COMPLETE
```

---

## Files Modified

1. **`__SPEC_Engine/_Commander_SPEC/Spec_Commander.md`**
   - Added Step 2.5 (MCP Tool Analysis)
   - Updated Step 3 output format (includes MCP Toolset)
   - Revised Step 3a (combined review + installation)

2. **`__SPEC_Engine/_templates/Spec_template.md`**
   - Added "MCP Toolset" section (lines 62-147)
   - Includes tool lists, rationale, installation commands
   - Explains verification process

3. **`__SPEC_Engine/_templates/parameters_template.toml`**
   - Added `[mcp_tools]` section (lines 67-106)
   - Tool arrays: required, recommended, optional
   - Verification settings
   - Optional tool-specific configuration

4. **`__SPEC_Engine/_templates/exe_template.md`**
   - Added Section 1.11 (MCP Tool Verification) (lines 248-440)
   - Detailed verification process
   - Error handling and troubleshooting
   - Example outputs (success/failure)
   - JSON logging format

5. **`__SPEC_Engine/WORKFLOW_DIAGRAM.md`**
   - Added Step 2.5 visual (lines 302-331)
   - Revised Step 3a visual (lines 332-414)
   - Shows 3-phase combined workflow

6. **`__SPEC_Engine/GETTING_STARTED.md`**
   - Updated tutorial flow (lines 128-216)
   - Added tool selection example
   - Explained new Step 3a workflow
   - Updated proposal example with toolset

7. **`__SPEC_Engine/README.md`**
   - Added "MCP Tool Integration" section (lines 172-192)
   - High-level overview
   - Benefits and references

---

## Testing Recommendations

### 1. Commander Workflow Test
- Provide goal requiring specific tools (e.g., "Build Postgres-backed data dashboard")
- Verify Commander:
  - Reads `mcp_tools_catalog.yaml` successfully
  - Recommends postgres (REQUIRED), maybe grafana (RECOMMENDED)
  - Includes toolset in Draft Proposal
  - Presents [A/R/T/C] options correctly
  - Shows installation instructions after [A]
  - Loops correctly on [R]/[T]/[C]
  - Proceeds to Step 4 after [Y] confirmation

### 2. SPEC Generation Test
- After approval, verify generated files contain:
  - `spec_[descriptor].md` has MCP Toolset section with correct tools
  - `parameters_[descriptor].toml` has `[mcp_tools]` section populated
  - `exe_[descriptor].md` includes Section 1.11 verbatim

### 3. Executor Verification Test (Success Path)
- Generate SPEC with required tools already installed
- Execute `exe_[descriptor].md`
- Verify Section 1.11:
  - Reads tool lists from parameters.toml
  - Detects installed tools successfully
  - Logs success messages
  - Updates progress.json correctly
  - Proceeds to Section 2

### 4. Executor Verification Test (Failure Path)
- Generate SPEC with required tools
- Do NOT install tools (or uninstall after generation)
- Execute `exe_[descriptor].md`
- Verify Section 1.11:
  - Detects missing required tool
  - Displays detailed error message
  - Shows installation command from spec.md
  - Shows MCP config locations
  - HALTS execution (if configured)
  - Does NOT proceed to Section 2

### 5. Human Workflow Test
- Real user scenario:
  - Provide goal: "Analyse sentiment in 10k product reviews from CSV"
  - Review Commander's tool recommendations (maybe filesystem + github)
  - Agree/disagree with recommendations
  - Try [T] Modify tools option
  - Accept proposal [A]
  - Follow installation instructions
  - Install tools in terminal
  - Configure MCP client
  - Restart MCP client
  - Confirm [Y] installation
  - Verify Commander proceeds
  - Execute generated SPEC
  - Verify tools work during execution

### 6. Edge Cases
- Goal with NO required tools (Commander should recommend none or very few)
- Goal with MANY potential tools (Commander should be selective)
- User rejects all recommendations ([T] Modify → remove all)
- User adds custom tool not in catalog (check if Commander accepts)
- User skips installation ([S] → verify warning shown)
- Verification disabled (`check_on_startup = false` → verify Section 1.11 skipped)

---

## Future Enhancements (Not Implemented)

### 1. Tool Availability Detection
- Current: Section 1.11 "attempts to detect" but method not fully specified
- Future: Implement actual MCP server detection logic
  - Check MCP client config file for server entries
  - Attempt to ping MCP servers
  - Parse MCP client logs for server status
  - Platform-specific detection methods

### 2. Auto-Installation Support
- Current: Human must manually install tools
- Future: Option to auto-install via Commander
  - Run npm install commands automatically
  - Modify MCP client config file programmatically
  - Restart MCP client via system commands
  - Verify installation success
  - Fallback to manual if auto-install fails

### 3. Tool Usage Tracking
- Current: Tools recommended but usage not tracked
- Future: Track which tools were actually used during execution
  - Log tool invocations in progress.json
  - Compare recommended vs. actually used
  - Feedback loop: improve future recommendations
  - Identify over-specification (recommended but unused)

### 4. Catalog Version Management
- Current: Static catalog file
- Future: Version-aware catalog updates
  - Check for catalog updates on SPEC creation
  - Download new versions of mcp_tools_catalog.yaml
  - Track catalog version in parameters.toml
  - Warn if catalog significantly outdated

### 5. Tool Dependency Resolution
- Current: Tools recommended independently
- Future: Detect tool dependencies
  - Some tools require others (e.g., github + filesystem)
  - Auto-recommend dependencies
  - Warn about incompatibilities
  - Suggest complementary tools

### 6. DNA Profile Tool Preferences
- Current: DNA profile not integrated with tool selection
- Future: Add tool preferences to project_constitution.toml
  - Preferred tool providers (e.g., always use Postgres vs. MySQL)
  - Excluded tools (e.g., never recommend AWS if using Azure)
  - Custom tool aliases or wrappers
  - Commander respects DNA preferences during Step 2.5

---

## Notes

### Linter Warnings
- Markdown linter shows 438 warnings across modified files
- Most are pre-existing style issues (blanks around headings, list formatting)
- No functional errors introduced
- Acceptable for now (style, not syntax)
- Consider markdown linting pass as separate task if desired

### Tool Detection Implementation
- Section 1.11 describes verification process but doesn't specify exact detection method
- Platform-specific implementation needed:
  - Windows: Check `%APPDATA%\Claude\claude_desktop_config.json`
  - macOS: Check `~/Library/Application Support/Claude/claude_desktop_config.json`
  - Linux: Check `~/.config/Claude/claude_desktop_config.json`
- Alternative: Attempt MCP server invocation and check for response
- Left as implementation detail for executor runtime

### Handlebars Syntax
- Used Handlebars-like syntax (`{{#each}}`) in spec_template.md
- This is template syntax for Commander to populate
- Not actual Handlebars rendering (Commander does string replacement)
- Clarifies structure for Commander LLM when generating concrete specs

### Non-Prescriptive Philosophy
- Critical design choice: LLM autonomy in tool selection
- Avoids rigid decision trees that become outdated
- Respects LLM's reasoning capabilities
- User explicitly requested this approach
- Balance: Provide guidelines, not rules

---

## Completion Checklist

- ✅ Commander Step 2.5 added (MCP Tool Analysis)
- ✅ Commander Step 3a revised (Combined review + installation)
- ✅ spec_template.md updated (MCP Toolset section)
- ✅ parameters_template.toml updated ([mcp_tools] section)
- ✅ exe_template.md updated (Section 1.11 verification)
- ✅ WORKFLOW_DIAGRAM.md updated (Steps 2.5 and 3a)
- ✅ GETTING_STARTED.md updated (Tutorial with examples)
- ✅ README.md updated (Overview section)
- ✅ Single pause workflow implemented
- ✅ Non-prescriptive framework for LLM autonomy
- ✅ Human-in-the-loop maintained (review + install)
- ✅ Safety check design (verification, not installation)
- ✅ Three-tier classification (REQUIRED/RECOMMENDED/OPTIONAL)
- ✅ Rationale documentation required
- ✅ Installation commands included
- ✅ Troubleshooting guidance provided
- ✅ Example outputs included
- ✅ Progress.json logging format defined

---

## User Feedback Integration

All user requests integrated:

1. **"This should be part of every SPEC process"**
   - ✅ Step 2.5 is now mandatory in Commander workflow
   - ✅ MCP Toolset section now in every spec_template.md
   - ✅ Section 1.11 now in every exe_template.md

2. **"File system changes to templates need to be generic, but you may add examples"**
   - ✅ Templates use generic Handlebars-like syntax for population
   - ✅ Examples provided separately (postgres, github, playwright, notion)
   - ✅ Comments explain how to populate

3. **"You should not be biasing the LLM decisions about tool type or provider"**
   - ✅ Non-prescriptive framework implemented
   - ✅ Guidelines provided, not rigid rules
   - ✅ LLM makes autonomous decisions
   - ✅ No "if X always use Y" mappings
   - ✅ Quality principles focus on reasoning process

4. **"Step 3a will combine Human approval and Installation"**
   - ✅ Single pause point implemented
   - ✅ Phase 1: Review + approve
   - ✅ Phase 2: Install (human action)
   - ✅ Phase 3: Confirm
   - ✅ No separate pause points

5. **"Smoother, single pause workflow"**
   - ✅ Everything happens at Step 3a
   - ✅ Review → Approve → Install → Confirm → Proceed
   - ✅ No fragmentation
   - ✅ Loop on [R]/[T]/[C] until [A]
   - ✅ Single exit to Step 4

---

## Document Storage

This summary document saved to:
- **Location:** `@filing/_chats/MCP_TOOL_INTEGRATION_IMPLEMENTATION_SUMMARY.md`
- **Purpose:** Reference for key responses and implementation details
- **Aligns with:** User's preference to store original documents as markdown in @filing/ folder

---

**END OF SUMMARY**



