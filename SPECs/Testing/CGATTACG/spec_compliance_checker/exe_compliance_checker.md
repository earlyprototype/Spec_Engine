# Execution Controller: FDA Compliance Checker

**DNA Profile:** CGATTACG  
**Mode:** Collaborative (MANDATORY)  
**Strategy:** halt_on_critical  
**Risk Level:** HIGH

---

## 1. Initialisation

### 1.1 Load Files
- Read: `spec_compliance_checker.md`
- Read: `parameters_compliance_checker.toml`
- Read: `../../project_constitution.toml`

### 1.2 HIGH RISK ENFORCEMENT
**This is a HIGH-RISK medical compliance project.**
- Collaborative mode is MANDATORY
- Cannot proceed without human oversight
- All critical failures HALT execution immediately

### 1.3 Validate Structure
- Verify 3 tasks, 9 steps total
- Check 8 critical steps (89% - HIGH RISK)
- Confirm regulatory compliance requirements

---

## 2. Execution Flow

### 2.1 Critical Steps (8 of 9)
**EVERY critical step requires:**
1. Human approval before execution
2. Verification after execution
3. Regulatory compliance check
4. Audit log entry

### 2.2 Halt on Critical Failure
**If ANY critical step fails:**
- STOP all execution immediately
- Log failure with full details
- Alert human operator
- Await decision: abort or manual fix
- DO NOT CONTINUE automatically

---

## 3. Medical Compliance Checks

**Before each task:**
- [ ] FDA regulation database loaded and current
- [ ] Compliance validation logic tested
- [ ] Audit trail active
- [ ] No medical decisions made without validation

**After each task:**
- [ ] Compliance report accurate
- [ ] Violations correctly identified
- [ ] All operations logged

---

## 4. Progress Logging

Log to: `progress_compliance_checker.json` (VERBOSE mode)

```json
{
  "dna_code": "CGATTACG",
  "risk_level": "HIGH",
  "spec_id": "compliance_checker",
  "execution_mode": "collaborative",
  "regulatory_checks": [
    {
      "regulation_id": "FDA-21CFR820",
      "compliance_status": "validated",
      "human_verified": true,
      "timestamp": "[ISO-8601]"
    }
  ]
}
```

---

## 5. Completion

### 5.1 Regulatory Verification
- FDA regulation database complete
- Compliance validation accurate
- Violation detection tested
- Audit trail complete

### 5.2 Final Status
**PASS:** All critical medical compliance requirements met  
**FAIL:** Any critical step failed (execution halted)

---

## Constitutional Compliance

**DNA Profile:** CGATTACG (high-risk medical)
- Critical balance: 89% (HIGH RISK) ✓
- Mode: Collaborative (mandatory) ✓
- Strategy: halt_on_critical ✓
- Compliance: FDA, HIPAA ✓



