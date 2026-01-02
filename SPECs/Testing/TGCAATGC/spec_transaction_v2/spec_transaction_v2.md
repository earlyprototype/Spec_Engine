# Spec: Charity Shop Transaction System

**DNA Profile:** TGCAATGC 
**Version:** 2.0 (Reconstituted from DNA Profile)  
**Date:** 2025-11-02

---

## Goal

Build a complete point-of-sale transaction system for charity shop volunteers that handles cash and card payments, prints itemised receipts, tracks daily totals, and integrates with Square payment processor.

---

## Components

- Square API for card payments
- Receipt printer (thermal, 58mm)
- SQLite database for transaction records
- Python backend with simple GUI

---

## Constraints

- Must work offline for cash transactions (sync later)
- Receipt must include charity registration number
- Daily totals must reconcile with till count
- No personal data stored (GDPR compliance)
- Volunteer-friendly interface (minimal training needed)

---

## User Stories

- As a volunteer, I want to process cash sales quickly so customers aren't waiting
- As a volunteer, I want the system to calculate change automatically so I don't make mistakes
- As a volunteer, I want card payments to be simple so I'm not embarrassed if it fails
- As a manager, I want daily sales reports so I can reconcile the till
- As a customer, I want a proper receipt so I can claim Gift Aid

---

## Tasks

### Task 1: Payment Processing Core

**TOML Reference:** `tasks[0]`

- **Step 1.1:** Integrate Square API for card payments
  - **Primary method:** Use Square Python SDK, implement payment intent with amount, get approval, capture transaction
  - **Backup 1:** Use Square REST API directly if SDK has issues
  - **Backup 2:** Implement manual card entry form with Stripe as fallback processor
  - **Expected output:** Function `process_card_payment(amount, description)` returns transaction_id or error
  - **Critical:** true
  - **Mode:** silent
  - **Verification:** Test transactions of £1, £10, £100 all succeed, £1,000,000 fails validation, declined card returns specific error
  - **Logging:** Log transaction_id, amount, timestamp, payment_method to progress_transaction_v2.json

- **Step 1.2:** Implement cash payment handling
  - **Primary method:** Accept amount tendered, calculate change, record cash transaction in database
  - **Backup 1:** Use decimal library for precise currency calculations if floating point issues
  - **Expected output:** Function `process_cash_payment(amount, tendered)` returns change and transaction_id
  - **Critical:** true
  - **Mode:** silent
  - **Verification:** £10 item with £20 tendered returns £10 change exactly, £5.99 item with £10 returns £4.01, handles pence correctly
  - **Logging:** Log transaction_id, amount, change_given, timestamp

- **Step 1.3:** Handle payment failures gracefully
  - **Primary method:** Catch Square API errors, display user-friendly message, log technical details, allow retry or cancel
  - **Backup 1:** Queue failed card transactions for manual processing later if network unavailable
  - **Expected output:** Payment failure shows "Card declined - please try another card" not raw error, transaction marked as failed in DB
  - **Critical:** true
  - **Mode:** silent
  - **Verification:** Simulate network failure, card decline, timeout - all show appropriate messages and don't crash
  - **Logging:** Log failure_reason, user_message_shown, retry_count

- **Step 1.4:** Store all transactions in database
  - **Primary method:** SQLite database with transactions table: id, timestamp, amount, payment_method, status, receipt_printed
  - **Backup 1:** Write to CSV file if database locked or corrupted
  - **Expected output:** Every sale persisted, query `SELECT SUM(amount) WHERE date = today` returns daily total
  - **Critical:** true
  - **Mode:** silent
  - **Verification:** Process 10 transactions, database contains exactly 10 records, amounts match, no duplicates
  - **Logging:** Log database_path, records_inserted, any_errors

---

### Task 2: Receipt Generation & Printing

**TOML Reference:** `tasks[1]`

