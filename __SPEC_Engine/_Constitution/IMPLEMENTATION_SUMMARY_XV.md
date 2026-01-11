# Article XV Implementation Summary

**Biological Insight → Practical Implementation**

---

## The Core Insight (Keep This Internal)

The biological model revealed:
1. **Immune System** = Learn from past mistakes
2. **Environmental Sensing** = Probe before building
3. **Morphogenesis** = Let solutions emerge from constraints
4. **Epigenetics** = Context-dependent behavior

## The Practical Translation (Use This)

1. **Pattern Recognition** - Learned constraints from divergences
2. **Pre-flight Checks** - Scan environment before execution
3. **Guidance Principles** - Heuristics, not rigid steps
4. **Context Profiles** - Execution adapts to project stage

---

## What Actually Changes

### Minimal Changeset: 3 Files, 3 New Sections

#### 1. Update `parameters_template.toml`

**Add 3 optional sections:**

```toml
# ====================================================================
# NEW: Pattern Recognition (Optional)
# ====================================================================

[learned_constraints]
# Prevent repeating past mistakes
enabled = false  # Set true to enable pattern checking

# Example patterns added by humans after divergence analysis:
# [[learned_constraints.pattern]]
# id = "check_existing_before_create"
# description = "When building interface for existing data, verify data location first"
# applies_when = ["file_system_integration", "management_terminology"]
# guidance = "Probe filesystem. If data exists → Browse interface. If not → Create interface."
# learned_from = "Dashboard_SPEC_v1.0"
# severity = "high"  # Options: critical, high, medium, low

# ====================================================================
# NEW: Pre-flight Environment Scanning (Optional)
# ====================================================================

[pre_flight]
enabled = false  # Set true to enable environment scanning before execution

# Example checks:
# [[pre_flight.checks]]
# type = "filesystem_scan"
# paths = ["SPECs/*/", "data/"]
# purpose = "Detect existing data structures before designing interface"
# report = true

# [[pre_flight.checks]]
# type = "terminology_disambiguation"
# ambiguous_terms = ["management", "interface", "profile"]
# require_clarification = true

# ====================================================================
# NEW: Guidance Principles (Optional)
# ====================================================================

[guidance]
# High-level heuristics that guide decision-making when steps lack detail
# Executor applies these when ambiguity detected

enabled = false  # Set true to enable guidance principles

# Standard principles (inherited by default):
# - Seek existing structures before creating new
# - File system is source of truth when integration required
# - Simplest solution that satisfies constraints
# - Explicit over implicit (never assume, always verify)
# - CRUD vs Browse must be explicit

# Add SPEC-specific principles here:
principles = []

# Example:
# principles = [
#     "Database is metadata cache only, not primary storage",
#     "Integration requires environment probe before interface design"
# ]
```

**Location:** `__SPEC_Engine/_templates/parameters_template.toml`

**Backward compatibility:** All sections optional. If missing, current behavior.

---

#### 2. Update `project_constitution.toml` template

**Extend `[execution]` section:**

```toml
[execution]
default_mode = "dynamic"
escalation_threshold = 3
confidence_threshold = 0.6

# NEW: Context-aware execution (Optional)
[execution.context]
environment = "prototype"  # Options: prototype, production, learning, maintenance
stage = "early"           # Options: early, mature, declining
risk_exposure = "low"     # Options: low, medium, high

# Context automatically adjusts:
# - Prototype+Early: more autonomous, faster, lower validation
# - Production+Mature: more cautious, slower, higher validation
# Manual SPEC parameters always override these adjustments
```

**Add project-level learned constraints:**

```toml
# NEW: Project-specific learned patterns (Optional)
[learned_constraints]
enabled = false

# Patterns accumulate as project encounters divergences
# Example:
# [[learned_constraints.pattern]]
# id = "project_specific_pattern"
# description = "..."
# applies_when = [...]
# guidance = "..."
# learned_from = "SPEC_ID"
```

**Location:** `__SPEC_Engine/_DNA/DNA_SPEC.md` template output

---

#### 3. Add Article XV to Constitution

**Location:** `__SPEC_Engine/_Constitution/constitution.md`

**Integration:** Append Article XV after existing articles

