# Spec: Charity Shop POS - Complete System (v3)

## Goal
Build a complete point-of-sale transaction system for charity shop volunteers that handles cash and card payments, prints itemised receipts, tracks daily totals, and integrates with Square payment processor.

---

## Software Stack & Architecture

**MANDATORY: Build/create/system goal requires software stack definition**

### Deployment Type
- [x] Desktop Application (installable Windows executable)

### Technology Stack
- **Language:** Python 3.10+
- **Framework:** PyQt5 (desktop GUI)
- **Database:** SQLite (local, embedded)
- **UI Library:** PyQt5 (cross-platform desktop UI)
- **Packaging:** PyInstaller (creates `volunteers_pos.exe`)

### User Interface Requirements
- **Primary users:** Charity shop volunteers (non-technical, varying ages and tech literacy)
- **Interaction method:** GUI with large, clearly labelled buttons and touch-screen friendly design
- **Technical skill level:** None (must be usable by someone with no computer experience beyond basic use)
- **Accessibility requirements:** 
  - Large buttons (minimum 80px height)
  - Simple, jargon-free language
  - High contrast text
  - Clear status messages
  - Minimal required actions per workflow

### Deployment Requirements
- **Target environment:** Windows 10+ (charity shop computers)
- **Installation method:** Portable `.exe` file (no installation needed, can run from USB) OR simple installer
- **Configuration needed:** 
  - Square API credentials (via first-run setup wizard)
  - Thermal printer configuration (COM port detection)
  - Shop name and charity registration number
- **Startup process:** Double-click desktop icon "Volunteers POS" or `volunteers_pos.exe`

---

## Definition of Complete

**This goal is ACHIEVED when ALL criteria below are met:**

### Functional Completeness
- [ ] Volunteer processes £5.99 cash sale, system calculates £4.01 change correctly
- [ ] Volunteer processes £25.00 card payment via **actual** Square API (not test mode)
- [ ] Receipt prints to physical thermal printer with itemisation, charity info, date/time
- [ ] End-of-day report generates showing:  
  - Total cash sales  
  - Total card sales  
  - Expected till balance  
  - Discrepancy flagging
- [ ] System handles network failures gracefully (cash transactions work offline)
- [ ] System handles printer failures gracefully (saves receipt to file, prompts retry)

### Deployment Completeness
- [ ] `volunteers_pos.exe` exists in `dist/` folder (15-20 MB single file)
- [ ] Executable runs on clean Windows 10 machine without Python installed
- [ ] Configuration wizard launches on first run, guides volunteer through Square API setup
- [ ] Volunteer can start system by double-clicking desktop shortcut
- [ ] System tested on at least 2 different Windows machines (simulating different charity shops)

### User Acceptance
- [ ] Non-technical volunteer (test user) completes 5 sales (3 cash, 2 card) without assistance
- [ ] Volunteer can print receipt after transaction
- [ ] Volunteer can generate end-of-day report
- [ ] Volunteer can recover from these scenarios without help:
  - Printer out of paper → system displays clear message
  - Card declined → system shows user-friendly error
  - Network down → system continues with cash sales
- [ ] Receipt format approved by charity shop manager

### Production Readiness
- [ ] Square API connected to **production** endpoint (not sandbox/test)
- [ ] Square API credentials loaded from config file or wizard (not hardcoded)
- [ ] Printer COM port configurable via settings
- [ ] Error logging to `logs/volunteer_pos.log` for troubleshooting
- [ ] Security: No sensitive data (card numbers) stored locally

---

## Definitions
- goal: Build a complete, runnable POS system usable by non-technical volunteers
- task[n]: Discrete objectives (GUI, backend, packaging, docs)
- step[m]: Concrete actions within each task
- backup[p]: Alternative methods if primary fails
- critical_flag: true = failure blocks goal achievement
- mode: "dynamic" (default), escalates intelligently
- progress.json: Structured log tracking execution

---

## User Stories

- **As a charity shop volunteer**, I want to quickly process cash sales so customers don't wait in queue
- **As a charity shop volunteer**, I want clear error messages if card payment fails so I can guide the customer
- **As a shop manager**, I want accurate end-of-day reports so I can reconcile the till and bank deposits
- **As a customer**, I want an itemised receipt showing my donation for tax relief purposes
- **As a shop manager**, I want the system to work offline for cash sales so we don't lose business during internet outages
- **As a volunteer coordinator**, I want the system to be simple enough that new volunteers can use it after 5 minutes of training

