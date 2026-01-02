# Research SPEC_Engine

**Version:** 1.0  
**Last Updated:** 2 January 2026  
**Purpose:** Systematically research SPEC_Engine framework and compare it to similar projects, identifying strengths, weaknesses, and opportunities

---

## Goal

Conduct comprehensive research on SPEC_Engine, compare it to similar workflow/specification frameworks, and produce a detailed analysis report highlighting strengths, weaknesses, and opportunities for improvement.

---

## Software Stack & Architecture

**Not Applicable** - This is a research and analysis task, not a build goal.

---

## Definition of Complete

What must exist and be verified:
- [ ] **Primary deliverable:** Comprehensive research report (SPEC_Engine_Research_Report.md) saved to `@filing/`
- [ ] **Quality standards met:** 
  - At least 3 similar frameworks analysed
  - Each framework compared across minimum 8 dimensions
  - Strengths, weaknesses, and opportunities clearly documented
  - Research backed by official documentation, academic papers, or industry sources
- [ ] **Verification method:** Report contains complete comparison matrices, SWOT analysis, and actionable recommendations

---

## MCP Toolset

### Installed Tools (Verified During SPEC Creation)

**REQUIRED Tools:**
- **tavily-search** (Web search for finding similar frameworks and current information)
  - Rationale: Essential for discovering similar projects, gathering current data, and finding academic research
  - Install: MCP server for Tavily search functionality

- **huggingface** (Access to research papers and ML community projects)
  - Rationale: Many similar frameworks are discussed in ML/AI research papers
  - Install: MCP Docker tools for Hugging Face paper search

**RECOMMENDED Tools:**
- **github** (Repository analysis for similar open-source projects)
  - Rationale: Most similar frameworks are open-source with GitHub repositories
  - Alternative: Manual repository inspection via browser
  - Install: `npm install @modelcontextprotocol/server-github`

**OPTIONAL Tools:**
- **context7** (Documentation lookup for frameworks)
  - Use case: Quick access to framework documentation
  - Install: MCP context7 server if available

---

## Definitions

- **goal**: Research SPEC_Engine and produce comparative analysis report
- **task[n]**: Discrete research objectives (discover, analyse, synthesise)
- **step[m]**: Concrete research actions within each task
- **backup[p]**: Alternative research approaches when primary method blocked
- **critical_flag**: Boolean indicating whether step failure blocks goal achievement
- **mode**: Dynamic (autonomous with intelligent escalation when needed)
- **progress.json**: Structured log tracking research activities and findings

---

## Components

Research requires access to:
- **SPEC_Engine documentation:** README, GETTING_STARTED, Constitution, templates, workflow diagrams
- **External frameworks:** Lia Workflow Specs, GitHub Spec Kit, similar systems
- **Research sources:** Web searches, academic papers, GitHub repositories, official documentation
- **Output location:** `@filing/` for report storage

**Deliverables Generated:**
- **Research report:** Comprehensive markdown document with analysis
- **Comparison matrices:** Structured tables comparing frameworks
- **SWOT analysis:** Strengths, Weaknesses, Opportunities, Threats
- **progress_Research_SPEC_Engine.json:** Complete research activity log

**Machine-Readable Components:**  
See `[components]` section in parameters_Research_SPEC_Engine.toml

---

## Constraints

- Research must be evidence-based (cite sources)
- Minimum 3 similar frameworks for meaningful comparison
- Analysis must cover at least 8 comparison dimensions
- Recommendations must be actionable and specific
- Report must maintain UK English throughout
- Original research documents must be preserved (not deleted)

**Machine-Readable Constraints:**  
See `[constraints]` section in parameters_Research_SPEC_Engine.toml:
- `min_frameworks_compared = 3`
- `min_comparison_dimensions = 8`
- `citations_required = true`
- `use_uk_english = true`

---

## User Stories

