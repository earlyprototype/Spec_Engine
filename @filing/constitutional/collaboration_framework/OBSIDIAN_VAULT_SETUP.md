# Obsidian Vault Setup for Constitutional
## Repository-Based Writing Environment

**Version:** 1.0  
**Date:** 2 November 2025  
**Purpose:** Configure Obsidian vault for novel writing workflow

---

## WHY OBSIDIAN?

**Advantages for this project:**
- ✅ Markdown native (plain text, no lock-in)
- ✅ Links between files (connect scenes, characters, notes)
- ✅ Tags for organization
- ✅ Graph view (visualize story structure)
- ✅ Templates (consistent scene formatting)
- ✅ Quick switcher (jump between files fast - ADHD friendly)
- ✅ Local files (works in your repo)
- ✅ No distraction (minimal interface)
- ✅ Free for personal use

---

## VAULT CREATION

### Step 1: Create Vault Folder

**In your repo root:**
```
C:\Users\Fab2\Desktop\AI\Specs\constitutional_vault\
```

**Or create it here:**
```powershell
cd "C:\Users\Fab2\Desktop\AI\Specs"
mkdir constitutional_vault
```

### Step 2: Open in Obsidian

1. Launch Obsidian
2. "Open folder as vault"
3. Navigate to `constitutional_vault`
4. Open

**Vault is now active.**

---

## FOLDER STRUCTURE

```
constitutional_vault/
│
├── 00_architecture/
│   ├── story_structure.md (link to filing docs)
│   ├── characters.md
│   ├── world_building.md
│   ├── themes.md
│   └── quick_reference.md
│
├── 01_frameworks/
│   ├── chapter_01/
│   │   ├── scene_1.1_framework.md
│   │   ├── scene_1.2_framework.md
│   │   └── ...
│   └── chapter_02/
│       └── ...
│
├── 02_drafts/
│   ├── prologue/
│   │   ├── scene_01_draft.md
│   │   ├── scene_02_draft.md
│   │   └── scene_03_draft.md
│   ├── chapter_01/
│   │   ├── scene_1.1_draft.md
│   │   └── ...
│   └── compiled/
│       ├── prologue_complete.md
│       ├── chapter_01_complete.md
│       └── MANUSCRIPT_FULL.md
│
├── 03_audio/
│   ├── voice_notes/
│   │   ├── 2025-11-03_chapter01_brainstorm.m4a
│   │   └── ...
│   └── transcripts/
│       ├── 2025-11-03_chapter01_transcript.md
│       └── ...
│
├── 04_patterns/
│   ├── style_learning_log.md
│   ├── user_preferences.md
│   └── pattern_analysis/
│       ├── week_1_patterns.md
│       └── ...
│
├── 05_consistency/
│   ├── character_tracker.md
│   ├── timeline.md
│   ├── sics_scores.md
│   └── world_facts.md
│
├── 06_sessions/
│   ├── 2025-11-03_session_01.md
│   ├── 2025-11-04_session_02.md
│   └── ...
│
├── 07_revision/
│   ├── revision_notes.md
│   ├── cut_scenes/
│   └── alternatives/
│
└── templates/
    ├── scene_framework_template.md
    ├── scene_draft_template.md
    └── session_log_template.md
```

---

## INITIAL SETUP

### Link Architecture Documents

**In `00_architecture/`, create files that link to your main docs:**

**File: `00_architecture/story_structure.md`**
```markdown
# Story Structure

Main documentation: [[../../@filing/constitutional/constitutional_complete_structure.md]]

## Quick Overview
- Prologue: Mother sets up apartment
- Part 1 (Ch 1-5): Recognition
- Part 2 (Ch 6-10): Doubt
- Part 3 (Ch 11-15): Confusion
- Part 4 (Ch 16-20): Loss
- Part 5 (Ch 21-24): Dissolution
- Epilogue: Six months later

[Copy key details here for quick reference]
```

**Benefit:** Main docs stay in `@filing/`, vault has working copies and links

---

## TEMPLATES

### Template 1: Scene Framework

**File: `templates/scene_framework_template.md`**
```markdown
# Scene {{chapter}}.{{scene}}: {{Title}}

**Chapter:** {{chapter}}  
**Scene:** {{scene}}  
**Status:** 🟡 Framework | ⚪ Drafted | ✅ Revised  
**Word Count Target:** {{word_count}}

---

## Scene Details

**Location:** {{location}}  
**Time:** {{time_of_day}} / {{relative_timing}}  
**Present:** {{characters}}  
**POV:** Maya (close third-person)

---

## What Happens (Beats)

1. {{beat_1}}
2. {{beat_2}}
3. {{beat_3}}
4. {{beat_4}}

---

## Emotional Tone

{{tone_description}}

---

## Purpose

{{why_this_scene_exists}}

---

## Key Moments

- {{key_moment_1}}
- {{key_moment_2}}
- {{key_moment_3}}

---

## Dialogue Notes

{{any_specific_dialogue_to_hit}}

---

## Ends With

{{final_beat_or_image}}

---

## Links

**Previous:** [[scene_{{prev}}_framework]]  
**Next:** [[scene_{{next}}_framework]]  
**Draft:** [[../../02_drafts/{{chapter}}/scene_{{scene}}_draft]]

---

## Voice Brainstorm Transcript

[[../../03_audio/transcripts/{{date}}_{{chapter}}_{{scene}}_transcript]]

---

**Status:** Framework approved: {{date}}
```