---

## Components
- **GUI:** PyQt5 main window, buttons, forms
- **Backend:** Payment processor (cash + Square card), database, receipt generator
- **Database:** SQLite local file (`transactions.db`)
- **Printer:** Thermal receipt printer via serial/USB
- **Configuration:** JSON settings file + first-run wizard

**Machine-Readable Components:**
Per `parameters_transaction_v3.toml`:
- `main_window = "PyQt5 main application window at src/gui/main_window.py"`
- `payment_backend = "Payment processing module at src/payment_processor.py"`
- `database = "SQLite database at data/transactions.db"`
- `printer_interface = "Thermal printer wrapper at src/printer.py"`

---

## Constraints
- **Offline-first:** Cash transactions must work without network
- **GDPR compliant:** No personal customer data stored
- **Accuracy:** All monetary calculations use Decimal type (no float errors)
- **Speed:** Transaction processing < 2 seconds
- **Security:** Card data never touches local system (handled by Square SDK)
- **Usability:** Non-technical volunteers can use without training
- **Reliability:** System must handle printer/network failures gracefully

**Machine-Readable Constraints:**
Per `parameters_transaction_v3.toml`:
- `max_transaction_time_seconds = 2`
- `offline_capable = true`
- `gdpr_compliant = true`
- `precision_decimal = true`

---

## Tasks

### Task 1: Build PyQt5 Desktop Application GUI
**TOML Reference:** `[[tasks]] id = 1`

#### Step 1.1: Create main window with volunteer interface
- **Description:** Design and implement the main POS window with large, touch-friendly buttons
- **Primary method:** Use Qt Designer to create `.ui` file, then convert to Python. Main window has:
  - "New Cash Sale" button (green, 100px height)
  - "New Card Sale" button (blue, 100px height)
  - "End of Day Report" button (orange, 80px height)
  - Transaction display area (shows last 5 transactions)
  - Status bar (connection status, printer status, date/time)
- **Backup [1]:** If Qt Designer unavailable, code PyQt5 layout manually using QVBoxLayout
- **Expected output:** `src/gui/main_window.py` with functional window, buttons clickable
- **Critical:** true
- **Mode:** dynamic
- **Verification:** 
  - Run `python src/gui/main_window.py` → window appears
  - Click buttons → console log confirms events captured
  - Window resizes correctly, buttons remain readable
- **Logging:** Append to `progress_transaction_v3.json`

#### Step 1.2: Create cash sale dialog
- **Description:** Modal dialog for cash transactions with amount entry, tendered amount, change calculation
- **Primary method:** Create `CashSaleDialog` class extending QDialog:
  - Amount input field (numeric, £ symbol)
  - Tendered amount input field
  - Live change calculation display
  - "Complete Sale" button (large, green)
  - "Cancel" button
- **Backup [1]:** If validation complex, use QDoubleValidator for input fields
- **Expected output:** `src/gui/cash_dialog.py` with working dialog
- **Critical:** true
- **Mode:** dynamic
- **Verification:**
  - Dialog displays when "New Cash Sale" clicked
  - Enter £5.99 sale, £10 tendered → shows £4.01 change
  - Change updates live as volunteer types
  - "Complete" calls backend payment processor
- **Logging:** Append to `progress_transaction_v3.json`

#### Step 1.3: Create card sale dialog
- **Description:** Modal dialog for card transactions with Square API integration
- **Primary method:** Create `CardSaleDialog` class:
  - Amount input field
  - "Process Card Payment" button
  - Progress spinner during API call
  - Success/failure message display
  - Auto-close on success, retry option on failure
- **Backup [1]:** If Square SDK integration complex, show clear error messages for common failures
- **Expected output:** `src/gui/card_dialog.py` with Square integration
- **Critical:** true
- **Mode:** dynamic
- **Verification:**
  - Dialog displays when "New Card Sale" clicked
  - Enter £25.00 → "Process Card Payment" calls Square API
  - Success message displayed with transaction ID
  - Failure shows user-friendly message ("Card declined" not "API error 402")
- **Logging:** Append to `progress_transaction_v3.json`

