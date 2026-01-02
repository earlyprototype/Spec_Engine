# Migration Guide: v1.3 → v2.0

**Constitutional Slow-Code Engine v2.0**  
**Migration Date:** 2 January 2026  
**Backward Compatibility:** Maintained ✅

---

## Summary of Changes

### Major Additions (Non-Breaking)
1. **Article XV** - The Slow-Code Principle added to Constitution
2. **Notepad template** - Knowledge capture for all executions
3. **Education Mode** - Learning-focused execution with approval gates
4. **Troubleshooting Ecosystem** - Three specialized TOOLSPECs (WTF, Forensic, enhanced Troubleshoot)
5. **TOOLSPEC Library** - Documented workflow patterns with quick selection guide

### Template Enhancements
- `Spec_template.md` - Added "Knowledge Capture" section
- `parameters_template.toml` - Added `[knowledge_capture]` and `[education]` sections
- `exe_template.md` - Added Section 2.7 (Notepad Update) and Education Mode logic
- `notepad_template.md` - NEW template for knowledge capture

### No Breaking Changes
All v1.3 SPECs continue to work without modification.

---

## Do I Need to Migrate?

### NO Migration Required If:
- Your existing SPECs execute successfully
- You don't need troubleshooting TOOLSPECs
- You're satisfied without notepad/education features
- You prefer current workflow

**v1.3 SPECs remain fully functional in v2.0**

### Consider Migration If:
- You want knowledge capture (notepad.md) for your SPECs
- You want to use Education Mode for learning
- You create SPECs frequently and want TOOLSPEC shortcuts
- You need troubleshooting/archaeology capabilities

---

## What's Backward Compatible?

### ✅ Fully Compatible (No Changes Needed)

**Existing SPECs:**
- All v1.0 - v1.3 SPECs execute identically in v2.0
- Constitution Articles I-XIV unchanged
- Triple-file architecture unchanged
- Validation logic unchanged
- Execution modes (silent, collaborative, dynamic) work as before

**Templates:**
- Old SPECs generated from v1.x templates still work
- New optional sections in templates don't affect old SPECs

**DNA Profiles:**
- v1.x project_constitution.toml files remain valid
- New v2.0 features are additive, not replacements

### ⚠️ Optional Upgrades (Non-Breaking)

**Notepad Generation:**
- Old SPECs won't generate notepad.md automatically
- Can manually create notepad for old SPECs if desired
- New SPECs auto-generate notepad

**Education Mode:**
- Not available in old SPECs (requires [education] section)
- Old SPECs use original modes (silent, collaborative, dynamic)
- Can manually add [education] section to enable

---

## Migration Options

### Option 1: No Migration (Continue as v1.3)
**Who:** Users satisfied with current functionality  
**Action:** None required  
**Trade-off:** Miss out on notepad, education mode, troubleshooting TOOLSPECs

### Option 2: Hybrid Approach (Recommended)
**Who:** Most users  
**Action:** 
- Keep existing SPECs as-is (they still work)
- Use new TOOLSPECs (Troubleshoot, WTF, Forensic) for new needs
- Generate new SPECs with Commander (automatically includes v2.0 features)
**Trade-off:** Mixed v1.x and v2.0 SPECs (not a problem, both work)

### Option 3: Full Upgrade
**Who:** Users wanting v2.0 features in all SPECs  
**Action:**
- Manually add sections to existing SPECs (see below)
- Or regenerate SPECs using Commander
**Trade-off:** Time investment for marginal benefit

---

## Manual Upgrade Guide (Optional)

If you want to upgrade an existing v1.x SPEC to v2.0:

### Step 1: Add Knowledge Capture Section to spec.md

After the Goal section, add:

```markdown
## Knowledge Capture (Notepad)

**Purpose:** Capture insights, observations, and learnings during execution.

This notepad will be populated during execution with:
- Key insights and aha moments
- Technical discoveries and decisions
- Ideas for future enhancements
- Cross-system connections and patterns
- Observations from both AI executor and human user

**File:** `notepad_[descriptor].md` (automatically created during execution)

**Update Frequency:** Configured in parameters.toml (per_task by default)
```

### Step 2: Add Sections to parameters.toml

After `[error_propagation]`, add:

```toml
[knowledge_capture]
enabled = true
notepad_path = "notepad_[descriptor].md"
capture_types = ["insights", "technical_notes", "ideas", "connections", "observations"]
update_frequency = "per_task"
```

Optionally, update `[execution]` and add `[education]`:

```toml
[execution]
default_mode = "dynamic"  # Add "education" as option

[education]
enabled = false
approval_gates = "increased"
rationale_required = true
alternatives_shown = true
comparison_depth = "detailed"
learning_pace = "moderate"
```

