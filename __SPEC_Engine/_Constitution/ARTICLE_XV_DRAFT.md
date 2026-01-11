# Article XV: Pattern Recognition & Architectural Adaptation

**Version:** 1.0 Draft  
**Date:** 2 January 2026  
**Purpose:** Handle fundamental design flaws discovered during or after implementation

---

## Context

SPECs can achieve their stated goal while implementing the **wrong solution**. This happens when:
- Requirements are ambiguous and misinterpreted
- Constraints are implicit rather than explicit
- Architecture emerges from wrong assumptions
- Implementation diverges from intent despite successful execution

**Example:** Dashboard SPEC built a database-backed CRUD app when file-system browser was needed. Goal technically "achieved" but fundamentally wrong architecture.

This Article establishes mechanisms to:
1. Detect divergence between intent and implementation
2. Learn from past mistakes to prevent recurrence
3. Manage architectural pivots mid-implementation
4. Preserve knowledge across SPEC versions

---

## Section 15.1: Divergence Detection

### 15.1.1 When to Trigger
Create `DIVERGENCE_ANALYSIS.md` when:
- Goal achieved but wrong solution delivered
- Fundamental architecture incompatible with constraints
- Post-completion realization of design flaw
- Source of truth misidentified
- Interface type mismatch (CRUD vs Browse, etc.)

### 15.1.2 Required Analysis
`DIVERGENCE_ANALYSIS.md` MUST document:
1. **What was built** - Actual implementation
2. **What should exist** - Correct interpretation
3. **Root cause** - Why divergence occurred
4. **Impact assessment** - What's affected
5. **Remediation path** - How to correct

### 15.1.3 Halt Condition
Implementation MUST pause when divergence discovered, regardless of "completion" status.

---

## Section 15.2: Pattern Recognition System

### 15.2.1 Purpose
Prevent repeating mistakes by encoding learned constraints from past divergences.

### 15.2.2 Storage Location
- **Project-level:** `SPECs/{DNA_CODE}/project_constitution.toml`
- **Global:** `__SPEC_Engine/_Constitution/learned_patterns.toml`

### 15.2.3 Pattern Structure
```toml
[[learned_constraints.pattern]]
id = "unique_identifier"
description = "What mistake this prevents"
applies_when = ["condition1", "condition2"]
guidance = "What to do instead"
learned_from = "SPEC_ID where divergence occurred"
severity = "critical|high|medium|low"
```

### 15.2.4 Pre-flight Integration
Executor MUST check learned patterns during Section 1.1 initialization:
1. Load patterns from DNA profile
2. Load patterns from global repository
3. Scan current SPEC for matching conditions
4. **WARN** (medium/low) or **HALT** (critical/high) if match found

**Example Output:**
```
⚠ PATTERN MATCH DETECTED (HIGH SEVERITY)
Pattern: "database_before_filesystem_check"
Condition: SPEC mentions "file_system_integration" + "management interface"
Learned from: Dashboard_SPEC_v1.0

Guidance: Before designing interface, probe filesystem for existing data.
Question: Does data already exist on disk?

Continue? [yes/no]
```

---

## Section 15.3: Pre-flight Environment Scanning

### 15.3.1 Purpose
Probe environment **before** building to detect existing structures.

### 15.3.2 When Required
Enable pre-flight scanning when SPEC mentions:
- Integration with existing systems
- File system operations
- Database + file system together
- "Management" without explicit CRUD/Browse clarification

### 15.3.3 Scan Configuration
In `parameters_[descriptor].toml`:
```toml
[pre_flight]
enabled = true

[[pre_flight.checks]]
type = "filesystem_scan"
paths = ["SPECs/*/", "__SPEC_Engine/", "data/"]
purpose = "Detect existing data structures"
report_findings = true

[[pre_flight.checks]]
type = "terminology_disambiguation"
ambiguous_terms = ["management", "interface", "profile"]
require_clarification = true
halt_until_resolved = true
```

### 15.3.4 Integration with Execution
Executor runs pre-flight checks in Section 1.1 **before** task planning:
1. Execute filesystem scans
2. Parse constraint ambiguities
3. Prompt for clarifications if needed
4. Report findings to user
5. Proceed only after resolution

---

