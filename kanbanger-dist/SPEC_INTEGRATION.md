# Spec_Engine ↔ Kanbanger Integration

Integration guidelines for generating kanban boards from Spec_Engine specifications.

## Overview

**Spec_Engine** defines structured autonomous workflows with:
- **Goal** → What to achieve
- **Tasks** → How to break it down (sequential)
- **Steps** → Atomic actions
- **Backups** → Fallback methods

**Kanbanger** tracks implementation progress with:
- **Markdown kanban** → Developer-friendly task list
- **GitHub Projects** → Visual dashboard
- **LLM interface** → Conversational management

## Integration Flow

```
Spec Generated → Parse Structure → Generate Kanban → Sync to GitHub
      ↓              ↓                  ↓               ↓
  spec.md      Goal/Tasks/Steps    _kanban.md    Project Board
```

---

## First-Time Setup in Spec_Engine Project

### Prerequisites

1. Existing Spec_Engine repository (already set up)
2. Python 3.8+ installed
3. GitHub repository with access
4. GitHub Personal Access Token

### Decision: Project Structure

**Choose one approach:**

#### Option A: Single Board for All SPECs (Recommended for small projects)

**Structure:**
```
Spec_Engine/
├── SPECs/
│   ├── my_project/
│   │   ├── spec_my_project.md
│   │   └── parameters_my_project.toml
│   └── another_project/
├── _kanban.md              ← Single kanban for all SPECs
├── .kanban.json            ← State tracking
└── .env                    ← Configuration
```

**Pros:**
- Single GitHub Project board
- Unified view of all work
- Simple configuration

**Cons:**
- Can get crowded with many SPECs
- Less granular tracking

#### Option B: Per-SPEC Boards (Recommended for complex projects)

**Structure:**
```
Spec_Engine/
├── SPECs/
│   ├── my_project/
│   │   ├── spec_my_project.md
│   │   ├── _kanban.md      ← Per-SPEC kanban
│   │   └── .kanban.json    ← Per-SPEC state
│   └── another_project/
│       ├── spec_another_project.md
│       ├── _kanban.md
│       └── .kanban.json
├── .env                    ← Shared configuration
└── .gitignore
```

**Pros:**
- Clear separation per SPEC
- Focused tracking
- Can link different GitHub Projects

**Cons:**
- Multiple boards to manage
- Need to sync each separately

### Step 1: Install Kanbanger

```bash
# From within your Spec_Engine project
cd /path/to/Spec_Engine

# Install kanbanger
pip install git+https://github.com/earlyprototype/kanbanger.git

# Or if you have it locally
pip install /path/to/kanbanger
```

### Step 2: Update .gitignore

Add kanbanger files to your existing `.gitignore`:

```bash
# Add to Spec_Engine/.gitignore

# Kanbanger state files (local only)
.kanban.json
**/SPECs/**/.kanban.json

# Kanbanger configuration (contains secrets)
.env
.env.local

# Optional: Ignore kanban markdown if you prefer to generate on-demand
# _kanban.md
# **/SPECs/**/_kanban.md
```

**Note:** You may want to commit `_kanban.md` files to track task planning in version control, but NEVER commit `.env` or `.kanban.json`.

### Step 3: Run Setup Wizard

```bash
# From Spec_Engine root
kanban-sync-setup
```

**Wizard will ask:**

1. **GitHub Token** → Get from https://github.com/settings/tokens
   - Scopes needed: `repo`, `project`

2. **Repository** → Your Spec_Engine repo
   - Example: `earlyprototype/Spec_Engine`

3. **Project** → Choose or create:
   - **Option A (single board):** "Spec_Engine Execution Tracker"
   - **Option B (per-SPEC):** Will prompt for each SPEC

4. **Status Field** → Ensure GitHub Project has:
   - `Backlog`
   - `Todo`
   - `InProgress`
   - `Done`

**Output:**
```
============================================================
  kanban-project-sync Setup Wizard
============================================================

[Step 1/6] Checking .gitignore
-------------------------------------------------------------
  [OK] .gitignore updated with kanbanger entries

[Step 2/6] GitHub Personal Access Token
-------------------------------------------------------------
  [OK] Token valid! Logged in as: earlyprototype

[Step 3/6] GitHub Repository
-------------------------------------------------------------
  [INFO] Using: earlyprototype/Spec_Engine

[Step 4/6] Checking Linked Projects
-------------------------------------------------------------
  [OK] Found 1 linked project(s):
    #1: Spec_Engine Tracker

[Step 5/6] Checking Status Field Configuration
-------------------------------------------------------------
  [OK] Status field configured correctly!

[Step 6/6] Saving Configuration
-------------------------------------------------------------
  [OK] .env file created

Setup Complete!
```