- As a **SPEC_Engine developer**, I want to understand competitive landscape so I can prioritise improvements
- As a **framework user**, I want to know SPEC_Engine's strengths so I can leverage them effectively
- As a **researcher**, I want evidence-based comparisons so decisions are data-driven
- As a **contributor**, I want to identify weaknesses so I know where to focus enhancements

---

## Task [0]: Prepare Research Scope

**TOML Reference:** `tasks[id=0]` in parameters_Research_SPEC_Engine.toml  
**Purpose:** Define clear research boundaries and success criteria

- **Step [0]:** Read SPEC_Engine core documentation
  - **Primary method:** Read README.md, GETTING_STARTED.md, constitution.md, DESIGN_PHILOSOPHY.md
  - **Expected output:** Complete understanding of SPEC_Engine features, architecture, and principles
  - **Critical:** true
  - **Mode:** silent

- **Step [1]:** Identify comparison dimensions
  - **Primary method:** Extract key features from documentation (3-file architecture, constitutional governance, modes, etc.)
  - **Backup [1]:** If features unclear, analyse template structures directly
  - **Expected output:** List of 8+ comparison dimensions (architecture, governance, execution, etc.)
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Define research questions
  - **Primary method:** Formulate specific questions: "What similar systems exist?", "How does SPEC_Engine differ?", "What are unique innovations?"
  - **Expected output:** Structured list of research questions guiding investigation
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Core documentation understood, comparison dimensions defined, research questions clear
- **Logging:** Record scope in progress_Research_SPEC_Engine.json

---

## Task [1]: Discover Similar Frameworks

**TOML Reference:** `tasks[id=1]` in parameters_Research_SPEC_Engine.toml  
**Purpose:** Find frameworks with comparable goals and approaches  
**Research Enabled:** true  
**Research Sources:** web_search, github_repos, academic

- **Step [1]:** Web search for specification-driven frameworks
  - **Primary method:** Search: "specification-driven development frameworks", "LLM workflow systems", "goal-driven AI frameworks", "constitutional AI frameworks"
  - **Backup [1]:** If results too broad, narrow to "structured LLM task frameworks" or "AI workflow engines"
  - **Expected output:** List of 10-15 candidate frameworks with URLs
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Search academic papers for self-improving systems
  - **Primary method:** Search Hugging Face papers: "self-improving AI frameworks", "meta-programming systems", "autonomous agent frameworks"
  - **Backup [1]:** Search arXiv if Hugging Face insufficient
  - **Expected output:** List of relevant academic papers and systems
  - **Critical:** false
  - **Mode:** silent

- **Step [3]:** Identify GitHub repositories of similar systems
  - **Primary method:** Search GitHub for "specification framework", "workflow engine LLM", "structured prompts"
  - **Expected output:** List of open-source repositories with star counts
  - **Critical:** false
  - **Mode:** silent

- **Step [4]:** Filter to most relevant frameworks
  - **Primary method:** Select frameworks that share core characteristics: structured specifications, LLM execution, workflow management
  - **Backup [1]:** If too many candidates, prioritise by popularity (stars, papers citing) and feature overlap
  - **Expected output:** Shortlist of 3-5 frameworks for deep analysis
  - **Critical:** true
  - **Mode:** silent

- **Verification:** At least 3 suitable frameworks identified with accessible documentation
- **Logging:** Record discovered frameworks in progress_Research_SPEC_Engine.json

---

## Task [2]: Deep Analysis of Similar Frameworks

**TOML Reference:** `tasks[id=2]` in parameters_Research_SPEC_Engine.toml  
**Purpose:** Understand each framework's architecture, philosophy, and capabilities  
**Research Enabled:** true  
**Research Sources:** documentation, github_repos, technical_specs