---

### Template 2: Scene Draft

**File: `templates/scene_draft_template.md`**
```markdown
# Scene {{chapter}}.{{scene}}: {{Title}} [DRAFT]

**Chapter:** {{chapter}}  
**Scene:** {{scene}}  
**Status:** ⚪ First Draft | 🟡 Edited | ✅ Final  
**Word Count:** {{current_word_count}} / {{target}}

---

## Framework Reference

[[../../01_frameworks/{{chapter}}/scene_{{scene}}_framework]]

---

## Draft

{{prose_goes_here}}

---

## Revision Notes

**First Draft:** {{date}}  
**User Edits:** {{date}}  
**Changes:**
- {{change_1}}
- {{change_2}}

**Pattern Learning:**
- {{pattern_observed}}

---

## Links

**Previous Scene:** [[scene_{{prev}}_draft]]  
**Next Scene:** [[scene_{{next}}_draft]]

---

Tags: #draft #{{chapter}} #{{character_tags}}
```

---

### Template 3: Session Log

**File: `templates/session_log_template.md`**
```markdown
# Session {{number}} - {{date}}

**Date:** {{date}}  
**Duration:** {{minutes}} minutes  
**Goal:** {{session_goal}}

---

## Completed

- [x] {{task_1}}
- [x] {{task_2}}
- [ ] {{incomplete_task}}

---

## Progress

**Scenes:**
- Frameworks approved: {{count}}
- Drafts written: {{count}}
- Revisions complete: {{count}}

**Words:** {{words_today}} (Total: {{cumulative_words}})

---

## Pattern Learning

{{any_patterns_observed_this_session}}

---

## Notes

{{session_notes}}

---

## Next Session

**Goal:** {{next_goal}}  
**Starting point:** {{next_starting_point}}

---

Tags: #session #progress
```

---

## OBSIDIAN SETTINGS

### Recommended Settings

**Files & Links:**
- New link format: Relative path to file
- Use [[Wikilinks]]: Yes
- Default location for new notes: Same folder as current

**Editor:**
- Default view: Reading view OFF (stay in editing)
- Show line numbers: Yes (helpful for referencing)
- Vim key bindings: Optional (if you like them)

**Appearance:**
- Theme: Minimal or Default (less distraction)
- Base mode: Dark (easier on eyes)

---

## USEFUL PLUGINS (Core - Free)

### Templates
- Enables quick scene/session creation
- Settings → Core plugins → Templates → Enable
- Templates folder location: `templates/`
- Hotkey: Ctrl+T

### Daily Notes (Optional)
- Auto-create session logs
- Settings → Core plugins → Daily notes → Enable
- New file location: `06_sessions/`
- Template: `session_log_template.md`

### Graph View
- Visualize connections between scenes
- Useful for seeing story structure
- View → Open graph view

### Quick Switcher
- Jump between files fast
- Hotkey: Ctrl+O
- **ADHD essential** - no digging through folders

### Tag Pane
- See all tags
- Useful for filtering scenes by character
- View → Tag pane

---

## COMMUNITY PLUGINS (Optional - All Free)

### Obsidian Git
- Auto-commit changes
- Backup to GitHub
- Settings → Community plugins → Browse → "Git"

### Dataview
- Query your scenes (e.g., "show all incomplete drafts")
- Advanced, learn later if needed

### Calendar
- Visualize when you worked
- Good for ADHD (see consistency visually)

**Recommendation:** Start with core plugins only. Add community plugins later if needed.

---

## WORKFLOW IN OBSIDIAN

### Starting a New Chapter

1. Create folder: `01_frameworks/chapter_XX/`
2. Use template to create scene frameworks
3. Voice record brainstorm → save to `03_audio/`
4. AI transcribes → save to `03_audio/transcripts/`
5. Collaborate to fill framework template
6. Approve framework
7. Create draft in `02_drafts/chapter_XX/`
8. AI generates prose in draft file
9. You edit directly in Obsidian
10. AI analyzes diff, logs patterns
11. Mark scene ✅ complete
12. Next scene

### Daily Session

1. Open Obsidian
2. Quick switcher (Ctrl+O) → type "session"
3. Create today's session log from template
4. Review what's next
5. Open relevant scene file
6. Work
7. Update session log
8. Save

**Obsidian auto-saves** - no worry about losing work

---

## LINKING STRATEGY

### Link Everything

**From framework to draft:**
```markdown
**Draft:** [[../../02_drafts/chapter_01/scene_1.1_draft]]
```