### Step 4: Configure for Your Structure

**For Option A (Single Board):**

Your `.env` should contain:
```bash
GITHUB_TOKEN=ghp_your_token_here
GITHUB_REPO=earlyprototype/Spec_Engine
GITHUB_PROJECT_NUMBER=1
```

**For Option B (Per-SPEC Boards):**

Create multiple GitHub Projects first, then configure per-SPEC:

```bash
# In each SPEC directory, create a .env symlink or override
cd SPECs/my_project/

# Option 1: Symlink to root .env (shares token/repo)
ln -s ../../.env .env

# Option 2: Create local .env with specific project
cat > .env << EOF
GITHUB_TOKEN=ghp_your_token_here
GITHUB_REPO=earlyprototype/Spec_Engine
GITHUB_PROJECT_NUMBER=2
EOF
```

### Step 5: Create Initial Kanban

**Option A (Manual):**
```bash
# Create from scratch
cat > _kanban.md << 'EOF'
# Spec_Engine Execution Tracker

## BACKLOG
*   [ ] Future SPECs and improvements

## TODO
*   [ ] [Add SPECs here as they're created]

## DOING

## DONE
*   [x] Kanbanger integration setup
EOF
```

**Option B (Generated from existing SPEC):**
```bash
# If you already have a SPEC
spec-to-kanban SPECs/my_project/spec_my_project.md
```

### Step 6: Initial Sync

```bash
# Test with dry-run first
kanban-sync _kanban.md --dry-run

# If looks good, sync to GitHub
kanban-sync _kanban.md
```

**Verify:** Check your GitHub Project - should see the initial items!

### Step 7: Automate (Optional)

**Option 1: Git Hook (Auto-sync on commit)**

```bash
# Install hook
cat > .git/hooks/post-commit << 'EOF'
#!/bin/sh
# Auto-sync kanban files when committed

if git diff-tree --no-commit-id --name-only -r HEAD | grep -q "_kanban.md"; then
    echo "Syncing kanban to GitHub..."
    
    # Find and sync all changed kanban files
    for kanban in $(git diff-tree --no-commit-id --name-only -r HEAD | grep "_kanban.md"); do
        echo "  Syncing $kanban"
        kanban-sync "$kanban" 2>&1 | grep -v "^Parsing\|^Loading\|^Connecting"
    done
    
    echo "Kanban sync complete!"
fi
EOF

chmod +x .git/hooks/post-commit
```

**Option 2: Progress Tracking Script**

```bash
# Create sync-all-specs.sh
cat > sync-all-specs.sh << 'EOF'
#!/bin/bash
# Sync all SPEC kanbans to GitHub

SPECS_DIR="SPECs"

if [ -d "$SPECS_DIR" ]; then
    for spec_dir in "$SPECS_DIR"/*/; do
        kanban_file="${spec_dir}_kanban.md"
        if [ -f "$kanban_file" ]; then
            echo "Syncing: $kanban_file"
            cd "$spec_dir"
            kanban-sync _kanban.md
            cd ../..
        fi
    done
else
    # Single board mode
    if [ -f "_kanban.md" ]; then
        kanban-sync _kanban.md
    fi
fi

echo "All kanbans synced!"
EOF

chmod +x sync-all-specs.sh
```

---

## Post-Setup Workflow

### Creating a New SPEC

**1. Generate SPEC (existing Spec_Engine workflow):**
```bash
# Your existing SPEC creation process
create_spec my_new_project
```

**2. Generate corresponding kanban:**
```bash
# Auto-generate from SPEC
spec-to-kanban SPECs/my_new_project/spec_my_new_project.md

# Or manually create
cd SPECs/my_new_project
cat > _kanban.md << EOF
# My New Project Implementation

## TODO
*   [ ] Task 1: [from SPEC]
*   [ ] Task 2: [from SPEC]

## DOING

## DONE
EOF
```

