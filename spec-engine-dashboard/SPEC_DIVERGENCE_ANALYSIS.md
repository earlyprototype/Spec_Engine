# SPEC Divergence Analysis
**Date:** 2 January 2026  
**Purpose:** Document where the implementation diverges from the original SPEC requirements

---

## Critical Finding: Wrong Interpretation of "DNA Profile Management"

### What the SPEC Actually Requested

**From SPEC lines 118-120:**
```
- DNA Profile Manager (create, edit, view profiles)
```

**From SPEC lines 208-216 (SPECLet 3):**
```
### SPECLet [3]: DNA Profile Management
Purpose: Enable creation and management of DNA profiles

Tasks:
- Task [3.1]: Build DNA profile list view
- Task [3.2]: Implement DNA creation form
- Task [3.3]: Add DNA editing and viewing capabilities
```

**From SPEC Constraints (lines 153-159):**
```
- Must integrate with existing SPEC Engine file structure (respect __SPEC_Engine/ and SPECs/ directories)
- Cannot modify core SPEC Engine framework files (read-only access to _Constitution, _templates, etc.)
- Parameter file editing must preserve TOML structure and validate against SPEC Engine schema
```

### What Was Actually Built

**WRONG:** A UI form to CREATE NEW DNA profiles from scratch

**What the image shows:**
- "Create DNA Profile" form
- Fields for: Project Name, Testing Approach, Risk Tolerance, Autonomy Level, Custom Tools, Constraints
- "Create DNA Profile" button

### What SHOULD Have Been Built

**DNA Profile Management = Managing EXISTING DNA profiles**

The SPEC Engine already has DNA profiles stored as **`project_constitution.toml`** files in **`SPECs/{DNA_CODE}/`** directories.

**Correct interpretation:**
1. **List View:** Browse EXISTING DNA profiles by reading `project_constitution.toml` files from `SPECs/*/`
2. **View Details:** Display the contents of an existing `project_constitution.toml`
3. **Edit:** Allow editing existing DNA profile settings (if needed)

**The dashboard was supposed to:**
- BROWSE the file system for existing `SPECs/GCATTAGC/`, `SPECs/ATGCATGC/`, etc.
- READ the `project_constitution.toml` files
- DISPLAY them in a nice UI
- Potentially allow EDITING (not creating from scratch)

---

## Fundamental Misunderstanding

### The Core Problem

**The SPEC Engine is a FILE-BASED FRAMEWORK.**

It manages:
- **`__SPEC_Engine/`** - Framework templates and constitution (READ-ONLY)
- **`SPECs/{DNA_CODE}/`** - User projects with their DNA profiles
- **`SPECs/{DNA_CODE}/project_constitution.toml`** - The DNA profile file
- **`SPECs/{DNA_CODE}/spec_{descriptor}/`** - Individual SPECs

**What the dashboard should do:**
1. **Read** the existing file structure
2. **Display** it in a nice web UI
3. **Manage** existing files (view, edit, create NEW SPECs within existing DNA codes)
4. **Monitor** executions

**What the dashboard is doing instead:**
- Trying to CREATE NEW DNA profiles through forms
- Storing metadata in SQLite instead of reading from the file system
- Building a CRUD application instead of a FILE SYSTEM VIEWER/MANAGER

---

## Why This Happened

### Root Cause: Misinterpreted "DNA Profile Management"

The phrase "DNA Profile Management" was interpreted as:
- "Build a CRUD interface to manage DNA profile records"

But it should have been interpreted as:
- "Build a UI to browse/view/manage EXISTING DNA profile files on disk"

### Contributing Factors

1. **No explicit file path examples in SPEC**
   - The SPEC mentioned "respect __SPEC_Engine/ and SPECs/ directories" but didn't show concrete examples
   - Should have explicitly stated: "Read from SPECs/{DNA_CODE}/project_constitution.toml"

2. **Database-first thinking**
   - The SPEC included Prisma/SQLite in the stack
   - This led to building a database-backed app instead of a file-system-backed viewer
   - The database should only store METADATA (execution history, logs), not the primary data

3. **Missing file structure diagram**
   - The SPEC should have included a visual of the file structure to make it crystal clear

---

## What Was Built vs What Should Exist

### Current (WRONG) Implementation

**DNA Profiles:**
```
Frontend: Form to create DNA profiles → 
Backend: POST /api/dna → 
Database: INSERT into dna_profiles → 
File System: Write to SPECs/{NEW_DNA_CODE}/project_constitution.toml
```

