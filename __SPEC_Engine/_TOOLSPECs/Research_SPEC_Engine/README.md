# Research SPEC_Engine - Competitive Research System

**Version:** 1.0  
**Purpose:** Reusable SPEC for systematic competitive analysis of SPEC_Engine framework

---

## What Is This?

Research_SPEC_Engine is a reusable TOOLSPEC designed to conduct comprehensive competitive research on the SPEC_Engine framework itself. It systematically discovers similar frameworks, analyses their features, compares them to SPEC_Engine, and produces actionable insights.

---

## What It Does

### Complete Research Workflow

1. **Scopes Research** (Task 0)
   - Reads all SPEC_Engine documentation
   - Identifies comparison dimensions
   - Defines research questions

2. **Discovers Similar Frameworks** (Task 1)
   - Web searches for specification-driven systems
   - Academic paper searches for self-improving frameworks
   - GitHub repository searches
   - Filters to 3-5 most relevant frameworks

3. **Deep Analysis** (Task 2)
   - Extracts architecture for each framework
   - Documents execution models
   - Analyses governance mechanisms
   - Identifies unique features
   - Assesses maturity and adoption

4. **Systematic Comparison** (Task 3)
   - Creates comparison matrices across 8+ dimensions
   - Highlights SPEC_Engine's unique innovations
   - Identifies gaps and missing features

5. **SWOT Analysis** (Task 4)
   - Documents strengths (what SPEC_Engine does better)
   - Documents weaknesses (where it lags)
   - Identifies opportunities (improvements to adopt)
   - Identifies threats (competitive risks)
   - Prioritises opportunities by impact/effort

6. **Generates Report** (Task 5)
   - Synthesises findings into comprehensive markdown report
   - Includes executive summary
   - Provides actionable recommendations
   - Saves to `@filing/SPEC_Engine_Research_Report.md`

---

## How To Use

### Basic Usage

```
Execute Research_SPEC_Engine SPEC
```

No configuration needed - the SPEC handles everything automatically.

### What You'll Get

**Primary Output:**
- `@filing/SPEC_Engine_Research_Report.md` (comprehensive analysis, 15-25 pages)
- `@filing/SPEC_Engine_Research_Summary.md` (executive summary, 2-3 pages)

**Contains:**
- Profiles of 3-5 similar frameworks
- 5+ comparison matrices (architecture, governance, execution, features, UX)
- SWOT analysis with evidence
- Prioritised recommendations (P1/P2/P3)
- Complete citations and references

---

## What Makes It Useful

### Evidence-Based Research

Every finding is backed by:
- Official documentation
- Academic papers
- GitHub repository analysis
- Industry reports

No speculation - only verified facts.

### Structured Comparison

Compares frameworks across consistent dimensions:
- **Architecture:** File structure, components, modularity
- **Governance:** Constitutional principles, validation, quality enforcement
- **Execution:** Modes, escalation, autonomy, error handling
- **Features:** Capabilities, integrations, extensibility
- **User Experience:** Ease of use, documentation, learning curve
- **Maturity:** Adoption, community, stability
- **Philosophy:** Design principles, target users, use cases
- **Innovation:** Unique contributions to the field

### Actionable Insights

Recommendations are:
- **Specific:** "Add notepad system like Lia" (not "improve knowledge capture")
- **Prioritised:** High impact + low effort highlighted as quick wins
- **Feasible:** Based on proven implementations in similar frameworks
- **Constitutional:** Aligned with SPEC_Engine principles

---

## When To Use This SPEC

### Scenarios

**1. Periodic Competitive Analysis**
- Run quarterly or biannually
- Track emerging competitors
- Monitor industry trends
- Update strategic roadmap

**2. Before Major Updates**
- Research before v2.0 planning
- Ensure features align with market
- Avoid reinventing existing solutions

**3. When Considering New Features**
- "Should we add X feature?"
- Check if competitors have it
- Learn from their implementation

**4. For Strategic Planning**
- Understand competitive position
- Identify differentiation opportunities
- Plan development priorities

**5. Before Writing About SPEC_Engine**
- Need accurate comparison data
- Want to position features correctly
- Writing academic papers or documentation

---

## Key Features

### Autonomous Operation