#### Step 1.4: Integrate backend with GUI
- **Description:** Connect GUI button clicks to payment processing backend modules
- **Primary method:** Wire Qt signals to backend slots:
  - Cash sale completion → `process_cash_payment()`
  - Card sale completion → `process_card_payment()`
  - Transaction success → update database, print receipt, refresh display
  - Transaction failure → display error, offer retry
- **Backup [1]:** If signal/slot complex, use direct function calls with try/except
- **Expected output:** Fully functional GUI→backend data flow
- **Critical:** true
- **Mode:** dynamic
- **Verification:**
  - Complete cash sale in GUI → transaction appears in database
  - Complete card sale in GUI → Square API called, transaction logged
  - Receipt generation triggered automatically
  - Error in backend → user sees friendly message in GUI
- **Logging:** Append to `progress_transaction_v3.json`

---

### Task 2: Implement Production-Ready Backend
**TOML Reference:** `[[tasks]] id = 2`

#### Step 2.1: Configure Square API for production use
- **Description:** Implement Square API client with production endpoint and configurable credentials
- **Primary method:** 
  - Use Square Python SDK with production endpoint
  - Load API credentials from `config/settings.json`
  - Implement error handling for API failures (network, declined, etc.)
  - Add retry logic with exponential backoff
- **Backup [1]:** If production API fails, fall back to cash-only mode with clear warning to volunteer
- **Expected output:** `src/payment_processor.py` with production Square API integration
- **Critical:** true
- **Mode:** dynamic
- **Verification:**
  - Test mode flag = false or configurable
  - API credentials loaded from config file (not hardcoded)
  - Process actual £1.00 card payment via Square production API
  - Declined card shows user-friendly error
  - Network failure handled gracefully
- **Logging:** Append to `progress_transaction_v3.json`

#### Step 2.2: Implement offline-capable cash transactions
- **Description:** Ensure cash transactions work without network, queue for sync when online
- **Primary method:**
  - Cash transactions write to local SQLite immediately
  - Add `sync_status` field ('synced' | 'pending')
  - Background thread checks connectivity, syncs pending transactions
- **Backup [1]:** If background sync fails, manual sync button in GUI
- **Expected output:** Cash transactions work offline, sync automatically
- **Critical:** true
- **Mode:** dynamic
- **Verification:**
  - Disable network → complete cash sale → transaction recorded locally
  - Re-enable network → pending transactions sync automatically
  - `sync_status` updated to 'synced'
- **Logging:** Append to `progress_transaction_v3.json`

#### Step 2.3: Implement robust printer interface
- **Description:** Thermal printer wrapper with error handling and fallback
- **Primary method:**
  - Detect printer COM port automatically (or load from config)
  - Send receipt data in thermal printer format (32-char width)
  - Handle printer errors (out of paper, disconnected)
  - Save receipt to `receipts/backup_[id].txt` if print fails
- **Backup [1]:** If auto-detect fails, prompt volunteer to select COM port from dropdown
- **Backup [2]:** If printer unavailable, save all receipts to file, offer batch print later
- **Expected output:** `src/printer.py` with robust error handling
- **Critical:** false (system must work without printer)
- **Mode:** dynamic
- **Verification:**
  - Receipt prints successfully to thermal printer
  - Printer disconnected → receipt saved to file, volunteer notified
  - Printer reconnected → volunteer can reprint from transaction history
- **Logging:** Append to `progress_transaction_v3.json`

---

### Task 3: Package as Deployable Executable
**TOML Reference:** `[[tasks]] id = 3`

#### Step 3.1: Configure PyInstaller for single-file executable
- **Description:** Create PyInstaller spec file to bundle application as `volunteers_pos.exe`
- **Primary method:**
  - Generate `volunteers_pos.spec` with PyInstaller
  - Include all dependencies (PyQt5, Square SDK, SQLite)
  - Bundle icon file (`assets/icon.ico`)
  - Set executable name, version info
  - Configure hidden imports for dynamic modules
- **Backup [1]:** If single-file fails (too slow), use one-folder mode
- **Expected output:** `volunteers_pos.spec` configured and tested
- **Critical:** true
- **Mode:** dynamic
- **Verification:**
  - Run `pyinstaller volunteers_pos.spec`
  - `dist/volunteers_pos.exe` created (15-20 MB)
  - No console window appears when exe launched
- **Logging:** Append to `progress_transaction_v3.json`