**Between scenes:**
```markdown
**Previous:** [[scene_1.1_framework]]
**Next:** [[scene_1.3_framework]]
```

**To character profiles:**
```markdown
Maya's profile: [[../../00_architecture/characters#Maya Chen]]
```

**Benefits:**
- Click to navigate instantly
- See connections in graph view
- Never lose context

---

## TAGS STRATEGY

### Suggested Tags

**By status:**
- `#framework_approved`
- `#draft_first`
- `#draft_edited`
- `#draft_final`

**By chapter:**
- `#prologue`
- `#chapter_01` ... `#chapter_24`
- `#epilogue`

**By part:**
- `#part_one` ... `#part_five`

**By character focus:**
- `#maya`
- `#mother`
- `#jordan`
- `#lily`
- `#thorne`

**By scene type:**
- `#audit_scene`
- `#mother_message`
- `#construct_interaction`
- `#cult_scene`

**Search examples:**
```
tag:#mother AND tag:#part_one
```
Shows all mother scenes in Part One

---

## GRAPH VIEW USAGE

**View → Open graph view**

**What you see:**
- Nodes = files
- Lines = links between files

**Useful for:**
- Visualizing story structure
- Seeing which scenes connect
- Finding orphaned notes (no links)
- Understanding story architecture visually

**Filters:**
- Can filter by tag
- Can hide certain folders
- Can focus on specific files

**ADHD benefit:** Visual representation of progress

---

## MOBILE SYNC (Optional)

**Obsidian has mobile app (free):**
- iOS and Android
- Can sync via iCloud, Dropbox, or Obsidian Sync (paid)
- Edit on phone during commute
- Voice notes on phone → transfer to vault

**If interested, set up later.**

---

## CURSOR + OBSIDIAN WORKFLOW

### How They Work Together

**Cursor:**
- AI collaboration
- Voice recording (native)
- Pattern analysis
- Consistency checking

**Obsidian:**
- Writing environment
- File organization
- Visual structure
- Quick navigation

**Flow:**
1. Voice record in Cursor → save to vault `03_audio/`
2. AI transcribes in Cursor → save to vault `03_audio/transcripts/`
3. Collaborate in Cursor to create framework → save to vault `01_frameworks/`
4. AI drafts prose in Cursor → save to vault `02_drafts/`
5. **Switch to Obsidian** → edit prose directly
6. Switch back to Cursor → AI analyzes diffs
7. Repeat

**Alternative flow:**
- Do everything in Obsidian (can edit, AI can read files from vault)
- Cursor reads vault files as needed
- Whichever feels better for you

---

## BACKUP STRATEGY

### Built-in Protection

**Your vault is in repo:**
- `C:\Users\Fab2\Desktop\AI\Specs\constitutional_vault\`
- Plain markdown files
- Can back up entire repo

**Options:**

**1. Manual backup:**
- Copy `constitutional_vault/` to external drive weekly

**2. Git (if comfortable):**
- Track vault in git
- Push to GitHub private repo
- Automatic version history

**3. Cloud sync:**
- OneDrive / Dropbox / Google Drive
- Point to your Specs folder
- Auto-backup

**Recommendation:** At minimum, manual backup weekly to external drive.

---

## FIRST SESSION SETUP CHECKLIST

- [ ] Create `constitutional_vault/` folder in repo
- [ ] Open as vault in Obsidian
- [ ] Create folder structure (00-07 + templates)
- [ ] Create three templates (framework, draft, session)
- [ ] Enable Templates plugin
- [ ] Enable Quick Switcher
- [ ] Set theme to minimal/dark
- [ ] Create `00_architecture/quick_reference.md` with key info
- [ ] Create first session log
- [ ] Ready to work

**Time estimate:** 15-20 minutes setup

---

## TROUBLESHOOTING

### "Can't find file when clicking link"
- Check relative path is correct
- Obsidian uses `/` not `\` in paths
- Case-sensitive on some systems

### "Templates not showing"
- Check Templates plugin enabled
- Check template folder path set correctly
- Try absolute path if relative doesn't work

### "Graph view is overwhelming"
- Filter by tag to show subset
- Hide folders you don't need
- Focus on current chapter only

### "Obsidian slow"
- Likely have many large files
- Consider splitting very large files
- Close graph view if not using

---

## RESOURCES

**Obsidian Help:**
- Help → Obsidian Help (built-in documentation)
- https://help.obsidian.md/

**Markdown Reference:**
- https://www.markdownguide.org/basic-syntax/

**When you need it:**
- Not urgent, can learn as you go
- Obsidian is simple at core (just markdown editing)

---

## REMEMBER

**Obsidian is:**
- Your writing environment
- Your organization system
- Your visual structure

**Obsidian is NOT:**
- Where AI collaboration happens (that's Cursor)
- Complex to learn (markdown + folders + links)
- Required to be perfect (just needs to work for you)

**Start simple. Add complexity only if needed.**

---

**Ready to create your vault and begin writing.**

