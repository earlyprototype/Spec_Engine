"""
Spec_Engine Integration Script for Kanbanger

Automatically sets up kanbanger in a Spec_Engine project.
"""
import os
import sys
import shutil
from pathlib import Path


def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def print_step(step, text):
    print(f"\n[{step}] {text}")
    print("-" * 60)


def print_success(text):
    print(f"  [OK] {text}")


def print_error(text):
    print(f"  [ERROR] {text}")


def print_info(text):
    print(f"  [INFO] {text}")


def check_spec_engine_project():
    """Verify we're in a Spec_Engine project."""
    specs_dir = Path("SPECs")
    
    if not specs_dir.exists():
        print_error("SPECs directory not found")
        print_info("This doesn't appear to be a Spec_Engine project")
        print_info("Expected directory structure:")
        print_info("  SPECs/")
        print_info("  __SPEC_Engine/")
        return False
    
    print_success("Spec_Engine project detected")
    return True


def update_gitignore():
    """Add kanbanger entries to .gitignore."""
    gitignore_path = Path(".gitignore")
    
    kanbanger_entries = """
# Kanbanger state files (local only)
.kanban.json
**/SPECs/**/.kanban.json

# Kanbanger configuration (contains secrets)
.env
.env.local

# Optional: Uncomment to ignore kanban markdown files
# _kanban.md
# **/SPECs/**/_kanban.md
"""
    
    if not gitignore_path.exists():
        print_info("Creating .gitignore")
        with open(gitignore_path, 'w') as f:
            f.write(kanbanger_entries)
        print_success(".gitignore created")
        return
    
    with open(gitignore_path, 'r') as f:
        content = f.read()
    
    if '.kanban.json' in content:
        print_success(".gitignore already has kanbanger entries")
        return
    
    with open(gitignore_path, 'a') as f:
        f.write(kanbanger_entries)
    
    print_success(".gitignore updated with kanbanger entries")


def create_env_template():
    """Create .env.example template."""
    env_example = Path(".env.example")
    
    content = """# GitHub Personal Access Token
# Get yours at: https://github.com/settings/tokens
# Required scopes: repo, project
GITHUB_TOKEN=ghp_your_token_here

# GitHub Repository (format: owner/repo)
GITHUB_REPO=earlyprototype/Spec_Engine

# Default GitHub Project Number (optional)
# Can be overridden per-SPEC or auto-discovered
# GITHUB_PROJECT_NUMBER=1
"""
    
    with open(env_example, 'w') as f:
        f.write(content)
    
    print_success(".env.example created")
    print_info("Copy to .env and fill in your values:")
    print_info("  cp .env.example .env")


def create_sync_all_script():
    """Create script to sync all SPEC kanbans."""
    script_path = Path("sync-all-specs.sh")
    
    content = """#!/bin/bash
# Sync all SPEC kanbans to GitHub

SPECS_DIR="SPECs"

echo "Syncing all SPEC kanbans..."

if [ -d "$SPECS_DIR" ]; then
    for spec_dir in "$SPECS_DIR"/*/; do
        kanban_file="${spec_dir}_kanban.md"
        if [ -f "$kanban_file" ]; then
            spec_name=$(basename "$spec_dir")
            echo "  Syncing: $spec_name"
            (cd "$spec_dir" && kanban-sync _kanban.md 2>&1 | grep -E "CREATE|UPDATE|ARCHIVE|OK|ERROR")
        fi
    done
    echo "All SPEC kanbans synced!"
else
    # Single board mode
    if [ -f "_kanban.md" ]; then
        echo "  Syncing master kanban"
        kanban-sync _kanban.md
        echo "Master kanban synced!"
    else
        echo "No kanban files found"
    fi
fi
"""
    
    with open(script_path, 'w') as f:
        f.write(content)
    
    # Make executable
    try:
        os.chmod(script_path, 0o755)
        print_success("sync-all-specs.sh created (executable)")
    except Exception as e:
        print_success("sync-all-specs.sh created")
        print_info("Make executable with: chmod +x sync-all-specs.sh")