### Step 3: Add Section 2.7 to exe.md

After Section 2.6 (Backup Method Selection), add:

```markdown
## 2.7 Notepad Update (Knowledge Capture)

After completing each task, update the knowledge capture notepad:

1. Reflect on execution outcomes
2. Identify key insights or discoveries
3. Note technical decisions and rationale
4. Capture ideas for improvement
5. Append to notepad_[descriptor].md with timestamp

See exe_template.md Section 2.7 for complete logic.
```

### Step 4: Test Upgraded SPEC

Execute the SPEC and verify:
- ✅ Validates successfully
- ✅ Generates notepad_[descriptor].md
- ✅ Notepad contains insights after execution
- ✅ No execution errors from new sections

---

## New Features You Get (v2.0)

### 1. Troubleshooting TOOLSPECs
- **Troubleshoot:** Fix broken development code systematically
- **WTF:** Understand mysterious/legacy code via archaeology
- **Forensic:** Investigate critical production incidents

**Usage:** Navigate to `_TOOLSPECs/[NAME]/` and launch the SPEC

### 2. Knowledge Capture
- Every execution generates `notepad_[descriptor].md`
- Captures insights, decisions, ideas, connections
- Human-readable complement to machine progress.json

**Usage:** Automatic when SPECs generated from v2.0 templates

### 3. Education Mode
- Learning-focused execution with approval gates
- Explains WHY decisions are made
- Shows alternatives with pros/cons
- Logs learning to notepad

**Usage:** Set `default_mode = "education"` in parameters.toml

### 4. TOOLSPEC Library
- Pre-built workflows for common patterns
- Quick selection guide and decision trees
- 5 available now, 13 more planned

**Usage:** See `_TOOLSPECs/README_WORKFLOW_LIBRARY.md`

### 5. Constitutional Article XV
- Understanding over speed when learning matters
- Troubleshooting ecosystem parity with creation workflows
- Mandatory knowledge capture for all executions
- Education mode requirements

**Impact:** Formalizes slow-code philosophy in governance

---

## FAQ

**Q: Will my v1.3 SPECs break in v2.0?**  
A: No. All v1.x SPECs are fully backward compatible.

**Q: Do I have to upgrade existing SPECs?**  
A: No. Upgrade is optional and provides marginal benefit for working SPECs.

**Q: Can I mix v1.x and v2.0 SPECs?**  
A: Yes. They coexist perfectly in the same workspace.

**Q: How do I know which version my SPEC is?**  
A: Check parameters.toml - if it has `[knowledge_capture]` section, it's v2.0.

**Q: What if I want v2.0 features in old SPEC?**  
A: Follow manual upgrade guide above, or regenerate with Commander.

**Q: Are TOOLSPECs different from regular SPECs?**  
A: No. TOOLSPECs are regular SPECs for common workflows. They use the same framework.

**Q: Do I need to update my DNA profiles?**  
A: No. Old DNA profiles work fine. New features are optional.

**Q: What about MCP server?**  
A: Planned for v2.1. Not required for v2.0 features to work.

---

## Rollback (If Needed)

If you experience issues with v2.0:

### Quick Rollback
1. Revert to v1.3 templates in `_templates/` directory
2. Existing SPECs will continue working
3. Report issues for investigation

### What You Lose
- Cannot use new TOOLSPECs (Troubleshoot, WTF, Forensic)
- No notepad generation for new SPECs
- No education mode
- Constitution reverts to Articles I-XIV only

### What You Keep
- All existing v1.x SPECs remain functional
- Commander, DNA, core templates still work
- Better_SPEC and Dev_Analysis TOOLSPECs unchanged

---

## Support

**Questions about migration:**
- Review this guide
- Check `GETTING_STARTED_v2.md` for new features
- Consult `_Constitution/constitution.md` Article XV

**Issues with upgraded SPECs:**
- Validate against constitution (all 15 Articles)
- Check bridging between spec.md and parameters.toml
- Review progress.json for validation errors

**Want to contribute:**
- Submit improved TOOLSPECs
- Share successful migration experiences
- Report bugs or edge cases

---

## Timeline

| Phase | Date | Status |
|-------|------|--------|
| v2.0 Core Release | 2026-01-02 | ✅ Complete |
| Community Testing | 2026-01-02 onwards | In Progress |
| MCP Server (v2.1) | Q1 2026 | Planned |
| Additional TOOLSPECs (v2.2-2.3) | Q2 2026 | Planned |

---

**Migration Philosophy:** Backward compatibility first. v2.0 enhances rather than replaces v1.x functionality.

**Recommendation:** Use hybrid approach - keep old SPECs, use new features for new work.

---

*Last Updated: 2 January 2026*  
*From: v1.3 → v2.0*  
*Breaking Changes: None ✅*