**3. Sync to GitHub:**
```bash
kanban-sync SPECs/my_new_project/_kanban.md
```

### Executing a SPEC with Tracking

**Traditional (no tracking):**
```bash
execute_spec my_project
```

**With kanban tracking:**
```bash
# Terminal 1: Execute SPEC
execute_spec my_project

# Terminal 2: Watch progress and sync
watch -n 60 'sync-spec-progress SPECs/my_project/'
```

This keeps your GitHub board updated in real-time!

---

## Troubleshooting First-Time Setup

### "kanban-sync: command not found"

**Cause:** Scripts directory not in PATH

**Fix:**
```bash
# Use Python module syntax
python -m sync_kanban _kanban.md

# Or add to PATH (PowerShell)
$env:PATH += ";C:\Users\YourName\AppData\Local\Programs\Python\Python312\Scripts"

# Or add to PATH (Bash)
export PATH="$HOME/.local/bin:$PATH"
```

### "No projects found linked to repository"

**Cause:** GitHub Project not linked to repo

**Fix:**
1. Go to https://github.com/earlyprototype/Spec_Engine
2. Click "Projects" tab
3. Click "Link a project"
4. Create new project: "Spec_Engine Tracker"
5. Re-run `kanban-sync-setup`

### "No 'Status' field found"

**Cause:** GitHub Project missing Status field

**Fix:**
1. Open your project on GitHub
2. Click "+ New field"
3. Choose "Single select"
4. Name it "Status"
5. Add options: `Backlog`, `Todo`, `InProgress`, `Done`
6. Re-run `kanban-sync-setup`

### ".env file not loaded"

**Cause:** `python-dotenv` not finding .env

**Fix:**
```bash
# Ensure .env is in the same directory as _kanban.md
# Or in the directory where you run kanban-sync

# Check it's being read
cat .env

# Verify values
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GITHUB_REPO'))"
```

### "Multiple .env files in nested structure"

**Cause:** Per-SPEC .env files not working as expected

**Fix:**
```bash
# Run kanban-sync from within the SPEC directory
cd SPECs/my_project/
kanban-sync _kanban.md

# Or use explicit flags
kanban-sync SPECs/my_project/_kanban.md --repo earlyprototype/Spec_Engine --project 2
```

---

## Recommended Configuration for Spec_Engine

### Directory Structure
```
Spec_Engine/
├── .env                           # Shared: token, default repo
├── .gitignore                     # Includes .kanban.json, .env
├── sync-all-specs.sh              # Sync all kanban boards
├── _kanban.md                     # Optional: master board
├── .kanban.json                   # Optional: master state
├── SPECs/
│   ├── data_pipeline/
│   │   ├── spec_data_pipeline.md
│   │   ├── parameters_data_pipeline.toml
│   │   ├── exe_data_pipeline.md
│   │   ├── progress_data_pipeline.json
│   │   ├── _kanban.md             # Per-SPEC kanban
│   │   └── .kanban.json           # Per-SPEC state (gitignored)
│   └── api_integration/
│       ├── spec_api_integration.md
│       ├── _kanban.md
│       └── .kanban.json
└── .git/hooks/
    └── post-commit                # Auto-sync on commit
```

### .gitignore (Complete)
```bash
# Python
__pycache__/
*.pyc
*.pyo

# Spec_Engine
progress_*.json
*.db

# Kanbanger
.env
.env.local
.kanban.json
**/SPECs/**/.kanban.json

# Optional: Kanban markdown files
# Uncomment if you prefer to generate on-demand
# _kanban.md
# **/SPECs/**/_kanban.md
```

### .env (Template)
```bash
# GitHub Personal Access Token
# Get yours at: https://github.com/settings/tokens
# Required scopes: repo, project
GITHUB_TOKEN=ghp_your_token_here

# GitHub Repository (format: owner/repo)
GITHUB_REPO=earlyprototype/Spec_Engine

# Default GitHub Project Number
# Can be overridden per-SPEC
GITHUB_PROJECT_NUMBER=1
```

---

## Integration Checklist