- **Step 2.1:** Design receipt template
  - **Primary method:** Create text-based receipt with charity header, itemised line (description, £amount), total, payment method, timestamp, charity reg number, Gift Aid message
  - **Backup 1:** Use simplified single-line receipt if formatting fails
  - **Expected output:** Receipt string formatted for 58mm thermal printer (32 characters wide)
  - **Critical:** false
  - **Mode:** silent
  - **Verification:** Receipt includes all required fields, fits 58mm width, charity reg number visible, looks professional
  - **Logging:** Log template_version, fields_included

- **Step 2.2:** Generate PDF receipt backup
  - **Primary method:** Use ReportLab to create PDF receipt, save to receipts/ folder with transaction_id filename
  - **Backup 1:** Generate HTML receipt if PDF library unavailable
  - **Backup 2:** Skip PDF generation if both fail (thermal print is primary)
  - **Expected output:** PDF file saved as receipts/TX_{transaction_id}.pdf containing same info as thermal receipt
  - **Critical:** false
  - **Mode:** silent
  - **Verification:** PDF opens correctly, all text readable, charity logo present if configured
  - **Logging:** Log pdf_path, file_size, generation_time

- **Step 2.3:** Print to thermal printer
  - **Primary method:** Send formatted receipt to USB thermal printer using python-escpos library
  - **Backup 1:** Use generic USB printing if escpos fails
  - **Backup 2:** Display "Printer unavailable - email receipt?" if printing impossible
  - **Expected output:** Physical receipt printed within 3 seconds of transaction completion
  - **Critical:** false
  - **Mode:** silent
  - **Verification:** Print test receipt, verify alignment, text clarity, no character corruption
  - **Logging:** Log printer_status, print_time, any_errors

---

### Task 3: Daily Reconciliation

**TOML Reference:** `tasks[2]`

- **Step 3.1:** Calculate daily totals by payment method
  - **Primary method:** Query database: `SELECT payment_method, SUM(amount) FROM transactions WHERE DATE(timestamp) = today GROUP BY payment_method`
  - **Backup 1:** Iterate through transactions manually if SQL GROUP BY fails
  - **Expected output:** Report showing Cash: £X, Card: £Y, Total: £Z
  - **Critical:** true
  - **Mode:** silent
  - **Verification:** Process 5 cash (£50 total) + 3 card (£75 total) transactions, report shows Cash: £50.00, Card: £75.00, Total: £125.00
  - **Logging:** Log cash_total, card_total, transaction_count, report_generated_time

- **Step 3.2:** Generate end-of-day report
  - **Primary method:** Create PDF report with daily totals, transaction count, hourly breakdown, expected till cash (opening float + cash sales)
  - **Backup 1:** Generate CSV report if PDF fails
  - **Expected output:** Daily report PDF saved to reports/YYYY-MM-DD.pdf
  - **Critical:** false
  - **Mode:** silent
  - **Verification:** Report includes all transactions, math is correct, till expected cash matches recorded cash sales + opening float
  - **Logging:** Log report_path, transactions_included, discrepancies_found

---

## Bridging: Markdown ↔ TOML Synchronisation

- Task IDs 1, 2, 3 must match `tasks[0], tasks[1], tasks[2]` in TOML
- Step IDs 1.1-1.4, 2.1-2.3, 3.1-3.2 must match TOML step arrays
- All backup methods described here must have corresponding TOML entries
- Critical flags must match: 5 critical / 9 total = 56% (within 40-60% moderate range)
- Expected outputs must be identical in both files

---

## Instructions for LLM

1. Read DNA profile TGCAATGC: MODERATE risk, dynamic mode, collaborative_review strategy
2. Verify 5 of 9 steps marked critical (56% - within 40-60% target)
3. Enable user stories: charity shop volunteer workflow informs all design decisions
4. Implement offline-first: cash transactions must work without network
5. Error propagation: read prior step outcomes, especially payment processing success before receipt printing
6. GDPR compliance: no personal data stored, receipts don't identify customers
7. Use collaborative_review: pause on financial calculation errors or data integrity issues
8. Log everything to progress_transaction_v2.json with detailed financial audit trail

