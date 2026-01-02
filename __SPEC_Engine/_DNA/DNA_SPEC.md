# Project DNA_SPEC Project Framing Interview Template

**Version:** 1.0  
**Last Updated:** 2025-11-02  
**Purpose:** Quick configuration to establish project-specific governance  
**Time:** 3-5 minutes  
**Questions:** 5 essential questions  
**Output:** `project_constitution.toml` (machine-readable configuration for Commander)

---

## For Users

This interview gathers minimal information about your project to configure:
- How autonomous spec execution should be
- What level of testing/validation to apply
- Technical constraints and dependencies
- Custom tooling preferences

- Execution autonomy level
- Testing/validation approach
- Technical constraints
- Custom tooling

Everything else uses smart defaults.

Re-run anytime to update configuration.

---

## For LLMs: Execution Instructions

**Your Task:** Conduct a 5-question interview, infer project characteristics, generate `project_constitution.toml`.

### The 5 Questions

1. **What are you trying to achieve with this project?** (1-2 sentences)
2. **Required software stack?** (languages, frameworks, tools - or "flexible")
3. **External dependencies?** (APIs, databases, cloud services - or "none")
4. **Custom backup tools?** (scripts/tools for backup methods - or "none")
5. **Execution autonomy preference?**
   - Silent (fully autonomous)
   - Dynamic (autonomous with intelligent escalation) - RECOMMENDED
   - Collaborative (frequent human oversight)

### What to Infer from Q1

Analyse the project description to determine:

**Domain:** Software dev, data analysis, content, sysadmin, ML, automation

**Risk Level:**
- HIGH: Medical, financial, security, production systems → 60-80% critical steps
- LOW: Prototypes, experiments, content, documentation → 20-40% critical steps
- MODERATE: Everything else (DEFAULT) → 40-60% critical steps

**Complexity:** Simple (single focused task), Moderate (multiple components), Complex (multiple systems)

**User-Facing:** Does it have users/UI/API? → Enables user stories if yes

**Failure Strategy:**
- HIGH risk → halt_on_critical
- MODERATE risk → collaborative_review
- LOW risk → continue_and_log

**Backend Preference:** (for web/API projects only)
- RAPID_PROTOTYPE: Learning, MVP, proof-of-concept → prefer BaaS (Insforge, Supabase)
- PRODUCTION: Scalable, custom infra needed → flexible (custom backend)
- ENTERPRISE: Compliance, audit, custom requirements → avoid BaaS

**Insforge Recommended When:**
- Risk level = LOW (prototypes, learning)
- Complexity = Simple or Moderate
- User-facing = true (CRUD operations common)
- Domain = Software dev + "web app" or "API" mentioned
- NOT recommended when: "high-performance", "real-time", "enterprise", "compliance" mentioned

### Smart Defaults

- Testing: ALWAYS enabled (unit, integration, TDD preferred)
- Backups: Mandatory for critical steps, max 2 per step
- Retries: 2 attempts, exponential backoff
- Error propagation: Always enabled
- Escalation: 3 failures for Dynamic, 5 for Silent
- Logging: Standard detail with metrics, 90-day retention

### Backend Preference Inference (Web/API Projects Only)

**Step 1: Check if backend relevant**
- Does Q1 mention "web", "app", "API", "database", or "backend"?
- If NO → skip backend preference (set to "not_applicable")
- If YES → proceed to Step 2

**Step 2: Assess project characteristics**

Classify as `insforge_preferred` when:
- Risk level = LOW or MODERATE (not HIGH)
- Complexity = Simple or Moderate (not Complex)
- Q1 indicates: prototype, learning, CRUD operations, standard features
- Q2 (stack) is flexible or mentions web frameworks
- Q3 (dependencies) minimal or standard (not heavy data processing)

Classify as `flexible` when:
- Risk level = MODERATE
- Complexity = Moderate
- Could use BaaS but custom backend also viable
- Future scalability might be needed

Classify as `custom_required` when:
- Risk level = HIGH (medical, financial, security)
- Complexity = Complex (multiple systems, heavy processing)
- Q1 mentions: "real-time", "high-performance", "enterprise", "compliance"
- Q3 lists heavy dependencies or custom infrastructure

**Step 3: Populate TOML fields**
```toml
# Example for Learning Project:
backend_preference = "insforge_preferred"
backend_reasoning = "Learning project with CRUD operations, low risk, rapid iteration prioritised"
insforge_suitable = true
insforge_use_cases = ["learning", "crud_app", "rapid_prototype"]
insforge_avoid_reasons = []

# Example for Enterprise System:
backend_preference = "custom_required"
backend_reasoning = "High risk financial system requiring audit trails and compliance"
insforge_suitable = false
insforge_use_cases = []
insforge_avoid_reasons = ["compliance_requirements", "audit_trails", "enterprise_scale"]
```

### After Interview

1. **Generate DNA folder code:**
   - Hash the `project_name` (inferred from Q1)
   - Convert to 8-character DNA code using A, T, G, C
   - Example: "auth-system" → `ATGCTCGA`

2. **Create DNA folder structure:**
   ```
   Specs/ATGCTCGA/
   └── project_constitution.toml
   ```