**Initial Setup:**
- [ ] Kanbanger installed (`pip install kanbanger`)
- [ ] `.gitignore` updated with kanbanger files
- [ ] GitHub Personal Access Token created
- [ ] GitHub Project created and linked to repo
- [ ] Status field configured (Backlog, Todo, InProgress, Done)
- [ ] Setup wizard completed (`kanban-sync-setup`)
- [ ] `.env` file created and verified
- [ ] Decision made: single board vs per-SPEC boards
- [ ] Initial kanban file created
- [ ] Initial sync tested (`kanban-sync --dry-run`)
- [ ] First sync to GitHub successful

**Per-SPEC Setup:**
- [ ] SPEC created in `SPECs/[name]/`
- [ ] Kanban generated (`spec-to-kanban` or manual)
- [ ] Kanban synced to GitHub
- [ ] GitHub Project board verified

**Optional Automation:**
- [ ] Git hook installed (auto-sync on commit)
- [ ] Sync-all script created
- [ ] Progress tracking configured
- [ ] Team notified of GitHub board locations

---

## Next Steps After Setup

1. **Create your first SPEC with kanban tracking**
2. **Execute and observe progress on GitHub**
3. **Iterate on kanban structure** based on what's useful
4. **Share GitHub Projects with team** for visibility
5. **Use LLM to manage kanbans** conversationally

You're now ready to track Spec_Engine executions visually!

---

## Mapping: SPEC Structure → Kanban Columns

### Option A: Sequential Execution (Recommended)

Maps to the **sequential nature** of SPEC tasks:

```markdown
## BACKLOG
*   [ ] [Future tasks not in current SPEC]

## TODO
*   [ ] Task 1: [task_description]
*   [ ] Task 2: [task_description]
*   [ ] Task 3: [task_description]

## DOING
*   [ ] Currently executing task with steps

## DONE
*   [x] Completed tasks
```

**Rationale:** SPECs execute tasks sequentially, so TODO holds the queue.

### Option B: Hierarchical Decomposition

Shows **task → steps** relationship:

```markdown
## PLANNING (Tasks from SPEC)
*   [ ] Task 1: Data validation
*   [ ] Task 2: Transform data
*   [ ] Task 3: Generate report

## TODO (Active task's steps)
*   [ ] Step 1.1: Load CSV file
*   [ ] Step 1.2: Validate schema
*   [ ] Step 1.3: Check for nulls

## DOING (Currently executing step)
*   [ ] Step 1.1: Load CSV file

## DONE (Completed steps + tasks)
*   [x] Step 1.1: Load CSV file
*   [x] Task 1: Data validation
```

**Rationale:** Exposes step-level granularity for detailed tracking.

### Option C: Execution State Mapping

Maps to **exe_[descriptor].md** execution states:

```markdown
## QUEUED (Upcoming tasks)
*   [ ] Task 2: Transform data
*   [ ] Task 3: Generate report

## IN_PROGRESS (Active task + steps)
*   [ ] Task 1: Data validation
*   [ ]   └─ Step 1.1: Load CSV file [EXECUTING]
*   [ ]   └─ Step 1.2: Validate schema [PENDING]
*   [ ]   └─ Step 1.3: Check for nulls [PENDING]

## BLOCKED (Failed steps with exhausted backups)
*   [ ] Step 2.2: API call (all backups failed)

## COMPLETED
*   [x] Task 1: Data validation
```

**Rationale:** Direct reflection of SPEC execution state.

---

## Automatic Generation Rules

### Rule 1: Parse SPEC → Extract Structure

**Input:** `spec_[descriptor].md`

**Extract:**
1. **Goal** (single, top-level)
2. **Tasks** (list with IDs, descriptions)
3. **Steps** (nested under tasks, with expected outputs)
4. **Criticality** (from parameters.toml if needed)

**Example SPEC:**
```markdown
# Goal
Analyze user feedback data and generate insights report.

## Task 1: Data Collection
### Step 1.1: Fetch feedback from API
Expected Output: JSON file with 100+ feedback entries

### Step 1.2: Validate data completeness
Expected Output: Validation report

## Task 2: Sentiment Analysis
### Step 2.1: Run NLP model on feedback
Expected Output: Sentiment scores per entry
```

### Rule 2: Generate Kanban Structure

**Output:** `_kanban.md`

```markdown
# [SPEC Goal as Title]

## BACKLOG
[Empty initially - for future enhancements]

## TODO
*   [ ] Task 1: Data Collection
*   [ ] Task 2: Sentiment Analysis

## DOING
[Empty initially - populated when execution starts]

## DONE
[Empty initially - populated as tasks complete]
```

