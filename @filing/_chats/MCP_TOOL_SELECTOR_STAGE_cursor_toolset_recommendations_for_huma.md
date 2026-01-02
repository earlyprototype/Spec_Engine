# Toolset recommendations for human codesigner
_Exported on 11/3/2025 at 19:03:14 GMT from Cursor (2.0.40)_

---

**User**

@GETTING_STARTED.md @README.md are we asking our SPECs to examine our  @mcp_tools_catalog.yaml to suggest a toolset for the human codesigner to install to support development

---

**Cursor**

Looking at the documentation you've provided, I **don't see explicit integration** between the SPEC generation process and the `mcp_tools_catalog.yaml` for tool selection.

## Current State

From `GETTING_STARTED.md` and `README.md`:
- The Commander generates SPECs based on goals
- DNA profiles configure project-level preferences (testing, risk, autonomy)
- Software stack is defined for build goals (Article XIV)
- **No mention of MCP tool catalog examination or tool suggestions**

From `mcp_tools_catalog.yaml`:
- Comprehensive catalog exists (269 servers, 2900+ tools, 24 categories)
- Usage guidelines suggest reviewing categories relevant to goal type
- Section at bottom: "Category Usage Guidelines" maps goal types to tool categories
- But this appears to be **reference documentation**, not an automated integration

## The Gap

The catalog has **usage notes** that suggest humans should:
```yaml
## Category Usage Guidelines

- **Web apps:** Web Development, Databases, Cloud & Infrastructure, Testing
- **APIs:** APIs & Integration, Testing, Development Tools
- **Desktop apps:** File Operations, Databases (local), Development Tools
```

But there's no documented process where:
1. Commander examines the catalog
2. Matches goal type to relevant tool categories
3. Suggests specific MCP servers to install
4. Marks them as "Required" or "Optional"

## Question for You

**Are you asking whether:**

**A)** This integration currently exists but isn't documented in the files I'm seeing?

**B)** This integration SHOULD exist, and you want to add it to the SPEC workflow?

**C)** Something else?

If **(B)**, I can help design where this would fit. Logically, it would slot into the Commander workflow during **Step 2-3** (high-level structure drafting) where it could:
- Analyse the goal type
- Scan `mcp_tools_catalog.yaml` for relevant categories
- Suggest 3-5 key MCP servers
- Present them during the mandatory human review phase

Would you like me to propose how to integrate this?

```yaml
## Category Usage Guidelines

- **Web apps:** Web Development, Databases, Cloud & Infrastructure, Testing
- **APIs:** APIs & Integration, Testing, Development Tools
- **Desktop apps:** File Operations, Databases (local), Development Tools
```

---

**User**

Yeah, this should be part of every SPEC process

---

**Cursor**

Right, let's design this integration properly. Here's how MCP tool catalog examination should fit into the SPEC workflow:

## Proposed Integration: MCP Tool Selection Phase

### Where It Fits

Add a new **Step 2.5** in the Commander workflow:

```
Step 2: Draft high-level structure
Step 2.5: [NEW] Analyse goal and recommend MCP tools  ← INSERT HERE
Step 3: Present structure for review
Step 3a: MANDATORY HUMAN REVIEW (now includes tool selections)
Step 4: Generate detailed steps
```

### How It Works

#### Commander Workflow Addition

**Step 2.5: MCP Tool Analysis**

1. **Goal Classification**
   - Extract goal type from high-level structure
   - Map to catalog categories using Usage Guidelines (lines 3967-3976)
   - Example: "Build a REST API" → APIs & Integration, Databases, Testing

2. **Catalog Examination**
   - Read `__SPEC_Engine/_tools/mcp_tools_catalog.yaml`
   - Filter to relevant categories
   - Rank by popularity (★ rating) and tool count
   - Consider DNA profile preferences if they exist

3. **Recommendation Generation**
   - Select 3-7 MCP servers per goal
   - Classify each as:
     - **REQUIRED:** Goal cannot be achieved without this
     - **RECOMMENDED:** Significantly improves efficiency
     - **OPTIONAL:** Nice to have, alternatives exist

4. **Present to Human**

```markdown
# SPEC Proposal for Review

## Goal
[Your goal here]

## Recommended MCP Toolset  ← NEW SECTION

### REQUIRED Tools
- **postgres** (Popularity: ★★★★★)
  - Why: Database operations essential for data management goal
  - Tools provided: 1 (query)
  - Install: `npm install @modelcontextprotocol/server-postgres`

### RECOMMENDED Tools
- **github** (Popularity: ★★★★★)
  - Why: Repository management and version control
  - Tools provided: 26 (file operations, PR management)
  - Install: `npm install @modelcontextprotocol/server-github`

### OPTIONAL Tools
- **playwright** (Popularity: ★★★★★)
  - Why: Automated testing for web interfaces
  - Tools provided: 21 (browser automation)
  - Install: `npm install @modelcontextprotocol/server-playwright`

## Tasks (High-Level)
[Rest of proposal...]
```

### During Human Review (Step 3a)

Commander asks:
```
[A] Approve structure AND toolset
[R] Revise structure or toolset
[T] Modify tools only
[C] Clarify
```

Human can:
- Accept all recommendations
- Remove optional tools
- Add tools Commander didn't suggest
- Upgrade optional → required
- Downgrade required → recommended

### File System Changes

#### 1. Add to `spec_[descriptor].md`

New section after "Definition of Complete":

```markdown
## MCP Toolset

### Installation Required
Before executing this SPEC, install these MCP servers:

**REQUIRED:**
- postgres (`npm install @modelcontextprotocol/server-postgres`)
- github (`npm install @modelcontextprotocol/server-github`)

**RECOMMENDED:**
- playwright (`npm install @modelcontextprotocol/server-playwright`)

### Tool Verification
The executor will verify tool availability during initialisation (Section 1.11).
```

#### 2. Add to `parameters_[descriptor].toml`

```toml
[mcp_tools]
required = ["postgres", "github"]
recommended = ["playwright"]
optional = []

[mcp_tools.verification]
check_on_startup = true
halt_if_required_missing = true
warn_if_recommended_missing = true
```

#### 3. Add to `exe_[descriptor].md`

New Section 1.11 (after constitutional validation):

```markdown
### Section 1.11: MCP Tool Verification

**Purpose:** Verify required MCP servers are available before execution.

1. Read `mcp_tools.required` from parameters.toml
2. For each required tool:
   - Attempt to detect availability (check MCP server connection)
   - If unavailable:
     - Log error: "Required MCP server '[name]' not found"
     - Display installation command
     - HALT execution

3. Read `mcp_tools.recommended` from parameters.toml
4. For each recommended tool:
   - Attempt to detect availability
   - If unavailable:
     - Log warning: "Recommended MCP server '[name]' not found"
     - Display installation command
     - Continue execution (do not halt)

5. Update progress.json with tool availability status
```

### Tool Selection Logic

Commander should use this decision tree:

```
1. Is this a build goal? (Article XIV applies)
   YES → Include relevant language/framework tools
   NO → Continue

2. What's the primary goal category?
   - Web Development → cloudflare-browser-rendering, playwright, puppeteer
   - Database Operations → postgres, mongodb, redis (based on stack)
   - API Integration → fetch, postman, openapi-schema
   - File Operations → filesystem, rust-mcp-filesystem
   - Research/Analysis → paper-search, brave, tavily
   - Communication → slack, gmail-mcp, resend
   - Cloud/DevOps → aws-*, azure, kubernetes, docker
   - etc.

3. What's the secondary category? (cross-functional)
   - Most goals → github (version control)
   - Testing needed → playwright, browserbase
   - Documentation → notion, obsidian, markdownify
   - Security → semgrep, ramparts

4. Check DNA profile (if exists)
   - Does project_constitution.toml specify preferred tools?
   - Does it exclude certain categories?
   - Apply those constraints

5. Rank by:
   - Popularity (★★★★★ first)
   - Tool count (more tools = more versatile)
   - Relevance to specific goal
```

### Example: Full Integration

**User Goal:** "Build a REST API for managing customer data with PostgreSQL backend"

**Commander Step 2.5 Output:**

```markdown
## Recommended MCP Toolset

### REQUIRED Tools (3)

1. **postgres** (★★★★★ | 1 tool)
   - Essential for PostgreSQL database operations
   - Provides: Read-only database access, query execution
   - `npm install @modelcontextprotocol/server-postgres`

2. **github** (★★★★★ | 26 tools)
   - Version control and repository management
   - Provides: File operations, PR creation, branch management
   - `npm install @modelcontextprotocol/server-github`

3. **postman** (★★☆☆☆ | 38 tools)
   - API testing and documentation
   - Provides: Collection management, request testing
   - `npm install @modelcontextprotocol/server-postman`

### RECOMMENDED Tools (2)

4. **openapi-schema** (★★☆☆☆ | 10 tools)
   - API documentation and schema validation
   - Provides: OpenAPI spec generation and validation
   - Alternative: Manual OpenAPI file creation
   - `npm install @modelcontextprotocol/server-openapi-schema`

5. **sentry** (★★★★★ | 1 tool)
   - Error tracking and monitoring
   - Provides: Issue retrieval and debugging info
   - Alternative: Console logging
   - `npm install @modelcontextprotocol/server-sentry`

### Tool Selection Rationale
- **Goal type:** Web Development + Databases + APIs
- **Primary category:** Databases (postgres required)
- **Secondary categories:** API Integration, Version Control
- **Build goal detected:** Yes (Article XIV applies)
- **Software stack:** Python, PostgreSQL, REST
```

**Human Review:**
```
Review MCP Toolset Selection
============================

[A] Approve all 5 tools (3 required, 2 recommended)
[R] Revise selections
[T] Modify tools individually
[S] Skip tool recommendations (use system defaults)

Selection: T

Modify Tools:
1. postgres [REQUIRED] - Keep? [Y/n]: Y
2. github [REQUIRED] - Keep? [Y/n]: Y
3. postman [REQUIRED] - Keep? [Y/n]: n (change to RECOMMENDED)
4. openapi-schema [RECOMMENDED] - Keep? [Y/n]: Y
5. sentry [RECOMMENDED] - Keep? [Y/n]: n (remove)

Add additional tools? [y/N]: N

Final toolset: 2 required, 2 recommended
```

### Benefits of This Integration

1. **Reduces friction:** Human doesn't need to manually browse 269 MCP servers
2. **Context-aware:** Recommendations match goal type automatically
3. **Validates availability:** Exe checks tools before execution starts
4. **Educational:** Humans learn which tools exist for which purposes
5. **Flexible:** Can override, add, or remove suggestions
6. **Constitutional:** Aligns with Article II (clear prerequisites) and Article X (logging)

### Next Steps to Implement

Would you like me to:

**A)** Draft the specific Commander workflow additions (detailed step-by-step)?

**B)** Create the template modifications (spec, parameters, exe templates)?

**C)** Design the tool detection/verification logic for exe?

**D)** All of the above?

This should become **mandatory** in every SPEC generation, not optional, since having the right tools fundamentally affects goal achievability.

```plaintext
Step 2: Draft high-level structure
Step 2.5: [NEW] Analyse goal and recommend MCP tools  ← INSERT HERE
Step 3: Present structure for review
Step 3a: MANDATORY HUMAN REVIEW (now includes tool selections)
Step 4: Generate detailed steps
```

```markdown
# SPEC Proposal for Review

## Goal
[Your goal here]

## Recommended MCP Toolset  ← NEW SECTION

### REQUIRED Tools
- **postgres** (Popularity: ★★★★★)
  - Why: Database operations essential for data management goal
  - Tools provided: 1 (query)
  - Install: `npm install @modelcontextprotocol/server-postgres`

### RECOMMENDED Tools
- **github** (Popularity: ★★★★★)
  - Why: Repository management and version control
  - Tools provided: 26 (file operations, PR management)
  - Install: `npm install @modelcontextprotocol/server-github`

### OPTIONAL Tools
- **playwright** (Popularity: ★★★★★)
  - Why: Automated testing for web interfaces
  - Tools provided: 21 (browser automation)
  - Install: `npm install @modelcontextprotocol/server-playwright`

## Tasks (High-Level)
[Rest of proposal...]
```

```plaintext
[A] Approve structure AND toolset
[R] Revise structure or toolset
[T] Modify tools only
[C] Clarify
```

```markdown
## MCP Toolset

### Installation Required
Before executing this SPEC, install these MCP servers:

**REQUIRED:**
- postgres (`npm install @modelcontextprotocol/server-postgres`)
- github (`npm install @modelcontextprotocol/server-github`)

**RECOMMENDED:**
- playwright (`npm install @modelcontextprotocol/server-playwright`)

### Tool Verification
The executor will verify tool availability during initialisation (Section 1.11).
```

```toml
[mcp_tools]
required = ["postgres", "github"]
recommended = ["playwright"]
optional = []

[mcp_tools.verification]
check_on_startup = true
halt_if_required_missing = true
warn_if_recommended_missing = true
```

```markdown
### Section 1.11: MCP Tool Verification

**Purpose:** Verify required MCP servers are available before execution.

1. Read `mcp_tools.required` from parameters.toml
2. For each required tool:
   - Attempt to detect availability (check MCP server connection)
   - If unavailable:
     - Log error: "Required MCP server '[name]' not found"
     - Display installation command
     - HALT execution

3. Read `mcp_tools.recommended` from parameters.toml
4. For each recommended tool:
   - Attempt to detect availability
   - If unavailable:
     - Log warning: "Recommended MCP server '[name]' not found"
     - Display installation command
     - Continue execution (do not halt)

5. Update progress.json with tool availability status
```

```plaintext
1. Is this a build goal? (Article XIV applies)
   YES → Include relevant language/framework tools
   NO → Continue

2. What's the primary goal category?
   - Web Development → cloudflare-browser-rendering, playwright, puppeteer
   - Database Operations → postgres, mongodb, redis (based on stack)
   - API Integration → fetch, postman, openapi-schema
   - File Operations → filesystem, rust-mcp-filesystem
   - Research/Analysis → paper-search, brave, tavily
   - Communication → slack, gmail-mcp, resend
   - Cloud/DevOps → aws-*, azure, kubernetes, docker
   - etc.

3. What's the secondary category? (cross-functional)
   - Most goals → github (version control)
   - Testing needed → playwright, browserbase
   - Documentation → notion, obsidian, markdownify
   - Security → semgrep, ramparts

4. Check DNA profile (if exists)
   - Does project_constitution.toml specify preferred tools?
   - Does it exclude certain categories?
   - Apply those constraints

5. Rank by:
   - Popularity (★★★★★ first)
   - Tool count (more tools = more versatile)
   - Relevance to specific goal
```

```markdown
## Recommended MCP Toolset

### REQUIRED Tools (3)

1. **postgres** (★★★★★ | 1 tool)
   - Essential for PostgreSQL database operations
   - Provides: Read-only database access, query execution
   - `npm install @modelcontextprotocol/server-postgres`

2. **github** (★★★★★ | 26 tools)
   - Version control and repository management
   - Provides: File operations, PR creation, branch management
   - `npm install @modelcontextprotocol/server-github`

3. **postman** (★★☆☆☆ | 38 tools)
   - API testing and documentation
   - Provides: Collection management, request testing
   - `npm install @modelcontextprotocol/server-postman`

### RECOMMENDED Tools (2)

4. **openapi-schema** (★★☆☆☆ | 10 tools)
   - API documentation and schema validation
   - Provides: OpenAPI spec generation and validation
   - Alternative: Manual OpenAPI file creation
   - `npm install @modelcontextprotocol/server-openapi-schema`

5. **sentry** (★★★★★ | 1 tool)
   - Error tracking and monitoring
   - Provides: Issue retrieval and debugging info
   - Alternative: Console logging
   - `npm install @modelcontextprotocol/server-sentry`

### Tool Selection Rationale
- **Goal type:** Web Development + Databases + APIs
- **Primary category:** Databases (postgres required)
- **Secondary categories:** API Integration, Version Control
- **Build goal detected:** Yes (Article XIV applies)
- **Software stack:** Python, PostgreSQL, REST
```

```plaintext
Review MCP Toolset Selection
============================

[A] Approve all 5 tools (3 required, 2 recommended)
[R] Revise selections
[T] Modify tools individually
[S] Skip tool recommendations (use system defaults)

Selection: T

Modify Tools:
1. postgres [REQUIRED] - Keep? [Y/n]: Y
2. github [REQUIRED] - Keep? [Y/n]: Y
3. postman [REQUIRED] - Keep? [Y/n]: n (change to RECOMMENDED)
4. openapi-schema [RECOMMENDED] - Keep? [Y/n]: Y
5. sentry [RECOMMENDED] - Keep? [Y/n]: n (remove)

Add additional tools? [y/N]: N

Final toolset: 2 required, 2 recommended
```

---

**User**

File system changes to templates need to be generic, but you may add examples.



In tool selection logic, you should not be biasing the LLM decisions about tool type or provider, they can make their own mind up

---

**Cursor**

You're absolutely right. Let me revise with those constraints:

## Revised Approach: Generic Templates + LLM Autonomous Decision

### File System Changes (Generic)

#### 1. `spec_template.md` - Add after "Definition of Complete"

```markdown
## MCP Toolset

### Installation Required
Before executing this SPEC, install these MCP servers:

**REQUIRED:**
{{#each mcp_tools.required}}
- {{this.name}} (`{{this.install_command}}`)
  - Rationale: {{this.rationale}}
{{/each}}

**RECOMMENDED:**
{{#each mcp_tools.recommended}}
- {{this.name}} (`{{this.install_command}}`)
  - Rationale: {{this.rationale}}
  - Alternative: {{this.alternative}}
{{/each}}

**OPTIONAL:**
{{#each mcp_tools.optional}}
- {{this.name}} (`{{this.install_command}}`)
  - Use case: {{this.use_case}}
{{/each}}

### Tool Verification
The executor will verify tool availability during initialisation (Section 1.11).

---

**Example (populated):**

## MCP Toolset

### Installation Required
Before executing this SPEC, install these MCP servers:

**REQUIRED:**
- postgres (`npm install @modelcontextprotocol/server-postgres`)
  - Rationale: Core database operations essential for data management goal

**RECOMMENDED:**
- github (`npm install @modelcontextprotocol/server-github`)
  - Rationale: Version control and collaboration features enhance workflow
  - Alternative: Manual git operations via terminal

**OPTIONAL:**
- playwright (`npm install @modelcontextprotocol/server-playwright`)
  - Use case: Automated browser testing if UI components added later
```

#### 2. `parameters_template.toml` - Add new section

```toml
[mcp_tools]
# List of MCP server names (strings)
required = []      # Must be installed, executor will halt if missing
recommended = []   # Should be installed, executor will warn if missing
optional = []      # Nice to have, no warning if missing

# Verification settings
[mcp_tools.verification]
check_on_startup = true                    # Verify tools before execution
halt_if_required_missing = true            # Stop execution if required tools absent
warn_if_recommended_missing = true         # Show warning for missing recommended
log_available_tools = true                 # Log which tools were found

# Optional: Tool-specific configuration
# Add sections as needed for tools requiring config
# [mcp_tools.config.postgres]
# connection_string = "postgresql://localhost:5432/mydb"
# readonly = true

---

**Example (populated):**

[mcp_tools]
required = ["postgres", "github"]
recommended = ["playwright"]
optional = ["notion", "slack"]

[mcp_tools.verification]
check_on_startup = true
halt_if_required_missing = true
warn_if_recommended_missing = true
log_available_tools = true

[mcp_tools.config.postgres]
connection_string = "postgresql://localhost:5432/mydb"
readonly = true
```

#### 3. `exe_template.md` - Add Section 1.11

```markdown
### Section 1.11: MCP Tool Verification

**Purpose:** Verify required and recommended MCP servers are available before execution begins.

**Process:**

1. **Read tool lists from parameters.toml**
   ```
   required_tools = parameters.toml["mcp_tools"]["required"]
   recommended_tools = parameters.toml["mcp_tools"]["recommended"]
   optional_tools = parameters.toml["mcp_tools"]["optional"]
   ```

2. **Verify required tools**
   - For each tool in `required_tools`:
     - Attempt to detect MCP server availability
     - If unavailable:
       - Log error: `"REQUIRED MCP server '{tool_name}' not available"`
       - Check spec.md for installation command
       - Display installation instructions
       - **HALT execution** (do not proceed to Section 2)
     - If available:
       - Log success: `"✅ REQUIRED tool '{tool_name}' verified"`

3. **Verify recommended tools**
   - For each tool in `recommended_tools`:
     - Attempt to detect MCP server availability
     - If unavailable:
       - Log warning: `"⚠️ RECOMMENDED MCP server '{tool_name}' not available"`
       - Display installation instructions
       - **Continue execution** (do not halt)
     - If available:
       - Log success: `"✅ RECOMMENDED tool '{tool_name}' verified"`

4. **Log optional tools** (no verification required)
   - For each tool in `optional_tools`:
     - Log info: `"ℹ️ OPTIONAL tool '{tool_name}' listed"`

5. **Update progress.json**
   ```json
   {
     "mcp_tools": {
       "required_verified": ["postgres", "github"],
       "required_missing": [],
       "recommended_verified": ["playwright"],
       "recommended_missing": [],
       "verification_timestamp": "2025-11-03T12:00:00Z"
     }
   }
   ```

6. **Proceed to Section 2** (if all required tools verified)

**Validation Outcome:**
- All required tools available → Proceed
- Any required tool missing → HALT with installation instructions

---

**Example output:**

```
Section 1.11: MCP Tool Verification
====================================

Checking 2 required tools...
  ✅ REQUIRED tool 'postgres' verified
  ✅ REQUIRED tool 'github' verified

Checking 1 recommended tool...
  ⚠️ RECOMMENDED tool 'playwright' not available
     Install: npm install @modelcontextprotocol/server-playwright
     Rationale: Automated browser testing if UI components added later
     Continuing without this tool...

All required tools verified. Proceeding to execution.
```
```

### Tool Selection Logic (Non-Prescriptive Framework)

Instead of "Web Development → use playwright", give the LLM a reasoning framework:

#### Commander Step 2.5: MCP Tool Analysis Process

```markdown
## Step 2.5: Analyse Goal and Recommend MCP Tools

**Your task:** Examine the goal, review the MCP catalog, and recommend tools using autonomous reasoning.

### Process

1. **Load the catalog**
   - Read `__SPEC_Engine/_tools/mcp_tools_catalog.yaml` completely
   - Available: 269 MCP servers, 2900+ tools, 24 categories

2. **Analyse the goal characteristics**
   - What is the primary activity? (building, analysing, researching, processing, etc.)
   - What resources will be accessed? (files, databases, APIs, websites, etc.)
   - What outputs will be created? (code, reports, data, documentation, etc.)
   - What scale/complexity? (simple script, full application, data pipeline, etc.)
   - Are there explicit technology mentions? (languages, frameworks, platforms)

3. **Identify relevant categories**
   - Review the 24 categories in the catalog
   - Consider which categories align with goal characteristics
   - Don't limit yourself to obvious categories - consider cross-functional needs

4. **Evaluate individual MCP servers**
   For each potentially relevant server, consider:
   - **Relevance:** How directly does this support the goal?
   - **Capability:** Does it provide tools that would be actively used?
   - **Popularity:** ★ rating indicates maturity and reliability
   - **Tool count:** More tools = more versatile, but evaluate if needed
   - **Alternatives:** Are there other ways to achieve the same outcome?

5. **Classify tools into tiers**

   **REQUIRED:** Mark as required ONLY if:
   - Goal cannot be achieved without this tool
   - No reasonable alternative exists within the goal scope
   - Absence would block core functionality
   
   **RECOMMENDED:** Mark as recommended if:
   - Significantly improves efficiency or quality
   - Common practice for this type of goal
   - Reasonable alternatives exist but are less efficient
   
   **OPTIONAL:** Mark as optional if:
   - Nice to have for edge cases
   - Relevant to potential future extensions
   - Enhances but not essential to core goal

6. **Document rationale**
   - For each selected tool, explain WHY it's relevant
   - Reference specific goal requirements
   - For recommended/optional, note the alternative approach

7. **Present recommendations**
   - Show 3-10 tools typically (not too few, not overwhelming)
   - Include installation commands from catalog
   - Invite human to modify selections

### Guidelines (Not Rules)

- **Don't over-specify:** If goal can be achieved multiple ways, suggest one tool but note alternatives
- **Consider ecosystem:** Some tools work well together (e.g., github + gitlab redundant)
- **Respect DNA profile:** If project constitution specifies preferences, factor those in
- **Balance coverage:** Don't select 5 database tools for one database operation
- **Think holistically:** Consider full lifecycle (development, testing, deployment, monitoring)

### What NOT to do

❌ Don't apply rigid category mappings ("if X then always Y")
❌ Don't recommend tools just because they're popular
❌ Don't mark everything as REQUIRED (be selective)
❌ Don't ignore the human review phase (they may have better context)
❌ Don't recommend redundant tools that do the same thing

### Output Format

Present recommendations in this structure:
```

Then show the markdown template structure I provided earlier, but emphasize it's the LLM's autonomous analysis, not following a decision tree.

### Example: LLM Reasoning (Not Prescriptive)

**User Goal:** "Analyse customer feedback CSV and generate sentiment report"

**LLM's autonomous reasoning:**

```markdown
## Step 2.5: MCP Tool Analysis

### Goal Analysis
- Primary activity: Data analysis
- Resources accessed: CSV file (local filesystem)
- Outputs created: Sentiment analysis report (text/markdown)
- Scale: Single-file processing, analytical output
- Technology: Not specified (implementation flexible)

### Catalog Review
Examined 269 servers across 24 categories. Focused on:
- File Operations (filesystem access)
- Data & Analysis (processing capabilities)
- AI & ML (sentiment analysis)
- Search & Research (context gathering if needed)

### Tool Recommendations

**REQUIRED: 1 tool**

1. **filesystem** (★★★★★ | 11 tools | Cloud & Infrastructure)
   - Rationale: Must read CSV file from local storage
   - Tools needed: `read_file`, `write_file` (for output report)
   - No alternative: Goal specifies CSV file, requires filesystem access
   - Install: `npm install @modelcontextprotocol/server-filesystem`

**RECOMMENDED: 2 tools**

2. **paper-search** (★★★☆☆ | 23 tools | Search & Research)
   - Rationale: May need to reference sentiment analysis methodologies
   - Alternative: Implement sentiment logic without external reference
   - Tools useful: Research papers on NLP sentiment techniques
   - Install: `npm install @modelcontextprotocol/server-paper-search`

3. **markdownify** (★★★☆☆ | 10 tools | Content Processing)
   - Rationale: Generate structured markdown report from analysis results
   - Alternative: Manual markdown formatting in code
   - Tools useful: `get-markdown-file` for report generation
   - Install: `npm install @modelcontextprotocol/server-markdownify`

**OPTIONAL: 1 tool**

4. **notion** (★★★★☆ | 19 tools | Productivity & Collaboration)
   - Use case: If user wants to publish report to Notion workspace
   - Not essential: File-based report sufficient for stated goal
   - Install: `npm install @modelcontextprotocol/server-notion`

### Selection Rationale
- Only filesystem marked REQUIRED (direct goal dependency)
- Sentiment analysis can be implemented without external tools
- Research and formatting tools recommended for quality, not necessity
- Notion optional for potential workflow integration
- Intentionally avoided database tools (not needed for single CSV)
- Skipped browser automation (no web interaction in goal)
```

Notice: The LLM examined the catalog, reasoned about the goal, and made decisions. It didn't follow "CSV analysis → use these 5 tools" rules. It considered alternatives, evaluated necessity, and explained its thinking.

### Summary of Changes

**Templates:** Generic structures with examples, no hardcoded tools
**Logic:** Framework for reasoning, not prescriptive decision tree
**LLM Agency:** Full autonomy to analyse catalog and make contextual decisions
**Human Control:** Review phase allows override of any LLM recommendations

Does this approach better align with keeping the LLM's decision-making autonomous while providing structure?

```markdown
## MCP Toolset

### Installation Required
Before executing this SPEC, install these MCP servers:

**REQUIRED:**
{{#each mcp_tools.required}}
- {{this.name}} (`{{this.install_command}}`)
  - Rationale: {{this.rationale}}
{{/each}}

**RECOMMENDED:**
{{#each mcp_tools.recommended}}
- {{this.name}} (`{{this.install_command}}`)
  - Rationale: {{this.rationale}}
  - Alternative: {{this.alternative}}
{{/each}}

**OPTIONAL:**
{{#each mcp_tools.optional}}
- {{this.name}} (`{{this.install_command}}`)
  - Use case: {{this.use_case}}
{{/each}}

### Tool Verification
The executor will verify tool availability during initialisation (Section 1.11).

---

**Example (populated):**

## MCP Toolset

### Installation Required
Before executing this SPEC, install these MCP servers:

**REQUIRED:**
- postgres (`npm install @modelcontextprotocol/server-postgres`)
  - Rationale: Core database operations essential for data management goal

**RECOMMENDED:**
- github (`npm install @modelcontextprotocol/server-github`)
  - Rationale: Version control and collaboration features enhance workflow
  - Alternative: Manual git operations via terminal

**OPTIONAL:**
- playwright (`npm install @modelcontextprotocol/server-playwright`)
  - Use case: Automated browser testing if UI components added later
```

```toml
[mcp_tools]
# List of MCP server names (strings)
required = []      # Must be installed, executor will halt if missing
recommended = []   # Should be installed, executor will warn if missing
optional = []      # Nice to have, no warning if missing

# Verification settings
[mcp_tools.verification]
check_on_startup = true                    # Verify tools before execution
halt_if_required_missing = true            # Stop execution if required tools absent
warn_if_recommended_missing = true         # Show warning for missing recommended
log_available_tools = true                 # Log which tools were found

# Optional: Tool-specific configuration
# Add sections as needed for tools requiring config
# [mcp_tools.config.postgres]
# connection_string = "postgresql://localhost:5432/mydb"
# readonly = true

---

**Example (populated):**

[mcp_tools]
required = ["postgres", "github"]
recommended = ["playwright"]
optional = ["notion", "slack"]

[mcp_tools.verification]
check_on_startup = true
halt_if_required_missing = true
warn_if_recommended_missing = true
log_available_tools = true

[mcp_tools.config.postgres]
connection_string = "postgresql://localhost:5432/mydb"
readonly = true
```

```markdown
### Section 1.11: MCP Tool Verification

**Purpose:** Verify required and recommended MCP servers are available before execution begins.

**Process:**

1. **Read tool lists from parameters.toml**
   
```

```plaintext

2. **Verify required tools**
   - For each tool in `required_tools`:
     - Attempt to detect MCP server availability
     - If unavailable:
       - Log error: `"REQUIRED MCP server '{tool_name}' not available"`
       - Check spec.md for installation command
       - Display installation instructions
       - **HALT execution** (do not proceed to Section 2)
     - If available:
       - Log success: `"✅ REQUIRED tool '{tool_name}' verified"`

3. **Verify recommended tools**
   - For each tool in `recommended_tools`:
     - Attempt to detect MCP server availability
     - If unavailable:
       - Log warning: `"⚠️ RECOMMENDED MCP server '{tool_name}' not available"`
       - Display installation instructions
       - **Continue execution** (do not halt)
     - If available:
       - Log success: `"✅ RECOMMENDED tool '{tool_name}' verified"`

4. **Log optional tools** (no verification required)
   - For each tool in `optional_tools`:
     - Log info: `"ℹ️ OPTIONAL tool '{tool_name}' listed"`

5. **Update progress.json**
   ```json
   {
     "mcp_tools": {
       "required_verified": ["postgres", "github"],
       "required_missing": [],
       "recommended_verified": ["playwright"],
       "recommended_missing": [],
       "verification_timestamp": "2025-11-03T12:00:00Z"
     }
   }
   ```

6. **Proceed to Section 2** (if all required tools verified)

**Validation Outcome:**
- All required tools available → Proceed
- Any required tool missing → HALT with installation instructions

---

**Example output:**

```
Section 1.11: MCP Tool Verification
====================================

