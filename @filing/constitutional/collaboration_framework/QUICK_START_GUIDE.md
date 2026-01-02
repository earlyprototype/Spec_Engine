# Quick Start Guide - Constitutional Writing Sessions

**How to start a new writing session in a fresh LLM context**

---

## THE ONE-STEP PROCESS

### Starting Any Session (First or Continuing):

1. **Open new chat with your LLM**
2. **Share this file:** `@filing/constitutional/collaboration_framework/_SYSTEM_PROMPT_CONSTITUTIONAL_WRITER.md`
3. **Done.**

The LLM will automatically:
- Read the tracking documents
- Restore state (where you left off, learned patterns, story facts)
- Present today's goal
- Ask if you want to proceed

---

## WHAT HAPPENS AUTOMATICALLY

### The LLM reads these files:
- `MASTER_PROGRESS.md` → Knows where you left off
- `PATTERN_LEARNING_LOG.md` → Knows your style preferences
- `CONSISTENCY_TRACKER.md` → Knows story facts
- `constitutional_quick_reference.md` → Knows core story elements

### Then presents:
```
Last completed: Scene 3.1 (Maya decision log obsession)
Today's goal: Draft and revise Scene 3.2 (Jordan text exchange)
Estimated time: 30 minutes
Proceed?
```

### You say:
- "Yes" → Session begins
- "Actually, let's do Scene X instead" → Adjusts goal
- "Let me voice record some ideas first" → Voice brainstorm mode

---

## FIRST SESSION (Special Case)

If tracking files are empty (no previous progress):
- LLM recognizes this is Session 1
- Proceeds with baseline establishment
- You'll choose starting chapter
- Begin with scene framework creation

---

## DURING SESSION

**Modes automatically available:**
1. Voice brainstorm → You record ideas
2. Prose generation → LLM drafts scene
3. Edit & learn → You edit, LLM learns patterns
4. Real-time dialogue → Ask questions, request changes

**LLM does automatically:**
- Applies learned patterns during prose generation
- Flags consistency issues
- Tracks your edits for pattern learning
- Maintains professional tone (no excessive praise)

---

## END OF SESSION

**LLM automatically updates:**
- `MASTER_PROGRESS.md` → Marks scene complete, word count
- `PATTERN_LEARNING_LOG.md` → Documents observed patterns
- `CONSISTENCY_TRACKER.md` → Adds new story details

**Then presents:**
```
✅ Scene 3.2 complete (978 words)
📝 Next: Scene 3.3 (Lily's call)
🎯 Progress: Chapter 3 - 2 of 5 scenes complete
🔍 Pattern observed: You're shortening Maya's sentences. Applying to future scenes.
```

**No action needed from you** - everything is saved in tracking docs for next session.

---

## THAT'S IT

**Next session:** Just share `_SYSTEM_PROMPT_CONSTITUTIONAL_WRITER.md` again. Everything continues from where you left off.

**No setup. No configuration. No explaining context. Just one file.**

---

## OPTIONAL: TOOLS

**Obsidian Vault (if you want):**
- See `OBSIDIAN_VAULT_SETUP.md` for setup
- Visual organization, linking, graph view
- Not required - plain files work fine

**Voice Recording:**
- Cursor has native audio recording
- Or use phone voice memo
- Save to `03_audio/` folder in vault

**Read-Aloud (zero cost):**
- Edge browser: Select text → Right-click → "Read aloud"
- Windows Narrator: Win + Ctrl + N
- Helps catch rhythm issues

---

## IF SOMETHING GOES WRONG

**LLM seems confused about context:**
- Check that tracking files exist and are updated
- Manually point LLM to specific file: "Read MASTER_PROGRESS.md"

**Can't find files:**
- Provide full path: `C:\Users\Fab2\Desktop\AI\Specs\@filing\constitutional\progress_tracking\MASTER_PROGRESS.md`
- Or navigate to folder first

**Pattern learning not working:**
- Check PATTERN_LEARNING_LOG.md has entries
- Takes 3+ sessions to establish patterns
- LLM needs edited scenes to learn from

---

## REFERENCE DOCUMENTS (Don't need to share, but available)

**For you to consult:**
- `SPEC_CONSTITUTIONAL_WRITER.md` - Detailed system design
- `WRITING_COLLABORATION_FRAMEWORK.md` - Full workflow explanation
- `PROFESSIONAL_WRITING_PROCESS.md` - Industry standards
- `PROSE_CRAFT_GUIDE.md` - Writing techniques
- `NEXT_STEPS_ACTION_PLAN.md` - Roadmap

**Story architecture:**
- `constitutional_complete_structure.md` - Full outline
- `constitutional_character_profiles.md` - All characters
- `constitutional_sics_worldbuilding.md` - World mechanics
- All other docs in `@filing/constitutional/`

**LLM has access to all these via references in system prompt.**

---

## EXAMPLE COMPLETE WORKFLOW

**Day 1 - Session 1:**
1. Share `_SYSTEM_PROMPT_CONSTITUTIONAL_WRITER.md`
2. LLM: "Tracking files empty - this is Session 1. Which chapter to start?"
3. You: "Prologue"
4. Voice record: "Mother arrives, sets up apartment..."
5. LLM structures framework, you approve
6. LLM drafts scene
7. You edit
8. LLM updates tracking docs
9. Session ends

**Day 2 - Session 2:**
1. Share `_SYSTEM_PROMPT_CONSTITUTIONAL_WRITER.md`
2. LLM: "Last completed: Prologue Scene 1. Today: Prologue Scene 2?"
3. You: "Yes"
4. LLM drafts (applying patterns from Session 1)
5. You edit
6. LLM updates tracking docs
7. Session ends

**Day 10 - Session 10:**
1. Share `_SYSTEM_PROMPT_CONSTITUTIONAL_WRITER.md`
2. LLM: "Last completed: Chapter 2, Scene 3. Pattern confidence high. Today: Chapter 2, Scene 4?"
3. You: "Yes"
4. LLM drafts (prose much closer to your style now)
5. Minimal edits needed
6. Session ends

**First draft complete - Day 180:**
1. Share `_SYSTEM_PROMPT_CONSTITUTIONAL_WRITER.md`
2. LLM: "Progress: 80,000 words complete. Ready for revision?"
3. Continue with revision phase...

---

**The beauty:** Every session is identical. Share one file. LLM knows everything. Continue writing.

**That's the whole system.**