#### Step 3.2: Build and test executable on clean system
- **Description:** Package application and test on Windows machine without Python
- **Primary method:**
  - Run PyInstaller build
  - Copy `dist/volunteers_pos.exe` to clean Windows 10 VM
  - Launch exe, verify all functionality works
  - Test cash sale, card sale, printer, end-of-day report
- **Backup [1]:** If dependencies missing, use `pyinstaller --onefile --hidden-import=square` to bundle
- **Expected output:** Fully functional `volunteers_pos.exe` tested on clean system
- **Critical:** true
- **Mode:** dynamic
- **Verification:**
  - Clean Windows 10 VM (no Python, no dependencies)
  - Double-click `volunteers_pos.exe` → application launches
  - Complete cash sale → works
  - Complete card sale → works (with internet)
  - Generate end-of-day report → works
  - No Python errors or missing module errors
- **Logging:** Append to `progress_transaction_v3.json`

#### Step 3.3: Create first-run configuration wizard
- **Description:** Wizard dialog that launches on first run to configure Square API and printer
- **Primary method:**
  - Check if `config/settings.json` exists
  - If not, show `SetupWizardDialog`:
    - Welcome screen (explain setup)
    - Square API credentials entry (Application ID, Access Token)
    - "Test Connection" button (verify API works)
    - Printer configuration (auto-detect or manual COM port)
    - Shop info (name, charity number)
    - Save to `config/settings.json`
- **Backup [1]:** If auto-detect fails, provide manual configuration option
- **Expected output:** `src/gui/setup_wizard.py` with complete configuration flow
- **Critical:** true
- **Mode:** dynamic
- **Verification:**
  - Delete `config/settings.json`
  - Launch exe → wizard appears
  - Enter Square credentials → "Test Connection" succeeds
  - Complete wizard → `config/settings.json` created
  - Restart exe → wizard does not appear, main window loads
- **Logging:** Append to `progress_transaction_v3.json`

---

### Task 4: Create User Documentation
**TOML Reference:** `[[tasks]] id = 4`

#### Step 4.1: Write volunteer user guide
- **Description:** Create simple, illustrated guide for volunteers
- **Primary method:**
  - Write `docs/VOLUNTEER_GUIDE.md` with:
    - How to start the system
    - How to process cash sales (with screenshots)
    - How to process card sales
    - How to handle errors
    - How to generate end-of-day report
    - Troubleshooting common issues
  - Use simple language, step-by-step instructions
  - Include screenshots of each screen
- **Backup [1]:** If markdown too technical, create PDF with large text and images
- **Expected output:** `docs/VOLUNTEER_GUIDE.md` or `.pdf`
- **Critical:** false
- **Mode:** dynamic
- **Verification:**
  - Guide covers all primary workflows
  - Language is jargon-free
  - Screenshots match actual application
- **Logging:** Append to `progress_transaction_v3.json`

#### Step 4.2: Create installation and configuration guide
- **Description:** Guide for shop managers to install and configure system
- **Primary method:**
  - Write `docs/INSTALLATION.md` with:
    - System requirements
    - How to download/copy `volunteers_pos.exe`
    - First-run setup (Square API, printer)
    - Where to get Square API credentials
    - How to configure printer
    - Backup and data management
- **Expected output:** `docs/INSTALLATION.md`
- **Critical:** true
- **Mode:** dynamic
- **Verification:**
  - Shop manager can follow guide to set up system
  - Square API credential instructions clear
  - Printer setup explained with common COM port examples
- **Logging:** Append to `progress_transaction_v3.json`

---

## Bridging: Markdown ↔ TOML Synchronisation

This spec file must align perfectly with `parameters_transaction_v3.toml`:
- Task IDs: 1, 2, 3, 4 match in both files
- Step IDs: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 4.1, 4.2 match
- Expected outputs match between files
- Critical flags match
- Backups referenced in TOML structure

---

## Instructions for LLM

1. This is a **complete system build** (Article XIV applies)
2. Software stack is MANDATORY and fully defined above
3. Definition of Complete criteria are **non-negotiable** for ACHIEVED status
4. GUI development is REQUIRED (not optional)
5. Packaging to executable is REQUIRED (not optional)
6. Production Square API is REQUIRED (test mode = PARTIAL status)
7. User documentation is REQUIRED
8. Read `progress_transaction_v3.json` before each step
9. Log all actions, retries, backups to progress file
10. Verify deployment completeness before marking goal ACHIEVED