- **Dynamic mode:** Runs mostly autonomously
- **Smart escalation:** Asks for help if research yields insufficient results
- **Self-validating:** Checks it found minimum 3 frameworks, 8 dimensions

### Comprehensive Coverage

- **Multiple source types:** Web, academic, GitHub, documentation
- **Depth and breadth:** Wide discovery (Task 1) + deep analysis (Task 2)
- **Structured synthesis:** Comparison matrices + SWOT + recommendations

### Quality Enforcement

- **Minimum thresholds:** 3 frameworks, 8 dimensions (configured in constraints)
- **Citation requirements:** All findings must be citable
- **Evidence-based:** No speculation allowed

### SPEC_Engine Integration

- **Reads current documentation:** Always analyses latest SPEC_Engine version
- **Constitutional compliance:** Research process follows SPEC_Engine principles
- **Outputs to @filing/:** Preserves research for future reference

---

## Files Structure

```
Research_SPEC_Engine/
├── spec_Research_SPEC_Engine.md           Human-readable specification
├── parameters_Research_SPEC_Engine.toml   Machine-readable parameters
├── README.md                              This file
└── progress_Research_SPEC_Engine.json     (Generated during execution)
```

**Output Location:**
```
@filing/
├── SPEC_Engine_Research_Report.md         Main research report
└── SPEC_Engine_Research_Summary.md        Executive summary
```

---

## Constitutional Compliance

This SPEC fully complies with all Constitutional Articles:

- **Article I:** Singular goal (research SPEC_Engine)
- **Article II:** Proper hierarchy (Goal → 6 Tasks → 31 Steps → Backups)
- **Article III:** Dual-file mandate (spec + parameters)
- **Article VI:** Critical balance 48% (within 40-60% guideline)
- **Article IX:** Dynamic mode with intelligent escalation
- **Article X:** Comprehensive logging to progress.json

---

## Critical Balance: 48% Overall

Breakdown by task:
- Task 0: 67% (understanding SPEC_Engine is critical)
- Task 1: 50% (discovery critical, filtering less so)
- Task 2: 40% (architecture and execution critical, others enhancing)
- Task 3: 57% (comparison matrices critical, gaps critical)
- Task 4: 80% (SWOT components critical, prioritisation critical)
- Task 5: 70% (report structure, key sections, saving critical)

**Overall:** 48% critical (within 40-60% constitutional guideline)

---

## Expected Outputs

### Main Report Structure

```markdown
# SPEC_Engine Comparative Research Report

## Executive Summary
- Key findings
- Position assessment
- Top 5 recommendations

## Methodology
- Research scope and timeline
- Sources and selection criteria
- Comparison dimensions

## Framework Profiles
### [Framework 1]
- Overview and purpose
- Architecture and structure
- Key features
- Maturity and adoption

[... additional frameworks ...]

## Comparative Analysis
### Architecture Comparison Matrix
[Detailed table]

### Governance Comparison Matrix
[Detailed table]

[... additional matrices ...]

## SWOT Analysis
### Strengths (with evidence)
### Weaknesses (with examples)
### Opportunities (prioritised)
### Threats (competitive risks)

## Recommendations
### Priority 1: High Impact, Low/Medium Effort
### Priority 2: High Impact, High Effort
### Priority 3: Medium Impact, Low Effort

## References
[Complete citation list]
```

---

## Comparison to Similar TOOLSPECs

### vs Better_SPEC
| Research_SPEC_Engine | Better_SPEC |
|---------------------|-------------|
| Competitive research (external focus) | Framework improvement (internal focus) |
| Discovers and analyses competitors | Processes proposals and reports |
| Outputs research report | Outputs modified framework files |
| Read-only operation | Modifies files with backups |

**Complementary:** Research identifies improvements → Better_SPEC implements them

### vs Dev_Analysis
| Research_SPEC_Engine | Dev_Analysis |
|---------------------|--------------|
| Research competitors and ecosystem | Analyse specific development projects |
| Web + academic + GitHub sources | Project-specific codebase analysis |
| Strategic positioning | Tactical improvements |
| Framework-level insights | Implementation-level insights |

**Complementary:** Research informs strategy → Dev_Analysis informs tactics