def create_spec_to_kanban_script():
    """Create spec-to-kanban converter script."""
    script_path = Path("spec-to-kanban.py")
    
    content = '''#!/usr/bin/env python3
"""
Convert Spec_Engine SPEC to Kanban markdown.

Usage:
    python spec-to-kanban.py SPECs/my_project/spec_my_project.md
"""
import re
import sys
from pathlib import Path


def parse_spec(spec_file):
    """Extract goal and tasks from spec.md"""
    with open(spec_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract goal
    goal_match = re.search(r'^# Goal\\s*\\n(.+?)$', content, re.MULTILINE)
    goal = goal_match.group(1).strip() if goal_match else "SPEC Implementation"
    
    # Extract tasks
    tasks = []
    task_pattern = r'^## (Task \\d+): (.+?)$'
    for match in re.finditer(task_pattern, content, re.MULTILINE):
        task_id = match.group(1)
        task_desc = match.group(2).strip()
        tasks.append(f"*   [ ] {task_id}: {task_desc}")
    
    return goal, tasks


def generate_kanban(goal, tasks, spec_file):
    """Generate kanban markdown"""
    
    spec_name = Path(spec_file).stem
    
    content = f"""# {goal}

## BACKLOG
*   [ ] Future enhancements from retrospective
*   [ ] Additional features not in current SPEC

## TODO
{chr(10).join(tasks) if tasks else "*   [ ] [No tasks found in SPEC]"}
*   [ ] Validate results against acceptance criteria
*   [ ] Document execution results

## DOING

## DONE
*   [x] SPEC created and reviewed ({spec_name})
"""
    
    return content


def main():
    if len(sys.argv) < 2:
        print("Usage: python spec-to-kanban.py SPECs/my_project/spec_my_project.md")
        print("       python spec-to-kanban.py SPECs/my_project/spec_my_project.md -o output.md")
        sys.exit(1)
    
    spec_file = sys.argv[1]
    spec_path = Path(spec_file)
    
    if not spec_path.exists():
        print(f"Error: SPEC file not found: {spec_file}")
        sys.exit(1)
    
    # Determine output file
    if len(sys.argv) >= 4 and sys.argv[2] == '-o':
        output_file = Path(sys.argv[3])
    else:
        # Same directory as spec
        output_file = spec_path.parent / "_kanban.md"
    
    print(f"Parsing SPEC: {spec_file}")
    goal, tasks = parse_spec(spec_file)
    
    print(f"Goal: {goal}")
    print(f"Tasks found: {len(tasks)}")
    
    kanban_content = generate_kanban(goal, tasks, spec_file)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(kanban_content)
    
    print(f"\\nKanban created: {output_file}")
    print(f"\\nNext steps:")
    print(f"  1. Review and edit: {output_file}")
    print(f"  2. Sync to GitHub: kanban-sync {output_file}")


if __name__ == "__main__":
    main()
'''
    
    with open(script_path, 'w') as f:
        f.write(content)
    
    try:
        os.chmod(script_path, 0o755)
        print_success("spec-to-kanban.py created (executable)")
    except:
        print_success("spec-to-kanban.py created")


def create_git_hook():
    """Create git post-commit hook for auto-sync."""
    hook_path = Path(".git/hooks/post-commit")
    
    if not Path(".git").exists():
        print_info("Not a git repository, skipping hook creation")
        return
    
    content = """#!/bin/sh
# Auto-sync kanban files when committed

if git diff-tree --no-commit-id --name-only -r HEAD | grep -q "_kanban.md"; then
    echo "Kanban files changed, syncing to GitHub..."
    
    # Sync all changed kanban files
    for kanban in $(git diff-tree --no-commit-id --name-only -r HEAD | grep "_kanban.md"); do
        if [ -f "$kanban" ]; then
            echo "  Syncing: $kanban"
            kanban-sync "$kanban" 2>&1 | grep -E "CREATE|UPDATE|ARCHIVE|complete"
        fi
    done
    
    echo "Kanban sync complete!"
fi
"""
    
    # Check if hook already exists
    if hook_path.exists():
        print_info("Git post-commit hook already exists")
        print_info("To add auto-sync, append the following to .git/hooks/post-commit:")
        print(content)
        return
    
    # Create hooks directory if needed
    hook_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(hook_path, 'w') as f:
        f.write(content)
    
    try:
        os.chmod(hook_path, 0o755)
        print_success("Git post-commit hook created")
        print_info("Kanban files will auto-sync when committed")
    except:
        print_success("Git post-commit hook created")
        print_info("Make executable with: chmod +x .git/hooks/post-commit")