3. **Show inference summary:**
   - DNA code: `ATGCTCGA`
   - Detected domain, risk, complexity, user-facing
   - Why you classified it that way
   - Configuration applied
   - Smart defaults used

4. **Generate `project_constitution.toml`** in DNA folder using template below.

---

## TOML Template

```toml
# Project Constitution
# Generated by DNA Interview
# Date: [timestamp]

[metadata]
dna_code = "[8-char DNA code from hash]"
project_name = "[infer from Q1]"
constitution_version = "1.0"
generated_date = "[ISO-8601]"
system_constitution_version = "1.0"

[project]
purpose = "[Q1 answer]"
domain = "[inferred]"
risk_level = "[high|moderate|low]"
complexity = "[simple|moderate|complex]"
user_facing = [true|false]

[execution]
default_mode = "[Q5: silent|dynamic|collaborative]"
escalation_threshold = [5 for silent, 3 for dynamic]
confidence_threshold = 0.6

[quality]
critical_percentage = "[60-80|40-60|20-40 based on risk]"
output_specificity = "moderate"
documentation_required = ["progress_log", "summary_report"]

[error_handling]
propagation_enabled = true
propagation_strategy = "[halt_on_critical|collaborative_review|continue_and_log based on risk]"
failure_threshold = [2 for high, 3 for moderate, 5 for low]
read_prior_steps = true

[testing]
required = true
types = ["unit", "integration"]
tdd_preferred = true

[backups]
mandatory_for_critical = true
preferred_types = ["cognitive", "tool"]
custom_tools = ["[Q4 list or empty]"]
max_backups_per_step = 2

[retry]
max_retries = 2
backoff_strategy = "exponential"

[resources]
time_limit_minutes = 0
task_timeout_minutes = 0
step_timeout_seconds = 0
external_dependencies = ["[Q3 list or empty]"]
external_service_failures = "retry_with_backoff"

[constraints]
software_stack = "[Q2 answer]"
language = "[extract or null]"
frameworks = ["[extract or empty]"]
tools = ["[extract or empty]"]

# Backend preferences (for web/API projects only)
backend_preference = "[inferred: insforge_preferred|flexible|custom_required|not_applicable]"
backend_reasoning = "[why this preference was chosen based on Q1]"
insforge_suitable = [true|false]  # Specifically for Insforge BaaS
insforge_use_cases = ["[rapid_prototype|learning|crud_app|api_service or empty]"]
insforge_avoid_reasons = ["[or empty if suitable]"]

prohibited_actions = [
    "Do not delete files outside project directory",
    "Do not modify system configuration",
    "Do not expose credentials in logs",
    "Do not install packages without approval"
]

[optional_features]
user_stories = "[user_facing_only|never based on user_facing]"
clarification_phase = "complex_only"

# Research-enabled mode: Access external knowledge sources when LLM knowledge insufficient
# Set project-wide default (can be overridden per task in individual specs)
research_enabled_default = false  # Set to true for research-heavy projects
research_sources_available = ["web_search", "documentation"]  # Tools available to project
# Options: web_search, documentation, technical_specs, github_repos, academic
# Note: Actual availability depends on MCP tools configured in environment

quickstart_validation = true
parallel_execution = false

[logging]
detail_level = "standard"
include_metrics = true
retention_days = 90

[review]
required_before_execution = false
change_tracking = "git"

[compliance]
security_requirements = ["no_credentials_in_logs", "encrypt_sensitive_data"]
regulatory = []

[_inference_notes]
risk_reasoning = "[explain classification]"
domain_reasoning = "[explain detection]"
failure_strategy_reasoning = "[explain choice]"
user_stories_reasoning = "[explain enabled/disabled]"
complexity_reasoning = "[explain assessment]"
backend_preference_reasoning = "[explain why insforge_preferred|flexible|custom_required|not_applicable]"
insforge_analysis = "[explain suitability assessment]"

[[version_history]]
version = "1.0"
date = "[ISO-8601]"
changes = "Initial constitution via DNA interview"
```

---

## Commander Integration

Commander reads `Specs/[DNA_CODE]/project_constitution.toml` during spec generation.

**When generating a new SPEC:**
1. User provides DNA code (e.g., `ATGCTCGA`)
2. Commander reads `Specs/ATGCTCGA/project_constitution.toml`
3. Applies project-specific settings:
   - Critical balance from `[quality].critical_percentage`
   - Default mode from `[execution].default_mode`
   - Validates against `[constraints]`
   - Enables/disables user stories from `[optional_features]`
   - References custom tools from `[backups].custom_tools`
4. Generates SPEC in `Specs/ATGCTCGA/spec_[descriptor]/`

**Override Hierarchy:**
```
System Constitution (immutable)
  ↓
Project Constitution (Specs/[DNA_CODE]/project_constitution.toml)
  ↓
Individual SPEC settings
```

---

## Maintenance

**Update existing DNA profile:**
- Re-run interview with same project name → same DNA code
- Updates `project_constitution.toml` with new version history
- Existing SPECs in that DNA folder use updated settings

**Create new DNA profile:**
- Re-run interview with different project name → different DNA code
- Creates new DNA folder
- Old DNA folder and SPECs remain unchanged

**When to update:**
- Risk level changes (prototype → production)
- Team size changes
- New dependencies added
- Tooling updates
