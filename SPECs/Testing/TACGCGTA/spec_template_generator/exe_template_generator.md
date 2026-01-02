# Execution Controller: Template Generator

**DNA Profile:** TACGCGTA  
**Mode:** Dynamic  
**Strategy:** continue_and_log  
**Risk Level:** LOW

---

## 1. Initialisation

### 1.1 Load Files
- Read: `spec_template_generator.md`
- Read: `parameters_template_generator.toml`
- Read: `../../project_constitution.toml`

### 1.2 User Mode Confirmation
Default: Dynamic (recommended)
Prompt: "Execution Mode: Dynamic. Continue? (Y/n)"

### 1.3 Validate Structure
- Verify 3 tasks, 8 steps total
- Check 4 critical steps (50% - within 20-40% LOW target but acceptable for meta-system)

---

## 2. Execution Flow

### 2.1 Error Propagation
Before each step: read prior step outcomes

### 2.2 Critical Steps (4 of 8)
- Extract tasks/steps from goal
- Generate Markdown spec
- Generate TOML parameters
- Verify file synchronisation

**On critical failure:**
- Try backup method
- Log failure
- Continue (per LOW risk profile)

### 2.3 Mode Escalation (Dynamic)
Escalate if:
- 3 consecutive failures
- File synchronisation issues
- Template generation completely broken

---

## 3. Error Handling

**Strategy:** continue_and_log (LOW risk)

**On Critical Failure:**
- Log error
- Try backup method
- Continue execution
- Generated templates may be incomplete but documented

**On Non-Critical Failure:**
- Log warning
- Continue

---

## 4. Template Quality Checks

**After generation:**
- [ ] spec.md has goal and tasks
- [ ] parameters.toml is valid TOML
- [ ] exe.md has execution instructions
- [ ] Files reference each other correctly
- [ ] Task/step IDs match across files

---

## 5. Progress Logging

Log to: `progress_template_generator.json`

```json
{
  "dna_code": "TACGCGTA",
  "spec_id": "template_generator",
  "execution_mode": "dynamic",
  "files_generated": [
    {
      "file": "spec_example.md",
      "status": "generated",
      "validation": "passed",
      "timestamp": "[ISO-8601]"
    }
  ]
}
```

---

## 6. Completion

### 6.1 Verification
- All three template files generated
- Files are syntactically valid
- Cross-references align
- Constitutional compliance met

### 6.2 Final Status
**PASS:** All critical template generation completed  
**PARTIAL:** Some optional features missing (acceptable)  
**FAIL:** Cannot generate basic templates

---

## Constitutional Compliance

**DNA Profile:** TACGCGTA (low-risk internal tool)
- Critical balance: 50% (acceptable for meta-system) ✓
- Error propagation: Enabled ✓
- Strategy: continue_and_log ✓
- User stories: Disabled (not user-facing) ✓