Checking 2 required tools...
  ✅ REQUIRED tool 'postgres' verified
  ✅ REQUIRED tool 'github' verified

Checking 1 recommended tool...
  ⚠️ RECOMMENDED tool 'playwright' not available
     Install: npm install @modelcontextprotocol/server-playwright
     Rationale: Automated browser testing if UI components added later
     Continuing without this tool...

All required tools verified. Proceeding to execution.
```
```

### Tool Selection Logic (Non-Prescriptive Framework)

Instead of "Web Development → use playwright", give the LLM a reasoning framework:

#### Commander Step 2.5: MCP Tool Analysis Process

```markdown
## Step 2.5: Analyse Goal and Recommend MCP Tools

**Your task:** Examine the goal, review the MCP catalog, and recommend tools using autonomous reasoning.

### Process

1. **Load the catalog**
   - Read `__SPEC_Engine/_tools/mcp_tools_catalog.yaml` completely
   - Available: 269 MCP servers, 2900+ tools, 24 categories

2. **Analyse the goal characteristics**
   - What is the primary activity? (building, analysing, researching, processing, etc.)
   - What resources will be accessed? (files, databases, APIs, websites, etc.)
   - What outputs will be created? (code, reports, data, documentation, etc.)
   - What scale/complexity? (simple script, full application, data pipeline, etc.)
   - Are there explicit technology mentions? (languages, frameworks, platforms)

3. **Identify relevant categories**
   - Review the 24 categories in the catalog
   - Consider which categories align with goal characteristics
   - Don't limit yourself to obvious categories - consider cross-functional needs

4. **Evaluate individual MCP servers**
   For each potentially relevant server, consider:
   - **Relevance:** How directly does this support the goal?
   - **Capability:** Does it provide tools that would be actively used?
   - **Popularity:** ★ rating indicates maturity and reliability
   - **Tool count:** More tools = more versatile, but evaluate if needed
   - **Alternatives:** Are there other ways to achieve the same outcome?

5. **Classify tools into tiers**

   **REQUIRED:** Mark as required ONLY if:
   - Goal cannot be achieved without this tool
   - No reasonable alternative exists within the goal scope
   - Absence would block core functionality
   
   **RECOMMENDED:** Mark as recommended if:
   - Significantly improves efficiency or quality
   - Common practice for this type of goal
   - Reasonable alternatives exist but are less efficient
   
   **OPTIONAL:** Mark as optional if:
   - Nice to have for edge cases
   - Relevant to potential future extensions
   - Enhances but not essential to core goal

6. **Document rationale**
   - For each selected tool, explain WHY it's relevant
   - Reference specific goal requirements
   - For recommended/optional, note the alternative approach

7. **Present recommendations**
   - Show 3-10 tools typically (not too few, not overwhelming)
   - Include installation commands from catalog
   - Invite human to modify selections

### Guidelines (Not Rules)

- **Don't over-specify:** If goal can be achieved multiple ways, suggest one tool but note alternatives
- **Consider ecosystem:** Some tools work well together (e.g., github + gitlab redundant)
- **Respect DNA profile:** If project constitution specifies preferences, factor those in
- **Balance coverage:** Don't select 5 database tools for one database operation
- **Think holistically:** Consider full lifecycle (development, testing, deployment, monitoring)

### What NOT to do

❌ Don't apply rigid category mappings ("if X then always Y")
❌ Don't recommend tools just because they're popular
❌ Don't mark everything as REQUIRED (be selective)
❌ Don't ignore the human review phase (they may have better context)
❌ Don't recommend redundant tools that do the same thing

### Output Format

Present recommendations in this structure:
```

Then show the markdown template structure I provided earlier, but emphasize it's the LLM's autonomous analysis, not following a decision tree.

### Example: LLM Reasoning (Not Prescriptive)

**User Goal:** "Analyse customer feedback CSV and generate sentiment report"

**LLM's autonomous reasoning:**

```markdown
## Step 2.5: MCP Tool Analysis

### Goal Analysis
- Primary activity: Data analysis
- Resources accessed: CSV file (local filesystem)
- Outputs created: Sentiment analysis report (text/markdown)
- Scale: Single-file processing, analytical output
- Technology: Not specified (implementation flexible)

### Catalog Review
Examined 269 servers across 24 categories. Focused on:
- File Operations (filesystem access)
- Data & Analysis (processing capabilities)
- AI & ML (sentiment analysis)
- Search & Research (context gathering if needed)

### Tool Recommendations

**REQUIRED: 1 tool**

1. **filesystem** (★★★★★ | 11 tools | Cloud & Infrastructure)
   - Rationale: Must read CSV file from local storage
   - Tools needed: `read_file`, `write_file` (for output report)
   - No alternative: Goal specifies CSV file, requires filesystem access
   - Install: `npm install @modelcontextprotocol/server-filesystem`

**RECOMMENDED: 2 tools**

2. **paper-search** (★★★☆☆ | 23 tools | Search & Research)
   - Rationale: May need to reference sentiment analysis methodologies
   - Alternative: Implement sentiment logic without external reference
   - Tools useful: Research papers on NLP sentiment techniques
   - Install: `npm install @modelcontextprotocol/server-paper-search`

3. **markdownify** (★★★☆☆ | 10 tools | Content Processing)
   - Rationale: Generate structured markdown report from analysis results
   - Alternative: Manual markdown formatting in code
   - Tools useful: `get-markdown-file` for report generation
   - Install: `npm install @modelcontextprotocol/server-markdownify`

**OPTIONAL: 1 tool**

4. **notion** (★★★★☆ | 19 tools | Productivity & Collaboration)
   - Use case: If user wants to publish report to Notion workspace
   - Not essential: File-based report sufficient for stated goal
   - Install: `npm install @modelcontextprotocol/server-notion`

### Selection Rationale
- Only filesystem marked REQUIRED (direct goal dependency)
- Sentiment analysis can be implemented without external tools
- Research and formatting tools recommended for quality, not necessity
- Notion optional for potential workflow integration
- Intentionally avoided database tools (not needed for single CSV)
- Skipped browser automation (no web interaction in goal)
```

Notice: The LLM examined the catalog, reasoned about the goal, and made decisions. It didn't follow "CSV analysis → use these 5 tools" rules. It considered alternatives, evaluated necessity, and explained its thinking.

### Summary of Changes

**Templates:** Generic structures with examples, no hardcoded tools
**Logic:** Framework for reasoning, not prescriptive decision tree
**LLM Agency:** Full autonomy to analyse catalog and make contextual decisions
**Human Control:** Review phase allows override of any LLM recommendations

Does this approach better align with keeping the LLM's decision-making autonomous while providing structure?
```

```plaintext
Section 1.11: MCP Tool Verification
====================================

Checking 2 required tools...
  ✅ REQUIRED tool 'postgres' verified
  ✅ REQUIRED tool 'github' verified

Checking 1 recommended tool...
  ⚠️ RECOMMENDED tool 'playwright' not available
     Install: npm install @modelcontextprotocol/server-playwright
     Rationale: Automated browser testing if UI components added later
     Continuing without this tool...

All required tools verified. Proceeding to execution.
```

```plaintext

### Tool Selection Logic (Non-Prescriptive Framework)

Instead of "Web Development → use playwright", give the LLM a reasoning framework:

#### Commander Step 2.5: MCP Tool Analysis Process

```

```plaintext

Then show the markdown template structure I provided earlier, but emphasize it's the LLM's autonomous analysis, not following a decision tree.

### Example: LLM Reasoning (Not Prescriptive)

**User Goal:** "Analyse customer feedback CSV and generate sentiment report"

**LLM's autonomous reasoning:**

```

```plaintext

Notice: The LLM examined the catalog, reasoned about the goal, and made decisions. It didn't follow "CSV analysis → use these 5 tools" rules. It considered alternatives, evaluated necessity, and explained its thinking.

### Summary of Changes

**Templates:** Generic structures with examples, no hardcoded tools
**Logic:** Framework for reasoning, not prescriptive decision tree
**LLM Agency:** Full autonomy to analyse catalog and make contextual decisions
**Human Control:** Review phase allows override of any LLM recommendations

Does this approach better align with keeping the LLM's decision-making autonomous while providing structure?
```

---

**User**

1. spec_template - the LLM cant install the toolsets, they must recommend them to the user to install for them. The Spec must check that the tools have been installed by the user before continuing. But rest is good

---

**Cursor**

Ah yes, critical distinction! Let me fix the spec_template.md section:

#### 1. `spec_template.md` - Revised "MCP Toolset" Section

```markdown
## MCP Toolset

### User Installation Required
**Before executing this SPEC**, you must install the following MCP servers. The executor will verify installation during initialisation (Section 1.11) and will not proceed without required tools.