## Section 15.4: Guidance Principles

### 15.4.1 Purpose
Provide high-level heuristics when SPEC lacks prescriptive steps.

### 15.4.2 When Applied
Guidance principles activate when:
- Step lacks detailed method
- Multiple valid approaches exist
- Environment probing needed
- Ambiguity detected

### 15.4.3 Standard Principles
All SPECs inherit these defaults:
1. **Seek existing before creating new** - Probe for existing structures first
2. **File system is source of truth** - When integrating with files
3. **Simplest solution wins** - Choose minimal complexity
4. **Explicit over implicit** - Never assume, always verify
5. **CRUD vs Browse must be explicit** - Never infer from "management"

### 15.4.4 SPEC-Specific Principles
Add to `parameters_[descriptor].toml`:
```toml
[guidance]
principles = [
    "Database is metadata cache only, not primary storage",
    "Read existing .toml files before designing interface",
    "Integration requires environment probe first"
]
apply_when = "ambiguity_detected"
```

---

## Section 15.5: SPEC Versioning

### 15.5.1 Version Semantics
- **v1.0 → v1.1** - Clarification, no breaking changes
- **v1.0 → v2.0** - Breaking change, architectural redesign
- **v1.0 → v1.0.1** - Bug fix, implementation correction

### 15.5.2 Version Bump Triggers
Increment major version (v2.0) when:
- Fundamental architecture changes
- Source of truth relocated
- Interface paradigm shifts (CRUD → Browse)
- Dependencies substantially altered

### 15.5.3 Required Documentation
For major version bumps, create:
1. `spec_{descriptor}_v2.0.md` - Corrected SPEC
2. `parameters_{descriptor}_v2.0.toml` - Updated config
3. `DIVERGENCE_v1.0_to_v2.0.md` - What changed and why
4. `MIGRATION_v1.0_to_v2.0.md` - How to migrate implementation

### 15.5.4 Version History
Track in `parameters_[descriptor].toml`:
```toml
[meta]
version = "2.0"
previous_version = "1.0"

[[version_history]]
version = "1.0"
date = "2026-01-01"
status = "deprecated"
deprecated_reason = "database_as_source_of_truth antipattern"

[[version_history]]
version = "2.0"
date = "2026-01-02"
changes = "Corrected to file-system-first architecture"
breaking_changes = true
```

---

## Section 15.6: Remediation SPECs

### 15.6.1 When Required
Create `spec_REMEDIATE_{descriptor}.md` for:
- Fixing fundamentally flawed implementations
- Migrating v1.0 → v2.0 architectures
- Correcting divergences

### 15.6.2 Required Sections
Remediation SPECs MUST include:
1. **Original Flaw** - Reference to DIVERGENCE_ANALYSIS
2. **Corrected Understanding** - What should have been built
3. **Migration Strategy** - Preserve/Rebuild/Hybrid approach
4. **Rollback Plan** - How to revert if remediation fails
5. **Validation Criteria** - How to verify fix is correct

### 15.6.3 Execution Mode
Remediation SPECs default to **collaborative mode** due to high-risk changes.

---

## Section 15.7: Context-Aware Execution

### 15.7.1 Purpose
Adjust execution behavior based on project stage and environment.

### 15.7.2 Context Declaration
In `project_constitution.toml`:
```toml
[execution.context]
environment = "prototype"  # or: "production", "learning", "maintenance"
stage = "early"           # or: "mature", "declining"
risk_exposure = "low"     # or: "medium", "high"
```

### 15.7.3 Automatic Adjustments
Executor adjusts behavior based on context:

**Prototype + Early:**
- More autonomous (higher escalation threshold)
- Fewer critical steps (lower percentage)
- Divergence tolerance: medium (learning phase)

**Production + Mature:**
- More cautious (lower escalation threshold)
- More critical steps (higher percentage)
- Divergence tolerance: low (stability phase)

### 15.7.4 Manual Override
Context adjustments are recommendations. Individual SPEC parameters take precedence.

---

## Section 15.8: Compliance & Validation

### 15.8.1 Pre-flight Validation
Executor MUST verify in Section 1.1:
- [ ] Learned patterns checked for matches
- [ ] Pre-flight scans completed (if enabled)
- [ ] Ambiguous terminology clarified
- [ ] Guidance principles loaded

