# Better SPEC - Quick Start Guide

**Get started in 30 seconds**

---

## Three Ways to Use Better_SPEC

### 1. Process an Analysis Report (Mode A)

**You have:** A completed improvement report  
**You want:** To implement its recommendations

**What to say:**
```
Process the improvement recommendations from 
C:\Users\Fab2\Desktop\AI\Specs\@dev\_ANALYSIS\TGACGTCA_SPEC_Engine_Improvements.md
```

**What happens:**
- Reads report
- Extracts all recommendations
- Shows you prioritised list
- You approve/reject each one
- Implements approved changes

---

### 2. Work Through Proposals (Mode B)

**You have:** Proposals folder with pending ideas  
**You want:** To process them systematically, one at a time

**What to say:**
```
Let's work through proposals in @dev\_SPEC_dev_proposals/ one at a time
```

**What happens:**
- Scans all proposals
- Shows you inventory with impact/effort ratings
- Recommends next one (or you choose)
- Processes ONE proposal with you
- Asks if you want another
- Implements when you're done

---

### 3. Make Specific Improvement (Mode C)

**You have:** A specific idea  
**You want:** To implement just this one thing

**What to say:**
```
Add a requirement to Article IX that agents must verify fixes 
before claiming completion
```

**What happens:**
- Understands your request
- Designs implementation
- Shows you the plan
- Gets approval
- Makes the change

---

## What You'll Be Asked

Regardless of mode, expect these interactions:

1. **Confirmation before changes** - "Should I proceed with this implementation?"
2. **Before/after previews** - Always see what's changing
3. **Approval checkpoints** - At key decision points
4. **Continue/stop questions** - (Mode B only) "Process another proposal?"

---

## What Gets Changed

Better_SPEC can modify any SPEC_Engine file:

- Constitution (`__SPEC_Engine/_Constitution/constitution.md`)
- Templates (`__SPEC_Engine/_templates/*.md`)
- Commander (`__SPEC_Engine/_Commander_SPEC/Spec_Commander.md`)
- Workflow docs (`__SPEC_Engine/WORKFLOW_DIAGRAM.md`)
- DNA SPEC (`__SPEC_Engine/_DNA/DNA_SPEC.md`)
- Other framework files

**Safety:** Originals always backed up to `@filing/Better_SPEC_changes/[timestamp]/`

---

## What Gets Created

After execution, you'll have:

1. **Modified framework files** (with backups)
2. **Session summary** in `@filing/Better_SPEC_sessions/`
3. **Change log** documenting what was done
4. **Progress log** in `progress_Better_SPEC.json`

---

## Tips

### For Mode B (Proposals)
- Process proposals when you have focused time
- One proposal = one execution (ADHD-friendly)
- Can resume later - tracks what's been processed

### For Mode A (Reports)
- Best for batch processing multiple recommendations
- Review the prioritisation - you can change order
- Quick wins get highlighted

### For Mode C (Single Request)
- Great for "quick fix" ideas
- Be specific about what you want
- Better_SPEC will assess impact and show you plan

---

## Example Session (Mode B)

```
User: Let's work through proposals in @dev/_SPEC_dev_proposals/

Better_SPEC: 
I've found 5 proposals:

1. PROPOSED_COMMANDER_UPDATES.md
   Category: Commander Enhancement
   Impact: High | Effort: Low | Status: New
   
2. breakout_subSpecs_per_task.md
   Category: New Feature
   Impact: Medium | Effort: High | Status: New

3. invoke_context7.md
   Category: Integration
   Impact: Medium | Effort: Medium | Status: New

4. post_document_prep_handoff.md
   Category: Workflow Enhancement
   Impact: Low | Effort: Low | Status: New

5. error_logs (file)
   Category: Unknown
   Impact: Unknown | Status: New

Recommendation: Start with #1 (PROPOSED_COMMANDER_UPDATES.md) 
- High impact, low effort

Which proposal would you like to process?

User: Let's do #1

Better_SPEC: [Shows full proposal details, discusses with you, 
             gets approval, queues for implementation]

Better_SPEC: Would you like to process another proposal now?

User: No, let's implement this one first

Better_SPEC: [Implements approved changes, shows completion report]
```

---

## Common Questions

**Q: Can I stop mid-session and resume later?**  
A: Yes! Mode B tracks progress. Processed proposals won't be shown again.

**Q: What if I disagree with a recommendation?**  
A: Reject it, modify it, or defer it. You control everything.

**Q: Can I undo changes?**  
A: Originals are backed up. You can restore from `@filing/Better_SPEC_changes/`.

**Q: How do I know what mode I'm in?**  
A: You don't need to - Better_SPEC detects automatically based on what you ask for.

---

**Ready?** Just provide input matching one of the three modes above, and Better_SPEC will handle the rest.