### Rule 3: LLM Expansion (Optional)

LLM can **enrich** the basic structure:

**Prompt for LLM:**
```
Given this SPEC:
- Goal: [goal]
- Tasks: [list]

Generate a kanban board that:
1. Creates a task item for each SPEC task
2. Adds preparatory items (setup, environment, dependencies)
3. Adds verification items (testing, validation)
4. Suggests documentation tasks

Use kanban-sync markdown format.
```

**Example Enriched Output:**
```markdown
# User Feedback Analysis Kanban

## BACKLOG
*   [ ] Add support for additional data sources
*   [ ] Automate report delivery
*   [ ] Create dashboard visualization

## TODO
*   [ ] Set up Python environment with NLP dependencies
*   [ ] Task 1: Data Collection
*   [ ] Task 2: Sentiment Analysis
*   [ ] Validate report against acceptance criteria
*   [ ] Write execution summary

## DOING

## DONE
*   [x] Review SPEC requirements
```

---

## Integration Patterns

### Pattern 1: Pre-Execution Generation

**Trigger:** After SPEC is created, before execution

```bash
# 1. Generate SPEC
create_spec my_project

# 2. Auto-generate kanban
spec-to-kanban SPECs/my_project/spec_my_project.md

# 3. Sync to GitHub
kanban-sync SPECs/my_project/_kanban.md

# 4. Execute SPEC
execute_spec my_project
```

**Benefits:**
- Plan visible before execution
- Team can review task breakdown
- GitHub board ready for tracking

### Pattern 2: Live Execution Tracking

**Trigger:** During SPEC execution, update kanban from `progress.json`

```bash
# In background during execution:
watch -n 30 'sync-spec-progress SPECs/my_project/'

# Reads: progress_my_project.json
# Updates: _kanban.md (moves tasks to DOING/DONE)
# Syncs: kanban-sync automatically
```

**Benefits:**
- Real-time progress visibility
- GitHub board reflects current state
- No manual updates needed

### Pattern 3: Post-Execution Retrospective

**Trigger:** After SPEC completes

```bash
# Generate retrospective kanban showing:
# - What completed successfully
# - What required backups
# - What failed
# - Lessons learned

spec-retrospective SPECs/my_project/ > _retrospective.md
kanban-sync _retrospective.md --repo owner/repo --project 2
```

**Benefits:**
- Learning from execution
- Identify SPEC improvements
- Document for future reference

---

## Implementation: spec-to-kanban Command

### Basic Version

```python
import re
from pathlib import Path

def parse_spec(spec_file):
    """Extract goal and tasks from spec.md"""
    with open(spec_file, 'r') as f:
        content = f.read()
    
    # Extract goal
    goal_match = re.search(r'^# Goal\n(.+?)$', content, re.MULTILINE)
    goal = goal_match.group(1).strip() if goal_match else "SPEC Goal"
    
    # Extract tasks
    tasks = []
    task_pattern = r'^## (Task \d+): (.+?)$'
    for match in re.finditer(task_pattern, content, re.MULTILINE):
        task_id = match.group(1)
        task_desc = match.group(2)
        tasks.append(f"*   [ ] {task_id}: {task_desc}")
    
    return goal, tasks

def generate_kanban(goal, tasks, output_file):
    """Generate kanban markdown"""
    content = f"""# {goal} - Implementation Tracker

## BACKLOG
*   [ ] Future enhancements from retrospective

## TODO
{chr(10).join(tasks)}

## DOING

## DONE
*   [x] SPEC created and reviewed
"""
    
    with open(output_file, 'w') as f:
        f.write(content)

# Usage
spec_path = "SPECs/my_project/spec_my_project.md"
kanban_path = "SPECs/my_project/_kanban.md"

goal, tasks = parse_spec(spec_path)
generate_kanban(goal, tasks, kanban_path)
print(f"Kanban generated: {kanban_path}")
print(f"Next: kanban-sync {kanban_path}")
```

### Enhanced Version with LLM