- **Step [1]:** Extract core architecture for each framework
  - **Primary method:** Read official documentation, README files, architecture docs
  - **Backup [1]:** If documentation sparse, analyse repository structure and code
  - **Expected output:** Architecture summary for each framework (file structure, components, data flow)
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify execution models
  - **Primary method:** Document how each framework executes workflows (modes, escalation, autonomy levels)
  - **Expected output:** Execution model comparison showing autonomous vs supervised approaches
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Analyse governance and quality mechanisms
  - **Primary method:** Extract constitutional principles, validation rules, quality checks
  - **Backup [1]:** If principles not explicit, infer from template structures and examples
  - **Expected output:** Governance comparison showing how each enforces quality
  - **Critical:** false
  - **Mode:** silent

- **Step [4]:** Document unique features and innovations
  - **Primary method:** Identify features that distinguish each framework
  - **Expected output:** List of unique features per framework
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Assess maturity and adoption
  - **Primary method:** Check GitHub stars, commit frequency, issues, community activity, academic citations
  - **Backup [1]:** If metrics unavailable, assess documentation quality as proxy for maturity
  - **Expected output:** Maturity assessment for each framework
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Complete analysis for each framework covering architecture, execution, governance, features, maturity
- **Logging:** Record detailed framework profiles in progress_Research_SPEC_Engine.json

---

## Task [3]: Comparative Analysis

**TOML Reference:** `tasks[id=3]` in parameters_Research_SPEC_Engine.toml  
**Purpose:** Systematically compare SPEC_Engine to similar frameworks across all dimensions

- **Step [1]:** Create comparison matrix (architecture)
  - **Primary method:** Build table comparing: file structure, components, modularity, template systems
  - **Expected output:** Architecture comparison matrix
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Create comparison matrix (governance)
  - **Primary method:** Compare constitutional principles, validation mechanisms, quality enforcement
  - **Expected output:** Governance comparison matrix
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Create comparison matrix (execution & modes)
  - **Primary method:** Compare execution modes, escalation strategies, autonomy levels, error handling
  - **Expected output:** Execution comparison matrix
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Create comparison matrix (user experience)
  - **Primary method:** Compare ease of use, documentation quality, learning curve, tooling
  - **Expected output:** UX comparison matrix
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Create comparison matrix (features & capabilities)
  - **Primary method:** Compare feature sets, extensibility, integrations, supported workflows
  - **Expected output:** Features comparison matrix
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Identify unique SPEC_Engine innovations
  - **Primary method:** Highlight features present in SPEC_Engine but absent or weaker in alternatives
  - **Expected output:** List of SPEC_Engine's unique value propositions
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Identify features SPEC_Engine lacks
  - **Primary method:** Highlight valuable features in alternatives that SPEC_Engine could adopt
  - **Expected output:** Gap analysis showing missing capabilities
  - **Critical:** true
  - **Mode:** silent

- **Verification:** All comparison matrices complete, unique features identified, gaps documented
- **Logging:** Record comparison data in progress_Research_SPEC_Engine.json

---

## Task [4]: SWOT Analysis

**TOML Reference:** `tasks[id=4]` in parameters_Research_SPEC_Engine.toml  
**Purpose:** Synthesise findings into strengths, weaknesses, opportunities, and threats

- **Step [1]:** Identify SPEC_Engine strengths
  - **Primary method:** Based on comparison matrices, list what SPEC_Engine does better than alternatives
  - **Expected output:** Strengths list with evidence from comparisons
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify SPEC_Engine weaknesses
  - **Primary method:** Based on gap analysis, list areas where SPEC_Engine lags behind alternatives
  - **Expected output:** Weaknesses list with specific examples from competing frameworks
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Identify opportunities
  - **Primary method:** Cross-reference weaknesses with features from alternatives, emerging trends, user needs
  - **Backup [1]:** If opportunities unclear, review academic papers for cutting-edge concepts
  - **Expected output:** Opportunities list with potential improvements and innovations to adopt
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Identify threats
  - **Primary method:** Analyse competitive advantages of alternatives, trends that could make SPEC_Engine obsolete
  - **Expected output:** Threats list showing competitive risks
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Prioritise opportunities
  - **Primary method:** Rank opportunities by impact (high/medium/low) and effort (high/medium/low)
  - **Expected output:** Prioritised opportunity matrix showing quick wins and strategic investments
  - **Critical:** true
  - **Mode:** silent

