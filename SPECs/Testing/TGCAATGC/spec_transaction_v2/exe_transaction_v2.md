# Execution Controller: Charity Shop Transaction System v2

**DNA Profile:** TGCAATGC  
**Mode:** Dynamic  
**Strategy:** collaborative_review  
**Risk Level:** MODERATE

---

## 1. Initialisation

### 1.1 Load Files
- Read: `spec_transaction_v2.md`
- Read: `parameters_transaction_v2.toml`
- Read: `../../project_constitution.toml`

### 1.2 Validate DNA Compliance
- Check user stories present (required: user_facing = true) ✓
- Check critical percentage: 56% (target: 40-60%) ✓
- Check offline-first mentioned (external dependencies: payment processor) ✓
- Check GDPR compliance noted ✓

### 1.3 User Mode Confirmation
Display: "Execution Mode: Dynamic (autonomous with escalation on financial errors). Continue? (Y/n)"

### 1.4 Pre-Flight Validation
- Verify 3 tasks, 9 steps total
- Confirm 5 critical steps (payment processing, cash handling, failure handling, transaction storage, daily totals calculation)
- Check all backups described in spec match TOML
- Verify expected outputs are testable

---

## 2. Execution Flow

### 2.1 Task 1: Payment Processing Core (4 steps, all critical)

**Before starting:**
- Verify Square API credentials available (or test mode)
- Check database writeable
- Confirm error handling in place

**For each step:**
1. Read prior step outcomes from progress_transaction_v2.json
2. Execute primary method
3. Verify expected output against spec
4. If failure AND critical: try backup methods sequentially
5. If all backups fail AND critical: escalate to collaborative mode
6. Log: transaction_id, amounts, method_used, verification_passed

**Step 1.1 verification:**
- Test £1, £10, £100 transactions → all succeed
- Test £1,000,000 → validation fails
- Test declined card → specific error returned
- **CRITICAL: Financial calculation errors must be exact**

**Step 1.2 verification:**
- £10 item, £20 tendered → £10.00 change (not £9.99 or £10.01)
- £5.99 item, £10 tendered → £4.01 change exactly
- **CRITICAL: Use Decimal library, no float errors allowed**

**Error propagation:**
- If Step 1.4 (store transactions) fails, HALT - cannot proceed without transaction record

---

### 2.2 Task 2: Receipt Generation (3 steps, all non-critical)

**Before starting:**
- Verify printer connected (or skip gracefully)
- Check receipts/ directory exists and writeable
- Confirm transaction_id from Task 1 available

**Mode:** Silent (non-critical steps continue on failure)

**Step 2.3 printer handling:**
- Try primary: python-escpos
- Try backup 1: generic USB
- Try backup 2: display "Printer unavailable"
- **NON-CRITICAL:** Transaction still valid without printed receipt

---

### 2.3 Task 3: Daily Reconciliation (2 steps, 1 critical)

**Before starting:**
- Verify database contains today's transactions
- Check reports/ directory writeable

**Step 3.1 (CRITICAL):**
- Calculate cash total, card total, overall total
- Verify math: cash_total + card_total = overall_total
- **If discrepancy detected:** Escalate to collaborative mode
- Expected till cash = opening_float + cash_total

**Step 3.2 (NON-CRITICAL):**
- Generate PDF or CSV report
- Failure acceptable (manager can query database manually)

---

## 3. Mode Escalation (Dynamic)

**Escalate to collaborative mode if:**
- 3 consecutive failures in any task
- Financial calculation error (wrong change, wrong totals)
- Transaction storage fails (database corruption)
- Till reconciliation discrepancy detected

**When escalated:**
1. PAUSE execution
2. Display failure details + context
3. Show: step description, expected output, actual result, backups tried
4. Options: retry, skip (if non-critical), abort, manual fix
5. Log human decision and reasoning

---

## 4. Financial Safeguards

**Before any payment operation:**
- [ ] Amount is positive decimal (not negative, not string)
- [ ] Amount ≤ £1,000 (charity shop transaction limit)
- [ ] Currency is GBP (no conversion errors)

**After any payment operation:**
- [ ] Transaction recorded in database with unique ID
- [ ] Amount in database matches amount processed
- [ ] Timestamp is reasonable (not future, not years past)

**Daily reconciliation checks:**
- [ ] SUM(amounts) matches individual transaction sum
- [ ] No duplicate transaction IDs
- [ ] All transactions have valid payment_method

---

## 5. Progress Logging

Log to: `progress_transaction_v2.json`

**Standard fields:**
```json
{
  "dna_code": "TGCAATGC",
  "spec_id": "transaction_v2",
  "execution_mode": "dynamic",
  "start_time": "[ISO-8601]",
  "tasks": [
    {
      "task_id": 1,
      "description": "Payment Processing Core",
      "status": "completed",
      "steps": [
        {
          "step_id": 1,
          "description": "Integrate Square API",
          "status": "completed",
          "method_used": "primary",
          "verification_passed": true,
          "test_results": {
            "£1_transaction": "passed",
            "£10_transaction": "passed",
            "£100_transaction": "passed",
            "£1000000_transaction": "rejected_as_expected",
            "declined_card": "error_message_correct"
          },
          "timestamp": "[ISO-8601]"
        }
      ]
    }
  ],
  "financial_audit": {
    "total_transactions_processed": 0,
    "total_amount": "£0.00",
    "discrepancies_detected": 0
  },
  "mode_escalations": []
}
```

---

## 6. Completion & Verification

### 6.1 Payment Processing Verification
- [ ] Card payments functional (or gracefully degraded)
- [ ] Cash payments calculating change correctly
- [ ] Payment failures handled without crashes
- [ ] All transactions persisted to database

### 6.2 Receipt System Verification
- [ ] Receipt template includes all required fields
- [ ] PDF backups generated (or skipped gracefully)
- [ ] Printer working (or unavailable state handled)

### 6.3 Reconciliation Verification
- [ ] Daily totals calculation accurate
- [ ] Reports generated
- [ ] Expected till cash calculated correctly

### 6.4 Final Status

**PASS:** All critical steps completed, financial operations verified  
**PARTIAL:** Non-critical steps failed (printer, PDF) but core system works  
**FAIL:** Critical financial operations failed (payments, storage, reconciliation)

---

## Constitutional Compliance

**DNA Profile:** TGCAATGC (moderate-risk charity PoS)

- [x] Critical balance: 56% (within 40-60% target)
- [x] User stories: Present (5 stories for volunteers, managers, customers)
- [x] Error propagation: Enabled (prior steps read)
- [x] Mode: Dynamic with collaborative_review strategy
- [x] External dependencies documented: Square API, printer drivers
- [x] GDPR compliance: No personal data stored
- [x] Offline-first: Cash transactions work without network

**Quality Score:** 9/10 - Comprehensive spec with testable outputs and real-world constraints



