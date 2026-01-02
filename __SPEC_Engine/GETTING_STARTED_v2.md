# Getting Started with Constitutional Slow-Code Engine v2.0

**For:** Newcomers to SPEC Engine  
**Time:** 15-30 minutes  
**Updated:** 2 January 2026

---

## Welcome!

This guide introduces the Constitutional Slow-Code Engine v2.0 - a framework that combines structural rigour with educational philosophy for reliable, understandable AI-assisted development.

---

## Core Concepts (5 minutes)

### 1. One Goal, One SPEC
Every SPEC has exactly ONE goal. Multiple goals = separate SPECs.

**Good:** "Build a charity shop POS system"  
**Bad:** "Build POS system and inventory tracker and reporting dashboard"

### 2. Triple-File Architecture
Each SPEC consists of three synchronized files:
- **spec.md** - Human-readable (why & what)
- **parameters.toml** - Machine-readable (structure & config)
- **exe.md** - Execution controller (orchestration logic)
- **Plus:** `notepad.md` and `progress.json` generated during execution

### 3. Constitutional Governance
15 Articles (I-XV) ensure quality:
- Article I: One Goal Per SPEC
- Article II: Proper hierarchy (Goal → Task → Step → Backup)
- Article XV: Slow-Code Principle (understanding over speed when it matters)

### 4. Knowledge Capture (NEW v2.0)
Every execution generates:
- `progress.json` - Machine log (status, retries, errors)
- `notepad.md` - Human insights (discoveries, decisions, ideas)

### 5. Troubleshooting Ecosystem (NEW v2.0)
Three specialized TOOLSPECs for different problem types:
- **Troubleshoot:** Fix broken development code
- **WTF:** Understand mysterious/legacy code
- **Forensic:** Investigate critical production incidents

---

## Quick Start: Use a Pre-Built TOOLSPEC (10 minutes)

### Scenario: Your Code is Broken

1. **Navigate to Troubleshoot TOOLSPEC:**
```bash
cd __SPEC_Engine/_TOOLSPECs/Troubleshoot/
```

2. **Open Troubleshoot_SPEC.md in your AI assistant**

3. **Provide project path when prompted:**
```
Project Folder: C:\Users\Fab2\Desktop\MyProject
```

4. **Let the TOOLSPEC diagnose and fix systematically:**
- Gathers context from your project
- Categorizes issues by severity
- Implements fixes for critical issues
- Verifies fixes work
- Generates troubleshooting report

5. **Review outputs:**
- **progress_Troubleshoot.json** - What was fixed, how
- **notepad_Troubleshoot.md** - Insights captured during troubleshooting
- **Your fixed project** - Now working!

### Other Quick Start Scenarios

**Code is mysterious?** Use `_TOOLSPECs/WTF/`  
**Production incident?** Use `_TOOLSPECs/Forensic/`  
**Need code review?** Use `_TOOLSPECs/Better_SPEC/`

See `_TOOLSPECs/README_WORKFLOW_LIBRARY.md` for full selection guide.

---

## Create Your First Custom SPEC (15 minutes)

### Step 1: Define Your Goal

Think of ONE thing you want to achieve:
- "Build a markdown to PDF converter"
- "Analyze sentiment in customer reviews"
- "Create API documentation from code"

### Step 2: Optional - Create DNA Profile

If you'll create multiple SPECs for same project:

```bash
cd __SPEC_Engine/_DNA/
# Open DNA_SPEC.md
# Answer 5 questions (3 minutes)
# Get DNA code like ATGCTCGA
```

Skip this if it's a one-off goal.

### Step 3: Use Commander to Generate SPEC

```bash
cd __SPEC_Engine/_Commander_SPEC/
# Open Spec_Commander.md in your AI assistant
```

Provide your goal:
```
Goal: Build a markdown to PDF converter with table of contents
```

Commander will:
1. Analyze your goal
2. Propose task breakdown
3. **Wait for your approval** (MANDATORY - Article III)
4. Generate all 3 files in `SPECs/[DNA_CODE]/spec_[descriptor]/`

### Step 4: Review Generated Files

```
SPECs/[DNA_CODE]/spec_markdown_pdf/
├── spec_markdown_pdf.md
├── parameters_markdown_pdf.toml
├── exe_markdown_pdf.md
```

Check that:
- Goal is singular and clear
- Tasks make sense (2-5 tasks)
- Steps are concrete actions (1-5 per task)

### Step 5: Execute the SPEC

```bash
# Open exe_markdown_pdf.md in your AI assistant
```

You'll be prompted to select execution mode:
- **Dynamic (recommended):** Autonomous with intelligent escalation
- **Silent:** Fully autonomous, minimal pauses
- **Collaborative:** Pause at each critical decision
- **Education:** Learn as you go with explanations

### Step 6: Review Results

After execution:
- **progress_markdown_pdf.json** - What happened, step by step
- **notepad_markdown_pdf.md** - Insights, technical decisions, ideas
- **Your deliverable** - The markdown to PDF converter!

---

## Understanding Execution Modes

### Dynamic Mode (Default - Recommended)
- Runs autonomously most of the time
- Escalates intelligently when:
  - 3+ consecutive failures
  - Backup methods consistently needed
  - Output quality degrading
- Best for: Most workflows

### Education Mode (NEW v2.0)
- Runs autonomously but pauses at key decisions
- Shows alternatives with pros/cons
- Explains WHY approaches are chosen
- Logs learning to notepad
- Best for: Learning new patterns, onboarding