```python
def llm_enrich_kanban(goal, tasks, llm_client):
    """Use LLM to add preparatory and validation tasks"""
    
    prompt = f"""
    Given this SPEC goal: "{goal}"
    
    And these main tasks:
    {chr(10).join(tasks)}
    
    Generate a complete kanban board in markdown format that includes:
    1. Preparatory tasks (setup, dependencies, configuration)
    2. The main SPEC tasks
    3. Validation tasks (testing, verification)
    4. Documentation tasks
    
    Use this format:
    ## BACKLOG
    *   [ ] future tasks
    
    ## TODO
    *   [ ] all tasks in order
    
    ## DOING
    (empty)
    
    ## DONE
    *   [x] initial setup
    
    Follow kanban-sync format rules from LLM_GUIDANCE.md
    """
    
    enriched_kanban = llm_client.generate(prompt)
    return enriched_kanban
```

---

## Progress Tracking Integration

### Sync progress.json → Kanban

```python
import json

def sync_progress_to_kanban(progress_file, kanban_file):
    """Update kanban based on SPEC execution progress"""
    
    with open(progress_file, 'r') as f:
        progress = json.load(f)
    
    # Read current kanban
    with open(kanban_file, 'r') as f:
        kanban = f.read()
    
    # For each task in progress
    for task_id, task_data in progress.get('tasks', {}).items():
        status = task_data.get('status')
        task_desc = task_data.get('description')
        
        task_line = f"*   [ ] {task_id}: {task_desc}"
        
        if status == 'completed':
            # Move to DONE
            completed_line = f"*   [x] {task_id}: {task_desc}"
            kanban = move_task_to_column(kanban, task_line, 'DONE', completed_line)
        
        elif status == 'in_progress':
            # Move to DOING
            kanban = move_task_to_column(kanban, task_line, 'DOING')
        
        elif status == 'blocked':
            # Add note about blockage
            blocked_line = f"*   [ ] {task_id}: {task_desc} [BLOCKED - see progress.json]"
            kanban = move_task_to_column(kanban, task_line, 'DOING', blocked_line)
    
    # Write updated kanban
    with open(kanban_file, 'w') as f:
        f.write(kanban)
    
    return True

def move_task_to_column(kanban, task_line, target_column, new_line=None):
    """Helper to move task between columns"""
    # Implementation left as exercise
    # Remove task from current column
    # Add to target column
    # Optionally replace with new_line
    pass
```

---

## Configuration

### .spec-kanban.config.json

```json
{
  "auto_generate": true,
  "generate_on_spec_creation": true,
  "track_progress_live": false,
  "enrich_with_llm": true,
  "kanban_location": "same_as_spec",
  "sync_to_github": true,
  "column_mapping": "sequential",
  "include_steps": false,
  "add_preparatory_tasks": true,
  "add_validation_tasks": true
}
```

---

## LLM Guidance for SPEC → Kanban

### Prompts for LLMs

**Generate kanban from SPEC:**
```
I have a Spec_Engine SPEC file. Please:
1. Read the SPEC goal and tasks
2. Generate a kanban board in markdown format
3. Include preparatory tasks (setup, dependencies)
4. Include validation tasks (testing, verification)
5. Use the kanban-sync format from LLM_GUIDANCE.md
6. Save to _kanban.md

SPEC content:
[paste spec.md]
```

**Update kanban from progress:**
```
I have a progress.json from SPEC execution:
[paste progress.json]

Update my _kanban.md to reflect:
- Completed tasks → move to DONE
- In-progress tasks → move to DOING
- Blocked tasks → add [BLOCKED] note
```

**Create retrospective:**
```
SPEC execution completed. Based on progress.json:
[paste progress.json]

Create a retrospective kanban showing:
- What went well (used primary methods)
- What needed backups (list which backups)
- What failed (exhausted all backups)
- Lessons for improving the SPEC
```

---

## Workflow Examples

### Example 1: Data Pipeline SPEC

**SPEC Goal:** Process customer data and generate segmentation report

**Generated Kanban:**
```markdown
# Customer Segmentation Pipeline

## BACKLOG
*   [ ] Add real-time processing capability
*   [ ] Support additional data sources
*   [ ] Automate report distribution

## TODO
*   [ ] Set up Python environment (pandas, scikit-learn)
*   [ ] Configure database connections
*   [ ] Task 1: Extract customer data from database
*   [ ] Task 2: Clean and transform data
*   [ ] Task 3: Apply clustering algorithm
*   [ ] Task 4: Generate segmentation report
*   [ ] Validate report accuracy
*   [ ] Document methodology

## DOING

## DONE
*   [x] Review SPEC requirements
*   [x] Prepare test dataset
```