**Cross-references:**
- Update Article I Section 1.3: Add note about solution correctness
- Update Article XIV Section 14.3: Add architectural validation check
- Update `exe_template.md` Section 1.1: Add pre-flight check step

---

## New Template Files (2)

#### 4. DIVERGENCE_ANALYSIS.md Template

```markdown
# SPEC Divergence Analysis

**SPEC:** [descriptor]  
**Version:** [v1.0]  
**Date:** [YYYY-MM-DD]  
**Status:** Critical architectural flaw discovered

---

## What Was Built

[Describe actual implementation]

## What Should Exist

[Describe correct interpretation of requirements]

## Root Cause Analysis

### Why Divergence Occurred
1. [Ambiguity in SPEC language]
2. [Missing constraints]
3. [Incorrect assumptions]

### Contributing Factors
- [Architectural guidance missing]
- [Terminology ambiguity]
- [Environmental context not probed]

## Impact Assessment

### Affected Components
- [HIGH] Component X (complete rewrite)
- [MEDIUM] Component Y (partial changes)
- [LOW] Component Z (minimal impact)

### Effort Estimation
- Remediation: [X SPECLets / Y weeks]
- Testing: [estimate]
- Migration: [estimate]

## Remediation Path

### Strategy
- **PRESERVE:** [What to keep]
- **REBUILD:** [What to rewrite]
- **REFACTOR:** [What to modify]

### Next Steps
1. Create `spec_REMEDIATE_{descriptor}.md`
2. Version bump to v2.0
3. Document learned patterns
4. Execute remediation SPEC

## Learned Patterns

### Patterns to Add
```toml
[[learned_constraints.pattern]]
id = "[unique_id]"
description = "[what this prevents]"
applies_when = ["[condition1]", "[condition2]"]
guidance = """
[what to do instead]
"""
learned_from = "[this SPEC ID]"
severity = "high"
```

### Constitutional Feedback
- [What guidance should Article XV include?]
- [What SPEC template improvements needed?]

---

**Status:** Awaiting remediation SPEC creation
```

**Location:** `__SPEC_Engine/_templates/DIVERGENCE_ANALYSIS_template.md`

---

#### 5. MIGRATION_GUIDE.md Template

```markdown
# Migration Guide: [SPEC] v[old] → v[new]

**SPEC:** [descriptor]  
**From:** v[1.0]  
**To:** v[2.0]  
**Date:** [YYYY-MM-DD]

---

## Breaking Changes

### Architectural Shift
- **Before:** [database-first]
- **After:** [file-system-first]

### Component Changes
1. **[Component Name]**
   - Old: [description]
   - New: [description]
   - Action: [rewrite/refactor/preserve]

## Migration Strategy

### Phase 1: Audit (1 day)
- [ ] List all affected components
- [ ] Identify dependencies
- [ ] Backup current state

### Phase 2: Rebuild (X days)
- [ ] Implement corrected architecture
- [ ] Preserve working components
- [ ] Update dependencies

### Phase 3: Validation (1 day)
- [ ] Verify architectural correctness
- [ ] Test integration points
- [ ] Confirm constraints satisfied

## Rollback Plan

If remediation fails:
1. [Restore from backup]
2. [Revert to v1.0]
3. [Document failure reason]

## Success Criteria

- [ ] Architectural intent matched
- [ ] Integration points verified
- [ ] Divergence resolved
- [ ] Learned patterns documented
```

**Location:** `__SPEC_Engine/_templates/MIGRATION_GUIDE_template.md`

---

## Integration with Execution Flow

### Current Execution: exe_template.md Section 1.1

**Add to pre-flight checks:**

```markdown
### Step 1.11: Pattern Recognition Check (NEW - Optional)

**If `[learned_constraints].enabled = true` in parameters or DNA profile:**

1. **Load learned patterns:**
   - From DNA profile: `SPECs/{DNA_CODE}/project_constitution.toml`
   - From global repo: `__SPEC_Engine/_Constitution/learned_patterns.toml`

2. **Scan current SPEC for condition matches:**
   - Parse SPEC terminology
   - Check constraint declarations
   - Identify integration requirements

3. **If pattern match detected:**
   - **Severity: Critical/High** → HALT execution
   - **Severity: Medium/Low** → WARN user
   - Display pattern guidance
   - Prompt: "Continue? [yes/no]"

**Example Output:**
```
⚠ PATTERN MATCH DETECTED (HIGH SEVERITY)
Pattern: "database_before_filesystem_check"
Applies when: file_system_integration + management_interface
Learned from: Dashboard_SPEC_v1.0

