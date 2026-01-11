# LLM-First Kanban Workflow

Guide for using kanbanger with AI assistants as the primary interface for project management.

## The Vision

Instead of clicking around GitHub's UI, you **talk to an LLM** to manage your projects:

> **You:** "Create a kanban board for my Python web scraper project"
> 
> **LLM:** [Creates `_kanban.md` with starter tasks]
> 
> **You:** "I finished the HTTP client part"
> 
> **LLM:** [Moves task to DONE]
> 
> **You:** kanban-sync _kanban.md
> 
> **Tool:** Syncs to GitHub → Visual project board updated!

**Result:** Natural language project management with GitHub as your visual dashboard.

---

## Core Workflow

### 1. Start New Project

**You to LLM:**
```
"I'm starting a [project type]. Create a kanban board 
with typical tasks for this kind of project."
```

**LLM creates:** `_kanban.md`

**You run:**
```bash
kanban-sync-setup  # One-time: configure GitHub
kanban-sync _kanban.md  # Sync to GitHub
```

**GitHub shows:** Your project board populated with tasks

### 2. Daily Updates

**Morning:**
> **You:** "Show me what's in progress"
> **LLM:** [Reads DOING section]

**Throughout day:**
> **You:** "Add 'fix the caching bug' to TODO"
> **LLM:** [Edits markdown]

> **You:** "Move 'implement API client' to done"
> **LLM:** [Moves task, marks complete]

**End of day:**
```bash
kanban-sync _kanban.md
```

**GitHub updates** with your progress

### 3. Planning Sessions

**You to LLM:**
```
"Review my backlog and suggest what to prioritize for next sprint"
```

**LLM:**
- Analyzes current tasks
- Suggests priorities
- Moves items from BACKLOG → TODO
- Breaks down large tasks

**You:**
```bash
kanban-sync _kanban.md  # Publish the plan
```

**Team sees** updated priorities on GitHub

---

## LLM-Enhanced Features

### 1. Smart Task Generation

**User:** "Add tasks for implementing user authentication"

**LLM generates:**
```markdown
## TODO
*   [ ] Design database schema for users table
*   [ ] Implement password hashing with bcrypt
*   [ ] Create login endpoint
*   [ ] Create registration endpoint
*   [ ] Add JWT token generation
*   [ ] Implement token validation middleware
*   [ ] Add password reset flow
*   [ ] Write unit tests for auth module
```

### 2. Task Breakdown

**User:** "Break down 'build frontend' into smaller tasks"

**LLM:**
```markdown
## BACKLOG
*   [ ] Build frontend  ← Removed

## TODO
*   [ ] Set up React project with Vite
*   [ ] Create component structure
*   [ ] Implement routing with React Router
*   [ ] Build authentication UI
*   [ ] Create dashboard layout
*   [ ] Add state management (Redux/Zustand)
*   [ ] Integrate with backend API
*   [ ] Add error handling and loading states
```

### 3. Progress Summaries

**User:** "What did I accomplish this week?"

**LLM reads DONE section:**
```
This week you completed:
- Implemented API authentication (moved to Done on Mon)
- Fixed caching bug (moved to Done on Wed)  
- Updated documentation (moved to Done on Fri)

Still in progress:
- Database migration (in DOING since Mon)

Next up in TODO:
- Add error handling
- Write integration tests
```

### 4. Smart Prioritization

**User:** "Reorganize my TODO by what's most important"

**LLM analyzes and reorders:**
```markdown
## TODO
*   [ ] Fix critical payment processing bug  ← High priority
*   [ ] Implement data backup  ← High priority
*   [ ] Add error logging  ← Medium priority
*   [ ] Update README  ← Low priority
*   [ ] Refactor old code  ← Low priority
```

### 5. Context-Aware Suggestions

**User:** "What should I work on next?"