**REQUIRED Tools:**
{{#each mcp_tools.required}}
- **{{this.name}}**
  - Rationale: {{this.rationale}}
  - Install command: `{{this.install_command}}`
  - Verify: Executor will check availability before proceeding
{{/each}}

**RECOMMENDED Tools:**
{{#each mcp_tools.recommended}}
- **{{this.name}}**
  - Rationale: {{this.rationale}}
  - Alternative: {{this.alternative}}
  - Install command: `{{this.install_command}}`
  - Verify: Executor will warn if missing but continue execution
{{/each}}

**OPTIONAL Tools:**
{{#each mcp_tools.optional}}
- **{{this.name}}**
  - Use case: {{this.use_case}}
  - Install command: `{{this.install_command}}`
  - Verify: No verification required
{{/each}}

### Installation Instructions
1. Install each REQUIRED tool using the commands above
2. Configure MCP servers in your environment (e.g., Claude Desktop config)
3. Restart your MCP client if necessary
4. When ready, execute `exe_[descriptor].md`

### Tool Verification Process
The executor (Section 1.11) will:
- **Check** that all REQUIRED tools are available
- **HALT execution** if any REQUIRED tool is missing
- **Warn** if RECOMMENDED tools are missing (but continue)
- **Log** verification status to progress.json

**Do not attempt execution until REQUIRED tools are installed.**

---

**Example (populated):**

## MCP Toolset

### User Installation Required
**Before executing this SPEC**, you must install the following MCP servers. The executor will verify installation during initialisation (Section 1.11) and will not proceed without required tools.

**REQUIRED Tools:**

- **postgres**
  - Rationale: Core database operations essential for data management goal
  - Install command: `npm install @modelcontextprotocol/server-postgres`
  - Verify: Executor will check availability before proceeding

- **github**
  - Rationale: Version control and file operations required for code management
  - Install command: `npm install @modelcontextprotocol/server-github`
  - Verify: Executor will check availability before proceeding

**RECOMMENDED Tools:**

- **playwright**
  - Rationale: Browser automation improves testing workflow efficiency
  - Alternative: Manual browser testing via UI
  - Install command: `npm install @modelcontextprotocol/server-playwright`
  - Verify: Executor will warn if missing but continue execution

**OPTIONAL Tools:**

- **notion**
  - Use case: Documentation publishing if project uses Notion workspace
  - Install command: `npm install @modelcontextprotocol/server-notion`
  - Verify: No verification required

### Installation Instructions
1. Install each REQUIRED tool using the commands above
2. Configure MCP servers in your environment (e.g., Claude Desktop config at `%APPDATA%\Claude\claude_desktop_config.json` on Windows)
3. Restart Claude Desktop or your MCP client
4. When ready, execute `exe_csv_validation.md`

### Tool Verification Process
The executor (Section 1.11) will:
- **Check** that postgres and github are available
- **HALT execution** if either tool is missing
- **Warn** if playwright is missing (but continue)
- **Log** verification status to progress_csv_validation.json

**Do not attempt execution until postgres and github are installed.**
```

### Key Changes:

1. **"User Installation Required"** - Makes it clear this is human action
2. **"you must install"** - Direct instruction to user
3. **"Do not attempt execution until..."** - Explicit sequencing
4. **"Verify: Executor will check"** - Clarifies verification is automated check, not automated install
5. **Installation Instructions** - Added step-by-step process for user
6. **MCP client configuration** - Reminds user to configure their environment

### Workflow Sequence (Clarified)

```
┌─────────────────────────────────────────────────┐
│ Commander Step 2.5: Analyse & Recommend Tools   │
│ - LLM examines mcp_tools_catalog.yaml          │
│ - LLM reasons about goal requirements          │
│ - LLM classifies: REQUIRED/RECOMMENDED/OPTIONAL│
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Commander Step 3a: Human Review & Approval      │
│ - Human reviews tool recommendations           │
│ - Human approves/modifies tool list            │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Commander Generates: spec_[descriptor].md       │
│ - "User Installation Required" section         │
│ - Lists tools with install commands            │
│ - Warns: "Do not execute until installed"      │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ PAUSE: Human Installs Tools                     │
│ - User runs install commands                   │
│ - User configures MCP environment              │
│ - User restarts MCP client if needed           │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Human Launches: exe_[descriptor].md             │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Executor Section 1.11: Tool Verification        │
│ - Checks if REQUIRED tools available           │
│ - If missing: HALT with error message          │
│ - If present: Log success, continue to Sec 2   │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Executor Section 2: Execute Tasks               │
│ - Uses verified MCP tools during execution     │
└─────────────────────────────────────────────────┘
```

The critical point: **The LLM never installs anything. It recommends → Human installs → Executor verifies → Execution proceeds.**

Does this correctly capture the human-in-the-loop installation workflow?

```markdown
## MCP Toolset

### User Installation Required
**Before executing this SPEC**, you must install the following MCP servers. The executor will verify installation during initialisation (Section 1.11) and will not proceed without required tools.

**REQUIRED Tools:**
{{#each mcp_tools.required}}
- **{{this.name}}**
  - Rationale: {{this.rationale}}
  - Install command: `{{this.install_command}}`
  - Verify: Executor will check availability before proceeding
{{/each}}

**RECOMMENDED Tools:**
{{#each mcp_tools.recommended}}
- **{{this.name}}**
  - Rationale: {{this.rationale}}
  - Alternative: {{this.alternative}}
  - Install command: `{{this.install_command}}`
  - Verify: Executor will warn if missing but continue execution
{{/each}}

**OPTIONAL Tools:**
{{#each mcp_tools.optional}}
- **{{this.name}}**
  - Use case: {{this.use_case}}
  - Install command: `{{this.install_command}}`
  - Verify: No verification required
{{/each}}

### Installation Instructions
1. Install each REQUIRED tool using the commands above
2. Configure MCP servers in your environment (e.g., Claude Desktop config)
3. Restart your MCP client if necessary
4. When ready, execute `exe_[descriptor].md`

### Tool Verification Process
The executor (Section 1.11) will:
- **Check** that all REQUIRED tools are available
- **HALT execution** if any REQUIRED tool is missing
- **Warn** if RECOMMENDED tools are missing (but continue)
- **Log** verification status to progress.json

**Do not attempt execution until REQUIRED tools are installed.**

---

**Example (populated):**

## MCP Toolset

### User Installation Required
**Before executing this SPEC**, you must install the following MCP servers. The executor will verify installation during initialisation (Section 1.11) and will not proceed without required tools.

**REQUIRED Tools:**

- **postgres**
  - Rationale: Core database operations essential for data management goal
  - Install command: `npm install @modelcontextprotocol/server-postgres`
  - Verify: Executor will check availability before proceeding

- **github**
  - Rationale: Version control and file operations required for code management
  - Install command: `npm install @modelcontextprotocol/server-github`
  - Verify: Executor will check availability before proceeding

**RECOMMENDED Tools:**

- **playwright**
  - Rationale: Browser automation improves testing workflow efficiency
  - Alternative: Manual browser testing via UI
  - Install command: `npm install @modelcontextprotocol/server-playwright`
  - Verify: Executor will warn if missing but continue execution

**OPTIONAL Tools:**

- **notion**
  - Use case: Documentation publishing if project uses Notion workspace
  - Install command: `npm install @modelcontextprotocol/server-notion`
  - Verify: No verification required

### Installation Instructions
1. Install each REQUIRED tool using the commands above
2. Configure MCP servers in your environment (e.g., Claude Desktop config at `%APPDATA%\Claude\claude_desktop_config.json` on Windows)
3. Restart Claude Desktop or your MCP client
4. When ready, execute `exe_csv_validation.md`

### Tool Verification Process
The executor (Section 1.11) will:
- **Check** that postgres and github are available
- **HALT execution** if either tool is missing
- **Warn** if playwright is missing (but continue)
- **Log** verification status to progress_csv_validation.json

**Do not attempt execution until postgres and github are installed.**
```

```plaintext
┌─────────────────────────────────────────────────┐
│ Commander Step 2.5: Analyse & Recommend Tools   │
│ - LLM examines mcp_tools_catalog.yaml          │
│ - LLM reasons about goal requirements          │
│ - LLM classifies: REQUIRED/RECOMMENDED/OPTIONAL│
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Commander Step 3a: Human Review & Approval      │
│ - Human reviews tool recommendations           │
│ - Human approves/modifies tool list            │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Commander Generates: spec_[descriptor].md       │
│ - "User Installation Required" section         │
│ - Lists tools with install commands            │
│ - Warns: "Do not execute until installed"      │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ PAUSE: Human Installs Tools                     │
│ - User runs install commands                   │
│ - User configures MCP environment              │
│ - User restarts MCP client if needed           │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Human Launches: exe_[descriptor].md             │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Executor Section 1.11: Tool Verification        │
│ - Checks if REQUIRED tools available           │
│ - If missing: HALT with error message          │
│ - If present: Log success, continue to Sec 2   │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Executor Section 2: Execute Tasks               │
│ - Uses verified MCP tools during execution     │
└─────────────────────────────────────────────────┘
```

---

**User**

No, Step 3a will combine Human approval and Installation. If human approves they will install and then trigger next step. If the dissaprove, they will inform the LLM and loop that step until the human is ahppy and installs the required tools. This will create a smoother, single pause workflow

---

**Cursor**

Ah, much cleaner! Single pause point. Let me revise:

## Revised Workflow: Combined Approval + Installation (Step 3a)

### Commander Step 3a: MANDATORY HUMAN REVIEW & TOOL INSTALLATION

```markdown
## Step 3a: Human Review, Approval, and Tool Installation

**Present to human:**

```
═══════════════════════════════════════════════════════
SPEC PROPOSAL FOR REVIEW
═══════════════════════════════════════════════════════

## Goal
[Your goal statement]

## Definition of Complete
- [ ] Criterion 1
- [ ] Criterion 2

## Recommended MCP Toolset

### REQUIRED Tools (must be installed to proceed)
1. postgres (★★★★★)
   - Rationale: Core database operations essential
   - Install: `npm install @modelcontextprotocol/server-postgres`

2. github (★★★★★)
   - Rationale: Version control and file operations
   - Install: `npm install @modelcontextprotocol/server-github`

### RECOMMENDED Tools (optional but beneficial)
3. playwright (★★★★★)
   - Rationale: Browser automation for testing
   - Alternative: Manual browser testing
   - Install: `npm install @modelcontextprotocol/server-playwright`

## Tasks (High-Level)
1. [Task 1 description]
2. [Task 2 description]
3. [Task 3 description]

═══════════════════════════════════════════════════════
REVIEW OPTIONS
═══════════════════════════════════════════════════════

[A] APPROVE structure and toolset → I will install tools now
[R] REVISE structure or toolset → suggest changes
[T] MODIFY tools only → adjust tool classifications
[C] CLARIFY → ask questions before deciding

Selection:
```

### If Human Selects [A] APPROVE:

```
You selected: [A] APPROVE

INSTALLATION PHASE
══════════════════

Please install the following REQUIRED tools now:

1. postgres
   Command: npm install @modelcontextprotocol/server-postgres
   
2. github
   Command: npm install @modelcontextprotocol/server-github

Optional (RECOMMENDED) tools:
3. playwright
   Command: npm install @modelcontextprotocol/server-playwright

INSTALLATION INSTRUCTIONS:
1. Run the install commands above in your terminal
2. Configure MCP servers in your environment
   (e.g., Claude Desktop: %APPDATA%\Claude\claude_desktop_config.json)
3. Restart your MCP client if necessary
4. Test tool availability (optional but recommended)

═══════════════════════════════════════════════════════

When installation is complete, confirm:

[Y] Tools installed and configured → Proceed to SPEC generation
[N] Installation failed → Need help troubleshooting
[S] Skip tool installation for now → Generate SPEC anyway (risky)

Confirmation:
```

### If Human Confirms [Y] Tools Installed:

```
✅ Tools installed and configured
✅ Proceeding to detailed SPEC generation (Step 4)

Generating:
- spec_[descriptor].md
- parameters_[descriptor].toml  
- exe_[descriptor].md

Please wait...
```

### If Human Selects [R] REVISE or [T] MODIFY:

Loop back within Step 3a with modifications, then present updated proposal again.

**Example revision loop:**

```
You selected: [R] REVISE

What would you like to revise?
1. Goal statement or completion criteria
2. Tool recommendations
3. Task structure
4. Multiple aspects

Please describe your changes:
_______________________________________

[After human input, Commander adjusts and re-presents the proposal]

═══════════════════════════════════════════════════════
UPDATED SPEC PROPOSAL FOR REVIEW
═══════════════════════════════════════════════════════

[Shows revised version with changes highlighted]

[A] APPROVE → I will install tools now
[R] REVISE again
[etc.]
```

### Updated Workflow Sequence

```
Step 2.5: Analyse and recommend MCP tools
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ Step 3a: MANDATORY HUMAN REVIEW & TOOL INSTALLATION     │
│ ════════════════════════════════════════════════════════│
│                                                         │
│ 1. Present: Structure + Tools + Tasks                  │
│ 2. Human reviews                                       │
│                                                         │
│    If [R] REVISE or [T] MODIFY:                        │
│    ┌──────────────────────────────┐                   │
│    │ Loop: Adjust and re-present  │                   │
│    │ Until human satisfied        │                   │
│    └────────────┬─────────────────┘                   │
│                 │                                       │
│                 ▼                                       │
│    If [A] APPROVE:                                     │
│    3. Show installation commands                       │
│    4. Human installs tools NOW                         │
│    5. Human configures MCP environment                 │
│    6. Human confirms: [Y] Ready                        │
│                                                         │
│    If [Y] Confirmed:                                   │
│    ✅ Exit Step 3a → Proceed to Step 4                │
│                                                         │
│    If [N] Installation failed:                         │
│    7. Troubleshoot installation issues                 │
│    8. Loop until [Y] confirmed                         │
│                                                         │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
Step 4: Generate detailed SPEC files
  (Commander knows tools are already installed)
                  │
                  ▼
Step 5: Pre-flight validation
                  │
                  ▼
Step 6: Files written to Specs/[DNA]/spec_[descriptor]/
                  │
                  ▼
═══════════════════════════════════════════════════════════
SPEC GENERATION COMPLETE
═══════════════════════════════════════════════════════════

Files created:
✅ spec_[descriptor].md
✅ parameters_[descriptor].toml
✅ exe_[descriptor].md

MCP Tools Status:
✅ 2 REQUIRED tools installed and verified
✅ 1 RECOMMENDED tool installed

Ready for execution!
Launch: exe_[descriptor].md

═══════════════════════════════════════════════════════════
                  │
                  ▼
[Human launches exe_[descriptor].md]
                  │
                  ▼
Executor Section 1.11: Tool Verification
  (Should pass since tools were installed in Step 3a)
  - Verifies postgres: ✅ Available
  - Verifies github: ✅ Available
  - Verifies playwright: ✅ Available
                  │
                  ▼
Executor Section 2: Execute Tasks
  (Uses verified tools during execution)
```

### Benefits of Combined Workflow

1. **Single pause point:** Human doesn't have to come back later
2. **Smoother flow:** Approve → Install → Generate → Execute
3. **Verification is redundant safety check:** Tools should already work by Section 1.11
4. **Immediate feedback:** Installation problems discovered during approval phase, not later
5. **Context maintained:** Human has the tool rationale fresh in mind while installing

### What Changes in spec_template.md

Since tools are already installed by the time the SPEC is generated, the section becomes:

```markdown
## MCP Toolset

### Installed Tools (Verified During SPEC Creation)

**REQUIRED Tools:**
- postgres - Core database operations
- github - Version control and file operations

**RECOMMENDED Tools:**
- playwright - Browser automation for testing

**OPTIONAL Tools:**
- (none selected)

### Tool Verification
The executor will verify tool availability during initialisation (Section 1.11) as a safety check. These tools were installed during SPEC creation (Step 3a), so verification should pass automatically.

If verification fails, it indicates:
- MCP configuration changed since SPEC creation
- MCP client was not properly restarted
- Installation was incomplete

Refer to installation commands in Step 3a output if re-installation needed.
```

This makes the spec_template documentation of what WAS done, not instructions for what TO DO.

### What exe_template Section 1.11 Becomes

```markdown
### Section 1.11: MCP Tool Verification (Safety Check)

**Purpose:** Verify that tools installed during SPEC creation (Step 3a) are still available.

**Expected outcome:** All checks should PASS (tools were already installed).

1. Read tool lists from parameters.toml
2. Verify each REQUIRED tool
   - If missing: HALT with error "Tool removed since SPEC creation"
3. Verify each RECOMMENDED tool  
   - If missing: WARN but continue
4. Log verification status to progress.json
5. If all required tools present: Proceed to Section 2

**Note:** This is a safety check, not initial installation. Tools should have been installed during SPEC creation Step 3a. If verification fails, check:
- MCP client configuration
- Whether client was restarted after installation
- Whether tools were uninstalled since SPEC creation
```

Is this the workflow you envisioned? Single pause at Step 3a where everything happens: review → approve → install → confirm → proceed?

```markdown
## Step 3a: Human Review, Approval, and Tool Installation

**Present to human:**

```

```plaintext

### If Human Selects [A] APPROVE:

```

```plaintext

### If Human Confirms [Y] Tools Installed:

```

```plaintext

### If Human Selects [R] REVISE or [T] MODIFY:

Loop back within Step 3a with modifications, then present updated proposal again.

**Example revision loop:**

```

```plaintext

### Updated Workflow Sequence

```

```plaintext

### Benefits of Combined Workflow

1. **Single pause point:** Human doesn't have to come back later
2. **Smoother flow:** Approve → Install → Generate → Execute
3. **Verification is redundant safety check:** Tools should already work by Section 1.11
4. **Immediate feedback:** Installation problems discovered during approval phase, not later
5. **Context maintained:** Human has the tool rationale fresh in mind while installing

### What Changes in spec_template.md

Since tools are already installed by the time the SPEC is generated, the section becomes:

```markdown
## MCP Toolset

### Installed Tools (Verified During SPEC Creation)

**REQUIRED Tools:**
- postgres - Core database operations
- github - Version control and file operations

**RECOMMENDED Tools:**
- playwright - Browser automation for testing

**OPTIONAL Tools:**
- (none selected)

### Tool Verification
The executor will verify tool availability during initialisation (Section 1.11) as a safety check. These tools were installed during SPEC creation (Step 3a), so verification should pass automatically.

If verification fails, it indicates:
- MCP configuration changed since SPEC creation
- MCP client was not properly restarted
- Installation was incomplete

Refer to installation commands in Step 3a output if re-installation needed.
```

This makes the spec_template documentation of what WAS done, not instructions for what TO DO.

### What exe_template Section 1.11 Becomes

```markdown
### Section 1.11: MCP Tool Verification (Safety Check)

**Purpose:** Verify that tools installed during SPEC creation (Step 3a) are still available.

**Expected outcome:** All checks should PASS (tools were already installed).

1. Read tool lists from parameters.toml
2. Verify each REQUIRED tool
   - If missing: HALT with error "Tool removed since SPEC creation"
3. Verify each RECOMMENDED tool  
   - If missing: WARN but continue
4. Log verification status to progress.json
5. If all required tools present: Proceed to Section 2

**Note:** This is a safety check, not initial installation. Tools should have been installed during SPEC creation Step 3a. If verification fails, check:
- MCP client configuration
- Whether client was restarted after installation
- Whether tools were uninstalled since SPEC creation
```

Is this the workflow you envisioned? Single pause at Step 3a where everything happens: review → approve → install → confirm → proceed?
```

```markdown
### Section 1.11: MCP Tool Verification (Safety Check)

**Purpose:** Verify that tools installed during SPEC creation (Step 3a) are still available.

**Expected outcome:** All checks should PASS (tools were already installed).

1. Read tool lists from parameters.toml
2. Verify each REQUIRED tool
   - If missing: HALT with error "Tool removed since SPEC creation"
3. Verify each RECOMMENDED tool  
   - If missing: WARN but continue
4. Log verification status to progress.json
5. If all required tools present: Proceed to Section 2

**Note:** This is a safety check, not initial installation. Tools should have been installed during SPEC creation Step 3a. If verification fails, check:
- MCP client configuration
- Whether client was restarted after installation
- Whether tools were uninstalled since SPEC creation
```

---

**User**

agree

---

**Cursor**

Perfect! Let me summarise what needs to be implemented:

## Implementation Checklist

### 1. **Commander Workflow Changes**

**Add Step 2.5: MCP Tool Analysis**
- LLM reads `__SPEC_Engine/_tools/mcp_tools_catalog.yaml`
- LLM analyses goal autonomously (no prescriptive rules)
- LLM recommends REQUIRED/RECOMMENDED/OPTIONAL tools with rationale

**Modify Step 3a: Combined Review + Installation**
- Present structure + tools together
- Human reviews and decides: [A] Approve / [R] Revise / [T] Modify / [C] Clarify
- If [R] or [T]: Loop within Step 3a until satisfied
- If [A] Approve:
  - Show installation commands
  - Human installs tools NOW
  - Human confirms [Y] Ready / [N] Failed / [S] Skip
  - If [Y]: Exit to Step 4 (tools verified as installed)
  - If [N]: Troubleshoot and loop

### 2. **Template File Updates**

**`spec_template.md`**
- Add "MCP Toolset" section after "Definition of Complete"
- Documents tools that WERE installed during Step 3a
- Notes that Section 1.11 is safety verification only
- Generic structure with example

**`parameters_template.toml`**
- Add `[mcp_tools]` section
- Lists: `required = []`, `recommended = []`, `optional = []`
- Add `[mcp_tools.verification]` settings
- Generic structure with example

**`exe_template.md`**
- Add Section 1.11: "MCP Tool Verification (Safety Check)"
- Verify REQUIRED tools (HALT if missing)
- Verify RECOMMENDED tools (WARN if missing)
- Log to progress.json
- Frame as safety check, not initial installation
- Generic structure with example

### 3. **Documentation Updates**

**`WORKFLOW_DIAGRAM.md`**
- Add Step 2.5 (MCP Tool Analysis) 
- Update Step 3a (Combined Review + Installation)
- Update flow diagram showing single pause point

**`GETTING_STARTED.md`**
- Add tool installation instructions in tutorial
- Update example walkthroughs to include tool selection

**`README.md`**
- Note MCP tool integration in system architecture
- Add to "Key Concepts" section

---

## Next Steps

Would you like me to:

**A)** Draft the complete Commander workflow additions (Steps 2.5 and 3a detailed procedures)?

**B)** Update all three template files with the new sections?

**C)** Update WORKFLOW_DIAGRAM.md to reflect the new process?

**D)** Update GETTING_STARTED.md with tool installation tutorial?

**E)** All of the above?

Let me know which you'd like to tackle first, or if you want to handle the implementation yourself with these specifications.

---

**User**

E

---

**Cursor**

Excellent! Let me implement all changes systematically. I'll start by reading the current files to understand their structure, then update them.

Now I'll implement all the changes systematically. Let me start by updating each file:

## A) Commander Workflow Additions

```markdown
# commander-spec.md

---
## LLM Context & Role

You are a **Spec Generating Agent**.  

A **Spec** is a structured set of files designed to evoke goal-driven, agentic behaviour in LLMs.  

Your role is to **analyze a given goal or desired behaviour** and translate it into a complete, coherent Spec composed of the following files:

1. **spec_[descriptor].md** — A structured human-readable specification describing:
   - The goal, tasks, and steps required to achieve it.  
   - Constraints, components, and reasoning scaffolds.  
   - Definitions of key terms and their relationships (goal → task → step → backup).    

2. **exe_[descriptor].md** — The execution controller.  
   - This file instructs an LLM on how to interpret and act upon `spec.md` and `parameters.toml`.  
   - It defines logic for handling retries, modes, backups, and logging behaviour.

3. **parameters_[descriptor].toml** — A machine-readable version of the same spec, encoding the same goal, tasks, and steps in a format that enforces clear delineation and reduces ambiguity.

Together, these files form a **Spec**, a folder which functions as a self-contained unit of instruction that can be executed by an LLM in “agentic” mode.

---

## [META]
- **File Role:** Master coordinator for generating Spec documents.  
- **Purpose:** Guides the LLM to create a full set of structured files (known as a 'Spec') for executing a single goal.  
- **Descriptor Example:** research, debug, prototype, test, etc.  
- **Creation Folder:** `[root]/Specs/[descriptor]/`  

---

## Guidance for Goal Interpretation

You will be provided with a description of a **goal or behaviour** to model.  

This goal is your **North Star**.

Everything you generate — tasks, steps, backups, constraints — must directly support achieving this goal.

Before writing, you must:
1. Understand the intent and scope of the goal.  
2. Decompose it into logical, sequential **tasks** that collectively achieve the goal.  
3. Within each task, define clear **steps** that represent concrete, actionable reasoning or production actions.  
4. Identify where failures may occur and define **backups** or alternative methods for those steps.  
5. Ensure each step and task is logically aligned with the North Star.

---

## Procedural Instructions

Follow these steps exactly and sequentially.

### Step 0. Project Profile Detection (DNA)

**Purpose:** Ensure project-level configuration exists before generating SPECs.

#### 0.1 Check for Existing DNA Profile

Scan for DNA folders in `Specs/` directory:
- Look for folders matching pattern: 8 characters from alphabet [A, T, G, C]
- Check for `project_constitution.toml` in each DNA folder
- If found: Load the project name from the TOML

**If DNA profile exists:**
```
✅ Found project profile: [PROJECT_NAME] (DNA: [DNA_CODE])
Loading project configuration...
Proceed to Step 1
```

**If NO DNA profile exists:**
```
⚠️ No project profile detected.

A project profile defines project-wide preferences:
- Domain and risk level
- Testing requirements
- Failure handling strategy
- Common constraints

This helps generate consistent SPECs across your project.

OPTIONS:
[A] Create project profile now (recommended, ~2 minutes)
[B] Skip - use system defaults only
[C] Use existing DNA code (if you have one)

Enter your choice (A/B/C):
```

#### 0.2 Handle User Choice

**If user selects [A] - Create Profile:**

Run the DNA profile interview from `__SPEC_Engine/_DNA/DNA_SPEC.md`:

```
Invoking DNA profile interview...

Please answer 5 brief questions to establish project parameters.
This only needs to be done once per project.
```

Execute DNA_SPEC.md interview process:
1. Ask the 5 questions
2. Generate DNA code from project name
3. Create `Specs/[DNA_CODE]/project_constitution.toml`
4. Display: "✅ Project profile created (DNA: [DNA_CODE])"
5. Proceed to Step 1

**If user selects [B] - Skip:**
```
Using system defaults only.
Note: You can create a project profile later by running DNA_SPEC.md
Proceeding with goal-specific SPEC generation...
```
Proceed to Step 1 (Commander will use system constitution only)

**If user selects [C] - Use Existing:**
```
Enter your 8-character DNA code: _______
```
- Validate code (8 chars, A/T/G/C only)
- Check if `Specs/[DNA_CODE]/project_constitution.toml` exists
- If exists: Load and proceed
- If not exists: Display error, return to options

#### 0.3 Load Project Configuration

Once DNA profile is confirmed (or skipped):
- If DNA exists: Load `project_constitution.toml` into context
- If skipped: Note that only system constitution will be used
- Display loaded configuration summary

**Proceed to Step 1**

---

### Step 1. Context

**IMPORTANT: Before beginning, read the Design Philosophy document:** `C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_Constitution\DESIGN_PHILOSOPHY.md`

This document contains:
- Core principles guiding Spec design
- Detailed rationale for architectural decisions
- Execution mode definitions and behaviours
- Backup method types (cognitive vs tool-based)
- Error propagation strategies
- Quality standards and anti-patterns to avoid

Reading this document ensures you understand the system's design intent and can generate Specs that align with established principles.

---

A) You are a **Spec-generating agent**.  

A spec is a set of files containing **explicit and scaffolded instructions** which are ingested by an LLM to evoke agentic behaviour.  

You can see the templates for a spec here (which you must replicate):
- `C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_templates\Spec_template.md`
- `C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_templates\parameters_template.toml`
- `C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_templates\exe_template.md`

B) You will be given a description of a **goal/behaviour** which must be carefully examined in the context of descriptor A) and used as the "North Star" guiding your development of the Spec documents.

---

### Step 2. File Generation
- Generate a **new folder** for the Spec, postpended with a one word '[descriptor]' that reflects the core goal/behaviour of the Spec. e.g., `[root]/Specs/[descriptor]/`  
- Create the following files inside this folder:
  - `spec_[descriptor].md` – human-readable specification
  - `parameters_[descriptor].toml` – machine-readable parameters
  - `exe_[descriptor].md` – execution controller  
- Postpend the descriptor to filenames: e.g., `spec_research.md`
- Initialize a placeholder file `progress.json` for logging execution and retry events.

Here is how the new folder and file system should look: 

/Specs/
   └── [descriptor]/
        ├── spec_[descriptor].md
        ├── parameters_[descriptor].toml
        ├── exe_[descriptor].md
        └── progress_[descriptor].json   # (created at runtime)
---

### Step 2.5. MCP Tool Analysis and Recommendation

**Purpose:** Examine goal requirements and recommend relevant MCP tools for human installation before detailed step generation.

#### Process

1. **Load MCP Tools Catalog**
   - Read `__SPEC_Engine/_tools/mcp_tools_catalog.yaml` completely
   - Available: 269 MCP servers, 2900+ tools, 24 categories
   - Understand catalog structure: categories, tool counts, popularity ratings

2. **Analyse Goal Characteristics**
   
   Consider these dimensions autonomously:
   - **Primary activity:** What is being done? (building, analysing, researching, processing, testing, etc.)
   - **Resource access:** What will be accessed? (files, databases, APIs, websites, documentation, etc.)
   - **Output creation:** What will be produced? (code, reports, data, documentation, visualisations, etc.)
   - **Scale/complexity:** How large? (simple script, full application, data pipeline, multi-component system)
   - **Technology mentions:** Are specific technologies referenced? (languages, frameworks, platforms, services)

3. **Identify Relevant Tool Categories**
   
   Review the 24 categories in catalog:
   - Consider which categories align with goal characteristics
   - Think holistically about full lifecycle needs (not just primary task)
   - Don't limit to obvious categories - consider cross-functional requirements
   - Examples: version control (github), documentation (notion), testing (playwright), monitoring (grafana)

4. **Evaluate Individual MCP Servers**
   
   For each potentially relevant server, autonomously assess:
   - **Relevance:** How directly does this support the goal?
   - **Capability:** Does it provide tools that would be actively used?
   - **Popularity:** ★ rating indicates maturity and reliability (but don't over-weight this)
   - **Tool count:** More tools = more versatile, but only if needed
   - **Alternatives:** Are there other ways to achieve the same outcome?

5. **Classify Tools into Tiers**
   
   Use autonomous reasoning to classify (no prescriptive rules):
   
   **REQUIRED:** Mark as required ONLY if:
   - Goal fundamentally cannot be achieved without this tool
   - No reasonable alternative exists within goal scope
   - Absence would block core functionality completely
   - Be conservative - most goals don't require many tools
   
   **RECOMMENDED:** Mark as recommended if:
   - Significantly improves efficiency or quality
   - Common practice for this type of goal
   - Reasonable alternatives exist but are substantially less efficient
   - Would require workarounds if absent
   
   **OPTIONAL:** Mark as optional if:
   - Nice to have for edge cases or future extensions
   - Relevant to potential workflow improvements
   - Enhances but not essential to core goal
   - Addresses convenience, not necessity

6. **Document Rationale**
   
   For each selected tool:
   - Explain WHY it's relevant to THIS specific goal
   - Reference specific goal requirements
   - For recommended/optional, note the alternative approach
   - Be clear about installation commands

7. **Quality Guidelines** (not rigid rules)
   
   - **Don't over-specify:** If goal can be achieved multiple ways, acknowledge alternatives
   - **Consider ecosystem:** Some tools overlap (github + gitlab redundant)
   - **Respect DNA profile:** Factor in project preferences if they exist
   - **Balance coverage:** Don't select 5 database tools for one database operation
   - **Think lifecycle:** Consider development, testing, deployment, monitoring phases
   
   **What NOT to do:**
   - ❌ Don't apply rigid mappings ("if X always use Y")
   - ❌ Don't recommend tools just because popular
   - ❌ Don't mark everything REQUIRED (be selective)
   - ❌ Don't ignore human review (they may have better context)
   - ❌ Don't recommend redundant tools doing same thing

#### Output Format

Present recommendations alongside high-level structure (see Step 3 output below).

---

### Step 3. Draft Requirements, Completion Criteria, and Tasks

**Purpose:** Create high-level structure for human review before detailed work.

##### PREPARE
Analyse the user's goal description:

  1. Define **one overarching Goal** (singular, clear, measurable)
  2. Identify **completion criteria** (what must exist and be verified)
  3. Decompose goal into **2–5 logical tasks** (objectives that advance the goal)
  4. For build/create goals: define software stack and deployment requirements

##### OUTPUT — Draft Proposal Document

Present to user:

```markdown
# SPEC Proposal for Review

## Goal
[Singular, clear goal statement]

## Definition of Complete
What must exist and be verified:
- [ ] Primary deliverable: [specific, measurable]
- [ ] Quality standards: [specific metrics]
- [ ] Verification method: [how to confirm]

[For build/create goals, include:]
### Software Stack
- Deployment type: [web_app|desktop_app|cli|etc.]
- Language/Framework: [specific]
- Target users: [who will use this]
- Deployment artifact: [what gets deployed]

## Tasks (High-Level)
1. **Task 1:** [Description - what objective this achieves]
2. **Task 2:** [Description]
3. **Task 3:** [Description]
[2-5 tasks total]

## Estimated Complexity
- Total steps: [estimate 1-5 per task]
- Critical steps: [estimate 40-60%]
- Build requirements: [if applicable: GUI, packaging, production API, etc.]
```

**Do NOT generate detailed steps yet.**

---

### Step 3a. MANDATORY HUMAN REVIEW

**CRITICAL: This step CANNOT be skipped. No silent mode allowed.**

Present the Draft Proposal to the user and request explicit approval:

```
==================================================
SPEC PROPOSAL REVIEW REQUIRED
==================================================

The following SPEC structure has been drafted based on your goal.
Please review and approve before detailed step generation begins.

[Show Draft Proposal from Step 3]

==================================================
REQUIRED ACTION:
==================================================

1. Review the Goal - Is it correct and singular?
2. Review Completion Criteria - Are these the right success measures?
3. Review Tasks - Do these collectively achieve the goal?
4. Review Software Stack - Is this the right technical approach? (if applicable)

OPTIONS:
[A] APPROVE - Proceed to generate detailed steps
[R] REVISE - Provide specific changes needed
[C] CLARIFY - Ask questions before deciding

Enter your choice (A/R/C):
```

**Pause execution and wait for user response.**

**If user selects:**
- **APPROVE (A):** Proceed to Step 4
- **REVISE (R):** Apply user's changes to Draft Proposal, present updated version, request approval again
- **CLARIFY (C):** Answer user's questions, then re-present proposal for approval

**Do NOT proceed until user explicitly approves with "A" or equivalent affirmative response.**

**Rationale:** This checkpoint prevents wasted effort on detailed steps if the high-level structure is wrong. Catching issues at the task level is far cheaper than catching them after full step generation.

---

### Step 4. Generate Detailed Steps and Files

**Prerequisites:** User has approved Draft Proposal from Step 3a

Now generate detailed implementation:

##### STEP GENERATION

For each approved task:
  1. Define **1–5 concrete steps** (specific actions, not abstract objectives)
  2. Identify failure points and define **0–2 backup methods** per step (alternative approaches, not retries)
  3. Mark **critical steps** (40-60% of total)
  4. Define **expected outputs** (specific, measurable)
  5. Assign **mode** (dynamic default, override if needed)
  6. **Determine if research_enabled needed** (see Research Inference below)

##### RESEARCH-ENABLED INFERENCE

For each task, determine if `research_enabled = true` should be set:

**Set to TRUE when task involves:**
- Words indicating knowledge-seeking: "research", "investigate", "explore", "discover", "find current", "identify latest"
- External systems requiring current docs: "API integration", "library usage", "framework setup"
- Rapidly evolving domains: "authentication best practices", "security standards", "modern patterns"
- Verification against external sources: "validate against spec", "check compliance", "confirm standards"
- Domain-specific expertise: Medical, legal, financial standards that LLM may not have current knowledge of

**Set to FALSE (default) when task involves:**
- Implementation using known patterns: "write function", "create class", "implement algorithm"
- Analysis/reasoning: "analyse code", "identify bugs", "optimise performance"
- File operations: "read file", "parse data", "generate report"
- Testing: "write tests", "run test suite", "verify functionality"

**Examples:**

Task: "Research current FastAPI authentication best practices"
→ `research_enabled = true`
→ `research_sources = ["web_search", "documentation"]`

Task: "Implement JWT token validation using researched approach"
→ `research_enabled = false` (implementation, not discovery)

Task: "Identify and integrate appropriate PDF parsing library"
→ `research_enabled = true` (discovery + current options)

##### FILE GENERATION
1. **spec_[descriptor].md**  
   - See template for guidance: 'C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_templates\Spec_template.md'
   - Follow the provided Spec Template structure.  
   - Include definitions for goal, tasks, steps, and backups.  
   - Ensure clarity and logical flow.  
   - Provide one illustrative example in the placeholder section.  

2. **parameters_[descriptor].toml**  
   - See template for guidance: 'C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_templates\parameters_template.toml'
   - Encode the same structure in TOML format.  
   - Maintain one-to-one correspondence between Markdown and TOML elements.  
   - Ensure task, step, and backup IDs match their counterparts.  

3. **exe_[descriptor].md**  
   - See template for guidance: 'C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_templates\exe_template.md'
   - Generate the execution controller for this Spec.  
   - Include logic for reading the spec, handling modes, retries, and error propagation.  
   - Ensure execution is sequential and logs are written to `progress.json`.

### Step 5. — Pre-Flight Validation

Before generating files, perform comprehensive validation:

#### 5.1 Constitutional Compliance Check
1. Read `constitution.md` from `__SPEC_Engine/_Constitution/` directory
2. Verify the goal description complies with Article I (singular, clear, measurable)
3. Confirm task count is within Article II limits (2-5 tasks)
4. Confirm step count per task is within Article II limits (1-5 steps)
5. Verify backup count per step is within Article II limits (0-2 backups)
6. Check that 40-60% of steps are marked critical (Article VI)
7. Ensure all expected outputs are specific and measurable (Article V)
8. Confirm no anti-patterns are present (Article XII)

#### 5.1a Software Stack Validation (MANDATORY for Build/Create Goals)

**Trigger:** If goal contains keywords: "build", "create", "develop", "system", "application", "app"

**Required Actions:**

1. **Verify Software Stack & Architecture section defined in spec_[descriptor].md:**
   - [ ] Deployment Type selected (web_app, desktop_app, cli, mobile, api, library)
   - [ ] Technology Stack specified (language, framework, database, UI library, packaging)
   - [ ] User Interface Requirements defined (if user-facing)
   - [ ] Deployment Requirements specified (target platform, installation method, startup process)

2. **Verify Definition of Complete section exists in spec_[descriptor].md:**
   - [ ] Functional Completeness checklist present
   - [ ] Deployment Completeness checklist present
   - [ ] User Acceptance criteria defined (if user-facing)
   - [ ] Production Readiness criteria specified (if applicable)

3. **Verify [software_stack] section populated in parameters_[descriptor].toml:**
   - [ ] `deployment_type` not empty
   - [ ] `primary_language` not empty
   - [ ] `framework` defined (or "none" if not applicable)
   - [ ] `packaging_method` defined

4. **Verify [user_interface] section defined in parameters_[descriptor].toml:**
   - [ ] `required` field set appropriately
   - [ ] If `required = true`: `interface_type`, `target_users`, `skill_level` all defined

5. **Verify [deployment] section defined in parameters_[descriptor].toml:**
   - [ ] `target_platform` defined
   - [ ] `installation_type` defined
   - [ ] `startup_method` defined
   - [ ] `configuration_required` list present (even if empty)

6. **Verify [completion_criteria] section exists in parameters_[descriptor].toml:**
   - [ ] All boolean fields present (functional_complete, interface_complete, deployment_complete, production_ready, user_tested, documentation_complete)
   - [ ] `acceptance_criteria` list populated with specific, testable criteria

**If goal contains "for [users]" (e.g., "for volunteers", "for doctors"):**
- MUST have `user_interface.required = true`
- MUST have User Acceptance section in Definition of Complete
- MUST include user stories in spec_[descriptor].md

**Quality Gates:**
```
✅ **PASS**: Software stack fully defined
   - deployment_type = "desktop_app"
   - primary_language = "python"
   - framework = "pyqt5"
   - ui_required = true
   - completion_criteria = 6 defined

❌ **FAIL**: Software stack missing or incomplete
   - deployment_type = "" (empty)
   - ui_library undefined
   - completion_criteria section missing
   - HALT: Cannot generate spec without knowing what to build
```

**If validation fails:**
- DO NOT proceed to file generation
- Log specific missing fields
- Request clarification: "Goal requires building a system but software stack undefined. Please specify: deployment type, target users, technology stack, and completion criteria."

#### 5.2 Structural Validation
1. Ensure goal is singular and non-ambiguous
2. Verify tasks logically decompose the goal
3. Check steps are concrete actions (not abstract objectives)
4. Validate backups are alternative methods (not simple retries)
5. Confirm backup descriptions explain the alternative approach

#### 5.3 Pre-Generation Quality Gates
Generate a validation report showing:
- ✅ **PASS**: Goal is singular and clear
- ✅ **PASS**: 3 tasks defined (within 2-5 range)
- ✅ **PASS**: Step counts are [3, 4, 5] (within 1-5 range)
- ✅ **PASS**: 7 of 12 steps marked critical (58%, within 40-60%)
- ✅ **PASS**: All expected outputs are specific
- ⚠️ **WARN**: Task 2 Step 3 has no backup (non-critical, acceptable)

If any **FAIL** conditions detected:
1. Log validation failures
2. Request clarification or correction
3. Do NOT proceed to file generation until resolved

#### 5.4 Alignment Check
- Tasks and Steps must be **synchronized** across the spec and parameters files
- Verify all content across the three files refers to the **same goal** and **identical task/step IDs**
- Ensure all steps logically contribute to the goal
- Confirm backups align with their parent steps
- Verification mechanisms must be in place to confirm consistency before execution
- Ensure JSON logging (`progress.json`) is referenced for tracking retries, critical failures, and mode switches

---

### Step 6. Output Check
At the end of generation, present:

/Specs/
   └── [descriptor]/
        ├── spec_[descriptor].md
        ├── parameters_[descriptor].toml
        ├── exe_[descriptor].md
        └── progress_[descriptor].json   # (created at runtime)

        
## Quality Standards

- Maintain **internal consistency** across all files.  
- Avoid repetition — reuse terms and IDs precisely.  
- Each step, backup, and constraint must **serve the goal**.  
- All file contents must be syntactically valid and human-readable.  
- Be explicit — avoid placeholder ambiguity except where instructed.  

---

## Reminder
All generated output must:
- Follow the provided templates exactly.  
- Remain tightly focused on achieving the North Star goal.  
- Be internally cohesive and execution-ready.

---

**End of Commander Spec**
```

```markdown
# commander-spec.md

---
## LLM Context & Role

You are a **Spec Generating Agent**.  

A **Spec** is a structured set of files designed to evoke goal-driven, agentic behaviour in LLMs.  

Your role is to **analyze a given goal or desired behaviour** and translate it into a complete, coherent Spec composed of the following files:

1. **spec_[descriptor].md** — A structured human-readable specification describing:
   - The goal, tasks, and steps required to achieve it.  
   - Constraints, components, and reasoning scaffolds.  
   - Definitions of key terms and their relationships (goal → task → step → backup).    

2. **exe_[descriptor].md** — The execution controller.  
   - This file instructs an LLM on how to interpret and act upon `spec.md` and `parameters.toml`.  
   - It defines logic for handling retries, modes, backups, and logging behaviour.

3. **parameters_[descriptor].toml** — A machine-readable version of the same spec, encoding the same goal, tasks, and steps in a format that enforces clear delineation and reduces ambiguity.

Together, these files form a **Spec**, a folder which functions as a self-contained unit of instruction that can be executed by an LLM in “agentic” mode.

---

## [META]
- **File Role:** Master coordinator for generating Spec documents.  
- **Purpose:** Guides the LLM to create a full set of structured files (known as a 'Spec') for executing a single goal.  
- **Descriptor Example:** research, debug, prototype, test, etc.  
- **Creation Folder:** `[root]/Specs/[descriptor]/`  

---

## Guidance for Goal Interpretation

You will be provided with a description of a **goal or behaviour** to model.  

This goal is your **North Star**.

Everything you generate — tasks, steps, backups, constraints — must directly support achieving this goal.

Before writing, you must:
1. Understand the intent and scope of the goal.  
2. Decompose it into logical, sequential **tasks** that collectively achieve the goal.  
3. Within each task, define clear **steps** that represent concrete, actionable reasoning or production actions.  
4. Identify where failures may occur and define **backups** or alternative methods for those steps.  
5. Ensure each step and task is logically aligned with the North Star.

---

## Procedural Instructions

Follow these steps exactly and sequentially.

### Step 0. Project Profile Detection (DNA)

**Purpose:** Ensure project-level configuration exists before generating SPECs.

#### 0.1 Check for Existing DNA Profile

Scan for DNA folders in `Specs/` directory:
- Look for folders matching pattern: 8 characters from alphabet [A, T, G, C]
- Check for `project_constitution.toml` in each DNA folder
- If found: Load the project name from the TOML

**If DNA profile exists:**
```
✅ Found project profile: [PROJECT_NAME] (DNA: [DNA_CODE])
Loading project configuration...
Proceed to Step 1
```

**If NO DNA profile exists:**
```
⚠️ No project profile detected.

A project profile defines project-wide preferences:
- Domain and risk level
- Testing requirements
- Failure handling strategy
- Common constraints

This helps generate consistent SPECs across your project.

OPTIONS:
[A] Create project profile now (recommended, ~2 minutes)
[B] Skip - use system defaults only
[C] Use existing DNA code (if you have one)

Enter your choice (A/B/C):
```

#### 0.2 Handle User Choice

**If user selects [A] - Create Profile:**

Run the DNA profile interview from `__SPEC_Engine/_DNA/DNA_SPEC.md`:

```
Invoking DNA profile interview...

Please answer 5 brief questions to establish project parameters.
This only needs to be done once per project.
```

Execute DNA_SPEC.md interview process:
1. Ask the 5 questions
2. Generate DNA code from project name
3. Create `Specs/[DNA_CODE]/project_constitution.toml`
4. Display: "✅ Project profile created (DNA: [DNA_CODE])"
5. Proceed to Step 1

**If user selects [B] - Skip:**
```
Using system defaults only.
Note: You can create a project profile later by running DNA_SPEC.md
Proceeding with goal-specific SPEC generation...
```
Proceed to Step 1 (Commander will use system constitution only)

**If user selects [C] - Use Existing:**
```
Enter your 8-character DNA code: _______
```
- Validate code (8 chars, A/T/G/C only)
- Check if `Specs/[DNA_CODE]/project_constitution.toml` exists
- If exists: Load and proceed
- If not exists: Display error, return to options

#### 0.3 Load Project Configuration

Once DNA profile is confirmed (or skipped):
- If DNA exists: Load `project_constitution.toml` into context
- If skipped: Note that only system constitution will be used
- Display loaded configuration summary

**Proceed to Step 1**

---

### Step 1. Context

**IMPORTANT: Before beginning, read the Design Philosophy document:** `C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_Constitution\DESIGN_PHILOSOPHY.md`

This document contains:
- Core principles guiding Spec design
- Detailed rationale for architectural decisions
- Execution mode definitions and behaviours
- Backup method types (cognitive vs tool-based)
- Error propagation strategies
- Quality standards and anti-patterns to avoid

Reading this document ensures you understand the system's design intent and can generate Specs that align with established principles.

---

A) You are a **Spec-generating agent**.  

A spec is a set of files containing **explicit and scaffolded instructions** which are ingested by an LLM to evoke agentic behaviour.  

You can see the templates for a spec here (which you must replicate):
- `C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_templates\Spec_template.md`
- `C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_templates\parameters_template.toml`
- `C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_templates\exe_template.md`

B) You will be given a description of a **goal/behaviour** which must be carefully examined in the context of descriptor A) and used as the "North Star" guiding your development of the Spec documents.

---

### Step 2. File Generation
- Generate a **new folder** for the Spec, postpended with a one word '[descriptor]' that reflects the core goal/behaviour of the Spec. e.g., `[root]/Specs/[descriptor]/`  
- Create the following files inside this folder:
  - `spec_[descriptor].md` – human-readable specification
  - `parameters_[descriptor].toml` – machine-readable parameters
  - `exe_[descriptor].md` – execution controller  
- Postpend the descriptor to filenames: e.g., `spec_research.md`
- Initialize a placeholder file `progress.json` for logging execution and retry events.

Here is how the new folder and file system should look: 

/Specs/
   └── [descriptor]/
        ├── spec_[descriptor].md
        ├── parameters_[descriptor].toml
        ├── exe_[descriptor].md
        └── progress_[descriptor].json   # (created at runtime)
---

### Step 2.5. MCP Tool Analysis and Recommendation

**Purpose:** Examine goal requirements and recommend relevant MCP tools for human installation before detailed step generation.

#### Process

1. **Load MCP Tools Catalog**
   - Read `__SPEC_Engine/_tools/mcp_tools_catalog.yaml` completely
   - Available: 269 MCP servers, 2900+ tools, 24 categories
   - Understand catalog structure: categories, tool counts, popularity ratings

2. **Analyse Goal Characteristics**
   
   Consider these dimensions autonomously:
   - **Primary activity:** What is being done? (building, analysing, researching, processing, testing, etc.)
   - **Resource access:** What will be accessed? (files, databases, APIs, websites, documentation, etc.)
   - **Output creation:** What will be produced? (code, reports, data, documentation, visualisations, etc.)
   - **Scale/complexity:** How large? (simple script, full application, data pipeline, multi-component system)
   - **Technology mentions:** Are specific technologies referenced? (languages, frameworks, platforms, services)

3. **Identify Relevant Tool Categories**
   
   Review the 24 categories in catalog:
   - Consider which categories align with goal characteristics
   - Think holistically about full lifecycle needs (not just primary task)
   - Don't limit to obvious categories - consider cross-functional requirements
   - Examples: version control (github), documentation (notion), testing (playwright), monitoring (grafana)

4. **Evaluate Individual MCP Servers**
   
   For each potentially relevant server, autonomously assess:
   - **Relevance:** How directly does this support the goal?
   - **Capability:** Does it provide tools that would be actively used?
   - **Popularity:** ★ rating indicates maturity and reliability (but don't over-weight this)
   - **Tool count:** More tools = more versatile, but only if needed
   - **Alternatives:** Are there other ways to achieve the same outcome?

5. **Classify Tools into Tiers**
   
   Use autonomous reasoning to classify (no prescriptive rules):
   
   **REQUIRED:** Mark as required ONLY if:
   - Goal fundamentally cannot be achieved without this tool
   - No reasonable alternative exists within goal scope
   - Absence would block core functionality completely
   - Be conservative - most goals don't require many tools
   
   **RECOMMENDED:** Mark as recommended if:
   - Significantly improves efficiency or quality
   - Common practice for this type of goal
   - Reasonable alternatives exist but are substantially less efficient
   - Would require workarounds if absent
   
   **OPTIONAL:** Mark as optional if:
   - Nice to have for edge cases or future extensions
   - Relevant to potential workflow improvements
   - Enhances but not essential to core goal
   - Addresses convenience, not necessity

6. **Document Rationale**
   
   For each selected tool:
   - Explain WHY it's relevant to THIS specific goal
   - Reference specific goal requirements
   - For recommended/optional, note the alternative approach
   - Be clear about installation commands

7. **Quality Guidelines** (not rigid rules)
   
   - **Don't over-specify:** If goal can be achieved multiple ways, acknowledge alternatives
   - **Consider ecosystem:** Some tools overlap (github + gitlab redundant)
   - **Respect DNA profile:** Factor in project preferences if they exist
   - **Balance coverage:** Don't select 5 database tools for one database operation
   - **Think lifecycle:** Consider development, testing, deployment, monitoring phases
   
   **What NOT to do:**
   - ❌ Don't apply rigid mappings ("if X always use Y")
   - ❌ Don't recommend tools just because popular
   - ❌ Don't mark everything REQUIRED (be selective)
   - ❌ Don't ignore human review (they may have better context)
   - ❌ Don't recommend redundant tools doing same thing

#### Output Format

Present recommendations alongside high-level structure (see Step 3 output below).

---

### Step 3. Draft Requirements, Completion Criteria, and Tasks

**Purpose:** Create high-level structure for human review before detailed work.

##### PREPARE
Analyse the user's goal description:

  1. Define **one overarching Goal** (singular, clear, measurable)
  2. Identify **completion criteria** (what must exist and be verified)
  3. Decompose goal into **2–5 logical tasks** (objectives that advance the goal)
  4. For build/create goals: define software stack and deployment requirements

##### OUTPUT — Draft Proposal Document

Present to user:

```markdown
# SPEC Proposal for Review

## Goal
[Singular, clear goal statement]

## Definition of Complete
What must exist and be verified:
- [ ] Primary deliverable: [specific, measurable]
- [ ] Quality standards: [specific metrics]
- [ ] Verification method: [how to confirm]

[For build/create goals, include:]
### Software Stack
- Deployment type: [web_app|desktop_app|cli|etc.]
- Language/Framework: [specific]
- Target users: [who will use this]
- Deployment artifact: [what gets deployed]

## Recommended MCP Toolset

### REQUIRED Tools ([n] tools)
[For each required tool:]
- **[tool_name]** (★★★★★ | [n] tools | [category])
  - Rationale: [Why essential for THIS goal]
  - Provides: [Key capabilities needed]
  - Install: `[installation command from catalog]`

### RECOMMENDED Tools ([n] tools)
[For each recommended tool:]
- **[tool_name]** (★★★☆☆ | [n] tools | [category])
  - Rationale: [Why beneficial for THIS goal]
  - Alternative: [What would be done without it]
  - Install: `[installation command from catalog]`

### OPTIONAL Tools ([n] tools)
[For each optional tool:]
- **[tool_name]** (★★☆☆☆ | [n] tools | [category])
  - Use case: [When/why this might be helpful]
  - Install: `[installation command from catalog]`

## Tasks (High-Level)
1. **Task 1:** [Description - what objective this achieves]
2. **Task 2:** [Description]
3. **Task 3:** [Description]
[2-5 tasks total]

## Estimated Complexity
- Total steps: [estimate 1-5 per task]
- Critical steps: [estimate 40-60%]
- Build requirements: [if applicable: GUI, packaging, production API, etc.]
```

**Do NOT generate detailed steps yet.**

---

### Step 3a. MANDATORY HUMAN REVIEW

**CRITICAL: This step CANNOT be skipped. No silent mode allowed.**

Present the Draft Proposal to the user and request explicit approval:

```
==================================================
SPEC PROPOSAL REVIEW REQUIRED
==================================================

The following SPEC structure has been drafted based on your goal.
Please review and approve before detailed step generation begins.

[Show Draft Proposal from Step 3]

==================================================
REQUIRED ACTION:
==================================================

1. Review the Goal - Is it correct and singular?
2. Review Completion Criteria - Are these the right success measures?
3. Review Tasks - Do these collectively achieve the goal?
4. Review Software Stack - Is this the right technical approach? (if applicable)

OPTIONS:
[A] APPROVE - Proceed to generate detailed steps
[R] REVISE - Provide specific changes needed
[C] CLARIFY - Ask questions before deciding

Enter your choice (A/R/C):
```

**Pause execution and wait for user response.**

**If user selects:**
- **APPROVE (A):** Proceed to Step 4
- **REVISE (R):** Apply user's changes to Draft Proposal, present updated version, request approval again
- **CLARIFY (C):** Answer user's questions, then re-present proposal for approval

**Do NOT proceed until user explicitly approves with "A" or equivalent affirmative response.**

**Rationale:** This checkpoint prevents wasted effort on detailed steps if the high-level structure is wrong. Catching issues at the task level is far cheaper than catching them after full step generation.

---

### Step 4. Generate Detailed Steps and Files

**Prerequisites:** User has approved Draft Proposal from Step 3a

Now generate detailed implementation:

##### STEP GENERATION

For each approved task:
  1. Define **1–5 concrete steps** (specific actions, not abstract objectives)
  2. Identify failure points and define **0–2 backup methods** per step (alternative approaches, not retries)
  3. Mark **critical steps** (40-60% of total)
  4. Define **expected outputs** (specific, measurable)
  5. Assign **mode** (dynamic default, override if needed)
  6. **Determine if research_enabled needed** (see Research Inference below)

##### RESEARCH-ENABLED INFERENCE

For each task, determine if `research_enabled = true` should be set:

**Set to TRUE when task involves:**
- Words indicating knowledge-seeking: "research", "investigate", "explore", "discover", "find current", "identify latest"
- External systems requiring current docs: "API integration", "library usage", "framework setup"
- Rapidly evolving domains: "authentication best practices", "security standards", "modern patterns"
- Verification against external sources: "validate against spec", "check compliance", "confirm standards"
- Domain-specific expertise: Medical, legal, financial standards that LLM may not have current knowledge of

**Set to FALSE (default) when task involves:**
- Implementation using known patterns: "write function", "create class", "implement algorithm"
- Analysis/reasoning: "analyse code", "identify bugs", "optimise performance"
- File operations: "read file", "parse data", "generate report"
- Testing: "write tests", "run test suite", "verify functionality"

**Examples:**

Task: "Research current FastAPI authentication best practices"
→ `research_enabled = true`
→ `research_sources = ["web_search", "documentation"]`

Task: "Implement JWT token validation using researched approach"
→ `research_enabled = false` (implementation, not discovery)

Task: "Identify and integrate appropriate PDF parsing library"
→ `research_enabled = true` (discovery + current options)

##### FILE GENERATION
1. **spec_[descriptor].md**  
   - See template for guidance: 'C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_templates\Spec_template.md'
   - Follow the provided Spec Template structure.  
   - Include definitions for goal, tasks, steps, and backups.  
   - Ensure clarity and logical flow.  
   - Provide one illustrative example in the placeholder section.  

2. **parameters_[descriptor].toml**  
   - See template for guidance: 'C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_templates\parameters_template.toml'
   - Encode the same structure in TOML format.  
   - Maintain one-to-one correspondence between Markdown and TOML elements.  
   - Ensure task, step, and backup IDs match their counterparts.  

3. **exe_[descriptor].md**  
   - See template for guidance: 'C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_templates\exe_template.md'
   - Generate the execution controller for this Spec.  
   - Include logic for reading the spec, handling modes, retries, and error propagation.  
   - Ensure execution is sequential and logs are written to `progress.json`.

### Step 5. — Pre-Flight Validation

Before generating files, perform comprehensive validation:

#### 5.1 Constitutional Compliance Check
1. Read `constitution.md` from `__SPEC_Engine/_Constitution/` directory
2. Verify the goal description complies with Article I (singular, clear, measurable)
3. Confirm task count is within Article II limits (2-5 tasks)
4. Confirm step count per task is within Article II limits (1-5 steps)
5. Verify backup count per step is within Article II limits (0-2 backups)
6. Check that 40-60% of steps are marked critical (Article VI)
7. Ensure all expected outputs are specific and measurable (Article V)
8. Confirm no anti-patterns are present (Article XII)

#### 5.1a Software Stack Validation (MANDATORY for Build/Create Goals)

**Trigger:** If goal contains keywords: "build", "create", "develop", "system", "application", "app"

**Required Actions:**

1. **Verify Software Stack & Architecture section defined in spec_[descriptor].md:**
   - [ ] Deployment Type selected (web_app, desktop_app, cli, mobile, api, library)
   - [ ] Technology Stack specified (language, framework, database, UI library, packaging)
   - [ ] User Interface Requirements defined (if user-facing)
   - [ ] Deployment Requirements specified (target platform, installation method, startup process)

2. **Verify Definition of Complete section exists in spec_[descriptor].md:**
   - [ ] Functional Completeness checklist present
   - [ ] Deployment Completeness checklist present
   - [ ] User Acceptance criteria defined (if user-facing)
   - [ ] Production Readiness criteria specified (if applicable)

3. **Verify [software_stack] section populated in parameters_[descriptor].toml:**
   - [ ] `deployment_type` not empty
   - [ ] `primary_language` not empty
   - [ ] `framework` defined (or "none" if not applicable)
   - [ ] `packaging_method` defined

4. **Verify [user_interface] section defined in parameters_[descriptor].toml:**
   - [ ] `required` field set appropriately
   - [ ] If `required = true`: `interface_type`, `target_users`, `skill_level` all defined

5. **Verify [deployment] section defined in parameters_[descriptor].toml:**
   - [ ] `target_platform` defined
   - [ ] `installation_type` defined
   - [ ] `startup_method` defined
   - [ ] `configuration_required` list present (even if empty)

6. **Verify [completion_criteria] section exists in parameters_[descriptor].toml:**
   - [ ] All boolean fields present (functional_complete, interface_complete, deployment_complete, production_ready, user_tested, documentation_complete)
   - [ ] `acceptance_criteria` list populated with specific, testable criteria

**If goal contains "for [users]" (e.g., "for volunteers", "for doctors"):**
- MUST have `user_interface.required = true`
- MUST have User Acceptance section in Definition of Complete
- MUST include user stories in spec_[descriptor].md

**Quality Gates:**
```
✅ **PASS**: Software stack fully defined
   - deployment_type = "desktop_app"
   - primary_language = "python"
   - framework = "pyqt5"
   - ui_required = true
   - completion_criteria = 6 defined

❌ **FAIL**: Software stack missing or incomplete
   - deployment_type = "" (empty)
   - ui_library undefined
   - completion_criteria section missing
   - HALT: Cannot generate spec without knowing what to build
```

**If validation fails:**
- DO NOT proceed to file generation
- Log specific missing fields
- Request clarification: "Goal requires building a system but software stack undefined. Please specify: deployment type, target users, technology stack, and completion criteria."

#### 5.2 Structural Validation
1. Ensure goal is singular and non-ambiguous
2. Verify tasks logically decompose the goal
3. Check steps are concrete actions (not abstract objectives)
4. Validate backups are alternative methods (not simple retries)
5. Confirm backup descriptions explain the alternative approach

#### 5.3 Pre-Generation Quality Gates
Generate a validation report showing:
- ✅ **PASS**: Goal is singular and clear
- ✅ **PASS**: 3 tasks defined (within 2-5 range)
- ✅ **PASS**: Step counts are [3, 4, 5] (within 1-5 range)
- ✅ **PASS**: 7 of 12 steps marked critical (58%, within 40-60%)
- ✅ **PASS**: All expected outputs are specific
- ⚠️ **WARN**: Task 2 Step 3 has no backup (non-critical, acceptable)

If any **FAIL** conditions detected:
1. Log validation failures
2. Request clarification or correction
3. Do NOT proceed to file generation until resolved

#### 5.4 Alignment Check
- Tasks and Steps must be **synchronized** across the spec and parameters files
- Verify all content across the three files refers to the **same goal** and **identical task/step IDs**
- Ensure all steps logically contribute to the goal
- Confirm backups align with their parent steps
- Verification mechanisms must be in place to confirm consistency before execution
- Ensure JSON logging (`progress.json`) is referenced for tracking retries, critical failures, and mode switches

---

### Step 6. Output Check
At the end of generation, present:

/Specs/
   └── [descriptor]/
        ├── spec_[descriptor].md
        ├── parameters_[descriptor].toml
        ├── exe_[descriptor].md
        └── progress_[descriptor].json   # (created at runtime)

        
## Quality Standards

- Maintain **internal consistency** across all files.  
- Avoid repetition — reuse terms and IDs precisely.  
- Each step, backup, and constraint must **serve the goal**.  
- All file contents must be syntactically valid and human-readable.  
- Be explicit — avoid placeholder ambiguity except where instructed.  

---

## Reminder
All generated output must:
- Follow the provided templates exactly.  
- Remain tightly focused on achieving the North Star goal.  
- Be internally cohesive and execution-ready.

---

**End of Commander Spec**
```

```markdown
# commander-spec.md

---
## LLM Context & Role

You are a **Spec Generating Agent**.  

A **Spec** is a structured set of files designed to evoke goal-driven, agentic behaviour in LLMs.  

Your role is to **analyze a given goal or desired behaviour** and translate it into a complete, coherent Spec composed of the following files:

1. **spec_[descriptor].md** — A structured human-readable specification describing:
   - The goal, tasks, and steps required to achieve it.  
   - Constraints, components, and reasoning scaffolds.  
   - Definitions of key terms and their relationships (goal → task → step → backup).    

2. **exe_[descriptor].md** — The execution controller.  
   - This file instructs an LLM on how to interpret and act upon `spec.md` and `parameters.toml`.  
   - It defines logic for handling retries, modes, backups, and logging behaviour.

3. **parameters_[descriptor].toml** — A machine-readable version of the same spec, encoding the same goal, tasks, and steps in a format that enforces clear delineation and reduces ambiguity.

Together, these files form a **Spec**, a folder which functions as a self-contained unit of instruction that can be executed by an LLM in “agentic” mode.

---

## [META]
- **File Role:** Master coordinator for generating Spec documents.  
- **Purpose:** Guides the LLM to create a full set of structured files (known as a 'Spec') for executing a single goal.  
- **Descriptor Example:** research, debug, prototype, test, etc.  
- **Creation Folder:** `[root]/Specs/[descriptor]/`  

---

## Guidance for Goal Interpretation

You will be provided with a description of a **goal or behaviour** to model.  

This goal is your **North Star**.

Everything you generate — tasks, steps, backups, constraints — must directly support achieving this goal.

Before writing, you must:
1. Understand the intent and scope of the goal.  
2. Decompose it into logical, sequential **tasks** that collectively achieve the goal.  
3. Within each task, define clear **steps** that represent concrete, actionable reasoning or production actions.  
4. Identify where failures may occur and define **backups** or alternative methods for those steps.  
5. Ensure each step and task is logically aligned with the North Star.

---

## Procedural Instructions

Follow these steps exactly and sequentially.

### Step 0. Project Profile Detection (DNA)

**Purpose:** Ensure project-level configuration exists before generating SPECs.

#### 0.1 Check for Existing DNA Profile

Scan for DNA folders in `Specs/` directory:
- Look for folders matching pattern: 8 characters from alphabet [A, T, G, C]
- Check for `project_constitution.toml` in each DNA folder
- If found: Load the project name from the TOML

**If DNA profile exists:**
```
✅ Found project profile: [PROJECT_NAME] (DNA: [DNA_CODE])
Loading project configuration...
Proceed to Step 1
```

**If NO DNA profile exists:**
```
⚠️ No project profile detected.

A project profile defines project-wide preferences:
- Domain and risk level
- Testing requirements
- Failure handling strategy
- Common constraints

This helps generate consistent SPECs across your project.

OPTIONS:
[A] Create project profile now (recommended, ~2 minutes)
[B] Skip - use system defaults only
[C] Use existing DNA code (if you have one)

Enter your choice (A/B/C):
```

#### 0.2 Handle User Choice

**If user selects [A] - Create Profile:**

Run the DNA profile interview from `__SPEC_Engine/_DNA/DNA_SPEC.md`:

```
Invoking DNA profile interview...

Please answer 5 brief questions to establish project parameters.
This only needs to be done once per project.
```

Execute DNA_SPEC.md interview process:
1. Ask the 5 questions
2. Generate DNA code from project name
3. Create `Specs/[DNA_CODE]/project_constitution.toml`
4. Display: "✅ Project profile created (DNA: [DNA_CODE])"
5. Proceed to Step 1

**If user selects [B] - Skip:**
```
Using system defaults only.
Note: You can create a project profile later by running DNA_SPEC.md
Proceeding with goal-specific SPEC generation...
```
Proceed to Step 1 (Commander will use system constitution only)

**If user selects [C] - Use Existing:**
```
Enter your 8-character DNA code: _______
```
- Validate code (8 chars, A/T/G/C only)
- Check if `Specs/[DNA_CODE]/project_constitution.toml` exists
- If exists: Load and proceed
- If not exists: Display error, return to options

#### 0.3 Load Project Configuration

Once DNA profile is confirmed (or skipped):
- If DNA exists: Load `project_constitution.toml` into context
- If skipped: Note that only system constitution will be used
- Display loaded configuration summary

**Proceed to Step 1**

---

### Step 1. Context

**IMPORTANT: Before beginning, read the Design Philosophy document:** `C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_Constitution\DESIGN_PHILOSOPHY.md`

This document contains:
- Core principles guiding Spec design
- Detailed rationale for architectural decisions
- Execution mode definitions and behaviours
- Backup method types (cognitive vs tool-based)
- Error propagation strategies
- Quality standards and anti-patterns to avoid

Reading this document ensures you understand the system's design intent and can generate Specs that align with established principles.

---

A) You are a **Spec-generating agent**.  

A spec is a set of files containing **explicit and scaffolded instructions** which are ingested by an LLM to evoke agentic behaviour.  

You can see the templates for a spec here (which you must replicate):
- `C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_templates\Spec_template.md`
- `C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_templates\parameters_template.toml`
- `C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_templates\exe_template.md`

B) You will be given a description of a **goal/behaviour** which must be carefully examined in the context of descriptor A) and used as the "North Star" guiding your development of the Spec documents.

---

### Step 2. File Generation
- Generate a **new folder** for the Spec, postpended with a one word '[descriptor]' that reflects the core goal/behaviour of the Spec. e.g., `[root]/Specs/[descriptor]/`  
- Create the following files inside this folder:
  - `spec_[descriptor].md` – human-readable specification
  - `parameters_[descriptor].toml` – machine-readable parameters
  - `exe_[descriptor].md` – execution controller  
- Postpend the descriptor to filenames: e.g., `spec_research.md`
- Initialize a placeholder file `progress.json` for logging execution and retry events.

Here is how the new folder and file system should look: 

/Specs/
   └── [descriptor]/
        ├── spec_[descriptor].md
        ├── parameters_[descriptor].toml
        ├── exe_[descriptor].md
        └── progress_[descriptor].json   # (created at runtime)
---

### Step 2.5. MCP Tool Analysis and Recommendation

**Purpose:** Examine goal requirements and recommend relevant MCP tools for human installation before detailed step generation.

#### Process

1. **Load MCP Tools Catalog**
   - Read `__SPEC_Engine/_tools/mcp_tools_catalog.yaml` completely
   - Available: 269 MCP servers, 2900+ tools, 24 categories
   - Understand catalog structure: categories, tool counts, popularity ratings

2. **Analyse Goal Characteristics**
   
   Consider these dimensions autonomously:
   - **Primary activity:** What is being done? (building, analysing, researching, processing, testing, etc.)
   - **Resource access:** What will be accessed? (files, databases, APIs, websites, documentation, etc.)
   - **Output creation:** What will be produced? (code, reports, data, documentation, visualisations, etc.)
   - **Scale/complexity:** How large? (simple script, full application, data pipeline, multi-component system)
   - **Technology mentions:** Are specific technologies referenced? (languages, frameworks, platforms, services)

3. **Identify Relevant Tool Categories**
   
   Review the 24 categories in catalog:
   - Consider which categories align with goal characteristics
   - Think holistically about full lifecycle needs (not just primary task)
   - Don't limit to obvious categories - consider cross-functional requirements
   - Examples: version control (github), documentation (notion), testing (playwright), monitoring (grafana)

4. **Evaluate Individual MCP Servers**
   
   For each potentially relevant server, autonomously assess:
   - **Relevance:** How directly does this support the goal?
   - **Capability:** Does it provide tools that would be actively used?
   - **Popularity:** ★ rating indicates maturity and reliability (but don't over-weight this)
   - **Tool count:** More tools = more versatile, but only if needed
   - **Alternatives:** Are there other ways to achieve the same outcome?

5. **Classify Tools into Tiers**
   
   Use autonomous reasoning to classify (no prescriptive rules):
   
   **REQUIRED:** Mark as required ONLY if:
   - Goal fundamentally cannot be achieved without this tool
   - No reasonable alternative exists within goal scope
   - Absence would block core functionality completely
   - Be conservative - most goals don't require many tools
   
   **RECOMMENDED:** Mark as recommended if:
   - Significantly improves efficiency or quality
   - Common practice for this type of goal
   - Reasonable alternatives exist but are substantially less efficient
   - Would require workarounds if absent
   
   **OPTIONAL:** Mark as optional if:
   - Nice to have for edge cases or future extensions
   - Relevant to potential workflow improvements
   - Enhances but not essential to core goal
   - Addresses convenience, not necessity

6. **Document Rationale**
   
   For each selected tool:
   - Explain WHY it's relevant to THIS specific goal
   - Reference specific goal requirements
   - For recommended/optional, note the alternative approach
   - Be clear about installation commands

7. **Quality Guidelines** (not rigid rules)
   
   - **Don't over-specify:** If goal can be achieved multiple ways, acknowledge alternatives
   - **Consider ecosystem:** Some tools overlap (github + gitlab redundant)
   - **Respect DNA profile:** Factor in project preferences if they exist
   - **Balance coverage:** Don't select 5 database tools for one database operation
   - **Think lifecycle:** Consider development, testing, deployment, monitoring phases
   
   **What NOT to do:**
   - ❌ Don't apply rigid mappings ("if X always use Y")
   - ❌ Don't recommend tools just because popular
   - ❌ Don't mark everything REQUIRED (be selective)
   - ❌ Don't ignore human review (they may have better context)
   - ❌ Don't recommend redundant tools doing same thing

#### Output Format

Present recommendations alongside high-level structure (see Step 3 output below).

---

### Step 3. Draft Requirements, Completion Criteria, and Tasks

**Purpose:** Create high-level structure for human review before detailed work.

##### PREPARE
Analyse the user's goal description:

  1. Define **one overarching Goal** (singular, clear, measurable)
  2. Identify **completion criteria** (what must exist and be verified)
  3. Decompose goal into **2–5 logical tasks** (objectives that advance the goal)
  4. For build/create goals: define software stack and deployment requirements

##### OUTPUT — Draft Proposal Document

Present to user:

```markdown
# SPEC Proposal for Review

## Goal
[Singular, clear goal statement]

## Definition of Complete
What must exist and be verified:
- [ ] Primary deliverable: [specific, measurable]
- [ ] Quality standards: [specific metrics]
- [ ] Verification method: [how to confirm]

[For build/create goals, include:]
### Software Stack
- Deployment type: [web_app|desktop_app|cli|etc.]
- Language/Framework: [specific]
- Target users: [who will use this]
- Deployment artifact: [what gets deployed]

## Recommended MCP Toolset

### REQUIRED Tools ([n] tools)
[For each required tool:]
- **[tool_name]** (★★★★★ | [n] tools | [category])
  - Rationale: [Why essential for THIS goal]
  - Provides: [Key capabilities needed]
  - Install: `[installation command from catalog]`

### RECOMMENDED Tools ([n] tools)
[For each recommended tool:]
- **[tool_name]** (★★★☆☆ | [n] tools | [category])
  - Rationale: [Why beneficial for THIS goal]
  - Alternative: [What would be done without it]
  - Install: `[installation command from catalog]`

### OPTIONAL Tools ([n] tools)
[For each optional tool:]
- **[tool_name]** (★★☆☆☆ | [n] tools | [category])
  - Use case: [When/why this might be helpful]
  - Install: `[installation command from catalog]`

## Tasks (High-Level)
1. **Task 1:** [Description - what objective this achieves]
2. **Task 2:** [Description]
3. **Task 3:** [Description]
[2-5 tasks total]

## Estimated Complexity
- Total steps: [estimate 1-5 per task]
- Critical steps: [estimate 40-60%]
- Build requirements: [if applicable: GUI, packaging, production API, etc.]
```

**Do NOT generate detailed steps yet.**

---

### Step 3a. MANDATORY HUMAN REVIEW & TOOL INSTALLATION

**CRITICAL: This step CANNOT be skipped. No silent mode allowed.**

This is a **single pause point** combining structure review, tool approval, and tool installation.

#### Phase 1: Present Proposal

Present the Draft Proposal to the user and request explicit approval:

```
═══════════════════════════════════════════════════════════════
SPEC PROPOSAL REVIEW REQUIRED
═══════════════════════════════════════════════════════════════

The following SPEC structure has been drafted based on your goal.
Please review and approve before proceeding.

[Show complete Draft Proposal from Step 3, including MCP Toolset]

═══════════════════════════════════════════════════════════════
REQUIRED ACTION:
═══════════════════════════════════════════════════════════════

1. Review the Goal - Is it correct and singular?
2. Review Completion Criteria - Are these the right success measures?
3. Review MCP Toolset - Are these the right tools? Any missing?
4. Review Tasks - Do these collectively achieve the goal?
5. Review Software Stack - Is this the right technical approach? (if applicable)

OPTIONS:
[A] APPROVE structure and toolset → I will install tools now
[R] REVISE structure or toolset → suggest changes
[T] MODIFY tools only → adjust tool classifications
[C] CLARIFY → ask questions before deciding

Enter your choice (A/R/T/C):
```

**Pause execution and wait for user response.**

#### Phase 2: Handle User Response

**If user selects [R] REVISE or [T] MODIFY:**
- Accept user's specific changes to proposal or tool selections
- Apply changes to Draft Proposal
- Re-present updated proposal
- Return to Phase 1 (loop until user selects [A] or [C])

**If user selects [C] CLARIFY:**
- Answer user's questions
- Re-present proposal for approval
- Return to Phase 1

**If user selects [A] APPROVE:**
- Proceed to Phase 3 (Installation)

#### Phase 3: Tool Installation Instructions

Once user approves (selects [A]), present installation instructions:

```
═══════════════════════════════════════════════════════════════
✅ STRUCTURE AND TOOLSET APPROVED
═══════════════════════════════════════════════════════════════

INSTALLATION PHASE
══════════════════

Please install the following MCP servers now before proceeding:

REQUIRED TOOLS (must be installed):
[For each required tool:]
1. [tool_name]
   Command: [installation command]
   
[If RECOMMENDED tools exist:]
RECOMMENDED TOOLS (optional but beneficial):
[For each recommended tool:]
N. [tool_name]
   Command: [installation command]

[If OPTIONAL tools exist:]
OPTIONAL TOOLS (install if desired):
[For each optional tool:]
N. [tool_name]
   Command: [installation command]

═══════════════════════════════════════════════════════════════
INSTALLATION INSTRUCTIONS:
═══════════════════════════════════════════════════════════════

1. Run the install commands above in your terminal
2. Configure MCP servers in your environment:
   - Windows: %APPDATA%\Claude\claude_desktop_config.json
   - macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
   - Linux: ~/.config/Claude/claude_desktop_config.json
3. Restart your MCP client (e.g., Claude Desktop)
4. Test tool availability (optional but recommended)

═══════════════════════════════════════════════════════════════

When installation is complete, confirm:

[Y] Tools installed and configured → Proceed to SPEC generation
[N] Installation failed → Need help troubleshooting
[S] Skip tool installation for now → Generate SPEC anyway (not recommended)

Confirmation:
```

**Pause execution and wait for user confirmation.**

#### Phase 4: Confirm Installation

**If user confirms [Y] Tools Installed:**
- Log: "MCP tools installed and verified by user"
- Update internal state: tools_installed = true
- Display: "✅ Tools installed and configured"
- Display: "✅ Proceeding to detailed SPEC generation (Step 4)"
- Proceed to Step 4

**If user selects [N] Installation Failed:**
- Enter troubleshooting mode
- Ask: "Which tool failed to install? [tool name]"
- Ask: "What error occurred?"
- Provide troubleshooting guidance based on error
- Re-present installation instructions
- Loop until user confirms [Y] or [S]

**If user selects [S] Skip Installation:**
- Display warning:
  ```
  ⚠️ WARNING: Skipping tool installation is not recommended.
  The executor will verify tool availability (Section 1.11) and may HALT
  if required tools are missing.
  
  You can install tools later, but execution will fail if they're needed.
  
  Confirm skip? [Y/N]:
  ```
- If confirmed: Proceed to Step 4 with warning logged
- If not confirmed: Return to installation instructions

#### Phase 5: Exit Checkpoint

Once user confirms installation (or skip with warning):
- **Single pause point complete**
- All approvals collected
- Tools installed (or installation deferred with warning)
- Ready for detailed SPEC generation
- Proceed to Step 4

**Rationale:** This combined checkpoint prevents:
1. Wasted effort on detailed steps if high-level structure is wrong
2. Execution failures due to missing tools
3. Multiple pause points fragmenting the workflow

Catching issues at the proposal level AND ensuring tools are ready creates a smooth path from approval to execution.

---

### Step 4. Generate Detailed Steps and Files

**Prerequisites:** User has approved Draft Proposal from Step 3a

Now generate detailed implementation:

##### STEP GENERATION

For each approved task:
  1. Define **1–5 concrete steps** (specific actions, not abstract objectives)
  2. Identify failure points and define **0–2 backup methods** per step (alternative approaches, not retries)
  3. Mark **critical steps** (40-60% of total)
  4. Define **expected outputs** (specific, measurable)
  5. Assign **mode** (dynamic default, override if needed)
  6. **Determine if research_enabled needed** (see Research Inference below)

##### RESEARCH-ENABLED INFERENCE

For each task, determine if `research_enabled = true` should be set:

**Set to TRUE when task involves:**
- Words indicating knowledge-seeking: "research", "investigate", "explore", "discover", "find current", "identify latest"
- External systems requiring current docs: "API integration", "library usage", "framework setup"
- Rapidly evolving domains: "authentication best practices", "security standards", "modern patterns"
- Verification against external sources: "validate against spec", "check compliance", "confirm standards"
- Domain-specific expertise: Medical, legal, financial standards that LLM may not have current knowledge of

**Set to FALSE (default) when task involves:**
- Implementation using known patterns: "write function", "create class", "implement algorithm"
- Analysis/reasoning: "analyse code", "identify bugs", "optimise performance"
- File operations: "read file", "parse data", "generate report"
- Testing: "write tests", "run test suite", "verify functionality"

**Examples:**

Task: "Research current FastAPI authentication best practices"
→ `research_enabled = true`
→ `research_sources = ["web_search", "documentation"]`

Task: "Implement JWT token validation using researched approach"
→ `research_enabled = false` (implementation, not discovery)

Task: "Identify and integrate appropriate PDF parsing library"
→ `research_enabled = true` (discovery + current options)

##### FILE GENERATION
1. **spec_[descriptor].md**  
   - See template for guidance: 'C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_templates\Spec_template.md'
   - Follow the provided Spec Template structure.  
   - Include definitions for goal, tasks, steps, and backups.  
   - Ensure clarity and logical flow.  
   - Provide one illustrative example in the placeholder section.  

2. **parameters_[descriptor].toml**  
   - See template for guidance: 'C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_templates\parameters_template.toml'
   - Encode the same structure in TOML format.  
   - Maintain one-to-one correspondence between Markdown and TOML elements.  
   - Ensure task, step, and backup IDs match their counterparts.  

3. **exe_[descriptor].md**  
   - See template for guidance: 'C:\Users\Fab2\Desktop\AI\Specs\__SPEC_Engine\_templates\exe_template.md'
   - Generate the execution controller for this Spec.  
   - Include logic for reading the spec, handling modes, retries, and error propagation.  
   - Ensure execution is sequential and logs are written to `progress.json`.

### Step 5. — Pre-Flight Validation

Before generating files, perform comprehensive validation:

#### 5.1 Constitutional Compliance Check
1. Read `constitution.md` from `__SPEC_Engine/_Constitution/` directory
2. Verify the goal description complies with Article I (singular, clear, measurable)
3. Confirm task count is within Article II limits (2-5 tasks)
4. Confirm step count per task is within Article II limits (1-5 steps)
5. Verify backup count per step is within Article II limits (0-2 backups)
6. Check that 40-60% of steps are marked critical (Article VI)
7. Ensure all expected outputs are specific and measurable (Article V)
8. Confirm no anti-patterns are present (Article XII)

#### 5.1a Software Stack Validation (MANDATORY for Build/Create Goals)

**Trigger:** If goal contains keywords: "build", "create", "develop", "system", "application", "app"

**Required Actions:**

1. **Verify Software Stack & Architecture section defined in spec_[descriptor].md:**
   - [ ] Deployment Type selected (web_app, desktop_app, cli, mobile, api, library)
   - [ ] Technology Stack specified (language, framework, database, UI library, packaging)
   - [ ] User Interface Requirements defined (if user-facing)
   - [ ] Deployment Requirements specified (target platform, installation method, startup process)

2. **Verify Definition of Complete section exists in spec_[descriptor].md:**
   - [ ] Functional Completeness checklist present
   - [ ] Deployment Completeness checklist present
   - [ ] User Acceptance criteria defined (if user-facing)
   - [ ] Production Readiness criteria specified (if applicable)

3. **Verify [software_stack] section populated in parameters_[descriptor].toml:**
   - [ ] `deployment_type` not empty
   - [ ] `primary_language` not empty
   - [ ] `framework` defined (or "none" if not applicable)
   - [ ] `packaging_method` defined

4. **Verify [user_interface] section defined in parameters_[descriptor].toml:**
   - [ ] `required` field set appropriately
   - [ ] If `required = true`: `interface_type`, `target_users`, `skill_level` all defined

5. **Verify [deployment] section defined in parameters_[descriptor].toml:**
   - [ ] `target_platform` defined
   - [ ] `installation_type` defined
   - [ ] `startup_method` defined
   - [ ] `configuration_required` list present (even if empty)

6. **Verify [completion_criteria] section exists in parameters_[descriptor].toml:**
   - [ ] All boolean fields present (functional_complete, interface_complete, deployment_complete, production_ready, user_tested, documentation_complete)
   - [ ] `acceptance_criteria` list populated with specific, testable criteria

**If goal contains "for [users]" (e.g., "for volunteers", "for doctors"):**
- MUST have `user_interface.required = true`
- MUST have User Acceptance section in Definition of Complete
- MUST include user stories in spec_[descriptor].md

**Quality Gates:**
```
✅ **PASS**: Software stack fully defined
   - deployment_type = "desktop_app"
   - primary_language = "python"
   - framework = "pyqt5"
   - ui_required = true
   - completion_criteria = 6 defined

❌ **FAIL**: Software stack missing or incomplete
   - deployment_type = "" (empty)
   - ui_library undefined
   - completion_criteria section missing
   - HALT: Cannot generate spec without knowing what to build
```

**If validation fails:**
- DO NOT proceed to file generation
- Log specific missing fields
- Request clarification: "Goal requires building a system but software stack undefined. Please specify: deployment type, target users, technology stack, and completion criteria."

#### 5.2 Structural Validation
1. Ensure goal is singular and non-ambiguous
2. Verify tasks logically decompose the goal
3. Check steps are concrete actions (not abstract objectives)
4. Validate backups are alternative methods (not simple retries)
5. Confirm backup descriptions explain the alternative approach

#### 5.3 Pre-Generation Quality Gates
Generate a validation report showing:
- ✅ **PASS**: Goal is singular and clear
- ✅ **PASS**: 3 tasks defined (within 2-5 range)
- ✅ **PASS**: Step counts are [3, 4, 5] (within 1-5 range)
- ✅ **PASS**: 7 of 12 steps marked critical (58%, within 40-60%)
- ✅ **PASS**: All expected outputs are specific
- ⚠️ **WARN**: Task 2 Step 3 has no backup (non-critical, acceptable)

If any **FAIL** conditions detected:
1. Log validation failures
2. Request clarification or correction
3. Do NOT proceed to file generation until resolved

#### 5.4 Alignment Check
- Tasks and Steps must be **synchronized** across the spec and parameters files
- Verify all content across the three files refers to the **same goal** and **identical task/step IDs**
- Ensure all steps logically contribute to the goal
- Confirm backups align with their parent steps
- Verification mechanisms must be in place to confirm consistency before execution
- Ensure JSON logging (`progress.json`) is referenced for tracking retries, critical failures, and mode switches

---

### Step 6. Output Check
At the end of generation, present:

/Specs/
   └── [descriptor]/
        ├── spec_[descriptor].md
        ├── parameters_[descriptor].toml
        ├── exe_[descriptor].md
        └── progress_[descriptor].json   # (created at runtime)

        
## Quality Standards

- Maintain **internal consistency** across all files.  
- Avoid repetition — reuse terms and IDs precisely.  
- Each step, backup, and constraint must **serve the goal**.  
- All file contents must be syntactically valid and human-readable.  
- Be explicit — avoid placeholder ambiguity except where instructed.  

---

## Reminder
All generated output must:
- Follow the provided templates exactly.  
- Remain tightly focused on achieving the North Star goal.  
- Be internally cohesive and execution-ready.

---

**End of Commander Spec**
```

Now let me update the template files. Starting with spec_template.md:

```markdown
# Spec Template (Goal-First)

**Version:** 1.0  
**Last Updated:** 2025-11-02  
**Purpose:** Human-readable specification template for goal-driven LLM execution

---

## Goal
[Insert single overarching goal here]

---

## Software Stack & Architecture

**MANDATORY for goals containing: "build", "create", "system", "application", "app", "develop"**

### Deployment Type
Select ONE:
- [ ] Web Application (browser-based)
- [ ] Desktop Application (installable exe/app)
- [ ] Command-line Tool (terminal-based, for technical users)
- [ ] Mobile Application
- [ ] API Service
- [ ] Library/Module (for developers)

### Technology Stack
- **Language:** [Python/JavaScript/TypeScript/Go/Rust/etc.]
- **Framework:** [Flask/Django/Electron/Qt/React/Next.js/etc.]
- **Database:** [SQLite/PostgreSQL/MongoDB/None/etc.]
- **UI Library:** [PyQt/Tkinter/HTML+CSS/React/None/etc.]
- **Packaging:** [PyInstaller/Electron Builder/Docker/npm package/etc.]

### User Interface Requirements
- **Primary users:** [Who will use this system? Be specific: "developers", "shop volunteers", "medical staff"]
- **Interaction method:** [GUI buttons/CLI commands/Web browser/Touch screen/API calls]
- **Technical skill level:** [None/Basic/Advanced]
- **Accessibility requirements:** [Large buttons/Screen reader support/High contrast/Simple language/etc.]

### Deployment Requirements
- **Target environment:** [Windows 10+/macOS/Linux/Cloud/Docker/Browser/etc.]
- **Installation method:** [Double-click installer/Portable .exe/npm install/Docker compose/Web URL/etc.]
- **Configuration needed:** [API keys/Database credentials/Printer setup/None/etc.]
- **Startup process:** [Click desktop icon/Run command/Open URL/etc.]

---

## Definition of Complete

**MANDATORY: Define specific, measurable criteria for when this goal is ACHIEVED.**

What must exist and be verified:
- [ ] Primary deliverable (report, executable, test suite, documentation, etc.)
- [ ] Quality standards met (specific, measurable)
- [ ] Verification method defined (how to objectively confirm completion)

For build/create/system goals, see Software Stack section above.  
Validation logic in `exe_template.md` Section 6.4.

---

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
{{#each mcp_tools.recommended}}
- **{{this.name}}**
  - Rationale: {{this.rationale}}
  - Alternative: {{this.alternative}}
  - Install command: `{{this.install_command}}`
{{/each}}

**OPTIONAL Tools:**
{{#each mcp_tools.optional}}
- **{{this.name}}**
  - Use case: {{this.use_case}}
  - Install command: `{{this.install_command}}`
{{/each}}

### Tool Verification

The executor will verify tool availability during initialisation (Section 1.11) as a **safety check**.

These tools were installed during SPEC creation (Step 3a), so verification should pass automatically.

**If verification fails**, it indicates:
- MCP configuration changed since SPEC creation
- MCP client was not properly restarted after installation
- Installation was incomplete or tools were uninstalled

Refer to installation commands above if re-installation is needed.

---

**Example (populated):**

## MCP Toolset

### Installed Tools (Verified During SPEC Creation)

The following MCP servers were approved and installed during SPEC creation (Step 3a).

**REQUIRED Tools:**
- **postgres**
  - Rationale: Core database operations essential for data management goal
  - Install command: `npm install @modelcontextprotocol/server-postgres`

- **github**
  - Rationale: Version control and file operations required for code management
  - Install command: `npm install @modelcontextprotocol/server-github`

**RECOMMENDED Tools:**
- **playwright**
  - Rationale: Browser automation improves testing workflow efficiency
  - Alternative: Manual browser testing via UI
  - Install command: `npm install @modelcontextprotocol/server-playwright`

**OPTIONAL Tools:**
- **notion**
  - Use case: Documentation publishing if project uses Notion workspace
  - Install command: `npm install @modelcontextprotocol/server-notion`

### Tool Verification

The executor will verify tool availability during initialisation (Section 1.11) as a **safety check**.

These tools were installed during SPEC creation (Step 3a), so verification should pass automatically.

**If verification fails**, it indicates:
- MCP configuration changed since SPEC creation
- MCP client was not properly restarted after installation
- Installation was incomplete or tools were uninstalled

Refer to installation commands above if re-installation is needed.

---

## Definitions
- goal: The overarching objective the agent must achieve.
- task[n]: Discrete objectives derived from the goal. `[n]` denotes task number.
- step[m]: Concrete actions or reasoning sub-unit within a task. `[m]` denotes step number.
- backup[p]: Alternative method or reasoning path for step[m]. `[p]` denotes backup number.
- critical_flag: Boolean indicating whether a step is critical.
- mode: Execution mode per step[m]: `silent` or `collaborative`.
- progress.json: Structured log tracking execution, retries, outputs, and flags.

## Components
- Codebase  
- Test framework  
- Documentation sources

**Machine-Readable Components (Optional):**  
For specs that need to validate component references, define them in the `[components]` section of parameters_[descriptor].toml:
- `codebase = "Main source repository at /src"`
- `test_framework = "PyTest testing suite v7.0"`
- `api_endpoint = "Production API at https://api.example.com"`

This enables exe Section 1.9 to verify that steps only reference defined components.  

## Constraints
- All critical functionality must be tested  
- Steps must be goal-directed  
- Logging must be completed for every step

**Machine-Readable Constraints (Optional):**  
For automated validation of numeric/boolean constraints, define them in the `[constraints]` section of parameters_[descriptor].toml:
- `max_latency_ms = 200` (numeric threshold - exe controller can validate)
- `coverage_required = true` (boolean requirement - exe controller can check)
- `output_format = "markdown"` (string requirement - exe controller can verify)

**Freeform Constraints:**  
Narrative constraints can remain in Markdown only without TOML definition. Use machine-readable constraints when you need the exe controller to automatically validate thresholds.

**Bridging Note:** When using machine-readable constraints, reference them explicitly:  
Example: "Maximum latency: See `constraints.max_latency_ms` in parameters_[descriptor].toml (must be ≤ 200ms)"  

---

## User Stories (Optional)

**When to Use:** User-facing features or workflows where linking technical implementation to user intent provides valuable context.

**When to Skip:** Technical tasks with no direct user impact (e.g., refactoring, optimisation, infrastructure work).

User stories follow the format:
- As a [role], I want [capability] so that [benefit]

**Example:**
- As a developer, I want documentation automatically extracted so I can understand module behaviour without reading code
- As a QA engineer, I want edge cases identified so testing is comprehensive
- As a maintainer, I want bugs traced to functions so fixes are targeted

**Purpose:** User stories bridge abstract goals and technical tasks, providing design insights that guide task-level decisions.

---

## Clarification Steps (Optional)

**When to Use:** Goals that inherently require human judgment or domain knowledge that the LLM cannot infer.

**How to Implement:** Create an explicit collaborative step that pauses for human input:

```markdown
### Task [1]: Gather Requirements

- **Step [1]:** Identify ambiguous requirements
  - **Primary method:** Analyse goal description for undefined terms, unclear scope, missing criteria
  - **Expected output:** List of specific questions requiring human clarification
  - **Critical:** true
  - **Mode:** collaborative (pauses execution for human response)

- **Step [2]:** Document clarified requirements
  - **Primary method:** Structure human responses into testable requirements
  - **Expected output:** Requirements document with specific, measurable criteria
  - **Critical:** true
  - **Mode:** silent (proceeds autonomously with clarified inputs)
```

**Key Principle:** Clarification is a step within the spec, not a separate phase. This preserves autonomous execution while handling ambiguity explicitly.

---

## Goal Example

**Goal:** Perform a comprehensive review and testing of a software module.

### Task [1]: Research module functionality
**TOML Reference:** `tasks[id=1]` in parameters_[descriptor].toml  
**Research Enabled:** Optional (`research_enabled = true` for knowledge-intensive tasks)

- **Step [1]:** Extract specifications from documentation  
  - **Primary method:** Parse documentation files systematically  
  - **Backup [1]:** If documentation incomplete, inspect source code directly  
  - **Backup [2]:** If source unclear, reference similar module implementations  
  - **Expected output:** Structured summary of module functions and dependencies  
  - **Critical:** true  
  - **Mode:** silent  

- **Step [2]:** Analyse module dependencies and function signatures  
  - **Primary method:** Map import statements and function declarations  
  - **Expected output:** Dependency graph and signature list  
  - **Critical:** true  
  - **Mode:** silent  

- **Step [3]:** Summarise intended behaviour  
  - **Primary method:** Synthesise findings into coherent summary  
  - **Backup [1]:** If synthesis unclear, request collaborative review  
  - **Expected output:** Behaviour description document  
  - **Critical:** false  
  - **Mode:** silent  

- **Verification:** All functions documented or inferred; TOML constraint `coverage_required = true` satisfied  
- **Logging:** Append structured entry to progress_[descriptor].json for each step  

### Task [2]: Create automated tests
**TOML Reference:** `tasks[id=2]` in parameters_[descriptor].toml

- **Step [1]:** Identify core functions  
  - **Primary method:** Extract public API functions from module  
  - **Expected output:** List of functions requiring tests  
  - **Critical:** true  
  - **Mode:** silent  

- **Step [2]:** Determine edge cases  
  - **Primary method:** Analyse function parameters and boundary conditions  
  - **Backup [1]:** Reference previous modules for common edge case patterns  
  - **Expected output:** Edge case matrix  
  - **Critical:** true  
  - **Mode:** silent  

- **Step [3]:** Draft test scenarios  
  - **Primary method:** Create test case specifications for each function  
  - **Expected output:** Test scenario documentation  
  - **Critical:** false  
  - **Mode:** silent  

- **Step [4]:** Implement initial test suite  
  - **Primary method:** Write test code using project testing framework  
  - **Backup [1]:** If framework unclear, reference testing templates  
  - **Expected output:** Executable test suite  
  - **Critical:** true  
  - **Mode:** silent  

- **Verification:** Test coverage includes core and edge functions; meets `constraints.min_coverage` in TOML  
- **Logging:** Append structured entry to progress_[descriptor].json for each step  

### Task [3]: Debug and verify module behaviour
**TOML Reference:** `tasks[id=3]` in parameters_[descriptor].toml

- **Step [1]:** Run test suite and record failures  
  - **Primary method:** Execute test suite and capture failure logs  
  - **Expected output:** Failure report with stack traces  
  - **Critical:** true  
  - **Mode:** silent  

- **Step [2]:** Trace errors to specific functions  
  - **Primary method:** Analyse stack traces and debug logs  
  - **Backup [1]:** Use debugger for step-through analysis  
  - **Expected output:** Root cause identification  
  - **Critical:** true  
  - **Mode:** silent  

- **Step [3]:** Apply fixes  
  - **Primary method:** Implement corrections based on root cause  
  - **Expected output:** Modified source code  
  - **Critical:** true  
  - **Mode:** silent  

- **Step [4]:** Re-run tests and verify pass/fail status  
  - **Primary method:** Execute full test suite again  
  - **Backup [1]:** Manual verification if automated tests inconclusive  
  - **Expected output:** Test results showing all passes  
  - **Critical:** true  
  - **Mode:** silent  

- **Step [5]:** Document fixes and update test coverage  
  - **Primary method:** Update documentation with fix descriptions  
  - **Expected output:** Updated documentation and coverage report  
  - **Critical:** false  
  - **Mode:** silent  

- **Verification:** Test suite passes; meets `constraints.pass_rate = 100%` in TOML; documentation updated  
- **Logging:** Append structured entry to progress_[descriptor].json for each step  

### JSON Log Example
````json
{
  "task_id": "task1",
  "step_id": "step2",
  "attempt_number": 1,
  "method_used": "primary",
  "constraint_status": {
      "coverage": "pass",
      "alignment_with_goal": "pass"
  },
  "mode": "silent",
  "critical_flag": true,
  "timestamp": "2025-11-01T12:00Z"
}

---

## Bridging: Markdown ↔ TOML Synchronisation

This spec file (spec_[descriptor].md) must maintain perfect alignment with its companion file (parameters_[descriptor].toml).

**Bridging Requirements:**
1. Each task in this file must have a corresponding `[[tasks]]` entry in TOML with matching ID
2. Each step within a task must have a corresponding `[[tasks.steps]]` entry with matching ID
3. Each backup method must be referenced in TOML structure
4. Constraints and components should cross-reference TOML keys explicitly
5. Expected outputs in this file should match `expected_output` fields in TOML

**Example Cross-References:**
- "See `constraints.max_latency` in parameters_[descriptor].toml"
- "As defined in `tasks[id=2].steps[id=3]` in TOML"
- "Must satisfy TOML verification requirements"

The exe_[descriptor].md controller validates this synchronisation during initialisation (Section 1.8).

---

### Instructions for LLM
1. Start with the **goal** (singular, clear, North Star).  
2. Break the goal into **tasks `[n]`** (discrete objectives).  
3. For each task, define **steps `[m]`** needed to achieve it (concrete actions).  
4. Include **backup `[p]`** methods where appropriate (alternative reasoning paths, not just retries).  
5. Ensure **bridging alignment**: every task/step ID must match between this file and parameters_[descriptor].toml.  
6. Add explicit **TOML cross-references** for constraints and configuration values.  
7. Log each step in **progress_[descriptor].json**, including mode, retries, and critical flags.  
8. Verify outputs and constraints after each step.  
9. Read prior step results from progress.json before executing dependent steps (error propagation).  


```

Now update parameters_template.toml:

```plaintext
# parameters_[descriptor].toml
# Template Version: 1.0
# Last Updated: 2025-11-02
# Purpose: Machine-readable parameters template for structured execution

[meta]
file_role = "Machine-readable parameters for structured execution"
created_by = "commander-spec.md"
goal_descriptor = "[descriptor]"
related_files = ["spec_[descriptor].md", "exe_[descriptor].md"]
log_output = "progress_[descriptor].json"
created_date = "YYYY-MM-DD"
version = "1.0"

[execution]
default_mode = "dynamic"  # Options: "dynamic" (default), "silent", "collaborative"
# User will be prompted at runtime to confirm or change mode
# Dynamic mode: autonomous with intelligent escalation
# Silent mode: fully autonomous, minimal interruption
# Collaborative mode: pause at each critical decision

[goal]
description = "[Insert goal description]"

# === MANDATORY FOR BUILD/CREATE/SYSTEM GOALS: Software Stack & Deployment ===
# If goal contains "build", "create", "system", "application", "app", these sections are REQUIRED
# Exe Section 1.1a validates these before proceeding

[software_stack]
deployment_type = ""  # REQUIRED: "web_app" | "desktop_app" | "cli" | "mobile" | "api" | "library"
primary_language = ""  # REQUIRED: "python" | "javascript" | "typescript" | "go" | "rust" | etc.
framework = ""  # Framework if applicable: "flask" | "django" | "electron" | "pyqt" | "react" | "none"
database = ""  # "sqlite" | "postgresql" | "mongodb" | "none"
ui_library = ""  # "pyqt5" | "tkinter" | "html_css" | "react" | "none"
packaging_method = ""  # "pyinstaller" | "electron_builder" | "docker" | "npm" | "none"

[user_interface]
required = false  # MANDATORY: true for user-facing systems, false for libraries/APIs
interface_type = ""  # "gui" | "cli" | "web" | "touch" | "api_only"
target_users = ""  # Who uses this? "developers" | "shop volunteers" | "medical staff" | etc.
skill_level = ""  # "none" | "basic" | "advanced"
accessibility = []  # ["large_buttons", "simple_language", "screen_reader", "high_contrast"]

[deployment]
target_platform = ""  # "windows" | "macos" | "linux" | "web" | "docker" | "cross_platform"
installation_type = ""  # "installer" | "portable_exe" | "web_url" | "package_manager" | "docker_compose"
configuration_required = []  # ["api_keys", "database_credentials", "printer_setup", "none"]
startup_method = ""  # "desktop_icon" | "run_command" | "open_url" | "import_module"

[completion_criteria]
# MANDATORY: Define what "complete" means for this goal
# Exe Section 6.4 verifies these before marking ACHIEVED

# List specific, measurable criteria for goal completion
acceptance_criteria = [
    # Examples:
    # "Test suite passes with ≥95% coverage"
    # "Analysis report includes sentiment scores for 10k reviews"
    # "Executable runs on clean Windows 10 without Python"
    # "Documentation covers all API endpoints with examples"
]

# Optional flags for build/system goals
# production_ready = false  # Real APIs (not test mode) - uncomment if needed
# user_tested = false       # Verified by target users - uncomment if needed

# === MCP Tools Configuration ===
# Tools selected during SPEC creation (Step 3a) and installed by human before execution

[mcp_tools]
# List of MCP server names (strings) installed during Step 3a
required = []      # Must be installed - executor will HALT if missing (Section 1.11)
recommended = []   # Should be installed - executor will WARN if missing but continue
optional = []      # Nice to have - no warning if missing

# Verification settings
[mcp_tools.verification]
check_on_startup = true                    # Verify tools before execution (Section 1.11)
halt_if_required_missing = true            # Stop execution if required tools absent
warn_if_recommended_missing = true         # Show warning for missing recommended tools
log_available_tools = true                 # Log which tools were successfully detected

# Optional: Tool-specific configuration (add sections as needed)
# [mcp_tools.config.postgres]
# connection_string = "postgresql://localhost:5432/mydb"
# readonly = true
#
# [mcp_tools.config.github]
# default_repo = "owner/repo"
# default_branch = "main"

# === Example (populated) ===
# [mcp_tools]
# required = ["postgres", "github"]
# recommended = ["playwright"]
# optional = ["notion"]
#
# [mcp_tools.verification]
# check_on_startup = true
# halt_if_required_missing = true
# warn_if_recommended_missing = true
# log_available_tools = true
#
# [mcp_tools.config.postgres]
# connection_string = "postgresql://localhost:5432/mydb"
# readonly = true

# === Components & Constraints ===
# Only define these sections if your spec requires machine-readable validation
# For freeform specs, leave commented or delete these sections

[components]
# Define components that will be referenced or validated
# Use when steps need to reference specific system components
# Example: codebase = "Main source repository at /src"
# Example: test_framework = "PyTest testing suite v7.0"
# Example: api_endpoint = "Production API at https://api.example.com"

[constraints]
# Define machine-readable constraints for automated validation
# Particularly useful for numeric/boolean thresholds that exe controller can check
#
# Numeric constraints (validated as numbers):
# Example: max_latency_ms = 200
# Example: min_accuracy_pct = 95
# Example: max_file_size_mb = 50
#
# Boolean constraints (validated as true/false):
# Example: coverage_required = true
# Example: tests_must_pass = true
# Example: documentation_required = false
#
# String constraints (validated as specific values):
# Example: output_format = "markdown"
# Example: language = "python"
#
# Freeform constraints can remain in spec_[descriptor].md only
# Machine-readable constraints defined here enable exe Section 1.9 validation

# Tasks execute sequentially by ID
# mode: "silent" (autonomous) | "collaborative" (requires user input) | per-step, overridden by execution.default_mode
# critical_flag: true = step failure triggers escalation; false = logs and continues
#
# BACKUP STRUCTURE:
# Backups can be cognitive (LLM alternative approach) or tool-based (external scripts/programs)
# For tool-based backups, add:
#   execution_method = "tool" or "script"
#   tool_path = "path/to/tool_or_script"
#   tool_args = "--argument-flags"
#
# Example tool-based backup:
#   [[tasks.steps.backups]]
#   id = 1
#   description = "Use pypdf2 for PDF conversion"
#   execution_method = "tool"
#   tool_path = "scripts/convert_pdf_pypdf2.py"
#   tool_args = "--preserve-layout"
#   trigger_condition = "primary_failure"

[[tasks]]
id = 1
description = "[Task 1 description]"
research_enabled = false  # Set to true for knowledge-intensive tasks (discovery, verification, current info)
# research_sources = ["web_search", "documentation", "technical_specs", "github_repos", "academic"]  # Uncomment if research_enabled = true
# Research sources options:
#   - web_search: General web searches for current information
#   - documentation: Official documentation (provide URLs if specific)
#   - technical_specs: API specs, RFCs, standards documents
#   - github_repos: Repository searches for implementation examples
#   - academic: Research papers (arXiv, PubMed, etc.)

  [[tasks.steps]]
  id = 1
  description = "[Step 1 action]"
  expected_output = "[Expected output description]"
  critical_flag = true
  mode = "silent"
  max_retries = 2

    [[tasks.steps.backups]]
    id = 1
    description = "[Backup method 1 if primary fails]"
    trigger_condition = "primary_failure"

    [[tasks.steps.backups]]
    id = 2
    description = "[Backup method 2 if backup 1 fails]"
    trigger_condition = "backup_1_failure"

  [[tasks.steps]]
  id = 2
  description = "[Step 2 action]"
  expected_output = "[Expected output description]"
  critical_flag = true
  mode = "silent"
  max_retries = 2

    [[tasks.steps.backups]]
    id = 1
    description = "[Backup method if primary fails]"
    trigger_condition = "primary_failure"

  [[tasks.steps]]
  id = 3
  description = "[Step 3 action]"
  expected_output = "[Expected output description]"
  critical_flag = false
  mode = "silent"
  max_retries = 1

[[tasks]]
id = 2
description = "[Task 2 description]"

  [[tasks.steps]]
  id = 1
  description = "[Step 1 action]"
  expected_output = "[Expected output description]"
  critical_flag = true
  mode = "silent"
  max_retries = 2

    [[tasks.steps.backups]]
    id = 1
    description = "[Backup method if primary fails]"
    trigger_condition = "primary_failure"

  [[tasks.steps]]
  id = 2
  description = "[Step 2 action]"
  expected_output = "[Expected output description]"
  critical_flag = false
  mode = "silent"
  max_retries = 1

    [[tasks.steps.backups]]
    id = 1
    description = "[Backup method if primary fails]"
    trigger_condition = "primary_failure"

  [[tasks.steps]]
  id = 3
  description = "[Step 3 action]"
  expected_output = "[Expected output description]"
  critical_flag = false
  mode = "silent"
  max_retries = 1

  [[tasks.steps]]
  id = 4
  description = "[Step 4 action]"
  expected_output = "[Expected output description]"
  critical_flag = true
  mode = "silent"
  max_retries = 2

    [[tasks.steps.backups]]
    id = 1
    description = "[Backup method if primary fails]"
    trigger_condition = "primary_failure"

[[tasks]]
id = 3
description = "[Task 3 description]"

  [[tasks.steps]]
  id = 1
  description = "[Step 1 action]"
  expected_output = "[Expected output description]"
  critical_flag = true
  mode = "silent"
  max_retries = 2

    [[tasks.steps.backups]]
    id = 1
    description = "[Backup method if primary fails]"
    trigger_condition = "primary_failure"

  [[tasks.steps]]
  id = 2
  description = "[Step 2 action]"
  expected_output = "[Expected output description]"
  critical_flag = true
  mode = "silent"
  max_retries = 2

    [[tasks.steps.backups]]
    id = 1
    description = "[Backup method if primary fails]"
    trigger_condition = "primary_failure"

  [[tasks.steps]]
  id = 3
  description = "[Step 3 action]"
  expected_output = "[Expected output description]"
  critical_flag = true
  mode = "silent"
  max_retries = 2

  [[tasks.steps]]
  id = 4
  description = "[Step 4 action]"
  expected_output = "[Expected output description]"
  critical_flag = true
  mode = "silent"
  max_retries = 2

    [[tasks.steps.backups]]
    id = 1
    description = "[Backup method 1 if primary fails]"
    trigger_condition = "primary_failure"

    [[tasks.steps.backups]]
    id = 2
    description = "[Backup method 2 if backup 1 fails]"
    trigger_condition = "backup_1_failure"

  [[tasks.steps]]
  id = 5
  description = "[Step 5 action]"
  expected_output = "[Expected output description]"
  critical_flag = false
  mode = "silent"
  max_retries = 1

[error_propagation]
enabled = true
read_prior_steps = true                # Steps read progress.json before executing
dependency_tracking = true             # Track inter-step dependencies
propagation_strategy = "collaborative_review"  # Options: "halt_on_critical", "continue_and_log", "collaborative_review"
                                       # Recommended for dynamic mode: "collaborative_review"
                                       # Recommended for silent mode: "halt_on_critical"
failure_threshold = 3                  # Escalate after N consecutive failures (for dynamic mode)

[logging]
output_file = "progress_[descriptor].json"
log_events = ["start", "step_complete", "retry", "error", "completion"]
record_retries = true
record_timestamps = true
record_mode_switches = true

[verification]
check_task_alignment = true
check_step_order = true
check_file_integrity = true
check_mode_consistency = true
validate_backup_coverage = true        # Ensure critical steps have backups
verify_cross_references = true         # Validate Markdown ↔ TOML bridging
check_expected_outputs = true          # Confirm all steps define expected outputs
validate_backup_trigger_conditions = true  # Ensure backup triggers are valid

[progress_tracking]
progress_file = "progress_[descriptor].json"
fields = ["task_id", "step_id", "status", "retry_count", "timestamp", "message"]
update_frequency = "on_step_completion"


```

Now add Section 1.11 to exe_template.md:

```markdown
# exe_template.md

**Version:** 1.0  
**Last Updated:** 2025-11-02  
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

```

Now let me update WORKFLOW_DIAGRAM.md to include the new Step 2.5 and updated Step 3a:

```markdown
# SPEC Engine Workflow Diagram

**Complete lifecycle from goal to execution to completion**

---

## High-Level Overview

```
USER GOAL → SPEC GENERATION → HUMAN REVIEW → FILE GENERATION → VALIDATION → EXECUTION → VERIFICATION → COMPLETE
```

---

## System Architecture Diagram

### Complete SPEC Engine Ecosystem

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                              SPEC ENGINE ARCHITECTURE                         │
└───────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                                  USER LAYER                                     │
│  ┌─────────────┐        ┌──────────────┐        ┌─────────────────┐           │
│  │   Define    │        │   Review &   │        │   Monitor       │           │
│  │   Goal      │───────▶│   Approve    │───────▶│   Execution     │           │
│  └─────────────┘        └──────────────┘        └─────────────────┘           │
└─────────────────────────────────────────────────────────────────────────────────┘
         │                         │                         │
         ▼                         ▼                         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FRAMEWORK LAYER                                    │
│                          (__SPEC_Engine directory)                              │
│                                                                                 │
│  ┌────────────────────┐           ┌─────────────────────┐                     │
│  │   CONSTITUTIONAL   │           │      GENERATION      │                     │
│  │      LAYER         │           │        LAYER         │                     │
│  │                    │           │                      │                     │
│  │  ┌──────────────┐  │           │  ┌───────────────┐  │                     │
│  │  │constitution  │  │◀──governs──│  │  Commander    │  │                     │
│  │  │    .md       │  │           │  │  Spec.md      │  │                     │
│  │  │              │  │           │  └───────┬───────┘  │                     │
│  │  │ 14 Articles  │  │           │          │          │                     │
│  │  └──────────────┘  │           │          ▼          │                     │
│  │                    │           │  ┌───────────────┐  │                     │
│  │  ┌──────────────┐  │           │  │   Templates   │  │                     │
│  │  │  DESIGN_     │  │           │  │               │  │                     │
│  │  │  PHILOSOPHY  │  │           │  │ • Spec.md     │  │                     │
│  │  │    .md       │  │           │  │ • params.toml │  │                     │
│  │  │              │  │           │  │ • exe.md      │  │                     │
│  │  │ Rationale    │  │           │  └───────────────┘  │                     │
│  │  └──────────────┘  │           │                      │                     │
│  └────────────────────┘           └──────────────────────┘                     │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────┐                  │
│  │               CONFIGURATION LAYER                        │                  │
│  │                                                           │                  │
│  │              ┌──────────────────────┐                    │                  │
│  │              │     DNA_SPEC.md      │                    │                  │
│  │              │                      │                    │                  │
│  │              │  5-Question          │                    │                  │
│  │              │  Interview           │                    │                  │
│  │              └──────────┬───────────┘                    │                  │
│  │                         │                                │                  │
│  │                         ▼                                │                  │
│  │              ┌──────────────────────┐                    │                  │
│  │              │  project_            │                    │                  │
│  │              │  constitution.toml   │                    │                  │
│  │              │                      │                    │                  │
│  │              │  • Risk level        │                    │                  │
│  │              │  • Test strategy     │                    │                  │
│  │              │  • Execution mode    │                    │                  │
│  │              │  • Backend prefs     │                    │                  │
│  │              └──────────────────────┘                    │                  │
│  └─────────────────────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ generates
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SPECIFICATION LAYER                                │
│                           (SPECs/[DNA_CODE]/spec_[descriptor]/)                 │
│                                                                                 │
│  ┌─────────────────────┐   ┌──────────────────────┐   ┌────────────────────┐  │
│  │  spec_[desc].md     │   │ parameters_[desc]    │   │  exe_[desc].md     │  │
│  │                     │   │       .toml          │   │                    │  │
│  │  Human Story        │◀─▶│                      │   │  Executor Logic    │  │
│  │                     │   │  Machine Config      │◀─▶│                    │  │
│  │  • Goal             │   │                      │   │  • Validation      │  │
│  │  • Tasks            │   │  • Task structure    │   │  • Execution flow  │  │
│  │  • Steps            │   │  • Flags & settings  │   │  • Mode control    │  │
│  │  • Backups          │   │  • Expected outputs  │   │  • Analysis        │  │
│  │  • Reasoning        │   │  • Constraints       │   │  • Verification    │  │
│  └─────────────────────┘   └──────────────────────┘   └─────────┬──────────┘  │
│                                                                  │             │
│                                                                  │ executes    │
└──────────────────────────────────────────────────────────────────┼─────────────┘
                                                                   │
                                                                   ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              EXECUTION LAYER                                    │
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                          INITIALIZATION PHASE                             │  │
│  │  ┌──────────────┐  ┌───────────────┐  ┌──────────────┐  ┌────────────┐  │  │
│  │  │ File Check   │─▶│ Parse Files   │─▶│  Validation  │─▶│ Mode       │  │  │
│  │  │ (Section 1.1)│  │ (Section 1.3) │  │ (1.4-1.10)   │  │ Selection  │  │  │
│  │  └──────────────┘  └───────────────┘  └──────────────┘  └────────────┘  │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                       │                                         │
│                                       ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                          EXECUTION PHASE                                  │  │
│  │                                                                            │  │
│  │  FOR EACH TASK (sequential):                                              │  │
│  │  ┌────────────────────────────────────────────────────────────────────┐  │  │
│  │  │  ┌──────────────┐       ┌──────────────┐      ┌────────────────┐  │  │  │
│  │  │  │Constitutional│       │   Execute    │      │  Dynamic Mode  │  │  │  │
│  │  │  │    Check     │──────▶│   Steps      │─────▶│  Evaluation    │  │  │  │
│  │  │  │ (Section 2.0)│       │ (Section 2.1)│      │ (Section 2.2)  │  │  │  │
│  │  │  └──────────────┘       └──────┬───────┘      └────────────────┘  │  │  │
│  │  │                                 │                                   │  │  │
│  │  │         FOR EACH STEP:          ▼                                   │  │  │
│  │  │         ┌─────────────────────────────────────────┐                │  │  │
│  │  │         │  1. Read prior outcomes (error prop)    │                │  │  │
│  │  │         │  2. Attempt PRIMARY method              │                │  │  │
│  │  │         │  3. If fail → Try BACKUP [1]            │                │  │  │
│  │  │         │  4. If fail → Try BACKUP [2]            │                │  │  │
│  │  │         │  5. If critical + all fail → Escalate   │                │  │  │
│  │  │         │  6. Log to progress.json                │                │  │  │
│  │  │         └─────────────────────────────────────────┘                │  │  │
│  │  └────────────────────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                       │                                         │
│                                       ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                      POST-EXECUTION ANALYSIS                              │  │
│  │  ┌───────────────┐  ┌─────────────────┐  ┌─────────────────────────┐    │  │
│  │  │   Failure     │  │  Constitutional │  │   Completion            │    │  │
│  │  │   Pattern     │─▶│   Compliance    │─▶│   Verification          │    │  │
│  │  │   Analysis    │  │   Review        │  │   (Section 6.4)         │    │  │
│  │  │ (Section 6.1) │  │ (Section 6.2)   │  │                         │    │  │
│  │  └───────────────┘  └─────────────────┘  └────────┬────────────────┘    │  │
│  └────────────────────────────────────────────────────┼───────────────────────┘│
└─────────────────────────────────────────────────────────┼─────────────────────┘
                                                          │
                                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PERSISTENCE LAYER                                  │
│                                                                                 │
│              ┌────────────────────────────────────────────────┐                │
│              │      progress_[descriptor].json                │                │
│              │                                                │                │
│              │  Immutable append-only log containing:         │                │
│              │  • All step outcomes                           │                │
│              │  • Methods attempted (primary/backup)          │                │
│              │  • Retry counts and mode switches              │                │
│              │  • Error propagation decisions                 │                │
│              │  • Constitutional compliance tracking          │                │
│              │  • Post-execution analysis                     │                │
│              │  • Final goal achievement status               │                │
│              │                                                │                │
│              │  STATUS: ACHIEVED | PARTIAL | NOT_ACHIEVED     │                │
│              └────────────────────────────────────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────────┘

LEGEND:
  ──▶  Data flow / Process flow
  ◀─▶  Bidirectional synchronisation / Cross-reference
  │    Sequential relationship
  ═══  Constitutional governance
```

### Key Architectural Principles

1. **Separation of Concerns:**
   - Constitutional: Immutable governance (Articles I-XIV)
   - Generation: Commander creates specs from templates
   - Configuration: Optional project-level settings (DNA)
   - Specification: Three synchronized files per goal
   - Execution: Validation → Execution → Analysis → Verification
   - Persistence: Immutable audit trail

2. **Hierarchical Governance:**
   ```
   System Constitution (immutable)
        ↓ governs
   Project Constitution (per-project, optional)
        ↓ configures
   Individual SPEC (per-goal, required)
        ↓ executed by
   Executor (validates, executes, verifies)
        ↓ produces
   Progress Log (immutable audit trail)
   ```

3. **Validation Checkpoints:**
   - **Pre-Generation:** Commander validates constitutional compliance
   - **Pre-Execution:** Exe Section 1 validates files and structure
   - **Runtime:** Exe Section 2.0 checks compliance per task
   - **Post-Execution:** Exe Section 6.2 reviews adherence
   - **Completion:** Exe Section 6.4 verifies goal achievement

4. **Error Handling Layers:**
   - **Step Level:** Primary → Backup[1] → Backup[2]
   - **Task Level:** Error propagation between steps
   - **SPEC Level:** Dynamic mode escalation to collaborative
   - **System Level:** Constitutional violation tracking

---

## Detailed Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SPEC GENERATION PHASE                       │
└─────────────────────────────────────────────────────────────────────┘

[USER INPUT TO LLM]
  │
  ├─→ "Launch SPEC Commander to build a charity shop POS system for volunteers"
  └─→ "Launch SPEC Commander with 'Specs/[DNA_CODE]' to continue SPEC development to analyse user sentiment in 10k product reviews"
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: Project Setup & Initialization                         │
│  ──────────────────────────────────                             │
│  Run Spec_Commander.md                                          │
└─────────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1a: Project Profile Detection                             │
│  ──────────────────────────────                                 │
│  Commander checks: Does DNA folder exist in Specs/?             │
│  (Scans for 8-char folders [A,T,G,C] with project_constitution.toml)
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐       │
│  │ IF FOUND:                                            │       │
│  │ ✅ Load existing project_constitution.toml          │       │
│  │ Display: "Using project: [NAME] (DNA: [CODE])"      │       │
│  │ → Proceed to Step 1b                                │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐       │
│  │ IF NOT FOUND:                                        │       │
│  │ ⚠️ Prompt user:                                      │       │
│  │   [A] Create profile now (invokes DNA_SPEC.md)      │       │
│  │   [B] Skip - use system defaults                    │       │
│  │   [C] Enter existing DNA code                       │       │
│  │                                                       │       │
│  │ IF [A]: Commander invokes DNA_SPEC.md:              │       │
│  │   Q1: What are you trying to achieve?               │       │
│  │   Q2: How will you measure success?                 │       │
│  │   Q3: Critical risks/constraints?                   │       │
│  │   Q4: Required software stack?                      │       │
│  │   Q5: Preferred approach to failures?               │       │
│  │   → Generates DNA code (e.g., ATGCATGC)             │       │
│  │   → Creates Specs/[DNA_CODE]/project_constitution.toml     │
│  │   → Returns to Commander                            │       │
│  │                                                       │       │
│  │ IF [B]: Continue with system defaults only          │       │
│  │ IF [C]: Validate & load specified DNA code          │       │
│  └─────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1b: Context Loading                                       │
│  ────────────────────────                                       │
│  Commander reads:                                               │
│  • DESIGN_PHILOSOPHY.md (principles, patterns, anti-patterns)   │
│  • constitution.md (Articles I-XIV, governance rules)           │
│  • project_constitution.toml (if DNA profile exists)            │
└─────────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1c: Folder Preparation                                    │
│  ───────────────────────────                                    │
│  Create: Specs/[DNA_CODE]/spec_[descriptor]/                    │
│  Placeholder for 3 files + progress.json                        │
└─────────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: Draft High-Level Structure                             │
│  ──────────────────────────────                                 │
│  Commander analyses goal and drafts:                            │
│  ✓ Goal (singular, clear, measurable)                           │
│  ✓ Definition of Complete (what exists + how to verify)        │
│  ✓ Tasks (2-5 high-level objectives)                            │
│  ✓ Software Stack (if build/create goal)                        │
│  ✓ Estimated complexity                                         │
│                                                                  │
│  ⚠ NO DETAILED STEPS YET                                        │
└─────────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2.5: MCP Tool Analysis (NEW)                              │
│  ──────────────────────────────                                 │
│  Commander examines goal and recommends MCP tools:              │
│                                                                  │
│  1. Load: __SPEC_Engine/_tools/mcp_tools_catalog.yaml          │
│     (269 servers, 2900+ tools, 24 categories)                   │
│                                                                  │
│  2. Analyse goal characteristics autonomously:                  │
│     - What activity? (build, analyse, research, etc.)           │
│     - What resources? (files, databases, APIs, etc.)            │
│     - What outputs? (code, reports, data, etc.)                 │
│     - What scale? (script, app, pipeline, system)               │
│                                                                  │
│  3. Identify relevant tool categories                           │
│     - Review 24 categories in catalog                           │
│     - Consider full lifecycle (not just primary task)           │
│     - Think cross-functionally                                  │
│                                                                  │
│  4. Evaluate and classify individual tools:                     │
│     ✓ REQUIRED: Goal cannot be achieved without                 │
│     ✓ RECOMMENDED: Significantly improves efficiency            │
│     ✓ OPTIONAL: Nice to have, enhances workflow                 │
│                                                                  │
│  5. Document rationale for each tool selection                  │
│                                                                  │
│  Output: MCP Toolset recommendations (added to proposal)        │
└─────────────────────────────────────────────────────────────────┘
      │
      ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  STEP 3: MANDATORY HUMAN REVIEW                                ┃
┃  ═══════════════════════════════                               ┃
┃  🚨 NO SILENT MODE ALLOWED - MUST PAUSE FOR USER 🚨            ┃
┃                                                                 ┃
┃  Present Draft Proposal:                                        ┃
┃  ┌─────────────────────────────────────────────┐               ┃
┃  │ SPEC PROPOSAL FOR REVIEW                    │               ┃
┃  │                                              │               ┃
┃  │ Goal: [singular statement]                  │               ┃
┃  │                                              │               ┃
┃  │ Definition of Complete:                     │               ┃
┃  │ • Primary deliverable: [...]                │               ┃
┃  │ • Quality standards: [...]                  │               ┃
┃  │ • Verification method: [...]                │               ┃
┃  │                                              │               ┃
┃  │ Tasks:                                       │               ┃
┃  │ 1. [High-level objective]                   │               ┃
┃  │ 2. [High-level objective]                   │               ┃
┃  │ 3. [High-level objective]                   │               ┃
┃  │                                              │               ┃
┃  │ Software Stack: (if applicable)             │               ┃
┃  │ • Deployment type: desktop_app              │               ┃
┃  │ • Language: Python                          │               ┃
┃  │ • UI: PyQt5 GUI                             │               ┃
┃  │ • Packaging: PyInstaller                    │               ┃
┃  └─────────────────────────────────────────────┘               ┃
┃                                                                 ┃
┃  User Options:                                                  ┃
┃  [A] APPROVE → Continue to Step 4                              ┃
┃  [R] REVISE → Apply changes, re-present                        ┃
┃  [C] CLARIFY → Answer questions, re-present                    ┃
┃                                                                 ┃
┃  ⏸ EXECUTION PAUSED UNTIL USER RESPONDS                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
      │
      │ [USER APPROVES]
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: Generate Detailed Steps and Files                      │
│  ─────────────────────────────────────                          │
│  NOW generate for each approved task:                           │
│  ✓ Concrete steps (1-5 per task)                                │
│  ✓ Backup methods (0-2 per step)                                │
│  ✓ Critical flags (40-60% of steps)                             │
│  ✓ Expected outputs (specific, measurable)                      │
│  ✓ Execution modes (dynamic default)                            │
│                                                                  │
│  Generate 3 files:                                              │
│  ▸ spec_[descriptor].md (human-readable)                        │
│  ▸ parameters_[descriptor].toml (machine-readable)              │
│  ▸ exe_[descriptor].md (execution controller)                   │
└─────────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 5: Pre-Flight Validation                                  │
│  ─────────────────────────                                      │
│  5a. Constitutional Compliance Check                            │
│      • Article I: Goal singular?                                │
│      • Article II: 2-5 tasks, 1-5 steps per task?               │
│      • Article VI: 40-60% critical balance?                     │
│      • Article XIV: Software stack defined (if build goal)?     │
│                                                                  │
│  5b. Software Stack Validation (if build/create goal)           │
│      • deployment_type defined?                                 │
│      • user_interface.required = true (if "for [users]")?       │
│      • completion_criteria populated?                           │
│                                                                  │
│  5c. Structural Validation                                      │
│      • Tasks decompose goal logically?                          │
│      • Steps are concrete actions?                              │
│      • Backups are alternatives (not retries)?                  │
│                                                                  │
│  5d. Quality Gates                                              │
│      ✅ PASS: All checks green → Proceed                        │
│      ❌ FAIL: Violations found → HALT, request fixes            │
└─────────────────────────────────────────────────────────────────┘
      │
      │ [VALIDATION PASS]
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 6: Output Complete SPEC                                   │
│  ────────────────────────────                                   │
│  Specs/[DNA_CODE]/spec_[descriptor]/                            │
│  ├── spec_[descriptor].md                                       │
│  ├── parameters_[descriptor].toml                               │
│  ├── exe_[descriptor].md                                        │
│  └── progress_[descriptor].json (created at runtime)            │
│                                                                  │
│  ✅ SPEC GENERATION COMPLETE                                    │
└─────────────────────────────────────────────────────────────────┘

═════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────┐
│                          EXECUTION PHASE                             │
│                     (exe_[descriptor].md Process)                    │
└─────────────────────────────────────────────────────────────────────┘

[USER INVOKES EXECUTION IN LLM]
  │
  └─→ "Run spec_[descriptor]" or "Execute SPEC"
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  SECTION 1: Initialization and Validation                       │
│  ────────────────────────────────────                           │
│  1.1  File presence check                                       │
│  1.1a Software Stack Validation (if build goal)                 │
│  1.2  Initialize progress.json                                  │
│  1.2a USER MODE SELECTION (Dynamic/Silent/Collaborative)        │
│  1.3  Parse spec.md and parameters.toml                         │
│  1.4  Validate goal                                             │
│  1.5  Validate tasks                                            │
│  1.6  Validate steps                                            │
│  1.7  Validate backups                                          │
│  1.8  Bridging verification (Markdown ↔ TOML sync)              │
│  1.9  Validate components and constraints                       │
│  1.10 Final pre-flight check                                    │
│                                                                  │
│  ✅ IF PASS: Proceed to Section 2                               │
│  ❌ IF FAIL: HALT, log errors, escalate to collaborative        │
└─────────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  SECTION 2: Execution Flow (Per Task)                           │
│  ────────────────────────────                                   │
│  FOR EACH TASK (sequentially):                                  │
│                                                                  │
│  2.0 Constitutional Compliance Check (per task)                 │
│      • Article IV: Error propagation enabled?                   │
│      • Article VI: Critical balance appropriate?                │
│      • Article VIII: Prior step outcomes read?                  │
│      • Article X: Logging comprehensive?                        │
│                                                                  │
│  2.1 Execute Task Steps (sequentially)                          │
│      FOR EACH STEP:                                             │
│      ┌────────────────────────────────────┐                    │
│      │ • Read progress.json (error prop)  │                    │
│      │ • Execute PRIMARY method           │                    │
│      │ • IF FAIL: Try BACKUP [1]          │                    │
│      │ • IF FAIL: Try BACKUP [2]          │                    │
│      │ • IF FAIL: Escalate (if critical)  │                    │
│      │ • Log outcome to progress.json     │                    │
│      └────────────────────────────────────┘                    │
│                                                                  │
│  2.2 Dynamic Mode Evaluation (per step)                         │
│      Check for escalation triggers:                             │
│      • 3+ consecutive failures?                                 │
│      • Backup depletion pattern?                                │
│      • Confidence degradation?                                  │
│      • Critical step failure?                                   │
│      → IF TRIGGERED: Switch to collaborative mode               │
│                                                                  │
│  2.3 Log Progress                                               │
│      Record to progress.json:                                   │
│      • task_id, step_id, status                                 │
│      • method_used (primary/backup[n])                          │
│      • retry_count, timestamp, mode                             │
│      • error_propagation_decisions                              │
└─────────────────────────────────────────────────────────────────┘
      │
      │ [ALL TASKS COMPLETE]
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  SECTION 6: Post-Execution Analysis                             │
│  ──────────────────────────────                                 │
│  6.1 Failure Pattern Analysis                                   │
│      • Which steps frequently fail?                             │
│      • Which backups work best?                                 │
│      • Overall failure rate?                                    │
│                                                                  │
│  6.2 Constitutional Compliance Review                           │
│      • Article VI: Was critical balance appropriate?            │
│      • Article VII: Were backups effective alternatives?        │
│      • Article VIII: Did error propagation work?                │
│      • Article IX: Were mode escalations appropriate?           │
│      • Article X: Is logging complete?                          │
│      → Compliance score (0-100)                                 │
│                                                                  │
│  6.3 Append Analysis to progress.json                           │
│                                                                  │
│  6.4 Completion Verification (MANDATORY)                        │
│      ┌──────────────────────────────────────────┐              │
│      │ Universal Checks (ALL goals):            │              │
│      │ ✓ Primary deliverable exists?            │              │
│      │ ✓ Quality standards met?                 │              │
│      │ ✓ Verification method passed?            │              │
│      │                                           │              │
│      │ Additional for Build Goals:              │              │
│      │ ✓ Deployment artifact exists?            │              │
│      │   (exe, web app, package, etc.)          │              │
│      │ ✓ User interface implemented?            │              │
│      │   (if user_interface.required = true)    │              │
│      │ ✓ Production ready?                      │              │
│      │   (real APIs, not test mode)             │              │
│      │ ✓ User documentation exists?             │              │
│      │   (if "for [users]" in goal)             │              │
│      └──────────────────────────────────────────┘              │
│                                                                  │
│  Status Assignment:                                             │
│  ✅ ACHIEVED: All applicable checks PASS                        │
│  ⚠️ PARTIAL: Core works but deployment/quality incomplete       │
│  ❌ NOT ACHIEVED: Core deliverable missing/broken               │
└─────────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  COMPLETION                                                      │
│  ──────────                                                      │
│  • Final status logged to progress.json                         │
│  • Recommendations for future SPECs generated                   │
│  • User notified of completion status                           │
│                                                                  │
│  ✅ EXECUTION COMPLETE                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Decision Points

### 1. Project Detection (Step 1a)
**When:** Commander starts - first action  
**How:** Scans `Specs/` for 8-character DNA folders [A,T,G,C]  
**Options:** Load existing / Create new / Skip  
**Purpose:** Determine if continuing existing project or starting new

### 2. Mandatory Human Review (Step 3)
**When:** After high-level structure drafted, before detailed steps  
**Why:** Catch structural issues early, prevent wasted effort  
**Options:** Approve / Revise / Clarify  
**Can't skip:** No silent mode allowed

### 3. User Mode Selection (Execution Section 1.2a)
**When:** After initialization, before validation  
**Options:** Dynamic (default) / Silent / Collaborative  
**Default:** Dynamic (balances autonomy with safety)

### 4. Dynamic Mode Escalation (Execution Section 2.2)
**When:** During step execution  
**Triggers:** Consecutive failures, backup depletion, critical failure  
**Action:** Auto-escalate to collaborative mode

### 5. Completion Verification (Execution Section 6.4)
**When:** Before marking goal ACHIEVED  
**Checks:** Universal (all goals) + Build-specific (if applicable)  
**Prevents:** Marking incomplete systems as complete

---

## File Flow

```
┌────────────────────┐
│ User provides goal │
└──────────┬─────────┘
           │
     ┌─────▼─────┐
     │ Commander │ (generates)
     └─────┬─────┘
           │
     ┌─────▼──────────────────────────────┐
     │ SPEC Files (3):                    │
     │ • spec_[descriptor].md             │
     │ • parameters_[descriptor].toml     │
     │ • exe_[descriptor].md              │
     └─────┬──────────────────────────────┘
           │
     ┌─────▼─────┐
     │    Exe    │ (executes)
     └─────┬─────┘
           │
     ┌─────▼──────────────────────────────┐
     │ progress_[descriptor].json         │
     │ (runtime log + completion status)  │
     └────────────────────────────────────┘
```

---

## Governance Hierarchy

```
┌─────────────────────────────────────┐
│  System Constitution (immutable)    │
│  Articles I-XIV                     │
│  __SPEC_Engine/_Constitution/       │
└──────────────┬──────────────────────┘
               │ governs
        ┌──────▼──────┐
        │  Commander  │
        │  generates  │
        └──────┬──────┘
               │
        ┌──────▼────────────────────────┐
        │  Project Constitution         │
        │  (optional, per DNA)          │
        │  Specs/[DNA_CODE]/            │
        │  project_constitution.toml    │
        └──────┬────────────────────────┘
               │ configures
        ┌──────▼──────┐
        │ Individual  │
        │    SPEC     │
        └─────────────┘
```

---

## File System Requirements

### Expected Directory Structure

The SPEC Engine assumes the following workspace organisation:

```
[Your Workspace Root]/
│
├── __SPEC_Engine/               # Framework files (this directory)
│   ├── README.md
│   ├── WORKFLOW_DIAGRAM.md
│   ├── COHERENCE_REVIEW.md
│   ├── GETTING_STARTED.md
│   │
│   ├── _Constitution/
│   │   ├── constitution.md
│   │   └── DESIGN_PHILOSOPHY.md
│   │
│   ├── _Commander_SPEC/
│   │   └── Spec_Commander.md
│   │
│   ├── _DNA/
│   │   └── DNA_SPEC.md
│   │
│   └── _templates/
│       ├── Spec_template.md
│       ├── parameters_template.toml
│       └── exe_template.md
│
└── SPECs/                       # Generated specifications (created by Commander)
    │
    ├── [DNA_CODE_1]/            # Project 1 (e.g., ATGCTCGA)
    │   │
    │   ├── project_constitution.toml  # Project configuration
    │   │
    │   ├── spec_[descriptor_1]/       # First spec for this project
    │   │   ├── spec_[descriptor_1].md
    │   │   ├── parameters_[descriptor_1].toml
    │   │   ├── exe_[descriptor_1].md
    │   │   └── progress_[descriptor_1].json  # Runtime log
    │   │
    │   └── spec_[descriptor_2]/       # Second spec for this project
    │       ├── spec_[descriptor_2].md
    │       ├── parameters_[descriptor_2].toml
    │       ├── exe_[descriptor_2].md
    │       └── progress_[descriptor_2].json
    │
    └── [DNA_CODE_2]/            # Project 2 (e.g., TGCAATGC)
        ├── project_constitution.toml
        └── spec_[descriptor]/
            └── ...
```

### Path Conventions

**Framework Files:**
- Root: `__SPEC_Engine/`
- Constitution: `__SPEC_Engine/_Constitution/constitution.md`
- Commander: `__SPEC_Engine/_Commander_SPEC/Spec_Commander.md`
- DNA Interview: `__SPEC_Engine/_DNA/DNA_SPEC.md`
- Templates: `__SPEC_Engine/_templates/[template_name]`

**Generated Specs:**
- Root: `SPECs/`
- Project folder: `SPECs/[DNA_CODE]/` (8 characters, A/T/G/C only)
- Project config: `SPECs/[DNA_CODE]/project_constitution.toml`
- Spec folder: `SPECs/[DNA_CODE]/spec_[descriptor]/`
- Spec files: `SPECs/[DNA_CODE]/spec_[descriptor]/[spec|parameters|exe|progress]_[descriptor].[md|toml|json]`

### DNA Code Format

- **Length:** Exactly 8 characters
- **Alphabet:** A, T, G, C only (DNA nucleotides)
- **Generation:** Hash of project name, mapped to genetic code
- **Examples:** `ATGCTCGA`, `TGCAATGC`, `GCATTACG`
- **Uniqueness:** Project name determines DNA code consistently

### File Naming Conventions

| Component | Format | Example |
|-----------|--------|---------|
| Spec markdown | `spec_[descriptor].md` | `spec_charity_pos.md` |
| Parameters TOML | `parameters_[descriptor].toml` | `parameters_charity_pos.toml` |
| Execution controller | `exe_[descriptor].md` | `exe_charity_pos.md` |
| Progress log | `progress_[descriptor].json` | `progress_charity_pos.json` |
| Project config | `project_constitution.toml` | `project_constitution.toml` |

**Descriptor:** Single word summarising the goal (e.g., `research`, `debug`, `prototype`, `charity_pos`, `ecommerce`)

### Workspace Root Detection

The system assumes it's running from a workspace where:
1. `__SPEC_Engine/` directory exists at the root
2. `SPECs/` directory exists (or will be created) at the root
3. All paths are relative to this workspace root

**Cross-references in files** use these assumptions:
- Commander references: `__SPEC_Engine/_templates/Spec_template.md`
- Constitution references: `__SPEC_Engine/_Constitution/constitution.md`
- Spec references: `SPECs/[DNA_CODE]/spec_[descriptor]/`

### File Creation Rules

**Framework files (read-only):**
- Never modified by Commander or Exe
- Updated only during system maintenance
- Serve as templates and governance

**Project constitution (created once, updated rarely):**
- Created by DNA_SPEC.md interview
- Updated when project requirements change
- Shared across all specs in DNA folder

**Spec files (created per goal):**
- Generated by Spec_Commander.md
- Three files created simultaneously (spec, parameters, exe)
- Progress log created at runtime

**Runtime files (auto-generated):**
- `progress_[descriptor].json` created on first execution
- Append-only (never modified, only appended)
- Immutable after completion

### Permissions Assumptions

The system assumes it has permission to:
- Read all files in `__SPEC_Engine/`
- Create directories in `SPECs/`
- Create/read/append files in `SPECs/[DNA_CODE]/`
- Create spec folders in `SPECs/[DNA_CODE]/spec_[descriptor]/`

**No permission required for:**
- Modifying framework files (system never does this)
- Deleting any files (system preserves all logs and specs)

---

## Time Estimates

| Phase | Duration | Notes |
|-------|----------|-------|
| Step 1: Project Setup | 1-3 min | DNA detection + context + folder prep |
| Step 2: Draft Structure | 2-5 min | Depends on goal complexity |
| Step 3: Human Review | 1-10 min | User review time |
| Step 4: Generate Files | 3-10 min | Includes detailed steps |
| Step 5: Validation | 1-2 min | Automated checks |
| Step 6: Output | <1 min | File write |
| **Total Generation** | **8-31 min** | **Average: ~20 min** |
| Execution Section 1: Init | 1-2 min | Validation + mode selection |
| Execution Section 2: Tasks | Variable | Depends on goal complexity |
| Execution Section 6: Analysis | 2-5 min | Post-execution review |

---

## Success Metrics

| Metric | Target | Measured By |
|--------|--------|-------------|
| Goal singularity | 100% | Article I compliance |
| Critical balance | 40-60% | Article VI compliance |
| Spec completion rate | >90% | Execution Section 6.4 verification |
| Human review catch rate | N/A | Issues found at Step 3 |
| Execution failures | <20% | progress.json analysis |
| Article XIV compliance | 100% | For build goals |
| DNA profile adoption | >80% | Projects using project_constitution.toml |

---

**End of Workflow Diagram**


```

```markdown
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  STEP 3a: MANDATORY HUMAN REVIEW & TOOL INSTALLATION (NEW)    ┃
┃  ════════════════════════════════════════════════════         ┃
┃  🚨 NO SILENT MODE ALLOWED - SINGLE PAUSE POINT 🚨             ┃
┃                                                                 ┃
┃  ┌──────────────────────────────────────────────────────────┐ ┃
┃  │ PHASE 1: Present Complete Proposal                       │ ┃
┃  └──────────────────────────────────────────────────────────┘ ┃
┃                                                                 ┃
┃  Commander presents:                                           ┃
┃  • Goal statement                                              ┃
┃  • Definition of complete                                      ┃
┃  • Software stack (if build goal)                              ┃
┃  • MCP Toolset (REQUIRED/RECOMMENDED/OPTIONAL) ← NEW          ┃
┃  • High-level tasks (2-5)                                      ┃
┃  • Estimated complexity                                        ┃
┃                                                                 ┃
┃  ┌──────────────────────────────────────────────────┐         ┃
┃  │ USER REVIEWS AND SELECTS:                         │         ┃
┃  │                                                    │         ┃
┃  │ [A] APPROVE structure & toolset → Install now     │         ┃
┃  │ [R] REVISE structure or toolset                   │         ┃
┃  │ [T] MODIFY tools only                             │         ┃
┃  │ [C] CLARIFY questions                             │         ┃
┃  │                                                    │         ┃
┃  │ IF [R] or [T]: Loop until satisfied, then [A]     │         ┃
┃  │ IF [C]: Answer, re-present, get [A]              │         ┃
┃  └──────────────────────────────────────────────────┘         ┃
┃                                                                 ┃
┃  ┌──────────────────────────────────────────────────────────┐ ┃
┃  │ PHASE 2: Tool Installation (After [A] Approved)          │ ┃
┃  └──────────────────────────────────────────────────────────┘ ┃
┃                                                                 ┃
┃  Commander displays installation instructions:                 ┃
┃  ✓ Lists all REQUIRED tools with install commands             ┃
┃  ✓ Lists RECOMMENDED tools (optional)                          ┃
┃  ✓ Lists OPTIONAL tools (if desired)                           ┃
┃  ✓ Shows MCP config file locations (OS-specific)               ┃
┃  ✓ Reminds to restart MCP client                               ┃
┃                                                                 ┃
┃  ┌──────────────────────────────────────────────────┐         ┃
┃  │ HUMAN INSTALLS TOOLS NOW                          │         ┃
┃  │                                                    │         ┃
┃  │ 1. Run install commands in terminal               │         ┃
┃  │ 2. Configure MCP client config file               │         ┃
┃  │ 3. Restart MCP client                             │         ┃
┃  │ 4. Test availability (optional)                   │         ┃
┃  └──────────────────────────────────────────────────┘         ┃
┃                                                                 ┃
┃  ┌──────────────────────────────────────────────────────────┐ ┃
┃  │ PHASE 3: Confirm Installation                            │ ┃
┃  └──────────────────────────────────────────────────────────┘ ┃
┃                                                                 ┃
┃  ┌──────────────────────────────────────────────────┐         ┃
┃  │ USER CONFIRMS:                                    │         ┃
┃  │                                                    │         ┃
┃  │ [Y] Tools installed → Proceed to Step 4           │         ┃
┃  │ [N] Installation failed → Troubleshoot            │         ┃
┃  │ [S] Skip (not recommended) → Warning + proceed    │         ┃
┃  │                                                    │         ┃
┃  │ IF [N]: Help troubleshoot, loop until [Y]         │         ┃
┃  │ IF [S]: Warn about Section 1.11 verification      │         ┃
┃  └──────────────────────────────────────────────────┘         ┃
┃                                                                 ┃
┃  ✅ EXIT: Single pause point complete                          ┃
┃  ✅ Structure approved + Tools installed                       ┃
┃  ✅ Ready for detailed SPEC generation                         ┃
┃                                                                 ┃
┃  Rationale:                                                    ┃
┃  • Catch structural issues BEFORE detailed generation          ┃
┃  • Ensure tools ready BEFORE execution                         ┃
┃  • Single pause = smoother workflow                            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

```markdown
# SPEC Engine Workflow Diagram

**Complete lifecycle from goal to execution to completion**

---

## High-Level Overview

```
USER GOAL → SPEC GENERATION → HUMAN REVIEW → FILE GENERATION → VALIDATION → EXECUTION → VERIFICATION → COMPLETE
```

---

## System Architecture Diagram

### Complete SPEC Engine Ecosystem

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                              SPEC ENGINE ARCHITECTURE                         │
└───────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                                  USER LAYER                                     │
│  ┌─────────────┐        ┌──────────────┐        ┌─────────────────┐           │
│  │   Define    │        │   Review &   │        │   Monitor       │           │
│  │   Goal      │───────▶│   Approve    │───────▶│   Execution     │           │
│  └─────────────┘        └──────────────┘        └─────────────────┘           │
└─────────────────────────────────────────────────────────────────────────────────┘
         │                         │                         │
         ▼                         ▼                         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FRAMEWORK LAYER                                    │
│                          (__SPEC_Engine directory)                              │
│                                                                                 │
│  ┌────────────────────┐           ┌─────────────────────┐                     │
│  │   CONSTITUTIONAL   │           │      GENERATION      │                     │
│  │      LAYER         │           │        LAYER         │                     │
│  │                    │           │                      │                     │
│  │  ┌──────────────┐  │           │  ┌───────────────┐  │                     │
│  │  │constitution  │  │◀──governs──│  │  Commander    │  │                     │
│  │  │    .md       │  │           │  │  Spec.md      │  │                     │
│  │  │              │  │           │  └───────┬───────┘  │                     │
│  │  │ 14 Articles  │  │           │          │          │                     │
│  │  └──────────────┘  │           │          ▼          │                     │
│  │                    │           │  ┌───────────────┐  │                     │
│  │  ┌──────────────┐  │           │  │   Templates   │  │                     │
│  │  │  DESIGN_     │  │           │  │               │  │                     │
│  │  │  PHILOSOPHY  │  │           │  │ • Spec.md     │  │                     │
│  │  │    .md       │  │           │  │ • params.toml │  │                     │
│  │  │              │  │           │  │ • exe.md      │  │                     │
│  │  │ Rationale    │  │           │  └───────────────┘  │                     │
│  │  └──────────────┘  │           │                      │                     │
│  └────────────────────┘           └──────────────────────┘                     │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────┐                  │
│  │               CONFIGURATION LAYER                        │                  │
│  │                                                           │                  │
│  │              ┌──────────────────────┐                    │                  │
│  │              │     DNA_SPEC.md      │                    │                  │
│  │              │                      │                    │                  │
│  │              │  5-Question          │                    │                  │
│  │              │  Interview           │                    │                  │
│  │              └──────────┬───────────┘                    │                  │
│  │                         │                                │                  │
│  │                         ▼                                │                  │
│  │              ┌──────────────────────┐                    │                  │
│  │              │  project_            │                    │                  │
│  │              │  constitution.toml   │                    │                  │
│  │              │                      │                    │                  │
│  │              │  • Risk level        │                    │                  │
│  │              │  • Test strategy     │                    │                  │
│  │              │  • Execution mode    │                    │                  │
│  │              │  • Backend prefs     │                    │                  │
│  │              └──────────────────────┘                    │                  │
│  └─────────────────────────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ generates
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SPECIFICATION LAYER                                │
│                           (SPECs/[DNA_CODE]/spec_[descriptor]/)                 │
│                                                                                 │
│  ┌─────────────────────┐   ┌──────────────────────┐   ┌────────────────────┐  │
│  │  spec_[desc].md     │   │ parameters_[desc]    │   │  exe_[desc].md     │  │
│  │                     │   │       .toml          │   │                    │  │
│  │  Human Story        │◀─▶│                      │   │  Executor Logic    │  │
│  │                     │   │  Machine Config      │◀─▶│                    │  │
│  │  • Goal             │   │                      │   │  • Validation      │  │
│  │  • Tasks            │   │  • Task structure    │   │  • Execution flow  │  │
│  │  • Steps            │   │  • Flags & settings  │   │  • Mode control    │  │
│  │  • Backups          │   │  • Expected outputs  │   │  • Analysis        │  │
│  │  • Reasoning        │   │  • Constraints       │   │  • Verification    │  │
│  └─────────────────────┘   └──────────────────────┘   └─────────┬──────────┘  │
│                                                                  │             │
│                                                                  │ executes    │
└──────────────────────────────────────────────────────────────────┼─────────────┘
                                                                   │
                                                                   ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              EXECUTION LAYER                                    │
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                          INITIALIZATION PHASE                             │  │
│  │  ┌──────────────┐  ┌───────────────┐  ┌──────────────┐  ┌────────────┐  │  │
│  │  │ File Check   │─▶│ Parse Files   │─▶│  Validation  │─▶│ Mode       │  │  │
│  │  │ (Section 1.1)│  │ (Section 1.3) │  │ (1.4-1.10)   │  │ Selection  │  │  │
│  │  └──────────────┘  └───────────────┘  └──────────────┘  └────────────┘  │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                       │                                         │
│                                       ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                          EXECUTION PHASE                                  │  │
│  │                                                                            │  │
│  │  FOR EACH TASK (sequential):                                              │  │
│  │  ┌────────────────────────────────────────────────────────────────────┐  │  │
│  │  │  ┌──────────────┐       ┌──────────────┐      ┌────────────────┐  │  │  │
│  │  │  │Constitutional│       │   Execute    │      │  Dynamic Mode  │  │  │  │
│  │  │  │    Check     │──────▶│   Steps      │─────▶│  Evaluation    │  │  │  │
│  │  │  │ (Section 2.0)│       │ (Section 2.1)│      │ (Section 2.2)  │  │  │  │
│  │  │  └──────────────┘       └──────┬───────┘      └────────────────┘  │  │  │
│  │  │                                 │                                   │  │  │
│  │  │         FOR EACH STEP:          ▼                                   │  │  │
│  │  │         ┌─────────────────────────────────────────┐                │  │  │
│  │  │         │  1. Read prior outcomes (error prop)    │                │  │  │
│  │  │         │  2. Attempt PRIMARY method              │                │  │  │
│  │  │         │  3. If fail → Try BACKUP [1]            │                │  │  │
│  │  │         │  4. If fail → Try BACKUP [2]            │                │  │  │
│  │  │         │  5. If critical + all fail → Escalate   │                │  │  │
│  │  │         │  6. Log to progress.json                │                │  │  │
│  │  │         └─────────────────────────────────────────┘                │  │  │
│  │  └────────────────────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                       │                                         │
│                                       ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                      POST-EXECUTION ANALYSIS                              │  │
│  │  ┌───────────────┐  ┌─────────────────┐  ┌─────────────────────────┐    │  │
│  │  │   Failure     │  │  Constitutional │  │   Completion            │    │  │
│  │  │   Pattern     │─▶│   Compliance    │─▶│   Verification          │    │  │
│  │  │   Analysis    │  │   Review        │  │   (Section 6.4)         │    │  │
│  │  │ (Section 6.1) │  │ (Section 6.2)   │  │                         │    │  │
│  │  └───────────────┘  └─────────────────┘  └────────┬────────────────┘    │  │
│  └────────────────────────────────────────────────────┼───────────────────────┘│
└─────────────────────────────────────────────────────────┼─────────────────────┘
                                                          │
                                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PERSISTENCE LAYER                                  │
│                                                                                 │
│              ┌────────────────────────────────────────────────┐                │
│              │      progress_[descriptor].json                │                │
│              │                                                │                │
│              │  Immutable append-only log containing:         │                │
│              │  • All step outcomes                           │                │
│              │  • Methods attempted (primary/backup)          │                │
│              │  • Retry counts and mode switches              │                │
│              │  • Error propagation decisions                 │                │
│              │  • Constitutional compliance tracking          │                │
│              │  • Post-execution analysis                     │                │
│              │  • Final goal achievement status               │                │
│              │                                                │                │
│              │  STATUS: ACHIEVED | PARTIAL | NOT_ACHIEVED     │                │
│              └────────────────────────────────────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────────┘

LEGEND:
  ──▶  Data flow / Process flow
  ◀─▶  Bidirectional synchronisation / Cross-reference
  │    Sequential relationship
  ═══  Constitutional governance
```

### Key Architectural Principles

1. **Separation of Concerns:**
   - Constitutional: Immutable governance (Articles I-XIV)
   - Generation: Commander creates specs from templates
   - Configuration: Optional project-level settings (DNA)
   - Specification: Three synchronized files per goal
   - Execution: Validation → Execution → Analysis → Verification
   - Persistence: Immutable audit trail

2. **Hierarchical Governance:**
   ```
   System Constitution (immutable)
        ↓ governs
   Project Constitution (per-project, optional)
        ↓ configures
   Individual SPEC (per-goal, required)
        ↓ executed by
   Executor (validates, executes, verifies)
        ↓ produces
   Progress Log (immutable audit trail)
   ```

3. **Validation Checkpoints:**
   - **Pre-Generation:** Commander validates constitutional compliance
   - **Pre-Execution:** Exe Section 1 validates files and structure
   - **Runtime:** Exe Section 2.0 checks compliance per task
   - **Post-Execution:** Exe Section 6.2 reviews adherence
   - **Completion:** Exe Section 6.4 verifies goal achievement

4. **Error Handling Layers:**
   - **Step Level:** Primary → Backup[1] → Backup[2]
   - **Task Level:** Error propagation between steps
   - **SPEC Level:** Dynamic mode escalation to collaborative
   - **System Level:** Constitutional violation tracking

---

## Detailed Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SPEC GENERATION PHASE                       │
└─────────────────────────────────────────────────────────────────────┘

[USER INPUT TO LLM]
  │
  ├─→ "Launch SPEC Commander to build a charity shop POS system for volunteers"
  └─→ "Launch SPEC Commander with 'Specs/[DNA_CODE]' to continue SPEC development to analyse user sentiment in 10k product reviews"
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: Project Setup & Initialization                         │
│  ──────────────────────────────────                             │
│  Run Spec_Commander.md                                          │
└─────────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1a: Project Profile Detection                             │
│  ──────────────────────────────                                 │
│  Commander checks: Does DNA folder exist in Specs/?             │
│  (Scans for 8-char folders [A,T,G,C] with project_constitution.toml)
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐       │
│  │ IF FOUND:                                            │       │
│  │ ✅ Load existing project_constitution.toml          │       │
│  │ Display: "Using project: [NAME] (DNA: [CODE])"      │       │
│  │ → Proceed to Step 1b                                │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐       │
│  │ IF NOT FOUND:                                        │       │
│  │ ⚠️ Prompt user:                                      │       │
│  │   [A] Create profile now (invokes DNA_SPEC.md)      │       │
│  │   [B] Skip - use system defaults                    │       │
│  │   [C] Enter existing DNA code                       │       │
│  │                                                       │       │
│  │ IF [A]: Commander invokes DNA_SPEC.md:              │       │
│  │   Q1: What are you trying to achieve?               │       │
│  │   Q2: How will you measure success?                 │       │
│  │   Q3: Critical risks/constraints?                   │       │
│  │   Q4: Required software stack?                      │       │
│  │   Q5: Preferred approach to failures?               │       │
│  │   → Generates DNA code (e.g., ATGCATGC)             │       │
│  │   → Creates Specs/[DNA_CODE]/project_constitution.toml     │
│  │   → Returns to Commander                            │       │
│  │                                                       │       │
│  │ IF [B]: Continue with system defaults only          │       │
│  │ IF [C]: Validate & load specified DNA code          │       │
│  └─────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1b: Context Loading                                       │
│  ────────────────────────                                       │
│  Commander reads:                                               │
│  • DESIGN_PHILOSOPHY.md (principles, patterns, anti-patterns)   │
│  • constitution.md (Articles I-XIV, governance rules)           │
│  • project_constitution.toml (if DNA profile exists)            │
└─────────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1c: Folder Preparation                                    │
│  ───────────────────────────                                    │
│  Create: Specs/[DNA_CODE]/spec_[descriptor]/                    │
│  Placeholder for 3 files + progress.json                        │
└─────────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: Draft High-Level Structure                             │
│  ──────────────────────────────                                 │
│  Commander analyses goal and drafts:                            │
│  ✓ Goal (singular, clear, measurable)                           │
│  ✓ Definition of Complete (what exists + how to verify)        │
│  ✓ Tasks (2-5 high-level objectives)                            │
│  ✓ Software Stack (if build/create goal)                        │
│  ✓ Estimated complexity                                         │
│                                                                  │
│  ⚠ NO DETAILED STEPS YET                                        │
└─────────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2.5: MCP Tool Analysis (NEW)                              │
│  ──────────────────────────────                                 │
│  Commander examines goal and recommends MCP tools:              │
│                                                                  │
│  1. Load: __SPEC_Engine/_tools/mcp_tools_catalog.yaml          │
│     (269 servers, 2900+ tools, 24 categories)                   │
│                                                                  │
│  2. Analyse goal characteristics autonomously:                  │
│     - What activity? (build, analyse, research, etc.)           │
│     - What resources? (files, databases, APIs, etc.)            │
│     - What outputs? (code, reports, data, etc.)                 │
│     - What scale? (script, app, pipeline, system)               │
│                                                                  │
│  3. Identify relevant tool categories                           │
│     - Review 24 categories in catalog                           │
│     - Consider full lifecycle (not just primary task)           │
│     - Think cross-functionally                                  │
│                                                                  │
│  4. Evaluate and classify individual tools:                     │
│     ✓ REQUIRED: Goal cannot be achieved without                 │
│     ✓ RECOMMENDED: Significantly improves efficiency            │
│     ✓ OPTIONAL: Nice to have, enhances workflow                 │
│                                                                  │
│  5. Document rationale for each tool selection                  │
│                                                                  │
│  Output: MCP Toolset recommendations (added to proposal)        │
└─────────────────────────────────────────────────────────────────┘
      │
      ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  STEP 3a: MANDATORY HUMAN REVIEW & TOOL INSTALLATION (NEW)    ┃
┃  ════════════════════════════════════════════════════         ┃
┃  🚨 NO SILENT MODE - SINGLE PAUSE POINT 🚨                     ┃
┃                                                                 ┃
┃  ┌──────────────────────────────────────────────────────────┐ ┃
┃  │ PHASE 1: Present Complete Proposal                       │ ┃
┃  └──────────────────────────────────────────────────────────┘ ┃
┃                                                                 ┃
┃  ┌─────────────────────────────────────────────┐               ┃
┃  │ SPEC PROPOSAL FOR REVIEW                    │               ┃
┃  │                                              │               ┃
┃  │ Goal: [singular statement]                  │               ┃
┃  │                                              │               ┃
┃  │ Definition of Complete:                     │               ┃
┃  │ • Primary deliverable: [...]                │               ┃
┃  │ • Quality standards: [...]                  │               ┃
┃  │ • Verification method: [...]                │               ┃
┃  │                                              │               ┃
┃  │ MCP Toolset: (NEW)                          │               ┃
┃  │ REQUIRED (2): postgres, github              │               ┃
┃  │ RECOMMENDED (1): playwright                 │               ┃
┃  │ OPTIONAL (1): notion                        │               ┃
┃  │                                              │               ┃
┃  │ Tasks:                                       │               ┃
┃  │ 1. [High-level objective]                   │               ┃
┃  │ 2. [High-level objective]                   │               ┃
┃  │ 3. [High-level objective]                   │               ┃
┃  │                                              │               ┃
┃  │ Software Stack: (if applicable)             │               ┃
┃  │ • Deployment type: desktop_app              │               ┃
┃  │ • Language: Python                          │               ┃
┃  │ • UI: PyQt5 GUI                             │               ┃
┃  │ • Packaging: PyInstaller                    │               ┃
┃  └─────────────────────────────────────────────┘               ┃
┃                                                                 ┃
┃  User Options:                                                  ┃
┃  [A] APPROVE → I will install tools now                        ┃
┃  [R] REVISE structure or toolset                               ┃
┃  [T] MODIFY tools only                                         ┃
┃  [C] CLARIFY → Ask questions                                   ┃
┃                                                                 ┃
┃  IF [R]/[T]: Loop until satisfied, then [A]                    ┃
┃  IF [C]: Answer, re-present, get [A]                           ┃
┃                                                                 ┃
┃  ⏸ EXECUTION PAUSED UNTIL USER RESPONDS                        ┃
┃                                                                 ┃
┃  ┌──────────────────────────────────────────────────────────┐ ┃
┃  │ PHASE 2: Installation (After [A] Approved)               │ ┃
┃  └──────────────────────────────────────────────────────────┘ ┃
┃                                                                 ┃
┃  Commander displays:                                            ┃
┃  ✅ Structure & Toolset Approved                               ┃
┃                                                                 ┃
┃  REQUIRED Tools (must install):                                ┃
┃  1. postgres: npm install @modelcontextprotocol/...            ┃
┃  2. github: npm install @modelcontextprotocol/...              ┃
┃                                                                 ┃
┃  RECOMMENDED Tools (optional):                                 ┃
┃  3. playwright: npm install @modelcontextprotocol/...          ┃
┃                                                                 ┃
┃  Instructions:                                                  ┃
┃  1. Run install commands in terminal                           ┃
┃  2. Configure MCP client config (OS-specific path shown)       ┃
┃  3. Restart MCP client                                         ┃
┃  4. Test (optional)                                            ┃
┃                                                                 ┃
┃  ┌────────────────────────────────────┐                        ┃
┃  │ 👤 HUMAN INSTALLS TOOLS NOW        │                        ┃
┃  └────────────────────────────────────┘                        ┃
┃                                                                 ┃
┃  ┌──────────────────────────────────────────────────────────┐ ┃
┃  │ PHASE 3: Confirm Installation                            │ ┃
┃  └──────────────────────────────────────────────────────────┘ ┃
┃                                                                 ┃
┃  [Y] Installed → Proceed to Step 4                             ┃
┃  [N] Failed → Troubleshoot, loop                               ┃
┃  [S] Skip → Warning + proceed (not recommended)                ┃
┃                                                                 ┃
┃  ⏸ EXECUTION PAUSED UNTIL [Y] CONFIRMED                        ┃
┃                                                                 ┃
┃  ✅ EXIT: Structure approved + Tools installed                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
      │
      │ [USER CONFIRMED INSTALLATION]
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: Generate Detailed Steps and Files                      │
│  ─────────────────────────────────────                          │
│  NOW generate for each approved task:                           │
│  ✓ Concrete steps (1-5 per task)                                │
│  ✓ Backup methods (0-2 per step)                                │
│  ✓ Critical flags (40-60% of steps)                             │
│  ✓ Expected outputs (specific, measurable)                      │
│  ✓ Execution modes (dynamic default)                            │
│                                                                  │
│  Generate 3 files:                                              │
│  ▸ spec_[descriptor].md (human-readable)                        │
│  ▸ parameters_[descriptor].toml (machine-readable)              │
│  ▸ exe_[descriptor].md (execution controller)                   │
└─────────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 5: Pre-Flight Validation                                  │
│  ─────────────────────────                                      │
│  5a. Constitutional Compliance Check                            │
│      • Article I: Goal singular?                                │
│      • Article II: 2-5 tasks, 1-5 steps per task?               │
│      • Article VI: 40-60% critical balance?                     │
│      • Article XIV: Software stack defined (if build goal)?     │
│                                                                  │
│  5b. Software Stack Validation (if build/create goal)           │
│      • deployment_type defined?                                 │
│      • user_interface.required = true (if "for [users]")?       │
│      • completion_criteria populated?                           │
│                                                                  │
│  5c. Structural Validation                                      │
│      • Tasks decompose goal logically?                          │
│      • Steps are concrete actions?                              │
│      • Backups are alternatives (not retries)?                  │
│                                                                  │
│  5d. Quality Gates                                              │
│      ✅ PASS: All checks green → Proceed                        │
│      ❌ FAIL: Violations found → HALT, request fixes            │
└─────────────────────────────────────────────────────────────────┘
      │
      │ [VALIDATION PASS]
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 6: Output Complete SPEC                                   │
│  ────────────────────────────                                   │
│  Specs/[DNA_CODE]/spec_[descriptor]/                            │
│  ├── spec_[descriptor].md                                       │
│  ├── parameters_[descriptor].toml                               │
│  ├── exe_[descriptor].md                                        │
│  └── progress_[descriptor].json (created at runtime)            │
│                                                                  │
│  ✅ SPEC GENERATION COMPLETE                                    │
└─────────────────────────────────────────────────────────────────┘

═════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────┐
│                          EXECUTION PHASE                             │
│                     (exe_[descriptor].md Process)                    │
└─────────────────────────────────────────────────────────────────────┘

[USER INVOKES EXECUTION IN LLM]
  │
  └─→ "Run spec_[descriptor]" or "Execute SPEC"
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  SECTION 1: Initialization and Validation                       │
│  ────────────────────────────────────                           │
│  1.1  File presence check                                       │
│  1.1a Software Stack Validation (if build goal)                 │
│  1.2  Initialize progress.json                                  │
│  1.2a USER MODE SELECTION (Dynamic/Silent/Collaborative)        │
│  1.3  Parse spec.md and parameters.toml                         │
│  1.4  Validate goal                                             │
│  1.5  Validate tasks                                            │
│  1.6  Validate steps                                            │
│  1.7  Validate backups                                          │
│  1.8  Bridging verification (Markdown ↔ TOML sync)              │
│  1.9  Validate components and constraints                       │
│  1.10 Final pre-flight check                                    │
│                                                                  │
│  ✅ IF PASS: Proceed to Section 2                               │
│  ❌ IF FAIL: HALT, log errors, escalate to collaborative        │
└─────────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  SECTION 2: Execution Flow (Per Task)                           │
│  ────────────────────────────                                   │
│  FOR EACH TASK (sequentially):                                  │
│                                                                  │
│  2.0 Constitutional Compliance Check (per task)                 │
│      • Article IV: Error propagation enabled?                   │
│      • Article VI: Critical balance appropriate?                │
│      • Article VIII: Prior step outcomes read?                  │
│      • Article X: Logging comprehensive?                        │
│                                                                  │
│  2.1 Execute Task Steps (sequentially)                          │
│      FOR EACH STEP:                                             │
│      ┌────────────────────────────────────┐                    │
│      │ • Read progress.json (error prop)  │                    │
│      │ • Execute PRIMARY method           │                    │
│      │ • IF FAIL: Try BACKUP [1]          │                    │
│      │ • IF FAIL: Try BACKUP [2]          │                    │
│      │ • IF FAIL: Escalate (if critical)  │                    │
│      │ • Log outcome to progress.json     │                    │
│      └────────────────────────────────────┘                    │
│                                                                  │
│  2.2 Dynamic Mode Evaluation (per step)                         │
│      Check for escalation triggers:                             │
│      • 3+ consecutive failures?                                 │
│      • Backup depletion pattern?                                │
│      • Confidence degradation?                                  │
│      • Critical step failure?                                   │
│      → IF TRIGGERED: Switch to collaborative mode               │
│                                                                  │
│  2.3 Log Progress                                               │
│      Record to progress.json:                                   │
│      • task_id, step_id, status                                 │
│      • method_used (primary/backup[n])                          │
│      • retry_count, timestamp, mode                             │
│      • error_propagation_decisions                              │
└─────────────────────────────────────────────────────────────────┘
      │
      │ [ALL TASKS COMPLETE]
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  SECTION 6: Post-Execution Analysis                             │
│  ──────────────────────────────                                 │
│  6.1 Failure Pattern Analysis                                   │
│      • Which steps frequently fail?                             │
│      • Which backups work best?                                 │
│      • Overall failure rate?                                    │
│                                                                  │
│  6.2 Constitutional Compliance Review                           │
│      • Article VI: Was critical balance appropriate?            │
│      • Article VII: Were backups effective alternatives?        │
│      • Article VIII: Did error propagation work?                │
│      • Article IX: Were mode escalations appropriate?           │
│      • Article X: Is logging complete?                          │
│      → Compliance score (0-100)                                 │
│                                                                  │
│  6.3 Append Analysis to progress.json                           │
│                                                                  │
│  6.4 Completion Verification (MANDATORY)                        │
│      ┌──────────────────────────────────────────┐              │
│      │ Universal Checks (ALL goals):            │              │
│      │ ✓ Primary deliverable exists?            │              │
│      │ ✓ Quality standards met?                 │              │
│      │ ✓ Verification method passed?            │              │
│      │                                           │              │
│      │ Additional for Build Goals:              │              │
│      │ ✓ Deployment artifact exists?            │              │
│      │   (exe, web app, package, etc.)          │              │
│      │ ✓ User interface implemented?            │              │
│      │   (if user_interface.required = true)    │              │
│      │ ✓ Production ready?                      │              │
│      │   (real APIs, not test mode)             │              │
│      │ ✓ User documentation exists?             │              │
│      │   (if "for [users]" in goal)             │              │
│      └──────────────────────────────────────────┘              │
│                                                                  │
│  Status Assignment:                                             │
│  ✅ ACHIEVED: All applicable checks PASS                        │
│  ⚠️ PARTIAL: Core works but deployment/quality incomplete       │
│  ❌ NOT ACHIEVED: Core deliverable missing/broken               │
└─────────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│  COMPLETION                                                      │
│  ──────────                                                      │
│  • Final status logged to progress.json                         │
│  • Recommendations for future SPECs generated                   │
│  • User notified of completion status                           │
│                                                                  │
│  ✅ EXECUTION COMPLETE                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Decision Points

### 1. Project Detection (Step 1a)
**When:** Commander starts - first action  
**How:** Scans `Specs/` for 8-character DNA folders [A,T,G,C]  
**Options:** Load existing / Create new / Skip  
**Purpose:** Determine if continuing existing project or starting new

### 2. Mandatory Human Review (Step 3)
**When:** After high-level structure drafted, before detailed steps  
**Why:** Catch structural issues early, prevent wasted effort  
**Options:** Approve / Revise / Clarify  
**Can't skip:** No silent mode allowed

### 3. User Mode Selection (Execution Section 1.2a)
**When:** After initialization, before validation  
**Options:** Dynamic (default) / Silent / Collaborative  
**Default:** Dynamic (balances autonomy with safety)

### 4. Dynamic Mode Escalation (Execution Section 2.2)
**When:** During step execution  
**Triggers:** Consecutive failures, backup depletion, critical failure  
**Action:** Auto-escalate to collaborative mode

### 5. Completion Verification (Execution Section 6.4)
**When:** Before marking goal ACHIEVED  
**Checks:** Universal (all goals) + Build-specific (if applicable)  
**Prevents:** Marking incomplete systems as complete

---

## File Flow

```
┌────────────────────┐
│ User provides goal │
└──────────┬─────────┘
           │
     ┌─────▼─────┐
     │ Commander │ (generates)
     └─────┬─────┘
           │
     ┌─────▼──────────────────────────────┐
     │ SPEC Files (3):                    │
     │ • spec_[descriptor].md             │
     │ • parameters_[descriptor].toml     │
     │ • exe_[descriptor].md              │
     └─────┬──────────────────────────────┘
           │
     ┌─────▼─────┐
     │    Exe    │ (executes)
     └─────┬─────┘
           │
     ┌─────▼──────────────────────────────┐
     │ progress_[descriptor].json         │
     │ (runtime log + completion status)  │
     └────────────────────────────────────┘
```

---

## Governance Hierarchy

```
┌─────────────────────────────────────┐
│  System Constitution (immutable)    │
│  Articles I-XIV                     │
│  __SPEC_Engine/_Constitution/       │
└──────────────┬──────────────────────┘
               │ governs
        ┌──────▼──────┐
        │  Commander  │
        │  generates  │
        └──────┬──────┘
               │
        ┌──────▼────────────────────────┐
        │  Project Constitution         │
        │  (optional, per DNA)          │
        │  Specs/[DNA_CODE]/            │
        │  project_constitution.toml    │
        └──────┬────────────────────────┘
               │ configures
        ┌──────▼──────┐
        │ Individual  │
        │    SPEC     │
        └─────────────┘
```

---

## File System Requirements

### Expected Directory Structure

The SPEC Engine assumes the following workspace organisation:

```
[Your Workspace Root]/
│
├── __SPEC_Engine/               # Framework files (this directory)
│   ├── README.md
│   ├── WORKFLOW_DIAGRAM.md
│   ├── COHERENCE_REVIEW.md
│   ├── GETTING_STARTED.md
│   │
│   ├── _Constitution/
│   │   ├── constitution.md
│   │   └── DESIGN_PHILOSOPHY.md
│   │
│   ├── _Commander_SPEC/
│   │   └── Spec_Commander.md
│   │
│   ├── _DNA/
│   │   └── DNA_SPEC.md
│   │
│   └── _templates/
│       ├── Spec_template.md
│       ├── parameters_template.toml
│       └── exe_template.md
│
└── SPECs/                       # Generated specifications (created by Commander)
    │
    ├── [DNA_CODE_1]/            # Project 1 (e.g., ATGCTCGA)
    │   │
    │   ├── project_constitution.toml  # Project configuration
    │   │
    │   ├── spec_[descriptor_1]/       # First spec for this project
    │   │   ├── spec_[descriptor_1].md
    │   │   ├── parameters_[descriptor_1].toml
    │   │   ├── exe_[descriptor_1].md
    │   │   └── progress_[descriptor_1].json  # Runtime log
    │   │
    │   └── spec_[descriptor_2]/       # Second spec for this project
    │       ├── spec_[descriptor_2].md
    │       ├── parameters_[descriptor_2].toml
    │       ├── exe_[descriptor_2].md
    │       └── progress_[descriptor_2].json
    │
    └── [DNA_CODE_2]/            # Project 2 (e.g., TGCAATGC)
        ├── project_constitution.toml
        └── spec_[descriptor]/
            └── ...
```

### Path Conventions

**Framework Files:**
- Root: `__SPEC_Engine/`
- Constitution: `__SPEC_Engine/_Constitution/constitution.md`
- Commander: `__SPEC_Engine/_Commander_SPEC/Spec_Commander.md`
- DNA Interview: `__SPEC_Engine/_DNA/DNA_SPEC.md`
- Templates: `__SPEC_Engine/_templates/[template_name]`

**Generated Specs:**
- Root: `SPECs/`
- Project folder: `SPECs/[DNA_CODE]/` (8 characters, A/T/G/C only)
- Project config: `SPECs/[DNA_CODE]/project_constitution.toml`
- Spec folder: `SPECs/[DNA_CODE]/spec_[descriptor]/`
- Spec files: `SPECs/[DNA_CODE]/spec_[descriptor]/[spec|parameters|exe|progress]_[descriptor].[md|toml|json]`

### DNA Code Format

- **Length:** Exactly 8 characters
- **Alphabet:** A, T, G, C only (DNA nucleotides)
- **Generation:** Hash of project name, mapped to genetic code
- **Examples:** `ATGCTCGA`, `TGCAATGC`, `GCATTACG`
- **Uniqueness:** Project name determines DNA code consistently

### File Naming Conventions

| Component | Format | Example |
|-----------|--------|---------|
| Spec markdown | `spec_[descriptor].md` | `spec_charity_pos.md` |
| Parameters TOML | `parameters_[descriptor].toml` | `parameters_charity_pos.toml` |
| Execution controller | `exe_[descriptor].md` | `exe_charity_pos.md` |
| Progress log | `progress_[descriptor].json` | `progress_charity_pos.json` |
| Project config | `project_constitution.toml` | `project_constitution.toml` |

**Descriptor:** Single word summarising the goal (e.g., `research`, `debug`, `prototype`, `charity_pos`, `ecommerce`)

### Workspace Root Detection

The system assumes it's running from a workspace where:
1. `__SPEC_Engine/` directory exists at the root
2. `SPECs/` directory exists (or will be created) at the root
3. All paths are relative to this workspace root

**Cross-references in files** use these assumptions:
- Commander references: `__SPEC_Engine/_templates/Spec_template.md`
- Constitution references: `__SPEC_Engine/_Constitution/constitution.md`
- Spec references: `SPECs/[DNA_CODE]/spec_[descriptor]/`

### File Creation Rules

**Framework files (read-only):**
- Never modified by Commander or Exe
- Updated only during system maintenance
- Serve as templates and governance

**Project constitution (created once, updated rarely):**
- Created by DNA_SPEC.md interview
- Updated when project requirements change
- Shared across all specs in DNA folder

**Spec files (created per goal):**
- Generated by Spec_Commander.md
- Three files created simultaneously (spec, parameters, exe)
- Progress log created at runtime

**Runtime files (auto-generated):**
- `progress_[descriptor].json` created on first execution
- Append-only (never modified, only appended)
- Immutable after completion

### Permissions Assumptions

The system assumes it has permission to:
- Read all files in `__SPEC_Engine/`
- Create directories in `SPECs/`
- Create/read/append files in `SPECs/[DNA_CODE]/`
- Create spec folders in `SPECs/[DNA_CODE]/spec_[descriptor]/`

**No permission required for:**
- Modifying framework files (system never does this)
- Deleting any files (system preserves all logs and specs)

---

## Time Estimates

| Phase | Duration | Notes |
|-------|----------|-------|
| Step 1: Project Setup | 1-3 min | DNA detection + context + folder prep |
| Step 2: Draft Structure | 2-5 min | Depends on goal complexity |
| Step 3: Human Review | 1-10 min | User review time |
| Step 4: Generate Files | 3-10 min | Includes detailed steps |
| Step 5: Validation | 1-2 min | Automated checks |
| Step 6: Output | <1 min | File write |
| **Total Generation** | **8-31 min** | **Average: ~20 min** |
| Execution Section 1: Init | 1-2 min | Validation + mode selection |
| Execution Section 2: Tasks | Variable | Depends on goal complexity |
| Execution Section 6: Analysis | 2-5 min | Post-execution review |

---

## Success Metrics

| Metric | Target | Measured By |
|--------|--------|-------------|
| Goal singularity | 100% | Article I compliance |
| Critical balance | 40-60% | Article VI compliance |
| Spec completion rate | >90% | Execution Section 6.4 verification |
| Human review catch rate | N/A | Issues found at Step 3 |
| Execution failures | <20% | progress.json analysis |
| Article XIV compliance | 100% | For build goals |
| DNA profile adoption | >80% | Projects using project_constitution.toml |

---

**End of Workflow Diagram**


```

Perfect! Now I need to add a brief mention in GETTING_STARTED.md and README.md. Let me add a concise section to GETTING_STARTED:

```markdown
# Getting Started with the SPEC Engine

**Version:** 1.0  
**Last Updated:** 2025-11-02  
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

3. **Draft high-level structure** (Step 2-3)
   - Commander proposes goal, tasks, completion criteria
   - Shows you something like:

```markdown
# SPEC Proposal for Review

## Goal
Analyse the structure and quality of Python module /src/auth.py

## Definition of Complete
- [ ] Analysis report generated covering functions, classes, dependencies
- [ ] Code quality metrics calculated (complexity, maintainability)
- [ ] Report saved as auth_analysis.md

## Tasks (High-Level)
1. **Parse and map module structure**
2. **Analyse code quality metrics**
3. **Generate comprehensive report**
```

4. **MANDATORY HUMAN REVIEW** (Step 3a)
   - This is where you approve or revise
   - Commander will ask: [A] Approve, [R] Revise, [C] Clarify

**Your action:** Review carefully! This is your chance to catch issues before detailed work begins.

Questions to ask yourself:
- Is the goal singular and clear?
- Do the tasks collectively achieve the goal?
- Are completion criteria specific?

If everything looks good: **Select [A] Approve**

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


```

```markdown
# Getting Started with the SPEC Engine

**Version:** 1.0  
**Last Updated:** 2025-11-02  
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

## Tasks (High-Level)
1. **Parse and map module structure**
2. **Analyse code quality metrics**
3. **Generate comprehensive report**
```

4. **MANDATORY HUMAN REVIEW** (Step 3a)
   - This is where you approve or revise
   - Commander will ask: [A] Approve, [R] Revise, [C] Clarify

**Your action:** Review carefully! This is your chance to catch issues before detailed work begins.

Questions to ask yourself:
- Is the goal singular and clear?
- Do the tasks collectively achieve the goal?
- Are completion criteria specific?

If everything looks good: **Select [A] Approve**

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


```

```markdown
# Getting Started with the SPEC Engine

**Version:** 1.0  
**Last Updated:** 2025-11-02  
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
   - This is where you approve or revise
   - Commander will ask: [A] Approve, [R] Revise, [C] Clarify

**Your action:** Review carefully! This is your chance to catch issues before detailed work begins.

Questions to ask yourself:
- Is the goal singular and clear?
- Do the tasks collectively achieve the goal?
- Are completion criteria specific?

If everything looks good: **Select [A] Approve**

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


```

```markdown
# Getting Started with the SPEC Engine

**Version:** 1.0  
**Last Updated:** 2025-11-02  
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


```

Now let me add a brief mention in README.md:

```markdown
### MCP Tool Integration (NEW)

The SPEC Engine now integrates MCP (Model Context Protocol) tool selection:
- **Step 2.5:** Commander analyses goals and recommends relevant MCP servers from catalog
- **Step 3a:** Combined human review + tool installation (single pause point)
- **Section 1.11:** Executor verifies tools before execution as safety check

Catalog: `__SPEC_Engine/_tools/mcp_tools_catalog.yaml` (269 servers, 2900+ tools, 24 categories)

Benefits:
- LLM autonomously selects appropriate tools based on goal requirements
- Human approves and installs in one workflow step
- Execution validates availability before proceeding
- Reduces friction and prevents execution failures

---

### Typical Workflow

### Phase 1: Project Setup (Optional, ~3 minutes)
```

```markdown
# SPEC Engine Documentation

**Version:** 1.0  
**Last Updated:** 2025-11-02  
**Purpose:** Structured workflow system for LLM-driven goal achievement

---

## What Is This?

The SPEC Engine is a constitutional framework that transforms high-level goals into structured, executable specifications for LLMs. It provides:

- **Goal-driven architecture:** Every element serves a singular North Star goal
- **Constitutional governance:** 14 Articles ensure quality and consistency
- **Three-file architecture:** Human-readable + Machine-readable + Execution controller
- **Project-level configuration:** Optional DNA profiles for per-project preferences
- **Built-in validation:** Pre-flight, runtime, and post-execution quality checks

---

## Quick Start: First Time Here?

**Step 1: Read This Overview** (you are here)  
**Step 2: Read `WORKFLOW_DIAGRAM.md`** - See the complete lifecycle  
**Step 3: Read `_Constitution/constitution.md`** - Understand governing principles  
**Step 4: Try creating a spec with `_Commander_SPEC/Spec_Commander.md`**

**For Beginners:** Start with `GETTING_STARTED.md` (beginner-friendly tutorial)

---

## Document Map

### Core Governance
```
_Constitution/
├── constitution.md          ⭐ START HERE - 14 immutable Articles
└── DESIGN_PHILOSOPHY.md     WHY decisions were made this way
```

**Read these first** to understand the system's foundations.

### Spec Generation
```
_Commander_SPEC/
└── Spec_Commander.md        🤖 Master coordinator for generating specs
```

**Use this** to create new specifications from goals.

### Project Configuration (Optional)
```
_DNA/
└── DNA_SPEC.md              🧬 Project-level preferences interview
```

**Use this** to configure project-wide settings (testing, risk, autonomy).

### Templates
```
_templates/
├── Spec_template.md         📄 Human-readable spec structure
├── parameters_template.toml ⚙️  Machine-readable parameters
└── exe_template.md          🚀 Execution controller logic
```

**These are templates** - don't edit directly. Commander generates from these.

### Meta-Documentation
```
WORKFLOW_DIAGRAM.md          Complete lifecycle from goal → execution → completion
COHERENCE_REVIEW.md          System-wide consistency validation (2025-11-02)
README.md                    This file
GETTING_STARTED.md           Beginner tutorial (coming soon)
```

---

## System Architecture

### Three Layers

```
┌─────────────────────────────────────────────────────┐
│  SYSTEM CONSTITUTION (immutable)                    │
│  Articles I-XIV                                     │
│  _Constitution/constitution.md                      │
└──────────────────┬──────────────────────────────────┘
                   │ governs
            ┌──────▼──────────────────────────────┐
            │  PROJECT CONSTITUTION (optional)    │
            │  Per-project preferences            │
            │  Specs/[DNA_CODE]/                  │
            │  project_constitution.toml          │
            └──────┬──────────────────────────────┘
                   │ configures
            ┌──────▼──────────────────────────────┐
            │  INDIVIDUAL SPEC (goal-specific)    │
            │  3 files per goal:                  │
            │  • spec_[descriptor].md             │
            │  • parameters_[descriptor].toml     │
            │  • exe_[descriptor].md              │
            └─────────────────────────────────────┘
```

### Three-File Specification

Every goal becomes a **SPEC** consisting of:

1. **spec_[descriptor].md** - Human-readable narrative
   - Goal, tasks, steps, backups
   - Software stack (for build goals)
   - Definition of complete
   - Cross-references to TOML

2. **parameters_[descriptor].toml** - Machine-readable config
   - Identical structure to markdown
   - Enables automated validation
   - Logging and error handling config

3. **exe_[descriptor].md** - Execution controller
   - Validation logic (Section 1)
   - Execution flow (Section 2)
   - Mode control (Section 3)
   - Post-execution analysis (Section 6)

4. **progress_[descriptor].json** - Runtime log (auto-generated)
   - Step outcomes
   - Retry counts
   - Mode switches
   - Constitutional compliance tracking

---

## Key Concepts

### The North Star Principle (Article I)
Every spec has **exactly one goal**. Multiple goals require separate specs.

### Goal → Task → Step → Backup Hierarchy (Article II)
```
GOAL (singular outcome)
  └── TASK [n] (discrete objective, 2-5 per spec)
      └── STEP [m] (concrete action, 1-5 per task)
          └── BACKUP [p] (alternative method, 0-2 per step)
```

### Execution Modes (Article IX)
- **Silent:** Fully autonomous
- **Collaborative:** Human-in-loop
- **Dynamic (default):** Autonomous with intelligent escalation

### Critical Flags (Article VI)
- `critical = true`: Failure blocks goal, escalate after exhaustion
- `critical = false`: Log failure, continue execution
- **Balance:** 40-60% of steps should be critical

### Backups as Alternatives (Article VII)
Backups must be **alternative reasoning paths**, not simple retries.

**Invalid:** "Try again"  
**Valid:** "If documentation incomplete, inspect source code directly"

### Constitutional Enforcement (Articles I-XIV)
Three checkpoints:
1. **Pre-flight:** Commander validates before generation
2. **Runtime:** Exe checks compliance during execution
3. **Post-execution:** Analysis reviews adherence

---

## MCP Tool Integration (NEW - 2025-11-03)

The SPEC Engine now integrates MCP (Model Context Protocol) tool selection into the workflow:

- **Step 2.5:** Commander analyses goals and autonomously recommends relevant MCP servers
- **Step 3a:** Combined human review + tool installation (single pause point)  
- **Section 1.11:** Executor verifies tools before execution as safety check

**Tool Catalog:** `__SPEC_Engine/_tools/mcp_tools_catalog.yaml`
- 269 MCP servers
- 2900+ individual tools
- 24 categories (Databases, Cloud, AI/ML, Search, etc.)

**Benefits:**
- LLM autonomously selects tools based on goal requirements
- Human approves and installs in one workflow step
- Execution validates availability before proceeding
- Prevents tool-related execution failures

**See:** `GETTING_STARTED.md` for tutorial, `WORKFLOW_DIAGRAM.md` for complete flow

---

## Typical Workflow

### Phase 1: Project Setup (Optional, ~3 minutes)
```
Run DNA_SPEC.md interview
  ↓
Answer 5 questions about project
  ↓
Generate DNA code (e.g., ATGCTCGA)
  ↓
Create Specs/ATGCTCGA/project_constitution.toml
```

**When to use DNA profiles:**
- Multiple specs for same project
- Want consistent testing/risk preferences
- Custom tooling or constraints

**When to skip:**
- One-off goal
- Flexible about configuration
- Want system defaults

### Phase 2: Spec Generation (~20 minutes)
```
Launch Spec_Commander.md with goal
  ↓
Commander drafts high-level structure
  ↓
MANDATORY HUMAN REVIEW (approve/revise/clarify)
  ↓
Commander generates detailed steps
  ↓
Pre-flight validation (constitutional compliance)
  ↓
3 files created in Specs/[DNA_CODE]/spec_[descriptor]/
```

### Phase 3: Execution (Variable)
```
Launch exe_[descriptor].md
  ↓
Initialization & validation (Section 1)
  ↓
User selects mode (Dynamic/Silent/Collaborative)
  ↓
Execute tasks sequentially (Section 2)
  - Try primary method
  - Try backups if failure
  - Escalate if critical + exhausted
  - Log everything to progress.json
  ↓
Post-execution analysis (Section 6)
  - Failure patterns
  - Backup effectiveness
  - Constitutional compliance review
  - Completion verification
  ↓
Goal ACHIEVED / PARTIAL / NOT ACHIEVED
```

---

## When To Use Each Document

| Document | When To Use |
|----------|-------------|
| `constitution.md` | Before creating any spec (understand rules) |
| `DESIGN_PHILOSOPHY.md` | When you want to know WHY (rationale) |
| `WORKFLOW_DIAGRAM.md` | To see complete lifecycle flow |
| `Spec_Commander.md` | To CREATE a new spec from a goal |
| `DNA_SPEC.md` | To configure project-level preferences |
| `exe_[descriptor].md` | To EXECUTE an existing spec |
| `Spec_template.md` | Reference when writing custom specs |
| `parameters_template.toml` | Reference for TOML structure |
| `GETTING_STARTED.md` | First-time beginner tutorial |

---

## File System Requirements

### Expected Directory Structure
```
[Your Workspace Root]/
├── __SPEC_Engine/           # This directory (framework)
│   ├── README.md
│   ├── WORKFLOW_DIAGRAM.md
│   ├── COHERENCE_REVIEW.md
│   ├── _Constitution/
│   ├── _Commander_SPEC/
│   ├── _DNA/
│   └── _templates/
│
└── SPECs/                   # Generated specs live here
    ├── [DNA_CODE_1]/        # Project 1 (e.g., ATGCTCGA)
    │   ├── project_constitution.toml
    │   ├── spec_[descriptor_1]/
    │   │   ├── spec_[descriptor_1].md
    │   │   ├── parameters_[descriptor_1].toml
    │   │   ├── exe_[descriptor_1].md
    │   │   └── progress_[descriptor_1].json
    │   └── spec_[descriptor_2]/
    │
    └── [DNA_CODE_2]/        # Project 2 (e.g., TGCAATGC)
        └── ...
```

**Important:** 
- Framework files live in `__SPEC_Engine/`
- Generated specs live in `SPECs/[DNA_CODE]/spec_[descriptor]/`
- DNA codes are 8 characters using A, T, G, C only
- Each spec lives in its own folder

---

## Common Questions

### Q: Do I need a DNA profile?
**A:** No, it's optional. DNA profiles are useful when:
- Creating multiple specs for same project
- Want consistent testing/risk/autonomy settings
- Have custom tools or constraints

Without DNA, Commander uses system defaults.

### Q: Can I edit templates directly?
**A:** No. Templates in `_templates/` are blueprints. Commander generates from these. Edit generated files in `SPECs/[DNA_CODE]/spec_[descriptor]/` instead.

### Q: What if validation fails?
**A:** Exe will HALT and explain what's missing. Common issues:
- Goal not singular (Article I)
- Tasks/steps out of 2-5 / 1-5 range (Article II)
- Markdown ↔ TOML mismatch (Article III)
- Software stack undefined for build goals (Article XIV)

Fix the spec files and re-run.

### Q: Can I use this for non-coding goals?
**A:** Yes! SPECs work for any goal:
- Research and analysis
- Content creation
- Data processing
- Testing and QA
- System administration
- And yes, building software

### Q: How do I know if my goal is "complete"?
**A:** Exe Section 6.4 verifies completion criteria from your spec:
- Primary deliverable exists
- Quality standards met
- Verification method passed
- (For build goals) Deployment artifact exists, UI implemented, production-ready

Status: ACHIEVED (all pass) / PARTIAL (core works, deployment incomplete) / NOT ACHIEVED (broken)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-02 | Initial README created during structural review |

---

## Getting Help

**Read first:**
1. This README (overview)
2. `WORKFLOW_DIAGRAM.md` (detailed workflow)
3. `_Constitution/constitution.md` (governing rules)

**Stuck?**
- Check `COHERENCE_REVIEW.md` for system health status
- Review example specs in `SPECs/Testing/`
- Consult `DESIGN_PHILOSOPHY.md` for design rationale

**Contributing:**
- Document must align with constitution.md
- Changes require constitutional amendment process (Article XIII)
- Test changes with example specs before committing

---

**Next Steps:** Read `WORKFLOW_DIAGRAM.md` to see the complete lifecycle, then try creating your first spec with `Spec_Commander.md`.


```

Now let me check for linter errors in the files I modified:

The linter warnings are mostly pre-existing markdown style issues (blanks around headings, list formatting, etc.) rather than functional errors introduced by my changes. These are acceptable for now.

Let me create a comprehensive summary document:

```markdown
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

```

## Complete! MCP Tool Integration Implemented

I've successfully integrated MCP tool selection into the SPEC Engine workflow. Here's what was delivered:

### Core Changes

**A) Commander Workflow** (`Spec_Commander.md`)
- **Step 2.5 (NEW):** LLM analyses goal and recommends MCP tools autonomously
  - Non-prescriptive framework (guidelines, not rigid rules)
  - Three-tier classification: REQUIRED/RECOMMENDED/OPTIONAL
  - Rationale documented for each selection
- **Step 3a (REVISED):** Single pause point combining review + installation
  - Phase 1: Present proposal (structure + toolset)
  - Phase 2: Human installs tools NOW
  - Phase 3: Confirm installation
  - Options: [A] Approve, [R] Revise, [T] Modify tools, [C] Clarify

**B) Template Files**
- **`spec_template.md`:** Added "MCP Toolset" section with installation commands
- **`parameters_template.toml`:** Added `[mcp_tools]` section for machine-readable config
- **`exe_template.md`:** Added Section 1.11 for tool verification (safety check)

**C) Documentation**
- **`WORKFLOW_DIAGRAM.md`:** Visual diagrams for Steps 2.5 and 3a
- **`GETTING_STARTED.md`:** Tutorial updated with concrete examples
- **`README.md`:** New "MCP Tool Integration" overview section

### Key Features

1. **LLM Autonomy:** Non-prescriptive reasoning framework (no "if X always Y" rules)
2. **Single Pause:** Combined review + installation at one checkpoint (smooth workflow)
3. **Human Control:** LLM recommends, human approves and installs
4. **Safety Check:** Executor verifies tools before execution (not initial install)
5. **Rationale Required:** Every recommendation explains WHY for THIS goal
6. **Three Tiers:** Conservative REQUIRED, beneficial RECOMMENDED, nice-to-have OPTIONAL

### Workflow Summary

```
Goal → Commander analyses → Recommends tools → Human reviews proposal → 
Human approves → Human installs tools → Human confirms → Commander generates SPEC → 
Executor verifies tools → Execution proceeds
```

### Files Modified

1. `__SPEC_Engine/_Commander_SPEC/Spec_Commander.md`
2. `__SPEC_Engine/_templates/Spec_template.md`
3. `__SPEC_Engine/_templates/parameters_template.toml`
4. `__SPEC_Engine/_templates/exe_template.md`
5. `__SPEC_Engine/WORKFLOW_DIAGRAM.md`
6. `__SPEC_Engine/GETTING_STARTED.md`
7. `__SPEC_Engine/README.md`

### Reference Document

Complete implementation summary saved to:
**`@filing/_chats/MCP_TOOL_INTEGRATION_IMPLEMENTATION_SUMMARY.md`**

Contains: detailed changes, design principles, testing recommendations, future enhancements

---

All your requirements integrated: mandatory for every SPEC, generic templates with examples, LLM autonomy, single pause workflow. Ready to test! 🎯

```plaintext
Goal → Commander analyses → Recommends tools → Human reviews proposal → 
Human approves → Human installs tools → Human confirms → Commander generates SPEC → 
Executor verifies tools → Execution proceeds
```

---

**User**

Please verify your work

---

**Cursor**

I'll verify my work by checking each modified file to ensure the changes were applied correctly and are coherent.

## Verification Complete ✅

I've systematically verified all changes. Here's the verification report:

### ✅ Commander Workflow (`Spec_Commander.md`)

**Step 2.5 (Lines 190-276):** VERIFIED
- MCP Tool Analysis section properly added
- Non-prescriptive framework correctly implemented
- Seven-step process documented (Load → Analyse → Identify → Evaluate → Classify → Document → Guidelines)
- Quality guidelines emphasize autonomy ("no rigid mappings")
- References `mcp_tools_catalog.yaml` correctly

**Step 3 Output Format (Lines 313-334):** VERIFIED
- Draft Proposal now includes "Recommended MCP Toolset" section
- Three-tier structure: REQUIRED/RECOMMENDED/OPTIONAL
- Each tier has appropriate fields (Rationale, Provides/Alternative/Use case, Install command)
- Properly formatted with placeholders for Commander to populate

**Step 3a (Lines 351-511):** VERIFIED
- Correctly restructured as combined review + installation workflow
- Five phases properly sequenced:
  1. Present Proposal (with toolset)
  2. Handle User Response ([A]/[R]/[T]/[C] options)
  3. Tool Installation Instructions (after [A])
  4. Confirm Installation ([Y]/[N]/[S] options)
  5. Exit Checkpoint
- Single pause point design maintained
- References to "Phase 3" match installation phase
- Rationale clearly explains benefits

### ✅ Template Files

**`Spec_template.md` (Lines 62-147):** VERIFIED
- MCP Toolset section added in correct position (after Definition of Complete)
- Handlebars-like syntax for Commander population: `{{#each mcp_tools.required}}`
- Tool Verification subsection explains safety check nature
- Complete example provided (postgres, github, playwright, notion)
- Cross-references Section 1.11 correctly

**`parameters_template.toml` (Lines 67-106):** VERIFIED
- `[mcp_tools]` section properly formatted
- Three arrays: required, recommended, optional (with clear comments)
- `[mcp_tools.verification]` subsection with four boolean/log settings
- Optional tool-specific config structure shown
- Complete example in comments matches spec_template example
- References Section 1.11 in comments

**`exe_template.md` (Lines 248-442):** VERIFIED
- Section 1.11 "MCP Tool Verification (Safety Check)" properly added
- Seven-step process documented with detailed sub-steps
- Verification logic for REQUIRED (halt), RECOMMENDED (warn), OPTIONAL (log only)
- Detailed error messages with OS-specific config paths
- Progress.json logging format specified (lines 359-382)
- Example success output (lines 401-419)
- Example failure output (lines 421-438)
- "Initialization Complete" message updated to mention MCP tools verification

### ✅ Documentation Updates

**`WORKFLOW_DIAGRAM.md`:**
- **Lines 302-331:** Step 2.5 visual diagram added with 5-point process
- **Lines 332-414:** Step 3a revised to show 3-phase combined workflow
  - Phase 1: Present Proposal (including MCP Toolset in example)
  - Phase 2: Installation (with install commands)
  - Phase 3: Confirm Installation ([Y]/[N]/[S])
- Visual formatting preserved (box-drawing characters)
- Rationale noted at bottom of Step 3a box

**`GETTING_STARTED.md` (Lines 142-216):** VERIFIED
- Step 3 title updated to "Commander Interview and Tool Selection"
- Steps renumbered to include Step 4 (Analyse and recommend MCP tools)
- Step 5 shows complete proposal example with MCP Toolset
- Concrete example: filesystem (REQUIRED), github (RECOMMENDED) for Python module analysis
- Step 6 explanation includes tool-related questions and workflow paths
- All three paths explained: [A] Approve, [R]/[T] Revise/Modify, [C] Clarify

**`README.md` (Lines 172-192):** VERIFIED
- New "MCP Tool Integration (NEW - 2025-11-03)" section added
- Three integration points listed: Step 2.5, Step 3a, Section 1.11
- Catalog statistics: 269 servers, 2900+ tools, 24 categories
- Four benefits clearly stated
- References to GETTING_STARTED.md and WORKFLOW_DIAGRAM.md

### ✅ Coherence Checks

**Terminology Consistency:** VERIFIED
- "Step 2.5" used consistently for tool analysis
- "Step 3a" used consistently for combined review + installation
- "Section 1.11" used consistently for executor verification
- "REQUIRED/RECOMMENDED/OPTIONAL" classification consistent across all files
- "Safety check" language consistent (not "installation")

**Cross-References:** VERIFIED
- Commander references `__SPEC_Engine/_tools/mcp_tools_catalog.yaml` ✅
- Spec template references "Step 3a" and "Section 1.11" ✅
- Parameters template references "Section 1.11" in comments ✅
- Exe template references "Step 3a" as when tools were installed ✅
- All references to "269 servers, 2900+ tools, 24 categories" consistent ✅

**Workflow Flow:** VERIFIED
- Commander Step 2.5 → Commander Step 3 (proposal includes toolset) → Commander Step 3a (review + install) → Commander Step 4 (generate files) → Executor Section 1.11 (verify) → Executor Section 2 (execute)
- Single pause point maintained at Step 3a (no fragmentation)
- Human installs during Step 3a, executor verifies during Section 1.11 ✅

**Example Consistency:** VERIFIED
- Same tools used across examples where appropriate:
  - WORKFLOW_DIAGRAM: postgres, github, playwright, notion
  - Spec_template: postgres, github, playwright, notion
  - Parameters_template: postgres, github, playwright, notion (in comments)
  - GETTING_STARTED: filesystem, github (contextually appropriate for Python analysis goal)

### ✅ Design Principles Verified

1. **Single Pause Workflow:** All documents show ONE pause at Step 3a ✅
2. **LLM Autonomy:** Non-prescriptive framework, no rigid rules ✅
3. **Human Control:** LLM recommends, human installs ✅
4. **Safety Check:** Section 1.11 verifies (not installs) ✅
5. **Rationale Required:** Every tool classification includes "why" ✅
6. **Three-Tier System:** REQUIRED/RECOMMENDED/OPTIONAL consistently applied ✅

### 📋 Summary Document

Created: **`@filing/_chats/MCP_TOOL_INTEGRATION_IMPLEMENTATION_SUMMARY.md`**
- Complete implementation details
- Design principles
- Testing recommendations
- Future enhancements
- User feedback integration checklist

---

## Final Status: ✅ ALL VERIFIED

All changes have been correctly implemented:
- 7 files modified as documented
- Workflow coherent across all documents
- Cross-references accurate
- Terminology consistent
- Examples aligned
- Design principles maintained

**The MCP tool integration is complete and ready for testing.** 🎯