- **Verification:** SWOT analysis complete with priorities, all findings evidence-based
- **Logging:** Record SWOT analysis in progress_Research_SPEC_Engine.json

---

## Task [5]: Generate Research Report

**TOML Reference:** `tasks[id=5]` in parameters_Research_SPEC_Engine.toml  
**Purpose:** Synthesise all findings into comprehensive, actionable research report

- **Step [1]:** Structure report outline
  - **Primary method:** Create hierarchical outline: Executive Summary, Methodology, Framework Profiles, Comparative Analysis, SWOT, Recommendations
  - **Expected output:** Report structure with section headings
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Write executive summary
  - **Primary method:** Summarise key findings, SPEC_Engine position, top 3-5 recommendations
  - **Expected output:** 1-2 page executive summary
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Document methodology
  - **Primary method:** Describe research process, sources used, selection criteria, comparison dimensions
  - **Expected output:** Methodology section explaining how research was conducted
  - **Critical:** false
  - **Mode:** silent

- **Step [4]:** Write framework profiles
  - **Primary method:** For each framework, provide overview, architecture, key features, maturity
  - **Expected output:** Detailed profiles section (2-3 pages per framework)
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Integrate comparison matrices
  - **Primary method:** Embed all comparison tables from Task 3 with analysis narratives
  - **Expected output:** Comparative analysis section with tables and commentary
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Write SWOT analysis section
  - **Primary method:** Present strengths, weaknesses, opportunities, threats with evidence
  - **Expected output:** SWOT section with prioritised opportunities
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Write recommendations
  - **Primary method:** Based on opportunities, provide specific, actionable recommendations with rationale
  - **Backup [1]:** If recommendations unclear, focus on highest-impact opportunities from priority matrix
  - **Expected output:** Recommendations section (3-5 priority 1 items, 5-8 priority 2/3 items)
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Add citations and references
  - **Primary method:** List all sources used (URLs, papers, repositories) with proper formatting
  - **Expected output:** References section with complete citation information
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Save report to @filing/
  - **Primary method:** Write complete report to `@filing/SPEC_Engine_Research_Report.md`
  - **Backup [1]:** If @filing/ inaccessible, save to workspace root and log location
  - **Expected output:** Report file created in @filing/ directory
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Create executive summary as separate file
  - **Primary method:** Extract executive summary to `@filing/SPEC_Engine_Research_Summary.md`
  - **Expected output:** Standalone summary file for quick reference
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Report complete, all sections present, citations included, files saved to @filing/
- **Logging:** Record report generation in progress_Research_SPEC_Engine.json

---

## Bridging: Markdown ↔ TOML Synchronisation

This spec file (spec_Research_SPEC_Engine.md) must maintain perfect alignment with its companion file (parameters_Research_SPEC_Engine.toml).

**Bridging Requirements:**
1. Each task in this file must have corresponding `[[tasks]]` entry in TOML with matching ID (0-5)
2. Each step within a task must have corresponding `[[tasks.steps]]` entry with matching ID
3. Expected outputs in this file must match `expected_output` fields in TOML
4. Critical flags must be synchronised between files
5. Constraints referenced must exist in TOML `[constraints]` section

**Example Cross-References:**
- "See `constraints.min_frameworks_compared` in parameters_Research_SPEC_Engine.toml" (Task 1)
- "As defined in `tasks[id=3]` in TOML" (Comparative Analysis)
- "Must satisfy TOML verification requirements" (All task verifications)

The exe controller validates this synchronisation during initialisation (Section 1.8).