Enable in parameters.toml:
```toml
[execution]
default_mode = "education"

[education]
enabled = true
learning_pace = "moderate"
comparison_depth = "detailed"
```

### Silent Mode
- Fully autonomous, never pauses
- Only escalates when all methods exhausted
- Best for: Routine, well-understood workflows

### Collaborative Mode
- Pauses at every critical step
- Requests human approval frequently
- Best for: High-stakes, sensitive workflows

---

## Troubleshooting Decision Tree

```
Something is wrong?
│
├─ Is this a production incident?
│  ├─ Yes, critical (data loss/breach) → Use FORENSIC
│  └─ Yes, but less critical → Use TROUBLESHOOT
│
├─ Is code mysterious/undocumented?
│  └─ Yes → Use WTF (What's This Feature)
│
└─ Is development code broken?
   └─ Yes → Use TROUBLESHOOT
```

See `_TOOLSPECs/README_WORKFLOW_LIBRARY.md` for complete guide.

---

## Key Features of v2.0

### 1. Troubleshooting Ecosystem
**Problem:** AI tools excel at creation but fail at debugging (the "Troubleshooting Cliff")  
**Solution:** Three specialized TOOLSPECs with systematic approaches

### 2. Knowledge Capture
**Problem:** Insights get lost after execution  
**Solution:** Persistent notepad captures discoveries, decisions, ideas

### 3. Education Mode
**Problem:** Fast code generation without understanding creates debt  
**Solution:** Learning-focused mode with explanations and alternatives

### 4. TOOLSPEC Library
**Problem:** Starting from scratch for common workflows wastes time  
**Solution:** Pre-built, tested TOOLSPECs for common patterns

### 5. Constitutional Governance
**Problem:** Inconsistent quality across SPECs  
**Solution:** 15 Articles enforced at pre-flight, runtime, post-execution

---

## Common Workflows

### Workflow 1: Fix Broken Project
```
1. cd _TOOLSPECs/Troubleshoot/
2. Open Troubleshoot_SPEC.md
3. Provide project path
4. Review fixes in notepad.md
```

### Workflow 2: Understand Mystery Code
```
1. cd _TOOLSPECs/WTF/
2. Open WTF_SPEC.md
3. Specify mysterious file/module
4. Read generated documentation
```

### Workflow 3: Build New Feature
```
1. cd _Commander_SPEC/
2. Open Spec_Commander.md
3. Describe feature goal
4. Review & approve task breakdown
5. Execute generated SPEC
```

### Workflow 4: Investigate Production Incident
```
1. Preserve evidence FIRST (logs, config)
2. cd _TOOLSPECs/Forensic/
3. Open Forensic_SPEC.md
4. Provide incident context
5. Read postmortem report
```

---

## Best Practices

### DO:
✅ Define ONE clear goal per SPEC  
✅ Use pre-built TOOLSPECs when they match your need  
✅ Review Commander's task breakdown before approval  
✅ Read notepad.md after execution for insights  
✅ Use Education Mode when learning new patterns  
✅ Preserve evidence before forensic investigation  

### DON'T:
❌ Create multi-goal SPECs  
❌ Skip Commander's approval gate  
❌ Ignore constitutional validation errors  
❌ Modify templates directly (use Commander)  
❌ Start troubleshooting without context gathering  
❌ Use Silent Mode for unfamiliar workflows  

---

## Next Steps

### Immediate:
1. Try a TOOLSPEC (Troubleshoot, WTF, or Forensic)
2. Read `_Constitution/constitution.md` (15 Articles)
3. Create your first custom SPEC with Commander

### Short-Term:
4. Read `DESIGN_PHILOSOPHY.md` for rationale
5. Review `WORKFLOW_DIAGRAM.md` for complete lifecycle
6. Explore other available TOOLSPECs

### Long-Term:
7. Create DNA profile for your main project
8. Contribute TOOLSPECs for common patterns you discover
9. Use Education Mode to build team knowledge

---

## Getting Help

**Documentation:**
- `README.md` - System overview
- `_Constitution/constitution.md` - Governing rules
- `_TOOLSPECs/README_WORKFLOW_LIBRARY.md` - TOOLSPEC guide
- `WORKFLOW_DIAGRAM.md` - Complete lifecycle

**Common Issues:**
- **"Validation failed"** - Check constitutional violations in error message
- **"Bridging error"** - Task/step IDs don't match between .md and .toml
- **"Goal not singular"** - Break into multiple SPECs
- **"Software stack undefined"** - For build goals, fill out Software Stack section

**Learning Resources:**
- Use Education Mode for hands-on learning
- Read notepad.md files from past executions
- Review Better_SPEC TOOLSPEC for SPEC improvement patterns

---

## Summary

**Constitutional Slow-Code Engine v2.0** combines:
- **Structural rigour** (validated triple-file architecture)
- **Troubleshooting excellence** (systematic debugging ecosystem)
- **Educational philosophy** (understanding over speed)
- **Knowledge capture** (persistent learning)
- **Pre-built workflows** (TOOLSPEC library)

Start with a TOOLSPEC, progress to custom SPECs, use Education Mode for learning, and capture insights in notepad.md.

**Welcome to understanding-first AI development!**

---

*Last Updated: 2 January 2026*  
*Version: 2.0*  
*Framework: Constitutional Slow-Code Engine*
