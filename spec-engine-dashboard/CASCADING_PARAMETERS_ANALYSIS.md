# Cascading Parameters: Value Analysis
**Date:** 2 January 2026  
**Purpose:** Evaluate the merit of hierarchical parameter inheritance in the SPEC Engine

---

## The Accidental Discovery

### What Was Built (By Accident)

A **three-tier parameter system:**

```
Tier 1: DNA Profile (Master Configuration)
  ├── testing: "standard"
  ├── risk: "medium"
  ├── autonomy: "high"
  ├── customTools: ["linter", "security_scanner"]
  └── constraints: ["no_external_apis", "windows_only"]
       ↓ CASCADE
Tier 2: SPEC parameters_{descriptor}.toml
  ├── Inherits DNA defaults
  ├── Can override specific values
  └── Adds SPEC-specific parameters
       ↓ CASCADE
Tier 3: SPECLet/Task parameters
  ├── Inherits SPEC defaults
  └── Can override for specific tasks
```

### The Question

**Is there value in Tier 1 → Tier 2 cascade?**

Should DNA profiles provide **project-wide defaults** that individual SPECs inherit and optionally override?

---

## Real-World Analogies

This pattern exists in many mature systems:

### 1. Docker Compose
```yaml
# Top-level defaults (like DNA Profile)
x-defaults: &defaults
  restart: always
  logging:
    driver: json-file

services:
  # Service inherits and overrides (like SPEC)
  api:
    <<: *defaults
    restart: on-failure  # Override
```

### 2. ESLint Configuration
```json
// Root .eslintrc (DNA level)
{
  "extends": "eslint:recommended",
  "rules": { "semi": "error" }
}

// Directory override (SPEC level)
{
  "rules": { "semi": "off" }  // Override for this directory
}
```

### 3. Kubernetes
```yaml
# Namespace defaults (DNA level)
apiVersion: v1
kind: LimitRange
metadata:
  namespace: production
spec:
  limits:
    - default:
        cpu: "500m"
        
# Pod override (SPEC level)
apiVersion: v1
kind: Pod
spec:
  containers:
    - resources:
        limits:
          cpu: "2"  # Override namespace default
```

### 4. Terraform Workspaces
```hcl
# Shared variables (DNA level)
variable "instance_type" {
  default = "t3.micro"
}

# Workspace override (SPEC level)
# production.tfvars
instance_type = "t3.large"  # Override for production
```

---

## Use Cases for SPEC Engine

### Use Case 1: Testing Strategy Inheritance

**Scenario:** Large project with 20 SPECs, mostly standard testing

**Without Cascade:**
```toml
# EVERY SPEC's parameters_{descriptor}.toml
[testing]
approach = "standard"
coverage = "standard"
```

**With Cascade:**
```toml
# DNA Profile (project_constitution.toml)
[defaults]
testing = "standard"

# Only SPECs that differ need to override
# parameters_critical_migration.toml
[testing]
approach = "comprehensive"  # Override for critical SPEC
```

**Benefit:** Reduce duplication, single source of truth for project defaults

---

### Use Case 2: Multi-Environment Management

**Scenario:** Same SPECs deployed to dev/staging/production

**Without Cascade:**
```toml
# EVERY SPEC needs environment-specific settings
[deployment]
environment = "production"
backup_enabled = true
monitoring = "full"
```

**With Cascade:**
```toml
# DNA Profile: PROJ-PROD
[defaults]
environment = "production"
backup_enabled = true
monitoring = "full"

# DNA Profile: PROJ-DEV
[defaults]
environment = "dev"
backup_enabled = false
monitoring = "basic"

# SPECs inherit from their DNA's defaults
```

**Benefit:** Same SPEC, different DNA = different behavior

---

### Use Case 3: Client-Specific Constraints

**Scenario:** Agency serving multiple clients with different requirements

**Without Cascade:**
```toml
# EVERY SPEC for Client A
[constraints]
no_external_apis = true
data_residency = "EU"
compliance = "GDPR"
```