def create_readme_section():
    """Create integration README."""
    readme_path = Path("KANBANGER_INTEGRATION.md")
    
    content = """# Kanbanger Integration in Spec_Engine

This Spec_Engine project has been integrated with kanbanger for visual task tracking.

## Quick Start

### 1. Configure GitHub Connection

```bash
# Copy template and edit
cp .env.example .env
# Add your GitHub token and repo details
```

### 2. Run Setup Wizard

```bash
kanban-sync-setup
```

This will:
- Validate your GitHub token
- Check repository access
- Verify project is linked
- Confirm Status field configuration

### 3. Create Kanban from SPEC

```bash
# Generate kanban from existing SPEC
python spec-to-kanban.py SPECs/my_project/spec_my_project.md

# Review the generated _kanban.md
# Edit as needed
```

### 4. Sync to GitHub

```bash
# Test first
kanban-sync SPECs/my_project/_kanban.md --dry-run

# Then sync
kanban-sync SPECs/my_project/_kanban.md
```

## Workflow

### Creating New SPEC with Kanban

```bash
# 1. Create SPEC (your existing workflow)
create_spec my_new_project

# 2. Generate kanban
python spec-to-kanban.py SPECs/my_new_project/spec_my_new_project.md

# 3. Edit kanban if needed
nano SPECs/my_new_project/_kanban.md

# 4. Sync to GitHub
kanban-sync SPECs/my_new_project/_kanban.md
```

### Syncing All SPECs

```bash
# Sync all SPEC kanbans at once
./sync-all-specs.sh
```

### Updating Kanban

Edit the markdown file and sync:

```bash
# Edit tasks
nano SPECs/my_project/_kanban.md

# Sync changes
kanban-sync SPECs/my_project/_kanban.md
```

## Files Created

- `.env.example` - Template for configuration
- `.gitignore` - Updated with kanbanger entries
- `spec-to-kanban.py` - Convert SPEC to kanban
- `sync-all-specs.sh` - Sync all kanbans
- `.git/hooks/post-commit` - Auto-sync on commit (optional)
- `KANBANGER_INTEGRATION.md` - This file

## Directory Structure

```
Spec_Engine/
├── .env                           # Config (gitignored)
├── .env.example                   # Config template
├── .gitignore                     # Includes kanbanger files
├── spec-to-kanban.py              # SPEC → Kanban converter
├── sync-all-specs.sh              # Sync all script
├── SPECs/
│   └── my_project/
│       ├── spec_my_project.md     # Your SPEC
│       ├── _kanban.md             # Generated kanban
│       └── .kanban.json           # State (gitignored)
└── .git/hooks/
    └── post-commit                # Auto-sync (optional)
```

## Tips

- Use LLM to manage kanbans conversationally (see LLM_GUIDANCE.md in kanbanger)
- Commit `_kanban.md` files to track task planning
- Never commit `.env` or `.kanban.json` (secrets and state)
- GitHub Projects provides visual dashboard for team

## Troubleshooting

See kanbanger documentation:
- `README.md` - General usage
- `SPEC_INTEGRATION.md` - Detailed integration guide
- `TESTING.md` - Testing scenarios

## Support

- Kanbanger issues: https://github.com/earlyprototype/kanbanger
- Spec_Engine issues: https://github.com/earlyprototype/Spec_Engine
"""
    
    with open(readme_path, 'w') as f:
        f.write(content)
    
    print_success("KANBANGER_INTEGRATION.md created")


def main():
    """Main integration setup."""
    print_header("Spec_Engine + Kanbanger Integration Setup")
    
    print("This script will set up kanbanger in your Spec_Engine project.")
    print()
    
    # Step 1: Verify Spec_Engine project
    print_step("1/6", "Checking Project Structure")
    if not check_spec_engine_project():
        print_error("Setup aborted")
        sys.exit(1)
    
    # Step 2: Update .gitignore
    print_step("2/6", "Updating .gitignore")
    update_gitignore()
    
    # Step 3: Create .env template
    print_step("3/6", "Creating Configuration Template")
    create_env_template()
    
    # Step 4: Create helper scripts
    print_step("4/6", "Creating Helper Scripts")
    create_spec_to_kanban_script()
    create_sync_all_script()
    
    # Step 5: Create git hook
    print_step("5/6", "Setting Up Git Hook (Optional)")
    create_git_hook()
    
    # Step 6: Create documentation
    print_step("6/6", "Creating Documentation")
    create_readme_section()
    
    # Summary
    print_header("Setup Complete!")
    
    print("Next steps:")
    print()
    print("1. Configure GitHub connection:")
    print("   cp .env.example .env")
    print("   # Edit .env with your token and repo")
    print()
    print("2. Run setup wizard:")
    print("   kanban-sync-setup")
    print()
    print("3. Generate kanban from SPEC:")
    print("   python spec-to-kanban.py SPECs/your_project/spec_your_project.md")
    print()
    print("4. Sync to GitHub:")
    print("   kanban-sync SPECs/your_project/_kanban.md")
    print()
    print("Read KANBANGER_INTEGRATION.md for detailed usage.")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