### 15.8.2 Post-execution Validation
Even when goal "ACHIEVED", verify:
- [ ] Implementation matches architectural intent
- [ ] No fundamental misunderstandings exist
- [ ] Source of truth correctly identified
- [ ] Interface type matches requirements

If divergence detected → Trigger Section 15.1

### 15.8.3 Constitutional Feedback Loop
Divergence analyses feed back into Constitution:
1. Extract patterns from DIVERGENCE_ANALYSIS.md
2. Add to learned_patterns.toml
3. Update Article XV guidance if pattern recurring
4. Improve SPEC template ambiguities

---

## Rationale

### Why This Matters
Traditional validation checks **goal achievement** but not **solution correctness**. 
A SPEC can be "successfully executed" while implementing the wrong architecture.

### Learning System
Unlike static validation, this Article creates a **learning system**:
- Each divergence teaches the framework
- Future SPECs benefit from past mistakes
- Pattern recognition improves over time
- Constitutional Articles evolve based on evidence

### Integration with Existing Articles
- **Article I (North Star):** Clarifies that goal achievement ≠ correct solution
- **Article VI (Critical Steps):** Adds pre-flight checks as critical validation
- **Article XIV (Completeness):** Extends definition to include architectural correctness

---

## Examples

### Example 1: Dashboard SPEC Pattern
**Learned Pattern:**
```toml
[[learned_constraints.pattern]]
id = "database_before_filesystem_check"
description = "When integrating with existing file structures, probe filesystem first"
applies_when = ["file_system_integration", "management_interface_mentioned"]
guidance = """
1. Run: ls SPECs/*/project_constitution.toml
2. Question: Does data already exist on disk?
3. If YES → Build browse/view interface (not CRUD)
4. If NO → Build creation interface
5. Explicitly document: Database is metadata cache only
"""
learned_from = "Dashboard_SPEC_v1.0"
severity = "high"
```

### Example 2: Context-Aware Execution
**DNA Profile Evolution:**
```toml
# Early prototype phase
[execution.context]
environment = "prototype"
stage = "early"
# Result: critical_percentage = 0.30, escalation_threshold = 5

# After 3 months, update:
[execution.context]
environment = "production"
stage = "mature"
# Result: critical_percentage = 0.55, escalation_threshold = 3
```

### Example 3: Pre-flight Detection
**Before execution:**
```
🔍 Pre-flight Environment Scan

Filesystem Scan:
✓ Found: SPECs/GCATTAGC/project_constitution.toml
✓ Found: SPECs/ATGCTAGC/project_constitution.toml
→ Conclusion: DNA profiles exist on disk

Pattern Recognition:
⚠ SPEC mentions "DNA Profile Management" + "file_system_integration"
⚠ Matches learned pattern: "database_before_filesystem_check"

Guidance Applied:
→ Data exists on filesystem
→ Interface should BROWSE existing files, not CREATE new records
→ Database role: execution history cache only

Proceed with file-system-first architecture? [yes/no]
```

---

## Implementation Checklist

### For Spec Authors
When creating SPECs:
- [ ] Check learned patterns in DNA profile
- [ ] Enable pre-flight scans if integrating with existing systems
- [ ] Disambiguate "management" terminology explicitly
- [ ] Add guidance principles for ambiguous steps
- [ ] Version SPEC properly if correcting past divergence

### For Executors (LLMs)
During execution:
- [ ] Run pre-flight checks before task planning (Section 1.1)
- [ ] Check learned patterns for condition matches
- [ ] Apply guidance principles when ambiguity detected
- [ ] Validate architectural correctness post-execution
- [ ] Create DIVERGENCE_ANALYSIS if mismatch detected

### For Framework Maintainers
System evolution:
- [ ] Extract patterns from divergence analyses
- [ ] Update learned_patterns.toml quarterly
- [ ] Review Article XV annually for improvements
- [ ] Incorporate recurring patterns into Constitution
- [ ] Maintain backward compatibility with existing SPECs

---

**Status:** DRAFT - Awaiting integration into Constitution v1.4  
**Backward Compatibility:** All features optional. Existing SPECs unaffected if new sections omitted.