**With Cascade:**
```toml
# DNA Profile: CLIENT-A
[constraints]
no_external_apis = true
data_residency = "EU"
compliance = "GDPR"

# DNA Profile: CLIENT-B
[constraints]
cloud_provider = "AWS-only"
compliance = "HIPAA"

# SPECs inherit client-specific constraints from DNA
```

**Benefit:** Reuse SPECs across clients, constraints cascade automatically

---

### Use Case 4: Security Posture

**Scenario:** Different projects with different security requirements

**High-Security Project (Banking):**
```toml
# DNA Profile
[security]
risk = "low"
code_review = "mandatory"
penetration_testing = true
encryption = "always"

# All SPECs inherit these strict defaults
```

**Internal Tool Project:**
```toml
# DNA Profile
[security]
risk = "medium"
code_review = "optional"
penetration_testing = false

# All SPECs inherit more relaxed defaults
```

**Benefit:** Security policy enforced at project level, not per-SPEC

---

### Use Case 5: Team Autonomy Levels

**Scenario:** Different teams with different experience levels

**Senior Team:**
```toml
# DNA Profile
[execution]
autonomy = "high"          # AI can make decisions
approval_required = false
silent_mode = true
```

**Junior Team:**
```toml
# DNA Profile
[execution]
autonomy = "low"           # More human oversight
approval_required = true
silent_mode = false
```

**Benefit:** Team-appropriate defaults, SPECs adapt to team capability

---

## The Cascade Mechanism

### Proposed Inheritance Rules

```
1. DNA Profile provides DEFAULTS
2. SPEC parameters_{descriptor}.toml OVERRIDES
3. Explicit > Inherited
4. No value in SPEC = Inherit from DNA
5. Empty string in SPEC = "I want empty" (not inherit)
```

### Example

**DNA Profile (project_constitution.toml):**
```toml
[defaults]
testing = "standard"
risk = "medium"
autonomy = "high"
custom_tools = "linter,security_scanner"
```

**SPEC A (parameters_api_endpoint.toml):**
```toml
# No testing specified → inherits "standard"
# No risk specified → inherits "medium"
autonomy = "low"  # OVERRIDE to "low" for this SPEC
# No custom_tools specified → inherits "linter,security_scanner"
```

**Effective Configuration for SPEC A:**
```toml
testing = "standard"        # ← Inherited from DNA
risk = "medium"             # ← Inherited from DNA
autonomy = "low"            # ← Explicitly overridden
custom_tools = "linter,security_scanner"  # ← Inherited from DNA
```

---

## Implementation Options

### Option 1: Enhance Existing File Structure

**Keep file-based, add cascade logic:**

```toml
# SPECs/GCATTAGC/project_constitution.toml (DNA Profile)
[metadata]
dna_code = "GCATTAGC"
project_name = "Innovation Dashboard"

[defaults]  # ← NEW SECTION
testing = "standard"
risk = "medium"
autonomy = "high"
custom_tools = "linter,security_scanner"
constraints = "no_external_apis"

# SPECs/GCATTAGC/spec_api/parameters_api.toml (SPEC)
[metadata]
inherits_from_dna = true  # ← NEW FLAG

[overrides]  # ← NEW SECTION
autonomy = "low"  # Only specify what's different
```

**Pros:**
- File-based (matches SPEC Engine philosophy)
- Explicit inheritance
- Version controllable

**Cons:**
- Requires parser updates
- More complex TOML structure

---

### Option 2: Database-Backed with File Sync

**Use database for UI convenience, sync to files:**

```
Dashboard UI ────┐
                 ├──> Database (cache + metadata)
File System ─────┘
                 │
                 └──> Cascade Logic in Backend
                      │
                      └──> Resolved Config for Execution
```

**Pros:**
- Fast UI queries
- Easy cascade logic
- Maintains file system as source of truth

**Cons:**
- Sync complexity
- Potential for drift

