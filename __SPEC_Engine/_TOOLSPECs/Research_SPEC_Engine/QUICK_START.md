# Research SPEC_Engine - Quick Start

**Get competitive intelligence in 45-90 minutes**

---

## What This SPEC Does

Automatically researches SPEC_Engine vs similar frameworks and produces:

**Output 1:** `@filing/SPEC_Engine_Research_Report.md` (comprehensive, 15-25 pages)  
**Output 2:** `@filing/SPEC_Engine_Research_Summary.md` (executive summary, 2-3 pages)

---

## How To Use

### 1. Check MCP Tools Installed

**Required:**
- tavily-search (web research)
- huggingface (paper search)

**Recommended:**
- github (repository analysis)

### 2. Execute the SPEC

```
Execute Research_SPEC_Engine SPEC using exe_template.md
```

Point the executor to:
- **Spec file:** `__SPEC_Engine/_TOOLSPECs/Research_SPEC_Engine/spec_Research_SPEC_Engine.md`
- **Parameters:** `__SPEC_Engine/_TOOLSPECs/Research_SPEC_Engine/parameters_Research_SPEC_Engine.toml`

### 3. Let It Run

The SPEC will:
- Read all SPEC_Engine docs (5 min)
- Discover 10-15 candidate frameworks (15-25 min)
- Deep analysis of top 3-5 (15-30 min)
- Create comparison matrices (10-20 min)
- Generate SWOT analysis (5-10 min)
- Write comprehensive report (10-15 min)

**Total time:** 45-90 minutes (mostly autonomous)

### 4. Review Results

Open `@filing/SPEC_Engine_Research_Report.md` to see:

- **Executive Summary:** Key findings and top recommendations
- **Framework Profiles:** Detailed analysis of each competitor
- **Comparison Matrices:** Side-by-side feature comparisons
- **SWOT Analysis:** Strengths, weaknesses, opportunities, threats
- **Recommendations:** Prioritised by impact and effort
- **References:** All sources cited

---

## What You'll Learn

### About SPEC_Engine

- What makes it unique (vs competitors)
- Where it's strongest
- Where it's weakest
- What it's missing

### About The Ecosystem

- What similar frameworks exist
- How they differ in approach
- What innovations others have made
- What trends are emerging

### Strategic Insights

- Quick wins (high impact, low effort)
- Strategic investments (high impact, high effort)
- Features to adopt
- Competitive threats to address

---

## Example Output Snippets

### Comparison Matrix Example

```markdown
| Feature | SPEC_Engine | Lia | GitHub Spec Kit |
|---------|-------------|-----|-----------------|
| File Structure | 3 files (MD+TOML+EXE) | 1 file (TOML) | Multiple MDs |
| Constitutional | 14 Articles | Implicit | 9 Articles |
| Execution Modes | 3 (S/D/C) | 2 (S/C) | Command-based |
| Validation | Pre+Runtime+Post | Template-based | Phase gates |
```

### SWOT Example

```markdown
## Strengths
1. **Triple-file architecture** - Only framework with MD+TOML separation
2. **Dynamic mode escalation** - Multi-signal intelligence unmatched
3. **Constitutional governance** - 14 articles most comprehensive

## Opportunities
1. **Adopt Lia's troubleshooting ecosystem** (HIGH priority)
2. **Add notepad knowledge capture** (HIGH priority)
3. **Build MCP server for external integration** (MEDIUM priority)
```

---

## When To Run

### Regular Schedule

- **Quarterly:** Quick update on new competitors
- **Biannually:** Full analysis with SWOT
- **Before v2.0/v3.0:** Always research before major versions

### Event-Driven

- New popular framework emerges
- Someone asks "how does this compare to X?"
- Planning significant new features
- Writing papers or presentations about SPEC_Engine

---

## Time Investment vs Value

### Time: 45-90 minutes (mostly autonomous)

You spend:
- 2 minutes: Launch SPEC
- 3 minutes: Confirm mode selection
- 40-85 minutes: SPEC runs autonomously
- 15 minutes: Review report

### Value: Strategic Intelligence

You get:
- Complete competitive landscape
- Evidence-based feature comparison
- Prioritised improvement roadmap
- Citation-backed analysis
- Reusable for future research

**ROI:** Hours of manual research compressed into 45-90 minutes of structured, reproducible analysis.

---

## Tips

### For Faster Results

1. **Reduce framework count:** Set `min_frameworks_compared = 2` in parameters
2. **Focus comparison:** Set `focus_area = "governance"` to narrow scope
3. **Skip optional steps:** Some steps are non-critical, will log and continue

### For Deeper Analysis

1. **Increase framework count:** Manually add frameworks to discovery if you know specific ones
2. **Add comparison dimensions:** Edit Task 3 to include more matrices
3. **Request academic focus:** Emphasize paper searches in Task 1

### For Specific Competitor Focus

Modify `parameters_Research_SPEC_Engine.toml`:
```toml
[constraints]
target_framework = "Lia Workflow Specs"  # Focus on this competitor
deep_dive = true  # More detailed analysis
```

---

## What Happens If...

### "Only 2 frameworks found"

Dynamic mode will escalate:
```
Research yielded 2 frameworks (minimum: 3)

OPTIONS:
[A] Continue with 2 frameworks (acceptable for initial analysis)
[B] Expand search criteria (add more search terms)
[C] Pause and provide specific frameworks to include
```

### "Documentation sparse for a framework"

Backup methods activate:
```
Step [2.0]: Extract architecture - Primary failed (docs incomplete)
→ Attempting Backup [1]: Analyse repository structure directly
→ ✓ Success: Architecture inferred from code organization
```

### "Comparison dimensions unclear"

Dynamic mode escalates:
```
Some comparison dimensions yielding ambiguous results.
Need human judgment on how to classify [Feature X]

Please clarify...
```

---

## Integration with Better_SPEC

**Research → Improvement Pipeline:**

1. **Run Research_SPEC_Engine:** Identify opportunities
2. **Create proposals:** Write proposal docs for high-priority opportunities
3. **Run Better_SPEC Mode B:** Process proposals one at a time
4. **Implement:** Better_SPEC executes approved improvements

**Example:**
```
Research SPEC finds: "Lia has notepad system - SPEC_Engine lacks this"
  ↓
Create proposal: @dev/_SPEC_dev_proposals/add_notepad_system.md
  ↓
Better_SPEC Mode B: Process proposal, get approval, implement
  ↓
SPEC_Engine now has notepad system
```

---

## Success Criteria

You'll know the research was successful if:

✓ Report saved to @filing/  
✓ At least 3 frameworks analysed  
✓ Minimum 8 comparison matrices complete  
✓ SWOT analysis with priorities  
✓ Recommendations specific and actionable  
✓ All claims cited

---

## Common Questions

**Q: Is this research biased toward SPEC_Engine?**  
A: No. Analysis is evidence-based. If competitors have superior features, the report will say so clearly.

**Q: Can I research frameworks outside workflow/spec domain?**  
A: Yes, modify Task 1 search terms to broaden or narrow scope.

**Q: How recent is the research?**  
A: Always current - web searches and GitHub data are live at execution time.

**Q: Can I export findings in other formats?**  
A: Output is Markdown - easily converted to PDF, HTML, presentations.

---

**Ready?** Execute the SPEC and get comprehensive competitive intelligence.

**Execution command:**
```
Execute __SPEC_Engine/_TOOLSPECs/Research_SPEC_Engine/ using exe_template.md
```

The SPEC handles everything else automatically.