**Problems:**
- Creates NEW DNA codes from scratch
- User has to fill in all fields manually
- Doesn't show EXISTING DNA profiles from the file system

### Correct Implementation

**DNA Profiles:**
```
Frontend: Browse DNA profiles → 
Backend: GET /api/dna → 
File System: READ SPECs/*/project_constitution.toml → 
Display: Show existing DNA profiles in a list
```

**For viewing a specific DNA:**
```
Frontend: Click on GCATTAGC → 
Backend: GET /api/dna/GCATTAGC → 
File System: READ SPECs/GCATTAGC/project_constitution.toml → 
Display: Show DNA details + list of SPECs under this DNA
```

---

## Other Major Divergences

### 1. SPEC Listing

**What was requested:**
- Browse EXISTING SPECs from `SPECs/{DNA_CODE}/spec_{descriptor}/` directories
- Display spec_{descriptor}.md and parameters_{descriptor}.toml contents

**What was built:**
- Appears partially correct (lists SPECs from file system)
- But the `/edit` page should open the **parameters_{descriptor}.toml** file, not create a new SPEC

### 2. Execution Service

**What was requested (SPEC lines 131-132):**
```
- Execution service (spawn exe_[descriptor].md processes)
```

**What was built:**
- Unknown - execution service may not spawn exe_*.md files correctly
- Should invoke the existing `exe_*.md` files, not re-implement execution logic

### 3. Progress Monitoring

**What was requested:**
```
- Progress monitoring service (watch progress.json files)
- WebSocket service (real-time progress broadcasts)
```

**What was built:**
- Unknown - needs verification that it reads `progress_{descriptor}.json` from file system
- Should NOT create new progress tracking; should READ existing SPEC Engine progress files

---

## Summary: The Fatal Flaw

**The dashboard was built as a DATABASE APPLICATION when it should be a FILE SYSTEM VIEWER.**

### Analogy

Imagine building Windows Explorer:

**WRONG (what was built):**
- A form where users create "folder profiles" with a name, location, permissions
- Store folder metadata in a SQL database
- Generate folders on disk after form submission

**RIGHT (what should exist):**
- Browse the EXISTING file system
- Display folders and files that already exist on disk
- Allow viewing, editing, and managing existing items
- Create NEW files/folders WITHIN existing structures

---

## Recommended Fix Path

### Short-term (Get it Working)

1. **Change DNA Profile Page:**
   - Remove "Create DNA Profile" form
   - Replace with "DNA Profile List" showing EXISTING DNA codes from `SPECs/`
   - Read from file system, not database

2. **Fix SPEC Detail Page:**
   - Should display `spec_{descriptor}.md` content
   - "Edit Parameters" should open `parameters_{descriptor}.toml`

3. **Execution Service:**
   - Verify it spawns `exe_{descriptor}.md` correctly
   - Should read, not create, execution files

### Long-term (Proper Architecture)

1. **File System Service as Primary Source of Truth:**
   - All data comes from reading `__SPEC_Engine/` and `SPECs/` directories
   - Database is SECONDARY (only for caching and execution history)

2. **Sync Service:**
   - Periodically scan file system for changes
   - Update database cache as needed

3. **Clear Separation:**
   - File System Service: Read/write TOML/MD files
   - Database Service: Store execution history and UI state only
   - Never store SPEC content or DNA profiles in the database

---

## Lessons Learned

### For Future SPECs

1. **Include file structure diagrams**
   - Show the actual directory tree
   - Point to specific files: `SPECs/GCATTAGC/project_constitution.toml`

2. **Clarify "management" terminology**
   - "Manage existing X" vs "Create new X"
   - Be explicit about file-based vs database-based

3. **Provide example user stories with file paths**
   - "As a user, I want to view the DNA profile stored in `SPECs/GCATTAGC/project_constitution.toml`"
   - "As a user, I want to create a new SPEC under `SPECs/GCATTAGC/spec_my_new_feature/`"

4. **Architecture diagrams**
   - Show data flow: File System → Backend Service → API → Frontend
   - Make it clear that files are the source of truth

---

## Conclusion

The implementation fundamentally misunderstood the SPEC Engine as a file-based framework and instead built a traditional database-backed web application. The "DNA Profile Management" feature creates new profiles instead of managing existing ones, which defeats the purpose of integrating with the existing SPEC Engine file structure.

**The fix requires rethinking the entire data layer** to treat the file system as the primary source of truth, with the database only caching metadata and execution history.