---

### Option 3: Pure Runtime Resolution

**Don't store cascaded values, compute on-demand:**

```
Execution Request
    ↓
1. Read DNA Profile defaults
2. Read SPEC parameters
3. Merge (SPEC overrides DNA)
4. Return resolved configuration
```

**Pros:**
- Simple
- No duplication
- Single source of truth

**Cons:**
- Compute overhead (minimal)
- No static validation of resolved config

---

## Architectural Benefits

### 1. DRY Principle
- Define once (DNA level)
- Inherit everywhere (SPEC level)
- Override when needed

### 2. Maintainability
- Change project-wide setting in ONE place
- All SPECs inherit automatically
- No need to update 20 parameter files

### 3. Consistency
- Enforces project-level standards
- Reduces configuration drift
- Makes defaults explicit

### 4. Flexibility
- SPECs can still override
- Balance between standardization and customization
- Progressive disclosure (simple SPECs inherit, complex SPECs customize)

---

## Potential Pitfalls

### 1. Hidden Configuration
**Problem:** Developer doesn't know where a setting comes from

**Mitigation:**
- Dashboard shows "inherited" vs "explicit" values
- CLI tool to show resolved configuration
- Clear documentation

### 2. Override Confusion
**Problem:** SPEC override doesn't seem to work (wrong key name)

**Mitigation:**
- Validation warns about unused overrides
- Auto-complete suggests inheritable keys

### 3. Cascade Complexity
**Problem:** Multiple inheritance levels become confusing

**Mitigation:**
- Keep it to 2 levels (DNA → SPEC)
- Don't add SPECLet-level cascade (too complex)

---

## Recommendation

### ✅ YES - The Cascade Pattern Has Value

**Implement cascading parameters with these principles:**

1. **DNA Profile = Project Defaults**
   - Stored in `project_constitution.toml`
   - Provides defaults for ALL SPECs under that DNA code

2. **SPEC Parameters = Overrides + Specifics**
   - `parameters_{descriptor}.toml` can override DNA defaults
   - Plus SPEC-specific configuration

3. **Explicit Inheritance**
   - Dashboard shows inherited vs explicit values
   - CLI tool: `spec-engine resolve GCATTAGC/api` shows final config

4. **Validation**
   - Warn if override key doesn't exist in DNA defaults
   - Validate resolved configuration before execution

5. **File-First**
   - Files are source of truth
   - Database caches for UI performance
   - Sync service keeps them aligned

---

## Next Steps

### Phase 1: Add Cascade Support (No UI Changes Yet)

1. Enhance `project_constitution.toml` parser to recognize `[defaults]` section
2. Build merge function: `resolveConfig(dnaCode, descriptor)`
3. Use resolved config for SPEC execution
4. Verify backward compatibility (existing SPECs without DNA defaults work)

### Phase 2: Dashboard Support

1. DNA Profile viewer shows defaults
2. SPEC parameter editor shows:
   - Inherited values (grayed out)
   - Explicit overrides (editable)
   - Toggle "Override DNA Default" per field
3. Visual indicator: "testing: standard (inherited from DNA)"

### Phase 3: Advanced Features

1. Multi-environment DNA profiles (dev/staging/prod)
2. DNA profile templates
3. Validation of resolved configurations
4. Diff tool (show what SPEC overrides from DNA)

---

## Conclusion

**The cascade pattern you accidentally built has significant value.**

It aligns with:
- Industry-standard configuration patterns (Docker, K8s, ESLint)
- DRY principle
- Separation of concerns (project-level vs SPEC-level settings)

**The key insight:**
- DNA Profile should be **project defaults**, not individual file metadata
- SPECs inherit and override as needed
- Dashboard manages this cascade explicitly

**The fix:**
- Keep the cascade concept
- Correct the file structure interpretation
- Add explicit inheritance UI support

This turns the "mistake" into a valuable feature enhancement of the SPEC Engine framework.
