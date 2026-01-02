# WTF TOOLSPEC - Quick Reference Guide

**What's This Feature** - Code archaeology for mysterious/legacy code

---

## When to Use WTF

Use this TOOLSPEC when:
- You've inherited legacy code with no documentation
- Code behaviour is unexpected or confusing
- You need to modify code but don't understand its purpose
- Preparing to refactor or replace mysterious code
- Building knowledge base for team onboarding

**Don't use WTF when:**
- Something is broken and needs fixing → Use **Troubleshoot** instead
- Production incident needs forensics → Use **Forensic** instead
- Code is well-documented already → Just read the docs

---

## Quick Start

### 1. Identify Your Target

Before starting, know:
- Which file(s) or module(s) are mysterious?
- Specific function/class or entire module?
- Why is it confusing? (context helps focus analysis)

**Example:**
```
File: src/lib/auth/session_manager.py
Scope: SessionManager class, especially expiry logic
Context: Need to extend sessions but don't understand current timeout behaviour
```

### 2. Launch WTF Executor

```bash
# Navigate to SPEC Engine
cd __SPEC_Engine/_TOOLSPECs/WTF

# Launch executor
# AI will prompt for target code specification
```

### 3. Provide Target When Prompted

```
Target: src/lib/auth/session_manager.py
Scope: SessionManager class
Context: Session expiry logic is unclear, need to modify timeout behaviour
```

### 4. Review Outputs

WTF generates:
- **Feature Documentation** (comprehensive markdown)
- **Usage Examples** (3-5 runnable snippets)
- **Dependency Map** (upstream and downstream)
- **Integration Guide** (how to safely modify/extend)
- **notepad_WTF.md** (insights captured during analysis)

---

## What WTF Produces

### Primary Deliverable: Feature Documentation

Structured markdown including:

#### 1. Feature Purpose (Plain English)
```markdown
## What This Feature Does

SessionManager maintains user authentication state across HTTP requests by:
1. Generating unique session tokens on login
2. Storing session data in Redis with TTL
3. Validating tokens on each authenticated request
4. Cleaning up expired sessions via background worker
```

#### 2. Code Flow Diagrams
```
User Login
  ↓
SessionManager.create()
  ├─ Generate token (UUID4)
  ├─ Store in Redis (TTL: 3600s)
  └─ Return token to client
  
User Request
  ↓
SessionManager.validate(token)
  ├─ Check Redis for token
  ├─ If exists: refresh TTL, return True
  └─ If missing: return False
```

#### 3. Dependencies
- **Upstream:** redis-py, secrets module, datetime
- **Downstream:** auth.py (login/logout), middleware.py (request validation)
- **External:** Redis server (localhost:6379)

#### 4. Usage Examples
```python
# Create session on login
session_mgr = SessionManager(redis_client)
token = session_mgr.create(user_id=123, metadata={'ip': '192.168.1.1'})

# Validate session on request
is_valid = session_mgr.validate(token)
if is_valid:
    user_data = session_mgr.get_data(token)
```

#### 5. Known Issues & Workarounds
- Issue #42: Race condition if multiple requests validate same token simultaneously
  - Workaround: Use Redis WATCH for atomic checks
- TODO comment line 156: "Need to add session renewal endpoint"

#### 6. Integration Guide
- **Safe to modify:** Timeout duration (DEFAULT_TTL constant)
- **Risky to modify:** Token generation logic (security-sensitive)
- **Extension points:** Custom session metadata (metadata dict)

---

## The 4-Task Archaeology Process

### Task 1: Code Survey (30 min)
**Goal:** Map the structure

**Outputs:**
- List of entry points (public APIs)
- Data structures used
- Existing documentation fragments

### Task 2: Behaviour Analysis (45 min)
**Goal:** Understand what it does

**Outputs:**
- Execution flow for common scenarios
- Side effects identified (I/O, state changes)
- Error handling patterns

### Task 3: Dependency Mapping (30 min)
**Goal:** Understand relationships

**Outputs:**
- Upstream dependencies (what it needs)
- Downstream dependents (what needs it)
- External integrations (databases, APIs)

### Task 4: Documentation Generation (60 min)
**Goal:** Create maintainable docs

**Outputs:**
- Plain English summary
- Usage examples
- Known issues list
- Integration guide

**Total Time:** ~3 hours for medium-sized feature

---

## Tips for Successful Archaeology

### 1. Start Small
- Begin with a single function/class, not entire module
- Expand scope if needed after initial survey

### 2. Trust the Code, Not Comments
- Comments may be outdated
- Actual behaviour is source of truth

### 3. Look for Patterns
- Naming conventions reveal intent
- Similar patterns elsewhere in codebase provide context

### 4. Use Git History
- Original commit messages explain "why"
- Evolution shows design decisions

### 5. Run Examples
- Best way to verify understanding
- Catch your misunderstandings early

---

## Validation Checkpoints

After each task, ask:

**Task 1:** Can I explain the feature's structure to a colleague?  
**Task 2:** Can I predict behaviour for new inputs?  
**Task 3:** Do I know what would break if this changed?  
**Task 4:** Could someone maintain the code using my documentation?

If **NO** to any: return to that task with deeper analysis.

---

## Common Mistakes to Avoid

❌ **Making assumptions about behaviour**
✅ Verify all claims with code inspection

❌ **Documenting only obvious parts**
✅ Cover edge cases and error paths

❌ **Using technical jargon without definition**
✅ Write for humans, not compilers

❌ **Skipping examples**
✅ Examples are the most valuable documentation

❌ **Modifying code during analysis**
✅ Read-only archaeology (WTF never edits)

---

## FAQ

**Q: How long does WTF take?**
A: 1-4 hours depending on feature complexity:
- Small (<500 lines): 1-2 hours
- Medium (500-2000 lines): 2-3 hours
- Large (>2000 lines): 3-4 hours or modular approach

**Q: Can I use WTF on obfuscated code?**
A: Yes, but quality depends on how obfuscated. WTF will document behaviour but may struggle with intent if names are meaningless.

**Q: What if the code calls many external libraries?**
A: WTF documents the calls and their purposes. Deep library internals are out of scope (treat as black boxes).

**Q: Should I fix bugs I find during archaeology?**
A: NO. WTF is read-only analysis. Document bugs in "Known Issues" section. Fix them later with a separate Troubleshoot or Dev spec.

**Q: Can I use WTF for compiled code?**
A: WTF works on source code. For binaries/compiled code without source, you need reverse engineering tools (out of SPEC Engine scope).

---

## Related TOOLSPECs

- **Troubleshoot:** Something's broken, needs fixing
- **Forensic:** Critical failure needs root cause investigation
- **Dev_Analysis:** Planning modifications to existing code
- **Docs:** Creating comprehensive project documentation

---

## Support Files

- **Full Specification:** `WTF_SPEC.md`
- **Configuration:** `parameters_WTF.toml`
- **Execution Controller:** `exe_WTF.md`
- **Progress Log:** `progress_WTF.json` (generated during execution)
- **Knowledge Capture:** `notepad_WTF.md` (generated during execution)

---

**Last Updated:** 2 January 2026  
**TOOLSPEC Version:** 1.0  
**Part of:** Constitutional Slow-Code Engine v2.0