Guidance: Probe filesystem for existing data before designing interface.
If data exists on disk → Build browse interface (not CRUD)

Continue? [yes/no]
```

### Step 1.12: Pre-flight Environment Scan (NEW - Optional)

**If `[pre_flight].enabled = true` in parameters:**

1. **Execute configured scans:**
   - Filesystem scans (check for existing structures)
   - Terminology disambiguation (clarify ambiguous terms)
   - Constraint validation (verify all required info present)

2. **Report findings:**
   ```
   🔍 Pre-flight Scan Results
   
   Filesystem: Found 3 existing DNA profiles in SPECs/*/
   Terminology: "management" is ambiguous - CRUD or Browse?
   Constraints: File system integration required
   
   Recommendation: Probe existing files before interface design
   ```

3. **Halt if critical ambiguity unresolved**

### Step 1.13: Load Guidance Principles (NEW - Optional)

**If `[guidance].enabled = true`:**

1. Load standard principles (inherited)
2. Load SPEC-specific principles from parameters
3. Store in executor context for decision-making

**When applied:** Executor consults principles when:
- Step lacks detailed method
- Multiple valid approaches exist
- Ambiguity detected during execution
```

**Location:** Update `__SPEC_Engine/_templates/exe_template.md`

---

## No Linguistic Changes Needed

### Keep All Existing Terminology
- SPEC, SPECLet, Task, Step, Backup ✓
- DNA codes ✓
- Critical balance ✓
- Execution modes (Silent, Dynamic, Collaborative) ✓
- All Constitutional Articles ✓

### Internal Concept → External Interface

| Biological Concept | Public Interface Name |
|-------------------|----------------------|
| Immune system | Pattern Recognition |
| Antigens | Learned Constraints |
| Antibodies | Pattern Guidance |
| Morphogenesis | Emergent Solutions |
| Epigenetics | Context Profiles |
| Environmental sensing | Pre-flight Checks |
| Growth rules | Guidance Principles |

**Philosophy:** Think biologically, speak pragmatically.

---

## Backward Compatibility Guarantee

### For Existing SPECs
All new features are **optional sections**:
- If `[learned_constraints]` missing → No pattern checking (current behavior)
- If `[pre_flight]` missing → No environment scan (current behavior)
- If `[guidance]` missing → Standard step-by-step execution (current behavior)

Old SPECs continue working **exactly as before**.

### For External Tools
No changes to:
- File naming conventions (spec_*, parameters_*, exe_*)
- JSON output format (progress_*.json)
- Directory structure (SPECs/{DNA_CODE}/)
- DNA code generation
- TOML syntax or structure (only new optional sections)

External tools that parse SPEC_Engine files remain compatible.

---

## Implementation Priority

### Phase 0: Critical (Week 1)
1. Draft Article XV (✓ Done)
2. Create DIVERGENCE_ANALYSIS template
3. Test on Dashboard SPEC remediation

### Phase 1: Core Features (Weeks 2-4)
1. Add `[learned_constraints]` to parameters template
2. Implement pattern checking in exe_template Section 1.11
3. Update DNA_SPEC to output `[execution.context]`

### Phase 2: Enhancement (Weeks 5-8)
1. Add `[pre_flight]` to parameters template
2. Implement environment scanning in exe_template Section 1.12
3. Create MIGRATION_GUIDE template

### Phase 3: Guidance System (Weeks 9-12)
1. Add `[guidance]` to parameters template
2. Implement principle loading in exe_template Section 1.13
3. Update Commander to prompt for guidance principles

---

## Success Metrics

### For Users
- Divergences detected **before** implementation (not after)
- Past mistakes prevent similar future errors
- SPECs self-improve over time
- Clear migration path when pivots needed

### For Framework
- Pattern library grows from real divergences
- Constitutional Articles evolve based on evidence
- Backward compatibility maintained
- External tool compatibility preserved

---

**Summary:** Extract biological insight, implement pragmatically, keep interface clean.

**No LARP, all utility.**