**LLM considers:**
- Dependencies (can't do X until Y is done)
- Priorities (critical bugs first)
- Context (if you just finished API work, suggest related tasks)
- Blockers (identify what's blocking progress)

```
I suggest working on "Add error handling to API" because:
1. It's blocking the integration tests
2. You just finished the API implementation (good context)
3. It's marked as high priority
4. No dependencies - you can start immediately
```

### 6. Template Generation

**User:** "Create a kanban for a typical React + Node.js project"

**LLM generates complete starter board:**
```markdown
# React + Node.js Project Kanban

## BACKLOG
*   [ ] Add user profile features
*   [ ] Implement notifications
*   [ ] Add analytics tracking
*   [ ] Set up CI/CD pipeline
*   [ ] Add monitoring and logging

## TODO
*   [ ] Set up project structure (frontend + backend)
*   [ ] Initialize Git repository
*   [ ] Set up database (PostgreSQL)
*   [ ] Design database schema
*   [ ] Create API endpoints
*   [ ] Build React components
*   [ ] Add authentication
*   [ ] Write tests

## DOING
*   [ ] Set up development environment

## DONE
*   [x] Choose tech stack
```

---

## GitHub as Visualization Layer

GitHub Projects becomes your **read-only visual dashboard** while markdown is the **write interface**.

### Benefits

**Markdown + LLM:**
- Fast text-based editing
- Natural language commands
- Version controlled (Git)
- Works offline
- Search with grep/ripgrep
- Easy bulk operations

**GitHub Projects:**
- Visual kanban board
- Shareable with team
- Mobile-friendly view
- Filterable/sortable
- Integrates with Issues/PRs
- Professional presentation

### Team Collaboration

**Your workflow:**
```
You + LLM → Edit _kanban.md → Sync → GitHub
```

**Team workflow:**
```
Team → View GitHub → (Optional) Edit directly → Sync pulls changes
```

**With bidirectional sync (future):**
- You use markdown + LLM
- Team uses GitHub UI
- Both stay in sync automatically

---

## LLM Prompt Templates

Share these with your AI assistant:

### Project Setup
```
Create a kanban board for [project type] with:
- Typical tasks for this kind of project
- Organized by priority
- Realistic scope for a [timeframe]
- Use the kanban-sync markdown format
```

### Daily Management
```
My kanban file is at _kanban.md. Please:
- Add "[task]" to [column]
- Move "[task]" from [column] to [column]
- Mark "[task]" as complete
- Show me what's in [column]
```

### Planning
```
Review my kanban board and:
- Suggest what to prioritize next
- Identify any blockers
- Break down large tasks
- Estimate effort (add tags like [2h], [1d])
```

### Retrospective
```
Analyze my kanban board's DONE section and summarize:
- What was completed
- Velocity (tasks per week)
- Patterns in the work
- Suggestions for improvement
```

---

## Advanced: Multi-Project Management

### Structure
```
project-root/
├── frontend/_kanban.md
├── backend/_kanban.md
├── devops/_kanban.md
└── docs/_kanban.md
```

### LLM Commands
```
"Show me all in-progress tasks across all projects"
"What's blocking progress in the backend?"
"Move all high-priority items to the top"
```

### Sync
```bash
# Sync all projects
find . -name "_kanban.md" -exec kanban-sync {} \;

# Or create a script
./sync-all-projects.sh
```

---

## Integration with Development Workflow

### Git Hooks

**Auto-sync on commit:**
```bash
# .git/hooks/post-commit
#!/bin/sh
if git diff-tree --no-commit-id --name-only -r HEAD | grep -q "_kanban.md"; then
    kanban-sync _kanban.md
    echo "Kanban synced to GitHub!"
fi
```

### VS Code Integration

**Tasks.json:**
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Sync Kanban",
      "type": "shell",
      "command": "kanban-sync _kanban.md",
      "problemMatcher": []
    }
  ]
}
```

Press `Ctrl+Shift+B` → Select "Sync Kanban"

### AI Assistant Integration

**Cursor/Continue/Copilot:**
```
Have AI read LLM_GUIDANCE.md for format rules
Can edit _kanban.md directly in IDE
Remind to run sync after edits
```

---

## Example: Full Project Lifecycle

### Week 1: Project Start

**You:** "Claude, I'm building a Rust CLI tool for file conversion. Create a kanban board."

**Claude creates `_kanban.md`:**
```markdown
## BACKLOG
*   [ ] Add GUI interface
*   [ ] Support batch processing
*   [ ] Add compression options

