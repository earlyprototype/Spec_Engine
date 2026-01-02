# exe_WTF.md

**Version:** 1.0  
**Last Updated:** 2 January 2026  
**Purpose:** Execution controller for WTF (What's This Feature) code archaeology

---

## Execution Model

This executor follows the standard SPEC Engine execution model defined in `__SPEC_Engine/_templates/exe_template.md` with WTF-specific customizations documented below.

**Standard Sections (use template):**
- Section 1: Initialization and Validation
- Section 2: Execution Flow
- Section 3: Mode Control
- Section 4: Error Handling
- Section 5: Completion
- Section 6: Post-Execution Analysis

**WTF-Specific Customizations:**
- Section 0: Target Code Identification (before standard Section 1)
- Section 2.8: Archaeology-Specific Validation (after each task)

---

## Section 0: Target Code Identification (WTF-Specific)

**Execute BEFORE Section 1 (Initialization):**

### Purpose
Feature archaeology requires clear target specification. Unlike build/create specs where the output is created, WTF analyses existing code that must be identified upfront.

### Process

1. **Check for target specification:**
   - Look for user-provided file paths or module names
   - Check if scope is defined (specific function/class vs entire module)

2. **If target is specified:**
   ```json
   {
     "target_code": {
       "files": ["lib/auth/session_manager.py"],
       "scope": "SessionManager class",
       "context": "Need to understand how session expiry works",
       "boundary_defined": true
     }
   }
   ```
   - Log target specification
   - Verify files/modules exist and are readable
   - Proceed to Section 1 (standard initialization)

3. **If target is NOT specified:**
   - **ESCALATE to collaborative mode immediately**
   - **HALT standard execution flow**
   - **Present target identification prompt:**

   ```
   [WTF SETUP - Target Identification Required]
   
   WTF (What's This Feature) requires identifying the mysterious code you want documented.
   
   Please provide:
   
   1. File path(s) or module name(s)
      Example: "src/lib/auth/session_manager.py"
      Example: "com.example.auth.SessionManager"
   
   2. Specific scope (if known)
      Example: "SessionManager class" or "login() function"
      Example: "Entire module" or "Just the authentication flow"
   
   3. Context - Why is this mysterious?
      Example: "Inherited legacy code, no docs, session expiry confusing"
      Example: "Need to modify but don't understand current behaviour"
   
   Enter target specification:
   ```

4. **Capture user input:**
   - Parse file paths/module names
   - Record scope definition
   - Store context for archaeology focus
   - Validate that target code exists and is accessible

5. **Log target specification:**
   ```json
   {
     "target_code": {
       "files": ["<user_provided>"],
       "scope": "<user_provided>",
       "context": "<user_provided>",
       "boundary_defined": true,
       "target_identified_at": "<ISO-8601>"
     }
   }
   ```

6. **Verify accessibility:**
   - Confirm files exist and are readable
   - If files don't exist: re-prompt with error message
   - If files exist: proceed to Section 1 (standard initialization)

### Why This Matters

**Problem:** Generic execution templates assume the work scope emerges during execution. Archaeology requires the scope upfront to avoid analyzing entire codebases.

**Solution:** Mandatory target identification before standard execution begins prevents wasted effort and ensures focused analysis.

---

## Section 2.8: Archaeology-Specific Validation (WTF-Specific)

**Execute AFTER each task completion (in addition to standard Section 2 logic):**

### Purpose
Verify archaeology quality standards are met before proceeding to next task.

### After Task 1 (Code Survey):
- **Check:** Can you explain the feature's structure to a colleague?
- **Validation:** Entry points list is complete (verified by checking no new entry points in Task 2)
- **If NO:** Return to Task 1, expand survey scope

### After Task 2 (Behaviour Analysis):
- **Check:** Can you predict the feature's behaviour for new inputs?
- **Validation:** Execution paths cover main scenarios (at least 2 common paths documented)
- **If NO:** Return to Task 2, trace additional scenarios

### After Task 3 (Dependency Mapping):
- **Check:** Do you know what would break if this feature changed?
- **Validation:** Both upstream and downstream dependencies identified
- **If NO:** Return to Task 3, expand dependency search

### After Task 4 (Documentation Generation):
- **Check:** Could someone maintain this feature using your documentation?
- **Validation:** Usage examples are executable or clearly marked as pseudocode
- **If NO:** Return to Task 4, improve documentation clarity

### Validation Process

```
1. Read current task output from progress.json
2. Check validation criteria for completed task
3. If validation passes:
   - Log validation success
   - Proceed to next task
4. If validation fails:
   - Log validation failure with specific gap
   - Switch to collaborative mode
   - Present gap to user:
     "[WTF VALIDATION FAILED - Task X]
      Validation check: [check_description]
      Gap identified: [specific_gap]
      
      Options:
      1. Return to Task X with expanded scope
      2. Accept current depth and proceed (document limitation)
      3. Manual review and confirmation
      
      Recommend: Option 1 (ensure thoroughness)
      Choose option:"
   - Execute user's decision
```

### Rationale

**Problem:** Generic specs can mark tasks complete without checking archaeology-specific quality (e.g., documentation that technically exists but is useless).

**Solution:** Task-specific validation questions ensure documentation quality meets "maintainability" standard, not just "existence" standard.

---

## WTF-Specific Constraints

In addition to standard constitutional constraints:

1. **Read-Only Operation**
   - NO code modifications during archaeology
   - Verify at each step that no files are being edited
   - If code modification detected: HALT and escalate

2. **Evidence-Based Claims**
   - All documentation claims MUST be verified against actual code
   - No assumptions or guesses
   - If behaviour is unclear: document uncertainty explicitly

3. **Comprehensive Coverage**
   - ALL entry points must be documented (not just obvious ones)
   - Verify no hidden entry points exist before marking Task 1 complete

4. **Plain English Requirement**
   - Documentation MUST be understandable by humans unfamiliar with code
   - Avoid jargon without definition
   - Test: Could a new team member maintain the code using this documentation?

---

## Logging Enhancements for Archaeology

In addition to standard progress.json logging, WTF adds:

```json
{
  "archaeology_metadata": {
    "target_code": {
      "files": ["list of analysed files"],
      "total_lines": 1234,
      "languages": ["python", "javascript"],
      "entry_points_found": 7,
      "dependencies_upstream": 12,
      "dependencies_downstream": 3
    },
    "analysis_depth": {
      "execution_paths_documented": 3,
      "data_structures_mapped": 8,
      "side_effects_identified": 5,
      "error_handlers_documented": 4
    },
    "documentation_generated": {
      "overview_paragraphs": 4,
      "usage_examples": 5,
      "known_issues": 2,
      "integration_guide_sections": 6
    }
  }
}
```

This metadata enables post-execution assessment of documentation comprehensiveness.

---

## Integration with Standard Execution

**WTF execution flow:**

```
0. Target Code Identification (WTF-specific)
   ↓
1. Initialization and Validation (standard, Section 1)
   ↓
2. Execution Flow (standard, Section 2)
   ├─ Task 1 → Task-specific validation (2.8)
   ├─ Task 2 → Task-specific validation (2.8)
   ├─ Task 3 → Task-specific validation (2.8)
   └─ Task 4 → Task-specific validation (2.8)
   ↓
3. Mode Control (standard, Section 3)
   ↓
4. Error Handling (standard, Section 4)
   ↓
5. Completion (standard, Section 5)
   ↓
6. Post-Execution Analysis (standard, Section 6)
```

**All standard sections from exe_template.md apply unless explicitly overridden above.**

---

## Reference Documents

- **Standard Execution Logic:** `__SPEC_Engine/_templates/exe_template.md`
- **SPEC Definition:** `WTF_SPEC.md`
- **Parameters:** `parameters_WTF.toml`
- **Constitution:** `__SPEC_Engine/_Constitution/constitution.md`
- **Design Philosophy:** `__SPEC_Engine/_Constitution/DESIGN_PHILOSOPHY.md`

---

**End of exe_WTF.md**

*This execution controller implements WTF-specific archaeology logic while inheriting standard SPEC Engine execution patterns. For complete execution details, consult exe_template.md.*