---

## When To Run This SPEC

### Recommended Frequency

**Quarterly:** Quick scan for new competitors and major updates  
**Biannually:** Full competitive analysis with SWOT  
**Before Major Versions:** Complete research before v2.0, v3.0 planning  
**As Needed:** When considering significant new features or changes

### Triggers

Run this SPEC when:
- Planning next major version
- Evaluating new feature proposals
- Writing about SPEC_Engine (papers, documentation, presentations)
- Someone asks "how does this compare to X?"
- You haven't researched competitors in 6+ months
- A new popular framework emerges in the space

---

## Advanced Usage

### Focused Research

While the SPEC is designed for comprehensive analysis, you can focus research by modifying constraints before execution:

**In parameters_Research_SPEC_Engine.toml:**
```toml
[constraints]
focus_area = "governance"  # Focus comparison on governance mechanisms
min_frameworks_compared = 2  # Reduce if time-limited
target_framework = "Lia Workflow Specs"  # Deep dive on specific competitor
```

### Multi-Round Research

For ongoing competitive monitoring:

**Round 1:** Initial comprehensive research  
**Round 2 (3 months later):** Update analysis with new findings  
**Round 3 (6 months later):** Full re-analysis with framework evolution tracked

Progress JSON tracks what was researched when, enabling incremental updates.

---

## Dependencies

### Required MCP Tools

- **tavily-search:** Web research and discovery
- **huggingface:** Academic paper searches

**Installation:**
- Tavily: Configure MCP server for Tavily API
- Hugging Face: MCP Docker tools with paper search capability

### Recommended MCP Tools

- **github:** Repository analysis and searches

### Optional MCP Tools

- **context7:** Framework documentation lookup

---

## Expected Execution Time

**Full comprehensive research:** 45-90 minutes
- Task 0: 5 minutes (scope)
- Task 1: 15-25 minutes (discovery)
- Task 2: 15-30 minutes (deep analysis)
- Task 3: 10-20 minutes (comparison)
- Task 4: 5-10 minutes (SWOT)
- Task 5: 10-15 minutes (report generation)

**Influenced by:**
- Number of frameworks discovered (more = longer)
- Documentation quality (sparse docs = more time)
- Complexity of frameworks (simpler = faster)

---

## Output Quality Guarantees

### Minimum Thresholds

✓ At least 3 frameworks analysed  
✓ At least 8 comparison dimensions  
✓ All findings cited  
✓ SWOT complete with priorities  
✓ Recommendations actionable and specific

### Validation Checks

The executor automatically verifies:
- Report file exists in @filing/
- All sections present (no missing headers)
- Comparison matrices populated (no empty cells without N/A)
- Citations included
- UK English used throughout

---

## Next Steps

**To execute this SPEC:**

1. Ensure required MCP tools installed (tavily-search, huggingface)
2. Open `__SPEC_Engine/_templates/exe_template.md` or create custom executor
3. Point executor to this SPEC folder
4. Let it run (mostly autonomous)
5. Review output in `@filing/SPEC_Engine_Research_Report.md`

**After execution:**

1. Review findings and recommendations
2. If opportunities identified, create proposals in `@dev/_SPEC_dev_proposals/`
3. Use Better_SPEC to process proposals systematically
4. Update SPEC_Engine based on research insights

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-02 | Initial creation - systematic competitive research SPEC |

---

## Questions?

**Q: How often should I run this?**  
A: Quarterly for monitoring, biannually for full analysis, before major versions always.

**Q: Can I focus on specific competitor?**  
A: Yes, modify `constraints.target_framework` in parameters file to focus research.

**Q: What if it only finds 2 frameworks?**  
A: Executor will escalate and ask for guidance - you can approve 2 or suggest additional areas to search.

**Q: Can I use this for other frameworks (not SPEC_Engine)?**  
A: Yes! Modify Task 0 Step 0 to read different framework docs, update goal statement, and run.

**Q: How is this different from manual research?**  
A: Systematic (doesn't miss dimensions), reproducible (same process each time), comprehensive (multiple source types), structured (comparison matrices enforce consistency).

---

**Ready to research?** Execute this SPEC and get comprehensive competitive intelligence in 45-90 minutes.