---

## Instructions for LLM Executor

### Execution Mode: DYNAMIC

This SPEC uses **Dynamic mode** throughout:
- Silent execution where possible (most research steps)
- Collaborative escalation if research yields insufficient results
- Intelligent mode switching based on findings quality

### Key Operational Principles

1. **Evidence-based research**: Every finding must be citable
2. **Minimum thresholds**: At least 3 frameworks, 8 comparison dimensions
3. **UK English**: All documentation in British English (analyse, prioritise, etc.)
4. **Preserve sources**: Don't delete or lose original documentation
5. **Structured output**: Use comparison matrices, tables, clear sections
6. **Actionable recommendations**: Specific, prioritised, with rationale

### Research Guidelines

1. **Start broad, narrow systematically**: Cast wide net (Task 1), then deep dive (Task 2)
2. **Use multiple source types**: Web, academic, GitHub, documentation
3. **Verify claims**: If a framework claims a feature, verify in documentation or code
4. **Compare apples-to-apples**: Ensure comparison dimensions are meaningful across all frameworks
5. **Prioritise by evidence**: Strong sources (official docs, papers) > weak sources (blog posts, reddit)
6. **Track all sources**: Maintain citation list throughout research

### Escalation Triggers

Escalate to collaborative mode when:
- Fewer than 3 suitable frameworks found (need human guidance on alternatives)
- Documentation for framework is sparse or unclear (need human interpretation)
- Comparison dimensions yield ambiguous results (need human judgment)
- Multiple opportunities have equal priority (need human preference)

### Quality Checks

Before marking tasks complete:
- Task 1: Verify at least 3 frameworks with accessible documentation
- Task 2: Confirm complete profiles for all frameworks (no gaps)
- Task 3: Ensure all comparison matrices populated (no empty cells without "N/A" justification)
- Task 4: Check SWOT has concrete examples, not abstract statements
- Task 5: Validate report structure complete, citations present, saved to correct location

---

## Expected Output Structure

### SPEC_Engine_Research_Report.md (Main Deliverable)

```markdown
# SPEC_Engine Comparative Research Report

**Date:** [Execution date]
**Version:** 1.0
**Purpose:** Comprehensive analysis of SPEC_Engine vs similar frameworks

---

## Executive Summary

[1-2 pages: Key findings, position assessment, top recommendations]

---

## Methodology

### Research Scope
- Frameworks analysed: [List]
- Comparison dimensions: [List]
- Time period: [Date range]

### Sources
- Academic papers: [Count]
- GitHub repositories: [Count]
- Official documentation: [Count]

---

## Framework Profiles

### Framework 1: [Name]
[Architecture, features, maturity, unique value]

### Framework 2: [Name]
[Architecture, features, maturity, unique value]

[... additional frameworks ...]

---

## Comparative Analysis

### Architecture Comparison
[Matrix comparing file structures, components, modularity]

### Governance Comparison
[Matrix comparing validation, quality enforcement, principles]

### Execution Comparison
[Matrix comparing modes, escalation, autonomy, error handling]

[... additional comparison matrices ...]

---

## SWOT Analysis

### Strengths
[What SPEC_Engine does better, with evidence]

### Weaknesses
[Where SPEC_Engine lags, with examples]

### Opportunities
[Potential improvements ranked by priority]

### Threats
[Competitive risks and trends]

---

## Recommendations

### Priority 1 (High Impact, Low/Medium Effort)
1. [Recommendation with rationale]
2. [Recommendation with rationale]

### Priority 2 (High Impact, High Effort)
[List]

### Priority 3 (Medium Impact, Low Effort)
[List]

---

## References

[Complete citation list]

---

**END OF REPORT**
```

---

**End of spec_Research_SPEC_Engine.md**

This SPEC is designed to be reusable for periodic competitive analysis, updated as new frameworks emerge and SPEC_Engine evolves.
