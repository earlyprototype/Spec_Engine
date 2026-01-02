# Create reusable SPEC for development analysis
_Exported on 11/3/2025 at 02:48:17 GMT from Cursor (2.0.40)_

---

**User**

@__SPEC_Engine create a reusable SPEC called 'Dev_Analysis_SPEC.md'  guided by the development docs in this folder, which will be used to analyse the development of a test SPEC. Include all vital metrics and ensure you track these elements too: @goal_text_propogation.md Create the new SPEC file here: C:\Users\Fab2\Desktop\AI\Specs\SPECs\Testing\_Fixed_SPECs

---

**Cursor**

I'll help you create a reusable Dev_Analysis_SPEC for analysing SPEC development. Let me first explore the development documentation in the __SPEC_Engine folder to understand the framework properly, then propose the structure before creating it.

Perfect! I've reviewed the SPEC Engine framework. Now I'll propose a structure for the Dev_Analysis_SPEC before creating it.

## Proposed Structure for Dev_Analysis_SPEC.md

This SPEC will be designed to analyse how a test SPEC was developed, tracking both traditional SPEC metrics AND the goal text propagation elements you've identified.

### Key Analysis Areas:

**1. Goal Text Analysis**
- Initial goal text characteristics (length, complexity, technical level, formatting)
- Language propagation throughout project files
- Correlation between goal phrasing and agent behaviour

**2. SPEC Construction Metrics**
- Constitutional compliance (Articles I-XIV)
- Task/step decomposition quality
- Critical flag balance
- Backup method effectiveness

**3. Execution Performance**
- Step success/failure rates
- Backup usage patterns
- Mode escalation frequency
- Error propagation effectiveness

**4. Behaviour Correlation**
- How goal language influenced task breakdown
- Impact of goal clarity on execution accuracy
- Relationship between goal complexity and error rates
- Agent thinking patterns vs output quality

**5. Cross-Project Comparison** (when applicable)
- Comparative metrics across different goal formulations
- Pattern identification

Would you like me to proceed with creating this SPEC file using this structure? I'll make it:
- Comprehensive with all vital SPEC metrics
- Specifically focused on goal text propagation analysis
- Structured for clear, manageable analysis steps
- Compliant with the SPEC Engine constitution

Shall I create it?

---

**User**

yes

---

**Cursor**

Excellent! I'll create the comprehensive Dev_Analysis_SPEC now.

```markdown
# Dev Analysis SPEC

**Version:** 1.0  
**Last Updated:** 2025-11-03  
**Purpose:** Analyse development of test SPECs to identify patterns, metrics, and goal text propagation effects

---

## Goal

Perform comprehensive analysis of a test SPEC's development lifecycle to identify how initial goal text propagates through the system and impacts agent behaviour, execution accuracy, and project outcomes.

---

## Software Stack & Architecture

**Not Applicable** - This is an analysis task, not a build goal.

---

## Definition of Complete

What must exist and be verified:
- [ ] **Primary deliverable:** Comprehensive analysis report (markdown format) covering all analysis areas
- [ ] **Quality standards met:** 
  - All 8 analysis tasks completed with documented findings
  - Goal text propagation patterns identified with specific examples
  - Quantitative metrics calculated for execution performance
  - Cross-correlation analysis between goal characteristics and outcomes
  - Recommendations provided based on findings
- [ ] **Verification method:** 
  - Report contains all required sections (see tasks below)
  - Quantitative metrics include numerical values with source citations
  - At least 3 specific examples of goal text propagation documented
  - Recommendations are actionable and linked to specific findings

---

## Definitions

- **goal**: Analyse how initial goal text characteristics influence SPEC development and execution
- **task[n]**: Discrete analysis objectives examining different aspects of SPEC development
- **step[m]**: Concrete analytical actions within each task
- **backup[p]**: Alternative analysis methods when primary approach is blocked
- **critical_flag**: Boolean indicating whether analysis step is essential to overall goal
- **mode**: Execution mode per step: `silent` (autonomous) or `collaborative` (human-in-loop)
- **progress.json**: Structured log tracking analysis execution and findings

---

## Components

Analysis requires access to:
- **Test SPEC files:** spec_[descriptor].md, parameters_[descriptor].toml, exe_[descriptor].md
- **Execution logs:** progress_[descriptor].json
- **Project artefacts:** Code files, documentation, error logs, validation reports
- **Chat history:** Conversation transcripts showing agent thinking and decision-making
- **Constitution:** __SPEC_Engine/_Constitution/constitution.md for compliance checking

**Machine-Readable Components:**  
See `[components]` section in parameters_Dev_Analysis.toml

---

## Constraints

- Analysis must be objective and evidence-based
- All metrics must be traceable to source data
- Goal text propagation analysis must include minimum 3 concrete examples
- Quantitative metrics must include: success rates, error rates, mode escalations, backup usage
- Findings must distinguish correlation from causation
- Recommendations must be specific and actionable

**Machine-Readable Constraints:**  
See `[constraints]` section in parameters_Dev_Analysis.toml:
- `min_examples_required = 3` (goal text propagation examples)
- `metrics_evidence_based = true` (all metrics must cite sources)
- `recommendation_specificity = "actionable"` (recommendations must be implementable)

---

## User Stories

- As a **SPEC developer**, I want to understand how goal phrasing impacts development so I can write more effective goals
- As a **system architect**, I want to identify patterns in SPEC execution so I can improve the framework
- As a **researcher**, I want to quantify goal text propagation so I can understand agent behaviour correlation
- As a **project manager**, I want metrics on SPEC performance so I can assess project quality

---

## Analysis Framework

This SPEC analyses development across 8 integrated dimensions:

### Dimension 1: Goal Text Characteristics
- Length (word count, character count, sentence complexity)
- Number of distinct elements/requirements
- Literacy level (Flesch-Kincaid, technical density)
- Formatting (structure, lists, emphasis)
- Familiarity/Technical specificity

### Dimension 2: Goal Text Propagation
- How goal language appears in task descriptions
- Goal terminology in step definitions
- Phrasing patterns in agent thinking/reasoning
- Language consistency across SPEC artefacts
- Conceptual drift from goal to implementation

### Dimension 3: Constitutional Compliance
- Article I-XIV adherence scoring
- Critical flag balance (target: 40-60%)
- Backup method quality assessment
- Bridging quality (Markdown-TOML sync)
- Validation checkpoint outcomes

### Dimension 4: Execution Performance
- Step success/failure rates
- Backup invocation frequency
- Mode escalation patterns
- Error propagation effectiveness
- Retry patterns and exhaustion

### Dimension 5: Agent Behaviour Correlation
- Thinking patterns vs goal complexity
- Decision quality vs goal clarity
- Output quality vs goal specificity
- Backup selection vs goal ambiguity
- Escalation triggers vs goal characteristics

### Dimension 6: Per-Task/Step Behaviour
- Task decomposition quality
- Step atomicity assessment
- Critical flag appropriateness
- Expected output clarity
- Method selection rationale

### Dimension 7: Error Analysis
- Error types and frequencies
- Root cause patterns
- Recovery effectiveness
- Constitutional violations
- Preventable vs inherent errors

### Dimension 8: Outcome Metrics
- Goal achievement status (ACHIEVED/PARTIAL/NOT_ACHIEVED)
- Deliverable completeness
- Quality standards met
- Time/step efficiency
- Comparison to expected outcomes

---

## Task [1]: Extract and Characterise Initial Goal Text

**TOML Reference:** `tasks[id=1]` in parameters_Dev_Analysis.toml  
**Purpose:** Establish baseline characteristics of the goal that initiated SPEC development

- **Step [1]:** Locate and extract initial goal text
  - **Primary method:** Read SPEC markdown file Goal section and chat history for original user goal statement
  - **Backup [1]:** If chat history unavailable, use goal section from spec_[descriptor].md as proxy
  - **Expected output:** Exact goal text with source citation and timestamp
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Calculate quantitative text characteristics
  - **Primary method:** Compute word count, character count, sentence count, avg sentence length, Flesch-Kincaid score
  - **Backup [1]:** If automated scoring unavailable, perform manual classification (simple/moderate/complex)
  - **Expected output:** Table with numerical metrics and complexity classification
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Identify distinct elements and requirements
  - **Primary method:** Parse goal for discrete requirements, constraints, deliverables, success criteria
  - **Backup [1]:** Use linguistic chunking to identify conceptual units if structure unclear
  - **Expected output:** Numbered list of distinct elements (target: 3-10 elements)
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess technical specificity and domain familiarity
  - **Primary method:** Identify technical terms, domain-specific language, assumed knowledge, explicit vs implicit requirements
  - **Backup [1]:** Compare vocabulary against common vs specialised term databases
  - **Expected output:** Technical specificity score (1-5 scale) with justification and term examples
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Analyse formatting and structure
  - **Primary method:** Document use of lists, emphasis, sections, explicit vs narrative format
  - **Expected output:** Formatting assessment noting structural elements present
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All goal characteristics documented with quantitative metrics where possible
- **Logging:** Record all measurements in progress_Dev_Analysis.json for correlation analysis

---

## Task [2]: Map Goal Text Propagation Throughout Project

**TOML Reference:** `tasks[id=2]` in parameters_Dev_Analysis.toml  
**Purpose:** Track how initial goal language and concepts propagate through SPEC artefacts

- **Step [1]:** Extract task descriptions from SPEC
  - **Primary method:** Parse spec_[descriptor].md for all task titles and descriptions
  - **Expected output:** List of tasks with full text
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify goal language in task descriptions
  - **Primary method:** Compare task descriptions to goal text, noting shared terminology, conceptual overlap, verbatim phrases
  - **Backup [1]:** Use semantic similarity scoring if direct comparison insufficient
  - **Expected output:** Table mapping goal terms to task descriptions with similarity scores
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Extract step definitions and analyse propagation
  - **Primary method:** Parse all step descriptions, identify goal/task terminology presence, track conceptual consistency
  - **Backup [1]:** Focus on critical steps only if volume is high (>20 steps)
  - **Expected output:** Propagation matrix showing goal→task→step language flow with specific examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse agent thinking and reasoning patterns
  - **Primary method:** Review chat history/logs for agent internal reasoning, note how goal concepts appear in thinking
  - **Backup [1]:** If full chat unavailable, analyse progress.json logs for method justifications
  - **Expected output:** Minimum 3 specific examples of goal text influencing agent reasoning with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify conceptual drift
  - **Primary method:** Compare final implementation/outputs against original goal, identify divergences in terminology, scope, or interpretation
  - **Expected output:** Conceptual drift assessment noting where implementation departed from goal language
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Assess language consistency across artefacts
  - **Primary method:** Check terminology consistency across spec.md, parameters.toml, progress.json, deliverables
  - **Expected output:** Consistency report identifying where language fragmented or evolved
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Minimum 3 concrete examples of goal text propagation documented with direct quotes
- **Logging:** Record propagation patterns and drift instances in progress_Dev_Analysis.json

---

## Task [3]: Evaluate Constitutional Compliance

**TOML Reference:** `tasks[id=3]` in parameters_Dev_Analysis.toml  
**Purpose:** Assess adherence to SPEC Engine Constitution (Articles I-XIV)

- **Step [1]:** Validate Article I compliance (North Star Principle)
  - **Primary method:** Verify goal singularity, clarity, measurability, explicitness
  - **Expected output:** Article I compliance score (pass/fail) with justification
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Validate Article II compliance (Hierarchical Structure)
  - **Primary method:** Count tasks (target: 2-5), count steps per task (target: 1-5), verify hierarchy maintained
  - **Backup [1]:** If counts borderline, assess whether structure serves goal effectively
  - **Expected output:** Article II compliance score with quantitative counts
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Validate Article III compliance (Dual-File Mandate)
  - **Primary method:** Cross-check spec.md and parameters.toml for ID matching, structure sync, cross-references
  - **Expected output:** Article III compliance score noting any bridging failures
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Validate Article VI compliance (Critical Flag Discipline)
  - **Primary method:** Calculate critical step percentage (target: 40-60%), assess appropriateness of critical flags
  - **Expected output:** Critical balance percentage and appropriateness assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Validate Article VII compliance (Backup Methods)
  - **Primary method:** Review all backup methods to ensure they are alternative reasoning paths, not retries
  - **Backup [1]:** Sample backup methods if total exceeds 15
  - **Expected output:** Backup quality score with examples of good/poor backups
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Check Article XIV compliance (if build goal)
  - **Primary method:** If goal contains build/create/system keywords, verify software stack defined, deployment criteria present
  - **Expected output:** Article XIV compliance (N/A or pass/fail with details)
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Review Articles IV, VIII, IX, X compliance from execution
  - **Primary method:** Analyse progress.json for validation execution, error propagation, mode discipline, comprehensive logging
  - **Expected output:** Compliance scores for Articles IV, VIII, IX, X with evidence from logs
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Calculate overall constitutional compliance score
  - **Primary method:** Aggregate individual article scores, weight by severity, generate 0-100 score
  - **Expected output:** Overall compliance score (0-100) with breakdown by article
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All applicable articles assessed with evidence-based scoring
- **Logging:** Record compliance scores and violations in progress_Dev_Analysis.json

---

## Task [4]: Analyse Execution Performance Metrics

**TOML Reference:** `tasks[id=4]` in parameters_Dev_Analysis.toml  
**Purpose:** Extract quantitative performance data from execution logs

- **Step [1]:** Parse progress.json for step outcomes
  - **Primary method:** Read progress_[descriptor].json, extract all step entries with status, method_used, retry_count
  - **Backup [1]:** If progress.json malformed, reconstruct from available logs
  - **Expected output:** Complete step outcome dataset with counts for success/failure/retry
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Calculate success and failure rates
  - **Primary method:** Compute: total steps, successful steps, failed steps, overall success rate, failure rate
  - **Expected output:** Success/failure metrics table with percentages
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Analyse backup method usage
  - **Primary method:** Count primary method uses, backup[1] uses, backup[2] uses, calculate backup invocation rate
  - **Expected output:** Backup usage statistics showing frequency and success rates per backup type
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Track mode escalations
  - **Primary method:** Identify all mode switches in progress.json, categorise escalation triggers
  - **Expected output:** Mode escalation count, trigger categorisation, escalation appropriateness assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Assess error propagation effectiveness
  - **Primary method:** Identify steps with dependencies, check if prior failures were read from progress.json, assess propagation handling
  - **Backup [1]:** If error propagation tracking sparse, infer from step sequence and outcomes
  - **Expected output:** Error propagation effectiveness score with examples
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Analyse retry patterns
  - **Primary method:** Extract retry_count per step, identify retry exhaustion cases, assess thoroughness
  - **Expected output:** Retry pattern analysis showing exhaustion rate and thoroughness score
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Calculate efficiency metrics
  - **Primary method:** Compute total steps attempted, steps per task, time per step (if timestamps available)
  - **Expected output:** Efficiency metrics table
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All quantitative metrics calculated with source data citations
- **Logging:** Record all performance metrics in progress_Dev_Analysis.json

---

## Task [5]: Correlate Agent Behaviour with Goal Characteristics

**TOML Reference:** `tasks[id=5]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify relationships between goal text properties and agent execution behaviour

- **Step [1]:** Establish correlation framework
  - **Primary method:** Define metrics for correlation: goal complexity vs task count, goal clarity vs error rate, goal specificity vs backup usage
  - **Expected output:** Correlation matrix framework listing goal characteristics and behaviour metrics
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Analyse goal complexity vs task decomposition
  - **Primary method:** Correlate goal complexity score (from Task 1) with number of tasks, steps per task, decomposition depth
  - **Backup [1]:** Use qualitative assessment if quantitative correlation weak
  - **Expected output:** Correlation finding: does complex goal lead to more/fewer tasks?
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Analyse goal clarity vs execution accuracy
  - **Primary method:** Correlate goal clarity indicators (explicit requirements, measurable criteria) with success rate, error rate
  - **Expected output:** Correlation finding: does clear goal reduce errors?
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse goal specificity vs backup usage
  - **Primary method:** Correlate technical specificity score with backup invocation rate, backup effectiveness
  - **Expected output:** Correlation finding: does vague goal increase backup reliance?
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Analyse goal formatting vs agent thinking patterns
  - **Primary method:** Review agent reasoning for structured vs narrative goals, assess thinking clarity and organisation
  - **Backup [1]:** If thinking logs sparse, assess output organisation as proxy
  - **Expected output:** Qualitative finding on formatting impact with examples
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Identify confounding factors
  - **Primary method:** Check for external factors affecting correlation: SPEC complexity, domain difficulty, resource availability
  - **Expected output:** List of confounding factors that may explain behaviour patterns
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Distinguish correlation from causation
  - **Primary method:** For each correlation found, assess whether relationship is causal, coincidental, or mediated by other factors
  - **Expected output:** Causality assessment for each correlation with confidence level
  - **Critical:** false
  - **Mode:** collaborative (human judgment needed for causality claims)

- **Verification:** Minimum 3 behaviour correlations identified with specific evidence
- **Logging:** Record correlations and causality assessments in progress_Dev_Analysis.json

---

## Task [6]: Assess Per-Task and Per-Step Behaviour Quality

**TOML Reference:** `tasks[id=6]` in parameters_Dev_Analysis.toml  
**Purpose:** Evaluate quality of task decomposition and step execution at granular level

- **Step [1]:** Evaluate task decomposition quality
  - **Primary method:** For each task, assess: Does task serve goal? Is task scope appropriate? Is task self-contained?
  - **Expected output:** Task quality assessment table with scores and rationale per task
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Assess step atomicity
  - **Primary method:** For each step, assess: Is step a single concrete action? Is step scope too broad/narrow? Is step executable?
  - **Backup [1]:** Sample steps if total exceeds 20
  - **Expected output:** Step atomicity assessment with examples of well/poorly scoped steps
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Evaluate critical flag appropriateness
  - **Primary method:** For each critical step, verify: Would failure truly block goal? For non-critical, verify: Can goal succeed without this?
  - **Expected output:** Critical flag appropriateness score with misclassification examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess expected output clarity
  - **Primary method:** For each step, rate expected output: specific/vague, measurable/subjective, achievable/unrealistic
  - **Expected output:** Expected output quality assessment with clarity distribution
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Evaluate method selection rationale
  - **Primary method:** For steps with multiple methods, assess whether primary/backup choices were well-justified
  - **Expected output:** Method selection quality score with examples
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All tasks and representative sample of steps assessed for quality
- **Logging:** Record quality assessments in progress_Dev_Analysis.json

---

## Task [7]: Conduct Error Analysis and Pattern Detection

**TOML Reference:** `tasks[id=7]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify error patterns, root causes, and improvement opportunities

- **Step [1]:** Categorise all errors by type
  - **Primary method:** Extract all failures from progress.json, categorise: validation errors, execution errors, resource errors, logic errors
  - **Expected output:** Error categorisation table with counts and percentages
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify error frequency patterns
  - **Primary method:** Analyse which tasks/steps had highest error rates, identify repeated failures
  - **Expected output:** Error hotspot analysis showing concentration areas
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Conduct root cause analysis
  - **Primary method:** For each error category, trace to root cause: SPEC design issue, execution issue, resource limitation, goal ambiguity
  - **Backup [1]:** Focus on top 5 most frequent errors if volume high
  - **Expected output:** Root cause mapping with prevention recommendations
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess recovery effectiveness
  - **Primary method:** For each error, check if backup methods resolved issue, assess recovery time, evaluate escalation appropriateness
  - **Expected output:** Recovery effectiveness score with successful/unsuccessful recovery examples
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify constitutional violations
  - **Primary method:** Check progress.json for constitutional_compliance section, extract all violations with severity
  - **Backup [1]:** Manual review of logs if compliance tracking absent
  - **Expected output:** Constitutional violation summary with article breakdown
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Distinguish preventable from inherent errors
  - **Primary method:** Classify each error: preventable through better SPEC design, inherent to task complexity, external/environmental
  - **Expected output:** Error preventability classification with improvement focus areas
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All errors analysed with root causes identified
- **Logging:** Record error analysis findings in progress_Dev_Analysis.json

---

## Task [8]: Generate Comprehensive Analysis Report with Recommendations

**TOML Reference:** `tasks[id=8]` in parameters_Dev_Analysis.toml  
**Purpose:** Synthesise all findings into actionable report

- **Step [1]:** Structure report outline
  - **Primary method:** Create report sections: Executive Summary, Goal Analysis, Propagation Findings, Performance Metrics, Correlations, Quality Assessment, Error Analysis, Recommendations
  - **Expected output:** Report outline with section headers
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Write Executive Summary
  - **Primary method:** Synthesise key findings: goal characteristics summary, main propagation patterns, overall performance, critical insights
  - **Expected output:** 200-300 word executive summary highlighting main findings
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Compile Goal Text Analysis section
  - **Primary method:** Aggregate Task 1 findings: goal characteristics table, complexity assessment, element breakdown
  - **Expected output:** Goal Text Analysis section with all metrics and assessments
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Compile Goal Text Propagation section
  - **Primary method:** Aggregate Task 2 findings: propagation examples, language flow diagram, conceptual drift assessment
  - **Expected output:** Goal Text Propagation section with minimum 3 concrete examples with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Compile Constitutional Compliance section
  - **Primary method:** Aggregate Task 3 findings: article-by-article scores, overall compliance score, violation summary
  - **Expected output:** Constitutional Compliance section with compliance scorecard
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Compile Execution Performance section
  - **Primary method:** Aggregate Task 4 findings: success/failure rates, backup usage, mode escalations, efficiency metrics
  - **Expected output:** Execution Performance section with metrics tables
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Compile Behaviour Correlation section
  - **Primary method:** Aggregate Task 5 findings: correlation matrix, causality assessments, confounding factors
  - **Expected output:** Behaviour Correlation section with correlation findings
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Compile Quality Assessment section
  - **Primary method:** Aggregate Task 6 findings: task quality scores, step atomicity, critical flag appropriateness
  - **Expected output:** Quality Assessment section with quality distributions
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Compile Error Analysis section
  - **Primary method:** Aggregate Task 7 findings: error categories, root causes, recovery effectiveness, preventability
  - **Expected output:** Error Analysis section with error breakdown and patterns
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Generate actionable recommendations
  - **Primary method:** Based on all findings, create specific recommendations for: goal formulation improvement, SPEC design enhancement, execution optimisation, constitutional compliance
  - **Backup [1]:** If recommendations unclear, escalate to collaborative mode for human input
  - **Expected output:** Minimum 5 specific, actionable recommendations linked to findings
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Add cross-project comparison framework (if applicable)
  - **Primary method:** If analysing multiple SPECs, create comparison tables for key metrics across projects
  - **Expected output:** Cross-project comparison section (optional, only if multiple projects analysed)
  - **Critical:** false
  - **Mode:** silent

- **Step [12]:** Finalise report formatting and references
  - **Primary method:** Ensure all sections formatted consistently, add table of contents, verify all data citations present
  - **Expected output:** Complete, polished analysis report in markdown format
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Report contains all required sections, metrics are evidence-based, recommendations are actionable
- **Logging:** Record report completion in progress_Dev_Analysis.json with final deliverable path

---

## Bridging: Markdown ↔ TOML Synchronisation

This spec file (Dev_Analysis_SPEC.md) must maintain perfect alignment with its companion file (parameters_Dev_Analysis.toml).

**Bridging Requirements:**
1. Each task in this file must have corresponding `[[tasks]]` entry in TOML with matching ID (1-8)
2. Each step within a task must have corresponding `[[tasks.steps]]` entry with matching ID
3. Expected outputs in this file must match `expected_output` fields in TOML
4. Critical flags must be synchronised between files
5. Constraints referenced must exist in TOML `[constraints]` section

**Example Cross-References:**
- "See `constraints.min_examples_required` in parameters_Dev_Analysis.toml" (Task 2, Step 4)
- "As defined in `tasks[id=4]` in TOML" (Task 4 reference)
- "Must satisfy TOML verification requirements" (All task verifications)

The exe_Dev_Analysis.md controller will validate this synchronisation during initialisation (Section 1.8).

---

## Instructions for LLM Executor

1. **Start with goal understanding**: This analysis examines how goal text propagates and influences SPEC development
2. **Execute tasks sequentially**: Tasks 1-2 gather data, Tasks 3-7 analyse patterns, Task 8 synthesises findings
3. **Maintain objectivity**: Base all findings on evidence from files, logs, and artefacts
4. **Track propagation carefully**: Pay special attention to how exact goal language appears throughout project
5. **Quantify where possible**: Use numerical metrics rather than subjective assessments when feasible
6. **Distinguish correlation from causation**: Note relationships but assess causality carefully
7. **Document thoroughly**: Log all findings in progress_Dev_Analysis.json for traceability
8. **Focus on actionability**: Recommendations should be specific and implementable
9. **Read prior outcomes**: Before each step, check progress.json for relevant prior findings
10. **Escalate appropriately**: Use collaborative mode for causality judgements and unclear recommendation priorities

---

## Expected Analysis Output Structure

The final report should follow this structure:

```markdown
# SPEC Development Analysis Report

## Executive Summary
[200-300 word overview of key findings]

## 1. Goal Text Analysis
### 1.1 Initial Goal Characteristics
- Quantitative metrics table
- Complexity classification
- Element breakdown

### 1.2 Technical Specificity Assessment
- Specificity score with justification
- Domain terminology analysis

## 2. Goal Text Propagation Analysis
### 2.1 Propagation Through Tasks
- Task-level language mapping
- Specific examples with quotes

### 2.2 Propagation Through Steps
- Step-level language mapping
- Propagation matrix

### 2.3 Agent Thinking Patterns
- Minimum 3 examples of goal text in reasoning
- Direct quotes from logs/chat

### 2.4 Conceptual Drift Assessment
- Identified divergences
- Impact analysis

## 3. Constitutional Compliance Assessment
### 3.1 Article-by-Article Scores
- Individual article compliance
- Evidence for each assessment

### 3.2 Overall Compliance Score
- Aggregate score (0-100)
- Violation summary

## 4. Execution Performance Metrics
### 4.1 Success and Failure Rates
- Quantitative metrics table
- Rate comparisons

### 4.2 Backup Method Usage
- Usage statistics
- Effectiveness assessment

### 4.3 Mode Escalations
- Escalation count and triggers
- Appropriateness evaluation

### 4.4 Efficiency Metrics
- Steps per task
- Time analysis (if available)

## 5. Behaviour Correlation Analysis
### 5.1 Identified Correlations
- Goal characteristics vs execution behaviour
- Correlation strength assessment

### 5.2 Causality Assessment
- Causal vs correlational relationships
- Confidence levels

### 5.3 Confounding Factors
- External influences
- Mediation effects

## 6. Quality Assessment
### 6.1 Task Decomposition Quality
- Per-task quality scores
- Decomposition effectiveness

### 6.2 Step Quality Analysis
- Atomicity assessment
- Critical flag appropriateness

### 6.3 Method Selection Quality
- Primary/backup rationale
- Method effectiveness

## 7. Error Analysis
### 7.1 Error Categorisation
- Error type distribution
- Frequency patterns

### 7.2 Root Cause Analysis
- Root cause mapping
- Prevention opportunities

### 7.3 Recovery Effectiveness
- Recovery success rates
- Backup effectiveness

### 7.4 Constitutional Violations
- Violation breakdown by article
- Severity assessment

## 8. Recommendations
### 8.1 Goal Formulation Improvements
[Specific, actionable recommendations]

### 8.2 SPEC Design Enhancements
[Specific, actionable recommendations]

### 8.3 Execution Optimisation
[Specific, actionable recommendations]

### 8.4 Constitutional Compliance
[Specific, actionable recommendations]

### 8.5 Future Research Directions
[Areas for deeper investigation]

## Appendices
### A. Raw Data Tables
### B. Propagation Examples (Full Quotes)
### C. Metrics Calculation Methods
### D. Source Citations
```

---

**End of Dev_Analysis_SPEC.md**

This SPEC is designed to be reusable across multiple test SPEC analyses, enabling systematic comparison and pattern identification.

```

Perfect! I've created the comprehensive **Dev_Analysis_SPEC.md** at the requested location. Here's what's included:

## What I've Built:

**8 Integrated Analysis Tasks:**
1. **Extract & Characterise Initial Goal Text** - Quantitative metrics, complexity, technical specificity
2. **Map Goal Text Propagation** - Track language flow through tasks, steps, agent thinking (minimum 3 concrete examples)
3. **Evaluate Constitutional Compliance** - All Articles I-XIV with scoring
4. **Analyse Execution Performance** - Success rates, backup usage, mode escalations, error propagation
5. **Correlate Agent Behaviour with Goal Characteristics** - Link goal properties to execution patterns
6. **Assess Per-Task/Step Quality** - Task decomposition, step atomicity, critical flags
7. **Conduct Error Analysis** - Error patterns, root causes, recovery effectiveness
8. **Generate Comprehensive Report** - Synthesise all findings with actionable recommendations

## Key Features:

- **Goal Text Propagation Tracking** - Specifically addresses your research questions about language propagation, correlation with behaviour, and impact on metrics
- **Quantitative Metrics** - Evidence-based analysis with numerical data
- **ADHD-Friendly Structure** - Broken into manageable chunks with clear progress tracking
- **Constitutional Compliance** - Follows SPEC Engine framework perfectly
- **Cross-Project Ready** - Designed for comparison across multiple SPECs
- **Actionable Output** - Generates specific recommendations linked to findings

Would you like me to create the companion **parameters_Dev_Analysis.toml** and **exe_Dev_Analysis.md** files to complete the three-file SPEC architecture?

---

**User**

i forgot to add, the SPEC should act in silent mode and require no user input except the locationof the project developmenet folder



Further, gather lots of data including steps taken, error logs, development length time, number of files, tokens etc... in this vein. Please be thorough and meticulous

---

**Cursor**

Excellent additions! I'll update the SPEC to be fully autonomous (silent mode only) and add comprehensive data gathering metrics. Let me revise it now.

```markdown
# Dev Analysis SPEC

**Version:** 1.0  
**Last Updated:** 2025-11-03  
**Purpose:** Analyse development of test SPECs to identify patterns, metrics, and goal text propagation effects

---

## Goal

Perform comprehensive analysis of a test SPEC's development lifecycle to identify how initial goal text propagates through the system and impacts agent behaviour, execution accuracy, and project outcomes.

---

## Software Stack & Architecture

**Not Applicable** - This is an analysis task, not a build goal.

---

## Definition of Complete

What must exist and be verified:
- [ ] **Primary deliverable:** Comprehensive analysis report (markdown format) covering all analysis areas
- [ ] **Quality standards met:** 
  - All 8 analysis tasks completed with documented findings
  - Goal text propagation patterns identified with specific examples
  - Quantitative metrics calculated for execution performance
  - Cross-correlation analysis between goal characteristics and outcomes
  - Recommendations provided based on findings
- [ ] **Verification method:** 
  - Report contains all required sections (see tasks below)
  - Quantitative metrics include numerical values with source citations
  - At least 3 specific examples of goal text propagation documented
  - Recommendations are actionable and linked to specific findings

---

## Definitions

- **goal**: Analyse how initial goal text characteristics influence SPEC development and execution
- **task[n]**: Discrete analysis objectives examining different aspects of SPEC development
- **step[m]**: Concrete analytical actions within each task
- **backup[p]**: Alternative analysis methods when primary approach is blocked
- **critical_flag**: Boolean indicating whether analysis step is essential to overall goal
- **mode**: `silent` (fully autonomous - NO USER INPUT REQUIRED except initial project folder location)
- **progress.json**: Structured log tracking analysis execution and findings
- **project_folder**: Target development project folder path (ONLY required user input)

---

## Components

Analysis requires access to:
- **Test SPEC files:** spec_[descriptor].md, parameters_[descriptor].toml, exe_[descriptor].md
- **Execution logs:** progress_[descriptor].json
- **Project artefacts:** Code files, documentation, error logs, validation reports
- **Chat history:** Conversation transcripts showing agent thinking and decision-making
- **Constitution:** __SPEC_Engine/_Constitution/constitution.md for compliance checking

**Machine-Readable Components:**  
See `[components]` section in parameters_Dev_Analysis.toml

---

## Constraints

- Analysis must be objective and evidence-based
- All metrics must be traceable to source data
- Goal text propagation analysis must include minimum 3 concrete examples
- Quantitative metrics must include: success rates, error rates, mode escalations, backup usage
- Findings must distinguish correlation from causation
- Recommendations must be specific and actionable

**Machine-Readable Constraints:**  
See `[constraints]` section in parameters_Dev_Analysis.toml:
- `min_examples_required = 3` (goal text propagation examples)
- `metrics_evidence_based = true` (all metrics must cite sources)
- `recommendation_specificity = "actionable"` (recommendations must be implementable)

---

## User Stories

- As a **SPEC developer**, I want to understand how goal phrasing impacts development so I can write more effective goals
- As a **system architect**, I want to identify patterns in SPEC execution so I can improve the framework
- As a **researcher**, I want to quantify goal text propagation so I can understand agent behaviour correlation
- As a **project manager**, I want metrics on SPEC performance so I can assess project quality

---

## Analysis Framework

This SPEC analyses development across 8 integrated dimensions:

### Dimension 1: Goal Text Characteristics
- Length (word count, character count, sentence complexity)
- Number of distinct elements/requirements
- Literacy level (Flesch-Kincaid, technical density)
- Formatting (structure, lists, emphasis)
- Familiarity/Technical specificity

### Dimension 2: Goal Text Propagation
- How goal language appears in task descriptions
- Goal terminology in step definitions
- Phrasing patterns in agent thinking/reasoning
- Language consistency across SPEC artefacts
- Conceptual drift from goal to implementation

### Dimension 3: Constitutional Compliance
- Article I-XIV adherence scoring
- Critical flag balance (target: 40-60%)
- Backup method quality assessment
- Bridging quality (Markdown-TOML sync)
- Validation checkpoint outcomes

### Dimension 4: Execution Performance
- Step success/failure rates
- Backup invocation frequency
- Mode escalation patterns
- Error propagation effectiveness
- Retry patterns and exhaustion

### Dimension 5: Agent Behaviour Correlation
- Thinking patterns vs goal complexity
- Decision quality vs goal clarity
- Output quality vs goal specificity
- Backup selection vs goal ambiguity
- Escalation triggers vs goal characteristics

### Dimension 6: Per-Task/Step Behaviour
- Task decomposition quality
- Step atomicity assessment
- Critical flag appropriateness
- Expected output clarity
- Method selection rationale

### Dimension 7: Error Analysis
- Error types and frequencies
- Root cause patterns
- Recovery effectiveness
- Constitutional violations
- Preventable vs inherent errors

### Dimension 8: Outcome Metrics
- Goal achievement status (ACHIEVED/PARTIAL/NOT_ACHIEVED)
- Deliverable completeness
- Quality standards met
- Time/step efficiency
- Comparison to expected outcomes

---

## Task [1]: Extract and Characterise Initial Goal Text

**TOML Reference:** `tasks[id=1]` in parameters_Dev_Analysis.toml  
**Purpose:** Establish baseline characteristics of the goal that initiated SPEC development

- **Step [1]:** Locate and extract initial goal text
  - **Primary method:** Read SPEC markdown file Goal section and chat history for original user goal statement
  - **Backup [1]:** If chat history unavailable, use goal section from spec_[descriptor].md as proxy
  - **Expected output:** Exact goal text with source citation and timestamp
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Calculate quantitative text characteristics
  - **Primary method:** Compute word count, character count, sentence count, avg sentence length, Flesch-Kincaid score
  - **Backup [1]:** If automated scoring unavailable, perform manual classification (simple/moderate/complex)
  - **Expected output:** Table with numerical metrics and complexity classification
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Identify distinct elements and requirements
  - **Primary method:** Parse goal for discrete requirements, constraints, deliverables, success criteria
  - **Backup [1]:** Use linguistic chunking to identify conceptual units if structure unclear
  - **Expected output:** Numbered list of distinct elements (target: 3-10 elements)
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess technical specificity and domain familiarity
  - **Primary method:** Identify technical terms, domain-specific language, assumed knowledge, explicit vs implicit requirements
  - **Backup [1]:** Compare vocabulary against common vs specialised term databases
  - **Expected output:** Technical specificity score (1-5 scale) with justification and term examples
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Analyse formatting and structure
  - **Primary method:** Document use of lists, emphasis, sections, explicit vs narrative format
  - **Expected output:** Formatting assessment noting structural elements present
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All goal characteristics documented with quantitative metrics where possible
- **Logging:** Record all measurements in progress_Dev_Analysis.json for correlation analysis

---

## Task [2]: Map Goal Text Propagation Throughout Project

**TOML Reference:** `tasks[id=2]` in parameters_Dev_Analysis.toml  
**Purpose:** Track how initial goal language and concepts propagate through SPEC artefacts

- **Step [1]:** Extract task descriptions from SPEC
  - **Primary method:** Parse spec_[descriptor].md for all task titles and descriptions
  - **Expected output:** List of tasks with full text
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify goal language in task descriptions
  - **Primary method:** Compare task descriptions to goal text, noting shared terminology, conceptual overlap, verbatim phrases
  - **Backup [1]:** Use semantic similarity scoring if direct comparison insufficient
  - **Expected output:** Table mapping goal terms to task descriptions with similarity scores
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Extract step definitions and analyse propagation
  - **Primary method:** Parse all step descriptions, identify goal/task terminology presence, track conceptual consistency
  - **Backup [1]:** Focus on critical steps only if volume is high (>20 steps)
  - **Expected output:** Propagation matrix showing goal→task→step language flow with specific examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse agent thinking and reasoning patterns
  - **Primary method:** Review chat history/logs for agent internal reasoning, note how goal concepts appear in thinking
  - **Backup [1]:** If full chat unavailable, analyse progress.json logs for method justifications
  - **Expected output:** Minimum 3 specific examples of goal text influencing agent reasoning with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify conceptual drift
  - **Primary method:** Compare final implementation/outputs against original goal, identify divergences in terminology, scope, or interpretation
  - **Expected output:** Conceptual drift assessment noting where implementation departed from goal language
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Assess language consistency across artefacts
  - **Primary method:** Check terminology consistency across spec.md, parameters.toml, progress.json, deliverables
  - **Expected output:** Consistency report identifying where language fragmented or evolved
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Minimum 3 concrete examples of goal text propagation documented with direct quotes
- **Logging:** Record propagation patterns and drift instances in progress_Dev_Analysis.json

---

## Task [3]: Evaluate Constitutional Compliance

**TOML Reference:** `tasks[id=3]` in parameters_Dev_Analysis.toml  
**Purpose:** Assess adherence to SPEC Engine Constitution (Articles I-XIV)

- **Step [1]:** Validate Article I compliance (North Star Principle)
  - **Primary method:** Verify goal singularity, clarity, measurability, explicitness
  - **Expected output:** Article I compliance score (pass/fail) with justification
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Validate Article II compliance (Hierarchical Structure)
  - **Primary method:** Count tasks (target: 2-5), count steps per task (target: 1-5), verify hierarchy maintained
  - **Backup [1]:** If counts borderline, assess whether structure serves goal effectively
  - **Expected output:** Article II compliance score with quantitative counts
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Validate Article III compliance (Dual-File Mandate)
  - **Primary method:** Cross-check spec.md and parameters.toml for ID matching, structure sync, cross-references
  - **Expected output:** Article III compliance score noting any bridging failures
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Validate Article VI compliance (Critical Flag Discipline)
  - **Primary method:** Calculate critical step percentage (target: 40-60%), assess appropriateness of critical flags
  - **Expected output:** Critical balance percentage and appropriateness assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Validate Article VII compliance (Backup Methods)
  - **Primary method:** Review all backup methods to ensure they are alternative reasoning paths, not retries
  - **Backup [1]:** Sample backup methods if total exceeds 15
  - **Expected output:** Backup quality score with examples of good/poor backups
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Check Article XIV compliance (if build goal)
  - **Primary method:** If goal contains build/create/system keywords, verify software stack defined, deployment criteria present
  - **Expected output:** Article XIV compliance (N/A or pass/fail with details)
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Review Articles IV, VIII, IX, X compliance from execution
  - **Primary method:** Analyse progress.json for validation execution, error propagation, mode discipline, comprehensive logging
  - **Expected output:** Compliance scores for Articles IV, VIII, IX, X with evidence from logs
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Calculate overall constitutional compliance score
  - **Primary method:** Aggregate individual article scores, weight by severity, generate 0-100 score
  - **Expected output:** Overall compliance score (0-100) with breakdown by article
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All applicable articles assessed with evidence-based scoring
- **Logging:** Record compliance scores and violations in progress_Dev_Analysis.json

---

## Task [4]: Analyse Execution Performance Metrics

**TOML Reference:** `tasks[id=4]` in parameters_Dev_Analysis.toml  
**Purpose:** Extract quantitative performance data from execution logs

- **Step [1]:** Parse progress.json for step outcomes
  - **Primary method:** Read progress_[descriptor].json, extract all step entries with status, method_used, retry_count
  - **Backup [1]:** If progress.json malformed, reconstruct from available logs
  - **Expected output:** Complete step outcome dataset with counts for success/failure/retry
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Calculate success and failure rates
  - **Primary method:** Compute: total steps, successful steps, failed steps, overall success rate, failure rate
  - **Expected output:** Success/failure metrics table with percentages
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Analyse backup method usage
  - **Primary method:** Count primary method uses, backup[1] uses, backup[2] uses, calculate backup invocation rate
  - **Expected output:** Backup usage statistics showing frequency and success rates per backup type
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Track mode escalations
  - **Primary method:** Identify all mode switches in progress.json, categorise escalation triggers
  - **Expected output:** Mode escalation count, trigger categorisation, escalation appropriateness assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Assess error propagation effectiveness
  - **Primary method:** Identify steps with dependencies, check if prior failures were read from progress.json, assess propagation handling
  - **Backup [1]:** If error propagation tracking sparse, infer from step sequence and outcomes
  - **Expected output:** Error propagation effectiveness score with examples
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Analyse retry patterns
  - **Primary method:** Extract retry_count per step, identify retry exhaustion cases, assess thoroughness
  - **Expected output:** Retry pattern analysis showing exhaustion rate and thoroughness score
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Calculate efficiency metrics
  - **Primary method:** Compute total steps attempted, steps per task, time per step (if timestamps available)
  - **Expected output:** Efficiency metrics table
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All quantitative metrics calculated with source data citations
- **Logging:** Record all performance metrics in progress_Dev_Analysis.json

---

## Task [5]: Correlate Agent Behaviour with Goal Characteristics

**TOML Reference:** `tasks[id=5]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify relationships between goal text properties and agent execution behaviour

- **Step [1]:** Establish correlation framework
  - **Primary method:** Define metrics for correlation: goal complexity vs task count, goal clarity vs error rate, goal specificity vs backup usage
  - **Expected output:** Correlation matrix framework listing goal characteristics and behaviour metrics
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Analyse goal complexity vs task decomposition
  - **Primary method:** Correlate goal complexity score (from Task 1) with number of tasks, steps per task, decomposition depth
  - **Backup [1]:** Use qualitative assessment if quantitative correlation weak
  - **Expected output:** Correlation finding: does complex goal lead to more/fewer tasks?
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Analyse goal clarity vs execution accuracy
  - **Primary method:** Correlate goal clarity indicators (explicit requirements, measurable criteria) with success rate, error rate
  - **Expected output:** Correlation finding: does clear goal reduce errors?
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse goal specificity vs backup usage
  - **Primary method:** Correlate technical specificity score with backup invocation rate, backup effectiveness
  - **Expected output:** Correlation finding: does vague goal increase backup reliance?
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Analyse goal formatting vs agent thinking patterns
  - **Primary method:** Review agent reasoning for structured vs narrative goals, assess thinking clarity and organisation
  - **Backup [1]:** If thinking logs sparse, assess output organisation as proxy
  - **Expected output:** Qualitative finding on formatting impact with examples
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Identify confounding factors
  - **Primary method:** Check for external factors affecting correlation: SPEC complexity, domain difficulty, resource availability
  - **Expected output:** List of confounding factors that may explain behaviour patterns
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Distinguish correlation from causation
  - **Primary method:** For each correlation found, assess whether relationship is causal, coincidental, or mediated by other factors
  - **Expected output:** Causality assessment for each correlation with confidence level
  - **Critical:** false
  - **Mode:** collaborative (human judgment needed for causality claims)

- **Verification:** Minimum 3 behaviour correlations identified with specific evidence
- **Logging:** Record correlations and causality assessments in progress_Dev_Analysis.json

---

## Task [6]: Assess Per-Task and Per-Step Behaviour Quality

**TOML Reference:** `tasks[id=6]` in parameters_Dev_Analysis.toml  
**Purpose:** Evaluate quality of task decomposition and step execution at granular level

- **Step [1]:** Evaluate task decomposition quality
  - **Primary method:** For each task, assess: Does task serve goal? Is task scope appropriate? Is task self-contained?
  - **Expected output:** Task quality assessment table with scores and rationale per task
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Assess step atomicity
  - **Primary method:** For each step, assess: Is step a single concrete action? Is step scope too broad/narrow? Is step executable?
  - **Backup [1]:** Sample steps if total exceeds 20
  - **Expected output:** Step atomicity assessment with examples of well/poorly scoped steps
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Evaluate critical flag appropriateness
  - **Primary method:** For each critical step, verify: Would failure truly block goal? For non-critical, verify: Can goal succeed without this?
  - **Expected output:** Critical flag appropriateness score with misclassification examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess expected output clarity
  - **Primary method:** For each step, rate expected output: specific/vague, measurable/subjective, achievable/unrealistic
  - **Expected output:** Expected output quality assessment with clarity distribution
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Evaluate method selection rationale
  - **Primary method:** For steps with multiple methods, assess whether primary/backup choices were well-justified
  - **Expected output:** Method selection quality score with examples
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All tasks and representative sample of steps assessed for quality
- **Logging:** Record quality assessments in progress_Dev_Analysis.json

---

## Task [7]: Conduct Error Analysis and Pattern Detection

**TOML Reference:** `tasks[id=7]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify error patterns, root causes, and improvement opportunities

- **Step [1]:** Categorise all errors by type
  - **Primary method:** Extract all failures from progress.json, categorise: validation errors, execution errors, resource errors, logic errors
  - **Expected output:** Error categorisation table with counts and percentages
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify error frequency patterns
  - **Primary method:** Analyse which tasks/steps had highest error rates, identify repeated failures
  - **Expected output:** Error hotspot analysis showing concentration areas
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Conduct root cause analysis
  - **Primary method:** For each error category, trace to root cause: SPEC design issue, execution issue, resource limitation, goal ambiguity
  - **Backup [1]:** Focus on top 5 most frequent errors if volume high
  - **Expected output:** Root cause mapping with prevention recommendations
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess recovery effectiveness
  - **Primary method:** For each error, check if backup methods resolved issue, assess recovery time, evaluate escalation appropriateness
  - **Expected output:** Recovery effectiveness score with successful/unsuccessful recovery examples
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify constitutional violations
  - **Primary method:** Check progress.json for constitutional_compliance section, extract all violations with severity
  - **Backup [1]:** Manual review of logs if compliance tracking absent
  - **Expected output:** Constitutional violation summary with article breakdown
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Distinguish preventable from inherent errors
  - **Primary method:** Classify each error: preventable through better SPEC design, inherent to task complexity, external/environmental
  - **Expected output:** Error preventability classification with improvement focus areas
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All errors analysed with root causes identified
- **Logging:** Record error analysis findings in progress_Dev_Analysis.json

---

## Task [8]: Generate Comprehensive Analysis Report with Recommendations

**TOML Reference:** `tasks[id=8]` in parameters_Dev_Analysis.toml  
**Purpose:** Synthesise all findings into actionable report

- **Step [1]:** Structure report outline
  - **Primary method:** Create report sections: Executive Summary, Goal Analysis, Propagation Findings, Performance Metrics, Correlations, Quality Assessment, Error Analysis, Recommendations
  - **Expected output:** Report outline with section headers
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Write Executive Summary
  - **Primary method:** Synthesise key findings: goal characteristics summary, main propagation patterns, overall performance, critical insights
  - **Expected output:** 200-300 word executive summary highlighting main findings
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Compile Goal Text Analysis section
  - **Primary method:** Aggregate Task 1 findings: goal characteristics table, complexity assessment, element breakdown
  - **Expected output:** Goal Text Analysis section with all metrics and assessments
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Compile Goal Text Propagation section
  - **Primary method:** Aggregate Task 2 findings: propagation examples, language flow diagram, conceptual drift assessment
  - **Expected output:** Goal Text Propagation section with minimum 3 concrete examples with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Compile Constitutional Compliance section
  - **Primary method:** Aggregate Task 3 findings: article-by-article scores, overall compliance score, violation summary
  - **Expected output:** Constitutional Compliance section with compliance scorecard
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Compile Execution Performance section
  - **Primary method:** Aggregate Task 4 findings: success/failure rates, backup usage, mode escalations, efficiency metrics
  - **Expected output:** Execution Performance section with metrics tables
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Compile Behaviour Correlation section
  - **Primary method:** Aggregate Task 5 findings: correlation matrix, causality assessments, confounding factors
  - **Expected output:** Behaviour Correlation section with correlation findings
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Compile Quality Assessment section
  - **Primary method:** Aggregate Task 6 findings: task quality scores, step atomicity, critical flag appropriateness
  - **Expected output:** Quality Assessment section with quality distributions
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Compile Error Analysis section
  - **Primary method:** Aggregate Task 7 findings: error categories, root causes, recovery effectiveness, preventability
  - **Expected output:** Error Analysis section with error breakdown and patterns
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Generate actionable recommendations
  - **Primary method:** Based on all findings, create specific recommendations for: goal formulation improvement, SPEC design enhancement, execution optimisation, constitutional compliance
  - **Backup [1]:** If recommendations unclear, escalate to collaborative mode for human input
  - **Expected output:** Minimum 5 specific, actionable recommendations linked to findings
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Add cross-project comparison framework (if applicable)
  - **Primary method:** If analysing multiple SPECs, create comparison tables for key metrics across projects
  - **Expected output:** Cross-project comparison section (optional, only if multiple projects analysed)
  - **Critical:** false
  - **Mode:** silent

- **Step [12]:** Finalise report formatting and references
  - **Primary method:** Ensure all sections formatted consistently, add table of contents, verify all data citations present
  - **Expected output:** Complete, polished analysis report in markdown format
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Report contains all required sections, metrics are evidence-based, recommendations are actionable
- **Logging:** Record report completion in progress_Dev_Analysis.json with final deliverable path

---

## Bridging: Markdown ↔ TOML Synchronisation

This spec file (Dev_Analysis_SPEC.md) must maintain perfect alignment with its companion file (parameters_Dev_Analysis.toml).

**Bridging Requirements:**
1. Each task in this file must have corresponding `[[tasks]]` entry in TOML with matching ID (1-8)
2. Each step within a task must have corresponding `[[tasks.steps]]` entry with matching ID
3. Expected outputs in this file must match `expected_output` fields in TOML
4. Critical flags must be synchronised between files
5. Constraints referenced must exist in TOML `[constraints]` section

**Example Cross-References:**
- "See `constraints.min_examples_required` in parameters_Dev_Analysis.toml" (Task 2, Step 4)
- "As defined in `tasks[id=4]` in TOML" (Task 4 reference)
- "Must satisfy TOML verification requirements" (All task verifications)

The exe_Dev_Analysis.md controller will validate this synchronisation during initialisation (Section 1.8).

---

## Instructions for LLM Executor

1. **Start with goal understanding**: This analysis examines how goal text propagates and influences SPEC development
2. **Execute tasks sequentially**: Tasks 1-2 gather data, Tasks 3-7 analyse patterns, Task 8 synthesises findings
3. **Maintain objectivity**: Base all findings on evidence from files, logs, and artefacts
4. **Track propagation carefully**: Pay special attention to how exact goal language appears throughout project
5. **Quantify where possible**: Use numerical metrics rather than subjective assessments when feasible
6. **Distinguish correlation from causation**: Note relationships but assess causality carefully
7. **Document thoroughly**: Log all findings in progress_Dev_Analysis.json for traceability
8. **Focus on actionability**: Recommendations should be specific and implementable
9. **Read prior outcomes**: Before each step, check progress.json for relevant prior findings
10. **Escalate appropriately**: Use collaborative mode for causality judgements and unclear recommendation priorities

---

## Expected Analysis Output Structure

The final report should follow this structure:

```markdown
# SPEC Development Analysis Report

## Executive Summary
[200-300 word overview of key findings]

## 1. Goal Text Analysis
### 1.1 Initial Goal Characteristics
- Quantitative metrics table
- Complexity classification
- Element breakdown

### 1.2 Technical Specificity Assessment
- Specificity score with justification
- Domain terminology analysis

## 2. Goal Text Propagation Analysis
### 2.1 Propagation Through Tasks
- Task-level language mapping
- Specific examples with quotes

### 2.2 Propagation Through Steps
- Step-level language mapping
- Propagation matrix

### 2.3 Agent Thinking Patterns
- Minimum 3 examples of goal text in reasoning
- Direct quotes from logs/chat

### 2.4 Conceptual Drift Assessment
- Identified divergences
- Impact analysis

## 3. Constitutional Compliance Assessment
### 3.1 Article-by-Article Scores
- Individual article compliance
- Evidence for each assessment

### 3.2 Overall Compliance Score
- Aggregate score (0-100)
- Violation summary

## 4. Execution Performance Metrics
### 4.1 Success and Failure Rates
- Quantitative metrics table
- Rate comparisons

### 4.2 Backup Method Usage
- Usage statistics
- Effectiveness assessment

### 4.3 Mode Escalations
- Escalation count and triggers
- Appropriateness evaluation

### 4.4 Efficiency Metrics
- Steps per task
- Time analysis (if available)

## 5. Behaviour Correlation Analysis
### 5.1 Identified Correlations
- Goal characteristics vs execution behaviour
- Correlation strength assessment

### 5.2 Causality Assessment
- Causal vs correlational relationships
- Confidence levels

### 5.3 Confounding Factors
- External influences
- Mediation effects

## 6. Quality Assessment
### 6.1 Task Decomposition Quality
- Per-task quality scores
- Decomposition effectiveness

### 6.2 Step Quality Analysis
- Atomicity assessment
- Critical flag appropriateness

### 6.3 Method Selection Quality
- Primary/backup rationale
- Method effectiveness

## 7. Error Analysis
### 7.1 Error Categorisation
- Error type distribution
- Frequency patterns

### 7.2 Root Cause Analysis
- Root cause mapping
- Prevention opportunities

### 7.3 Recovery Effectiveness
- Recovery success rates
- Backup effectiveness

### 7.4 Constitutional Violations
- Violation breakdown by article
- Severity assessment

## 8. Recommendations
### 8.1 Goal Formulation Improvements
[Specific, actionable recommendations]

### 8.2 SPEC Design Enhancements
[Specific, actionable recommendations]

### 8.3 Execution Optimisation
[Specific, actionable recommendations]

### 8.4 Constitutional Compliance
[Specific, actionable recommendations]

### 8.5 Future Research Directions
[Areas for deeper investigation]

## Appendices
### A. Raw Data Tables
### B. Propagation Examples (Full Quotes)
### C. Metrics Calculation Methods
### D. Source Citations
```

---

**End of Dev_Analysis_SPEC.md**

This SPEC is designed to be reusable across multiple test SPEC analyses, enabling systematic comparison and pattern identification.


```

```markdown
# Dev Analysis SPEC

**Version:** 1.0  
**Last Updated:** 2025-11-03  
**Purpose:** Analyse development of test SPECs to identify patterns, metrics, and goal text propagation effects

---

## Goal

Perform comprehensive analysis of a test SPEC's development lifecycle to identify how initial goal text propagates through the system and impacts agent behaviour, execution accuracy, and project outcomes.

---

## Software Stack & Architecture

**Not Applicable** - This is an analysis task, not a build goal.

---

## Definition of Complete

What must exist and be verified:
- [ ] **Primary deliverable:** Comprehensive analysis report (markdown format) covering all analysis areas
- [ ] **Quality standards met:** 
  - All 8 analysis tasks completed with documented findings
  - Goal text propagation patterns identified with specific examples
  - Quantitative metrics calculated for execution performance
  - Cross-correlation analysis between goal characteristics and outcomes
  - Recommendations provided based on findings
- [ ] **Verification method:** 
  - Report contains all required sections (see tasks below)
  - Quantitative metrics include numerical values with source citations
  - At least 3 specific examples of goal text propagation documented
  - Recommendations are actionable and linked to specific findings

---

## Definitions

- **goal**: Analyse how initial goal text characteristics influence SPEC development and execution
- **task[n]**: Discrete analysis objectives examining different aspects of SPEC development
- **step[m]**: Concrete analytical actions within each task
- **backup[p]**: Alternative analysis methods when primary approach is blocked
- **critical_flag**: Boolean indicating whether analysis step is essential to overall goal
- **mode**: `silent` (fully autonomous - NO USER INPUT REQUIRED except initial project folder location)
- **progress.json**: Structured log tracking analysis execution and findings
- **project_folder**: Target development project folder path (ONLY required user input)

---

## Components

Analysis requires access to:
- **Test SPEC files:** spec_[descriptor].md, parameters_[descriptor].toml, exe_[descriptor].md
- **Execution logs:** progress_[descriptor].json
- **Project artefacts:** Code files, documentation, error logs, validation reports
- **Chat history:** Conversation transcripts showing agent thinking and decision-making
- **Constitution:** __SPEC_Engine/_Constitution/constitution.md for compliance checking

**Machine-Readable Components:**  
See `[components]` section in parameters_Dev_Analysis.toml

---

## Constraints

- Analysis must be objective and evidence-based
- All metrics must be traceable to source data
- Goal text propagation analysis must include minimum 3 concrete examples
- Quantitative metrics must include: success rates, error rates, mode escalations, backup usage
- Findings must distinguish correlation from causation
- Recommendations must be specific and actionable

**Machine-Readable Constraints:**  
See `[constraints]` section in parameters_Dev_Analysis.toml:
- `min_examples_required = 3` (goal text propagation examples)
- `metrics_evidence_based = true` (all metrics must cite sources)
- `recommendation_specificity = "actionable"` (recommendations must be implementable)

---

## User Stories

- As a **SPEC developer**, I want to understand how goal phrasing impacts development so I can write more effective goals
- As a **system architect**, I want to identify patterns in SPEC execution so I can improve the framework
- As a **researcher**, I want to quantify goal text propagation so I can understand agent behaviour correlation
- As a **project manager**, I want metrics on SPEC performance so I can assess project quality

---

## Analysis Framework

This SPEC analyses development across 8 integrated dimensions:

### Dimension 1: Goal Text Characteristics
- Length (word count, character count, sentence complexity)
- Number of distinct elements/requirements
- Literacy level (Flesch-Kincaid, technical density)
- Formatting (structure, lists, emphasis)
- Familiarity/Technical specificity

### Dimension 2: Goal Text Propagation
- How goal language appears in task descriptions
- Goal terminology in step definitions
- Phrasing patterns in agent thinking/reasoning
- Language consistency across SPEC artefacts
- Conceptual drift from goal to implementation

### Dimension 3: Constitutional Compliance
- Article I-XIV adherence scoring
- Critical flag balance (target: 40-60%)
- Backup method quality assessment
- Bridging quality (Markdown-TOML sync)
- Validation checkpoint outcomes

### Dimension 4: Execution Performance
- Step success/failure rates
- Backup invocation frequency
- Mode escalation patterns
- Error propagation effectiveness
- Retry patterns and exhaustion

### Dimension 5: Agent Behaviour Correlation
- Thinking patterns vs goal complexity
- Decision quality vs goal clarity
- Output quality vs goal specificity
- Backup selection vs goal ambiguity
- Escalation triggers vs goal characteristics

### Dimension 6: Per-Task/Step Behaviour
- Task decomposition quality
- Step atomicity assessment
- Critical flag appropriateness
- Expected output clarity
- Method selection rationale

### Dimension 7: Error Analysis
- Error types and frequencies
- Root cause patterns
- Recovery effectiveness
- Constitutional violations
- Preventable vs inherent errors

### Dimension 8: Outcome Metrics
- Goal achievement status (ACHIEVED/PARTIAL/NOT_ACHIEVED)
- Deliverable completeness
- Quality standards met
- Time/step efficiency
- Comparison to expected outcomes

---

## Task [0]: Initialize Analysis and Gather Project Metadata

**TOML Reference:** `tasks[id=0]` in parameters_Dev_Analysis.toml  
**Purpose:** Locate project folder, scan structure, and collect comprehensive metadata

- **Step [0]:** Receive project folder location (ONLY USER INPUT REQUIRED)
  - **Primary method:** Prompt for project development folder path
  - **Expected output:** Absolute path to project folder
  - **Critical:** true
  - **Mode:** collaborative (ONE TIME ONLY - for folder path input)

- **Step [1]:** Scan and map complete project structure
  - **Primary method:** Recursively list all files and directories in project folder
  - **Backup [1]:** If permissions issue, request accessible subset of project
  - **Expected output:** Complete file tree with full paths
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count and categorise all files
  - **Primary method:** Count files by type: .md, .toml, .json, .py, .js, .ts, .log, .txt, etc.
  - **Expected output:** File count table with breakdown by extension
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Calculate file sizes and total project size
  - **Primary method:** Get file size for each file, sum by category and total
  - **Expected output:** Size metrics table (bytes, KB, MB) by file type and total
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Extract all timestamps
  - **Primary method:** Collect creation, modification, access times for all relevant files
  - **Backup [1]:** If timestamps unavailable, use git history if present
  - **Expected output:** Timeline table showing project chronology
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Calculate development duration
  - **Primary method:** Calculate time from earliest to latest timestamp, identify development phases
  - **Expected output:** Development duration metrics: total time, active development periods, gaps
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Count tokens across all text files
  - **Primary method:** For each text-based file, count tokens (words, characters, estimated LLM tokens)
  - **Backup [1]:** If token counting unavailable, use word/character counts as proxy
  - **Expected output:** Token count table by file type with totals
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Identify and catalogue error logs
  - **Primary method:** Locate all error log files, count error entries, categorise by severity
  - **Expected output:** Error log inventory with counts and locations
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Identify and catalogue chat/conversation logs
  - **Primary method:** Locate chat transcripts, conversation logs, agent thinking logs
  - **Backup [1]:** Check common locations: root, logs folder, subdirectories
  - **Expected output:** Conversation log inventory with file paths and sizes
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Count conversation turns and messages
  - **Primary method:** Parse chat logs to count: total messages, user messages, agent messages, turns
  - **Expected output:** Conversation metrics table
  - **Critical:** false
  - **Mode:** silent

- **Step [10]:** Identify SPEC files and versions
  - **Primary method:** Locate all spec_*.md, parameters_*.toml, exe_*.md, progress_*.json files
  - **Expected output:** SPEC file inventory with versions and timestamps
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Create project metadata snapshot
  - **Primary method:** Aggregate all collected metrics into comprehensive metadata document
  - **Expected output:** Project metadata JSON with all metrics organized
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Project folder scanned, all files catalogued, comprehensive metrics collected
- **Logging:** Record all metadata in progress_Dev_Analysis.json for reference throughout analysis

---

## Task [1]: Extract and Characterise Initial Goal Text

**TOML Reference:** `tasks[id=1]` in parameters_Dev_Analysis.toml  
**Purpose:** Establish baseline characteristics of the goal that initiated SPEC development

- **Step [1]:** Locate and extract initial goal text
  - **Primary method:** Read SPEC markdown file Goal section and chat history for original user goal statement
  - **Backup [1]:** If chat history unavailable, use goal section from spec_[descriptor].md as proxy
  - **Expected output:** Exact goal text with source citation and timestamp
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Calculate quantitative text characteristics
  - **Primary method:** Compute word count, character count, sentence count, avg sentence length, Flesch-Kincaid score
  - **Backup [1]:** If automated scoring unavailable, perform manual classification (simple/moderate/complex)
  - **Expected output:** Table with numerical metrics and complexity classification
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Identify distinct elements and requirements
  - **Primary method:** Parse goal for discrete requirements, constraints, deliverables, success criteria
  - **Backup [1]:** Use linguistic chunking to identify conceptual units if structure unclear
  - **Expected output:** Numbered list of distinct elements (target: 3-10 elements)
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess technical specificity and domain familiarity
  - **Primary method:** Identify technical terms, domain-specific language, assumed knowledge, explicit vs implicit requirements
  - **Backup [1]:** Compare vocabulary against common vs specialised term databases
  - **Expected output:** Technical specificity score (1-5 scale) with justification and term examples
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Analyse formatting and structure
  - **Primary method:** Document use of lists, emphasis, sections, explicit vs narrative format
  - **Expected output:** Formatting assessment noting structural elements present
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All goal characteristics documented with quantitative metrics where possible
- **Logging:** Record all measurements in progress_Dev_Analysis.json for correlation analysis

---

## Task [2]: Map Goal Text Propagation Throughout Project

**TOML Reference:** `tasks[id=2]` in parameters_Dev_Analysis.toml  
**Purpose:** Track how initial goal language and concepts propagate through SPEC artefacts

- **Step [1]:** Extract task descriptions from SPEC
  - **Primary method:** Parse spec_[descriptor].md for all task titles and descriptions
  - **Expected output:** List of tasks with full text
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify goal language in task descriptions
  - **Primary method:** Compare task descriptions to goal text, noting shared terminology, conceptual overlap, verbatim phrases
  - **Backup [1]:** Use semantic similarity scoring if direct comparison insufficient
  - **Expected output:** Table mapping goal terms to task descriptions with similarity scores
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Extract step definitions and analyse propagation
  - **Primary method:** Parse all step descriptions, identify goal/task terminology presence, track conceptual consistency
  - **Backup [1]:** Focus on critical steps only if volume is high (>20 steps)
  - **Expected output:** Propagation matrix showing goal→task→step language flow with specific examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse agent thinking and reasoning patterns
  - **Primary method:** Review chat history/logs for agent internal reasoning, note how goal concepts appear in thinking
  - **Backup [1]:** If full chat unavailable, analyse progress.json logs for method justifications
  - **Expected output:** Minimum 3 specific examples of goal text influencing agent reasoning with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify conceptual drift
  - **Primary method:** Compare final implementation/outputs against original goal, identify divergences in terminology, scope, or interpretation
  - **Expected output:** Conceptual drift assessment noting where implementation departed from goal language
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Assess language consistency across artefacts
  - **Primary method:** Check terminology consistency across spec.md, parameters.toml, progress.json, deliverables
  - **Expected output:** Consistency report identifying where language fragmented or evolved
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Minimum 3 concrete examples of goal text propagation documented with direct quotes
- **Logging:** Record propagation patterns and drift instances in progress_Dev_Analysis.json

---

## Task [3]: Evaluate Constitutional Compliance

**TOML Reference:** `tasks[id=3]` in parameters_Dev_Analysis.toml  
**Purpose:** Assess adherence to SPEC Engine Constitution (Articles I-XIV)

- **Step [1]:** Validate Article I compliance (North Star Principle)
  - **Primary method:** Verify goal singularity, clarity, measurability, explicitness
  - **Expected output:** Article I compliance score (pass/fail) with justification
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Validate Article II compliance (Hierarchical Structure)
  - **Primary method:** Count tasks (target: 2-5), count steps per task (target: 1-5), verify hierarchy maintained
  - **Backup [1]:** If counts borderline, assess whether structure serves goal effectively
  - **Expected output:** Article II compliance score with quantitative counts
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Validate Article III compliance (Dual-File Mandate)
  - **Primary method:** Cross-check spec.md and parameters.toml for ID matching, structure sync, cross-references
  - **Expected output:** Article III compliance score noting any bridging failures
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Validate Article VI compliance (Critical Flag Discipline)
  - **Primary method:** Calculate critical step percentage (target: 40-60%), assess appropriateness of critical flags
  - **Expected output:** Critical balance percentage and appropriateness assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Validate Article VII compliance (Backup Methods)
  - **Primary method:** Review all backup methods to ensure they are alternative reasoning paths, not retries
  - **Backup [1]:** Sample backup methods if total exceeds 15
  - **Expected output:** Backup quality score with examples of good/poor backups
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Check Article XIV compliance (if build goal)
  - **Primary method:** If goal contains build/create/system keywords, verify software stack defined, deployment criteria present
  - **Expected output:** Article XIV compliance (N/A or pass/fail with details)
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Review Articles IV, VIII, IX, X compliance from execution
  - **Primary method:** Analyse progress.json for validation execution, error propagation, mode discipline, comprehensive logging
  - **Expected output:** Compliance scores for Articles IV, VIII, IX, X with evidence from logs
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Calculate overall constitutional compliance score
  - **Primary method:** Aggregate individual article scores, weight by severity, generate 0-100 score
  - **Expected output:** Overall compliance score (0-100) with breakdown by article
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All applicable articles assessed with evidence-based scoring
- **Logging:** Record compliance scores and violations in progress_Dev_Analysis.json

---

## Task [4]: Analyse Execution Performance Metrics

**TOML Reference:** `tasks[id=4]` in parameters_Dev_Analysis.toml  
**Purpose:** Extract quantitative performance data from execution logs

- **Step [1]:** Parse progress.json for step outcomes
  - **Primary method:** Read progress_[descriptor].json, extract all step entries with status, method_used, retry_count
  - **Backup [1]:** If progress.json malformed, reconstruct from available logs
  - **Expected output:** Complete step outcome dataset with counts for success/failure/retry
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Calculate success and failure rates
  - **Primary method:** Compute: total steps, successful steps, failed steps, overall success rate, failure rate
  - **Expected output:** Success/failure metrics table with percentages
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Analyse backup method usage
  - **Primary method:** Count primary method uses, backup[1] uses, backup[2] uses, calculate backup invocation rate
  - **Expected output:** Backup usage statistics showing frequency and success rates per backup type
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Track mode escalations
  - **Primary method:** Identify all mode switches in progress.json, categorise escalation triggers
  - **Expected output:** Mode escalation count, trigger categorisation, escalation appropriateness assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Assess error propagation effectiveness
  - **Primary method:** Identify steps with dependencies, check if prior failures were read from progress.json, assess propagation handling
  - **Backup [1]:** If error propagation tracking sparse, infer from step sequence and outcomes
  - **Expected output:** Error propagation effectiveness score with examples
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Analyse retry patterns
  - **Primary method:** Extract retry_count per step, identify retry exhaustion cases, assess thoroughness
  - **Expected output:** Retry pattern analysis showing exhaustion rate and thoroughness score
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Calculate efficiency metrics
  - **Primary method:** Compute total steps attempted, steps per task, time per step (if timestamps available)
  - **Expected output:** Efficiency metrics table
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All quantitative metrics calculated with source data citations
- **Logging:** Record all performance metrics in progress_Dev_Analysis.json

---

## Task [5]: Correlate Agent Behaviour with Goal Characteristics

**TOML Reference:** `tasks[id=5]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify relationships between goal text properties and agent execution behaviour

- **Step [1]:** Establish correlation framework
  - **Primary method:** Define metrics for correlation: goal complexity vs task count, goal clarity vs error rate, goal specificity vs backup usage
  - **Expected output:** Correlation matrix framework listing goal characteristics and behaviour metrics
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Analyse goal complexity vs task decomposition
  - **Primary method:** Correlate goal complexity score (from Task 1) with number of tasks, steps per task, decomposition depth
  - **Backup [1]:** Use qualitative assessment if quantitative correlation weak
  - **Expected output:** Correlation finding: does complex goal lead to more/fewer tasks?
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Analyse goal clarity vs execution accuracy
  - **Primary method:** Correlate goal clarity indicators (explicit requirements, measurable criteria) with success rate, error rate
  - **Expected output:** Correlation finding: does clear goal reduce errors?
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse goal specificity vs backup usage
  - **Primary method:** Correlate technical specificity score with backup invocation rate, backup effectiveness
  - **Expected output:** Correlation finding: does vague goal increase backup reliance?
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Analyse goal formatting vs agent thinking patterns
  - **Primary method:** Review agent reasoning for structured vs narrative goals, assess thinking clarity and organisation
  - **Backup [1]:** If thinking logs sparse, assess output organisation as proxy
  - **Expected output:** Qualitative finding on formatting impact with examples
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Identify confounding factors
  - **Primary method:** Check for external factors affecting correlation: SPEC complexity, domain difficulty, resource availability
  - **Expected output:** List of confounding factors that may explain behaviour patterns
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Distinguish correlation from causation
  - **Primary method:** For each correlation found, assess whether relationship is causal, coincidental, or mediated by other factors
  - **Expected output:** Causality assessment for each correlation with confidence level
  - **Critical:** false
  - **Mode:** collaborative (human judgment needed for causality claims)

- **Verification:** Minimum 3 behaviour correlations identified with specific evidence
- **Logging:** Record correlations and causality assessments in progress_Dev_Analysis.json

---

## Task [6]: Assess Per-Task and Per-Step Behaviour Quality

**TOML Reference:** `tasks[id=6]` in parameters_Dev_Analysis.toml  
**Purpose:** Evaluate quality of task decomposition and step execution at granular level

- **Step [1]:** Evaluate task decomposition quality
  - **Primary method:** For each task, assess: Does task serve goal? Is task scope appropriate? Is task self-contained?
  - **Expected output:** Task quality assessment table with scores and rationale per task
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Assess step atomicity
  - **Primary method:** For each step, assess: Is step a single concrete action? Is step scope too broad/narrow? Is step executable?
  - **Backup [1]:** Sample steps if total exceeds 20
  - **Expected output:** Step atomicity assessment with examples of well/poorly scoped steps
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Evaluate critical flag appropriateness
  - **Primary method:** For each critical step, verify: Would failure truly block goal? For non-critical, verify: Can goal succeed without this?
  - **Expected output:** Critical flag appropriateness score with misclassification examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess expected output clarity
  - **Primary method:** For each step, rate expected output: specific/vague, measurable/subjective, achievable/unrealistic
  - **Expected output:** Expected output quality assessment with clarity distribution
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Evaluate method selection rationale
  - **Primary method:** For steps with multiple methods, assess whether primary/backup choices were well-justified
  - **Expected output:** Method selection quality score with examples
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All tasks and representative sample of steps assessed for quality
- **Logging:** Record quality assessments in progress_Dev_Analysis.json

---

## Task [7]: Conduct Error Analysis and Pattern Detection

**TOML Reference:** `tasks[id=7]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify error patterns, root causes, and improvement opportunities

- **Step [1]:** Categorise all errors by type
  - **Primary method:** Extract all failures from progress.json, categorise: validation errors, execution errors, resource errors, logic errors
  - **Expected output:** Error categorisation table with counts and percentages
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify error frequency patterns
  - **Primary method:** Analyse which tasks/steps had highest error rates, identify repeated failures
  - **Expected output:** Error hotspot analysis showing concentration areas
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Conduct root cause analysis
  - **Primary method:** For each error category, trace to root cause: SPEC design issue, execution issue, resource limitation, goal ambiguity
  - **Backup [1]:** Focus on top 5 most frequent errors if volume high
  - **Expected output:** Root cause mapping with prevention recommendations
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess recovery effectiveness
  - **Primary method:** For each error, check if backup methods resolved issue, assess recovery time, evaluate escalation appropriateness
  - **Expected output:** Recovery effectiveness score with successful/unsuccessful recovery examples
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify constitutional violations
  - **Primary method:** Check progress.json for constitutional_compliance section, extract all violations with severity
  - **Backup [1]:** Manual review of logs if compliance tracking absent
  - **Expected output:** Constitutional violation summary with article breakdown
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Distinguish preventable from inherent errors
  - **Primary method:** Classify each error: preventable through better SPEC design, inherent to task complexity, external/environmental
  - **Expected output:** Error preventability classification with improvement focus areas
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All errors analysed with root causes identified
- **Logging:** Record error analysis findings in progress_Dev_Analysis.json

---

## Task [8]: Generate Comprehensive Analysis Report with Recommendations

**TOML Reference:** `tasks[id=8]` in parameters_Dev_Analysis.toml  
**Purpose:** Synthesise all findings into actionable report

- **Step [1]:** Structure report outline
  - **Primary method:** Create report sections: Executive Summary, Goal Analysis, Propagation Findings, Performance Metrics, Correlations, Quality Assessment, Error Analysis, Recommendations
  - **Expected output:** Report outline with section headers
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Write Executive Summary
  - **Primary method:** Synthesise key findings: goal characteristics summary, main propagation patterns, overall performance, critical insights
  - **Expected output:** 200-300 word executive summary highlighting main findings
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Compile Goal Text Analysis section
  - **Primary method:** Aggregate Task 1 findings: goal characteristics table, complexity assessment, element breakdown
  - **Expected output:** Goal Text Analysis section with all metrics and assessments
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Compile Goal Text Propagation section
  - **Primary method:** Aggregate Task 2 findings: propagation examples, language flow diagram, conceptual drift assessment
  - **Expected output:** Goal Text Propagation section with minimum 3 concrete examples with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Compile Constitutional Compliance section
  - **Primary method:** Aggregate Task 3 findings: article-by-article scores, overall compliance score, violation summary
  - **Expected output:** Constitutional Compliance section with compliance scorecard
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Compile Execution Performance section
  - **Primary method:** Aggregate Task 4 findings: success/failure rates, backup usage, mode escalations, efficiency metrics
  - **Expected output:** Execution Performance section with metrics tables
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Compile Behaviour Correlation section
  - **Primary method:** Aggregate Task 5 findings: correlation matrix, causality assessments, confounding factors
  - **Expected output:** Behaviour Correlation section with correlation findings
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Compile Quality Assessment section
  - **Primary method:** Aggregate Task 6 findings: task quality scores, step atomicity, critical flag appropriateness
  - **Expected output:** Quality Assessment section with quality distributions
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Compile Error Analysis section
  - **Primary method:** Aggregate Task 7 findings: error categories, root causes, recovery effectiveness, preventability
  - **Expected output:** Error Analysis section with error breakdown and patterns
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Generate actionable recommendations
  - **Primary method:** Based on all findings, create specific recommendations for: goal formulation improvement, SPEC design enhancement, execution optimisation, constitutional compliance
  - **Backup [1]:** If recommendations unclear, escalate to collaborative mode for human input
  - **Expected output:** Minimum 5 specific, actionable recommendations linked to findings
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Add cross-project comparison framework (if applicable)
  - **Primary method:** If analysing multiple SPECs, create comparison tables for key metrics across projects
  - **Expected output:** Cross-project comparison section (optional, only if multiple projects analysed)
  - **Critical:** false
  - **Mode:** silent

- **Step [12]:** Finalise report formatting and references
  - **Primary method:** Ensure all sections formatted consistently, add table of contents, verify all data citations present
  - **Expected output:** Complete, polished analysis report in markdown format
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Report contains all required sections, metrics are evidence-based, recommendations are actionable
- **Logging:** Record report completion in progress_Dev_Analysis.json with final deliverable path

---

## Bridging: Markdown ↔ TOML Synchronisation

This spec file (Dev_Analysis_SPEC.md) must maintain perfect alignment with its companion file (parameters_Dev_Analysis.toml).

**Bridging Requirements:**
1. Each task in this file must have corresponding `[[tasks]]` entry in TOML with matching ID (1-8)
2. Each step within a task must have corresponding `[[tasks.steps]]` entry with matching ID
3. Expected outputs in this file must match `expected_output` fields in TOML
4. Critical flags must be synchronised between files
5. Constraints referenced must exist in TOML `[constraints]` section

**Example Cross-References:**
- "See `constraints.min_examples_required` in parameters_Dev_Analysis.toml" (Task 2, Step 4)
- "As defined in `tasks[id=4]` in TOML" (Task 4 reference)
- "Must satisfy TOML verification requirements" (All task verifications)

The exe_Dev_Analysis.md controller will validate this synchronisation during initialisation (Section 1.8).

---

## Instructions for LLM Executor

1. **Start with goal understanding**: This analysis examines how goal text propagates and influences SPEC development
2. **Execute tasks sequentially**: Tasks 1-2 gather data, Tasks 3-7 analyse patterns, Task 8 synthesises findings
3. **Maintain objectivity**: Base all findings on evidence from files, logs, and artefacts
4. **Track propagation carefully**: Pay special attention to how exact goal language appears throughout project
5. **Quantify where possible**: Use numerical metrics rather than subjective assessments when feasible
6. **Distinguish correlation from causation**: Note relationships but assess causality carefully
7. **Document thoroughly**: Log all findings in progress_Dev_Analysis.json for traceability
8. **Focus on actionability**: Recommendations should be specific and implementable
9. **Read prior outcomes**: Before each step, check progress.json for relevant prior findings
10. **Escalate appropriately**: Use collaborative mode for causality judgements and unclear recommendation priorities

---

## Expected Analysis Output Structure

The final report should follow this structure:

```markdown
# SPEC Development Analysis Report

## Executive Summary
[200-300 word overview of key findings]

## 1. Goal Text Analysis
### 1.1 Initial Goal Characteristics
- Quantitative metrics table
- Complexity classification
- Element breakdown

### 1.2 Technical Specificity Assessment
- Specificity score with justification
- Domain terminology analysis

## 2. Goal Text Propagation Analysis
### 2.1 Propagation Through Tasks
- Task-level language mapping
- Specific examples with quotes

### 2.2 Propagation Through Steps
- Step-level language mapping
- Propagation matrix

### 2.3 Agent Thinking Patterns
- Minimum 3 examples of goal text in reasoning
- Direct quotes from logs/chat

### 2.4 Conceptual Drift Assessment
- Identified divergences
- Impact analysis

## 3. Constitutional Compliance Assessment
### 3.1 Article-by-Article Scores
- Individual article compliance
- Evidence for each assessment

### 3.2 Overall Compliance Score
- Aggregate score (0-100)
- Violation summary

## 4. Execution Performance Metrics
### 4.1 Success and Failure Rates
- Quantitative metrics table
- Rate comparisons

### 4.2 Backup Method Usage
- Usage statistics
- Effectiveness assessment

### 4.3 Mode Escalations
- Escalation count and triggers
- Appropriateness evaluation

### 4.4 Efficiency Metrics
- Steps per task
- Time analysis (if available)

## 5. Behaviour Correlation Analysis
### 5.1 Identified Correlations
- Goal characteristics vs execution behaviour
- Correlation strength assessment

### 5.2 Causality Assessment
- Causal vs correlational relationships
- Confidence levels

### 5.3 Confounding Factors
- External influences
- Mediation effects

## 6. Quality Assessment
### 6.1 Task Decomposition Quality
- Per-task quality scores
- Decomposition effectiveness

### 6.2 Step Quality Analysis
- Atomicity assessment
- Critical flag appropriateness

### 6.3 Method Selection Quality
- Primary/backup rationale
- Method effectiveness

## 7. Error Analysis
### 7.1 Error Categorisation
- Error type distribution
- Frequency patterns

### 7.2 Root Cause Analysis
- Root cause mapping
- Prevention opportunities

### 7.3 Recovery Effectiveness
- Recovery success rates
- Backup effectiveness

### 7.4 Constitutional Violations
- Violation breakdown by article
- Severity assessment

## 8. Recommendations
### 8.1 Goal Formulation Improvements
[Specific, actionable recommendations]

### 8.2 SPEC Design Enhancements
[Specific, actionable recommendations]

### 8.3 Execution Optimisation
[Specific, actionable recommendations]

### 8.4 Constitutional Compliance
[Specific, actionable recommendations]

### 8.5 Future Research Directions
[Areas for deeper investigation]

## Appendices
### A. Raw Data Tables
### B. Propagation Examples (Full Quotes)
### C. Metrics Calculation Methods
### D. Source Citations
```

---

**End of Dev_Analysis_SPEC.md**

This SPEC is designed to be reusable across multiple test SPEC analyses, enabling systematic comparison and pattern identification.


```

```markdown
# Dev Analysis SPEC

**Version:** 1.0  
**Last Updated:** 2025-11-03  
**Purpose:** Analyse development of test SPECs to identify patterns, metrics, and goal text propagation effects

---

## Goal

Perform comprehensive analysis of a test SPEC's development lifecycle to identify how initial goal text propagates through the system and impacts agent behaviour, execution accuracy, and project outcomes.

---

## Software Stack & Architecture

**Not Applicable** - This is an analysis task, not a build goal.

---

## Definition of Complete

What must exist and be verified:
- [ ] **Primary deliverable:** Comprehensive analysis report (markdown format) covering all analysis areas
- [ ] **Quality standards met:** 
  - All 8 analysis tasks completed with documented findings
  - Goal text propagation patterns identified with specific examples
  - Quantitative metrics calculated for execution performance
  - Cross-correlation analysis between goal characteristics and outcomes
  - Recommendations provided based on findings
- [ ] **Verification method:** 
  - Report contains all required sections (see tasks below)
  - Quantitative metrics include numerical values with source citations
  - At least 3 specific examples of goal text propagation documented
  - Recommendations are actionable and linked to specific findings

---

## Definitions

- **goal**: Analyse how initial goal text characteristics influence SPEC development and execution
- **task[n]**: Discrete analysis objectives examining different aspects of SPEC development
- **step[m]**: Concrete analytical actions within each task
- **backup[p]**: Alternative analysis methods when primary approach is blocked
- **critical_flag**: Boolean indicating whether analysis step is essential to overall goal
- **mode**: `silent` (fully autonomous - NO USER INPUT REQUIRED except initial project folder location)
- **progress.json**: Structured log tracking analysis execution and findings
- **project_folder**: Target development project folder path (ONLY required user input)

---

## Components

Analysis requires access to:
- **Test SPEC files:** spec_[descriptor].md, parameters_[descriptor].toml, exe_[descriptor].md
- **Execution logs:** progress_[descriptor].json
- **Project artefacts:** Code files, documentation, error logs, validation reports
- **Chat history:** Conversation transcripts showing agent thinking and decision-making
- **Constitution:** __SPEC_Engine/_Constitution/constitution.md for compliance checking

**Machine-Readable Components:**  
See `[components]` section in parameters_Dev_Analysis.toml

---

## Constraints

- Analysis must be objective and evidence-based
- All metrics must be traceable to source data
- Goal text propagation analysis must include minimum 3 concrete examples
- Quantitative metrics must include: success rates, error rates, mode escalations, backup usage
- Findings must distinguish correlation from causation
- Recommendations must be specific and actionable

**Machine-Readable Constraints:**  
See `[constraints]` section in parameters_Dev_Analysis.toml:
- `min_examples_required = 3` (goal text propagation examples)
- `metrics_evidence_based = true` (all metrics must cite sources)
- `recommendation_specificity = "actionable"` (recommendations must be implementable)

---

## User Stories

- As a **SPEC developer**, I want to understand how goal phrasing impacts development so I can write more effective goals
- As a **system architect**, I want to identify patterns in SPEC execution so I can improve the framework
- As a **researcher**, I want to quantify goal text propagation so I can understand agent behaviour correlation
- As a **project manager**, I want metrics on SPEC performance so I can assess project quality

---

## Analysis Framework

This SPEC analyses development across 8 integrated dimensions:

### Dimension 1: Goal Text Characteristics
- Length (word count, character count, sentence complexity)
- Number of distinct elements/requirements
- Literacy level (Flesch-Kincaid, technical density)
- Formatting (structure, lists, emphasis)
- Familiarity/Technical specificity

### Dimension 2: Goal Text Propagation
- How goal language appears in task descriptions
- Goal terminology in step definitions
- Phrasing patterns in agent thinking/reasoning
- Language consistency across SPEC artefacts
- Conceptual drift from goal to implementation

### Dimension 3: Constitutional Compliance
- Article I-XIV adherence scoring
- Critical flag balance (target: 40-60%)
- Backup method quality assessment
- Bridging quality (Markdown-TOML sync)
- Validation checkpoint outcomes

### Dimension 4: Execution Performance
- Step success/failure rates
- Backup invocation frequency
- Mode escalation patterns
- Error propagation effectiveness
- Retry patterns and exhaustion

### Dimension 5: Agent Behaviour Correlation
- Thinking patterns vs goal complexity
- Decision quality vs goal clarity
- Output quality vs goal specificity
- Backup selection vs goal ambiguity
- Escalation triggers vs goal characteristics

### Dimension 6: Per-Task/Step Behaviour
- Task decomposition quality
- Step atomicity assessment
- Critical flag appropriateness
- Expected output clarity
- Method selection rationale

### Dimension 7: Error Analysis
- Error types and frequencies
- Root cause patterns
- Recovery effectiveness
- Constitutional violations
- Preventable vs inherent errors

### Dimension 8: Outcome Metrics
- Goal achievement status (ACHIEVED/PARTIAL/NOT_ACHIEVED)
- Deliverable completeness
- Quality standards met
- Time/step efficiency
- Comparison to expected outcomes

---

## Task [0]: Initialize Analysis and Gather Project Metadata

**TOML Reference:** `tasks[id=0]` in parameters_Dev_Analysis.toml  
**Purpose:** Locate project folder, scan structure, and collect comprehensive metadata

- **Step [0]:** Receive project folder location (ONLY USER INPUT REQUIRED)
  - **Primary method:** Prompt for project development folder path
  - **Expected output:** Absolute path to project folder
  - **Critical:** true
  - **Mode:** collaborative (ONE TIME ONLY - for folder path input)

- **Step [1]:** Scan and map complete project structure
  - **Primary method:** Recursively list all files and directories in project folder
  - **Backup [1]:** If permissions issue, request accessible subset of project
  - **Expected output:** Complete file tree with full paths
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count and categorise all files
  - **Primary method:** Count files by type: .md, .toml, .json, .py, .js, .ts, .log, .txt, etc.
  - **Expected output:** File count table with breakdown by extension
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Calculate file sizes and total project size
  - **Primary method:** Get file size for each file, sum by category and total
  - **Expected output:** Size metrics table (bytes, KB, MB) by file type and total
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Extract all timestamps
  - **Primary method:** Collect creation, modification, access times for all relevant files
  - **Backup [1]:** If timestamps unavailable, use git history if present
  - **Expected output:** Timeline table showing project chronology
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Calculate development duration
  - **Primary method:** Calculate time from earliest to latest timestamp, identify development phases
  - **Expected output:** Development duration metrics: total time, active development periods, gaps
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Count tokens across all text files
  - **Primary method:** For each text-based file, count tokens (words, characters, estimated LLM tokens)
  - **Backup [1]:** If token counting unavailable, use word/character counts as proxy
  - **Expected output:** Token count table by file type with totals
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Identify and catalogue error logs
  - **Primary method:** Locate all error log files, count error entries, categorise by severity
  - **Expected output:** Error log inventory with counts and locations
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Identify and catalogue chat/conversation logs
  - **Primary method:** Locate chat transcripts, conversation logs, agent thinking logs
  - **Backup [1]:** Check common locations: root, logs folder, subdirectories
  - **Expected output:** Conversation log inventory with file paths and sizes
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Count conversation turns and messages
  - **Primary method:** Parse chat logs to count: total messages, user messages, agent messages, turns
  - **Expected output:** Conversation metrics table
  - **Critical:** false
  - **Mode:** silent

- **Step [10]:** Identify SPEC files and versions
  - **Primary method:** Locate all spec_*.md, parameters_*.toml, exe_*.md, progress_*.json files
  - **Expected output:** SPEC file inventory with versions and timestamps
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Create project metadata snapshot
  - **Primary method:** Aggregate all collected metrics into comprehensive metadata document
  - **Expected output:** Project metadata JSON with all metrics organized
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Project folder scanned, all files catalogued, comprehensive metrics collected
- **Logging:** Record all metadata in progress_Dev_Analysis.json for reference throughout analysis

---

## Task [1]: Extract and Characterise Initial Goal Text

**TOML Reference:** `tasks[id=1]` in parameters_Dev_Analysis.toml  
**Purpose:** Establish baseline characteristics of the goal that initiated SPEC development

- **Step [1]:** Locate and extract initial goal text
  - **Primary method:** Read SPEC markdown file Goal section and chat history for original user goal statement
  - **Backup [1]:** If chat history unavailable, use goal section from spec_[descriptor].md as proxy
  - **Expected output:** Exact goal text with source citation and timestamp
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Calculate quantitative text characteristics
  - **Primary method:** Compute word count, character count, sentence count, avg sentence length, Flesch-Kincaid score
  - **Backup [1]:** If automated scoring unavailable, perform manual classification (simple/moderate/complex)
  - **Expected output:** Table with numerical metrics and complexity classification
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Identify distinct elements and requirements
  - **Primary method:** Parse goal for discrete requirements, constraints, deliverables, success criteria
  - **Backup [1]:** Use linguistic chunking to identify conceptual units if structure unclear
  - **Expected output:** Numbered list of distinct elements (target: 3-10 elements)
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess technical specificity and domain familiarity
  - **Primary method:** Identify technical terms, domain-specific language, assumed knowledge, explicit vs implicit requirements
  - **Backup [1]:** Compare vocabulary against common vs specialised term databases
  - **Expected output:** Technical specificity score (1-5 scale) with justification and term examples
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Analyse formatting and structure
  - **Primary method:** Document use of lists, emphasis, sections, explicit vs narrative format
  - **Expected output:** Formatting assessment noting structural elements present
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All goal characteristics documented with quantitative metrics where possible
- **Logging:** Record all measurements in progress_Dev_Analysis.json for correlation analysis

---

## Task [2]: Map Goal Text Propagation Throughout Project

**TOML Reference:** `tasks[id=2]` in parameters_Dev_Analysis.toml  
**Purpose:** Track how initial goal language and concepts propagate through SPEC artefacts

- **Step [1]:** Extract task descriptions from SPEC
  - **Primary method:** Parse spec_[descriptor].md for all task titles and descriptions
  - **Expected output:** List of tasks with full text
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify goal language in task descriptions
  - **Primary method:** Compare task descriptions to goal text, noting shared terminology, conceptual overlap, verbatim phrases
  - **Backup [1]:** Use semantic similarity scoring if direct comparison insufficient
  - **Expected output:** Table mapping goal terms to task descriptions with similarity scores
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Extract step definitions and analyse propagation
  - **Primary method:** Parse all step descriptions, identify goal/task terminology presence, track conceptual consistency
  - **Backup [1]:** Focus on critical steps only if volume is high (>20 steps)
  - **Expected output:** Propagation matrix showing goal→task→step language flow with specific examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse agent thinking and reasoning patterns
  - **Primary method:** Review chat history/logs for agent internal reasoning, note how goal concepts appear in thinking
  - **Backup [1]:** If full chat unavailable, analyse progress.json logs for method justifications
  - **Expected output:** Minimum 3 specific examples of goal text influencing agent reasoning with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify conceptual drift
  - **Primary method:** Compare final implementation/outputs against original goal, identify divergences in terminology, scope, or interpretation
  - **Expected output:** Conceptual drift assessment noting where implementation departed from goal language
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Assess language consistency across artefacts
  - **Primary method:** Check terminology consistency across spec.md, parameters.toml, progress.json, deliverables
  - **Expected output:** Consistency report identifying where language fragmented or evolved
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Minimum 3 concrete examples of goal text propagation documented with direct quotes
- **Logging:** Record propagation patterns and drift instances in progress_Dev_Analysis.json

---

## Task [3]: Evaluate Constitutional Compliance

**TOML Reference:** `tasks[id=3]` in parameters_Dev_Analysis.toml  
**Purpose:** Assess adherence to SPEC Engine Constitution (Articles I-XIV)

- **Step [1]:** Validate Article I compliance (North Star Principle)
  - **Primary method:** Verify goal singularity, clarity, measurability, explicitness
  - **Expected output:** Article I compliance score (pass/fail) with justification
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Validate Article II compliance (Hierarchical Structure)
  - **Primary method:** Count tasks (target: 2-5), count steps per task (target: 1-5), verify hierarchy maintained
  - **Backup [1]:** If counts borderline, assess whether structure serves goal effectively
  - **Expected output:** Article II compliance score with quantitative counts
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Validate Article III compliance (Dual-File Mandate)
  - **Primary method:** Cross-check spec.md and parameters.toml for ID matching, structure sync, cross-references
  - **Expected output:** Article III compliance score noting any bridging failures
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Validate Article VI compliance (Critical Flag Discipline)
  - **Primary method:** Calculate critical step percentage (target: 40-60%), assess appropriateness of critical flags
  - **Expected output:** Critical balance percentage and appropriateness assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Validate Article VII compliance (Backup Methods)
  - **Primary method:** Review all backup methods to ensure they are alternative reasoning paths, not retries
  - **Backup [1]:** Sample backup methods if total exceeds 15
  - **Expected output:** Backup quality score with examples of good/poor backups
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Check Article XIV compliance (if build goal)
  - **Primary method:** If goal contains build/create/system keywords, verify software stack defined, deployment criteria present
  - **Expected output:** Article XIV compliance (N/A or pass/fail with details)
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Review Articles IV, VIII, IX, X compliance from execution
  - **Primary method:** Analyse progress.json for validation execution, error propagation, mode discipline, comprehensive logging
  - **Expected output:** Compliance scores for Articles IV, VIII, IX, X with evidence from logs
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Calculate overall constitutional compliance score
  - **Primary method:** Aggregate individual article scores, weight by severity, generate 0-100 score
  - **Expected output:** Overall compliance score (0-100) with breakdown by article
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All applicable articles assessed with evidence-based scoring
- **Logging:** Record compliance scores and violations in progress_Dev_Analysis.json

---

## Task [4]: Analyse Execution Performance Metrics

**TOML Reference:** `tasks[id=4]` in parameters_Dev_Analysis.toml  
**Purpose:** Extract quantitative performance data from execution logs with comprehensive detail

- **Step [1]:** Parse progress.json for complete step data
  - **Primary method:** Read progress_[descriptor].json, extract ALL fields: task_id, step_id, status, method_used, retry_count, timestamp, mode, critical_flag, expected_output, actual_output, error_messages
  - **Backup [1]:** If progress.json malformed, reconstruct from available logs
  - **Expected output:** Complete step outcome dataset with full detail per step
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count total steps taken
  - **Primary method:** Count: total steps defined, total steps attempted, total steps completed, total steps skipped, total steps failed
  - **Expected output:** Comprehensive step count table with breakdown by status
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Calculate detailed success and failure rates
  - **Primary method:** Compute: overall success rate, failure rate, success rate by task, failure rate by task, first-attempt success rate, eventual success rate (after retries)
  - **Expected output:** Multi-level success/failure metrics table with percentages at step, task, and SPEC levels
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse backup method usage patterns
  - **Primary method:** Count: primary method attempts, primary successes, backup[1] attempts, backup[1] successes, backup[2] attempts, backup[2] successes, calculate success rates per method type
  - **Expected output:** Comprehensive backup usage statistics with success rates, effectiveness scores, and usage frequency distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Track mode usage and escalations
  - **Primary method:** Count: steps in silent mode, steps in collaborative mode, mode switches, categorise escalation triggers (consecutive failures, backup depletion, critical failure, confidence degradation)
  - **Expected output:** Mode usage table, escalation count by trigger type, escalation appropriateness assessment per instance
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Analyse timestamps and time metrics
  - **Primary method:** Extract all timestamps from progress.json, calculate: time per step, time per task, total execution time, longest steps, shortest steps, time distribution
  - **Backup [1]:** If timestamps sparse, use available data and note gaps
  - **Expected output:** Comprehensive time metrics table with duration statistics
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Assess error propagation effectiveness
  - **Primary method:** Identify all steps with dependencies, check if prior failures were read from progress.json, assess propagation handling quality, count propagation decisions
  - **Backup [1]:** If error propagation tracking sparse, infer from step sequence and outcomes
  - **Expected output:** Error propagation effectiveness score with example instances and propagation decision breakdown
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Analyse retry patterns in detail
  - **Primary method:** Extract retry_count per step, calculate: average retries per step, max retries reached, retry exhaustion rate, retry success rate, thoroughness score (methods exhausted before escalation)
  - **Expected output:** Detailed retry pattern analysis with distribution charts and exhaustion assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Calculate efficiency and productivity metrics
  - **Primary method:** Compute: total steps attempted vs planned, steps per task (actual vs expected), average time per step, steps per hour, rework rate (retries/total), productivity score
  - **Expected output:** Comprehensive efficiency metrics table with productivity indicators
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Analyse critical vs non-critical step performance
  - **Primary method:** Separate critical and non-critical steps, compare: success rates, retry rates, time per step, failure impact
  - **Expected output:** Critical flag performance comparison table
  - **Critical:** false
  - **Mode:** silent

- **Step [11]:** Extract and analyse expected vs actual outputs
  - **Primary method:** For each step, compare expected_output defined in SPEC to actual_output logged, categorise: exact match, partial match, mismatch, missing
  - **Expected output:** Output quality assessment with match rate and mismatch analysis
  - **Critical:** true
  - **Mode:** silent

- **Step [12]:** Count and categorise all errors encountered
  - **Primary method:** Extract all error messages from progress.json, categorise by type (validation, execution, resource, logic), count occurrences, identify most frequent errors
  - **Expected output:** Error frequency table by category with top 10 most common errors
  - **Critical:** true
  - **Mode:** silent

- **Step [13]:** Analyse token usage per step (if available)
  - **Primary method:** If token counts logged, extract tokens per step, calculate: tokens per task, total tokens, token efficiency (tokens per successful step)
  - **Backup [1]:** If not logged in progress.json, skip with note
  - **Expected output:** Token usage metrics table (if data available)
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All quantitative metrics calculated with source data citations, minimum 13 metric categories documented
- **Logging:** Record all performance metrics in progress_Dev_Analysis.json

---

## Task [5]: Correlate Agent Behaviour with Goal Characteristics

**TOML Reference:** `tasks[id=5]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify relationships between goal text properties and agent execution behaviour

- **Step [1]:** Establish correlation framework
  - **Primary method:** Define metrics for correlation: goal complexity vs task count, goal clarity vs error rate, goal specificity vs backup usage
  - **Expected output:** Correlation matrix framework listing goal characteristics and behaviour metrics
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Analyse goal complexity vs task decomposition
  - **Primary method:** Correlate goal complexity score (from Task 1) with number of tasks, steps per task, decomposition depth
  - **Backup [1]:** Use qualitative assessment if quantitative correlation weak
  - **Expected output:** Correlation finding: does complex goal lead to more/fewer tasks?
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Analyse goal clarity vs execution accuracy
  - **Primary method:** Correlate goal clarity indicators (explicit requirements, measurable criteria) with success rate, error rate
  - **Expected output:** Correlation finding: does clear goal reduce errors?
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse goal specificity vs backup usage
  - **Primary method:** Correlate technical specificity score with backup invocation rate, backup effectiveness
  - **Expected output:** Correlation finding: does vague goal increase backup reliance?
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Analyse goal formatting vs agent thinking patterns
  - **Primary method:** Review agent reasoning for structured vs narrative goals, assess thinking clarity and organisation
  - **Backup [1]:** If thinking logs sparse, assess output organisation as proxy
  - **Expected output:** Qualitative finding on formatting impact with examples
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Identify confounding factors
  - **Primary method:** Check for external factors affecting correlation: SPEC complexity, domain difficulty, resource availability
  - **Expected output:** List of confounding factors that may explain behaviour patterns
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Distinguish correlation from causation
  - **Primary method:** For each correlation found, assess whether relationship is causal, coincidental, or mediated by other factors
  - **Expected output:** Causality assessment for each correlation with confidence level
  - **Critical:** false
  - **Mode:** collaborative (human judgment needed for causality claims)

- **Verification:** Minimum 3 behaviour correlations identified with specific evidence
- **Logging:** Record correlations and causality assessments in progress_Dev_Analysis.json

---

## Task [6]: Assess Per-Task and Per-Step Behaviour Quality

**TOML Reference:** `tasks[id=6]` in parameters_Dev_Analysis.toml  
**Purpose:** Evaluate quality of task decomposition and step execution at granular level

- **Step [1]:** Evaluate task decomposition quality
  - **Primary method:** For each task, assess: Does task serve goal? Is task scope appropriate? Is task self-contained?
  - **Expected output:** Task quality assessment table with scores and rationale per task
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Assess step atomicity
  - **Primary method:** For each step, assess: Is step a single concrete action? Is step scope too broad/narrow? Is step executable?
  - **Backup [1]:** Sample steps if total exceeds 20
  - **Expected output:** Step atomicity assessment with examples of well/poorly scoped steps
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Evaluate critical flag appropriateness
  - **Primary method:** For each critical step, verify: Would failure truly block goal? For non-critical, verify: Can goal succeed without this?
  - **Expected output:** Critical flag appropriateness score with misclassification examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess expected output clarity
  - **Primary method:** For each step, rate expected output: specific/vague, measurable/subjective, achievable/unrealistic
  - **Expected output:** Expected output quality assessment with clarity distribution
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Evaluate method selection rationale
  - **Primary method:** For steps with multiple methods, assess whether primary/backup choices were well-justified
  - **Expected output:** Method selection quality score with examples
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All tasks and representative sample of steps assessed for quality
- **Logging:** Record quality assessments in progress_Dev_Analysis.json

---

## Task [7]: Conduct Error Analysis and Pattern Detection

**TOML Reference:** `tasks[id=7]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify error patterns, root causes, and improvement opportunities

- **Step [1]:** Categorise all errors by type
  - **Primary method:** Extract all failures from progress.json, categorise: validation errors, execution errors, resource errors, logic errors
  - **Expected output:** Error categorisation table with counts and percentages
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify error frequency patterns
  - **Primary method:** Analyse which tasks/steps had highest error rates, identify repeated failures
  - **Expected output:** Error hotspot analysis showing concentration areas
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Conduct root cause analysis
  - **Primary method:** For each error category, trace to root cause: SPEC design issue, execution issue, resource limitation, goal ambiguity
  - **Backup [1]:** Focus on top 5 most frequent errors if volume high
  - **Expected output:** Root cause mapping with prevention recommendations
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess recovery effectiveness
  - **Primary method:** For each error, check if backup methods resolved issue, assess recovery time, evaluate escalation appropriateness
  - **Expected output:** Recovery effectiveness score with successful/unsuccessful recovery examples
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify constitutional violations
  - **Primary method:** Check progress.json for constitutional_compliance section, extract all violations with severity
  - **Backup [1]:** Manual review of logs if compliance tracking absent
  - **Expected output:** Constitutional violation summary with article breakdown
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Distinguish preventable from inherent errors
  - **Primary method:** Classify each error: preventable through better SPEC design, inherent to task complexity, external/environmental
  - **Expected output:** Error preventability classification with improvement focus areas
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All errors analysed with root causes identified
- **Logging:** Record error analysis findings in progress_Dev_Analysis.json

---

## Task [8]: Generate Comprehensive Analysis Report with Recommendations

**TOML Reference:** `tasks[id=8]` in parameters_Dev_Analysis.toml  
**Purpose:** Synthesise all findings into actionable report

- **Step [1]:** Structure report outline
  - **Primary method:** Create report sections: Executive Summary, Goal Analysis, Propagation Findings, Performance Metrics, Correlations, Quality Assessment, Error Analysis, Recommendations
  - **Expected output:** Report outline with section headers
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Write Executive Summary
  - **Primary method:** Synthesise key findings: goal characteristics summary, main propagation patterns, overall performance, critical insights
  - **Expected output:** 200-300 word executive summary highlighting main findings
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Compile Goal Text Analysis section
  - **Primary method:** Aggregate Task 1 findings: goal characteristics table, complexity assessment, element breakdown
  - **Expected output:** Goal Text Analysis section with all metrics and assessments
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Compile Goal Text Propagation section
  - **Primary method:** Aggregate Task 2 findings: propagation examples, language flow diagram, conceptual drift assessment
  - **Expected output:** Goal Text Propagation section with minimum 3 concrete examples with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Compile Constitutional Compliance section
  - **Primary method:** Aggregate Task 3 findings: article-by-article scores, overall compliance score, violation summary
  - **Expected output:** Constitutional Compliance section with compliance scorecard
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Compile Execution Performance section
  - **Primary method:** Aggregate Task 4 findings: success/failure rates, backup usage, mode escalations, efficiency metrics
  - **Expected output:** Execution Performance section with metrics tables
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Compile Behaviour Correlation section
  - **Primary method:** Aggregate Task 5 findings: correlation matrix, causality assessments, confounding factors
  - **Expected output:** Behaviour Correlation section with correlation findings
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Compile Quality Assessment section
  - **Primary method:** Aggregate Task 6 findings: task quality scores, step atomicity, critical flag appropriateness
  - **Expected output:** Quality Assessment section with quality distributions
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Compile Error Analysis section
  - **Primary method:** Aggregate Task 7 findings: error categories, root causes, recovery effectiveness, preventability
  - **Expected output:** Error Analysis section with error breakdown and patterns
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Generate actionable recommendations
  - **Primary method:** Based on all findings, create specific recommendations for: goal formulation improvement, SPEC design enhancement, execution optimisation, constitutional compliance
  - **Backup [1]:** If recommendations unclear, escalate to collaborative mode for human input
  - **Expected output:** Minimum 5 specific, actionable recommendations linked to findings
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Add cross-project comparison framework (if applicable)
  - **Primary method:** If analysing multiple SPECs, create comparison tables for key metrics across projects
  - **Expected output:** Cross-project comparison section (optional, only if multiple projects analysed)
  - **Critical:** false
  - **Mode:** silent

- **Step [12]:** Finalise report formatting and references
  - **Primary method:** Ensure all sections formatted consistently, add table of contents, verify all data citations present
  - **Expected output:** Complete, polished analysis report in markdown format
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Report contains all required sections, metrics are evidence-based, recommendations are actionable
- **Logging:** Record report completion in progress_Dev_Analysis.json with final deliverable path

---

## Bridging: Markdown ↔ TOML Synchronisation

This spec file (Dev_Analysis_SPEC.md) must maintain perfect alignment with its companion file (parameters_Dev_Analysis.toml).

**Bridging Requirements:**
1. Each task in this file must have corresponding `[[tasks]]` entry in TOML with matching ID (1-8)
2. Each step within a task must have corresponding `[[tasks.steps]]` entry with matching ID
3. Expected outputs in this file must match `expected_output` fields in TOML
4. Critical flags must be synchronised between files
5. Constraints referenced must exist in TOML `[constraints]` section

**Example Cross-References:**
- "See `constraints.min_examples_required` in parameters_Dev_Analysis.toml" (Task 2, Step 4)
- "As defined in `tasks[id=4]` in TOML" (Task 4 reference)
- "Must satisfy TOML verification requirements" (All task verifications)

The exe_Dev_Analysis.md controller will validate this synchronisation during initialisation (Section 1.8).

---

## Instructions for LLM Executor

1. **Start with goal understanding**: This analysis examines how goal text propagates and influences SPEC development
2. **Execute tasks sequentially**: Tasks 1-2 gather data, Tasks 3-7 analyse patterns, Task 8 synthesises findings
3. **Maintain objectivity**: Base all findings on evidence from files, logs, and artefacts
4. **Track propagation carefully**: Pay special attention to how exact goal language appears throughout project
5. **Quantify where possible**: Use numerical metrics rather than subjective assessments when feasible
6. **Distinguish correlation from causation**: Note relationships but assess causality carefully
7. **Document thoroughly**: Log all findings in progress_Dev_Analysis.json for traceability
8. **Focus on actionability**: Recommendations should be specific and implementable
9. **Read prior outcomes**: Before each step, check progress.json for relevant prior findings
10. **Escalate appropriately**: Use collaborative mode for causality judgements and unclear recommendation priorities

---

## Expected Analysis Output Structure

The final report should follow this structure:

```markdown
# SPEC Development Analysis Report

## Executive Summary
[200-300 word overview of key findings]

## 1. Goal Text Analysis
### 1.1 Initial Goal Characteristics
- Quantitative metrics table
- Complexity classification
- Element breakdown

### 1.2 Technical Specificity Assessment
- Specificity score with justification
- Domain terminology analysis

## 2. Goal Text Propagation Analysis
### 2.1 Propagation Through Tasks
- Task-level language mapping
- Specific examples with quotes

### 2.2 Propagation Through Steps
- Step-level language mapping
- Propagation matrix

### 2.3 Agent Thinking Patterns
- Minimum 3 examples of goal text in reasoning
- Direct quotes from logs/chat

### 2.4 Conceptual Drift Assessment
- Identified divergences
- Impact analysis

## 3. Constitutional Compliance Assessment
### 3.1 Article-by-Article Scores
- Individual article compliance
- Evidence for each assessment

### 3.2 Overall Compliance Score
- Aggregate score (0-100)
- Violation summary

## 4. Execution Performance Metrics
### 4.1 Success and Failure Rates
- Quantitative metrics table
- Rate comparisons

### 4.2 Backup Method Usage
- Usage statistics
- Effectiveness assessment

### 4.3 Mode Escalations
- Escalation count and triggers
- Appropriateness evaluation

### 4.4 Efficiency Metrics
- Steps per task
- Time analysis (if available)

## 5. Behaviour Correlation Analysis
### 5.1 Identified Correlations
- Goal characteristics vs execution behaviour
- Correlation strength assessment

### 5.2 Causality Assessment
- Causal vs correlational relationships
- Confidence levels

### 5.3 Confounding Factors
- External influences
- Mediation effects

## 6. Quality Assessment
### 6.1 Task Decomposition Quality
- Per-task quality scores
- Decomposition effectiveness

### 6.2 Step Quality Analysis
- Atomicity assessment
- Critical flag appropriateness

### 6.3 Method Selection Quality
- Primary/backup rationale
- Method effectiveness

## 7. Error Analysis
### 7.1 Error Categorisation
- Error type distribution
- Frequency patterns

### 7.2 Root Cause Analysis
- Root cause mapping
- Prevention opportunities

### 7.3 Recovery Effectiveness
- Recovery success rates
- Backup effectiveness

### 7.4 Constitutional Violations
- Violation breakdown by article
- Severity assessment

## 8. Recommendations
### 8.1 Goal Formulation Improvements
[Specific, actionable recommendations]

### 8.2 SPEC Design Enhancements
[Specific, actionable recommendations]

### 8.3 Execution Optimisation
[Specific, actionable recommendations]

### 8.4 Constitutional Compliance
[Specific, actionable recommendations]

### 8.5 Future Research Directions
[Areas for deeper investigation]

## Appendices
### A. Raw Data Tables
### B. Propagation Examples (Full Quotes)
### C. Metrics Calculation Methods
### D. Source Citations
```

---

**End of Dev_Analysis_SPEC.md**

This SPEC is designed to be reusable across multiple test SPEC analyses, enabling systematic comparison and pattern identification.


```

```markdown
# Dev Analysis SPEC

**Version:** 1.0  
**Last Updated:** 2025-11-03  
**Purpose:** Analyse development of test SPECs to identify patterns, metrics, and goal text propagation effects

---

## Goal

Perform comprehensive analysis of a test SPEC's development lifecycle to identify how initial goal text propagates through the system and impacts agent behaviour, execution accuracy, and project outcomes.

---

## Software Stack & Architecture

**Not Applicable** - This is an analysis task, not a build goal.

---

## Definition of Complete

What must exist and be verified:
- [ ] **Primary deliverable:** Comprehensive analysis report (markdown format) covering all analysis areas
- [ ] **Quality standards met:** 
  - All 8 analysis tasks completed with documented findings
  - Goal text propagation patterns identified with specific examples
  - Quantitative metrics calculated for execution performance
  - Cross-correlation analysis between goal characteristics and outcomes
  - Recommendations provided based on findings
- [ ] **Verification method:** 
  - Report contains all required sections (see tasks below)
  - Quantitative metrics include numerical values with source citations
  - At least 3 specific examples of goal text propagation documented
  - Recommendations are actionable and linked to specific findings

---

## Definitions

- **goal**: Analyse how initial goal text characteristics influence SPEC development and execution
- **task[n]**: Discrete analysis objectives examining different aspects of SPEC development
- **step[m]**: Concrete analytical actions within each task
- **backup[p]**: Alternative analysis methods when primary approach is blocked
- **critical_flag**: Boolean indicating whether analysis step is essential to overall goal
- **mode**: `silent` (fully autonomous - NO USER INPUT REQUIRED except initial project folder location)
- **progress.json**: Structured log tracking analysis execution and findings
- **project_folder**: Target development project folder path (ONLY required user input)

---

## Components

Analysis requires access to:
- **Test SPEC files:** spec_[descriptor].md, parameters_[descriptor].toml, exe_[descriptor].md
- **Execution logs:** progress_[descriptor].json
- **Project artefacts:** Code files, documentation, error logs, validation reports
- **Chat history:** Conversation transcripts showing agent thinking and decision-making
- **Constitution:** __SPEC_Engine/_Constitution/constitution.md for compliance checking

**Machine-Readable Components:**  
See `[components]` section in parameters_Dev_Analysis.toml

---

## Constraints

- Analysis must be objective and evidence-based
- All metrics must be traceable to source data
- Goal text propagation analysis must include minimum 3 concrete examples
- Quantitative metrics must include: success rates, error rates, mode escalations, backup usage
- Findings must distinguish correlation from causation
- Recommendations must be specific and actionable

**Machine-Readable Constraints:**  
See `[constraints]` section in parameters_Dev_Analysis.toml:
- `min_examples_required = 3` (goal text propagation examples)
- `metrics_evidence_based = true` (all metrics must cite sources)
- `recommendation_specificity = "actionable"` (recommendations must be implementable)

---

## User Stories

- As a **SPEC developer**, I want to understand how goal phrasing impacts development so I can write more effective goals
- As a **system architect**, I want to identify patterns in SPEC execution so I can improve the framework
- As a **researcher**, I want to quantify goal text propagation so I can understand agent behaviour correlation
- As a **project manager**, I want metrics on SPEC performance so I can assess project quality

---

## Analysis Framework

This SPEC analyses development across 8 integrated dimensions:

### Dimension 1: Goal Text Characteristics
- Length (word count, character count, sentence complexity)
- Number of distinct elements/requirements
- Literacy level (Flesch-Kincaid, technical density)
- Formatting (structure, lists, emphasis)
- Familiarity/Technical specificity

### Dimension 2: Goal Text Propagation
- How goal language appears in task descriptions
- Goal terminology in step definitions
- Phrasing patterns in agent thinking/reasoning
- Language consistency across SPEC artefacts
- Conceptual drift from goal to implementation

### Dimension 3: Constitutional Compliance
- Article I-XIV adherence scoring
- Critical flag balance (target: 40-60%)
- Backup method quality assessment
- Bridging quality (Markdown-TOML sync)
- Validation checkpoint outcomes

### Dimension 4: Execution Performance
- Step success/failure rates
- Backup invocation frequency
- Mode escalation patterns
- Error propagation effectiveness
- Retry patterns and exhaustion

### Dimension 5: Agent Behaviour Correlation
- Thinking patterns vs goal complexity
- Decision quality vs goal clarity
- Output quality vs goal specificity
- Backup selection vs goal ambiguity
- Escalation triggers vs goal characteristics

### Dimension 6: Per-Task/Step Behaviour
- Task decomposition quality
- Step atomicity assessment
- Critical flag appropriateness
- Expected output clarity
- Method selection rationale

### Dimension 7: Error Analysis
- Error types and frequencies
- Root cause patterns
- Recovery effectiveness
- Constitutional violations
- Preventable vs inherent errors

### Dimension 8: Outcome Metrics
- Goal achievement status (ACHIEVED/PARTIAL/NOT_ACHIEVED)
- Deliverable completeness
- Quality standards met
- Time/step efficiency
- Comparison to expected outcomes

---

## Task [0]: Initialize Analysis and Gather Project Metadata

**TOML Reference:** `tasks[id=0]` in parameters_Dev_Analysis.toml  
**Purpose:** Locate project folder, scan structure, and collect comprehensive metadata

- **Step [0]:** Receive project folder location (ONLY USER INPUT REQUIRED)
  - **Primary method:** Prompt for project development folder path
  - **Expected output:** Absolute path to project folder
  - **Critical:** true
  - **Mode:** collaborative (ONE TIME ONLY - for folder path input)

- **Step [1]:** Scan and map complete project structure
  - **Primary method:** Recursively list all files and directories in project folder
  - **Backup [1]:** If permissions issue, request accessible subset of project
  - **Expected output:** Complete file tree with full paths
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count and categorise all files
  - **Primary method:** Count files by type: .md, .toml, .json, .py, .js, .ts, .log, .txt, etc.
  - **Expected output:** File count table with breakdown by extension
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Calculate file sizes and total project size
  - **Primary method:** Get file size for each file, sum by category and total
  - **Expected output:** Size metrics table (bytes, KB, MB) by file type and total
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Extract all timestamps
  - **Primary method:** Collect creation, modification, access times for all relevant files
  - **Backup [1]:** If timestamps unavailable, use git history if present
  - **Expected output:** Timeline table showing project chronology
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Calculate development duration
  - **Primary method:** Calculate time from earliest to latest timestamp, identify development phases
  - **Expected output:** Development duration metrics: total time, active development periods, gaps
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Count tokens across all text files
  - **Primary method:** For each text-based file, count tokens (words, characters, estimated LLM tokens)
  - **Backup [1]:** If token counting unavailable, use word/character counts as proxy
  - **Expected output:** Token count table by file type with totals
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Identify and catalogue error logs
  - **Primary method:** Locate all error log files, count error entries, categorise by severity
  - **Expected output:** Error log inventory with counts and locations
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Identify and catalogue chat/conversation logs
  - **Primary method:** Locate chat transcripts, conversation logs, agent thinking logs
  - **Backup [1]:** Check common locations: root, logs folder, subdirectories
  - **Expected output:** Conversation log inventory with file paths and sizes
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Count conversation turns and messages
  - **Primary method:** Parse chat logs to count: total messages, user messages, agent messages, turns
  - **Expected output:** Conversation metrics table
  - **Critical:** false
  - **Mode:** silent

- **Step [10]:** Identify SPEC files and versions
  - **Primary method:** Locate all spec_*.md, parameters_*.toml, exe_*.md, progress_*.json files
  - **Expected output:** SPEC file inventory with versions and timestamps
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Create project metadata snapshot
  - **Primary method:** Aggregate all collected metrics into comprehensive metadata document
  - **Expected output:** Project metadata JSON with all metrics organized
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Project folder scanned, all files catalogued, comprehensive metrics collected
- **Logging:** Record all metadata in progress_Dev_Analysis.json for reference throughout analysis

---

## Task [1]: Extract and Characterise Initial Goal Text

**TOML Reference:** `tasks[id=1]` in parameters_Dev_Analysis.toml  
**Purpose:** Establish baseline characteristics of the goal that initiated SPEC development

- **Step [1]:** Locate and extract initial goal text
  - **Primary method:** Read SPEC markdown file Goal section and chat history for original user goal statement
  - **Backup [1]:** If chat history unavailable, use goal section from spec_[descriptor].md as proxy
  - **Expected output:** Exact goal text with source citation and timestamp
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Calculate quantitative text characteristics
  - **Primary method:** Compute word count, character count, sentence count, avg sentence length, Flesch-Kincaid score
  - **Backup [1]:** If automated scoring unavailable, perform manual classification (simple/moderate/complex)
  - **Expected output:** Table with numerical metrics and complexity classification
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Identify distinct elements and requirements
  - **Primary method:** Parse goal for discrete requirements, constraints, deliverables, success criteria
  - **Backup [1]:** Use linguistic chunking to identify conceptual units if structure unclear
  - **Expected output:** Numbered list of distinct elements (target: 3-10 elements)
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess technical specificity and domain familiarity
  - **Primary method:** Identify technical terms, domain-specific language, assumed knowledge, explicit vs implicit requirements
  - **Backup [1]:** Compare vocabulary against common vs specialised term databases
  - **Expected output:** Technical specificity score (1-5 scale) with justification and term examples
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Analyse formatting and structure
  - **Primary method:** Document use of lists, emphasis, sections, explicit vs narrative format
  - **Expected output:** Formatting assessment noting structural elements present
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All goal characteristics documented with quantitative metrics where possible
- **Logging:** Record all measurements in progress_Dev_Analysis.json for correlation analysis

---

## Task [2]: Map Goal Text Propagation Throughout Project

**TOML Reference:** `tasks[id=2]` in parameters_Dev_Analysis.toml  
**Purpose:** Track how initial goal language and concepts propagate through SPEC artefacts

- **Step [1]:** Extract task descriptions from SPEC
  - **Primary method:** Parse spec_[descriptor].md for all task titles and descriptions
  - **Expected output:** List of tasks with full text
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify goal language in task descriptions
  - **Primary method:** Compare task descriptions to goal text, noting shared terminology, conceptual overlap, verbatim phrases
  - **Backup [1]:** Use semantic similarity scoring if direct comparison insufficient
  - **Expected output:** Table mapping goal terms to task descriptions with similarity scores
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Extract step definitions and analyse propagation
  - **Primary method:** Parse all step descriptions, identify goal/task terminology presence, track conceptual consistency
  - **Backup [1]:** Focus on critical steps only if volume is high (>20 steps)
  - **Expected output:** Propagation matrix showing goal→task→step language flow with specific examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse agent thinking and reasoning patterns
  - **Primary method:** Review chat history/logs for agent internal reasoning, note how goal concepts appear in thinking
  - **Backup [1]:** If full chat unavailable, analyse progress.json logs for method justifications
  - **Expected output:** Minimum 3 specific examples of goal text influencing agent reasoning with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify conceptual drift
  - **Primary method:** Compare final implementation/outputs against original goal, identify divergences in terminology, scope, or interpretation
  - **Expected output:** Conceptual drift assessment noting where implementation departed from goal language
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Assess language consistency across artefacts
  - **Primary method:** Check terminology consistency across spec.md, parameters.toml, progress.json, deliverables
  - **Expected output:** Consistency report identifying where language fragmented or evolved
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Minimum 3 concrete examples of goal text propagation documented with direct quotes
- **Logging:** Record propagation patterns and drift instances in progress_Dev_Analysis.json

---

## Task [3]: Evaluate Constitutional Compliance

**TOML Reference:** `tasks[id=3]` in parameters_Dev_Analysis.toml  
**Purpose:** Assess adherence to SPEC Engine Constitution (Articles I-XIV)

- **Step [1]:** Validate Article I compliance (North Star Principle)
  - **Primary method:** Verify goal singularity, clarity, measurability, explicitness
  - **Expected output:** Article I compliance score (pass/fail) with justification
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Validate Article II compliance (Hierarchical Structure)
  - **Primary method:** Count tasks (target: 2-5), count steps per task (target: 1-5), verify hierarchy maintained
  - **Backup [1]:** If counts borderline, assess whether structure serves goal effectively
  - **Expected output:** Article II compliance score with quantitative counts
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Validate Article III compliance (Dual-File Mandate)
  - **Primary method:** Cross-check spec.md and parameters.toml for ID matching, structure sync, cross-references
  - **Expected output:** Article III compliance score noting any bridging failures
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Validate Article VI compliance (Critical Flag Discipline)
  - **Primary method:** Calculate critical step percentage (target: 40-60%), assess appropriateness of critical flags
  - **Expected output:** Critical balance percentage and appropriateness assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Validate Article VII compliance (Backup Methods)
  - **Primary method:** Review all backup methods to ensure they are alternative reasoning paths, not retries
  - **Backup [1]:** Sample backup methods if total exceeds 15
  - **Expected output:** Backup quality score with examples of good/poor backups
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Check Article XIV compliance (if build goal)
  - **Primary method:** If goal contains build/create/system keywords, verify software stack defined, deployment criteria present
  - **Expected output:** Article XIV compliance (N/A or pass/fail with details)
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Review Articles IV, VIII, IX, X compliance from execution
  - **Primary method:** Analyse progress.json for validation execution, error propagation, mode discipline, comprehensive logging
  - **Expected output:** Compliance scores for Articles IV, VIII, IX, X with evidence from logs
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Calculate overall constitutional compliance score
  - **Primary method:** Aggregate individual article scores, weight by severity, generate 0-100 score
  - **Expected output:** Overall compliance score (0-100) with breakdown by article
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All applicable articles assessed with evidence-based scoring
- **Logging:** Record compliance scores and violations in progress_Dev_Analysis.json

---

## Task [4]: Analyse Execution Performance Metrics

**TOML Reference:** `tasks[id=4]` in parameters_Dev_Analysis.toml  
**Purpose:** Extract quantitative performance data from execution logs with comprehensive detail

- **Step [1]:** Parse progress.json for complete step data
  - **Primary method:** Read progress_[descriptor].json, extract ALL fields: task_id, step_id, status, method_used, retry_count, timestamp, mode, critical_flag, expected_output, actual_output, error_messages
  - **Backup [1]:** If progress.json malformed, reconstruct from available logs
  - **Expected output:** Complete step outcome dataset with full detail per step
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count total steps taken
  - **Primary method:** Count: total steps defined, total steps attempted, total steps completed, total steps skipped, total steps failed
  - **Expected output:** Comprehensive step count table with breakdown by status
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Calculate detailed success and failure rates
  - **Primary method:** Compute: overall success rate, failure rate, success rate by task, failure rate by task, first-attempt success rate, eventual success rate (after retries)
  - **Expected output:** Multi-level success/failure metrics table with percentages at step, task, and SPEC levels
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse backup method usage patterns
  - **Primary method:** Count: primary method attempts, primary successes, backup[1] attempts, backup[1] successes, backup[2] attempts, backup[2] successes, calculate success rates per method type
  - **Expected output:** Comprehensive backup usage statistics with success rates, effectiveness scores, and usage frequency distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Track mode usage and escalations
  - **Primary method:** Count: steps in silent mode, steps in collaborative mode, mode switches, categorise escalation triggers (consecutive failures, backup depletion, critical failure, confidence degradation)
  - **Expected output:** Mode usage table, escalation count by trigger type, escalation appropriateness assessment per instance
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Analyse timestamps and time metrics
  - **Primary method:** Extract all timestamps from progress.json, calculate: time per step, time per task, total execution time, longest steps, shortest steps, time distribution
  - **Backup [1]:** If timestamps sparse, use available data and note gaps
  - **Expected output:** Comprehensive time metrics table with duration statistics
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Assess error propagation effectiveness
  - **Primary method:** Identify all steps with dependencies, check if prior failures were read from progress.json, assess propagation handling quality, count propagation decisions
  - **Backup [1]:** If error propagation tracking sparse, infer from step sequence and outcomes
  - **Expected output:** Error propagation effectiveness score with example instances and propagation decision breakdown
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Analyse retry patterns in detail
  - **Primary method:** Extract retry_count per step, calculate: average retries per step, max retries reached, retry exhaustion rate, retry success rate, thoroughness score (methods exhausted before escalation)
  - **Expected output:** Detailed retry pattern analysis with distribution charts and exhaustion assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Calculate efficiency and productivity metrics
  - **Primary method:** Compute: total steps attempted vs planned, steps per task (actual vs expected), average time per step, steps per hour, rework rate (retries/total), productivity score
  - **Expected output:** Comprehensive efficiency metrics table with productivity indicators
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Analyse critical vs non-critical step performance
  - **Primary method:** Separate critical and non-critical steps, compare: success rates, retry rates, time per step, failure impact
  - **Expected output:** Critical flag performance comparison table
  - **Critical:** false
  - **Mode:** silent

- **Step [11]:** Extract and analyse expected vs actual outputs
  - **Primary method:** For each step, compare expected_output defined in SPEC to actual_output logged, categorise: exact match, partial match, mismatch, missing
  - **Expected output:** Output quality assessment with match rate and mismatch analysis
  - **Critical:** true
  - **Mode:** silent

- **Step [12]:** Count and categorise all errors encountered
  - **Primary method:** Extract all error messages from progress.json, categorise by type (validation, execution, resource, logic), count occurrences, identify most frequent errors
  - **Expected output:** Error frequency table by category with top 10 most common errors
  - **Critical:** true
  - **Mode:** silent

- **Step [13]:** Analyse token usage per step (if available)
  - **Primary method:** If token counts logged, extract tokens per step, calculate: tokens per task, total tokens, token efficiency (tokens per successful step)
  - **Backup [1]:** If not logged in progress.json, skip with note
  - **Expected output:** Token usage metrics table (if data available)
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All quantitative metrics calculated with source data citations, minimum 13 metric categories documented
- **Logging:** Record all performance metrics in progress_Dev_Analysis.json

---

## Task [5]: Correlate Agent Behaviour with Goal Characteristics

**TOML Reference:** `tasks[id=5]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify relationships between goal text properties and agent execution behaviour

- **Step [1]:** Establish correlation framework
  - **Primary method:** Define metrics for correlation: goal complexity vs task count, goal clarity vs error rate, goal specificity vs backup usage
  - **Expected output:** Correlation matrix framework listing goal characteristics and behaviour metrics
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Analyse goal complexity vs task decomposition
  - **Primary method:** Correlate goal complexity score (from Task 1) with number of tasks, steps per task, decomposition depth
  - **Backup [1]:** Use qualitative assessment if quantitative correlation weak
  - **Expected output:** Correlation finding: does complex goal lead to more/fewer tasks?
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Analyse goal clarity vs execution accuracy
  - **Primary method:** Correlate goal clarity indicators (explicit requirements, measurable criteria) with success rate, error rate
  - **Expected output:** Correlation finding: does clear goal reduce errors?
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse goal specificity vs backup usage
  - **Primary method:** Correlate technical specificity score with backup invocation rate, backup effectiveness
  - **Expected output:** Correlation finding: does vague goal increase backup reliance?
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Analyse goal formatting vs agent thinking patterns
  - **Primary method:** Review agent reasoning for structured vs narrative goals, assess thinking clarity and organisation
  - **Backup [1]:** If thinking logs sparse, assess output organisation as proxy
  - **Expected output:** Qualitative finding on formatting impact with examples
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Identify confounding factors
  - **Primary method:** Check for external factors affecting correlation: SPEC complexity, domain difficulty, resource availability
  - **Expected output:** List of confounding factors that may explain behaviour patterns
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Distinguish correlation from causation
  - **Primary method:** For each correlation found, assess whether relationship is causal, coincidental, or mediated by other factors using evidence-based analysis
  - **Backup [1]:** Apply Bradford Hill criteria for causation: strength, consistency, specificity, temporality, biological gradient
  - **Expected output:** Causality assessment for each correlation with confidence level and supporting evidence
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Minimum 3 behaviour correlations identified with specific evidence
- **Logging:** Record correlations and causality assessments in progress_Dev_Analysis.json

---

## Task [6]: Assess Per-Task and Per-Step Behaviour Quality

**TOML Reference:** `tasks[id=6]` in parameters_Dev_Analysis.toml  
**Purpose:** Evaluate quality of task decomposition and step execution at granular level

- **Step [1]:** Evaluate task decomposition quality
  - **Primary method:** For each task, assess: Does task serve goal? Is task scope appropriate? Is task self-contained?
  - **Expected output:** Task quality assessment table with scores and rationale per task
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Assess step atomicity
  - **Primary method:** For each step, assess: Is step a single concrete action? Is step scope too broad/narrow? Is step executable?
  - **Backup [1]:** Sample steps if total exceeds 20
  - **Expected output:** Step atomicity assessment with examples of well/poorly scoped steps
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Evaluate critical flag appropriateness
  - **Primary method:** For each critical step, verify: Would failure truly block goal? For non-critical, verify: Can goal succeed without this?
  - **Expected output:** Critical flag appropriateness score with misclassification examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess expected output clarity
  - **Primary method:** For each step, rate expected output: specific/vague, measurable/subjective, achievable/unrealistic
  - **Expected output:** Expected output quality assessment with clarity distribution
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Evaluate method selection rationale
  - **Primary method:** For steps with multiple methods, assess whether primary/backup choices were well-justified
  - **Expected output:** Method selection quality score with examples
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All tasks and representative sample of steps assessed for quality
- **Logging:** Record quality assessments in progress_Dev_Analysis.json

---

## Task [7]: Conduct Error Analysis and Pattern Detection

**TOML Reference:** `tasks[id=7]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify error patterns, root causes, and improvement opportunities

- **Step [1]:** Categorise all errors by type
  - **Primary method:** Extract all failures from progress.json, categorise: validation errors, execution errors, resource errors, logic errors
  - **Expected output:** Error categorisation table with counts and percentages
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify error frequency patterns
  - **Primary method:** Analyse which tasks/steps had highest error rates, identify repeated failures
  - **Expected output:** Error hotspot analysis showing concentration areas
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Conduct root cause analysis
  - **Primary method:** For each error category, trace to root cause: SPEC design issue, execution issue, resource limitation, goal ambiguity
  - **Backup [1]:** Focus on top 5 most frequent errors if volume high
  - **Expected output:** Root cause mapping with prevention recommendations
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess recovery effectiveness
  - **Primary method:** For each error, check if backup methods resolved issue, assess recovery time, evaluate escalation appropriateness
  - **Expected output:** Recovery effectiveness score with successful/unsuccessful recovery examples
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify constitutional violations
  - **Primary method:** Check progress.json for constitutional_compliance section, extract all violations with severity
  - **Backup [1]:** Manual review of logs if compliance tracking absent
  - **Expected output:** Constitutional violation summary with article breakdown
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Distinguish preventable from inherent errors
  - **Primary method:** Classify each error: preventable through better SPEC design, inherent to task complexity, external/environmental
  - **Expected output:** Error preventability classification with improvement focus areas
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All errors analysed with root causes identified
- **Logging:** Record error analysis findings in progress_Dev_Analysis.json

---

## Task [8]: Generate Comprehensive Analysis Report with Recommendations

**TOML Reference:** `tasks[id=8]` in parameters_Dev_Analysis.toml  
**Purpose:** Synthesise all findings into actionable report

- **Step [1]:** Structure report outline
  - **Primary method:** Create report sections: Executive Summary, Goal Analysis, Propagation Findings, Performance Metrics, Correlations, Quality Assessment, Error Analysis, Recommendations
  - **Expected output:** Report outline with section headers
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Write Executive Summary
  - **Primary method:** Synthesise key findings: goal characteristics summary, main propagation patterns, overall performance, critical insights
  - **Expected output:** 200-300 word executive summary highlighting main findings
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Compile Goal Text Analysis section
  - **Primary method:** Aggregate Task 1 findings: goal characteristics table, complexity assessment, element breakdown
  - **Expected output:** Goal Text Analysis section with all metrics and assessments
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Compile Goal Text Propagation section
  - **Primary method:** Aggregate Task 2 findings: propagation examples, language flow diagram, conceptual drift assessment
  - **Expected output:** Goal Text Propagation section with minimum 3 concrete examples with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Compile Constitutional Compliance section
  - **Primary method:** Aggregate Task 3 findings: article-by-article scores, overall compliance score, violation summary
  - **Expected output:** Constitutional Compliance section with compliance scorecard
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Compile Execution Performance section
  - **Primary method:** Aggregate Task 4 findings: success/failure rates, backup usage, mode escalations, efficiency metrics
  - **Expected output:** Execution Performance section with metrics tables
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Compile Behaviour Correlation section
  - **Primary method:** Aggregate Task 5 findings: correlation matrix, causality assessments, confounding factors
  - **Expected output:** Behaviour Correlation section with correlation findings
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Compile Quality Assessment section
  - **Primary method:** Aggregate Task 6 findings: task quality scores, step atomicity, critical flag appropriateness
  - **Expected output:** Quality Assessment section with quality distributions
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Compile Error Analysis section
  - **Primary method:** Aggregate Task 7 findings: error categories, root causes, recovery effectiveness, preventability
  - **Expected output:** Error Analysis section with error breakdown and patterns
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Generate actionable recommendations
  - **Primary method:** Based on all findings, create specific recommendations for: goal formulation improvement, SPEC design enhancement, execution optimisation, constitutional compliance
  - **Backup [1]:** If recommendations unclear, escalate to collaborative mode for human input
  - **Expected output:** Minimum 5 specific, actionable recommendations linked to findings
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Add cross-project comparison framework (if applicable)
  - **Primary method:** If analysing multiple SPECs, create comparison tables for key metrics across projects
  - **Expected output:** Cross-project comparison section (optional, only if multiple projects analysed)
  - **Critical:** false
  - **Mode:** silent

- **Step [12]:** Finalise report formatting and references
  - **Primary method:** Ensure all sections formatted consistently, add table of contents, verify all data citations present
  - **Expected output:** Complete, polished analysis report in markdown format
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Report contains all required sections, metrics are evidence-based, recommendations are actionable
- **Logging:** Record report completion in progress_Dev_Analysis.json with final deliverable path

---

## Bridging: Markdown ↔ TOML Synchronisation

This spec file (Dev_Analysis_SPEC.md) must maintain perfect alignment with its companion file (parameters_Dev_Analysis.toml).

**Bridging Requirements:**
1. Each task in this file must have corresponding `[[tasks]]` entry in TOML with matching ID (1-8)
2. Each step within a task must have corresponding `[[tasks.steps]]` entry with matching ID
3. Expected outputs in this file must match `expected_output` fields in TOML
4. Critical flags must be synchronised between files
5. Constraints referenced must exist in TOML `[constraints]` section

**Example Cross-References:**
- "See `constraints.min_examples_required` in parameters_Dev_Analysis.toml" (Task 2, Step 4)
- "As defined in `tasks[id=4]` in TOML" (Task 4 reference)
- "Must satisfy TOML verification requirements" (All task verifications)

The exe_Dev_Analysis.md controller will validate this synchronisation during initialisation (Section 1.8).

---

## Instructions for LLM Executor

1. **Start with goal understanding**: This analysis examines how goal text propagates and influences SPEC development
2. **Execute tasks sequentially**: Tasks 1-2 gather data, Tasks 3-7 analyse patterns, Task 8 synthesises findings
3. **Maintain objectivity**: Base all findings on evidence from files, logs, and artefacts
4. **Track propagation carefully**: Pay special attention to how exact goal language appears throughout project
5. **Quantify where possible**: Use numerical metrics rather than subjective assessments when feasible
6. **Distinguish correlation from causation**: Note relationships but assess causality carefully
7. **Document thoroughly**: Log all findings in progress_Dev_Analysis.json for traceability
8. **Focus on actionability**: Recommendations should be specific and implementable
9. **Read prior outcomes**: Before each step, check progress.json for relevant prior findings
10. **Escalate appropriately**: Use collaborative mode for causality judgements and unclear recommendation priorities

---

## Expected Analysis Output Structure

The final report should follow this structure:

```markdown
# SPEC Development Analysis Report

## Executive Summary
[200-300 word overview of key findings]

## 1. Goal Text Analysis
### 1.1 Initial Goal Characteristics
- Quantitative metrics table
- Complexity classification
- Element breakdown

### 1.2 Technical Specificity Assessment
- Specificity score with justification
- Domain terminology analysis

## 2. Goal Text Propagation Analysis
### 2.1 Propagation Through Tasks
- Task-level language mapping
- Specific examples with quotes

### 2.2 Propagation Through Steps
- Step-level language mapping
- Propagation matrix

### 2.3 Agent Thinking Patterns
- Minimum 3 examples of goal text in reasoning
- Direct quotes from logs/chat

### 2.4 Conceptual Drift Assessment
- Identified divergences
- Impact analysis

## 3. Constitutional Compliance Assessment
### 3.1 Article-by-Article Scores
- Individual article compliance
- Evidence for each assessment

### 3.2 Overall Compliance Score
- Aggregate score (0-100)
- Violation summary

## 4. Execution Performance Metrics
### 4.1 Success and Failure Rates
- Quantitative metrics table
- Rate comparisons

### 4.2 Backup Method Usage
- Usage statistics
- Effectiveness assessment

### 4.3 Mode Escalations
- Escalation count and triggers
- Appropriateness evaluation

### 4.4 Efficiency Metrics
- Steps per task
- Time analysis (if available)

## 5. Behaviour Correlation Analysis
### 5.1 Identified Correlations
- Goal characteristics vs execution behaviour
- Correlation strength assessment

### 5.2 Causality Assessment
- Causal vs correlational relationships
- Confidence levels

### 5.3 Confounding Factors
- External influences
- Mediation effects

## 6. Quality Assessment
### 6.1 Task Decomposition Quality
- Per-task quality scores
- Decomposition effectiveness

### 6.2 Step Quality Analysis
- Atomicity assessment
- Critical flag appropriateness

### 6.3 Method Selection Quality
- Primary/backup rationale
- Method effectiveness

## 7. Error Analysis
### 7.1 Error Categorisation
- Error type distribution
- Frequency patterns

### 7.2 Root Cause Analysis
- Root cause mapping
- Prevention opportunities

### 7.3 Recovery Effectiveness
- Recovery success rates
- Backup effectiveness

### 7.4 Constitutional Violations
- Violation breakdown by article
- Severity assessment

## 8. Recommendations
### 8.1 Goal Formulation Improvements
[Specific, actionable recommendations]

### 8.2 SPEC Design Enhancements
[Specific, actionable recommendations]

### 8.3 Execution Optimisation
[Specific, actionable recommendations]

### 8.4 Constitutional Compliance
[Specific, actionable recommendations]

### 8.5 Future Research Directions
[Areas for deeper investigation]

## Appendices
### A. Raw Data Tables
### B. Propagation Examples (Full Quotes)
### C. Metrics Calculation Methods
### D. Source Citations
```

---

**End of Dev_Analysis_SPEC.md**

This SPEC is designed to be reusable across multiple test SPEC analyses, enabling systematic comparison and pattern identification.


```

```markdown
# Dev Analysis SPEC

**Version:** 1.0  
**Last Updated:** 2025-11-03  
**Purpose:** Analyse development of test SPECs to identify patterns, metrics, and goal text propagation effects

---

## Goal

Perform comprehensive analysis of a test SPEC's development lifecycle to identify how initial goal text propagates through the system and impacts agent behaviour, execution accuracy, and project outcomes.

---

## Software Stack & Architecture

**Not Applicable** - This is an analysis task, not a build goal.

---

## Definition of Complete

What must exist and be verified:
- [ ] **Primary deliverable:** Comprehensive analysis report (markdown format) covering all analysis areas
- [ ] **Quality standards met:** 
  - All 8 analysis tasks completed with documented findings
  - Goal text propagation patterns identified with specific examples
  - Quantitative metrics calculated for execution performance
  - Cross-correlation analysis between goal characteristics and outcomes
  - Recommendations provided based on findings
- [ ] **Verification method:** 
  - Report contains all required sections (see tasks below)
  - Quantitative metrics include numerical values with source citations
  - At least 3 specific examples of goal text propagation documented
  - Recommendations are actionable and linked to specific findings

---

## Definitions

- **goal**: Analyse how initial goal text characteristics influence SPEC development and execution
- **task[n]**: Discrete analysis objectives examining different aspects of SPEC development
- **step[m]**: Concrete analytical actions within each task
- **backup[p]**: Alternative analysis methods when primary approach is blocked
- **critical_flag**: Boolean indicating whether analysis step is essential to overall goal
- **mode**: `silent` (fully autonomous - NO USER INPUT REQUIRED except initial project folder location)
- **progress.json**: Structured log tracking analysis execution and findings
- **project_folder**: Target development project folder path (ONLY required user input)

---

## Components

Analysis requires access to:
- **Test SPEC files:** spec_[descriptor].md, parameters_[descriptor].toml, exe_[descriptor].md
- **Execution logs:** progress_[descriptor].json
- **Project artefacts:** Code files, documentation, error logs, validation reports
- **Chat history:** Conversation transcripts showing agent thinking and decision-making
- **Constitution:** __SPEC_Engine/_Constitution/constitution.md for compliance checking

**Machine-Readable Components:**  
See `[components]` section in parameters_Dev_Analysis.toml

---

## Constraints

- Analysis must be objective and evidence-based
- All metrics must be traceable to source data
- Goal text propagation analysis must include minimum 3 concrete examples
- Quantitative metrics must include: success rates, error rates, mode escalations, backup usage
- Findings must distinguish correlation from causation
- Recommendations must be specific and actionable

**Machine-Readable Constraints:**  
See `[constraints]` section in parameters_Dev_Analysis.toml:
- `min_examples_required = 3` (goal text propagation examples)
- `metrics_evidence_based = true` (all metrics must cite sources)
- `recommendation_specificity = "actionable"` (recommendations must be implementable)

---

## User Stories

- As a **SPEC developer**, I want to understand how goal phrasing impacts development so I can write more effective goals
- As a **system architect**, I want to identify patterns in SPEC execution so I can improve the framework
- As a **researcher**, I want to quantify goal text propagation so I can understand agent behaviour correlation
- As a **project manager**, I want metrics on SPEC performance so I can assess project quality

---

## Analysis Framework

This SPEC analyses development across 8 integrated dimensions:

### Dimension 1: Goal Text Characteristics
- Length (word count, character count, sentence complexity)
- Number of distinct elements/requirements
- Literacy level (Flesch-Kincaid, technical density)
- Formatting (structure, lists, emphasis)
- Familiarity/Technical specificity

### Dimension 2: Goal Text Propagation
- How goal language appears in task descriptions
- Goal terminology in step definitions
- Phrasing patterns in agent thinking/reasoning
- Language consistency across SPEC artefacts
- Conceptual drift from goal to implementation

### Dimension 3: Constitutional Compliance
- Article I-XIV adherence scoring
- Critical flag balance (target: 40-60%)
- Backup method quality assessment
- Bridging quality (Markdown-TOML sync)
- Validation checkpoint outcomes

### Dimension 4: Execution Performance
- Step success/failure rates
- Backup invocation frequency
- Mode escalation patterns
- Error propagation effectiveness
- Retry patterns and exhaustion

### Dimension 5: Agent Behaviour Correlation
- Thinking patterns vs goal complexity
- Decision quality vs goal clarity
- Output quality vs goal specificity
- Backup selection vs goal ambiguity
- Escalation triggers vs goal characteristics

### Dimension 6: Per-Task/Step Behaviour
- Task decomposition quality
- Step atomicity assessment
- Critical flag appropriateness
- Expected output clarity
- Method selection rationale

### Dimension 7: Error Analysis
- Error types and frequencies
- Root cause patterns
- Recovery effectiveness
- Constitutional violations
- Preventable vs inherent errors

### Dimension 8: Outcome Metrics
- Goal achievement status (ACHIEVED/PARTIAL/NOT_ACHIEVED)
- Deliverable completeness
- Quality standards met
- Time/step efficiency
- Comparison to expected outcomes

---

## Task [0]: Initialize Analysis and Gather Project Metadata

**TOML Reference:** `tasks[id=0]` in parameters_Dev_Analysis.toml  
**Purpose:** Locate project folder, scan structure, and collect comprehensive metadata

- **Step [0]:** Receive project folder location (ONLY USER INPUT REQUIRED)
  - **Primary method:** Prompt for project development folder path
  - **Expected output:** Absolute path to project folder
  - **Critical:** true
  - **Mode:** collaborative (ONE TIME ONLY - for folder path input)

- **Step [1]:** Scan and map complete project structure
  - **Primary method:** Recursively list all files and directories in project folder
  - **Backup [1]:** If permissions issue, request accessible subset of project
  - **Expected output:** Complete file tree with full paths
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count and categorise all files
  - **Primary method:** Count files by type: .md, .toml, .json, .py, .js, .ts, .log, .txt, etc.
  - **Expected output:** File count table with breakdown by extension
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Calculate file sizes and total project size
  - **Primary method:** Get file size for each file, sum by category and total
  - **Expected output:** Size metrics table (bytes, KB, MB) by file type and total
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Extract all timestamps
  - **Primary method:** Collect creation, modification, access times for all relevant files
  - **Backup [1]:** If timestamps unavailable, use git history if present
  - **Expected output:** Timeline table showing project chronology
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Calculate development duration
  - **Primary method:** Calculate time from earliest to latest timestamp, identify development phases
  - **Expected output:** Development duration metrics: total time, active development periods, gaps
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Count tokens across all text files
  - **Primary method:** For each text-based file, count tokens (words, characters, estimated LLM tokens)
  - **Backup [1]:** If token counting unavailable, use word/character counts as proxy
  - **Expected output:** Token count table by file type with totals
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Identify and catalogue error logs
  - **Primary method:** Locate all error log files, count error entries, categorise by severity
  - **Expected output:** Error log inventory with counts and locations
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Identify and catalogue chat/conversation logs
  - **Primary method:** Locate chat transcripts, conversation logs, agent thinking logs
  - **Backup [1]:** Check common locations: root, logs folder, subdirectories
  - **Expected output:** Conversation log inventory with file paths and sizes
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Count conversation turns and messages
  - **Primary method:** Parse chat logs to count: total messages, user messages, agent messages, turns
  - **Expected output:** Conversation metrics table
  - **Critical:** false
  - **Mode:** silent

- **Step [10]:** Identify SPEC files and versions
  - **Primary method:** Locate all spec_*.md, parameters_*.toml, exe_*.md, progress_*.json files
  - **Expected output:** SPEC file inventory with versions and timestamps
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Create project metadata snapshot
  - **Primary method:** Aggregate all collected metrics into comprehensive metadata document
  - **Expected output:** Project metadata JSON with all metrics organized
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Project folder scanned, all files catalogued, comprehensive metrics collected
- **Logging:** Record all metadata in progress_Dev_Analysis.json for reference throughout analysis

---

## Task [1]: Extract and Characterise Initial Goal Text

**TOML Reference:** `tasks[id=1]` in parameters_Dev_Analysis.toml  
**Purpose:** Establish baseline characteristics of the goal that initiated SPEC development

- **Step [1]:** Locate and extract initial goal text
  - **Primary method:** Read SPEC markdown file Goal section and chat history for original user goal statement
  - **Backup [1]:** If chat history unavailable, use goal section from spec_[descriptor].md as proxy
  - **Expected output:** Exact goal text with source citation and timestamp
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Calculate quantitative text characteristics
  - **Primary method:** Compute word count, character count, sentence count, avg sentence length, Flesch-Kincaid score
  - **Backup [1]:** If automated scoring unavailable, perform manual classification (simple/moderate/complex)
  - **Expected output:** Table with numerical metrics and complexity classification
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Identify distinct elements and requirements
  - **Primary method:** Parse goal for discrete requirements, constraints, deliverables, success criteria
  - **Backup [1]:** Use linguistic chunking to identify conceptual units if structure unclear
  - **Expected output:** Numbered list of distinct elements (target: 3-10 elements)
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess technical specificity and domain familiarity
  - **Primary method:** Identify technical terms, domain-specific language, assumed knowledge, explicit vs implicit requirements
  - **Backup [1]:** Compare vocabulary against common vs specialised term databases
  - **Expected output:** Technical specificity score (1-5 scale) with justification and term examples
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Analyse formatting and structure
  - **Primary method:** Document use of lists, emphasis, sections, explicit vs narrative format
  - **Expected output:** Formatting assessment noting structural elements present
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All goal characteristics documented with quantitative metrics where possible
- **Logging:** Record all measurements in progress_Dev_Analysis.json for correlation analysis

---

## Task [2]: Map Goal Text Propagation Throughout Project

**TOML Reference:** `tasks[id=2]` in parameters_Dev_Analysis.toml  
**Purpose:** Track how initial goal language and concepts propagate through SPEC artefacts

- **Step [1]:** Extract task descriptions from SPEC
  - **Primary method:** Parse spec_[descriptor].md for all task titles and descriptions
  - **Expected output:** List of tasks with full text
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify goal language in task descriptions
  - **Primary method:** Compare task descriptions to goal text, noting shared terminology, conceptual overlap, verbatim phrases
  - **Backup [1]:** Use semantic similarity scoring if direct comparison insufficient
  - **Expected output:** Table mapping goal terms to task descriptions with similarity scores
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Extract step definitions and analyse propagation
  - **Primary method:** Parse all step descriptions, identify goal/task terminology presence, track conceptual consistency
  - **Backup [1]:** Focus on critical steps only if volume is high (>20 steps)
  - **Expected output:** Propagation matrix showing goal→task→step language flow with specific examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse agent thinking and reasoning patterns
  - **Primary method:** Review chat history/logs for agent internal reasoning, note how goal concepts appear in thinking
  - **Backup [1]:** If full chat unavailable, analyse progress.json logs for method justifications
  - **Expected output:** Minimum 3 specific examples of goal text influencing agent reasoning with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify conceptual drift
  - **Primary method:** Compare final implementation/outputs against original goal, identify divergences in terminology, scope, or interpretation
  - **Expected output:** Conceptual drift assessment noting where implementation departed from goal language
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Assess language consistency across artefacts
  - **Primary method:** Check terminology consistency across spec.md, parameters.toml, progress.json, deliverables
  - **Expected output:** Consistency report identifying where language fragmented or evolved
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Minimum 3 concrete examples of goal text propagation documented with direct quotes
- **Logging:** Record propagation patterns and drift instances in progress_Dev_Analysis.json

---

## Task [3]: Evaluate Constitutional Compliance

**TOML Reference:** `tasks[id=3]` in parameters_Dev_Analysis.toml  
**Purpose:** Assess adherence to SPEC Engine Constitution (Articles I-XIV)

- **Step [1]:** Validate Article I compliance (North Star Principle)
  - **Primary method:** Verify goal singularity, clarity, measurability, explicitness
  - **Expected output:** Article I compliance score (pass/fail) with justification
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Validate Article II compliance (Hierarchical Structure)
  - **Primary method:** Count tasks (target: 2-5), count steps per task (target: 1-5), verify hierarchy maintained
  - **Backup [1]:** If counts borderline, assess whether structure serves goal effectively
  - **Expected output:** Article II compliance score with quantitative counts
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Validate Article III compliance (Dual-File Mandate)
  - **Primary method:** Cross-check spec.md and parameters.toml for ID matching, structure sync, cross-references
  - **Expected output:** Article III compliance score noting any bridging failures
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Validate Article VI compliance (Critical Flag Discipline)
  - **Primary method:** Calculate critical step percentage (target: 40-60%), assess appropriateness of critical flags
  - **Expected output:** Critical balance percentage and appropriateness assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Validate Article VII compliance (Backup Methods)
  - **Primary method:** Review all backup methods to ensure they are alternative reasoning paths, not retries
  - **Backup [1]:** Sample backup methods if total exceeds 15
  - **Expected output:** Backup quality score with examples of good/poor backups
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Check Article XIV compliance (if build goal)
  - **Primary method:** If goal contains build/create/system keywords, verify software stack defined, deployment criteria present
  - **Expected output:** Article XIV compliance (N/A or pass/fail with details)
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Review Articles IV, VIII, IX, X compliance from execution
  - **Primary method:** Analyse progress.json for validation execution, error propagation, mode discipline, comprehensive logging
  - **Expected output:** Compliance scores for Articles IV, VIII, IX, X with evidence from logs
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Calculate overall constitutional compliance score
  - **Primary method:** Aggregate individual article scores, weight by severity, generate 0-100 score
  - **Expected output:** Overall compliance score (0-100) with breakdown by article
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All applicable articles assessed with evidence-based scoring
- **Logging:** Record compliance scores and violations in progress_Dev_Analysis.json

---

## Task [4]: Analyse Execution Performance Metrics

**TOML Reference:** `tasks[id=4]` in parameters_Dev_Analysis.toml  
**Purpose:** Extract quantitative performance data from execution logs with comprehensive detail

- **Step [1]:** Parse progress.json for complete step data
  - **Primary method:** Read progress_[descriptor].json, extract ALL fields: task_id, step_id, status, method_used, retry_count, timestamp, mode, critical_flag, expected_output, actual_output, error_messages
  - **Backup [1]:** If progress.json malformed, reconstruct from available logs
  - **Expected output:** Complete step outcome dataset with full detail per step
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count total steps taken
  - **Primary method:** Count: total steps defined, total steps attempted, total steps completed, total steps skipped, total steps failed
  - **Expected output:** Comprehensive step count table with breakdown by status
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Calculate detailed success and failure rates
  - **Primary method:** Compute: overall success rate, failure rate, success rate by task, failure rate by task, first-attempt success rate, eventual success rate (after retries)
  - **Expected output:** Multi-level success/failure metrics table with percentages at step, task, and SPEC levels
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse backup method usage patterns
  - **Primary method:** Count: primary method attempts, primary successes, backup[1] attempts, backup[1] successes, backup[2] attempts, backup[2] successes, calculate success rates per method type
  - **Expected output:** Comprehensive backup usage statistics with success rates, effectiveness scores, and usage frequency distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Track mode usage and escalations
  - **Primary method:** Count: steps in silent mode, steps in collaborative mode, mode switches, categorise escalation triggers (consecutive failures, backup depletion, critical failure, confidence degradation)
  - **Expected output:** Mode usage table, escalation count by trigger type, escalation appropriateness assessment per instance
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Analyse timestamps and time metrics
  - **Primary method:** Extract all timestamps from progress.json, calculate: time per step, time per task, total execution time, longest steps, shortest steps, time distribution
  - **Backup [1]:** If timestamps sparse, use available data and note gaps
  - **Expected output:** Comprehensive time metrics table with duration statistics
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Assess error propagation effectiveness
  - **Primary method:** Identify all steps with dependencies, check if prior failures were read from progress.json, assess propagation handling quality, count propagation decisions
  - **Backup [1]:** If error propagation tracking sparse, infer from step sequence and outcomes
  - **Expected output:** Error propagation effectiveness score with example instances and propagation decision breakdown
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Analyse retry patterns in detail
  - **Primary method:** Extract retry_count per step, calculate: average retries per step, max retries reached, retry exhaustion rate, retry success rate, thoroughness score (methods exhausted before escalation)
  - **Expected output:** Detailed retry pattern analysis with distribution charts and exhaustion assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Calculate efficiency and productivity metrics
  - **Primary method:** Compute: total steps attempted vs planned, steps per task (actual vs expected), average time per step, steps per hour, rework rate (retries/total), productivity score
  - **Expected output:** Comprehensive efficiency metrics table with productivity indicators
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Analyse critical vs non-critical step performance
  - **Primary method:** Separate critical and non-critical steps, compare: success rates, retry rates, time per step, failure impact
  - **Expected output:** Critical flag performance comparison table
  - **Critical:** false
  - **Mode:** silent

- **Step [11]:** Extract and analyse expected vs actual outputs
  - **Primary method:** For each step, compare expected_output defined in SPEC to actual_output logged, categorise: exact match, partial match, mismatch, missing
  - **Expected output:** Output quality assessment with match rate and mismatch analysis
  - **Critical:** true
  - **Mode:** silent

- **Step [12]:** Count and categorise all errors encountered
  - **Primary method:** Extract all error messages from progress.json, categorise by type (validation, execution, resource, logic), count occurrences, identify most frequent errors
  - **Expected output:** Error frequency table by category with top 10 most common errors
  - **Critical:** true
  - **Mode:** silent

- **Step [13]:** Analyse token usage per step (if available)
  - **Primary method:** If token counts logged, extract tokens per step, calculate: tokens per task, total tokens, token efficiency (tokens per successful step)
  - **Backup [1]:** If not logged in progress.json, skip with note
  - **Expected output:** Token usage metrics table (if data available)
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All quantitative metrics calculated with source data citations, minimum 13 metric categories documented
- **Logging:** Record all performance metrics in progress_Dev_Analysis.json

---

## Task [5]: Correlate Agent Behaviour with Goal Characteristics

**TOML Reference:** `tasks[id=5]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify relationships between goal text properties and agent execution behaviour

- **Step [1]:** Establish correlation framework
  - **Primary method:** Define metrics for correlation: goal complexity vs task count, goal clarity vs error rate, goal specificity vs backup usage
  - **Expected output:** Correlation matrix framework listing goal characteristics and behaviour metrics
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Analyse goal complexity vs task decomposition
  - **Primary method:** Correlate goal complexity score (from Task 1) with number of tasks, steps per task, decomposition depth
  - **Backup [1]:** Use qualitative assessment if quantitative correlation weak
  - **Expected output:** Correlation finding: does complex goal lead to more/fewer tasks?
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Analyse goal clarity vs execution accuracy
  - **Primary method:** Correlate goal clarity indicators (explicit requirements, measurable criteria) with success rate, error rate
  - **Expected output:** Correlation finding: does clear goal reduce errors?
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse goal specificity vs backup usage
  - **Primary method:** Correlate technical specificity score with backup invocation rate, backup effectiveness
  - **Expected output:** Correlation finding: does vague goal increase backup reliance?
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Analyse goal formatting vs agent thinking patterns
  - **Primary method:** Review agent reasoning for structured vs narrative goals, assess thinking clarity and organisation
  - **Backup [1]:** If thinking logs sparse, assess output organisation as proxy
  - **Expected output:** Qualitative finding on formatting impact with examples
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Identify confounding factors
  - **Primary method:** Check for external factors affecting correlation: SPEC complexity, domain difficulty, resource availability
  - **Expected output:** List of confounding factors that may explain behaviour patterns
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Distinguish correlation from causation
  - **Primary method:** For each correlation found, assess whether relationship is causal, coincidental, or mediated by other factors using evidence-based analysis
  - **Backup [1]:** Apply Bradford Hill criteria for causation: strength, consistency, specificity, temporality, biological gradient
  - **Expected output:** Causality assessment for each correlation with confidence level and supporting evidence
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Minimum 3 behaviour correlations identified with specific evidence
- **Logging:** Record correlations and causality assessments in progress_Dev_Analysis.json

---

## Task [6]: Assess Per-Task and Per-Step Behaviour Quality

**TOML Reference:** `tasks[id=6]` in parameters_Dev_Analysis.toml  
**Purpose:** Evaluate quality of task decomposition and step execution at granular level

- **Step [1]:** Evaluate task decomposition quality
  - **Primary method:** For each task, assess: Does task serve goal? Is task scope appropriate? Is task self-contained?
  - **Expected output:** Task quality assessment table with scores and rationale per task
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Assess step atomicity
  - **Primary method:** For each step, assess: Is step a single concrete action? Is step scope too broad/narrow? Is step executable?
  - **Backup [1]:** Sample steps if total exceeds 20
  - **Expected output:** Step atomicity assessment with examples of well/poorly scoped steps
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Evaluate critical flag appropriateness
  - **Primary method:** For each critical step, verify: Would failure truly block goal? For non-critical, verify: Can goal succeed without this?
  - **Expected output:** Critical flag appropriateness score with misclassification examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess expected output clarity
  - **Primary method:** For each step, rate expected output: specific/vague, measurable/subjective, achievable/unrealistic
  - **Expected output:** Expected output quality assessment with clarity distribution
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Evaluate method selection rationale
  - **Primary method:** For steps with multiple methods, assess whether primary/backup choices were well-justified
  - **Expected output:** Method selection quality score with examples
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All tasks and representative sample of steps assessed for quality
- **Logging:** Record quality assessments in progress_Dev_Analysis.json

---

## Task [7]: Conduct Comprehensive Error Analysis and Pattern Detection

**TOML Reference:** `tasks[id=7]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify error patterns, root causes, and improvement opportunities through meticulous analysis

- **Step [1]:** Extract and inventory all error sources
  - **Primary method:** Collect errors from: progress.json, error log files (from Task 0), chat logs, validation reports, any other error documentation
  - **Expected output:** Complete error inventory with source file paths and line references
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count total errors across all sources
  - **Primary method:** Count: total errors logged, errors per source type, errors per task, errors per step, error density (errors per 100 steps)
  - **Expected output:** Comprehensive error count table with breakdowns
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Categorise all errors by type and severity
  - **Primary method:** Classify each error by type (validation, execution, resource, logic, syntax, semantic) and severity (critical, major, minor, warning)
  - **Expected output:** Error categorisation matrix with counts and percentages by type and severity
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse error log files in detail
  - **Primary method:** For each error log file identified in Task 0, parse contents, extract: error timestamps, error messages, stack traces, context, frequency
  - **Backup [1]:** If logs are unstructured, extract what's available and note format issues
  - **Expected output:** Detailed error log analysis with structured data extracted from logs
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify error frequency patterns and hotspots
  - **Primary method:** Analyse which tasks/steps had highest error rates, identify repeated failures, calculate error concentration by task/step/time period
  - **Expected output:** Error hotspot analysis showing: high-error tasks, high-error steps, error clustering patterns, temporal error distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Conduct comprehensive root cause analysis
  - **Primary method:** For each error category, trace to root cause: SPEC design flaw, step definition ambiguity, resource limitation, goal ambiguity, external dependency, constitutional violation, tooling issue
  - **Backup [1]:** Apply 5 Whys methodology for complex errors
  - **Expected output:** Root cause mapping for all error categories with prevention recommendations per cause
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Analyse error propagation chains
  - **Primary method:** Trace errors that caused downstream failures, identify cascading error patterns, assess propagation handling
  - **Expected output:** Error propagation chain diagram with cascade analysis
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Assess recovery effectiveness and time
  - **Primary method:** For each error, determine: was it recovered? which method succeeded? how many attempts? time to recovery? was escalation needed?
  - **Expected output:** Recovery effectiveness metrics: recovery rate, average attempts to recovery, average time to recovery, escalation rate, recovery method distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Analyse error messages for clarity and actionability
  - **Primary method:** Review all error messages, rate: clarity (clear/vague), actionability (specific guidance/generic), completeness (context provided/missing)
  - **Expected output:** Error message quality assessment with examples of good/poor messages
  - **Critical:** false
  - **Mode:** silent

- **Step [10]:** Identify constitutional violations
  - **Primary method:** Check progress.json constitutional_compliance section, extract violations; cross-reference error patterns with constitutional articles
  - **Backup [1]:** Manual review of execution logs if compliance tracking absent
  - **Expected output:** Constitutional violation summary with article breakdown, severity, and correlation to errors
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Distinguish preventable from inherent errors
  - **Primary method:** Classify each error: preventable through better SPEC design, preventable through better execution, inherent to task complexity, external/environmental, resource-based
  - **Expected output:** Error preventability classification with percentages and improvement focus areas
  - **Critical:** true
  - **Mode:** silent

- **Step [12]:** Calculate error-related time costs
  - **Primary method:** Sum time spent on: failed steps, retries, error recovery, escalations, rework
  - **Backup [1]:** Estimate if precise timestamps unavailable
  - **Expected output:** Error cost metrics: time lost to errors, percentage of total time, cost per error category
  - **Critical:** false
  - **Mode:** silent

- **Step [13]:** Identify error patterns by goal characteristics
  - **Primary method:** Correlate error rates/types with goal complexity, clarity, specificity metrics from Task 1
  - **Expected output:** Error pattern correlation analysis linking errors to goal characteristics
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All errors from all sources analysed with root causes, minimum 13 error metric categories documented
- **Logging:** Record comprehensive error analysis findings in progress_Dev_Analysis.json

---

## Task [8]: Generate Comprehensive Analysis Report with Recommendations

**TOML Reference:** `tasks[id=8]` in parameters_Dev_Analysis.toml  
**Purpose:** Synthesise all findings into actionable report

- **Step [1]:** Structure report outline
  - **Primary method:** Create report sections: Executive Summary, Goal Analysis, Propagation Findings, Performance Metrics, Correlations, Quality Assessment, Error Analysis, Recommendations
  - **Expected output:** Report outline with section headers
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Write Executive Summary
  - **Primary method:** Synthesise key findings: goal characteristics summary, main propagation patterns, overall performance, critical insights
  - **Expected output:** 200-300 word executive summary highlighting main findings
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Compile Goal Text Analysis section
  - **Primary method:** Aggregate Task 1 findings: goal characteristics table, complexity assessment, element breakdown
  - **Expected output:** Goal Text Analysis section with all metrics and assessments
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Compile Goal Text Propagation section
  - **Primary method:** Aggregate Task 2 findings: propagation examples, language flow diagram, conceptual drift assessment
  - **Expected output:** Goal Text Propagation section with minimum 3 concrete examples with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Compile Constitutional Compliance section
  - **Primary method:** Aggregate Task 3 findings: article-by-article scores, overall compliance score, violation summary
  - **Expected output:** Constitutional Compliance section with compliance scorecard
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Compile Execution Performance section
  - **Primary method:** Aggregate Task 4 findings: success/failure rates, backup usage, mode escalations, efficiency metrics
  - **Expected output:** Execution Performance section with metrics tables
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Compile Behaviour Correlation section
  - **Primary method:** Aggregate Task 5 findings: correlation matrix, causality assessments, confounding factors
  - **Expected output:** Behaviour Correlation section with correlation findings
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Compile Quality Assessment section
  - **Primary method:** Aggregate Task 6 findings: task quality scores, step atomicity, critical flag appropriateness
  - **Expected output:** Quality Assessment section with quality distributions
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Compile Error Analysis section
  - **Primary method:** Aggregate Task 7 findings: error categories, root causes, recovery effectiveness, preventability
  - **Expected output:** Error Analysis section with error breakdown and patterns
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Generate actionable recommendations
  - **Primary method:** Based on all findings, create specific recommendations for: goal formulation improvement, SPEC design enhancement, execution optimisation, constitutional compliance
  - **Backup [1]:** If recommendations unclear, escalate to collaborative mode for human input
  - **Expected output:** Minimum 5 specific, actionable recommendations linked to findings
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Add cross-project comparison framework (if applicable)
  - **Primary method:** If analysing multiple SPECs, create comparison tables for key metrics across projects
  - **Expected output:** Cross-project comparison section (optional, only if multiple projects analysed)
  - **Critical:** false
  - **Mode:** silent

- **Step [12]:** Finalise report formatting and references
  - **Primary method:** Ensure all sections formatted consistently, add table of contents, verify all data citations present
  - **Expected output:** Complete, polished analysis report in markdown format
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Report contains all required sections, metrics are evidence-based, recommendations are actionable
- **Logging:** Record report completion in progress_Dev_Analysis.json with final deliverable path

---

## Bridging: Markdown ↔ TOML Synchronisation

This spec file (Dev_Analysis_SPEC.md) must maintain perfect alignment with its companion file (parameters_Dev_Analysis.toml).

**Bridging Requirements:**
1. Each task in this file must have corresponding `[[tasks]]` entry in TOML with matching ID (1-8)
2. Each step within a task must have corresponding `[[tasks.steps]]` entry with matching ID
3. Expected outputs in this file must match `expected_output` fields in TOML
4. Critical flags must be synchronised between files
5. Constraints referenced must exist in TOML `[constraints]` section

**Example Cross-References:**
- "See `constraints.min_examples_required` in parameters_Dev_Analysis.toml" (Task 2, Step 4)
- "As defined in `tasks[id=4]` in TOML" (Task 4 reference)
- "Must satisfy TOML verification requirements" (All task verifications)

The exe_Dev_Analysis.md controller will validate this synchronisation during initialisation (Section 1.8).

---

## Instructions for LLM Executor

1. **Start with goal understanding**: This analysis examines how goal text propagates and influences SPEC development
2. **Execute tasks sequentially**: Tasks 1-2 gather data, Tasks 3-7 analyse patterns, Task 8 synthesises findings
3. **Maintain objectivity**: Base all findings on evidence from files, logs, and artefacts
4. **Track propagation carefully**: Pay special attention to how exact goal language appears throughout project
5. **Quantify where possible**: Use numerical metrics rather than subjective assessments when feasible
6. **Distinguish correlation from causation**: Note relationships but assess causality carefully
7. **Document thoroughly**: Log all findings in progress_Dev_Analysis.json for traceability
8. **Focus on actionability**: Recommendations should be specific and implementable
9. **Read prior outcomes**: Before each step, check progress.json for relevant prior findings
10. **Escalate appropriately**: Use collaborative mode for causality judgements and unclear recommendation priorities

---

## Expected Analysis Output Structure

The final report should follow this structure:

```markdown
# SPEC Development Analysis Report

## Executive Summary
[200-300 word overview of key findings]

## 1. Goal Text Analysis
### 1.1 Initial Goal Characteristics
- Quantitative metrics table
- Complexity classification
- Element breakdown

### 1.2 Technical Specificity Assessment
- Specificity score with justification
- Domain terminology analysis

## 2. Goal Text Propagation Analysis
### 2.1 Propagation Through Tasks
- Task-level language mapping
- Specific examples with quotes

### 2.2 Propagation Through Steps
- Step-level language mapping
- Propagation matrix

### 2.3 Agent Thinking Patterns
- Minimum 3 examples of goal text in reasoning
- Direct quotes from logs/chat

### 2.4 Conceptual Drift Assessment
- Identified divergences
- Impact analysis

## 3. Constitutional Compliance Assessment
### 3.1 Article-by-Article Scores
- Individual article compliance
- Evidence for each assessment

### 3.2 Overall Compliance Score
- Aggregate score (0-100)
- Violation summary

## 4. Execution Performance Metrics
### 4.1 Success and Failure Rates
- Quantitative metrics table
- Rate comparisons

### 4.2 Backup Method Usage
- Usage statistics
- Effectiveness assessment

### 4.3 Mode Escalations
- Escalation count and triggers
- Appropriateness evaluation

### 4.4 Efficiency Metrics
- Steps per task
- Time analysis (if available)

## 5. Behaviour Correlation Analysis
### 5.1 Identified Correlations
- Goal characteristics vs execution behaviour
- Correlation strength assessment

### 5.2 Causality Assessment
- Causal vs correlational relationships
- Confidence levels

### 5.3 Confounding Factors
- External influences
- Mediation effects

## 6. Quality Assessment
### 6.1 Task Decomposition Quality
- Per-task quality scores
- Decomposition effectiveness

### 6.2 Step Quality Analysis
- Atomicity assessment
- Critical flag appropriateness

### 6.3 Method Selection Quality
- Primary/backup rationale
- Method effectiveness

## 7. Error Analysis
### 7.1 Error Categorisation
- Error type distribution
- Frequency patterns

### 7.2 Root Cause Analysis
- Root cause mapping
- Prevention opportunities

### 7.3 Recovery Effectiveness
- Recovery success rates
- Backup effectiveness

### 7.4 Constitutional Violations
- Violation breakdown by article
- Severity assessment

## 8. Recommendations
### 8.1 Goal Formulation Improvements
[Specific, actionable recommendations]

### 8.2 SPEC Design Enhancements
[Specific, actionable recommendations]

### 8.3 Execution Optimisation
[Specific, actionable recommendations]

### 8.4 Constitutional Compliance
[Specific, actionable recommendations]

### 8.5 Future Research Directions
[Areas for deeper investigation]

## Appendices
### A. Raw Data Tables
### B. Propagation Examples (Full Quotes)
### C. Metrics Calculation Methods
### D. Source Citations
```

---

**End of Dev_Analysis_SPEC.md**

This SPEC is designed to be reusable across multiple test SPEC analyses, enabling systematic comparison and pattern identification.


```

```markdown
# Dev Analysis SPEC

**Version:** 1.0  
**Last Updated:** 2025-11-03  
**Purpose:** Analyse development of test SPECs to identify patterns, metrics, and goal text propagation effects

---

## Goal

Perform comprehensive analysis of a test SPEC's development lifecycle to identify how initial goal text propagates through the system and impacts agent behaviour, execution accuracy, and project outcomes.

---

## Software Stack & Architecture

**Not Applicable** - This is an analysis task, not a build goal.

---

## Definition of Complete

What must exist and be verified:
- [ ] **Primary deliverable:** Comprehensive analysis report (markdown format) covering all analysis areas
- [ ] **Quality standards met:** 
  - All 8 analysis tasks completed with documented findings
  - Goal text propagation patterns identified with specific examples
  - Quantitative metrics calculated for execution performance
  - Cross-correlation analysis between goal characteristics and outcomes
  - Recommendations provided based on findings
- [ ] **Verification method:** 
  - Report contains all required sections (see tasks below)
  - Quantitative metrics include numerical values with source citations
  - At least 3 specific examples of goal text propagation documented
  - Recommendations are actionable and linked to specific findings

---

## Definitions

- **goal**: Analyse how initial goal text characteristics influence SPEC development and execution
- **task[n]**: Discrete analysis objectives examining different aspects of SPEC development
- **step[m]**: Concrete analytical actions within each task
- **backup[p]**: Alternative analysis methods when primary approach is blocked
- **critical_flag**: Boolean indicating whether analysis step is essential to overall goal
- **mode**: `silent` (fully autonomous - NO USER INPUT REQUIRED except initial project folder location)
- **progress.json**: Structured log tracking analysis execution and findings
- **project_folder**: Target development project folder path (ONLY required user input)

---

## Components

Analysis requires access to:
- **Test SPEC files:** spec_[descriptor].md, parameters_[descriptor].toml, exe_[descriptor].md
- **Execution logs:** progress_[descriptor].json
- **Project artefacts:** Code files, documentation, error logs, validation reports
- **Chat history:** Conversation transcripts showing agent thinking and decision-making
- **Constitution:** __SPEC_Engine/_Constitution/constitution.md for compliance checking

**Machine-Readable Components:**  
See `[components]` section in parameters_Dev_Analysis.toml

---

## Constraints

- Analysis must be objective and evidence-based
- All metrics must be traceable to source data
- Goal text propagation analysis must include minimum 3 concrete examples
- Quantitative metrics must include: success rates, error rates, mode escalations, backup usage
- Findings must distinguish correlation from causation
- Recommendations must be specific and actionable

**Machine-Readable Constraints:**  
See `[constraints]` section in parameters_Dev_Analysis.toml:
- `min_examples_required = 3` (goal text propagation examples)
- `metrics_evidence_based = true` (all metrics must cite sources)
- `recommendation_specificity = "actionable"` (recommendations must be implementable)

---

## User Stories

- As a **SPEC developer**, I want to understand how goal phrasing impacts development so I can write more effective goals
- As a **system architect**, I want to identify patterns in SPEC execution so I can improve the framework
- As a **researcher**, I want to quantify goal text propagation so I can understand agent behaviour correlation
- As a **project manager**, I want metrics on SPEC performance so I can assess project quality

---

## Analysis Framework

This SPEC analyses development across 8 integrated dimensions:

### Dimension 1: Goal Text Characteristics
- Length (word count, character count, sentence complexity)
- Number of distinct elements/requirements
- Literacy level (Flesch-Kincaid, technical density)
- Formatting (structure, lists, emphasis)
- Familiarity/Technical specificity

### Dimension 2: Goal Text Propagation
- How goal language appears in task descriptions
- Goal terminology in step definitions
- Phrasing patterns in agent thinking/reasoning
- Language consistency across SPEC artefacts
- Conceptual drift from goal to implementation

### Dimension 3: Constitutional Compliance
- Article I-XIV adherence scoring
- Critical flag balance (target: 40-60%)
- Backup method quality assessment
- Bridging quality (Markdown-TOML sync)
- Validation checkpoint outcomes

### Dimension 4: Execution Performance
- Step success/failure rates
- Backup invocation frequency
- Mode escalation patterns
- Error propagation effectiveness
- Retry patterns and exhaustion

### Dimension 5: Agent Behaviour Correlation
- Thinking patterns vs goal complexity
- Decision quality vs goal clarity
- Output quality vs goal specificity
- Backup selection vs goal ambiguity
- Escalation triggers vs goal characteristics

### Dimension 6: Per-Task/Step Behaviour
- Task decomposition quality
- Step atomicity assessment
- Critical flag appropriateness
- Expected output clarity
- Method selection rationale

### Dimension 7: Error Analysis
- Error types and frequencies
- Root cause patterns
- Recovery effectiveness
- Constitutional violations
- Preventable vs inherent errors

### Dimension 8: Outcome Metrics
- Goal achievement status (ACHIEVED/PARTIAL/NOT_ACHIEVED)
- Deliverable completeness
- Quality standards met
- Time/step efficiency
- Comparison to expected outcomes

---

## Task [0]: Initialize Analysis and Gather Project Metadata

**TOML Reference:** `tasks[id=0]` in parameters_Dev_Analysis.toml  
**Purpose:** Locate project folder, scan structure, and collect comprehensive metadata

- **Step [0]:** Receive project folder location (ONLY USER INPUT REQUIRED)
  - **Primary method:** Prompt for project development folder path
  - **Expected output:** Absolute path to project folder
  - **Critical:** true
  - **Mode:** collaborative (ONE TIME ONLY - for folder path input)

- **Step [1]:** Scan and map complete project structure
  - **Primary method:** Recursively list all files and directories in project folder
  - **Backup [1]:** If permissions issue, request accessible subset of project
  - **Expected output:** Complete file tree with full paths
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count and categorise all files
  - **Primary method:** Count files by type: .md, .toml, .json, .py, .js, .ts, .log, .txt, etc.
  - **Expected output:** File count table with breakdown by extension
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Calculate file sizes and total project size
  - **Primary method:** Get file size for each file, sum by category and total
  - **Expected output:** Size metrics table (bytes, KB, MB) by file type and total
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Extract all timestamps
  - **Primary method:** Collect creation, modification, access times for all relevant files
  - **Backup [1]:** If timestamps unavailable, use git history if present
  - **Expected output:** Timeline table showing project chronology
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Calculate development duration
  - **Primary method:** Calculate time from earliest to latest timestamp, identify development phases
  - **Expected output:** Development duration metrics: total time, active development periods, gaps
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Count tokens across all text files
  - **Primary method:** For each text-based file, count tokens (words, characters, estimated LLM tokens)
  - **Backup [1]:** If token counting unavailable, use word/character counts as proxy
  - **Expected output:** Token count table by file type with totals
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Identify and catalogue error logs
  - **Primary method:** Locate all error log files, count error entries, categorise by severity
  - **Expected output:** Error log inventory with counts and locations
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Identify and catalogue chat/conversation logs
  - **Primary method:** Locate chat transcripts, conversation logs, agent thinking logs
  - **Backup [1]:** Check common locations: root, logs folder, subdirectories
  - **Expected output:** Conversation log inventory with file paths and sizes
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Count conversation turns and messages
  - **Primary method:** Parse chat logs to count: total messages, user messages, agent messages, turns
  - **Expected output:** Conversation metrics table
  - **Critical:** false
  - **Mode:** silent

- **Step [10]:** Identify SPEC files and versions
  - **Primary method:** Locate all spec_*.md, parameters_*.toml, exe_*.md, progress_*.json files
  - **Expected output:** SPEC file inventory with versions and timestamps
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Create project metadata snapshot
  - **Primary method:** Aggregate all collected metrics into comprehensive metadata document
  - **Expected output:** Project metadata JSON with all metrics organized
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Project folder scanned, all files catalogued, comprehensive metrics collected
- **Logging:** Record all metadata in progress_Dev_Analysis.json for reference throughout analysis

---

## Task [1]: Extract and Characterise Initial Goal Text

**TOML Reference:** `tasks[id=1]` in parameters_Dev_Analysis.toml  
**Purpose:** Establish baseline characteristics of the goal that initiated SPEC development

- **Step [1]:** Locate and extract initial goal text
  - **Primary method:** Read SPEC markdown file Goal section and chat history for original user goal statement
  - **Backup [1]:** If chat history unavailable, use goal section from spec_[descriptor].md as proxy
  - **Expected output:** Exact goal text with source citation and timestamp
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Calculate quantitative text characteristics
  - **Primary method:** Compute word count, character count, sentence count, avg sentence length, Flesch-Kincaid score
  - **Backup [1]:** If automated scoring unavailable, perform manual classification (simple/moderate/complex)
  - **Expected output:** Table with numerical metrics and complexity classification
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Identify distinct elements and requirements
  - **Primary method:** Parse goal for discrete requirements, constraints, deliverables, success criteria
  - **Backup [1]:** Use linguistic chunking to identify conceptual units if structure unclear
  - **Expected output:** Numbered list of distinct elements (target: 3-10 elements)
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess technical specificity and domain familiarity
  - **Primary method:** Identify technical terms, domain-specific language, assumed knowledge, explicit vs implicit requirements
  - **Backup [1]:** Compare vocabulary against common vs specialised term databases
  - **Expected output:** Technical specificity score (1-5 scale) with justification and term examples
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Analyse formatting and structure
  - **Primary method:** Document use of lists, emphasis, sections, explicit vs narrative format
  - **Expected output:** Formatting assessment noting structural elements present
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All goal characteristics documented with quantitative metrics where possible
- **Logging:** Record all measurements in progress_Dev_Analysis.json for correlation analysis

---

## Task [2]: Map Goal Text Propagation Throughout Project

**TOML Reference:** `tasks[id=2]` in parameters_Dev_Analysis.toml  
**Purpose:** Track how initial goal language and concepts propagate through SPEC artefacts

- **Step [1]:** Extract task descriptions from SPEC
  - **Primary method:** Parse spec_[descriptor].md for all task titles and descriptions
  - **Expected output:** List of tasks with full text
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify goal language in task descriptions
  - **Primary method:** Compare task descriptions to goal text, noting shared terminology, conceptual overlap, verbatim phrases
  - **Backup [1]:** Use semantic similarity scoring if direct comparison insufficient
  - **Expected output:** Table mapping goal terms to task descriptions with similarity scores
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Extract step definitions and analyse propagation
  - **Primary method:** Parse all step descriptions, identify goal/task terminology presence, track conceptual consistency
  - **Backup [1]:** Focus on critical steps only if volume is high (>20 steps)
  - **Expected output:** Propagation matrix showing goal→task→step language flow with specific examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse agent thinking and reasoning patterns
  - **Primary method:** Review chat history/logs for agent internal reasoning, note how goal concepts appear in thinking
  - **Backup [1]:** If full chat unavailable, analyse progress.json logs for method justifications
  - **Expected output:** Minimum 3 specific examples of goal text influencing agent reasoning with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify conceptual drift
  - **Primary method:** Compare final implementation/outputs against original goal, identify divergences in terminology, scope, or interpretation
  - **Expected output:** Conceptual drift assessment noting where implementation departed from goal language
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Assess language consistency across artefacts
  - **Primary method:** Check terminology consistency across spec.md, parameters.toml, progress.json, deliverables
  - **Expected output:** Consistency report identifying where language fragmented or evolved
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Minimum 3 concrete examples of goal text propagation documented with direct quotes
- **Logging:** Record propagation patterns and drift instances in progress_Dev_Analysis.json

---

## Task [3]: Evaluate Constitutional Compliance

**TOML Reference:** `tasks[id=3]` in parameters_Dev_Analysis.toml  
**Purpose:** Assess adherence to SPEC Engine Constitution (Articles I-XIV)

- **Step [1]:** Validate Article I compliance (North Star Principle)
  - **Primary method:** Verify goal singularity, clarity, measurability, explicitness
  - **Expected output:** Article I compliance score (pass/fail) with justification
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Validate Article II compliance (Hierarchical Structure)
  - **Primary method:** Count tasks (target: 2-5), count steps per task (target: 1-5), verify hierarchy maintained
  - **Backup [1]:** If counts borderline, assess whether structure serves goal effectively
  - **Expected output:** Article II compliance score with quantitative counts
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Validate Article III compliance (Dual-File Mandate)
  - **Primary method:** Cross-check spec.md and parameters.toml for ID matching, structure sync, cross-references
  - **Expected output:** Article III compliance score noting any bridging failures
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Validate Article VI compliance (Critical Flag Discipline)
  - **Primary method:** Calculate critical step percentage (target: 40-60%), assess appropriateness of critical flags
  - **Expected output:** Critical balance percentage and appropriateness assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Validate Article VII compliance (Backup Methods)
  - **Primary method:** Review all backup methods to ensure they are alternative reasoning paths, not retries
  - **Backup [1]:** Sample backup methods if total exceeds 15
  - **Expected output:** Backup quality score with examples of good/poor backups
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Check Article XIV compliance (if build goal)
  - **Primary method:** If goal contains build/create/system keywords, verify software stack defined, deployment criteria present
  - **Expected output:** Article XIV compliance (N/A or pass/fail with details)
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Review Articles IV, VIII, IX, X compliance from execution
  - **Primary method:** Analyse progress.json for validation execution, error propagation, mode discipline, comprehensive logging
  - **Expected output:** Compliance scores for Articles IV, VIII, IX, X with evidence from logs
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Calculate overall constitutional compliance score
  - **Primary method:** Aggregate individual article scores, weight by severity, generate 0-100 score
  - **Expected output:** Overall compliance score (0-100) with breakdown by article
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All applicable articles assessed with evidence-based scoring
- **Logging:** Record compliance scores and violations in progress_Dev_Analysis.json

---

## Task [4]: Analyse Execution Performance Metrics

**TOML Reference:** `tasks[id=4]` in parameters_Dev_Analysis.toml  
**Purpose:** Extract quantitative performance data from execution logs with comprehensive detail

- **Step [1]:** Parse progress.json for complete step data
  - **Primary method:** Read progress_[descriptor].json, extract ALL fields: task_id, step_id, status, method_used, retry_count, timestamp, mode, critical_flag, expected_output, actual_output, error_messages
  - **Backup [1]:** If progress.json malformed, reconstruct from available logs
  - **Expected output:** Complete step outcome dataset with full detail per step
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count total steps taken
  - **Primary method:** Count: total steps defined, total steps attempted, total steps completed, total steps skipped, total steps failed
  - **Expected output:** Comprehensive step count table with breakdown by status
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Calculate detailed success and failure rates
  - **Primary method:** Compute: overall success rate, failure rate, success rate by task, failure rate by task, first-attempt success rate, eventual success rate (after retries)
  - **Expected output:** Multi-level success/failure metrics table with percentages at step, task, and SPEC levels
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse backup method usage patterns
  - **Primary method:** Count: primary method attempts, primary successes, backup[1] attempts, backup[1] successes, backup[2] attempts, backup[2] successes, calculate success rates per method type
  - **Expected output:** Comprehensive backup usage statistics with success rates, effectiveness scores, and usage frequency distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Track mode usage and escalations
  - **Primary method:** Count: steps in silent mode, steps in collaborative mode, mode switches, categorise escalation triggers (consecutive failures, backup depletion, critical failure, confidence degradation)
  - **Expected output:** Mode usage table, escalation count by trigger type, escalation appropriateness assessment per instance
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Analyse timestamps and time metrics
  - **Primary method:** Extract all timestamps from progress.json, calculate: time per step, time per task, total execution time, longest steps, shortest steps, time distribution
  - **Backup [1]:** If timestamps sparse, use available data and note gaps
  - **Expected output:** Comprehensive time metrics table with duration statistics
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Assess error propagation effectiveness
  - **Primary method:** Identify all steps with dependencies, check if prior failures were read from progress.json, assess propagation handling quality, count propagation decisions
  - **Backup [1]:** If error propagation tracking sparse, infer from step sequence and outcomes
  - **Expected output:** Error propagation effectiveness score with example instances and propagation decision breakdown
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Analyse retry patterns in detail
  - **Primary method:** Extract retry_count per step, calculate: average retries per step, max retries reached, retry exhaustion rate, retry success rate, thoroughness score (methods exhausted before escalation)
  - **Expected output:** Detailed retry pattern analysis with distribution charts and exhaustion assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Calculate efficiency and productivity metrics
  - **Primary method:** Compute: total steps attempted vs planned, steps per task (actual vs expected), average time per step, steps per hour, rework rate (retries/total), productivity score
  - **Expected output:** Comprehensive efficiency metrics table with productivity indicators
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Analyse critical vs non-critical step performance
  - **Primary method:** Separate critical and non-critical steps, compare: success rates, retry rates, time per step, failure impact
  - **Expected output:** Critical flag performance comparison table
  - **Critical:** false
  - **Mode:** silent

- **Step [11]:** Extract and analyse expected vs actual outputs
  - **Primary method:** For each step, compare expected_output defined in SPEC to actual_output logged, categorise: exact match, partial match, mismatch, missing
  - **Expected output:** Output quality assessment with match rate and mismatch analysis
  - **Critical:** true
  - **Mode:** silent

- **Step [12]:** Count and categorise all errors encountered
  - **Primary method:** Extract all error messages from progress.json, categorise by type (validation, execution, resource, logic), count occurrences, identify most frequent errors
  - **Expected output:** Error frequency table by category with top 10 most common errors
  - **Critical:** true
  - **Mode:** silent

- **Step [13]:** Analyse token usage per step (if available)
  - **Primary method:** If token counts logged, extract tokens per step, calculate: tokens per task, total tokens, token efficiency (tokens per successful step)
  - **Backup [1]:** If not logged in progress.json, skip with note
  - **Expected output:** Token usage metrics table (if data available)
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All quantitative metrics calculated with source data citations, minimum 13 metric categories documented
- **Logging:** Record all performance metrics in progress_Dev_Analysis.json

---

## Task [5]: Correlate Agent Behaviour with Goal Characteristics

**TOML Reference:** `tasks[id=5]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify relationships between goal text properties and agent execution behaviour

- **Step [1]:** Establish correlation framework
  - **Primary method:** Define metrics for correlation: goal complexity vs task count, goal clarity vs error rate, goal specificity vs backup usage
  - **Expected output:** Correlation matrix framework listing goal characteristics and behaviour metrics
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Analyse goal complexity vs task decomposition
  - **Primary method:** Correlate goal complexity score (from Task 1) with number of tasks, steps per task, decomposition depth
  - **Backup [1]:** Use qualitative assessment if quantitative correlation weak
  - **Expected output:** Correlation finding: does complex goal lead to more/fewer tasks?
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Analyse goal clarity vs execution accuracy
  - **Primary method:** Correlate goal clarity indicators (explicit requirements, measurable criteria) with success rate, error rate
  - **Expected output:** Correlation finding: does clear goal reduce errors?
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse goal specificity vs backup usage
  - **Primary method:** Correlate technical specificity score with backup invocation rate, backup effectiveness
  - **Expected output:** Correlation finding: does vague goal increase backup reliance?
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Analyse goal formatting vs agent thinking patterns
  - **Primary method:** Review agent reasoning for structured vs narrative goals, assess thinking clarity and organisation
  - **Backup [1]:** If thinking logs sparse, assess output organisation as proxy
  - **Expected output:** Qualitative finding on formatting impact with examples
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Identify confounding factors
  - **Primary method:** Check for external factors affecting correlation: SPEC complexity, domain difficulty, resource availability
  - **Expected output:** List of confounding factors that may explain behaviour patterns
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Distinguish correlation from causation
  - **Primary method:** For each correlation found, assess whether relationship is causal, coincidental, or mediated by other factors using evidence-based analysis
  - **Backup [1]:** Apply Bradford Hill criteria for causation: strength, consistency, specificity, temporality, biological gradient
  - **Expected output:** Causality assessment for each correlation with confidence level and supporting evidence
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Minimum 3 behaviour correlations identified with specific evidence
- **Logging:** Record correlations and causality assessments in progress_Dev_Analysis.json

---

## Task [6]: Assess Per-Task and Per-Step Behaviour Quality

**TOML Reference:** `tasks[id=6]` in parameters_Dev_Analysis.toml  
**Purpose:** Evaluate quality of task decomposition and step execution at granular level

- **Step [1]:** Evaluate task decomposition quality
  - **Primary method:** For each task, assess: Does task serve goal? Is task scope appropriate? Is task self-contained?
  - **Expected output:** Task quality assessment table with scores and rationale per task
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Assess step atomicity
  - **Primary method:** For each step, assess: Is step a single concrete action? Is step scope too broad/narrow? Is step executable?
  - **Backup [1]:** Sample steps if total exceeds 20
  - **Expected output:** Step atomicity assessment with examples of well/poorly scoped steps
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Evaluate critical flag appropriateness
  - **Primary method:** For each critical step, verify: Would failure truly block goal? For non-critical, verify: Can goal succeed without this?
  - **Expected output:** Critical flag appropriateness score with misclassification examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess expected output clarity
  - **Primary method:** For each step, rate expected output: specific/vague, measurable/subjective, achievable/unrealistic
  - **Expected output:** Expected output quality assessment with clarity distribution
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Evaluate method selection rationale
  - **Primary method:** For steps with multiple methods, assess whether primary/backup choices were well-justified
  - **Expected output:** Method selection quality score with examples
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All tasks and representative sample of steps assessed for quality
- **Logging:** Record quality assessments in progress_Dev_Analysis.json

---

## Task [7]: Conduct Comprehensive Error Analysis and Pattern Detection

**TOML Reference:** `tasks[id=7]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify error patterns, root causes, and improvement opportunities through meticulous analysis

- **Step [1]:** Extract and inventory all error sources
  - **Primary method:** Collect errors from: progress.json, error log files (from Task 0), chat logs, validation reports, any other error documentation
  - **Expected output:** Complete error inventory with source file paths and line references
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count total errors across all sources
  - **Primary method:** Count: total errors logged, errors per source type, errors per task, errors per step, error density (errors per 100 steps)
  - **Expected output:** Comprehensive error count table with breakdowns
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Categorise all errors by type and severity
  - **Primary method:** Classify each error by type (validation, execution, resource, logic, syntax, semantic) and severity (critical, major, minor, warning)
  - **Expected output:** Error categorisation matrix with counts and percentages by type and severity
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse error log files in detail
  - **Primary method:** For each error log file identified in Task 0, parse contents, extract: error timestamps, error messages, stack traces, context, frequency
  - **Backup [1]:** If logs are unstructured, extract what's available and note format issues
  - **Expected output:** Detailed error log analysis with structured data extracted from logs
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify error frequency patterns and hotspots
  - **Primary method:** Analyse which tasks/steps had highest error rates, identify repeated failures, calculate error concentration by task/step/time period
  - **Expected output:** Error hotspot analysis showing: high-error tasks, high-error steps, error clustering patterns, temporal error distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Conduct comprehensive root cause analysis
  - **Primary method:** For each error category, trace to root cause: SPEC design flaw, step definition ambiguity, resource limitation, goal ambiguity, external dependency, constitutional violation, tooling issue
  - **Backup [1]:** Apply 5 Whys methodology for complex errors
  - **Expected output:** Root cause mapping for all error categories with prevention recommendations per cause
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Analyse error propagation chains
  - **Primary method:** Trace errors that caused downstream failures, identify cascading error patterns, assess propagation handling
  - **Expected output:** Error propagation chain diagram with cascade analysis
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Assess recovery effectiveness and time
  - **Primary method:** For each error, determine: was it recovered? which method succeeded? how many attempts? time to recovery? was escalation needed?
  - **Expected output:** Recovery effectiveness metrics: recovery rate, average attempts to recovery, average time to recovery, escalation rate, recovery method distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Analyse error messages for clarity and actionability
  - **Primary method:** Review all error messages, rate: clarity (clear/vague), actionability (specific guidance/generic), completeness (context provided/missing)
  - **Expected output:** Error message quality assessment with examples of good/poor messages
  - **Critical:** false
  - **Mode:** silent

- **Step [10]:** Identify constitutional violations
  - **Primary method:** Check progress.json constitutional_compliance section, extract violations; cross-reference error patterns with constitutional articles
  - **Backup [1]:** Manual review of execution logs if compliance tracking absent
  - **Expected output:** Constitutional violation summary with article breakdown, severity, and correlation to errors
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Distinguish preventable from inherent errors
  - **Primary method:** Classify each error: preventable through better SPEC design, preventable through better execution, inherent to task complexity, external/environmental, resource-based
  - **Expected output:** Error preventability classification with percentages and improvement focus areas
  - **Critical:** true
  - **Mode:** silent

- **Step [12]:** Calculate error-related time costs
  - **Primary method:** Sum time spent on: failed steps, retries, error recovery, escalations, rework
  - **Backup [1]:** Estimate if precise timestamps unavailable
  - **Expected output:** Error cost metrics: time lost to errors, percentage of total time, cost per error category
  - **Critical:** false
  - **Mode:** silent

- **Step [13]:** Identify error patterns by goal characteristics
  - **Primary method:** Correlate error rates/types with goal complexity, clarity, specificity metrics from Task 1
  - **Expected output:** Error pattern correlation analysis linking errors to goal characteristics
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All errors from all sources analysed with root causes, minimum 13 error metric categories documented
- **Logging:** Record comprehensive error analysis findings in progress_Dev_Analysis.json

---

## Task [8]: Generate Comprehensive Analysis Report with Recommendations

**TOML Reference:** `tasks[id=8]` in parameters_Dev_Analysis.toml  
**Purpose:** Synthesise all findings into actionable report

- **Step [1]:** Structure report outline
  - **Primary method:** Create report sections: Executive Summary, Goal Analysis, Propagation Findings, Performance Metrics, Correlations, Quality Assessment, Error Analysis, Recommendations
  - **Expected output:** Report outline with section headers
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Write Executive Summary
  - **Primary method:** Synthesise key findings: goal characteristics summary, main propagation patterns, overall performance, critical insights
  - **Expected output:** 200-300 word executive summary highlighting main findings
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Compile Goal Text Analysis section
  - **Primary method:** Aggregate Task 1 findings: goal characteristics table, complexity assessment, element breakdown
  - **Expected output:** Goal Text Analysis section with all metrics and assessments
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Compile Goal Text Propagation section
  - **Primary method:** Aggregate Task 2 findings: propagation examples, language flow diagram, conceptual drift assessment
  - **Expected output:** Goal Text Propagation section with minimum 3 concrete examples with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Compile Constitutional Compliance section
  - **Primary method:** Aggregate Task 3 findings: article-by-article scores, overall compliance score, violation summary
  - **Expected output:** Constitutional Compliance section with compliance scorecard
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Compile Execution Performance section
  - **Primary method:** Aggregate Task 4 findings: success/failure rates, backup usage, mode escalations, efficiency metrics
  - **Expected output:** Execution Performance section with metrics tables
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Compile Behaviour Correlation section
  - **Primary method:** Aggregate Task 5 findings: correlation matrix, causality assessments, confounding factors
  - **Expected output:** Behaviour Correlation section with correlation findings
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Compile Quality Assessment section
  - **Primary method:** Aggregate Task 6 findings: task quality scores, step atomicity, critical flag appropriateness
  - **Expected output:** Quality Assessment section with quality distributions
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Compile Error Analysis section
  - **Primary method:** Aggregate Task 7 findings: error categories, root causes, recovery effectiveness, preventability
  - **Expected output:** Error Analysis section with error breakdown and patterns
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Generate actionable recommendations
  - **Primary method:** Based on all findings, create specific recommendations for: goal formulation improvement, SPEC design enhancement, execution optimisation, constitutional compliance, error prevention, efficiency improvements
  - **Backup [1]:** Use evidence-based recommendation framework: identify issue, link to finding, propose specific action, justify with data
  - **Expected output:** Minimum 8 specific, actionable recommendations linked to findings with priority levels
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Add cross-project comparison framework (if applicable)
  - **Primary method:** If analysing multiple SPECs, create comparison tables for key metrics across projects
  - **Expected output:** Cross-project comparison section (optional, only if multiple projects analysed)
  - **Critical:** false
  - **Mode:** silent

- **Step [12]:** Finalise report formatting and references
  - **Primary method:** Ensure all sections formatted consistently, add table of contents, verify all data citations present
  - **Expected output:** Complete, polished analysis report in markdown format
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Report contains all required sections, metrics are evidence-based, recommendations are actionable
- **Logging:** Record report completion in progress_Dev_Analysis.json with final deliverable path

---

## Bridging: Markdown ↔ TOML Synchronisation

This spec file (Dev_Analysis_SPEC.md) must maintain perfect alignment with its companion file (parameters_Dev_Analysis.toml).

**Bridging Requirements:**
1. Each task in this file must have corresponding `[[tasks]]` entry in TOML with matching ID (1-8)
2. Each step within a task must have corresponding `[[tasks.steps]]` entry with matching ID
3. Expected outputs in this file must match `expected_output` fields in TOML
4. Critical flags must be synchronised between files
5. Constraints referenced must exist in TOML `[constraints]` section

**Example Cross-References:**
- "See `constraints.min_examples_required` in parameters_Dev_Analysis.toml" (Task 2, Step 4)
- "As defined in `tasks[id=4]` in TOML" (Task 4 reference)
- "Must satisfy TOML verification requirements" (All task verifications)

The exe_Dev_Analysis.md controller will validate this synchronisation during initialisation (Section 1.8).

---

## Instructions for LLM Executor

1. **Start with goal understanding**: This analysis examines how goal text propagates and influences SPEC development
2. **Execute tasks sequentially**: Tasks 1-2 gather data, Tasks 3-7 analyse patterns, Task 8 synthesises findings
3. **Maintain objectivity**: Base all findings on evidence from files, logs, and artefacts
4. **Track propagation carefully**: Pay special attention to how exact goal language appears throughout project
5. **Quantify where possible**: Use numerical metrics rather than subjective assessments when feasible
6. **Distinguish correlation from causation**: Note relationships but assess causality carefully
7. **Document thoroughly**: Log all findings in progress_Dev_Analysis.json for traceability
8. **Focus on actionability**: Recommendations should be specific and implementable
9. **Read prior outcomes**: Before each step, check progress.json for relevant prior findings
10. **Escalate appropriately**: Use collaborative mode for causality judgements and unclear recommendation priorities

---

## Expected Analysis Output Structure

The final report should follow this structure:

```markdown
# SPEC Development Analysis Report

## Executive Summary
[200-300 word overview of key findings]

## 1. Goal Text Analysis
### 1.1 Initial Goal Characteristics
- Quantitative metrics table
- Complexity classification
- Element breakdown

### 1.2 Technical Specificity Assessment
- Specificity score with justification
- Domain terminology analysis

## 2. Goal Text Propagation Analysis
### 2.1 Propagation Through Tasks
- Task-level language mapping
- Specific examples with quotes

### 2.2 Propagation Through Steps
- Step-level language mapping
- Propagation matrix

### 2.3 Agent Thinking Patterns
- Minimum 3 examples of goal text in reasoning
- Direct quotes from logs/chat

### 2.4 Conceptual Drift Assessment
- Identified divergences
- Impact analysis

## 3. Constitutional Compliance Assessment
### 3.1 Article-by-Article Scores
- Individual article compliance
- Evidence for each assessment

### 3.2 Overall Compliance Score
- Aggregate score (0-100)
- Violation summary

## 4. Execution Performance Metrics
### 4.1 Success and Failure Rates
- Quantitative metrics table
- Rate comparisons

### 4.2 Backup Method Usage
- Usage statistics
- Effectiveness assessment

### 4.3 Mode Escalations
- Escalation count and triggers
- Appropriateness evaluation

### 4.4 Efficiency Metrics
- Steps per task
- Time analysis (if available)

## 5. Behaviour Correlation Analysis
### 5.1 Identified Correlations
- Goal characteristics vs execution behaviour
- Correlation strength assessment

### 5.2 Causality Assessment
- Causal vs correlational relationships
- Confidence levels

### 5.3 Confounding Factors
- External influences
- Mediation effects

## 6. Quality Assessment
### 6.1 Task Decomposition Quality
- Per-task quality scores
- Decomposition effectiveness

### 6.2 Step Quality Analysis
- Atomicity assessment
- Critical flag appropriateness

### 6.3 Method Selection Quality
- Primary/backup rationale
- Method effectiveness

## 7. Error Analysis
### 7.1 Error Categorisation
- Error type distribution
- Frequency patterns

### 7.2 Root Cause Analysis
- Root cause mapping
- Prevention opportunities

### 7.3 Recovery Effectiveness
- Recovery success rates
- Backup effectiveness

### 7.4 Constitutional Violations
- Violation breakdown by article
- Severity assessment

## 8. Recommendations
### 8.1 Goal Formulation Improvements
[Specific, actionable recommendations]

### 8.2 SPEC Design Enhancements
[Specific, actionable recommendations]

### 8.3 Execution Optimisation
[Specific, actionable recommendations]

### 8.4 Constitutional Compliance
[Specific, actionable recommendations]

### 8.5 Future Research Directions
[Areas for deeper investigation]

## Appendices
### A. Raw Data Tables
### B. Propagation Examples (Full Quotes)
### C. Metrics Calculation Methods
### D. Source Citations
```

---

**End of Dev_Analysis_SPEC.md**

This SPEC is designed to be reusable across multiple test SPEC analyses, enabling systematic comparison and pattern identification.


```

```markdown
# Dev Analysis SPEC

**Version:** 1.0  
**Last Updated:** 2025-11-03  
**Purpose:** Analyse development of test SPECs to identify patterns, metrics, and goal text propagation effects

---

## Goal

Perform comprehensive analysis of a test SPEC's development lifecycle to identify how initial goal text propagates through the system and impacts agent behaviour, execution accuracy, and project outcomes.

---

## Software Stack & Architecture

**Not Applicable** - This is an analysis task, not a build goal.

---

## Definition of Complete

What must exist and be verified:
- [ ] **Primary deliverable:** Comprehensive analysis report (markdown format) covering all analysis areas
- [ ] **Quality standards met:** 
  - All 8 analysis tasks completed with documented findings
  - Goal text propagation patterns identified with specific examples
  - Quantitative metrics calculated for execution performance
  - Cross-correlation analysis between goal characteristics and outcomes
  - Recommendations provided based on findings
- [ ] **Verification method:** 
  - Report contains all required sections (see tasks below)
  - Quantitative metrics include numerical values with source citations
  - At least 3 specific examples of goal text propagation documented
  - Recommendations are actionable and linked to specific findings

---

## Definitions

- **goal**: Analyse how initial goal text characteristics influence SPEC development and execution
- **task[n]**: Discrete analysis objectives examining different aspects of SPEC development
- **step[m]**: Concrete analytical actions within each task
- **backup[p]**: Alternative analysis methods when primary approach is blocked
- **critical_flag**: Boolean indicating whether analysis step is essential to overall goal
- **mode**: `silent` (fully autonomous - NO USER INPUT REQUIRED except initial project folder location)
- **progress.json**: Structured log tracking analysis execution and findings
- **project_folder**: Target development project folder path (ONLY required user input)

---

## Components

Analysis requires access to:
- **Test SPEC files:** spec_[descriptor].md, parameters_[descriptor].toml, exe_[descriptor].md
- **Execution logs:** progress_[descriptor].json
- **Project artefacts:** Code files, documentation, error logs, validation reports
- **Chat history:** Conversation transcripts showing agent thinking and decision-making
- **Constitution:** __SPEC_Engine/_Constitution/constitution.md for compliance checking

**Machine-Readable Components:**  
See `[components]` section in parameters_Dev_Analysis.toml

---

## Constraints

- Analysis must be objective and evidence-based
- All metrics must be traceable to source data
- Goal text propagation analysis must include minimum 3 concrete examples
- Quantitative metrics must include: success rates, error rates, mode escalations, backup usage
- Findings must distinguish correlation from causation
- Recommendations must be specific and actionable

**Machine-Readable Constraints:**  
See `[constraints]` section in parameters_Dev_Analysis.toml:
- `min_examples_required = 3` (goal text propagation examples)
- `metrics_evidence_based = true` (all metrics must cite sources)
- `recommendation_specificity = "actionable"` (recommendations must be implementable)

---

## User Stories

- As a **SPEC developer**, I want to understand how goal phrasing impacts development so I can write more effective goals
- As a **system architect**, I want to identify patterns in SPEC execution so I can improve the framework
- As a **researcher**, I want to quantify goal text propagation so I can understand agent behaviour correlation
- As a **project manager**, I want metrics on SPEC performance so I can assess project quality

---

## Analysis Framework

This SPEC analyses development across 8 integrated dimensions:

### Dimension 1: Goal Text Characteristics
- Length (word count, character count, sentence complexity)
- Number of distinct elements/requirements
- Literacy level (Flesch-Kincaid, technical density)
- Formatting (structure, lists, emphasis)
- Familiarity/Technical specificity

### Dimension 2: Goal Text Propagation
- How goal language appears in task descriptions
- Goal terminology in step definitions
- Phrasing patterns in agent thinking/reasoning
- Language consistency across SPEC artefacts
- Conceptual drift from goal to implementation

### Dimension 3: Constitutional Compliance
- Article I-XIV adherence scoring
- Critical flag balance (target: 40-60%)
- Backup method quality assessment
- Bridging quality (Markdown-TOML sync)
- Validation checkpoint outcomes

### Dimension 4: Execution Performance
- Step success/failure rates
- Backup invocation frequency
- Mode escalation patterns
- Error propagation effectiveness
- Retry patterns and exhaustion

### Dimension 5: Agent Behaviour Correlation
- Thinking patterns vs goal complexity
- Decision quality vs goal clarity
- Output quality vs goal specificity
- Backup selection vs goal ambiguity
- Escalation triggers vs goal characteristics

### Dimension 6: Per-Task/Step Behaviour
- Task decomposition quality
- Step atomicity assessment
- Critical flag appropriateness
- Expected output clarity
- Method selection rationale

### Dimension 7: Error Analysis
- Error types and frequencies
- Root cause patterns
- Recovery effectiveness
- Constitutional violations
- Preventable vs inherent errors

### Dimension 8: Outcome Metrics
- Goal achievement status (ACHIEVED/PARTIAL/NOT_ACHIEVED)
- Deliverable completeness
- Quality standards met
- Time/step efficiency
- Comparison to expected outcomes

---

## Task [0]: Initialize Analysis and Gather Project Metadata

**TOML Reference:** `tasks[id=0]` in parameters_Dev_Analysis.toml  
**Purpose:** Locate project folder, scan structure, and collect comprehensive metadata

- **Step [0]:** Receive project folder location (ONLY USER INPUT REQUIRED)
  - **Primary method:** Prompt for project development folder path
  - **Expected output:** Absolute path to project folder
  - **Critical:** true
  - **Mode:** collaborative (ONE TIME ONLY - for folder path input)

- **Step [1]:** Scan and map complete project structure
  - **Primary method:** Recursively list all files and directories in project folder
  - **Backup [1]:** If permissions issue, request accessible subset of project
  - **Expected output:** Complete file tree with full paths
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count and categorise all files
  - **Primary method:** Count files by type: .md, .toml, .json, .py, .js, .ts, .log, .txt, etc.
  - **Expected output:** File count table with breakdown by extension
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Calculate file sizes and total project size
  - **Primary method:** Get file size for each file, sum by category and total
  - **Expected output:** Size metrics table (bytes, KB, MB) by file type and total
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Extract all timestamps
  - **Primary method:** Collect creation, modification, access times for all relevant files
  - **Backup [1]:** If timestamps unavailable, use git history if present
  - **Expected output:** Timeline table showing project chronology
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Calculate development duration
  - **Primary method:** Calculate time from earliest to latest timestamp, identify development phases
  - **Expected output:** Development duration metrics: total time, active development periods, gaps
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Count tokens across all text files
  - **Primary method:** For each text-based file, count tokens (words, characters, estimated LLM tokens)
  - **Backup [1]:** If token counting unavailable, use word/character counts as proxy
  - **Expected output:** Token count table by file type with totals
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Identify and catalogue error logs
  - **Primary method:** Locate all error log files, count error entries, categorise by severity
  - **Expected output:** Error log inventory with counts and locations
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Identify and catalogue chat/conversation logs
  - **Primary method:** Locate chat transcripts, conversation logs, agent thinking logs
  - **Backup [1]:** Check common locations: root, logs folder, subdirectories
  - **Expected output:** Conversation log inventory with file paths and sizes
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Count conversation turns and messages
  - **Primary method:** Parse chat logs to count: total messages, user messages, agent messages, turns
  - **Expected output:** Conversation metrics table
  - **Critical:** false
  - **Mode:** silent

- **Step [10]:** Identify SPEC files and versions
  - **Primary method:** Locate all spec_*.md, parameters_*.toml, exe_*.md, progress_*.json files
  - **Expected output:** SPEC file inventory with versions and timestamps
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Create project metadata snapshot
  - **Primary method:** Aggregate all collected metrics into comprehensive metadata document
  - **Expected output:** Project metadata JSON with all metrics organized
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Project folder scanned, all files catalogued, comprehensive metrics collected
- **Logging:** Record all metadata in progress_Dev_Analysis.json for reference throughout analysis

---

## Task [1]: Extract and Characterise Initial Goal Text

**TOML Reference:** `tasks[id=1]` in parameters_Dev_Analysis.toml  
**Purpose:** Establish baseline characteristics of the goal that initiated SPEC development

- **Step [1]:** Locate and extract initial goal text
  - **Primary method:** Read SPEC markdown file Goal section and chat history for original user goal statement
  - **Backup [1]:** If chat history unavailable, use goal section from spec_[descriptor].md as proxy
  - **Expected output:** Exact goal text with source citation and timestamp
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Calculate quantitative text characteristics
  - **Primary method:** Compute word count, character count, sentence count, avg sentence length, Flesch-Kincaid score
  - **Backup [1]:** If automated scoring unavailable, perform manual classification (simple/moderate/complex)
  - **Expected output:** Table with numerical metrics and complexity classification
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Identify distinct elements and requirements
  - **Primary method:** Parse goal for discrete requirements, constraints, deliverables, success criteria
  - **Backup [1]:** Use linguistic chunking to identify conceptual units if structure unclear
  - **Expected output:** Numbered list of distinct elements (target: 3-10 elements)
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess technical specificity and domain familiarity
  - **Primary method:** Identify technical terms, domain-specific language, assumed knowledge, explicit vs implicit requirements
  - **Backup [1]:** Compare vocabulary against common vs specialised term databases
  - **Expected output:** Technical specificity score (1-5 scale) with justification and term examples
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Analyse formatting and structure
  - **Primary method:** Document use of lists, emphasis, sections, explicit vs narrative format
  - **Expected output:** Formatting assessment noting structural elements present
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All goal characteristics documented with quantitative metrics where possible
- **Logging:** Record all measurements in progress_Dev_Analysis.json for correlation analysis

---

## Task [2]: Map Goal Text Propagation Throughout Project

**TOML Reference:** `tasks[id=2]` in parameters_Dev_Analysis.toml  
**Purpose:** Track how initial goal language and concepts propagate through SPEC artefacts

- **Step [1]:** Extract task descriptions from SPEC
  - **Primary method:** Parse spec_[descriptor].md for all task titles and descriptions
  - **Expected output:** List of tasks with full text
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify goal language in task descriptions
  - **Primary method:** Compare task descriptions to goal text, noting shared terminology, conceptual overlap, verbatim phrases
  - **Backup [1]:** Use semantic similarity scoring if direct comparison insufficient
  - **Expected output:** Table mapping goal terms to task descriptions with similarity scores
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Extract step definitions and analyse propagation
  - **Primary method:** Parse all step descriptions, identify goal/task terminology presence, track conceptual consistency
  - **Backup [1]:** Focus on critical steps only if volume is high (>20 steps)
  - **Expected output:** Propagation matrix showing goal→task→step language flow with specific examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse agent thinking and reasoning patterns
  - **Primary method:** Review chat history/logs for agent internal reasoning, note how goal concepts appear in thinking
  - **Backup [1]:** If full chat unavailable, analyse progress.json logs for method justifications
  - **Expected output:** Minimum 3 specific examples of goal text influencing agent reasoning with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify conceptual drift
  - **Primary method:** Compare final implementation/outputs against original goal, identify divergences in terminology, scope, or interpretation
  - **Expected output:** Conceptual drift assessment noting where implementation departed from goal language
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Assess language consistency across artefacts
  - **Primary method:** Check terminology consistency across spec.md, parameters.toml, progress.json, deliverables
  - **Expected output:** Consistency report identifying where language fragmented or evolved
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Minimum 3 concrete examples of goal text propagation documented with direct quotes
- **Logging:** Record propagation patterns and drift instances in progress_Dev_Analysis.json

---

## Task [3]: Evaluate Constitutional Compliance

**TOML Reference:** `tasks[id=3]` in parameters_Dev_Analysis.toml  
**Purpose:** Assess adherence to SPEC Engine Constitution (Articles I-XIV)

- **Step [1]:** Validate Article I compliance (North Star Principle)
  - **Primary method:** Verify goal singularity, clarity, measurability, explicitness
  - **Expected output:** Article I compliance score (pass/fail) with justification
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Validate Article II compliance (Hierarchical Structure)
  - **Primary method:** Count tasks (target: 2-5), count steps per task (target: 1-5), verify hierarchy maintained
  - **Backup [1]:** If counts borderline, assess whether structure serves goal effectively
  - **Expected output:** Article II compliance score with quantitative counts
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Validate Article III compliance (Dual-File Mandate)
  - **Primary method:** Cross-check spec.md and parameters.toml for ID matching, structure sync, cross-references
  - **Expected output:** Article III compliance score noting any bridging failures
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Validate Article VI compliance (Critical Flag Discipline)
  - **Primary method:** Calculate critical step percentage (target: 40-60%), assess appropriateness of critical flags
  - **Expected output:** Critical balance percentage and appropriateness assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Validate Article VII compliance (Backup Methods)
  - **Primary method:** Review all backup methods to ensure they are alternative reasoning paths, not retries
  - **Backup [1]:** Sample backup methods if total exceeds 15
  - **Expected output:** Backup quality score with examples of good/poor backups
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Check Article XIV compliance (if build goal)
  - **Primary method:** If goal contains build/create/system keywords, verify software stack defined, deployment criteria present
  - **Expected output:** Article XIV compliance (N/A or pass/fail with details)
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Review Articles IV, VIII, IX, X compliance from execution
  - **Primary method:** Analyse progress.json for validation execution, error propagation, mode discipline, comprehensive logging
  - **Expected output:** Compliance scores for Articles IV, VIII, IX, X with evidence from logs
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Calculate overall constitutional compliance score
  - **Primary method:** Aggregate individual article scores, weight by severity, generate 0-100 score
  - **Expected output:** Overall compliance score (0-100) with breakdown by article
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All applicable articles assessed with evidence-based scoring
- **Logging:** Record compliance scores and violations in progress_Dev_Analysis.json

---

## Task [4]: Analyse Execution Performance Metrics

**TOML Reference:** `tasks[id=4]` in parameters_Dev_Analysis.toml  
**Purpose:** Extract quantitative performance data from execution logs with comprehensive detail

- **Step [1]:** Parse progress.json for complete step data
  - **Primary method:** Read progress_[descriptor].json, extract ALL fields: task_id, step_id, status, method_used, retry_count, timestamp, mode, critical_flag, expected_output, actual_output, error_messages
  - **Backup [1]:** If progress.json malformed, reconstruct from available logs
  - **Expected output:** Complete step outcome dataset with full detail per step
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count total steps taken
  - **Primary method:** Count: total steps defined, total steps attempted, total steps completed, total steps skipped, total steps failed
  - **Expected output:** Comprehensive step count table with breakdown by status
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Calculate detailed success and failure rates
  - **Primary method:** Compute: overall success rate, failure rate, success rate by task, failure rate by task, first-attempt success rate, eventual success rate (after retries)
  - **Expected output:** Multi-level success/failure metrics table with percentages at step, task, and SPEC levels
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse backup method usage patterns
  - **Primary method:** Count: primary method attempts, primary successes, backup[1] attempts, backup[1] successes, backup[2] attempts, backup[2] successes, calculate success rates per method type
  - **Expected output:** Comprehensive backup usage statistics with success rates, effectiveness scores, and usage frequency distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Track mode usage and escalations
  - **Primary method:** Count: steps in silent mode, steps in collaborative mode, mode switches, categorise escalation triggers (consecutive failures, backup depletion, critical failure, confidence degradation)
  - **Expected output:** Mode usage table, escalation count by trigger type, escalation appropriateness assessment per instance
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Analyse timestamps and time metrics
  - **Primary method:** Extract all timestamps from progress.json, calculate: time per step, time per task, total execution time, longest steps, shortest steps, time distribution
  - **Backup [1]:** If timestamps sparse, use available data and note gaps
  - **Expected output:** Comprehensive time metrics table with duration statistics
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Assess error propagation effectiveness
  - **Primary method:** Identify all steps with dependencies, check if prior failures were read from progress.json, assess propagation handling quality, count propagation decisions
  - **Backup [1]:** If error propagation tracking sparse, infer from step sequence and outcomes
  - **Expected output:** Error propagation effectiveness score with example instances and propagation decision breakdown
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Analyse retry patterns in detail
  - **Primary method:** Extract retry_count per step, calculate: average retries per step, max retries reached, retry exhaustion rate, retry success rate, thoroughness score (methods exhausted before escalation)
  - **Expected output:** Detailed retry pattern analysis with distribution charts and exhaustion assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Calculate efficiency and productivity metrics
  - **Primary method:** Compute: total steps attempted vs planned, steps per task (actual vs expected), average time per step, steps per hour, rework rate (retries/total), productivity score
  - **Expected output:** Comprehensive efficiency metrics table with productivity indicators
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Analyse critical vs non-critical step performance
  - **Primary method:** Separate critical and non-critical steps, compare: success rates, retry rates, time per step, failure impact
  - **Expected output:** Critical flag performance comparison table
  - **Critical:** false
  - **Mode:** silent

- **Step [11]:** Extract and analyse expected vs actual outputs
  - **Primary method:** For each step, compare expected_output defined in SPEC to actual_output logged, categorise: exact match, partial match, mismatch, missing
  - **Expected output:** Output quality assessment with match rate and mismatch analysis
  - **Critical:** true
  - **Mode:** silent

- **Step [12]:** Count and categorise all errors encountered
  - **Primary method:** Extract all error messages from progress.json, categorise by type (validation, execution, resource, logic), count occurrences, identify most frequent errors
  - **Expected output:** Error frequency table by category with top 10 most common errors
  - **Critical:** true
  - **Mode:** silent

- **Step [13]:** Analyse token usage per step (if available)
  - **Primary method:** If token counts logged, extract tokens per step, calculate: tokens per task, total tokens, token efficiency (tokens per successful step)
  - **Backup [1]:** If not logged in progress.json, skip with note
  - **Expected output:** Token usage metrics table (if data available)
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All quantitative metrics calculated with source data citations, minimum 13 metric categories documented
- **Logging:** Record all performance metrics in progress_Dev_Analysis.json

---

## Task [5]: Correlate Agent Behaviour with Goal Characteristics

**TOML Reference:** `tasks[id=5]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify relationships between goal text properties and agent execution behaviour

- **Step [1]:** Establish correlation framework
  - **Primary method:** Define metrics for correlation: goal complexity vs task count, goal clarity vs error rate, goal specificity vs backup usage
  - **Expected output:** Correlation matrix framework listing goal characteristics and behaviour metrics
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Analyse goal complexity vs task decomposition
  - **Primary method:** Correlate goal complexity score (from Task 1) with number of tasks, steps per task, decomposition depth
  - **Backup [1]:** Use qualitative assessment if quantitative correlation weak
  - **Expected output:** Correlation finding: does complex goal lead to more/fewer tasks?
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Analyse goal clarity vs execution accuracy
  - **Primary method:** Correlate goal clarity indicators (explicit requirements, measurable criteria) with success rate, error rate
  - **Expected output:** Correlation finding: does clear goal reduce errors?
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse goal specificity vs backup usage
  - **Primary method:** Correlate technical specificity score with backup invocation rate, backup effectiveness
  - **Expected output:** Correlation finding: does vague goal increase backup reliance?
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Analyse goal formatting vs agent thinking patterns
  - **Primary method:** Review agent reasoning for structured vs narrative goals, assess thinking clarity and organisation
  - **Backup [1]:** If thinking logs sparse, assess output organisation as proxy
  - **Expected output:** Qualitative finding on formatting impact with examples
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Identify confounding factors
  - **Primary method:** Check for external factors affecting correlation: SPEC complexity, domain difficulty, resource availability
  - **Expected output:** List of confounding factors that may explain behaviour patterns
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Distinguish correlation from causation
  - **Primary method:** For each correlation found, assess whether relationship is causal, coincidental, or mediated by other factors using evidence-based analysis
  - **Backup [1]:** Apply Bradford Hill criteria for causation: strength, consistency, specificity, temporality, biological gradient
  - **Expected output:** Causality assessment for each correlation with confidence level and supporting evidence
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Minimum 3 behaviour correlations identified with specific evidence
- **Logging:** Record correlations and causality assessments in progress_Dev_Analysis.json

---

## Task [6]: Assess Per-Task and Per-Step Behaviour Quality

**TOML Reference:** `tasks[id=6]` in parameters_Dev_Analysis.toml  
**Purpose:** Evaluate quality of task decomposition and step execution at granular level

- **Step [1]:** Evaluate task decomposition quality
  - **Primary method:** For each task, assess: Does task serve goal? Is task scope appropriate? Is task self-contained?
  - **Expected output:** Task quality assessment table with scores and rationale per task
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Assess step atomicity
  - **Primary method:** For each step, assess: Is step a single concrete action? Is step scope too broad/narrow? Is step executable?
  - **Backup [1]:** Sample steps if total exceeds 20
  - **Expected output:** Step atomicity assessment with examples of well/poorly scoped steps
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Evaluate critical flag appropriateness
  - **Primary method:** For each critical step, verify: Would failure truly block goal? For non-critical, verify: Can goal succeed without this?
  - **Expected output:** Critical flag appropriateness score with misclassification examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess expected output clarity
  - **Primary method:** For each step, rate expected output: specific/vague, measurable/subjective, achievable/unrealistic
  - **Expected output:** Expected output quality assessment with clarity distribution
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Evaluate method selection rationale
  - **Primary method:** For steps with multiple methods, assess whether primary/backup choices were well-justified
  - **Expected output:** Method selection quality score with examples
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All tasks and representative sample of steps assessed for quality
- **Logging:** Record quality assessments in progress_Dev_Analysis.json

---

## Task [7]: Conduct Comprehensive Error Analysis and Pattern Detection

**TOML Reference:** `tasks[id=7]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify error patterns, root causes, and improvement opportunities through meticulous analysis

- **Step [1]:** Extract and inventory all error sources
  - **Primary method:** Collect errors from: progress.json, error log files (from Task 0), chat logs, validation reports, any other error documentation
  - **Expected output:** Complete error inventory with source file paths and line references
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count total errors across all sources
  - **Primary method:** Count: total errors logged, errors per source type, errors per task, errors per step, error density (errors per 100 steps)
  - **Expected output:** Comprehensive error count table with breakdowns
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Categorise all errors by type and severity
  - **Primary method:** Classify each error by type (validation, execution, resource, logic, syntax, semantic) and severity (critical, major, minor, warning)
  - **Expected output:** Error categorisation matrix with counts and percentages by type and severity
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse error log files in detail
  - **Primary method:** For each error log file identified in Task 0, parse contents, extract: error timestamps, error messages, stack traces, context, frequency
  - **Backup [1]:** If logs are unstructured, extract what's available and note format issues
  - **Expected output:** Detailed error log analysis with structured data extracted from logs
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify error frequency patterns and hotspots
  - **Primary method:** Analyse which tasks/steps had highest error rates, identify repeated failures, calculate error concentration by task/step/time period
  - **Expected output:** Error hotspot analysis showing: high-error tasks, high-error steps, error clustering patterns, temporal error distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Conduct comprehensive root cause analysis
  - **Primary method:** For each error category, trace to root cause: SPEC design flaw, step definition ambiguity, resource limitation, goal ambiguity, external dependency, constitutional violation, tooling issue
  - **Backup [1]:** Apply 5 Whys methodology for complex errors
  - **Expected output:** Root cause mapping for all error categories with prevention recommendations per cause
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Analyse error propagation chains
  - **Primary method:** Trace errors that caused downstream failures, identify cascading error patterns, assess propagation handling
  - **Expected output:** Error propagation chain diagram with cascade analysis
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Assess recovery effectiveness and time
  - **Primary method:** For each error, determine: was it recovered? which method succeeded? how many attempts? time to recovery? was escalation needed?
  - **Expected output:** Recovery effectiveness metrics: recovery rate, average attempts to recovery, average time to recovery, escalation rate, recovery method distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Analyse error messages for clarity and actionability
  - **Primary method:** Review all error messages, rate: clarity (clear/vague), actionability (specific guidance/generic), completeness (context provided/missing)
  - **Expected output:** Error message quality assessment with examples of good/poor messages
  - **Critical:** false
  - **Mode:** silent

- **Step [10]:** Identify constitutional violations
  - **Primary method:** Check progress.json constitutional_compliance section, extract violations; cross-reference error patterns with constitutional articles
  - **Backup [1]:** Manual review of execution logs if compliance tracking absent
  - **Expected output:** Constitutional violation summary with article breakdown, severity, and correlation to errors
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Distinguish preventable from inherent errors
  - **Primary method:** Classify each error: preventable through better SPEC design, preventable through better execution, inherent to task complexity, external/environmental, resource-based
  - **Expected output:** Error preventability classification with percentages and improvement focus areas
  - **Critical:** true
  - **Mode:** silent

- **Step [12]:** Calculate error-related time costs
  - **Primary method:** Sum time spent on: failed steps, retries, error recovery, escalations, rework
  - **Backup [1]:** Estimate if precise timestamps unavailable
  - **Expected output:** Error cost metrics: time lost to errors, percentage of total time, cost per error category
  - **Critical:** false
  - **Mode:** silent

- **Step [13]:** Identify error patterns by goal characteristics
  - **Primary method:** Correlate error rates/types with goal complexity, clarity, specificity metrics from Task 1
  - **Expected output:** Error pattern correlation analysis linking errors to goal characteristics
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All errors from all sources analysed with root causes, minimum 13 error metric categories documented
- **Logging:** Record comprehensive error analysis findings in progress_Dev_Analysis.json

---

## Task [8]: Generate Comprehensive Analysis Report with Recommendations

**TOML Reference:** `tasks[id=8]` in parameters_Dev_Analysis.toml  
**Purpose:** Synthesise all findings into actionable report

- **Step [1]:** Structure report outline
  - **Primary method:** Create report sections: Executive Summary, Goal Analysis, Propagation Findings, Performance Metrics, Correlations, Quality Assessment, Error Analysis, Recommendations
  - **Expected output:** Report outline with section headers
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Write Executive Summary
  - **Primary method:** Synthesise key findings: goal characteristics summary, main propagation patterns, overall performance, critical insights
  - **Expected output:** 200-300 word executive summary highlighting main findings
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Compile Goal Text Analysis section
  - **Primary method:** Aggregate Task 1 findings: goal characteristics table, complexity assessment, element breakdown
  - **Expected output:** Goal Text Analysis section with all metrics and assessments
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Compile Goal Text Propagation section
  - **Primary method:** Aggregate Task 2 findings: propagation examples, language flow diagram, conceptual drift assessment
  - **Expected output:** Goal Text Propagation section with minimum 3 concrete examples with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Compile Constitutional Compliance section
  - **Primary method:** Aggregate Task 3 findings: article-by-article scores, overall compliance score, violation summary
  - **Expected output:** Constitutional Compliance section with compliance scorecard
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Compile Execution Performance section
  - **Primary method:** Aggregate Task 4 findings: success/failure rates, backup usage, mode escalations, efficiency metrics
  - **Expected output:** Execution Performance section with metrics tables
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Compile Behaviour Correlation section
  - **Primary method:** Aggregate Task 5 findings: correlation matrix, causality assessments, confounding factors
  - **Expected output:** Behaviour Correlation section with correlation findings
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Compile Quality Assessment section
  - **Primary method:** Aggregate Task 6 findings: task quality scores, step atomicity, critical flag appropriateness
  - **Expected output:** Quality Assessment section with quality distributions
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Compile Error Analysis section
  - **Primary method:** Aggregate Task 7 findings: error categories, root causes, recovery effectiveness, preventability
  - **Expected output:** Error Analysis section with error breakdown and patterns
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Generate actionable recommendations
  - **Primary method:** Based on all findings, create specific recommendations for: goal formulation improvement, SPEC design enhancement, execution optimisation, constitutional compliance, error prevention, efficiency improvements
  - **Backup [1]:** Use evidence-based recommendation framework: identify issue, link to finding, propose specific action, justify with data
  - **Expected output:** Minimum 8 specific, actionable recommendations linked to findings with priority levels
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Add cross-project comparison framework (if applicable)
  - **Primary method:** If analysing multiple SPECs, create comparison tables for key metrics across projects
  - **Expected output:** Cross-project comparison section (optional, only if multiple projects analysed)
  - **Critical:** false
  - **Mode:** silent

- **Step [12]:** Finalise report formatting and references
  - **Primary method:** Ensure all sections formatted consistently, add table of contents, verify all data citations present
  - **Expected output:** Complete, polished analysis report in markdown format
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Report contains all required sections, metrics are evidence-based, recommendations are actionable
- **Logging:** Record report completion in progress_Dev_Analysis.json with final deliverable path

---

## Bridging: Markdown ↔ TOML Synchronisation

This spec file (Dev_Analysis_SPEC.md) must maintain perfect alignment with its companion file (parameters_Dev_Analysis.toml).

**Bridging Requirements:**
1. Each task in this file must have corresponding `[[tasks]]` entry in TOML with matching ID (1-8)
2. Each step within a task must have corresponding `[[tasks.steps]]` entry with matching ID
3. Expected outputs in this file must match `expected_output` fields in TOML
4. Critical flags must be synchronised between files
5. Constraints referenced must exist in TOML `[constraints]` section

**Example Cross-References:**
- "See `constraints.min_examples_required` in parameters_Dev_Analysis.toml" (Task 2, Step 4)
- "As defined in `tasks[id=4]` in TOML" (Task 4 reference)
- "Must satisfy TOML verification requirements" (All task verifications)

The exe_Dev_Analysis.md controller will validate this synchronisation during initialisation (Section 1.8).

---

## Instructions for LLM Executor

1. **Start with goal understanding**: This analysis examines how goal text propagates and influences SPEC development
2. **Execute tasks sequentially**: Tasks 1-2 gather data, Tasks 3-7 analyse patterns, Task 8 synthesises findings
3. **Maintain objectivity**: Base all findings on evidence from files, logs, and artefacts
4. **Track propagation carefully**: Pay special attention to how exact goal language appears throughout project
5. **Quantify where possible**: Use numerical metrics rather than subjective assessments when feasible
6. **Distinguish correlation from causation**: Note relationships but assess causality carefully
7. **Document thoroughly**: Log all findings in progress_Dev_Analysis.json for traceability
8. **Focus on actionability**: Recommendations should be specific and implementable
9. **Read prior outcomes**: Before each step, check progress.json for relevant prior findings
10. **Escalate appropriately**: Use collaborative mode for causality judgements and unclear recommendation priorities

---

## Expected Analysis Output Structure

The final report should follow this structure:

```markdown
# SPEC Development Analysis Report

## Executive Summary
[200-300 word overview of key findings]

## 0. Project Metadata Overview
### 0.1 Project Structure
- Total files by type
- Total project size
- File tree summary

### 0.2 Development Timeline
- Total development duration
- Development phases
- Key timestamps

### 0.3 Token Metrics
- Total tokens across all files
- Token distribution by file type
- Estimated LLM token usage

### 0.4 File Inventory
- SPEC files identified
- Error logs found
- Chat/conversation logs
- Other key artefacts

### 0.5 Conversation Metrics
- Total messages/turns
- User vs agent message counts
- Conversation duration

## 1. Goal Text Analysis
### 1.1 Initial Goal Characteristics
- Quantitative metrics table
- Complexity classification
- Element breakdown

### 1.2 Technical Specificity Assessment
- Specificity score with justification
- Domain terminology analysis

## 2. Goal Text Propagation Analysis
### 2.1 Propagation Through Tasks
- Task-level language mapping
- Specific examples with quotes

### 2.2 Propagation Through Steps
- Step-level language mapping
- Propagation matrix

### 2.3 Agent Thinking Patterns
- Minimum 3 examples of goal text in reasoning
- Direct quotes from logs/chat

### 2.4 Conceptual Drift Assessment
- Identified divergences
- Impact analysis

## 3. Constitutional Compliance Assessment
### 3.1 Article-by-Article Scores
- Individual article compliance
- Evidence for each assessment

### 3.2 Overall Compliance Score
- Aggregate score (0-100)
- Violation summary

## 4. Execution Performance Metrics
### 4.1 Success and Failure Rates
- Quantitative metrics table
- Rate comparisons

### 4.2 Backup Method Usage
- Usage statistics
- Effectiveness assessment

### 4.3 Mode Escalations
- Escalation count and triggers
- Appropriateness evaluation

### 4.4 Efficiency Metrics
- Steps per task
- Time analysis (if available)

## 5. Behaviour Correlation Analysis
### 5.1 Identified Correlations
- Goal characteristics vs execution behaviour
- Correlation strength assessment

### 5.2 Causality Assessment
- Causal vs correlational relationships
- Confidence levels

### 5.3 Confounding Factors
- External influences
- Mediation effects

## 6. Quality Assessment
### 6.1 Task Decomposition Quality
- Per-task quality scores
- Decomposition effectiveness

### 6.2 Step Quality Analysis
- Atomicity assessment
- Critical flag appropriateness

### 6.3 Method Selection Quality
- Primary/backup rationale
- Method effectiveness

## 7. Error Analysis
### 7.1 Error Categorisation
- Error type distribution
- Frequency patterns

### 7.2 Root Cause Analysis
- Root cause mapping
- Prevention opportunities

### 7.3 Recovery Effectiveness
- Recovery success rates
- Backup effectiveness

### 7.4 Constitutional Violations
- Violation breakdown by article
- Severity assessment

## 8. Recommendations
### 8.1 Goal Formulation Improvements
[Specific, actionable recommendations]

### 8.2 SPEC Design Enhancements
[Specific, actionable recommendations]

### 8.3 Execution Optimisation
[Specific, actionable recommendations]

### 8.4 Constitutional Compliance
[Specific, actionable recommendations]

### 8.5 Future Research Directions
[Areas for deeper investigation]

## Appendices
### A. Raw Data Tables
### B. Propagation Examples (Full Quotes)
### C. Metrics Calculation Methods
### D. Source Citations
```

---

**End of Dev_Analysis_SPEC.md**

This SPEC is designed to be reusable across multiple test SPEC analyses, enabling systematic comparison and pattern identification.


```

```markdown
# Dev Analysis SPEC

**Version:** 1.0  
**Last Updated:** 2025-11-03  
**Purpose:** Analyse development of test SPECs to identify patterns, metrics, and goal text propagation effects

---

## Goal

Perform comprehensive analysis of a test SPEC's development lifecycle to identify how initial goal text propagates through the system and impacts agent behaviour, execution accuracy, and project outcomes.

---

## Software Stack & Architecture

**Not Applicable** - This is an analysis task, not a build goal.

---

## Definition of Complete

What must exist and be verified:
- [ ] **Primary deliverable:** Comprehensive analysis report (markdown format) covering all analysis areas
- [ ] **Quality standards met:** 
  - All 8 analysis tasks completed with documented findings
  - Goal text propagation patterns identified with specific examples
  - Quantitative metrics calculated for execution performance
  - Cross-correlation analysis between goal characteristics and outcomes
  - Recommendations provided based on findings
- [ ] **Verification method:** 
  - Report contains all required sections (see tasks below)
  - Quantitative metrics include numerical values with source citations
  - At least 3 specific examples of goal text propagation documented
  - Recommendations are actionable and linked to specific findings

---

## Definitions

- **goal**: Analyse how initial goal text characteristics influence SPEC development and execution
- **task[n]**: Discrete analysis objectives examining different aspects of SPEC development
- **step[m]**: Concrete analytical actions within each task
- **backup[p]**: Alternative analysis methods when primary approach is blocked
- **critical_flag**: Boolean indicating whether analysis step is essential to overall goal
- **mode**: `silent` (fully autonomous - NO USER INPUT REQUIRED except initial project folder location)
- **progress.json**: Structured log tracking analysis execution and findings
- **project_folder**: Target development project folder path (ONLY required user input)

---

## Components

Analysis requires access to:
- **Test SPEC files:** spec_[descriptor].md, parameters_[descriptor].toml, exe_[descriptor].md
- **Execution logs:** progress_[descriptor].json
- **Project artefacts:** Code files, documentation, error logs, validation reports
- **Chat history:** Conversation transcripts showing agent thinking and decision-making
- **Constitution:** __SPEC_Engine/_Constitution/constitution.md for compliance checking

**Machine-Readable Components:**  
See `[components]` section in parameters_Dev_Analysis.toml

---

## Constraints

- Analysis must be objective and evidence-based
- All metrics must be traceable to source data
- Goal text propagation analysis must include minimum 3 concrete examples
- Quantitative metrics must include: success rates, error rates, mode escalations, backup usage
- Findings must distinguish correlation from causation
- Recommendations must be specific and actionable

**Machine-Readable Constraints:**  
See `[constraints]` section in parameters_Dev_Analysis.toml:
- `min_examples_required = 3` (goal text propagation examples)
- `metrics_evidence_based = true` (all metrics must cite sources)
- `recommendation_specificity = "actionable"` (recommendations must be implementable)

---

## User Stories

- As a **SPEC developer**, I want to understand how goal phrasing impacts development so I can write more effective goals
- As a **system architect**, I want to identify patterns in SPEC execution so I can improve the framework
- As a **researcher**, I want to quantify goal text propagation so I can understand agent behaviour correlation
- As a **project manager**, I want metrics on SPEC performance so I can assess project quality

---

## Analysis Framework

This SPEC analyses development across 8 integrated dimensions:

### Dimension 1: Goal Text Characteristics
- Length (word count, character count, sentence complexity)
- Number of distinct elements/requirements
- Literacy level (Flesch-Kincaid, technical density)
- Formatting (structure, lists, emphasis)
- Familiarity/Technical specificity

### Dimension 2: Goal Text Propagation
- How goal language appears in task descriptions
- Goal terminology in step definitions
- Phrasing patterns in agent thinking/reasoning
- Language consistency across SPEC artefacts
- Conceptual drift from goal to implementation

### Dimension 3: Constitutional Compliance
- Article I-XIV adherence scoring
- Critical flag balance (target: 40-60%)
- Backup method quality assessment
- Bridging quality (Markdown-TOML sync)
- Validation checkpoint outcomes

### Dimension 4: Execution Performance
- Step success/failure rates
- Backup invocation frequency
- Mode escalation patterns
- Error propagation effectiveness
- Retry patterns and exhaustion

### Dimension 5: Agent Behaviour Correlation
- Thinking patterns vs goal complexity
- Decision quality vs goal clarity
- Output quality vs goal specificity
- Backup selection vs goal ambiguity
- Escalation triggers vs goal characteristics

### Dimension 6: Per-Task/Step Behaviour
- Task decomposition quality
- Step atomicity assessment
- Critical flag appropriateness
- Expected output clarity
- Method selection rationale

### Dimension 7: Error Analysis
- Error types and frequencies
- Root cause patterns
- Recovery effectiveness
- Constitutional violations
- Preventable vs inherent errors

### Dimension 8: Outcome Metrics
- Goal achievement status (ACHIEVED/PARTIAL/NOT_ACHIEVED)
- Deliverable completeness
- Quality standards met
- Time/step efficiency
- Comparison to expected outcomes

---

## Task [0]: Initialize Analysis and Gather Project Metadata

**TOML Reference:** `tasks[id=0]` in parameters_Dev_Analysis.toml  
**Purpose:** Locate project folder, scan structure, and collect comprehensive metadata

- **Step [0]:** Receive project folder location (ONLY USER INPUT REQUIRED)
  - **Primary method:** Prompt for project development folder path
  - **Expected output:** Absolute path to project folder
  - **Critical:** true
  - **Mode:** collaborative (ONE TIME ONLY - for folder path input)

- **Step [1]:** Scan and map complete project structure
  - **Primary method:** Recursively list all files and directories in project folder
  - **Backup [1]:** If permissions issue, request accessible subset of project
  - **Expected output:** Complete file tree with full paths
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count and categorise all files
  - **Primary method:** Count files by type: .md, .toml, .json, .py, .js, .ts, .log, .txt, etc.
  - **Expected output:** File count table with breakdown by extension
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Calculate file sizes and total project size
  - **Primary method:** Get file size for each file, sum by category and total
  - **Expected output:** Size metrics table (bytes, KB, MB) by file type and total
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Extract all timestamps
  - **Primary method:** Collect creation, modification, access times for all relevant files
  - **Backup [1]:** If timestamps unavailable, use git history if present
  - **Expected output:** Timeline table showing project chronology
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Calculate development duration
  - **Primary method:** Calculate time from earliest to latest timestamp, identify development phases
  - **Expected output:** Development duration metrics: total time, active development periods, gaps
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Count tokens across all text files
  - **Primary method:** For each text-based file, count tokens (words, characters, estimated LLM tokens)
  - **Backup [1]:** If token counting unavailable, use word/character counts as proxy
  - **Expected output:** Token count table by file type with totals
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Identify and catalogue error logs
  - **Primary method:** Locate all error log files, count error entries, categorise by severity
  - **Expected output:** Error log inventory with counts and locations
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Identify and catalogue chat/conversation logs
  - **Primary method:** Locate chat transcripts, conversation logs, agent thinking logs
  - **Backup [1]:** Check common locations: root, logs folder, subdirectories
  - **Expected output:** Conversation log inventory with file paths and sizes
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Count conversation turns and messages
  - **Primary method:** Parse chat logs to count: total messages, user messages, agent messages, turns
  - **Expected output:** Conversation metrics table
  - **Critical:** false
  - **Mode:** silent

- **Step [10]:** Identify SPEC files and versions
  - **Primary method:** Locate all spec_*.md, parameters_*.toml, exe_*.md, progress_*.json files
  - **Expected output:** SPEC file inventory with versions and timestamps
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Create project metadata snapshot
  - **Primary method:** Aggregate all collected metrics into comprehensive metadata document
  - **Expected output:** Project metadata JSON with all metrics organized
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Project folder scanned, all files catalogued, comprehensive metrics collected
- **Logging:** Record all metadata in progress_Dev_Analysis.json for reference throughout analysis

---

## Task [1]: Extract and Characterise Initial Goal Text

**TOML Reference:** `tasks[id=1]` in parameters_Dev_Analysis.toml  
**Purpose:** Establish baseline characteristics of the goal that initiated SPEC development

- **Step [1]:** Locate and extract initial goal text
  - **Primary method:** Read SPEC markdown file Goal section and chat history for original user goal statement
  - **Backup [1]:** If chat history unavailable, use goal section from spec_[descriptor].md as proxy
  - **Expected output:** Exact goal text with source citation and timestamp
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Calculate quantitative text characteristics
  - **Primary method:** Compute word count, character count, sentence count, avg sentence length, Flesch-Kincaid score
  - **Backup [1]:** If automated scoring unavailable, perform manual classification (simple/moderate/complex)
  - **Expected output:** Table with numerical metrics and complexity classification
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Identify distinct elements and requirements
  - **Primary method:** Parse goal for discrete requirements, constraints, deliverables, success criteria
  - **Backup [1]:** Use linguistic chunking to identify conceptual units if structure unclear
  - **Expected output:** Numbered list of distinct elements (target: 3-10 elements)
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess technical specificity and domain familiarity
  - **Primary method:** Identify technical terms, domain-specific language, assumed knowledge, explicit vs implicit requirements
  - **Backup [1]:** Compare vocabulary against common vs specialised term databases
  - **Expected output:** Technical specificity score (1-5 scale) with justification and term examples
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Analyse formatting and structure
  - **Primary method:** Document use of lists, emphasis, sections, explicit vs narrative format
  - **Expected output:** Formatting assessment noting structural elements present
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All goal characteristics documented with quantitative metrics where possible
- **Logging:** Record all measurements in progress_Dev_Analysis.json for correlation analysis

---

## Task [2]: Map Goal Text Propagation Throughout Project

**TOML Reference:** `tasks[id=2]` in parameters_Dev_Analysis.toml  
**Purpose:** Track how initial goal language and concepts propagate through SPEC artefacts

- **Step [1]:** Extract task descriptions from SPEC
  - **Primary method:** Parse spec_[descriptor].md for all task titles and descriptions
  - **Expected output:** List of tasks with full text
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify goal language in task descriptions
  - **Primary method:** Compare task descriptions to goal text, noting shared terminology, conceptual overlap, verbatim phrases
  - **Backup [1]:** Use semantic similarity scoring if direct comparison insufficient
  - **Expected output:** Table mapping goal terms to task descriptions with similarity scores
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Extract step definitions and analyse propagation
  - **Primary method:** Parse all step descriptions, identify goal/task terminology presence, track conceptual consistency
  - **Backup [1]:** Focus on critical steps only if volume is high (>20 steps)
  - **Expected output:** Propagation matrix showing goal→task→step language flow with specific examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse agent thinking and reasoning patterns
  - **Primary method:** Review chat history/logs for agent internal reasoning, note how goal concepts appear in thinking
  - **Backup [1]:** If full chat unavailable, analyse progress.json logs for method justifications
  - **Expected output:** Minimum 3 specific examples of goal text influencing agent reasoning with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify conceptual drift
  - **Primary method:** Compare final implementation/outputs against original goal, identify divergences in terminology, scope, or interpretation
  - **Expected output:** Conceptual drift assessment noting where implementation departed from goal language
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Assess language consistency across artefacts
  - **Primary method:** Check terminology consistency across spec.md, parameters.toml, progress.json, deliverables
  - **Expected output:** Consistency report identifying where language fragmented or evolved
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Minimum 3 concrete examples of goal text propagation documented with direct quotes
- **Logging:** Record propagation patterns and drift instances in progress_Dev_Analysis.json

---

## Task [3]: Evaluate Constitutional Compliance

**TOML Reference:** `tasks[id=3]` in parameters_Dev_Analysis.toml  
**Purpose:** Assess adherence to SPEC Engine Constitution (Articles I-XIV)

- **Step [1]:** Validate Article I compliance (North Star Principle)
  - **Primary method:** Verify goal singularity, clarity, measurability, explicitness
  - **Expected output:** Article I compliance score (pass/fail) with justification
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Validate Article II compliance (Hierarchical Structure)
  - **Primary method:** Count tasks (target: 2-5), count steps per task (target: 1-5), verify hierarchy maintained
  - **Backup [1]:** If counts borderline, assess whether structure serves goal effectively
  - **Expected output:** Article II compliance score with quantitative counts
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Validate Article III compliance (Dual-File Mandate)
  - **Primary method:** Cross-check spec.md and parameters.toml for ID matching, structure sync, cross-references
  - **Expected output:** Article III compliance score noting any bridging failures
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Validate Article VI compliance (Critical Flag Discipline)
  - **Primary method:** Calculate critical step percentage (target: 40-60%), assess appropriateness of critical flags
  - **Expected output:** Critical balance percentage and appropriateness assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Validate Article VII compliance (Backup Methods)
  - **Primary method:** Review all backup methods to ensure they are alternative reasoning paths, not retries
  - **Backup [1]:** Sample backup methods if total exceeds 15
  - **Expected output:** Backup quality score with examples of good/poor backups
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Check Article XIV compliance (if build goal)
  - **Primary method:** If goal contains build/create/system keywords, verify software stack defined, deployment criteria present
  - **Expected output:** Article XIV compliance (N/A or pass/fail with details)
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Review Articles IV, VIII, IX, X compliance from execution
  - **Primary method:** Analyse progress.json for validation execution, error propagation, mode discipline, comprehensive logging
  - **Expected output:** Compliance scores for Articles IV, VIII, IX, X with evidence from logs
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Calculate overall constitutional compliance score
  - **Primary method:** Aggregate individual article scores, weight by severity, generate 0-100 score
  - **Expected output:** Overall compliance score (0-100) with breakdown by article
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All applicable articles assessed with evidence-based scoring
- **Logging:** Record compliance scores and violations in progress_Dev_Analysis.json

---

## Task [4]: Analyse Execution Performance Metrics

**TOML Reference:** `tasks[id=4]` in parameters_Dev_Analysis.toml  
**Purpose:** Extract quantitative performance data from execution logs with comprehensive detail

- **Step [1]:** Parse progress.json for complete step data
  - **Primary method:** Read progress_[descriptor].json, extract ALL fields: task_id, step_id, status, method_used, retry_count, timestamp, mode, critical_flag, expected_output, actual_output, error_messages
  - **Backup [1]:** If progress.json malformed, reconstruct from available logs
  - **Expected output:** Complete step outcome dataset with full detail per step
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count total steps taken
  - **Primary method:** Count: total steps defined, total steps attempted, total steps completed, total steps skipped, total steps failed
  - **Expected output:** Comprehensive step count table with breakdown by status
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Calculate detailed success and failure rates
  - **Primary method:** Compute: overall success rate, failure rate, success rate by task, failure rate by task, first-attempt success rate, eventual success rate (after retries)
  - **Expected output:** Multi-level success/failure metrics table with percentages at step, task, and SPEC levels
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse backup method usage patterns
  - **Primary method:** Count: primary method attempts, primary successes, backup[1] attempts, backup[1] successes, backup[2] attempts, backup[2] successes, calculate success rates per method type
  - **Expected output:** Comprehensive backup usage statistics with success rates, effectiveness scores, and usage frequency distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Track mode usage and escalations
  - **Primary method:** Count: steps in silent mode, steps in collaborative mode, mode switches, categorise escalation triggers (consecutive failures, backup depletion, critical failure, confidence degradation)
  - **Expected output:** Mode usage table, escalation count by trigger type, escalation appropriateness assessment per instance
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Analyse timestamps and time metrics
  - **Primary method:** Extract all timestamps from progress.json, calculate: time per step, time per task, total execution time, longest steps, shortest steps, time distribution
  - **Backup [1]:** If timestamps sparse, use available data and note gaps
  - **Expected output:** Comprehensive time metrics table with duration statistics
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Assess error propagation effectiveness
  - **Primary method:** Identify all steps with dependencies, check if prior failures were read from progress.json, assess propagation handling quality, count propagation decisions
  - **Backup [1]:** If error propagation tracking sparse, infer from step sequence and outcomes
  - **Expected output:** Error propagation effectiveness score with example instances and propagation decision breakdown
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Analyse retry patterns in detail
  - **Primary method:** Extract retry_count per step, calculate: average retries per step, max retries reached, retry exhaustion rate, retry success rate, thoroughness score (methods exhausted before escalation)
  - **Expected output:** Detailed retry pattern analysis with distribution charts and exhaustion assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Calculate efficiency and productivity metrics
  - **Primary method:** Compute: total steps attempted vs planned, steps per task (actual vs expected), average time per step, steps per hour, rework rate (retries/total), productivity score
  - **Expected output:** Comprehensive efficiency metrics table with productivity indicators
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Analyse critical vs non-critical step performance
  - **Primary method:** Separate critical and non-critical steps, compare: success rates, retry rates, time per step, failure impact
  - **Expected output:** Critical flag performance comparison table
  - **Critical:** false
  - **Mode:** silent

- **Step [11]:** Extract and analyse expected vs actual outputs
  - **Primary method:** For each step, compare expected_output defined in SPEC to actual_output logged, categorise: exact match, partial match, mismatch, missing
  - **Expected output:** Output quality assessment with match rate and mismatch analysis
  - **Critical:** true
  - **Mode:** silent

- **Step [12]:** Count and categorise all errors encountered
  - **Primary method:** Extract all error messages from progress.json, categorise by type (validation, execution, resource, logic), count occurrences, identify most frequent errors
  - **Expected output:** Error frequency table by category with top 10 most common errors
  - **Critical:** true
  - **Mode:** silent

- **Step [13]:** Analyse token usage per step (if available)
  - **Primary method:** If token counts logged, extract tokens per step, calculate: tokens per task, total tokens, token efficiency (tokens per successful step)
  - **Backup [1]:** If not logged in progress.json, skip with note
  - **Expected output:** Token usage metrics table (if data available)
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All quantitative metrics calculated with source data citations, minimum 13 metric categories documented
- **Logging:** Record all performance metrics in progress_Dev_Analysis.json

---

## Task [5]: Correlate Agent Behaviour with Goal Characteristics

**TOML Reference:** `tasks[id=5]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify relationships between goal text properties and agent execution behaviour

- **Step [1]:** Establish correlation framework
  - **Primary method:** Define metrics for correlation: goal complexity vs task count, goal clarity vs error rate, goal specificity vs backup usage
  - **Expected output:** Correlation matrix framework listing goal characteristics and behaviour metrics
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Analyse goal complexity vs task decomposition
  - **Primary method:** Correlate goal complexity score (from Task 1) with number of tasks, steps per task, decomposition depth
  - **Backup [1]:** Use qualitative assessment if quantitative correlation weak
  - **Expected output:** Correlation finding: does complex goal lead to more/fewer tasks?
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Analyse goal clarity vs execution accuracy
  - **Primary method:** Correlate goal clarity indicators (explicit requirements, measurable criteria) with success rate, error rate
  - **Expected output:** Correlation finding: does clear goal reduce errors?
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse goal specificity vs backup usage
  - **Primary method:** Correlate technical specificity score with backup invocation rate, backup effectiveness
  - **Expected output:** Correlation finding: does vague goal increase backup reliance?
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Analyse goal formatting vs agent thinking patterns
  - **Primary method:** Review agent reasoning for structured vs narrative goals, assess thinking clarity and organisation
  - **Backup [1]:** If thinking logs sparse, assess output organisation as proxy
  - **Expected output:** Qualitative finding on formatting impact with examples
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Identify confounding factors
  - **Primary method:** Check for external factors affecting correlation: SPEC complexity, domain difficulty, resource availability
  - **Expected output:** List of confounding factors that may explain behaviour patterns
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Distinguish correlation from causation
  - **Primary method:** For each correlation found, assess whether relationship is causal, coincidental, or mediated by other factors using evidence-based analysis
  - **Backup [1]:** Apply Bradford Hill criteria for causation: strength, consistency, specificity, temporality, biological gradient
  - **Expected output:** Causality assessment for each correlation with confidence level and supporting evidence
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Minimum 3 behaviour correlations identified with specific evidence
- **Logging:** Record correlations and causality assessments in progress_Dev_Analysis.json

---

## Task [6]: Assess Per-Task and Per-Step Behaviour Quality

**TOML Reference:** `tasks[id=6]` in parameters_Dev_Analysis.toml  
**Purpose:** Evaluate quality of task decomposition and step execution at granular level

- **Step [1]:** Evaluate task decomposition quality
  - **Primary method:** For each task, assess: Does task serve goal? Is task scope appropriate? Is task self-contained?
  - **Expected output:** Task quality assessment table with scores and rationale per task
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Assess step atomicity
  - **Primary method:** For each step, assess: Is step a single concrete action? Is step scope too broad/narrow? Is step executable?
  - **Backup [1]:** Sample steps if total exceeds 20
  - **Expected output:** Step atomicity assessment with examples of well/poorly scoped steps
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Evaluate critical flag appropriateness
  - **Primary method:** For each critical step, verify: Would failure truly block goal? For non-critical, verify: Can goal succeed without this?
  - **Expected output:** Critical flag appropriateness score with misclassification examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess expected output clarity
  - **Primary method:** For each step, rate expected output: specific/vague, measurable/subjective, achievable/unrealistic
  - **Expected output:** Expected output quality assessment with clarity distribution
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Evaluate method selection rationale
  - **Primary method:** For steps with multiple methods, assess whether primary/backup choices were well-justified
  - **Expected output:** Method selection quality score with examples
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All tasks and representative sample of steps assessed for quality
- **Logging:** Record quality assessments in progress_Dev_Analysis.json

---

## Task [7]: Conduct Comprehensive Error Analysis and Pattern Detection

**TOML Reference:** `tasks[id=7]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify error patterns, root causes, and improvement opportunities through meticulous analysis

- **Step [1]:** Extract and inventory all error sources
  - **Primary method:** Collect errors from: progress.json, error log files (from Task 0), chat logs, validation reports, any other error documentation
  - **Expected output:** Complete error inventory with source file paths and line references
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count total errors across all sources
  - **Primary method:** Count: total errors logged, errors per source type, errors per task, errors per step, error density (errors per 100 steps)
  - **Expected output:** Comprehensive error count table with breakdowns
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Categorise all errors by type and severity
  - **Primary method:** Classify each error by type (validation, execution, resource, logic, syntax, semantic) and severity (critical, major, minor, warning)
  - **Expected output:** Error categorisation matrix with counts and percentages by type and severity
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse error log files in detail
  - **Primary method:** For each error log file identified in Task 0, parse contents, extract: error timestamps, error messages, stack traces, context, frequency
  - **Backup [1]:** If logs are unstructured, extract what's available and note format issues
  - **Expected output:** Detailed error log analysis with structured data extracted from logs
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify error frequency patterns and hotspots
  - **Primary method:** Analyse which tasks/steps had highest error rates, identify repeated failures, calculate error concentration by task/step/time period
  - **Expected output:** Error hotspot analysis showing: high-error tasks, high-error steps, error clustering patterns, temporal error distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Conduct comprehensive root cause analysis
  - **Primary method:** For each error category, trace to root cause: SPEC design flaw, step definition ambiguity, resource limitation, goal ambiguity, external dependency, constitutional violation, tooling issue
  - **Backup [1]:** Apply 5 Whys methodology for complex errors
  - **Expected output:** Root cause mapping for all error categories with prevention recommendations per cause
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Analyse error propagation chains
  - **Primary method:** Trace errors that caused downstream failures, identify cascading error patterns, assess propagation handling
  - **Expected output:** Error propagation chain diagram with cascade analysis
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Assess recovery effectiveness and time
  - **Primary method:** For each error, determine: was it recovered? which method succeeded? how many attempts? time to recovery? was escalation needed?
  - **Expected output:** Recovery effectiveness metrics: recovery rate, average attempts to recovery, average time to recovery, escalation rate, recovery method distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Analyse error messages for clarity and actionability
  - **Primary method:** Review all error messages, rate: clarity (clear/vague), actionability (specific guidance/generic), completeness (context provided/missing)
  - **Expected output:** Error message quality assessment with examples of good/poor messages
  - **Critical:** false
  - **Mode:** silent

- **Step [10]:** Identify constitutional violations
  - **Primary method:** Check progress.json constitutional_compliance section, extract violations; cross-reference error patterns with constitutional articles
  - **Backup [1]:** Manual review of execution logs if compliance tracking absent
  - **Expected output:** Constitutional violation summary with article breakdown, severity, and correlation to errors
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Distinguish preventable from inherent errors
  - **Primary method:** Classify each error: preventable through better SPEC design, preventable through better execution, inherent to task complexity, external/environmental, resource-based
  - **Expected output:** Error preventability classification with percentages and improvement focus areas
  - **Critical:** true
  - **Mode:** silent

- **Step [12]:** Calculate error-related time costs
  - **Primary method:** Sum time spent on: failed steps, retries, error recovery, escalations, rework
  - **Backup [1]:** Estimate if precise timestamps unavailable
  - **Expected output:** Error cost metrics: time lost to errors, percentage of total time, cost per error category
  - **Critical:** false
  - **Mode:** silent

- **Step [13]:** Identify error patterns by goal characteristics
  - **Primary method:** Correlate error rates/types with goal complexity, clarity, specificity metrics from Task 1
  - **Expected output:** Error pattern correlation analysis linking errors to goal characteristics
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All errors from all sources analysed with root causes, minimum 13 error metric categories documented
- **Logging:** Record comprehensive error analysis findings in progress_Dev_Analysis.json

---

## Task [8]: Generate Comprehensive Analysis Report with Recommendations

**TOML Reference:** `tasks[id=8]` in parameters_Dev_Analysis.toml  
**Purpose:** Synthesise all findings into actionable report

- **Step [1]:** Structure report outline
  - **Primary method:** Create report sections: Executive Summary, Goal Analysis, Propagation Findings, Performance Metrics, Correlations, Quality Assessment, Error Analysis, Recommendations
  - **Expected output:** Report outline with section headers
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Write Executive Summary
  - **Primary method:** Synthesise key findings: goal characteristics summary, main propagation patterns, overall performance, critical insights
  - **Expected output:** 200-300 word executive summary highlighting main findings
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Compile Goal Text Analysis section
  - **Primary method:** Aggregate Task 1 findings: goal characteristics table, complexity assessment, element breakdown
  - **Expected output:** Goal Text Analysis section with all metrics and assessments
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Compile Goal Text Propagation section
  - **Primary method:** Aggregate Task 2 findings: propagation examples, language flow diagram, conceptual drift assessment
  - **Expected output:** Goal Text Propagation section with minimum 3 concrete examples with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Compile Constitutional Compliance section
  - **Primary method:** Aggregate Task 3 findings: article-by-article scores, overall compliance score, violation summary
  - **Expected output:** Constitutional Compliance section with compliance scorecard
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Compile Execution Performance section
  - **Primary method:** Aggregate Task 4 findings: success/failure rates, backup usage, mode escalations, efficiency metrics
  - **Expected output:** Execution Performance section with metrics tables
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Compile Behaviour Correlation section
  - **Primary method:** Aggregate Task 5 findings: correlation matrix, causality assessments, confounding factors
  - **Expected output:** Behaviour Correlation section with correlation findings
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Compile Quality Assessment section
  - **Primary method:** Aggregate Task 6 findings: task quality scores, step atomicity, critical flag appropriateness
  - **Expected output:** Quality Assessment section with quality distributions
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Compile Error Analysis section
  - **Primary method:** Aggregate Task 7 findings: error categories, root causes, recovery effectiveness, preventability
  - **Expected output:** Error Analysis section with error breakdown and patterns
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Generate actionable recommendations
  - **Primary method:** Based on all findings, create specific recommendations for: goal formulation improvement, SPEC design enhancement, execution optimisation, constitutional compliance, error prevention, efficiency improvements
  - **Backup [1]:** Use evidence-based recommendation framework: identify issue, link to finding, propose specific action, justify with data
  - **Expected output:** Minimum 8 specific, actionable recommendations linked to findings with priority levels
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Add cross-project comparison framework (if applicable)
  - **Primary method:** If analysing multiple SPECs, create comparison tables for key metrics across projects
  - **Expected output:** Cross-project comparison section (optional, only if multiple projects analysed)
  - **Critical:** false
  - **Mode:** silent

- **Step [12]:** Finalise report formatting and references
  - **Primary method:** Ensure all sections formatted consistently, add table of contents, verify all data citations present
  - **Expected output:** Complete, polished analysis report in markdown format
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Report contains all required sections, metrics are evidence-based, recommendations are actionable
- **Logging:** Record report completion in progress_Dev_Analysis.json with final deliverable path

---

## Bridging: Markdown ↔ TOML Synchronisation

This spec file (Dev_Analysis_SPEC.md) must maintain perfect alignment with its companion file (parameters_Dev_Analysis.toml).

**Bridging Requirements:**
1. Each task in this file must have corresponding `[[tasks]]` entry in TOML with matching ID (1-8)
2. Each step within a task must have corresponding `[[tasks.steps]]` entry with matching ID
3. Expected outputs in this file must match `expected_output` fields in TOML
4. Critical flags must be synchronised between files
5. Constraints referenced must exist in TOML `[constraints]` section

**Example Cross-References:**
- "See `constraints.min_examples_required` in parameters_Dev_Analysis.toml" (Task 2, Step 4)
- "As defined in `tasks[id=4]` in TOML" (Task 4 reference)
- "Must satisfy TOML verification requirements" (All task verifications)

The exe_Dev_Analysis.md controller will validate this synchronisation during initialisation (Section 1.8).

---

## Instructions for LLM Executor

1. **Start with goal understanding**: This analysis examines how goal text propagates and influences SPEC development
2. **Execute tasks sequentially**: Tasks 1-2 gather data, Tasks 3-7 analyse patterns, Task 8 synthesises findings
3. **Maintain objectivity**: Base all findings on evidence from files, logs, and artefacts
4. **Track propagation carefully**: Pay special attention to how exact goal language appears throughout project
5. **Quantify where possible**: Use numerical metrics rather than subjective assessments when feasible
6. **Distinguish correlation from causation**: Note relationships but assess causality carefully
7. **Document thoroughly**: Log all findings in progress_Dev_Analysis.json for traceability
8. **Focus on actionability**: Recommendations should be specific and implementable
9. **Read prior outcomes**: Before each step, check progress.json for relevant prior findings
10. **Escalate appropriately**: Use collaborative mode for causality judgements and unclear recommendation priorities

---

## Expected Analysis Output Structure

The final report should follow this structure:

```markdown
# SPEC Development Analysis Report

## Executive Summary
[200-300 word overview of key findings]

## 0. Project Metadata Overview
### 0.1 Project Structure
- Total files by type
- Total project size
- File tree summary

### 0.2 Development Timeline
- Total development duration
- Development phases
- Key timestamps

### 0.3 Token Metrics
- Total tokens across all files
- Token distribution by file type
- Estimated LLM token usage

### 0.4 File Inventory
- SPEC files identified
- Error logs found
- Chat/conversation logs
- Other key artefacts

### 0.5 Conversation Metrics
- Total messages/turns
- User vs agent message counts
- Conversation duration

## 1. Goal Text Analysis
### 1.1 Initial Goal Characteristics
- Quantitative metrics table
- Complexity classification
- Element breakdown

### 1.2 Technical Specificity Assessment
- Specificity score with justification
- Domain terminology analysis

## 2. Goal Text Propagation Analysis
### 2.1 Propagation Through Tasks
- Task-level language mapping
- Specific examples with quotes

### 2.2 Propagation Through Steps
- Step-level language mapping
- Propagation matrix

### 2.3 Agent Thinking Patterns
- Minimum 3 examples of goal text in reasoning
- Direct quotes from logs/chat

### 2.4 Conceptual Drift Assessment
- Identified divergences
- Impact analysis

## 3. Constitutional Compliance Assessment
### 3.1 Article-by-Article Scores
- Individual article compliance
- Evidence for each assessment

### 3.2 Overall Compliance Score
- Aggregate score (0-100)
- Violation summary

## 4. Execution Performance Metrics
### 4.1 Step Count Analysis
- Total steps: defined, attempted, completed, skipped, failed
- Step distribution by status

### 4.2 Success and Failure Rates
- Overall success/failure rates
- Success rates by task
- First-attempt vs eventual success rates
- Multi-level metrics (step, task, SPEC)

### 4.3 Backup Method Usage
- Primary vs backup usage distribution
- Success rates per method type
- Backup effectiveness scores
- Usage frequency patterns

### 4.4 Mode Usage and Escalations
- Silent vs collaborative mode distribution
- Mode switches count
- Escalation triggers breakdown
- Escalation appropriateness

### 4.5 Time Metrics
- Time per step (min, max, average, median)
- Time per task
- Total execution time
- Time distribution analysis
- Longest/shortest steps

### 4.6 Error Propagation
- Dependency tracking
- Propagation decision counts
- Propagation effectiveness score
- Example instances

### 4.7 Retry Patterns
- Average retries per step
- Max retries reached
- Retry exhaustion rate
- Retry success rate
- Thoroughness score

### 4.8 Efficiency and Productivity
- Steps attempted vs planned
- Steps per hour
- Rework rate
- Productivity score

### 4.9 Critical vs Non-Critical Performance
- Performance comparison by critical flag
- Success rate differences
- Time impact analysis

### 4.10 Expected vs Actual Outputs
- Output match rates
- Mismatch analysis
- Quality assessment

### 4.11 Error Frequency
- Total errors by category
- Top 10 most common errors
- Error concentration

### 4.12 Token Usage (if available)
- Tokens per step/task
- Total token consumption
- Token efficiency metrics

## 5. Behaviour Correlation Analysis
### 5.1 Identified Correlations
- Goal characteristics vs execution behaviour
- Correlation strength assessment

### 5.2 Causality Assessment
- Causal vs correlational relationships
- Confidence levels

### 5.3 Confounding Factors
- External influences
- Mediation effects

## 6. Quality Assessment
### 6.1 Task Decomposition Quality
- Per-task quality scores
- Decomposition effectiveness

### 6.2 Step Quality Analysis
- Atomicity assessment
- Critical flag appropriateness

### 6.3 Method Selection Quality
- Primary/backup rationale
- Method effectiveness

## 7. Error Analysis
### 7.1 Error Categorisation
- Error type distribution
- Frequency patterns

### 7.2 Root Cause Analysis
- Root cause mapping
- Prevention opportunities

### 7.3 Recovery Effectiveness
- Recovery success rates
- Backup effectiveness

### 7.4 Constitutional Violations
- Violation breakdown by article
- Severity assessment

## 8. Recommendations
### 8.1 Goal Formulation Improvements
[Specific, actionable recommendations]

### 8.2 SPEC Design Enhancements
[Specific, actionable recommendations]

### 8.3 Execution Optimisation
[Specific, actionable recommendations]

### 8.4 Constitutional Compliance
[Specific, actionable recommendations]

### 8.5 Future Research Directions
[Areas for deeper investigation]

## Appendices
### A. Raw Data Tables
### B. Propagation Examples (Full Quotes)
### C. Metrics Calculation Methods
### D. Source Citations
```

---

**End of Dev_Analysis_SPEC.md**

This SPEC is designed to be reusable across multiple test SPEC analyses, enabling systematic comparison and pattern identification.


```

```markdown
# Dev Analysis SPEC

**Version:** 1.0  
**Last Updated:** 2025-11-03  
**Purpose:** Analyse development of test SPECs to identify patterns, metrics, and goal text propagation effects

---

## Goal

Perform comprehensive analysis of a test SPEC's development lifecycle to identify how initial goal text propagates through the system and impacts agent behaviour, execution accuracy, and project outcomes.

---

## Software Stack & Architecture

**Not Applicable** - This is an analysis task, not a build goal.

---

## Definition of Complete

What must exist and be verified:
- [ ] **Primary deliverable:** Comprehensive analysis report (markdown format) covering all analysis areas
- [ ] **Quality standards met:** 
  - All 8 analysis tasks completed with documented findings
  - Goal text propagation patterns identified with specific examples
  - Quantitative metrics calculated for execution performance
  - Cross-correlation analysis between goal characteristics and outcomes
  - Recommendations provided based on findings
- [ ] **Verification method:** 
  - Report contains all required sections (see tasks below)
  - Quantitative metrics include numerical values with source citations
  - At least 3 specific examples of goal text propagation documented
  - Recommendations are actionable and linked to specific findings

---

## Definitions

- **goal**: Analyse how initial goal text characteristics influence SPEC development and execution
- **task[n]**: Discrete analysis objectives examining different aspects of SPEC development
- **step[m]**: Concrete analytical actions within each task
- **backup[p]**: Alternative analysis methods when primary approach is blocked
- **critical_flag**: Boolean indicating whether analysis step is essential to overall goal
- **mode**: `silent` (fully autonomous - NO USER INPUT REQUIRED except initial project folder location)
- **progress.json**: Structured log tracking analysis execution and findings
- **project_folder**: Target development project folder path (ONLY required user input)

---

## Components

Analysis requires access to:
- **Test SPEC files:** spec_[descriptor].md, parameters_[descriptor].toml, exe_[descriptor].md
- **Execution logs:** progress_[descriptor].json
- **Project artefacts:** Code files, documentation, error logs, validation reports
- **Chat history:** Conversation transcripts showing agent thinking and decision-making
- **Constitution:** __SPEC_Engine/_Constitution/constitution.md for compliance checking

**Machine-Readable Components:**  
See `[components]` section in parameters_Dev_Analysis.toml

---

## Constraints

- Analysis must be objective and evidence-based
- All metrics must be traceable to source data
- Goal text propagation analysis must include minimum 3 concrete examples
- Quantitative metrics must include: success rates, error rates, mode escalations, backup usage
- Findings must distinguish correlation from causation
- Recommendations must be specific and actionable

**Machine-Readable Constraints:**  
See `[constraints]` section in parameters_Dev_Analysis.toml:
- `min_examples_required = 3` (goal text propagation examples)
- `metrics_evidence_based = true` (all metrics must cite sources)
- `recommendation_specificity = "actionable"` (recommendations must be implementable)

---

## User Stories

- As a **SPEC developer**, I want to understand how goal phrasing impacts development so I can write more effective goals
- As a **system architect**, I want to identify patterns in SPEC execution so I can improve the framework
- As a **researcher**, I want to quantify goal text propagation so I can understand agent behaviour correlation
- As a **project manager**, I want metrics on SPEC performance so I can assess project quality

---

## Analysis Framework

This SPEC analyses development across 8 integrated dimensions:

### Dimension 1: Goal Text Characteristics
- Length (word count, character count, sentence complexity)
- Number of distinct elements/requirements
- Literacy level (Flesch-Kincaid, technical density)
- Formatting (structure, lists, emphasis)
- Familiarity/Technical specificity

### Dimension 2: Goal Text Propagation
- How goal language appears in task descriptions
- Goal terminology in step definitions
- Phrasing patterns in agent thinking/reasoning
- Language consistency across SPEC artefacts
- Conceptual drift from goal to implementation

### Dimension 3: Constitutional Compliance
- Article I-XIV adherence scoring
- Critical flag balance (target: 40-60%)
- Backup method quality assessment
- Bridging quality (Markdown-TOML sync)
- Validation checkpoint outcomes

### Dimension 4: Execution Performance
- Step success/failure rates
- Backup invocation frequency
- Mode escalation patterns
- Error propagation effectiveness
- Retry patterns and exhaustion

### Dimension 5: Agent Behaviour Correlation
- Thinking patterns vs goal complexity
- Decision quality vs goal clarity
- Output quality vs goal specificity
- Backup selection vs goal ambiguity
- Escalation triggers vs goal characteristics

### Dimension 6: Per-Task/Step Behaviour
- Task decomposition quality
- Step atomicity assessment
- Critical flag appropriateness
- Expected output clarity
- Method selection rationale

### Dimension 7: Error Analysis
- Error types and frequencies
- Root cause patterns
- Recovery effectiveness
- Constitutional violations
- Preventable vs inherent errors

### Dimension 8: Outcome Metrics
- Goal achievement status (ACHIEVED/PARTIAL/NOT_ACHIEVED)
- Deliverable completeness
- Quality standards met
- Time/step efficiency
- Comparison to expected outcomes

---

## Task [0]: Initialize Analysis and Gather Project Metadata

**TOML Reference:** `tasks[id=0]` in parameters_Dev_Analysis.toml  
**Purpose:** Locate project folder, scan structure, and collect comprehensive metadata

- **Step [0]:** Receive project folder location (ONLY USER INPUT REQUIRED)
  - **Primary method:** Prompt for project development folder path
  - **Expected output:** Absolute path to project folder
  - **Critical:** true
  - **Mode:** collaborative (ONE TIME ONLY - for folder path input)

- **Step [1]:** Scan and map complete project structure
  - **Primary method:** Recursively list all files and directories in project folder
  - **Backup [1]:** If permissions issue, request accessible subset of project
  - **Expected output:** Complete file tree with full paths
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count and categorise all files
  - **Primary method:** Count files by type: .md, .toml, .json, .py, .js, .ts, .log, .txt, etc.
  - **Expected output:** File count table with breakdown by extension
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Calculate file sizes and total project size
  - **Primary method:** Get file size for each file, sum by category and total
  - **Expected output:** Size metrics table (bytes, KB, MB) by file type and total
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Extract all timestamps
  - **Primary method:** Collect creation, modification, access times for all relevant files
  - **Backup [1]:** If timestamps unavailable, use git history if present
  - **Expected output:** Timeline table showing project chronology
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Calculate development duration
  - **Primary method:** Calculate time from earliest to latest timestamp, identify development phases
  - **Expected output:** Development duration metrics: total time, active development periods, gaps
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Count tokens across all text files
  - **Primary method:** For each text-based file, count tokens (words, characters, estimated LLM tokens)
  - **Backup [1]:** If token counting unavailable, use word/character counts as proxy
  - **Expected output:** Token count table by file type with totals
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Identify and catalogue error logs
  - **Primary method:** Locate all error log files, count error entries, categorise by severity
  - **Expected output:** Error log inventory with counts and locations
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Identify and catalogue chat/conversation logs
  - **Primary method:** Locate chat transcripts, conversation logs, agent thinking logs
  - **Backup [1]:** Check common locations: root, logs folder, subdirectories
  - **Expected output:** Conversation log inventory with file paths and sizes
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Count conversation turns and messages
  - **Primary method:** Parse chat logs to count: total messages, user messages, agent messages, turns
  - **Expected output:** Conversation metrics table
  - **Critical:** false
  - **Mode:** silent

- **Step [10]:** Identify SPEC files and versions
  - **Primary method:** Locate all spec_*.md, parameters_*.toml, exe_*.md, progress_*.json files
  - **Expected output:** SPEC file inventory with versions and timestamps
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Create project metadata snapshot
  - **Primary method:** Aggregate all collected metrics into comprehensive metadata document
  - **Expected output:** Project metadata JSON with all metrics organized
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Project folder scanned, all files catalogued, comprehensive metrics collected
- **Logging:** Record all metadata in progress_Dev_Analysis.json for reference throughout analysis

---

## Task [1]: Extract and Characterise Initial Goal Text

**TOML Reference:** `tasks[id=1]` in parameters_Dev_Analysis.toml  
**Purpose:** Establish baseline characteristics of the goal that initiated SPEC development

- **Step [1]:** Locate and extract initial goal text
  - **Primary method:** Read SPEC markdown file Goal section and chat history for original user goal statement
  - **Backup [1]:** If chat history unavailable, use goal section from spec_[descriptor].md as proxy
  - **Expected output:** Exact goal text with source citation and timestamp
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Calculate quantitative text characteristics
  - **Primary method:** Compute word count, character count, sentence count, avg sentence length, Flesch-Kincaid score
  - **Backup [1]:** If automated scoring unavailable, perform manual classification (simple/moderate/complex)
  - **Expected output:** Table with numerical metrics and complexity classification
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Identify distinct elements and requirements
  - **Primary method:** Parse goal for discrete requirements, constraints, deliverables, success criteria
  - **Backup [1]:** Use linguistic chunking to identify conceptual units if structure unclear
  - **Expected output:** Numbered list of distinct elements (target: 3-10 elements)
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess technical specificity and domain familiarity
  - **Primary method:** Identify technical terms, domain-specific language, assumed knowledge, explicit vs implicit requirements
  - **Backup [1]:** Compare vocabulary against common vs specialised term databases
  - **Expected output:** Technical specificity score (1-5 scale) with justification and term examples
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Analyse formatting and structure
  - **Primary method:** Document use of lists, emphasis, sections, explicit vs narrative format
  - **Expected output:** Formatting assessment noting structural elements present
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All goal characteristics documented with quantitative metrics where possible
- **Logging:** Record all measurements in progress_Dev_Analysis.json for correlation analysis

---

## Task [2]: Map Goal Text Propagation Throughout Project

**TOML Reference:** `tasks[id=2]` in parameters_Dev_Analysis.toml  
**Purpose:** Track how initial goal language and concepts propagate through SPEC artefacts

- **Step [1]:** Extract task descriptions from SPEC
  - **Primary method:** Parse spec_[descriptor].md for all task titles and descriptions
  - **Expected output:** List of tasks with full text
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify goal language in task descriptions
  - **Primary method:** Compare task descriptions to goal text, noting shared terminology, conceptual overlap, verbatim phrases
  - **Backup [1]:** Use semantic similarity scoring if direct comparison insufficient
  - **Expected output:** Table mapping goal terms to task descriptions with similarity scores
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Extract step definitions and analyse propagation
  - **Primary method:** Parse all step descriptions, identify goal/task terminology presence, track conceptual consistency
  - **Backup [1]:** Focus on critical steps only if volume is high (>20 steps)
  - **Expected output:** Propagation matrix showing goal→task→step language flow with specific examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse agent thinking and reasoning patterns
  - **Primary method:** Review chat history/logs for agent internal reasoning, note how goal concepts appear in thinking
  - **Backup [1]:** If full chat unavailable, analyse progress.json logs for method justifications
  - **Expected output:** Minimum 3 specific examples of goal text influencing agent reasoning with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify conceptual drift
  - **Primary method:** Compare final implementation/outputs against original goal, identify divergences in terminology, scope, or interpretation
  - **Expected output:** Conceptual drift assessment noting where implementation departed from goal language
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Assess language consistency across artefacts
  - **Primary method:** Check terminology consistency across spec.md, parameters.toml, progress.json, deliverables
  - **Expected output:** Consistency report identifying where language fragmented or evolved
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Minimum 3 concrete examples of goal text propagation documented with direct quotes
- **Logging:** Record propagation patterns and drift instances in progress_Dev_Analysis.json

---

## Task [3]: Evaluate Constitutional Compliance

**TOML Reference:** `tasks[id=3]` in parameters_Dev_Analysis.toml  
**Purpose:** Assess adherence to SPEC Engine Constitution (Articles I-XIV)

- **Step [1]:** Validate Article I compliance (North Star Principle)
  - **Primary method:** Verify goal singularity, clarity, measurability, explicitness
  - **Expected output:** Article I compliance score (pass/fail) with justification
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Validate Article II compliance (Hierarchical Structure)
  - **Primary method:** Count tasks (target: 2-5), count steps per task (target: 1-5), verify hierarchy maintained
  - **Backup [1]:** If counts borderline, assess whether structure serves goal effectively
  - **Expected output:** Article II compliance score with quantitative counts
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Validate Article III compliance (Dual-File Mandate)
  - **Primary method:** Cross-check spec.md and parameters.toml for ID matching, structure sync, cross-references
  - **Expected output:** Article III compliance score noting any bridging failures
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Validate Article VI compliance (Critical Flag Discipline)
  - **Primary method:** Calculate critical step percentage (target: 40-60%), assess appropriateness of critical flags
  - **Expected output:** Critical balance percentage and appropriateness assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Validate Article VII compliance (Backup Methods)
  - **Primary method:** Review all backup methods to ensure they are alternative reasoning paths, not retries
  - **Backup [1]:** Sample backup methods if total exceeds 15
  - **Expected output:** Backup quality score with examples of good/poor backups
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Check Article XIV compliance (if build goal)
  - **Primary method:** If goal contains build/create/system keywords, verify software stack defined, deployment criteria present
  - **Expected output:** Article XIV compliance (N/A or pass/fail with details)
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Review Articles IV, VIII, IX, X compliance from execution
  - **Primary method:** Analyse progress.json for validation execution, error propagation, mode discipline, comprehensive logging
  - **Expected output:** Compliance scores for Articles IV, VIII, IX, X with evidence from logs
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Calculate overall constitutional compliance score
  - **Primary method:** Aggregate individual article scores, weight by severity, generate 0-100 score
  - **Expected output:** Overall compliance score (0-100) with breakdown by article
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All applicable articles assessed with evidence-based scoring
- **Logging:** Record compliance scores and violations in progress_Dev_Analysis.json

---

## Task [4]: Analyse Execution Performance Metrics

**TOML Reference:** `tasks[id=4]` in parameters_Dev_Analysis.toml  
**Purpose:** Extract quantitative performance data from execution logs with comprehensive detail

- **Step [1]:** Parse progress.json for complete step data
  - **Primary method:** Read progress_[descriptor].json, extract ALL fields: task_id, step_id, status, method_used, retry_count, timestamp, mode, critical_flag, expected_output, actual_output, error_messages
  - **Backup [1]:** If progress.json malformed, reconstruct from available logs
  - **Expected output:** Complete step outcome dataset with full detail per step
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count total steps taken
  - **Primary method:** Count: total steps defined, total steps attempted, total steps completed, total steps skipped, total steps failed
  - **Expected output:** Comprehensive step count table with breakdown by status
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Calculate detailed success and failure rates
  - **Primary method:** Compute: overall success rate, failure rate, success rate by task, failure rate by task, first-attempt success rate, eventual success rate (after retries)
  - **Expected output:** Multi-level success/failure metrics table with percentages at step, task, and SPEC levels
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse backup method usage patterns
  - **Primary method:** Count: primary method attempts, primary successes, backup[1] attempts, backup[1] successes, backup[2] attempts, backup[2] successes, calculate success rates per method type
  - **Expected output:** Comprehensive backup usage statistics with success rates, effectiveness scores, and usage frequency distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Track mode usage and escalations
  - **Primary method:** Count: steps in silent mode, steps in collaborative mode, mode switches, categorise escalation triggers (consecutive failures, backup depletion, critical failure, confidence degradation)
  - **Expected output:** Mode usage table, escalation count by trigger type, escalation appropriateness assessment per instance
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Analyse timestamps and time metrics
  - **Primary method:** Extract all timestamps from progress.json, calculate: time per step, time per task, total execution time, longest steps, shortest steps, time distribution
  - **Backup [1]:** If timestamps sparse, use available data and note gaps
  - **Expected output:** Comprehensive time metrics table with duration statistics
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Assess error propagation effectiveness
  - **Primary method:** Identify all steps with dependencies, check if prior failures were read from progress.json, assess propagation handling quality, count propagation decisions
  - **Backup [1]:** If error propagation tracking sparse, infer from step sequence and outcomes
  - **Expected output:** Error propagation effectiveness score with example instances and propagation decision breakdown
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Analyse retry patterns in detail
  - **Primary method:** Extract retry_count per step, calculate: average retries per step, max retries reached, retry exhaustion rate, retry success rate, thoroughness score (methods exhausted before escalation)
  - **Expected output:** Detailed retry pattern analysis with distribution charts and exhaustion assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Calculate efficiency and productivity metrics
  - **Primary method:** Compute: total steps attempted vs planned, steps per task (actual vs expected), average time per step, steps per hour, rework rate (retries/total), productivity score
  - **Expected output:** Comprehensive efficiency metrics table with productivity indicators
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Analyse critical vs non-critical step performance
  - **Primary method:** Separate critical and non-critical steps, compare: success rates, retry rates, time per step, failure impact
  - **Expected output:** Critical flag performance comparison table
  - **Critical:** false
  - **Mode:** silent

- **Step [11]:** Extract and analyse expected vs actual outputs
  - **Primary method:** For each step, compare expected_output defined in SPEC to actual_output logged, categorise: exact match, partial match, mismatch, missing
  - **Expected output:** Output quality assessment with match rate and mismatch analysis
  - **Critical:** true
  - **Mode:** silent

- **Step [12]:** Count and categorise all errors encountered
  - **Primary method:** Extract all error messages from progress.json, categorise by type (validation, execution, resource, logic), count occurrences, identify most frequent errors
  - **Expected output:** Error frequency table by category with top 10 most common errors
  - **Critical:** true
  - **Mode:** silent

- **Step [13]:** Analyse token usage per step (if available)
  - **Primary method:** If token counts logged, extract tokens per step, calculate: tokens per task, total tokens, token efficiency (tokens per successful step)
  - **Backup [1]:** If not logged in progress.json, skip with note
  - **Expected output:** Token usage metrics table (if data available)
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All quantitative metrics calculated with source data citations, minimum 13 metric categories documented
- **Logging:** Record all performance metrics in progress_Dev_Analysis.json

---

## Task [5]: Correlate Agent Behaviour with Goal Characteristics

**TOML Reference:** `tasks[id=5]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify relationships between goal text properties and agent execution behaviour

- **Step [1]:** Establish correlation framework
  - **Primary method:** Define metrics for correlation: goal complexity vs task count, goal clarity vs error rate, goal specificity vs backup usage
  - **Expected output:** Correlation matrix framework listing goal characteristics and behaviour metrics
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Analyse goal complexity vs task decomposition
  - **Primary method:** Correlate goal complexity score (from Task 1) with number of tasks, steps per task, decomposition depth
  - **Backup [1]:** Use qualitative assessment if quantitative correlation weak
  - **Expected output:** Correlation finding: does complex goal lead to more/fewer tasks?
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Analyse goal clarity vs execution accuracy
  - **Primary method:** Correlate goal clarity indicators (explicit requirements, measurable criteria) with success rate, error rate
  - **Expected output:** Correlation finding: does clear goal reduce errors?
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse goal specificity vs backup usage
  - **Primary method:** Correlate technical specificity score with backup invocation rate, backup effectiveness
  - **Expected output:** Correlation finding: does vague goal increase backup reliance?
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Analyse goal formatting vs agent thinking patterns
  - **Primary method:** Review agent reasoning for structured vs narrative goals, assess thinking clarity and organisation
  - **Backup [1]:** If thinking logs sparse, assess output organisation as proxy
  - **Expected output:** Qualitative finding on formatting impact with examples
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Identify confounding factors
  - **Primary method:** Check for external factors affecting correlation: SPEC complexity, domain difficulty, resource availability
  - **Expected output:** List of confounding factors that may explain behaviour patterns
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Distinguish correlation from causation
  - **Primary method:** For each correlation found, assess whether relationship is causal, coincidental, or mediated by other factors using evidence-based analysis
  - **Backup [1]:** Apply Bradford Hill criteria for causation: strength, consistency, specificity, temporality, biological gradient
  - **Expected output:** Causality assessment for each correlation with confidence level and supporting evidence
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Minimum 3 behaviour correlations identified with specific evidence
- **Logging:** Record correlations and causality assessments in progress_Dev_Analysis.json

---

## Task [6]: Assess Per-Task and Per-Step Behaviour Quality

**TOML Reference:** `tasks[id=6]` in parameters_Dev_Analysis.toml  
**Purpose:** Evaluate quality of task decomposition and step execution at granular level

- **Step [1]:** Evaluate task decomposition quality
  - **Primary method:** For each task, assess: Does task serve goal? Is task scope appropriate? Is task self-contained?
  - **Expected output:** Task quality assessment table with scores and rationale per task
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Assess step atomicity
  - **Primary method:** For each step, assess: Is step a single concrete action? Is step scope too broad/narrow? Is step executable?
  - **Backup [1]:** Sample steps if total exceeds 20
  - **Expected output:** Step atomicity assessment with examples of well/poorly scoped steps
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Evaluate critical flag appropriateness
  - **Primary method:** For each critical step, verify: Would failure truly block goal? For non-critical, verify: Can goal succeed without this?
  - **Expected output:** Critical flag appropriateness score with misclassification examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess expected output clarity
  - **Primary method:** For each step, rate expected output: specific/vague, measurable/subjective, achievable/unrealistic
  - **Expected output:** Expected output quality assessment with clarity distribution
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Evaluate method selection rationale
  - **Primary method:** For steps with multiple methods, assess whether primary/backup choices were well-justified
  - **Expected output:** Method selection quality score with examples
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All tasks and representative sample of steps assessed for quality
- **Logging:** Record quality assessments in progress_Dev_Analysis.json

---

## Task [7]: Conduct Comprehensive Error Analysis and Pattern Detection

**TOML Reference:** `tasks[id=7]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify error patterns, root causes, and improvement opportunities through meticulous analysis

- **Step [1]:** Extract and inventory all error sources
  - **Primary method:** Collect errors from: progress.json, error log files (from Task 0), chat logs, validation reports, any other error documentation
  - **Expected output:** Complete error inventory with source file paths and line references
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count total errors across all sources
  - **Primary method:** Count: total errors logged, errors per source type, errors per task, errors per step, error density (errors per 100 steps)
  - **Expected output:** Comprehensive error count table with breakdowns
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Categorise all errors by type and severity
  - **Primary method:** Classify each error by type (validation, execution, resource, logic, syntax, semantic) and severity (critical, major, minor, warning)
  - **Expected output:** Error categorisation matrix with counts and percentages by type and severity
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse error log files in detail
  - **Primary method:** For each error log file identified in Task 0, parse contents, extract: error timestamps, error messages, stack traces, context, frequency
  - **Backup [1]:** If logs are unstructured, extract what's available and note format issues
  - **Expected output:** Detailed error log analysis with structured data extracted from logs
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify error frequency patterns and hotspots
  - **Primary method:** Analyse which tasks/steps had highest error rates, identify repeated failures, calculate error concentration by task/step/time period
  - **Expected output:** Error hotspot analysis showing: high-error tasks, high-error steps, error clustering patterns, temporal error distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Conduct comprehensive root cause analysis
  - **Primary method:** For each error category, trace to root cause: SPEC design flaw, step definition ambiguity, resource limitation, goal ambiguity, external dependency, constitutional violation, tooling issue
  - **Backup [1]:** Apply 5 Whys methodology for complex errors
  - **Expected output:** Root cause mapping for all error categories with prevention recommendations per cause
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Analyse error propagation chains
  - **Primary method:** Trace errors that caused downstream failures, identify cascading error patterns, assess propagation handling
  - **Expected output:** Error propagation chain diagram with cascade analysis
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Assess recovery effectiveness and time
  - **Primary method:** For each error, determine: was it recovered? which method succeeded? how many attempts? time to recovery? was escalation needed?
  - **Expected output:** Recovery effectiveness metrics: recovery rate, average attempts to recovery, average time to recovery, escalation rate, recovery method distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Analyse error messages for clarity and actionability
  - **Primary method:** Review all error messages, rate: clarity (clear/vague), actionability (specific guidance/generic), completeness (context provided/missing)
  - **Expected output:** Error message quality assessment with examples of good/poor messages
  - **Critical:** false
  - **Mode:** silent

- **Step [10]:** Identify constitutional violations
  - **Primary method:** Check progress.json constitutional_compliance section, extract violations; cross-reference error patterns with constitutional articles
  - **Backup [1]:** Manual review of execution logs if compliance tracking absent
  - **Expected output:** Constitutional violation summary with article breakdown, severity, and correlation to errors
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Distinguish preventable from inherent errors
  - **Primary method:** Classify each error: preventable through better SPEC design, preventable through better execution, inherent to task complexity, external/environmental, resource-based
  - **Expected output:** Error preventability classification with percentages and improvement focus areas
  - **Critical:** true
  - **Mode:** silent

- **Step [12]:** Calculate error-related time costs
  - **Primary method:** Sum time spent on: failed steps, retries, error recovery, escalations, rework
  - **Backup [1]:** Estimate if precise timestamps unavailable
  - **Expected output:** Error cost metrics: time lost to errors, percentage of total time, cost per error category
  - **Critical:** false
  - **Mode:** silent

- **Step [13]:** Identify error patterns by goal characteristics
  - **Primary method:** Correlate error rates/types with goal complexity, clarity, specificity metrics from Task 1
  - **Expected output:** Error pattern correlation analysis linking errors to goal characteristics
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All errors from all sources analysed with root causes, minimum 13 error metric categories documented
- **Logging:** Record comprehensive error analysis findings in progress_Dev_Analysis.json

---

## Task [8]: Generate Comprehensive Analysis Report with Recommendations

**TOML Reference:** `tasks[id=8]` in parameters_Dev_Analysis.toml  
**Purpose:** Synthesise all findings into actionable report

- **Step [1]:** Structure report outline
  - **Primary method:** Create report sections: Executive Summary, Goal Analysis, Propagation Findings, Performance Metrics, Correlations, Quality Assessment, Error Analysis, Recommendations
  - **Expected output:** Report outline with section headers
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Write Executive Summary
  - **Primary method:** Synthesise key findings: goal characteristics summary, main propagation patterns, overall performance, critical insights
  - **Expected output:** 200-300 word executive summary highlighting main findings
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Compile Goal Text Analysis section
  - **Primary method:** Aggregate Task 1 findings: goal characteristics table, complexity assessment, element breakdown
  - **Expected output:** Goal Text Analysis section with all metrics and assessments
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Compile Goal Text Propagation section
  - **Primary method:** Aggregate Task 2 findings: propagation examples, language flow diagram, conceptual drift assessment
  - **Expected output:** Goal Text Propagation section with minimum 3 concrete examples with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Compile Constitutional Compliance section
  - **Primary method:** Aggregate Task 3 findings: article-by-article scores, overall compliance score, violation summary
  - **Expected output:** Constitutional Compliance section with compliance scorecard
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Compile Execution Performance section
  - **Primary method:** Aggregate Task 4 findings: success/failure rates, backup usage, mode escalations, efficiency metrics
  - **Expected output:** Execution Performance section with metrics tables
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Compile Behaviour Correlation section
  - **Primary method:** Aggregate Task 5 findings: correlation matrix, causality assessments, confounding factors
  - **Expected output:** Behaviour Correlation section with correlation findings
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Compile Quality Assessment section
  - **Primary method:** Aggregate Task 6 findings: task quality scores, step atomicity, critical flag appropriateness
  - **Expected output:** Quality Assessment section with quality distributions
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Compile Error Analysis section
  - **Primary method:** Aggregate Task 7 findings: error categories, root causes, recovery effectiveness, preventability
  - **Expected output:** Error Analysis section with error breakdown and patterns
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Generate actionable recommendations
  - **Primary method:** Based on all findings, create specific recommendations for: goal formulation improvement, SPEC design enhancement, execution optimisation, constitutional compliance, error prevention, efficiency improvements
  - **Backup [1]:** Use evidence-based recommendation framework: identify issue, link to finding, propose specific action, justify with data
  - **Expected output:** Minimum 8 specific, actionable recommendations linked to findings with priority levels
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Add cross-project comparison framework (if applicable)
  - **Primary method:** If analysing multiple SPECs, create comparison tables for key metrics across projects
  - **Expected output:** Cross-project comparison section (optional, only if multiple projects analysed)
  - **Critical:** false
  - **Mode:** silent

- **Step [12]:** Finalise report formatting and references
  - **Primary method:** Ensure all sections formatted consistently, add table of contents, verify all data citations present
  - **Expected output:** Complete, polished analysis report in markdown format
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Report contains all required sections, metrics are evidence-based, recommendations are actionable
- **Logging:** Record report completion in progress_Dev_Analysis.json with final deliverable path

---

## Bridging: Markdown ↔ TOML Synchronisation

This spec file (Dev_Analysis_SPEC.md) must maintain perfect alignment with its companion file (parameters_Dev_Analysis.toml).

**Bridging Requirements:**
1. Each task in this file must have corresponding `[[tasks]]` entry in TOML with matching ID (1-8)
2. Each step within a task must have corresponding `[[tasks.steps]]` entry with matching ID
3. Expected outputs in this file must match `expected_output` fields in TOML
4. Critical flags must be synchronised between files
5. Constraints referenced must exist in TOML `[constraints]` section

**Example Cross-References:**
- "See `constraints.min_examples_required` in parameters_Dev_Analysis.toml" (Task 2, Step 4)
- "As defined in `tasks[id=4]` in TOML" (Task 4 reference)
- "Must satisfy TOML verification requirements" (All task verifications)

The exe_Dev_Analysis.md controller will validate this synchronisation during initialisation (Section 1.8).

---

## Instructions for LLM Executor

1. **Start with goal understanding**: This analysis examines how goal text propagates and influences SPEC development
2. **Execute tasks sequentially**: Tasks 1-2 gather data, Tasks 3-7 analyse patterns, Task 8 synthesises findings
3. **Maintain objectivity**: Base all findings on evidence from files, logs, and artefacts
4. **Track propagation carefully**: Pay special attention to how exact goal language appears throughout project
5. **Quantify where possible**: Use numerical metrics rather than subjective assessments when feasible
6. **Distinguish correlation from causation**: Note relationships but assess causality carefully
7. **Document thoroughly**: Log all findings in progress_Dev_Analysis.json for traceability
8. **Focus on actionability**: Recommendations should be specific and implementable
9. **Read prior outcomes**: Before each step, check progress.json for relevant prior findings
10. **Escalate appropriately**: Use collaborative mode for causality judgements and unclear recommendation priorities

---

## Expected Analysis Output Structure

The final report should follow this structure:

```markdown
# SPEC Development Analysis Report

## Executive Summary
[200-300 word overview of key findings]

## 0. Project Metadata Overview
### 0.1 Project Structure
- Total files by type
- Total project size
- File tree summary

### 0.2 Development Timeline
- Total development duration
- Development phases
- Key timestamps

### 0.3 Token Metrics
- Total tokens across all files
- Token distribution by file type
- Estimated LLM token usage

### 0.4 File Inventory
- SPEC files identified
- Error logs found
- Chat/conversation logs
- Other key artefacts

### 0.5 Conversation Metrics
- Total messages/turns
- User vs agent message counts
- Conversation duration

## 1. Goal Text Analysis
### 1.1 Initial Goal Characteristics
- Quantitative metrics table
- Complexity classification
- Element breakdown

### 1.2 Technical Specificity Assessment
- Specificity score with justification
- Domain terminology analysis

## 2. Goal Text Propagation Analysis
### 2.1 Propagation Through Tasks
- Task-level language mapping
- Specific examples with quotes

### 2.2 Propagation Through Steps
- Step-level language mapping
- Propagation matrix

### 2.3 Agent Thinking Patterns
- Minimum 3 examples of goal text in reasoning
- Direct quotes from logs/chat

### 2.4 Conceptual Drift Assessment
- Identified divergences
- Impact analysis

## 3. Constitutional Compliance Assessment
### 3.1 Article-by-Article Scores
- Individual article compliance
- Evidence for each assessment

### 3.2 Overall Compliance Score
- Aggregate score (0-100)
- Violation summary

## 4. Execution Performance Metrics
### 4.1 Step Count Analysis
- Total steps: defined, attempted, completed, skipped, failed
- Step distribution by status

### 4.2 Success and Failure Rates
- Overall success/failure rates
- Success rates by task
- First-attempt vs eventual success rates
- Multi-level metrics (step, task, SPEC)

### 4.3 Backup Method Usage
- Primary vs backup usage distribution
- Success rates per method type
- Backup effectiveness scores
- Usage frequency patterns

### 4.4 Mode Usage and Escalations
- Silent vs collaborative mode distribution
- Mode switches count
- Escalation triggers breakdown
- Escalation appropriateness

### 4.5 Time Metrics
- Time per step (min, max, average, median)
- Time per task
- Total execution time
- Time distribution analysis
- Longest/shortest steps

### 4.6 Error Propagation
- Dependency tracking
- Propagation decision counts
- Propagation effectiveness score
- Example instances

### 4.7 Retry Patterns
- Average retries per step
- Max retries reached
- Retry exhaustion rate
- Retry success rate
- Thoroughness score

### 4.8 Efficiency and Productivity
- Steps attempted vs planned
- Steps per hour
- Rework rate
- Productivity score

### 4.9 Critical vs Non-Critical Performance
- Performance comparison by critical flag
- Success rate differences
- Time impact analysis

### 4.10 Expected vs Actual Outputs
- Output match rates
- Mismatch analysis
- Quality assessment

### 4.11 Error Frequency
- Total errors by category
- Top 10 most common errors
- Error concentration

### 4.12 Token Usage (if available)
- Tokens per step/task
- Total token consumption
- Token efficiency metrics

## 5. Behaviour Correlation Analysis
### 5.1 Identified Correlations
- Goal characteristics vs execution behaviour
- Correlation strength assessment

### 5.2 Causality Assessment
- Causal vs correlational relationships
- Confidence levels

### 5.3 Confounding Factors
- External influences
- Mediation effects

## 6. Quality Assessment
### 6.1 Task Decomposition Quality
- Per-task quality scores
- Decomposition effectiveness

### 6.2 Step Quality Analysis
- Atomicity assessment
- Critical flag appropriateness

### 6.3 Method Selection Quality
- Primary/backup rationale
- Method effectiveness

## 7. Comprehensive Error Analysis
### 7.1 Error Source Inventory
- All error sources identified
- Error counts by source
- Source file references

### 7.2 Total Error Counts
- Total errors across all sources
- Errors per task
- Errors per step
- Error density (per 100 steps)

### 7.3 Error Categorisation Matrix
- Error types: validation, execution, resource, logic, syntax, semantic
- Error severity: critical, major, minor, warning
- Type-severity distribution

### 7.4 Error Log File Analysis
- Detailed analysis per log file
- Error timestamps
- Stack traces and context
- Frequency distributions

### 7.5 Error Frequency Patterns and Hotspots
- High-error tasks
- High-error steps
- Error clustering patterns
- Temporal error distribution
- Error concentration analysis

### 7.6 Root Cause Analysis
- Root cause mapping by category
- SPEC design flaws
- Step definition ambiguities
- Resource limitations
- Goal ambiguity impacts
- External dependencies
- Prevention recommendations per cause

### 7.7 Error Propagation Chains
- Cascading error patterns
- Downstream failure analysis
- Propagation chain diagrams

### 7.8 Recovery Effectiveness
- Recovery rate
- Average attempts to recovery
- Average time to recovery
- Escalation rate
- Recovery method distribution

### 7.9 Error Message Quality
- Clarity assessment
- Actionability assessment
- Completeness assessment
- Examples of good/poor messages

### 7.10 Constitutional Violations
- Violation breakdown by article
- Severity levels
- Correlation to errors

### 7.11 Error Preventability Classification
- Preventable vs inherent errors
- Percentages by category
- Improvement focus areas

### 7.12 Error-Related Time Costs
- Time lost to errors
- Percentage of total time
- Cost per error category

### 7.13 Error Patterns by Goal Characteristics
- Correlation between errors and goal complexity
- Error patterns by goal clarity
- Goal specificity impact on errors

## 8. Recommendations
### 8.1 Goal Formulation Improvements
[Specific, actionable recommendations]

### 8.2 SPEC Design Enhancements
[Specific, actionable recommendations]

### 8.3 Execution Optimisation
[Specific, actionable recommendations]

### 8.4 Constitutional Compliance
[Specific, actionable recommendations]

### 8.5 Future Research Directions
[Areas for deeper investigation]

## Appendices
### A. Raw Data Tables
### B. Propagation Examples (Full Quotes)
### C. Metrics Calculation Methods
### D. Source Citations
```

---

**End of Dev_Analysis_SPEC.md**

This SPEC is designed to be reusable across multiple test SPEC analyses, enabling systematic comparison and pattern identification.


```

```markdown
# Dev Analysis SPEC

**Version:** 1.0  
**Last Updated:** 2025-11-03  
**Purpose:** Analyse development of test SPECs to identify patterns, metrics, and goal text propagation effects

---

## Goal

Perform comprehensive analysis of a test SPEC's development lifecycle to identify how initial goal text propagates through the system and impacts agent behaviour, execution accuracy, and project outcomes.

---

## Software Stack & Architecture

**Not Applicable** - This is an analysis task, not a build goal.

---

## Definition of Complete

What must exist and be verified:
- [ ] **Primary deliverable:** Comprehensive analysis report (markdown format) covering all analysis areas
- [ ] **Quality standards met:** 
  - All 8 analysis tasks completed with documented findings
  - Goal text propagation patterns identified with specific examples
  - Quantitative metrics calculated for execution performance
  - Cross-correlation analysis between goal characteristics and outcomes
  - Recommendations provided based on findings
- [ ] **Verification method:** 
  - Report contains all required sections (see tasks below)
  - Quantitative metrics include numerical values with source citations
  - At least 3 specific examples of goal text propagation documented
  - Recommendations are actionable and linked to specific findings

---

## Definitions

- **goal**: Analyse how initial goal text characteristics influence SPEC development and execution
- **task[n]**: Discrete analysis objectives examining different aspects of SPEC development
- **step[m]**: Concrete analytical actions within each task
- **backup[p]**: Alternative analysis methods when primary approach is blocked
- **critical_flag**: Boolean indicating whether analysis step is essential to overall goal
- **mode**: `silent` (fully autonomous - NO USER INPUT REQUIRED except initial project folder location)
- **progress.json**: Structured log tracking analysis execution and findings
- **project_folder**: Target development project folder path (ONLY required user input)

---

## Components

Analysis requires access to:
- **Test SPEC files:** spec_[descriptor].md, parameters_[descriptor].toml, exe_[descriptor].md
- **Execution logs:** progress_[descriptor].json
- **Project artefacts:** Code files, documentation, error logs, validation reports
- **Chat history:** Conversation transcripts showing agent thinking and decision-making
- **Constitution:** __SPEC_Engine/_Constitution/constitution.md for compliance checking

**Machine-Readable Components:**  
See `[components]` section in parameters_Dev_Analysis.toml

---

## Constraints

- Analysis must be objective and evidence-based
- All metrics must be traceable to source data
- Goal text propagation analysis must include minimum 3 concrete examples
- Quantitative metrics must include: success rates, error rates, mode escalations, backup usage
- Findings must distinguish correlation from causation
- Recommendations must be specific and actionable

**Machine-Readable Constraints:**  
See `[constraints]` section in parameters_Dev_Analysis.toml:
- `min_examples_required = 3` (goal text propagation examples)
- `metrics_evidence_based = true` (all metrics must cite sources)
- `recommendation_specificity = "actionable"` (recommendations must be implementable)

---

## User Stories

- As a **SPEC developer**, I want to understand how goal phrasing impacts development so I can write more effective goals
- As a **system architect**, I want to identify patterns in SPEC execution so I can improve the framework
- As a **researcher**, I want to quantify goal text propagation so I can understand agent behaviour correlation
- As a **project manager**, I want metrics on SPEC performance so I can assess project quality

---

## Analysis Framework

This SPEC analyses development across 8 integrated dimensions:

### Dimension 1: Goal Text Characteristics
- Length (word count, character count, sentence complexity)
- Number of distinct elements/requirements
- Literacy level (Flesch-Kincaid, technical density)
- Formatting (structure, lists, emphasis)
- Familiarity/Technical specificity

### Dimension 2: Goal Text Propagation
- How goal language appears in task descriptions
- Goal terminology in step definitions
- Phrasing patterns in agent thinking/reasoning
- Language consistency across SPEC artefacts
- Conceptual drift from goal to implementation

### Dimension 3: Constitutional Compliance
- Article I-XIV adherence scoring
- Critical flag balance (target: 40-60%)
- Backup method quality assessment
- Bridging quality (Markdown-TOML sync)
- Validation checkpoint outcomes

### Dimension 4: Execution Performance
- Step success/failure rates
- Backup invocation frequency
- Mode escalation patterns
- Error propagation effectiveness
- Retry patterns and exhaustion

### Dimension 5: Agent Behaviour Correlation
- Thinking patterns vs goal complexity
- Decision quality vs goal clarity
- Output quality vs goal specificity
- Backup selection vs goal ambiguity
- Escalation triggers vs goal characteristics

### Dimension 6: Per-Task/Step Behaviour
- Task decomposition quality
- Step atomicity assessment
- Critical flag appropriateness
- Expected output clarity
- Method selection rationale

### Dimension 7: Error Analysis
- Error types and frequencies
- Root cause patterns
- Recovery effectiveness
- Constitutional violations
- Preventable vs inherent errors

### Dimension 8: Outcome Metrics
- Goal achievement status (ACHIEVED/PARTIAL/NOT_ACHIEVED)
- Deliverable completeness
- Quality standards met
- Time/step efficiency
- Comparison to expected outcomes

---

## Task [0]: Initialize Analysis and Gather Project Metadata

**TOML Reference:** `tasks[id=0]` in parameters_Dev_Analysis.toml  
**Purpose:** Locate project folder, scan structure, and collect comprehensive metadata

- **Step [0]:** Receive project folder location (ONLY USER INPUT REQUIRED)
  - **Primary method:** Prompt for project development folder path
  - **Expected output:** Absolute path to project folder
  - **Critical:** true
  - **Mode:** collaborative (ONE TIME ONLY - for folder path input)

- **Step [1]:** Scan and map complete project structure
  - **Primary method:** Recursively list all files and directories in project folder
  - **Backup [1]:** If permissions issue, request accessible subset of project
  - **Expected output:** Complete file tree with full paths
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count and categorise all files
  - **Primary method:** Count files by type: .md, .toml, .json, .py, .js, .ts, .log, .txt, etc.
  - **Expected output:** File count table with breakdown by extension
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Calculate file sizes and total project size
  - **Primary method:** Get file size for each file, sum by category and total
  - **Expected output:** Size metrics table (bytes, KB, MB) by file type and total
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Extract all timestamps
  - **Primary method:** Collect creation, modification, access times for all relevant files
  - **Backup [1]:** If timestamps unavailable, use git history if present
  - **Expected output:** Timeline table showing project chronology
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Calculate development duration
  - **Primary method:** Calculate time from earliest to latest timestamp, identify development phases
  - **Expected output:** Development duration metrics: total time, active development periods, gaps
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Count tokens across all text files
  - **Primary method:** For each text-based file, count tokens (words, characters, estimated LLM tokens)
  - **Backup [1]:** If token counting unavailable, use word/character counts as proxy
  - **Expected output:** Token count table by file type with totals
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Identify and catalogue error logs
  - **Primary method:** Locate all error log files, count error entries, categorise by severity
  - **Expected output:** Error log inventory with counts and locations
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Identify and catalogue chat/conversation logs
  - **Primary method:** Locate chat transcripts, conversation logs, agent thinking logs
  - **Backup [1]:** Check common locations: root, logs folder, subdirectories
  - **Expected output:** Conversation log inventory with file paths and sizes
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Count conversation turns and messages
  - **Primary method:** Parse chat logs to count: total messages, user messages, agent messages, turns
  - **Expected output:** Conversation metrics table
  - **Critical:** false
  - **Mode:** silent

- **Step [10]:** Identify SPEC files and versions
  - **Primary method:** Locate all spec_*.md, parameters_*.toml, exe_*.md, progress_*.json files
  - **Expected output:** SPEC file inventory with versions and timestamps
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Create project metadata snapshot
  - **Primary method:** Aggregate all collected metrics into comprehensive metadata document
  - **Expected output:** Project metadata JSON with all metrics organized
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Project folder scanned, all files catalogued, comprehensive metrics collected
- **Logging:** Record all metadata in progress_Dev_Analysis.json for reference throughout analysis

---

## Task [1]: Extract and Characterise Initial Goal Text

**TOML Reference:** `tasks[id=1]` in parameters_Dev_Analysis.toml  
**Purpose:** Establish baseline characteristics of the goal that initiated SPEC development

- **Step [1]:** Locate and extract initial goal text
  - **Primary method:** Read SPEC markdown file Goal section and chat history for original user goal statement
  - **Backup [1]:** If chat history unavailable, use goal section from spec_[descriptor].md as proxy
  - **Expected output:** Exact goal text with source citation and timestamp
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Calculate quantitative text characteristics
  - **Primary method:** Compute word count, character count, sentence count, avg sentence length, Flesch-Kincaid score
  - **Backup [1]:** If automated scoring unavailable, perform manual classification (simple/moderate/complex)
  - **Expected output:** Table with numerical metrics and complexity classification
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Identify distinct elements and requirements
  - **Primary method:** Parse goal for discrete requirements, constraints, deliverables, success criteria
  - **Backup [1]:** Use linguistic chunking to identify conceptual units if structure unclear
  - **Expected output:** Numbered list of distinct elements (target: 3-10 elements)
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess technical specificity and domain familiarity
  - **Primary method:** Identify technical terms, domain-specific language, assumed knowledge, explicit vs implicit requirements
  - **Backup [1]:** Compare vocabulary against common vs specialised term databases
  - **Expected output:** Technical specificity score (1-5 scale) with justification and term examples
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Analyse formatting and structure
  - **Primary method:** Document use of lists, emphasis, sections, explicit vs narrative format
  - **Expected output:** Formatting assessment noting structural elements present
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All goal characteristics documented with quantitative metrics where possible
- **Logging:** Record all measurements in progress_Dev_Analysis.json for correlation analysis

---

## Task [2]: Map Goal Text Propagation Throughout Project

**TOML Reference:** `tasks[id=2]` in parameters_Dev_Analysis.toml  
**Purpose:** Track how initial goal language and concepts propagate through SPEC artefacts

- **Step [1]:** Extract task descriptions from SPEC
  - **Primary method:** Parse spec_[descriptor].md for all task titles and descriptions
  - **Expected output:** List of tasks with full text
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify goal language in task descriptions
  - **Primary method:** Compare task descriptions to goal text, noting shared terminology, conceptual overlap, verbatim phrases
  - **Backup [1]:** Use semantic similarity scoring if direct comparison insufficient
  - **Expected output:** Table mapping goal terms to task descriptions with similarity scores
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Extract step definitions and analyse propagation
  - **Primary method:** Parse all step descriptions, identify goal/task terminology presence, track conceptual consistency
  - **Backup [1]:** Focus on critical steps only if volume is high (>20 steps)
  - **Expected output:** Propagation matrix showing goal→task→step language flow with specific examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse agent thinking and reasoning patterns
  - **Primary method:** Review chat history/logs for agent internal reasoning, note how goal concepts appear in thinking
  - **Backup [1]:** If full chat unavailable, analyse progress.json logs for method justifications
  - **Expected output:** Minimum 3 specific examples of goal text influencing agent reasoning with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify conceptual drift
  - **Primary method:** Compare final implementation/outputs against original goal, identify divergences in terminology, scope, or interpretation
  - **Expected output:** Conceptual drift assessment noting where implementation departed from goal language
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Assess language consistency across artefacts
  - **Primary method:** Check terminology consistency across spec.md, parameters.toml, progress.json, deliverables
  - **Expected output:** Consistency report identifying where language fragmented or evolved
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Minimum 3 concrete examples of goal text propagation documented with direct quotes
- **Logging:** Record propagation patterns and drift instances in progress_Dev_Analysis.json

---

## Task [3]: Evaluate Constitutional Compliance

**TOML Reference:** `tasks[id=3]` in parameters_Dev_Analysis.toml  
**Purpose:** Assess adherence to SPEC Engine Constitution (Articles I-XIV)

- **Step [1]:** Validate Article I compliance (North Star Principle)
  - **Primary method:** Verify goal singularity, clarity, measurability, explicitness
  - **Expected output:** Article I compliance score (pass/fail) with justification
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Validate Article II compliance (Hierarchical Structure)
  - **Primary method:** Count tasks (target: 2-5), count steps per task (target: 1-5), verify hierarchy maintained
  - **Backup [1]:** If counts borderline, assess whether structure serves goal effectively
  - **Expected output:** Article II compliance score with quantitative counts
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Validate Article III compliance (Dual-File Mandate)
  - **Primary method:** Cross-check spec.md and parameters.toml for ID matching, structure sync, cross-references
  - **Expected output:** Article III compliance score noting any bridging failures
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Validate Article VI compliance (Critical Flag Discipline)
  - **Primary method:** Calculate critical step percentage (target: 40-60%), assess appropriateness of critical flags
  - **Expected output:** Critical balance percentage and appropriateness assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Validate Article VII compliance (Backup Methods)
  - **Primary method:** Review all backup methods to ensure they are alternative reasoning paths, not retries
  - **Backup [1]:** Sample backup methods if total exceeds 15
  - **Expected output:** Backup quality score with examples of good/poor backups
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Check Article XIV compliance (if build goal)
  - **Primary method:** If goal contains build/create/system keywords, verify software stack defined, deployment criteria present
  - **Expected output:** Article XIV compliance (N/A or pass/fail with details)
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Review Articles IV, VIII, IX, X compliance from execution
  - **Primary method:** Analyse progress.json for validation execution, error propagation, mode discipline, comprehensive logging
  - **Expected output:** Compliance scores for Articles IV, VIII, IX, X with evidence from logs
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Calculate overall constitutional compliance score
  - **Primary method:** Aggregate individual article scores, weight by severity, generate 0-100 score
  - **Expected output:** Overall compliance score (0-100) with breakdown by article
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All applicable articles assessed with evidence-based scoring
- **Logging:** Record compliance scores and violations in progress_Dev_Analysis.json

---

## Task [4]: Analyse Execution Performance Metrics

**TOML Reference:** `tasks[id=4]` in parameters_Dev_Analysis.toml  
**Purpose:** Extract quantitative performance data from execution logs with comprehensive detail

- **Step [1]:** Parse progress.json for complete step data
  - **Primary method:** Read progress_[descriptor].json, extract ALL fields: task_id, step_id, status, method_used, retry_count, timestamp, mode, critical_flag, expected_output, actual_output, error_messages
  - **Backup [1]:** If progress.json malformed, reconstruct from available logs
  - **Expected output:** Complete step outcome dataset with full detail per step
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count total steps taken
  - **Primary method:** Count: total steps defined, total steps attempted, total steps completed, total steps skipped, total steps failed
  - **Expected output:** Comprehensive step count table with breakdown by status
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Calculate detailed success and failure rates
  - **Primary method:** Compute: overall success rate, failure rate, success rate by task, failure rate by task, first-attempt success rate, eventual success rate (after retries)
  - **Expected output:** Multi-level success/failure metrics table with percentages at step, task, and SPEC levels
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse backup method usage patterns
  - **Primary method:** Count: primary method attempts, primary successes, backup[1] attempts, backup[1] successes, backup[2] attempts, backup[2] successes, calculate success rates per method type
  - **Expected output:** Comprehensive backup usage statistics with success rates, effectiveness scores, and usage frequency distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Track mode usage and escalations
  - **Primary method:** Count: steps in silent mode, steps in collaborative mode, mode switches, categorise escalation triggers (consecutive failures, backup depletion, critical failure, confidence degradation)
  - **Expected output:** Mode usage table, escalation count by trigger type, escalation appropriateness assessment per instance
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Analyse timestamps and time metrics
  - **Primary method:** Extract all timestamps from progress.json, calculate: time per step, time per task, total execution time, longest steps, shortest steps, time distribution
  - **Backup [1]:** If timestamps sparse, use available data and note gaps
  - **Expected output:** Comprehensive time metrics table with duration statistics
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Assess error propagation effectiveness
  - **Primary method:** Identify all steps with dependencies, check if prior failures were read from progress.json, assess propagation handling quality, count propagation decisions
  - **Backup [1]:** If error propagation tracking sparse, infer from step sequence and outcomes
  - **Expected output:** Error propagation effectiveness score with example instances and propagation decision breakdown
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Analyse retry patterns in detail
  - **Primary method:** Extract retry_count per step, calculate: average retries per step, max retries reached, retry exhaustion rate, retry success rate, thoroughness score (methods exhausted before escalation)
  - **Expected output:** Detailed retry pattern analysis with distribution charts and exhaustion assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Calculate efficiency and productivity metrics
  - **Primary method:** Compute: total steps attempted vs planned, steps per task (actual vs expected), average time per step, steps per hour, rework rate (retries/total), productivity score
  - **Expected output:** Comprehensive efficiency metrics table with productivity indicators
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Analyse critical vs non-critical step performance
  - **Primary method:** Separate critical and non-critical steps, compare: success rates, retry rates, time per step, failure impact
  - **Expected output:** Critical flag performance comparison table
  - **Critical:** false
  - **Mode:** silent

- **Step [11]:** Extract and analyse expected vs actual outputs
  - **Primary method:** For each step, compare expected_output defined in SPEC to actual_output logged, categorise: exact match, partial match, mismatch, missing
  - **Expected output:** Output quality assessment with match rate and mismatch analysis
  - **Critical:** true
  - **Mode:** silent

- **Step [12]:** Count and categorise all errors encountered
  - **Primary method:** Extract all error messages from progress.json, categorise by type (validation, execution, resource, logic), count occurrences, identify most frequent errors
  - **Expected output:** Error frequency table by category with top 10 most common errors
  - **Critical:** true
  - **Mode:** silent

- **Step [13]:** Analyse token usage per step (if available)
  - **Primary method:** If token counts logged, extract tokens per step, calculate: tokens per task, total tokens, token efficiency (tokens per successful step)
  - **Backup [1]:** If not logged in progress.json, skip with note
  - **Expected output:** Token usage metrics table (if data available)
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All quantitative metrics calculated with source data citations, minimum 13 metric categories documented
- **Logging:** Record all performance metrics in progress_Dev_Analysis.json

---

## Task [5]: Correlate Agent Behaviour with Goal Characteristics

**TOML Reference:** `tasks[id=5]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify relationships between goal text properties and agent execution behaviour

- **Step [1]:** Establish correlation framework
  - **Primary method:** Define metrics for correlation: goal complexity vs task count, goal clarity vs error rate, goal specificity vs backup usage
  - **Expected output:** Correlation matrix framework listing goal characteristics and behaviour metrics
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Analyse goal complexity vs task decomposition
  - **Primary method:** Correlate goal complexity score (from Task 1) with number of tasks, steps per task, decomposition depth
  - **Backup [1]:** Use qualitative assessment if quantitative correlation weak
  - **Expected output:** Correlation finding: does complex goal lead to more/fewer tasks?
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Analyse goal clarity vs execution accuracy
  - **Primary method:** Correlate goal clarity indicators (explicit requirements, measurable criteria) with success rate, error rate
  - **Expected output:** Correlation finding: does clear goal reduce errors?
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse goal specificity vs backup usage
  - **Primary method:** Correlate technical specificity score with backup invocation rate, backup effectiveness
  - **Expected output:** Correlation finding: does vague goal increase backup reliance?
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Analyse goal formatting vs agent thinking patterns
  - **Primary method:** Review agent reasoning for structured vs narrative goals, assess thinking clarity and organisation
  - **Backup [1]:** If thinking logs sparse, assess output organisation as proxy
  - **Expected output:** Qualitative finding on formatting impact with examples
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Identify confounding factors
  - **Primary method:** Check for external factors affecting correlation: SPEC complexity, domain difficulty, resource availability
  - **Expected output:** List of confounding factors that may explain behaviour patterns
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Distinguish correlation from causation
  - **Primary method:** For each correlation found, assess whether relationship is causal, coincidental, or mediated by other factors using evidence-based analysis
  - **Backup [1]:** Apply Bradford Hill criteria for causation: strength, consistency, specificity, temporality, biological gradient
  - **Expected output:** Causality assessment for each correlation with confidence level and supporting evidence
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Minimum 3 behaviour correlations identified with specific evidence
- **Logging:** Record correlations and causality assessments in progress_Dev_Analysis.json

---

## Task [6]: Assess Per-Task and Per-Step Behaviour Quality

**TOML Reference:** `tasks[id=6]` in parameters_Dev_Analysis.toml  
**Purpose:** Evaluate quality of task decomposition and step execution at granular level

- **Step [1]:** Evaluate task decomposition quality
  - **Primary method:** For each task, assess: Does task serve goal? Is task scope appropriate? Is task self-contained?
  - **Expected output:** Task quality assessment table with scores and rationale per task
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Assess step atomicity
  - **Primary method:** For each step, assess: Is step a single concrete action? Is step scope too broad/narrow? Is step executable?
  - **Backup [1]:** Sample steps if total exceeds 20
  - **Expected output:** Step atomicity assessment with examples of well/poorly scoped steps
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Evaluate critical flag appropriateness
  - **Primary method:** For each critical step, verify: Would failure truly block goal? For non-critical, verify: Can goal succeed without this?
  - **Expected output:** Critical flag appropriateness score with misclassification examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess expected output clarity
  - **Primary method:** For each step, rate expected output: specific/vague, measurable/subjective, achievable/unrealistic
  - **Expected output:** Expected output quality assessment with clarity distribution
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Evaluate method selection rationale
  - **Primary method:** For steps with multiple methods, assess whether primary/backup choices were well-justified
  - **Expected output:** Method selection quality score with examples
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All tasks and representative sample of steps assessed for quality
- **Logging:** Record quality assessments in progress_Dev_Analysis.json

---

## Task [7]: Conduct Comprehensive Error Analysis and Pattern Detection

**TOML Reference:** `tasks[id=7]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify error patterns, root causes, and improvement opportunities through meticulous analysis

- **Step [1]:** Extract and inventory all error sources
  - **Primary method:** Collect errors from: progress.json, error log files (from Task 0), chat logs, validation reports, any other error documentation
  - **Expected output:** Complete error inventory with source file paths and line references
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count total errors across all sources
  - **Primary method:** Count: total errors logged, errors per source type, errors per task, errors per step, error density (errors per 100 steps)
  - **Expected output:** Comprehensive error count table with breakdowns
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Categorise all errors by type and severity
  - **Primary method:** Classify each error by type (validation, execution, resource, logic, syntax, semantic) and severity (critical, major, minor, warning)
  - **Expected output:** Error categorisation matrix with counts and percentages by type and severity
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse error log files in detail
  - **Primary method:** For each error log file identified in Task 0, parse contents, extract: error timestamps, error messages, stack traces, context, frequency
  - **Backup [1]:** If logs are unstructured, extract what's available and note format issues
  - **Expected output:** Detailed error log analysis with structured data extracted from logs
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify error frequency patterns and hotspots
  - **Primary method:** Analyse which tasks/steps had highest error rates, identify repeated failures, calculate error concentration by task/step/time period
  - **Expected output:** Error hotspot analysis showing: high-error tasks, high-error steps, error clustering patterns, temporal error distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Conduct comprehensive root cause analysis
  - **Primary method:** For each error category, trace to root cause: SPEC design flaw, step definition ambiguity, resource limitation, goal ambiguity, external dependency, constitutional violation, tooling issue
  - **Backup [1]:** Apply 5 Whys methodology for complex errors
  - **Expected output:** Root cause mapping for all error categories with prevention recommendations per cause
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Analyse error propagation chains
  - **Primary method:** Trace errors that caused downstream failures, identify cascading error patterns, assess propagation handling
  - **Expected output:** Error propagation chain diagram with cascade analysis
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Assess recovery effectiveness and time
  - **Primary method:** For each error, determine: was it recovered? which method succeeded? how many attempts? time to recovery? was escalation needed?
  - **Expected output:** Recovery effectiveness metrics: recovery rate, average attempts to recovery, average time to recovery, escalation rate, recovery method distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Analyse error messages for clarity and actionability
  - **Primary method:** Review all error messages, rate: clarity (clear/vague), actionability (specific guidance/generic), completeness (context provided/missing)
  - **Expected output:** Error message quality assessment with examples of good/poor messages
  - **Critical:** false
  - **Mode:** silent

- **Step [10]:** Identify constitutional violations
  - **Primary method:** Check progress.json constitutional_compliance section, extract violations; cross-reference error patterns with constitutional articles
  - **Backup [1]:** Manual review of execution logs if compliance tracking absent
  - **Expected output:** Constitutional violation summary with article breakdown, severity, and correlation to errors
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Distinguish preventable from inherent errors
  - **Primary method:** Classify each error: preventable through better SPEC design, preventable through better execution, inherent to task complexity, external/environmental, resource-based
  - **Expected output:** Error preventability classification with percentages and improvement focus areas
  - **Critical:** true
  - **Mode:** silent

- **Step [12]:** Calculate error-related time costs
  - **Primary method:** Sum time spent on: failed steps, retries, error recovery, escalations, rework
  - **Backup [1]:** Estimate if precise timestamps unavailable
  - **Expected output:** Error cost metrics: time lost to errors, percentage of total time, cost per error category
  - **Critical:** false
  - **Mode:** silent

- **Step [13]:** Identify error patterns by goal characteristics
  - **Primary method:** Correlate error rates/types with goal complexity, clarity, specificity metrics from Task 1
  - **Expected output:** Error pattern correlation analysis linking errors to goal characteristics
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All errors from all sources analysed with root causes, minimum 13 error metric categories documented
- **Logging:** Record comprehensive error analysis findings in progress_Dev_Analysis.json

---

## Task [8]: Generate Comprehensive Analysis Report with Recommendations

**TOML Reference:** `tasks[id=8]` in parameters_Dev_Analysis.toml  
**Purpose:** Synthesise all findings into actionable report

- **Step [1]:** Structure report outline
  - **Primary method:** Create report sections: Executive Summary, Goal Analysis, Propagation Findings, Performance Metrics, Correlations, Quality Assessment, Error Analysis, Recommendations
  - **Expected output:** Report outline with section headers
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Write Executive Summary
  - **Primary method:** Synthesise key findings: goal characteristics summary, main propagation patterns, overall performance, critical insights
  - **Expected output:** 200-300 word executive summary highlighting main findings
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Compile Goal Text Analysis section
  - **Primary method:** Aggregate Task 1 findings: goal characteristics table, complexity assessment, element breakdown
  - **Expected output:** Goal Text Analysis section with all metrics and assessments
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Compile Goal Text Propagation section
  - **Primary method:** Aggregate Task 2 findings: propagation examples, language flow diagram, conceptual drift assessment
  - **Expected output:** Goal Text Propagation section with minimum 3 concrete examples with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Compile Constitutional Compliance section
  - **Primary method:** Aggregate Task 3 findings: article-by-article scores, overall compliance score, violation summary
  - **Expected output:** Constitutional Compliance section with compliance scorecard
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Compile Execution Performance section
  - **Primary method:** Aggregate Task 4 findings: success/failure rates, backup usage, mode escalations, efficiency metrics
  - **Expected output:** Execution Performance section with metrics tables
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Compile Behaviour Correlation section
  - **Primary method:** Aggregate Task 5 findings: correlation matrix, causality assessments, confounding factors
  - **Expected output:** Behaviour Correlation section with correlation findings
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Compile Quality Assessment section
  - **Primary method:** Aggregate Task 6 findings: task quality scores, step atomicity, critical flag appropriateness
  - **Expected output:** Quality Assessment section with quality distributions
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Compile Error Analysis section
  - **Primary method:** Aggregate Task 7 findings: error categories, root causes, recovery effectiveness, preventability
  - **Expected output:** Error Analysis section with error breakdown and patterns
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Generate actionable recommendations
  - **Primary method:** Based on all findings, create specific recommendations for: goal formulation improvement, SPEC design enhancement, execution optimisation, constitutional compliance, error prevention, efficiency improvements
  - **Backup [1]:** Use evidence-based recommendation framework: identify issue, link to finding, propose specific action, justify with data
  - **Expected output:** Minimum 8 specific, actionable recommendations linked to findings with priority levels
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Add cross-project comparison framework (if applicable)
  - **Primary method:** If analysing multiple SPECs, create comparison tables for key metrics across projects
  - **Expected output:** Cross-project comparison section (optional, only if multiple projects analysed)
  - **Critical:** false
  - **Mode:** silent

- **Step [12]:** Finalise report formatting and references
  - **Primary method:** Ensure all sections formatted consistently, add table of contents, verify all data citations present
  - **Expected output:** Complete, polished analysis report in markdown format
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Report contains all required sections, metrics are evidence-based, recommendations are actionable
- **Logging:** Record report completion in progress_Dev_Analysis.json with final deliverable path

---

## Bridging: Markdown ↔ TOML Synchronisation

This spec file (Dev_Analysis_SPEC.md) must maintain perfect alignment with its companion file (parameters_Dev_Analysis.toml).

**Bridging Requirements:**
1. Each task in this file must have corresponding `[[tasks]]` entry in TOML with matching ID (1-8)
2. Each step within a task must have corresponding `[[tasks.steps]]` entry with matching ID
3. Expected outputs in this file must match `expected_output` fields in TOML
4. Critical flags must be synchronised between files
5. Constraints referenced must exist in TOML `[constraints]` section

**Example Cross-References:**
- "See `constraints.min_examples_required` in parameters_Dev_Analysis.toml" (Task 2, Step 4)
- "As defined in `tasks[id=4]` in TOML" (Task 4 reference)
- "Must satisfy TOML verification requirements" (All task verifications)

The exe_Dev_Analysis.md controller will validate this synchronisation during initialisation (Section 1.8).

---

## Instructions for LLM Executor

### Execution Mode: FULLY AUTONOMOUS (SILENT)

This SPEC requires **ONLY ONE USER INPUT**: The project development folder path at Task 0, Step 0. After receiving the folder location, execute ALL remaining steps autonomously in silent mode.

### Execution Guidelines:

1. **Start with folder location**: Prompt user for project folder path (Task 0, Step 0), then proceed autonomously
2. **Be thorough and meticulous**: This is a comprehensive analysis - gather ALL available data
3. **Execute tasks sequentially**: Task 0 (metadata), Tasks 1-2 (data gathering), Tasks 3-7 (analysis), Task 8 (synthesis)
4. **Maintain objectivity**: Base all findings on evidence from files, logs, and artefacts - no speculation
5. **Track propagation carefully**: Pay special attention to how exact goal language appears throughout project
6. **Quantify everything**: Use numerical metrics rather than subjective assessments whenever possible
7. **Count meticulously**: Track steps taken, files processed, errors encountered, tokens consumed
8. **Distinguish correlation from causation**: Note relationships but assess causality using evidence-based frameworks
9. **Document thoroughly**: Log all findings in progress_Dev_Analysis.json for complete traceability
10. **Focus on actionability**: All recommendations must be specific, implementable, and linked to findings
11. **Read prior outcomes**: Before each step, check progress.json for relevant prior findings and context
12. **Never escalate**: Remain in silent mode throughout - use backup methods if primary fails
13. **Extract all metrics**: File counts, token counts, timestamps, error counts, step counts, time durations
14. **Parse all logs**: Progress logs, error logs, chat logs, validation reports - extract structured data
15. **Create comprehensive report**: Ensure final report includes all sections with complete data

### Data Gathering Priorities:

- **Completeness**: Gather all available data, don't skip sources
- **Accuracy**: Verify counts and calculations
- **Structure**: Organize data in tables, matrices, and structured formats
- **Traceability**: Cite source files and line numbers for all findings
- **Context**: Include timestamps, file paths, and surrounding context

---

## Expected Analysis Output Structure

The final report should follow this structure:

```markdown
# SPEC Development Analysis Report

## Executive Summary
[200-300 word overview of key findings]

## 0. Project Metadata Overview
### 0.1 Project Structure
- Total files by type
- Total project size
- File tree summary

### 0.2 Development Timeline
- Total development duration
- Development phases
- Key timestamps

### 0.3 Token Metrics
- Total tokens across all files
- Token distribution by file type
- Estimated LLM token usage

### 0.4 File Inventory
- SPEC files identified
- Error logs found
- Chat/conversation logs
- Other key artefacts

### 0.5 Conversation Metrics
- Total messages/turns
- User vs agent message counts
- Conversation duration

## 1. Goal Text Analysis
### 1.1 Initial Goal Characteristics
- Quantitative metrics table
- Complexity classification
- Element breakdown

### 1.2 Technical Specificity Assessment
- Specificity score with justification
- Domain terminology analysis

## 2. Goal Text Propagation Analysis
### 2.1 Propagation Through Tasks
- Task-level language mapping
- Specific examples with quotes

### 2.2 Propagation Through Steps
- Step-level language mapping
- Propagation matrix

### 2.3 Agent Thinking Patterns
- Minimum 3 examples of goal text in reasoning
- Direct quotes from logs/chat

### 2.4 Conceptual Drift Assessment
- Identified divergences
- Impact analysis

## 3. Constitutional Compliance Assessment
### 3.1 Article-by-Article Scores
- Individual article compliance
- Evidence for each assessment

### 3.2 Overall Compliance Score
- Aggregate score (0-100)
- Violation summary

## 4. Execution Performance Metrics
### 4.1 Step Count Analysis
- Total steps: defined, attempted, completed, skipped, failed
- Step distribution by status

### 4.2 Success and Failure Rates
- Overall success/failure rates
- Success rates by task
- First-attempt vs eventual success rates
- Multi-level metrics (step, task, SPEC)

### 4.3 Backup Method Usage
- Primary vs backup usage distribution
- Success rates per method type
- Backup effectiveness scores
- Usage frequency patterns

### 4.4 Mode Usage and Escalations
- Silent vs collaborative mode distribution
- Mode switches count
- Escalation triggers breakdown
- Escalation appropriateness

### 4.5 Time Metrics
- Time per step (min, max, average, median)
- Time per task
- Total execution time
- Time distribution analysis
- Longest/shortest steps

### 4.6 Error Propagation
- Dependency tracking
- Propagation decision counts
- Propagation effectiveness score
- Example instances

### 4.7 Retry Patterns
- Average retries per step
- Max retries reached
- Retry exhaustion rate
- Retry success rate
- Thoroughness score

### 4.8 Efficiency and Productivity
- Steps attempted vs planned
- Steps per hour
- Rework rate
- Productivity score

### 4.9 Critical vs Non-Critical Performance
- Performance comparison by critical flag
- Success rate differences
- Time impact analysis

### 4.10 Expected vs Actual Outputs
- Output match rates
- Mismatch analysis
- Quality assessment

### 4.11 Error Frequency
- Total errors by category
- Top 10 most common errors
- Error concentration

### 4.12 Token Usage (if available)
- Tokens per step/task
- Total token consumption
- Token efficiency metrics

## 5. Behaviour Correlation Analysis
### 5.1 Identified Correlations
- Goal characteristics vs execution behaviour
- Correlation strength assessment

### 5.2 Causality Assessment
- Causal vs correlational relationships
- Confidence levels

### 5.3 Confounding Factors
- External influences
- Mediation effects

## 6. Quality Assessment
### 6.1 Task Decomposition Quality
- Per-task quality scores
- Decomposition effectiveness

### 6.2 Step Quality Analysis
- Atomicity assessment
- Critical flag appropriateness

### 6.3 Method Selection Quality
- Primary/backup rationale
- Method effectiveness

## 7. Comprehensive Error Analysis
### 7.1 Error Source Inventory
- All error sources identified
- Error counts by source
- Source file references

### 7.2 Total Error Counts
- Total errors across all sources
- Errors per task
- Errors per step
- Error density (per 100 steps)

### 7.3 Error Categorisation Matrix
- Error types: validation, execution, resource, logic, syntax, semantic
- Error severity: critical, major, minor, warning
- Type-severity distribution

### 7.4 Error Log File Analysis
- Detailed analysis per log file
- Error timestamps
- Stack traces and context
- Frequency distributions

### 7.5 Error Frequency Patterns and Hotspots
- High-error tasks
- High-error steps
- Error clustering patterns
- Temporal error distribution
- Error concentration analysis

### 7.6 Root Cause Analysis
- Root cause mapping by category
- SPEC design flaws
- Step definition ambiguities
- Resource limitations
- Goal ambiguity impacts
- External dependencies
- Prevention recommendations per cause

### 7.7 Error Propagation Chains
- Cascading error patterns
- Downstream failure analysis
- Propagation chain diagrams

### 7.8 Recovery Effectiveness
- Recovery rate
- Average attempts to recovery
- Average time to recovery
- Escalation rate
- Recovery method distribution

### 7.9 Error Message Quality
- Clarity assessment
- Actionability assessment
- Completeness assessment
- Examples of good/poor messages

### 7.10 Constitutional Violations
- Violation breakdown by article
- Severity levels
- Correlation to errors

### 7.11 Error Preventability Classification
- Preventable vs inherent errors
- Percentages by category
- Improvement focus areas

### 7.12 Error-Related Time Costs
- Time lost to errors
- Percentage of total time
- Cost per error category

### 7.13 Error Patterns by Goal Characteristics
- Correlation between errors and goal complexity
- Error patterns by goal clarity
- Goal specificity impact on errors

## 8. Recommendations
### 8.1 Goal Formulation Improvements
[Specific, actionable recommendations]

### 8.2 SPEC Design Enhancements
[Specific, actionable recommendations]

### 8.3 Execution Optimisation
[Specific, actionable recommendations]

### 8.4 Constitutional Compliance
[Specific, actionable recommendations]

### 8.5 Future Research Directions
[Areas for deeper investigation]

## Appendices
### A. Raw Data Tables
### B. Propagation Examples (Full Quotes)
### C. Metrics Calculation Methods
### D. Source Citations
```

---

**End of Dev_Analysis_SPEC.md**

This SPEC is designed to be reusable across multiple test SPEC analyses, enabling systematic comparison and pattern identification.


```

```markdown
# Dev Analysis SPEC

**Version:** 1.0  
**Last Updated:** 2025-11-03  
**Purpose:** Analyse development of test SPECs to identify patterns, metrics, and goal text propagation effects

---

## Goal

Perform comprehensive analysis of a test SPEC's development lifecycle to identify how initial goal text propagates through the system and impacts agent behaviour, execution accuracy, and project outcomes.

---

## Software Stack & Architecture

**Not Applicable** - This is an analysis task, not a build goal.

---

## Definition of Complete

What must exist and be verified:
- [ ] **Primary deliverable:** Comprehensive analysis report (markdown format) covering all analysis areas
- [ ] **Quality standards met:** 
  - All 8 analysis tasks completed with documented findings
  - Goal text propagation patterns identified with specific examples
  - Quantitative metrics calculated for execution performance
  - Cross-correlation analysis between goal characteristics and outcomes
  - Recommendations provided based on findings
- [ ] **Verification method:** 
  - Report contains all required sections (see tasks below)
  - Quantitative metrics include numerical values with source citations
  - At least 3 specific examples of goal text propagation documented
  - Recommendations are actionable and linked to specific findings

---

## Definitions

- **goal**: Analyse how initial goal text characteristics influence SPEC development and execution
- **task[n]**: Discrete analysis objectives examining different aspects of SPEC development
- **step[m]**: Concrete analytical actions within each task
- **backup[p]**: Alternative analysis methods when primary approach is blocked
- **critical_flag**: Boolean indicating whether analysis step is essential to overall goal
- **mode**: `silent` (fully autonomous - NO USER INPUT REQUIRED except initial project folder location)
- **progress.json**: Structured log tracking analysis execution and findings
- **project_folder**: Target development project folder path (ONLY required user input)

---

## Components

Analysis requires access to:
- **Test SPEC files:** spec_[descriptor].md, parameters_[descriptor].toml, exe_[descriptor].md
- **Execution logs:** progress_[descriptor].json
- **Project artefacts:** Code files, documentation, error logs, validation reports
- **Chat history:** Conversation transcripts showing agent thinking and decision-making
- **Constitution:** __SPEC_Engine/_Constitution/constitution.md for compliance checking

**Machine-Readable Components:**  
See `[components]` section in parameters_Dev_Analysis.toml

---

## Constraints

- Analysis must be objective and evidence-based
- All metrics must be traceable to source data
- Goal text propagation analysis must include minimum 3 concrete examples
- Quantitative metrics must include: success rates, error rates, mode escalations, backup usage
- Findings must distinguish correlation from causation
- Recommendations must be specific and actionable

**Machine-Readable Constraints:**  
See `[constraints]` section in parameters_Dev_Analysis.toml:
- `min_examples_required = 3` (goal text propagation examples)
- `metrics_evidence_based = true` (all metrics must cite sources)
- `recommendation_specificity = "actionable"` (recommendations must be implementable)

---

## User Stories

- As a **SPEC developer**, I want to understand how goal phrasing impacts development so I can write more effective goals
- As a **system architect**, I want to identify patterns in SPEC execution so I can improve the framework
- As a **researcher**, I want to quantify goal text propagation so I can understand agent behaviour correlation
- As a **project manager**, I want metrics on SPEC performance so I can assess project quality

---

## Analysis Framework

This SPEC analyses development across 8 integrated dimensions:

### Dimension 1: Goal Text Characteristics
- Length (word count, character count, sentence complexity)
- Number of distinct elements/requirements
- Literacy level (Flesch-Kincaid, technical density)
- Formatting (structure, lists, emphasis)
- Familiarity/Technical specificity

### Dimension 2: Goal Text Propagation
- How goal language appears in task descriptions
- Goal terminology in step definitions
- Phrasing patterns in agent thinking/reasoning
- Language consistency across SPEC artefacts
- Conceptual drift from goal to implementation

### Dimension 3: Constitutional Compliance
- Article I-XIV adherence scoring
- Critical flag balance (target: 40-60%)
- Backup method quality assessment
- Bridging quality (Markdown-TOML sync)
- Validation checkpoint outcomes

### Dimension 4: Execution Performance
- Step success/failure rates
- Backup invocation frequency
- Mode escalation patterns
- Error propagation effectiveness
- Retry patterns and exhaustion

### Dimension 5: Agent Behaviour Correlation
- Thinking patterns vs goal complexity
- Decision quality vs goal clarity
- Output quality vs goal specificity
- Backup selection vs goal ambiguity
- Escalation triggers vs goal characteristics

### Dimension 6: Per-Task/Step Behaviour
- Task decomposition quality
- Step atomicity assessment
- Critical flag appropriateness
- Expected output clarity
- Method selection rationale

### Dimension 7: Error Analysis
- Error types and frequencies
- Root cause patterns
- Recovery effectiveness
- Constitutional violations
- Preventable vs inherent errors

### Dimension 8: Outcome Metrics
- Goal achievement status (ACHIEVED/PARTIAL/NOT_ACHIEVED)
- Deliverable completeness
- Quality standards met
- Time/step efficiency
- Comparison to expected outcomes

---

## Task [0]: Initialize Analysis and Gather Project Metadata

**TOML Reference:** `tasks[id=0]` in parameters_Dev_Analysis.toml  
**Purpose:** Locate project folder, scan structure, and collect comprehensive metadata

- **Step [0]:** Receive project folder location (ONLY USER INPUT REQUIRED)
  - **Primary method:** Prompt for project development folder path
  - **Expected output:** Absolute path to project folder
  - **Critical:** true
  - **Mode:** collaborative (ONE TIME ONLY - for folder path input)

- **Step [1]:** Scan and map complete project structure
  - **Primary method:** Recursively list all files and directories in project folder
  - **Backup [1]:** If permissions issue, request accessible subset of project
  - **Expected output:** Complete file tree with full paths
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count and categorise all files
  - **Primary method:** Count files by type: .md, .toml, .json, .py, .js, .ts, .log, .txt, etc.
  - **Expected output:** File count table with breakdown by extension
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Calculate file sizes and total project size
  - **Primary method:** Get file size for each file, sum by category and total
  - **Expected output:** Size metrics table (bytes, KB, MB) by file type and total
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Extract all timestamps
  - **Primary method:** Collect creation, modification, access times for all relevant files
  - **Backup [1]:** If timestamps unavailable, use git history if present
  - **Expected output:** Timeline table showing project chronology
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Calculate development duration
  - **Primary method:** Calculate time from earliest to latest timestamp, identify development phases
  - **Expected output:** Development duration metrics: total time, active development periods, gaps
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Count tokens across all text files
  - **Primary method:** For each text-based file, count tokens (words, characters, estimated LLM tokens)
  - **Backup [1]:** If token counting unavailable, use word/character counts as proxy
  - **Expected output:** Token count table by file type with totals
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Identify and catalogue error logs
  - **Primary method:** Locate all error log files, count error entries, categorise by severity
  - **Expected output:** Error log inventory with counts and locations
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Identify and catalogue chat/conversation logs
  - **Primary method:** Locate chat transcripts, conversation logs, agent thinking logs
  - **Backup [1]:** Check common locations: root, logs folder, subdirectories
  - **Expected output:** Conversation log inventory with file paths and sizes
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Count conversation turns and messages
  - **Primary method:** Parse chat logs to count: total messages, user messages, agent messages, turns
  - **Expected output:** Conversation metrics table
  - **Critical:** false
  - **Mode:** silent

- **Step [10]:** Identify SPEC files and versions
  - **Primary method:** Locate all spec_*.md, parameters_*.toml, exe_*.md, progress_*.json files
  - **Expected output:** SPEC file inventory with versions and timestamps
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Create project metadata snapshot
  - **Primary method:** Aggregate all collected metrics into comprehensive metadata document
  - **Expected output:** Project metadata JSON with all metrics organized
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Project folder scanned, all files catalogued, comprehensive metrics collected
- **Logging:** Record all metadata in progress_Dev_Analysis.json for reference throughout analysis

---

## Task [1]: Extract and Characterise Initial Goal Text

**TOML Reference:** `tasks[id=1]` in parameters_Dev_Analysis.toml  
**Purpose:** Establish baseline characteristics of the goal that initiated SPEC development

- **Step [1]:** Locate and extract initial goal text
  - **Primary method:** Read SPEC markdown file Goal section and chat history for original user goal statement
  - **Backup [1]:** If chat history unavailable, use goal section from spec_[descriptor].md as proxy
  - **Expected output:** Exact goal text with source citation and timestamp
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Calculate quantitative text characteristics
  - **Primary method:** Compute word count, character count, sentence count, avg sentence length, Flesch-Kincaid score
  - **Backup [1]:** If automated scoring unavailable, perform manual classification (simple/moderate/complex)
  - **Expected output:** Table with numerical metrics and complexity classification
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Identify distinct elements and requirements
  - **Primary method:** Parse goal for discrete requirements, constraints, deliverables, success criteria
  - **Backup [1]:** Use linguistic chunking to identify conceptual units if structure unclear
  - **Expected output:** Numbered list of distinct elements (target: 3-10 elements)
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess technical specificity and domain familiarity
  - **Primary method:** Identify technical terms, domain-specific language, assumed knowledge, explicit vs implicit requirements
  - **Backup [1]:** Compare vocabulary against common vs specialised term databases
  - **Expected output:** Technical specificity score (1-5 scale) with justification and term examples
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Analyse formatting and structure
  - **Primary method:** Document use of lists, emphasis, sections, explicit vs narrative format
  - **Expected output:** Formatting assessment noting structural elements present
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All goal characteristics documented with quantitative metrics where possible
- **Logging:** Record all measurements in progress_Dev_Analysis.json for correlation analysis

---

## Task [2]: Map Goal Text Propagation Throughout Project

**TOML Reference:** `tasks[id=2]` in parameters_Dev_Analysis.toml  
**Purpose:** Track how initial goal language and concepts propagate through SPEC artefacts

- **Step [1]:** Extract task descriptions from SPEC
  - **Primary method:** Parse spec_[descriptor].md for all task titles and descriptions
  - **Expected output:** List of tasks with full text
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Identify goal language in task descriptions
  - **Primary method:** Compare task descriptions to goal text, noting shared terminology, conceptual overlap, verbatim phrases
  - **Backup [1]:** Use semantic similarity scoring if direct comparison insufficient
  - **Expected output:** Table mapping goal terms to task descriptions with similarity scores
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Extract step definitions and analyse propagation
  - **Primary method:** Parse all step descriptions, identify goal/task terminology presence, track conceptual consistency
  - **Backup [1]:** Focus on critical steps only if volume is high (>20 steps)
  - **Expected output:** Propagation matrix showing goal→task→step language flow with specific examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse agent thinking and reasoning patterns
  - **Primary method:** Review chat history/logs for agent internal reasoning, note how goal concepts appear in thinking
  - **Backup [1]:** If full chat unavailable, analyse progress.json logs for method justifications
  - **Expected output:** Minimum 3 specific examples of goal text influencing agent reasoning with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify conceptual drift
  - **Primary method:** Compare final implementation/outputs against original goal, identify divergences in terminology, scope, or interpretation
  - **Expected output:** Conceptual drift assessment noting where implementation departed from goal language
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Assess language consistency across artefacts
  - **Primary method:** Check terminology consistency across spec.md, parameters.toml, progress.json, deliverables
  - **Expected output:** Consistency report identifying where language fragmented or evolved
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Minimum 3 concrete examples of goal text propagation documented with direct quotes
- **Logging:** Record propagation patterns and drift instances in progress_Dev_Analysis.json

---

## Task [3]: Evaluate Constitutional Compliance

**TOML Reference:** `tasks[id=3]` in parameters_Dev_Analysis.toml  
**Purpose:** Assess adherence to SPEC Engine Constitution (Articles I-XIV)

- **Step [1]:** Validate Article I compliance (North Star Principle)
  - **Primary method:** Verify goal singularity, clarity, measurability, explicitness
  - **Expected output:** Article I compliance score (pass/fail) with justification
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Validate Article II compliance (Hierarchical Structure)
  - **Primary method:** Count tasks (target: 2-5), count steps per task (target: 1-5), verify hierarchy maintained
  - **Backup [1]:** If counts borderline, assess whether structure serves goal effectively
  - **Expected output:** Article II compliance score with quantitative counts
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Validate Article III compliance (Dual-File Mandate)
  - **Primary method:** Cross-check spec.md and parameters.toml for ID matching, structure sync, cross-references
  - **Expected output:** Article III compliance score noting any bridging failures
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Validate Article VI compliance (Critical Flag Discipline)
  - **Primary method:** Calculate critical step percentage (target: 40-60%), assess appropriateness of critical flags
  - **Expected output:** Critical balance percentage and appropriateness assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Validate Article VII compliance (Backup Methods)
  - **Primary method:** Review all backup methods to ensure they are alternative reasoning paths, not retries
  - **Backup [1]:** Sample backup methods if total exceeds 15
  - **Expected output:** Backup quality score with examples of good/poor backups
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Check Article XIV compliance (if build goal)
  - **Primary method:** If goal contains build/create/system keywords, verify software stack defined, deployment criteria present
  - **Expected output:** Article XIV compliance (N/A or pass/fail with details)
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Review Articles IV, VIII, IX, X compliance from execution
  - **Primary method:** Analyse progress.json for validation execution, error propagation, mode discipline, comprehensive logging
  - **Expected output:** Compliance scores for Articles IV, VIII, IX, X with evidence from logs
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Calculate overall constitutional compliance score
  - **Primary method:** Aggregate individual article scores, weight by severity, generate 0-100 score
  - **Expected output:** Overall compliance score (0-100) with breakdown by article
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All applicable articles assessed with evidence-based scoring
- **Logging:** Record compliance scores and violations in progress_Dev_Analysis.json

---

## Task [4]: Analyse Execution Performance Metrics

**TOML Reference:** `tasks[id=4]` in parameters_Dev_Analysis.toml  
**Purpose:** Extract quantitative performance data from execution logs with comprehensive detail

- **Step [1]:** Parse progress.json for complete step data
  - **Primary method:** Read progress_[descriptor].json, extract ALL fields: task_id, step_id, status, method_used, retry_count, timestamp, mode, critical_flag, expected_output, actual_output, error_messages
  - **Backup [1]:** If progress.json malformed, reconstruct from available logs
  - **Expected output:** Complete step outcome dataset with full detail per step
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count total steps taken
  - **Primary method:** Count: total steps defined, total steps attempted, total steps completed, total steps skipped, total steps failed
  - **Expected output:** Comprehensive step count table with breakdown by status
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Calculate detailed success and failure rates
  - **Primary method:** Compute: overall success rate, failure rate, success rate by task, failure rate by task, first-attempt success rate, eventual success rate (after retries)
  - **Expected output:** Multi-level success/failure metrics table with percentages at step, task, and SPEC levels
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse backup method usage patterns
  - **Primary method:** Count: primary method attempts, primary successes, backup[1] attempts, backup[1] successes, backup[2] attempts, backup[2] successes, calculate success rates per method type
  - **Expected output:** Comprehensive backup usage statistics with success rates, effectiveness scores, and usage frequency distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Track mode usage and escalations
  - **Primary method:** Count: steps in silent mode, steps in collaborative mode, mode switches, categorise escalation triggers (consecutive failures, backup depletion, critical failure, confidence degradation)
  - **Expected output:** Mode usage table, escalation count by trigger type, escalation appropriateness assessment per instance
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Analyse timestamps and time metrics
  - **Primary method:** Extract all timestamps from progress.json, calculate: time per step, time per task, total execution time, longest steps, shortest steps, time distribution
  - **Backup [1]:** If timestamps sparse, use available data and note gaps
  - **Expected output:** Comprehensive time metrics table with duration statistics
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Assess error propagation effectiveness
  - **Primary method:** Identify all steps with dependencies, check if prior failures were read from progress.json, assess propagation handling quality, count propagation decisions
  - **Backup [1]:** If error propagation tracking sparse, infer from step sequence and outcomes
  - **Expected output:** Error propagation effectiveness score with example instances and propagation decision breakdown
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Analyse retry patterns in detail
  - **Primary method:** Extract retry_count per step, calculate: average retries per step, max retries reached, retry exhaustion rate, retry success rate, thoroughness score (methods exhausted before escalation)
  - **Expected output:** Detailed retry pattern analysis with distribution charts and exhaustion assessment
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Calculate efficiency and productivity metrics
  - **Primary method:** Compute: total steps attempted vs planned, steps per task (actual vs expected), average time per step, steps per hour, rework rate (retries/total), productivity score
  - **Expected output:** Comprehensive efficiency metrics table with productivity indicators
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Analyse critical vs non-critical step performance
  - **Primary method:** Separate critical and non-critical steps, compare: success rates, retry rates, time per step, failure impact
  - **Expected output:** Critical flag performance comparison table
  - **Critical:** false
  - **Mode:** silent

- **Step [11]:** Extract and analyse expected vs actual outputs
  - **Primary method:** For each step, compare expected_output defined in SPEC to actual_output logged, categorise: exact match, partial match, mismatch, missing
  - **Expected output:** Output quality assessment with match rate and mismatch analysis
  - **Critical:** true
  - **Mode:** silent

- **Step [12]:** Count and categorise all errors encountered
  - **Primary method:** Extract all error messages from progress.json, categorise by type (validation, execution, resource, logic), count occurrences, identify most frequent errors
  - **Expected output:** Error frequency table by category with top 10 most common errors
  - **Critical:** true
  - **Mode:** silent

- **Step [13]:** Analyse token usage per step (if available)
  - **Primary method:** If token counts logged, extract tokens per step, calculate: tokens per task, total tokens, token efficiency (tokens per successful step)
  - **Backup [1]:** If not logged in progress.json, skip with note
  - **Expected output:** Token usage metrics table (if data available)
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All quantitative metrics calculated with source data citations, minimum 13 metric categories documented
- **Logging:** Record all performance metrics in progress_Dev_Analysis.json

---

## Task [5]: Correlate Agent Behaviour with Goal Characteristics

**TOML Reference:** `tasks[id=5]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify relationships between goal text properties and agent execution behaviour

- **Step [1]:** Establish correlation framework
  - **Primary method:** Define metrics for correlation: goal complexity vs task count, goal clarity vs error rate, goal specificity vs backup usage
  - **Expected output:** Correlation matrix framework listing goal characteristics and behaviour metrics
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Analyse goal complexity vs task decomposition
  - **Primary method:** Correlate goal complexity score (from Task 1) with number of tasks, steps per task, decomposition depth
  - **Backup [1]:** Use qualitative assessment if quantitative correlation weak
  - **Expected output:** Correlation finding: does complex goal lead to more/fewer tasks?
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Analyse goal clarity vs execution accuracy
  - **Primary method:** Correlate goal clarity indicators (explicit requirements, measurable criteria) with success rate, error rate
  - **Expected output:** Correlation finding: does clear goal reduce errors?
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse goal specificity vs backup usage
  - **Primary method:** Correlate technical specificity score with backup invocation rate, backup effectiveness
  - **Expected output:** Correlation finding: does vague goal increase backup reliance?
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Analyse goal formatting vs agent thinking patterns
  - **Primary method:** Review agent reasoning for structured vs narrative goals, assess thinking clarity and organisation
  - **Backup [1]:** If thinking logs sparse, assess output organisation as proxy
  - **Expected output:** Qualitative finding on formatting impact with examples
  - **Critical:** false
  - **Mode:** silent

- **Step [6]:** Identify confounding factors
  - **Primary method:** Check for external factors affecting correlation: SPEC complexity, domain difficulty, resource availability
  - **Expected output:** List of confounding factors that may explain behaviour patterns
  - **Critical:** false
  - **Mode:** silent

- **Step [7]:** Distinguish correlation from causation
  - **Primary method:** For each correlation found, assess whether relationship is causal, coincidental, or mediated by other factors using evidence-based analysis
  - **Backup [1]:** Apply Bradford Hill criteria for causation: strength, consistency, specificity, temporality, biological gradient
  - **Expected output:** Causality assessment for each correlation with confidence level and supporting evidence
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Minimum 3 behaviour correlations identified with specific evidence
- **Logging:** Record correlations and causality assessments in progress_Dev_Analysis.json

---

## Task [6]: Assess Per-Task and Per-Step Behaviour Quality

**TOML Reference:** `tasks[id=6]` in parameters_Dev_Analysis.toml  
**Purpose:** Evaluate quality of task decomposition and step execution at granular level

- **Step [1]:** Evaluate task decomposition quality
  - **Primary method:** For each task, assess: Does task serve goal? Is task scope appropriate? Is task self-contained?
  - **Expected output:** Task quality assessment table with scores and rationale per task
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Assess step atomicity
  - **Primary method:** For each step, assess: Is step a single concrete action? Is step scope too broad/narrow? Is step executable?
  - **Backup [1]:** Sample steps if total exceeds 20
  - **Expected output:** Step atomicity assessment with examples of well/poorly scoped steps
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Evaluate critical flag appropriateness
  - **Primary method:** For each critical step, verify: Would failure truly block goal? For non-critical, verify: Can goal succeed without this?
  - **Expected output:** Critical flag appropriateness score with misclassification examples
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Assess expected output clarity
  - **Primary method:** For each step, rate expected output: specific/vague, measurable/subjective, achievable/unrealistic
  - **Expected output:** Expected output quality assessment with clarity distribution
  - **Critical:** false
  - **Mode:** silent

- **Step [5]:** Evaluate method selection rationale
  - **Primary method:** For steps with multiple methods, assess whether primary/backup choices were well-justified
  - **Expected output:** Method selection quality score with examples
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All tasks and representative sample of steps assessed for quality
- **Logging:** Record quality assessments in progress_Dev_Analysis.json

---

## Task [7]: Conduct Comprehensive Error Analysis and Pattern Detection

**TOML Reference:** `tasks[id=7]` in parameters_Dev_Analysis.toml  
**Purpose:** Identify error patterns, root causes, and improvement opportunities through meticulous analysis

- **Step [1]:** Extract and inventory all error sources
  - **Primary method:** Collect errors from: progress.json, error log files (from Task 0), chat logs, validation reports, any other error documentation
  - **Expected output:** Complete error inventory with source file paths and line references
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Count total errors across all sources
  - **Primary method:** Count: total errors logged, errors per source type, errors per task, errors per step, error density (errors per 100 steps)
  - **Expected output:** Comprehensive error count table with breakdowns
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Categorise all errors by type and severity
  - **Primary method:** Classify each error by type (validation, execution, resource, logic, syntax, semantic) and severity (critical, major, minor, warning)
  - **Expected output:** Error categorisation matrix with counts and percentages by type and severity
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Analyse error log files in detail
  - **Primary method:** For each error log file identified in Task 0, parse contents, extract: error timestamps, error messages, stack traces, context, frequency
  - **Backup [1]:** If logs are unstructured, extract what's available and note format issues
  - **Expected output:** Detailed error log analysis with structured data extracted from logs
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Identify error frequency patterns and hotspots
  - **Primary method:** Analyse which tasks/steps had highest error rates, identify repeated failures, calculate error concentration by task/step/time period
  - **Expected output:** Error hotspot analysis showing: high-error tasks, high-error steps, error clustering patterns, temporal error distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Conduct comprehensive root cause analysis
  - **Primary method:** For each error category, trace to root cause: SPEC design flaw, step definition ambiguity, resource limitation, goal ambiguity, external dependency, constitutional violation, tooling issue
  - **Backup [1]:** Apply 5 Whys methodology for complex errors
  - **Expected output:** Root cause mapping for all error categories with prevention recommendations per cause
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Analyse error propagation chains
  - **Primary method:** Trace errors that caused downstream failures, identify cascading error patterns, assess propagation handling
  - **Expected output:** Error propagation chain diagram with cascade analysis
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Assess recovery effectiveness and time
  - **Primary method:** For each error, determine: was it recovered? which method succeeded? how many attempts? time to recovery? was escalation needed?
  - **Expected output:** Recovery effectiveness metrics: recovery rate, average attempts to recovery, average time to recovery, escalation rate, recovery method distribution
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Analyse error messages for clarity and actionability
  - **Primary method:** Review all error messages, rate: clarity (clear/vague), actionability (specific guidance/generic), completeness (context provided/missing)
  - **Expected output:** Error message quality assessment with examples of good/poor messages
  - **Critical:** false
  - **Mode:** silent

- **Step [10]:** Identify constitutional violations
  - **Primary method:** Check progress.json constitutional_compliance section, extract violations; cross-reference error patterns with constitutional articles
  - **Backup [1]:** Manual review of execution logs if compliance tracking absent
  - **Expected output:** Constitutional violation summary with article breakdown, severity, and correlation to errors
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Distinguish preventable from inherent errors
  - **Primary method:** Classify each error: preventable through better SPEC design, preventable through better execution, inherent to task complexity, external/environmental, resource-based
  - **Expected output:** Error preventability classification with percentages and improvement focus areas
  - **Critical:** true
  - **Mode:** silent

- **Step [12]:** Calculate error-related time costs
  - **Primary method:** Sum time spent on: failed steps, retries, error recovery, escalations, rework
  - **Backup [1]:** Estimate if precise timestamps unavailable
  - **Expected output:** Error cost metrics: time lost to errors, percentage of total time, cost per error category
  - **Critical:** false
  - **Mode:** silent

- **Step [13]:** Identify error patterns by goal characteristics
  - **Primary method:** Correlate error rates/types with goal complexity, clarity, specificity metrics from Task 1
  - **Expected output:** Error pattern correlation analysis linking errors to goal characteristics
  - **Critical:** false
  - **Mode:** silent

- **Verification:** All errors from all sources analysed with root causes, minimum 13 error metric categories documented
- **Logging:** Record comprehensive error analysis findings in progress_Dev_Analysis.json

---

## Task [8]: Generate Comprehensive Analysis Report with Recommendations

**TOML Reference:** `tasks[id=8]` in parameters_Dev_Analysis.toml  
**Purpose:** Synthesise all findings into actionable report

- **Step [1]:** Structure report outline
  - **Primary method:** Create report sections: Executive Summary, Goal Analysis, Propagation Findings, Performance Metrics, Correlations, Quality Assessment, Error Analysis, Recommendations
  - **Expected output:** Report outline with section headers
  - **Critical:** true
  - **Mode:** silent

- **Step [2]:** Write Executive Summary
  - **Primary method:** Synthesise key findings: goal characteristics summary, main propagation patterns, overall performance, critical insights
  - **Expected output:** 200-300 word executive summary highlighting main findings
  - **Critical:** true
  - **Mode:** silent

- **Step [3]:** Compile Goal Text Analysis section
  - **Primary method:** Aggregate Task 1 findings: goal characteristics table, complexity assessment, element breakdown
  - **Expected output:** Goal Text Analysis section with all metrics and assessments
  - **Critical:** true
  - **Mode:** silent

- **Step [4]:** Compile Goal Text Propagation section
  - **Primary method:** Aggregate Task 2 findings: propagation examples, language flow diagram, conceptual drift assessment
  - **Expected output:** Goal Text Propagation section with minimum 3 concrete examples with quotes
  - **Critical:** true
  - **Mode:** silent

- **Step [5]:** Compile Constitutional Compliance section
  - **Primary method:** Aggregate Task 3 findings: article-by-article scores, overall compliance score, violation summary
  - **Expected output:** Constitutional Compliance section with compliance scorecard
  - **Critical:** true
  - **Mode:** silent

- **Step [6]:** Compile Execution Performance section
  - **Primary method:** Aggregate Task 4 findings: success/failure rates, backup usage, mode escalations, efficiency metrics
  - **Expected output:** Execution Performance section with metrics tables
  - **Critical:** true
  - **Mode:** silent

- **Step [7]:** Compile Behaviour Correlation section
  - **Primary method:** Aggregate Task 5 findings: correlation matrix, causality assessments, confounding factors
  - **Expected output:** Behaviour Correlation section with correlation findings
  - **Critical:** true
  - **Mode:** silent

- **Step [8]:** Compile Quality Assessment section
  - **Primary method:** Aggregate Task 6 findings: task quality scores, step atomicity, critical flag appropriateness
  - **Expected output:** Quality Assessment section with quality distributions
  - **Critical:** true
  - **Mode:** silent

- **Step [9]:** Compile Error Analysis section
  - **Primary method:** Aggregate Task 7 findings: error categories, root causes, recovery effectiveness, preventability
  - **Expected output:** Error Analysis section with error breakdown and patterns
  - **Critical:** true
  - **Mode:** silent

- **Step [10]:** Generate actionable recommendations
  - **Primary method:** Based on all findings, create specific recommendations for: goal formulation improvement, SPEC design enhancement, execution optimisation, constitutional compliance, error prevention, efficiency improvements
  - **Backup [1]:** Use evidence-based recommendation framework: identify issue, link to finding, propose specific action, justify with data
  - **Expected output:** Minimum 8 specific, actionable recommendations linked to findings with priority levels
  - **Critical:** true
  - **Mode:** silent

- **Step [11]:** Add cross-project comparison framework (if applicable)
  - **Primary method:** If analysing multiple SPECs, create comparison tables for key metrics across projects
  - **Expected output:** Cross-project comparison section (optional, only if multiple projects analysed)
  - **Critical:** false
  - **Mode:** silent

- **Step [12]:** Finalise report formatting and references
  - **Primary method:** Ensure all sections formatted consistently, add table of contents, verify all data citations present
  - **Expected output:** Complete, polished analysis report in markdown format
  - **Critical:** false
  - **Mode:** silent

- **Verification:** Report contains all required sections, metrics are evidence-based, recommendations are actionable
- **Logging:** Record report completion in progress_Dev_Analysis.json with final deliverable path

---

## Bridging: Markdown ↔ TOML Synchronisation

This spec file (Dev_Analysis_SPEC.md) must maintain perfect alignment with its companion file (parameters_Dev_Analysis.toml).

**Bridging Requirements:**
1. Each task in this file must have corresponding `[[tasks]]` entry in TOML with matching ID (1-8)
2. Each step within a task must have corresponding `[[tasks.steps]]` entry with matching ID
3. Expected outputs in this file must match `expected_output` fields in TOML
4. Critical flags must be synchronised between files
5. Constraints referenced must exist in TOML `[constraints]` section

**Example Cross-References:**
- "See `constraints.min_examples_required` in parameters_Dev_Analysis.toml" (Task 2, Step 4)
- "As defined in `tasks[id=4]` in TOML" (Task 4 reference)
- "Must satisfy TOML verification requirements" (All task verifications)

The exe_Dev_Analysis.md controller will validate this synchronisation during initialisation (Section 1.8).

---

## Instructions for LLM Executor

### Execution Mode: FULLY AUTONOMOUS (SILENT)

This SPEC requires **ONLY ONE USER INPUT**: The project development folder path at Task 0, Step 0. After receiving the folder location, execute ALL remaining steps autonomously in silent mode.

### Execution Guidelines:

1. **Start with folder location**: Prompt user for project folder path (Task 0, Step 0), then proceed autonomously
2. **Be thorough and meticulous**: This is a comprehensive analysis - gather ALL available data
3. **Execute tasks sequentially**: Task 0 (metadata), Tasks 1-2 (data gathering), Tasks 3-7 (analysis), Task 8 (synthesis)
4. **Maintain objectivity**: Base all findings on evidence from files, logs, and artefacts - no speculation
5. **Track propagation carefully**: Pay special attention to how exact goal language appears throughout project
6. **Quantify everything**: Use numerical metrics rather than subjective assessments whenever possible
7. **Count meticulously**: Track steps taken, files processed, errors encountered, tokens consumed
8. **Distinguish correlation from causation**: Note relationships but assess causality using evidence-based frameworks
9. **Document thoroughly**: Log all findings in progress_Dev_Analysis.json for complete traceability
10. **Focus on actionability**: All recommendations must be specific, implementable, and linked to findings
11. **Read prior outcomes**: Before each step, check progress.json for relevant prior findings and context
12. **Never escalate**: Remain in silent mode throughout - use backup methods if primary fails
13. **Extract all metrics**: File counts, token counts, timestamps, error counts, step counts, time durations
14. **Parse all logs**: Progress logs, error logs, chat logs, validation reports - extract structured data
15. **Create comprehensive report**: Ensure final report includes all sections with complete data

### Data Gathering Priorities:

- **Completeness**: Gather all available data, don't skip sources
- **Accuracy**: Verify counts and calculations
- **Structure**: Organize data in tables, matrices, and structured formats
- **Traceability**: Cite source files and line numbers for all findings
- **Context**: Include timestamps, file paths, and surrounding context

---

## Expected Analysis Output Structure

The final report should follow this structure:

```markdown
# SPEC Development Analysis Report

## Executive Summary
[200-300 word overview of key findings]

## 0. Project Metadata Overview
### 0.1 Project Structure
- Total files by type
- Total project size
- File tree summary

### 0.2 Development Timeline
- Total development duration
- Development phases
- Key timestamps

### 0.3 Token Metrics
- Total tokens across all files
- Token distribution by file type
- Estimated LLM token usage

### 0.4 File Inventory
- SPEC files identified
- Error logs found
- Chat/conversation logs
- Other key artefacts

### 0.5 Conversation Metrics
- Total messages/turns
- User vs agent message counts
- Conversation duration

## 1. Goal Text Analysis
### 1.1 Initial Goal Characteristics
- Quantitative metrics table
- Complexity classification
- Element breakdown

### 1.2 Technical Specificity Assessment
- Specificity score with justification
- Domain terminology analysis

## 2. Goal Text Propagation Analysis
### 2.1 Propagation Through Tasks
- Task-level language mapping
- Specific examples with quotes

### 2.2 Propagation Through Steps
- Step-level language mapping
- Propagation matrix

### 2.3 Agent Thinking Patterns
- Minimum 3 examples of goal text in reasoning
- Direct quotes from logs/chat

### 2.4 Conceptual Drift Assessment
- Identified divergences
- Impact analysis

## 3. Constitutional Compliance Assessment
### 3.1 Article-by-Article Scores
- Individual article compliance
- Evidence for each assessment

### 3.2 Overall Compliance Score
- Aggregate score (0-100)
- Violation summary

## 4. Execution Performance Metrics
### 4.1 Step Count Analysis
- Total steps: defined, attempted, completed, skipped, failed
- Step distribution by status

### 4.2 Success and Failure Rates
- Overall success/failure rates
- Success rates by task
- First-attempt vs eventual success rates
- Multi-level metrics (step, task, SPEC)

### 4.3 Backup Method Usage
- Primary vs backup usage distribution
- Success rates per method type
- Backup effectiveness scores
- Usage frequency patterns

### 4.4 Mode Usage and Escalations
- Silent vs collaborative mode distribution
- Mode switches count
- Escalation triggers breakdown
- Escalation appropriateness

### 4.5 Time Metrics
- Time per step (min, max, average, median)
- Time per task
- Total execution time
- Time distribution analysis
- Longest/shortest steps

### 4.6 Error Propagation
- Dependency tracking
- Propagation decision counts
- Propagation effectiveness score
- Example instances

### 4.7 Retry Patterns
- Average retries per step
- Max retries reached
- Retry exhaustion rate
- Retry success rate
- Thoroughness score

### 4.8 Efficiency and Productivity
- Steps attempted vs planned
- Steps per hour
- Rework rate
- Productivity score

### 4.9 Critical vs Non-Critical Performance
- Performance comparison by critical flag
- Success rate differences
- Time impact analysis

### 4.10 Expected vs Actual Outputs
- Output match rates
- Mismatch analysis
- Quality assessment

### 4.11 Error Frequency
- Total errors by category
- Top 10 most common errors
- Error concentration

### 4.12 Token Usage (if available)
- Tokens per step/task
- Total token consumption
- Token efficiency metrics

## 5. Behaviour Correlation Analysis
### 5.1 Identified Correlations
- Goal characteristics vs execution behaviour
- Correlation strength assessment

### 5.2 Causality Assessment
- Causal vs correlational relationships
- Confidence levels

### 5.3 Confounding Factors
- External influences
- Mediation effects

## 6. Quality Assessment
### 6.1 Task Decomposition Quality
- Per-task quality scores
- Decomposition effectiveness

### 6.2 Step Quality Analysis
- Atomicity assessment
- Critical flag appropriateness

### 6.3 Method Selection Quality
- Primary/backup rationale
- Method effectiveness

## 7. Comprehensive Error Analysis
### 7.1 Error Source Inventory
- All error sources identified
- Error counts by source
- Source file references

### 7.2 Total Error Counts
- Total errors across all sources
- Errors per task
- Errors per step
- Error density (per 100 steps)

### 7.3 Error Categorisation Matrix
- Error types: validation, execution, resource, logic, syntax, semantic
- Error severity: critical, major, minor, warning
- Type-severity distribution

### 7.4 Error Log File Analysis
- Detailed analysis per log file
- Error timestamps
- Stack traces and context
- Frequency distributions

### 7.5 Error Frequency Patterns and Hotspots
- High-error tasks
- High-error steps
- Error clustering patterns
- Temporal error distribution
- Error concentration analysis

### 7.6 Root Cause Analysis
- Root cause mapping by category
- SPEC design flaws
- Step definition ambiguities
- Resource limitations
- Goal ambiguity impacts
- External dependencies
- Prevention recommendations per cause

### 7.7 Error Propagation Chains
- Cascading error patterns
- Downstream failure analysis
- Propagation chain diagrams

### 7.8 Recovery Effectiveness
- Recovery rate
- Average attempts to recovery
- Average time to recovery
- Escalation rate
- Recovery method distribution

### 7.9 Error Message Quality
- Clarity assessment
- Actionability assessment
- Completeness assessment
- Examples of good/poor messages

### 7.10 Constitutional Violations
- Violation breakdown by article
- Severity levels
- Correlation to errors

### 7.11 Error Preventability Classification
- Preventable vs inherent errors
- Percentages by category
- Improvement focus areas

### 7.12 Error-Related Time Costs
- Time lost to errors
- Percentage of total time
- Cost per error category

### 7.13 Error Patterns by Goal Characteristics
- Correlation between errors and goal complexity
- Error patterns by goal clarity
- Goal specificity impact on errors

## 8. Recommendations
### 8.1 Goal Formulation Improvements
[Specific, actionable recommendations]

### 8.2 SPEC Design Enhancements
[Specific, actionable recommendations]

### 8.3 Execution Optimisation
[Specific, actionable recommendations]

### 8.4 Constitutional Compliance
[Specific, actionable recommendations]

### 8.5 Future Research Directions
[Areas for deeper investigation]

## Appendices
### A. Complete Raw Data Tables
#### A.1 Project Metadata
- Complete file tree
- File count by extension (detailed)
- File sizes (all files)
- All timestamps (creation, modification)

#### A.2 Token Counts
- Token counts per file
- Character/word counts per file
- Estimated LLM tokens

#### A.3 Conversation Data
- Message-by-message breakdown
- Turn-by-turn analysis
- Timestamp sequence

#### A.4 Step Execution Data
- Complete step-by-step log
- All timestamps
- All method attempts
- All outcomes

#### A.5 Error Data
- All error messages (full text)
- All stack traces
- Error log file contents (parsed)
- Error frequency tables (complete)

### B. Goal Text Propagation Examples (Full Quotes)
- Minimum 3 detailed examples with:
  - Original goal text
  - Corresponding task/step text
  - Agent thinking quotes
  - Propagation path visualization

### C. Metrics Calculation Methods
- Formulas used for all calculated metrics
- Estimation methods (where exact data unavailable)
- Statistical methods applied
- Assumptions documented

### D. Source Citations
- Complete file paths for all data sources
- Line number references for quotes
- Timestamp references for events
- Cross-reference index

### E. Visual Data Representations
- Distribution charts (text descriptions if unable to generate images)
- Timeline visualizations
- Correlation matrices
- Error hotspot maps

### F. Complete Constitutional Compliance Scorecard
- Article-by-article detailed assessment
- All violations listed with context
- All compliance passes noted
- Evidence for each judgement
```

---

**End of Dev_Analysis_SPEC.md**

This SPEC is designed to be reusable across multiple test SPEC analyses, enabling systematic comparison and pattern identification.


```

Perfect! I've successfully updated the **Dev_Analysis_SPEC.md** to be comprehensive, meticulous, and fully autonomous. Here's what's now included:

## Key Updates:

### 1. **Fully Autonomous Execution** (Silent Mode)
   - **ONLY user input required**: Project folder path at the start
   - All other steps execute autonomously with no user interaction
   - Changed collaborative mode step in Task 5 to use evidence-based causality assessment

### 2. **New Task 0: Comprehensive Project Metadata** (11 steps)
   - Complete file tree scanning
   - File counts and categorisation by type
   - File size calculations
   - Timestamp extraction and timeline analysis
   - Development duration calculation
   - **Token counting** across all text files
   - Error log identification and cataloguing
   - Chat/conversation log discovery
   - Conversation turn and message counting
   - SPEC file version identification
   - Comprehensive metadata snapshot creation

### 3. **Enhanced Task 4: Execution Performance** (13 steps, up from 7)
   Now includes:
   - Total steps taken (defined, attempted, completed, skipped, failed)
   - Multi-level success/failure rates
   - Detailed backup method analysis
   - Mode usage and escalation tracking
   - **Comprehensive timestamp and time metrics**
   - Error propagation effectiveness
   - Detailed retry pattern analysis
   - Efficiency and productivity metrics
   - Critical vs non-critical performance comparison
   - Expected vs actual output analysis
   - **Error counting and categorisation**
   - **Token usage per step** (if available)

### 4. **Enhanced Task 7: Comprehensive Error Analysis** (13 steps, up from 6)
   Now includes:
   - Error source inventory from all locations
   - Total error counts with multiple breakdowns
   - Error categorisation by type AND severity
   - **Detailed error log file parsing**
   - Error hotspot and clustering analysis
   - Root cause analysis with 5 Whys methodology
   - Error propagation chain tracking
   - Recovery effectiveness with time metrics
   - Error message quality assessment
   - Constitutional violations correlation
   - Error preventability classification
   - **Error-related time cost calculation**
   - Error patterns by goal characteristics

### 5. **Expanded Report Structure**
   - New Section 0: Project Metadata Overview (5 subsections)
   - Expanded Section 4: Execution Performance (12 subsections with detailed metrics)
   - Expanded Section 7: Comprehensive Error Analysis (13 subsections)
   - Enhanced Appendices with 6 major sections including raw data tables

### 6. **Meticulous Data Gathering**
   The SPEC now tracks:
   - File counts, sizes, types, timestamps
   - Token counts (words, characters, estimated LLM tokens)
   - Development time duration
   - Conversation metrics (messages, turns, timestamps)
   - Step counts (all statuses)
   - Error counts from multiple sources
   - Time per step/task/total
   - Retry patterns
   - All timestamps and durations

## Statistics:
- **Total Tasks**: 9 (0-8)
- **Total Steps**: ~85+ detailed analysis steps
- **Minimum Recommendations**: 8 (up from 5)
- **Goal Text Propagation Examples**: Minimum 3 with full quotes
- **Metric Categories**: 40+ distinct metric types tracked

The SPEC is now ready for execution and will produce an extremely thorough, data-rich analysis of any test SPEC development project!

Would you like me to create the companion `parameters_Dev_Analysis.toml` and `exe_Dev_Analysis.md` files to complete the three-file SPEC architecture?