## TODO
*   [ ] Set up Cargo project
*   [ ] Define CLI argument structure
*   [ ] Implement file reading
*   [ ] Implement conversion logic
*   [ ] Add error handling
*   [ ] Write tests

## DOING
*   [ ] Research file format specifications

## DONE
```

```bash
kanban-sync-setup
kanban-sync _kanban.md
```

GitHub Project created with all tasks!

### Week 2: Development

**Monday morning:**
> **You:** "Move 'Research file format specifications' to done. Move 'Set up Cargo project' to doing."

**Throughout week:**
> **You:** "Add 'implement progress bar' to TODO"
> **You:** "Mark 'Set up Cargo project' as done"
> **You:** "Break down 'implement conversion logic' into smaller tasks"

**Friday evening:**
```bash
kanban-sync _kanban.md
```

Week's progress visible on GitHub!

### Week 3: Planning

**You:** "What should I focus on next week? Consider dependencies and priorities."

**Claude analyzes:**
```
Focus on these in order:
1. Implement file reading (blocks conversion logic)
2. Implement conversion logic (core feature)
3. Add error handling (important for stability)

Leave for later:
- Tests (do after core features)
- Progress bar (nice-to-have)
```

**You:** "Update my TODO to reflect that order"

**Claude reorders tasks**

```bash
kanban-sync _kanban.md
```

Team sees the weekly plan!

### Month End: Retrospective

**You:** "Summarize what we accomplished this month"

**Claude reads DONE:**
```
Completed this month:
- Project setup and structure
- File format research
- File reading implementation
- Basic conversion logic
- Error handling framework
- Unit test suite

Velocity: ~6 tasks/week
Next milestone: Release v0.1.0 with core features
```

---

## Why This Works

### Traditional Approach Problems
- ❌ Clicking through UIs is slow
- ❌ Context switching breaks flow
- ❌ Hard to bulk edit
- ❌ Can't version control board state
- ❌ Difficult to automate

### LLM + Markdown + kanbanger Solution
- ✅ Natural language commands
- ✅ Stay in terminal/editor
- ✅ Text operations are fast
- ✅ Git tracks all changes
- ✅ Scriptable and automatable
- ✅ LLM handles tedious organization
- ✅ GitHub provides visual polish

### The Killer Combo

```
Your Brain → LLM (task management assistant)
           ↓
    Markdown (fast, versionable, text-based)
           ↓
    kanbanger (sync engine)
           ↓
    GitHub Projects (visual dashboard, team sharing)
```

You get the **speed of text** with the **polish of GitHub's UI**.

---

## Getting Started

1. **Install kanbanger:**
   ```bash
   pip install .
   ```

2. **Run setup wizard:**
   ```bash
   kanban-sync-setup
   ```

3. **Tell your LLM:**
   ```
   "I'm using kanban-project-sync. Please read LLM_GUIDANCE.md 
   to learn the format. Create a kanban board for [my project]."
   ```

4. **Sync to GitHub:**
   ```bash
   kanban-sync _kanban.md
   ```

5. **Iterate:**
   - Talk to LLM to manage tasks
   - Sync periodically
   - View on GitHub anytime

---

## Future Enhancements

**Auto-sync on save:**
- File watcher detects changes
- Auto-runs sync in background
- No manual sync needed

**Rich LLM context:**
- LLM reads commit history
- Suggests tasks based on code changes
- Links tasks to code changes

**Voice interface:**
- "Siri/Alexa, add task to my kanban"
- Voice-to-text → LLM → Markdown → GitHub

**Analytics:**
- LLM generates velocity charts
- Burndown visualization
- Productivity insights

---

## Conclusion

Kanbanger enables a **conversational project management workflow** where:
- You tell an AI what you're working on
- AI maintains structured markdown
- GitHub displays beautiful project boards
- Everyone stays in sync

This is project management at the **speed of thought** with the **professionalism of GitHub Projects**.