**After Execution:**
```markdown
## DOING

## DONE
*   [x] Review SPEC requirements
*   [x] Prepare test dataset
*   [x] Set up Python environment
*   [x] Configure database connections
*   [x] Task 1: Extract customer data
*   [x] Task 2: Clean and transform data (used Backup #1 - pandas fallback)
*   [x] Task 3: Apply clustering algorithm
*   [x] Task 4: Generate report
*   [x] Validate report accuracy
```

### Example 2: API Integration SPEC

**SPEC Goal:** Integrate third-party payment API into e-commerce platform

**Generated Kanban:**
```markdown
# Payment API Integration

## BACKLOG
*   [ ] Add webhook handling for async notifications
*   [ ] Implement refund functionality
*   [ ] Add fraud detection

## TODO
*   [ ] Obtain API credentials from payment provider
*   [ ] Set up sandbox environment
*   [ ] Task 1: Implement authentication flow
*   [ ] Task 2: Create payment initiation endpoint
*   [ ] Task 3: Handle payment callbacks
*   [ ] Task 4: Add error handling and retries
*   [ ] Write integration tests
*   [ ] Test in sandbox
*   [ ] Document API usage

## DOING

## DONE
*   [x] Read API documentation
```

---

## Anti-Patterns to Avoid

**❌ Don't duplicate SPEC structure:**
```markdown
## TODO
*   [ ] Task 1
*   [ ]   └─ Step 1.1
*   [ ]   └─ Step 1.2
*   [ ] Task 2
```
**Why:** Too granular, hard to track, defeats kanban's simplicity

**✅ Do keep it task-level:**
```markdown
## TODO
*   [ ] Task 1: Data Collection
*   [ ] Task 2: Data Analysis
```

---

**❌ Don't lose SPEC context:**
```markdown
## TODO
*   [ ] Do the thing
*   [ ] Check stuff
```
**Why:** Kanban loses connection to SPEC

**✅ Do reference SPEC:**
```markdown
## TODO
*   [ ] Task 1: Data Collection (SPEC: spec_analysis.md)
*   [ ] Task 2: Data Analysis
```

---

**❌ Don't manually sync:**
```markdown
# Update kanban manually based on progress.json
```
**Why:** Error-prone, time-consuming

**✅ Do automate:**
```bash
# Automatic sync from progress tracking
sync-spec-progress SPECs/my_project/
```

---

## Integration Checklist

- [ ] SPEC created (`spec_[descriptor].md`)
- [ ] Kanban generated (`_kanban.md`)
- [ ] LLM enrichment applied (optional)
- [ ] Synced to GitHub (`kanban-sync`)
- [ ] Progress tracking configured (optional)
- [ ] Team notified of GitHub project board
- [ ] SPEC execution started
- [ ] Kanban updated during execution (manual or automatic)
- [ ] Retrospective created post-execution
- [ ] Lessons fed back to improve future SPECs

---

## Future Enhancements

1. **Bidirectional Sync:**
   - GitHub edits → Update SPEC
   - Kanban completion → Mark SPEC steps complete

2. **Backup Visibility:**
   - Show which backups were used
   - Track backup success rates
   - Visualize fallback paths

3. **SPEC Metrics:**
   - Task completion velocity
   - Backup usage frequency
   - Critical step failure rate
   - Use kanban as data source

4. **Multi-SPEC Dashboards:**
   - One kanban board per SPEC
   - Master board aggregating all SPECs
   - Cross-SPEC dependency tracking

---

## Conclusion

**Spec_Engine** provides structure for autonomous LLM execution.  
**Kanbanger** provides visibility and human oversight.

Together they enable:
- **Structured planning** (SPEC)
- **Visible execution** (Kanban)
- **Team collaboration** (GitHub)
- **LLM assistance** (Conversational management)

This integration turns SPECs from abstract specifications into **tracked, visible, collaborative workflows**.

---

## References

- [Spec_Engine Repository](https://github.com/earlyprototype/Spec_Engine)
- [Kanbanger LLM Guidance](LLM_GUIDANCE.md)
- [Kanbanger LLM Workflow](LLM_WORKFLOW.md)
