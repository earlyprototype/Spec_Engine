# Project Constitution: [PROJECT NAME]

**Version:** 1.0  
**Date:** [DATE]  
**Project Domain:** [DOMAIN]  
**Status:** Active  
**Purpose:** Define project-specific governance principles that guide all Spec development

---

## How to Use This Template

1. **Read the system constitution first:** `_commander/constitution.md` contains immutable system-wide principles
2. **Answer all questions in this template** to define your project-specific governance
3. **Review with team** (if applicable) to ensure alignment
4. **Save as:** `_commander/constitution_[project_name].md`
5. **Reference in specs** so Commander knows your project requirements

**Relationship to System Constitution:**
- **System Constitution** (`constitution.md`): Immutable rules for ALL specs
- **Project Constitution** (this file): Customisable rules for THIS project's specs

---

## Section 1: Project Context

### 1.1 Project Overview

**Question 1:** What is this project's primary purpose?

**Answer:**
```
[Describe what this project aims to achieve - be specific]
```

**Question 2:** What domain does this project operate in?

**Answer:**
- [ ] Software Development (testing, debugging, refactoring)
- [ ] Data Analysis / Research
- [ ] Content Creation / Documentation
- [ ] System Administration / DevOps
- [ ] Machine Learning / AI
- [ ] Business Process Automation
- [ ] Other: _______________

**Question 3:** What is the typical complexity level of specs in this project?

**Answer:**
- [ ] Simple (1-3 tasks, 3-8 steps total)
- [ ] Moderate (3-5 tasks, 8-15 steps total)
- [ ] Complex (4-5 tasks, 15-25 steps total)
- [ ] Highly Complex (5+ tasks, 25+ steps)

### 1.2 Stakeholders

**Question 4:** Who will create specs in this project?

**Answer:**
- [ ] Solo developer (just me)
- [ ] Small team (2-5 people)
- [ ] Large team (6+ people)
- [ ] External contributors

**Question 5:** Who will review/approve specs?

**Answer:**
```
[List roles: e.g., Tech Lead, Product Owner, etc.]
```

**Question 6:** What is the expected review/approval workflow?

**Answer:**
- [ ] No formal review (solo project, trust-based)
- [ ] Peer review (one other person)
- [ ] Formal approval process (designated approver)
- [ ] Committee review (multiple stakeholders)

---

## Section 2: Quality Standards

### 2.1 Success Criteria

**Question 7:** How do you measure if a spec execution is "successful"?

**Answer:**
Check all that apply:
- [ ] All tasks complete without critical failures
- [ ] Output matches expected results
- [ ] Execution time within acceptable limits
- [ ] No manual intervention required
- [ ] Documentation generated/updated
- [ ] Tests pass (if applicable)
- [ ] Other: _______________

**Question 8:** What is the acceptable failure rate for non-critical steps?

**Answer:**
- [ ] 0% (all steps must succeed)
- [ ] <10% (minimal failures acceptable)
- [ ] <25% (moderate failures tolerable)
- [ ] <50% (best-effort execution)

### 2.2 Output Quality

**Question 9:** How specific must expected outputs be?

**Answer:**
- [ ] Very specific (exact format, structure, content defined)
- [ ] Moderately specific (format defined, content general)
- [ ] General (high-level description sufficient)

**Question 10:** Are there standard output formats for this project?

**Answer:**
```
[List formats: e.g., Markdown, JSON, CSV, etc.]
[Include templates or examples if applicable]
```

### 2.3 Documentation Requirements

**Question 11:** What documentation must each spec produce?

**Answer:**
Check all that apply:
- [ ] Execution log (progress.json) - MANDATORY
- [ ] Output artefacts (files generated)
- [ ] Summary report (what was accomplished)
- [ ] Error report (if failures occurred)
- [ ] Recommendations for improvement
- [ ] Other: _______________

---

## Section 3: Execution Configuration

### 3.1 Default Execution Mode

**Question 12:** What is the preferred default execution mode for specs in this project?

**Answer:**
- [ ] **Silent Mode** - Fully autonomous, minimal interruption
  - Use when: Specs are well-tested, outcomes predictable
  - Risk: May complete with suboptimal results
  
- [ ] **Collaborative Mode** - Human-in-loop for all steps
  - Use when: High-stakes, learning mode, building confidence
  - Risk: Time-consuming, requires availability
  
- [ ] **Dynamic Mode (RECOMMENDED)** - Intelligent escalation
  - Use when: Balance needed between autonomy and safety
  - Risk: May interrupt at unexpected times

**Rationale for choice:**
```
[Explain why this mode suits your project]
```

### 3.2 Mode Escalation Preferences

**Question 13:** When should Dynamic Mode escalate to Collaborative?

**Answer:**
Configure escalation triggers (from most to least aggressive):

- [ ] **Strict** - Escalate after 2 consecutive failures
- [ ] **Moderate (RECOMMENDED)** - Escalate after 3 consecutive failures
- [ ] **Relaxed** - Escalate after 5 consecutive failures
- [ ] **Custom threshold:** _____ consecutive failures

**Question 14:** Should confidence degradation trigger escalation?

**Answer:**
- [ ] Yes - Escalate if confidence score drops below 0.6
- [ ] Yes - Escalate if confidence score drops below 0.5
- [ ] No - Only escalate on failure count

### 3.3 Critical Flags

**Question 15:** What percentage of steps are typically critical in your project?

**Answer:**
- [ ] High criticality project (60-80% critical) - Failures are serious
- [ ] Moderate criticality project (40-60% critical) - RECOMMENDED
- [ ] Low criticality project (20-40% critical) - Best-effort acceptable

**Question 16:** How should critical step failures be handled by default?

**Answer:**
- [ ] **halt_on_critical** - Stop immediately, no further execution
  - Use when: Each step depends on prior, no value in partial completion
  
- [ ] **collaborative_review** - Pause and ask human what to do
  - Use when: Human judgement needed on failure impact
  
- [ ] **continue_and_log** - Log warning but continue execution
  - Use when: Partial completion has value, failures tolerable

**Rationale:**
```
[Explain why this strategy suits your project]
```

---

## Section 4: Error Handling

### 4.1 Error Propagation Strategy

**Question 17:** Should downstream steps be aware of upstream failures?

**Answer:**
- [ ] Yes - Always read progress.json before each step (RECOMMENDED)
- [ ] No - Execute steps independently
- [ ] Only for steps with explicit dependencies

**Question 18:** What is the default propagation strategy?

**Answer:**
- [ ] **halt_on_critical** - Stop execution on critical failure
- [ ] **collaborative_review** - Ask human on critical failure (RECOMMENDED)
- [ ] **continue_and_log** - Continue with warnings

**Question 19:** What is the failure threshold for automatic escalation?

**Answer:**
```
After [___] consecutive failures, escalate to collaborative mode regardless of individual step criticality.

Recommended: 3 (strict), 5 (moderate), 7 (relaxed)
```

### 4.2 Backup Method Requirements

**Question 20:** Are backup methods mandatory for critical steps?

**Answer:**
- [ ] Yes - Every critical step MUST have at least one backup (RECOMMENDED)
- [ ] No - Backups are optional even for critical steps
- [ ] Partial - Critical steps in high-risk tasks must have backups

**Question 21:** What types of backups are preferred?

**Answer:**
Check all that apply:
- [ ] Cognitive alternatives (different reasoning approaches)
- [ ] Tool-based alternatives (different tools/scripts)
- [ ] Hybrid (mix of both)

**Question 22:** Are there standard backup tools for this project?

**Answer:**
```
[List tools and when to use them. Examples:]
- PDF extraction: Try pypdf2, then pdfplumber, then OCR
- Code analysis: Try AST parsing, then regex, then manual inspection
- [Add your project-specific tools]
```

### 4.3 Retry Configuration

**Question 23:** What is the default retry limit for steps?

**Answer:**
```
Max retries per step: [0-5]

Recommended: 2 (balance persistence with efficiency)
```

**Question 24:** Should retry delays increase over time?

**Answer:**
- [ ] Yes - Use exponential backoff (1s, 2s, 4s...)
- [ ] Yes - Use linear increase (1s, 2s, 3s...)
- [ ] No - Retry immediately

---

## Section 5: Resource Constraints

### 5.1 Time Limits

**Question 25:** Are there time limits for spec execution?

**Answer:**
- [ ] Yes - Strict time limit: _____ minutes
- [ ] Yes - Soft time limit: _____ minutes (warning but continue)
- [ ] No - Execute until complete or failure

**Question 26:** Are there time limits per task or step?

**Answer:**
```
Task timeout: [___] minutes (or N/A)
Step timeout: [___] seconds (or N/A)
```

### 5.2 Resource Usage

**Question 27:** Are there resource usage constraints?

**Answer:**
Check all that apply:
- [ ] Memory limit: _____ MB
- [ ] CPU limit: _____ % utilisation
- [ ] Disk space limit: _____ GB
- [ ] Network bandwidth limit: _____ MB/s
- [ ] No constraints

**Question 28:** What should happen if resource limits are exceeded?

**Answer:**
- [ ] Halt execution immediately
- [ ] Escalate to collaborative mode
- [ ] Log warning and continue
- [ ] Attempt cleanup and retry

### 5.3 External Dependencies

**Question 29:** Does this project rely on external services/APIs?

**Answer:**
- [ ] Yes - List below:
  ```
  [Service name, purpose, rate limits, fallback if unavailable]
  ```
- [ ] No

**Question 30:** How should external service failures be handled?

**Answer:**
- [ ] Retry with backoff
- [ ] Use cached data if available
- [ ] Skip step and log warning
- [ ] Fail critical and escalate

---

## Section 6: Testing & Validation

### 6.1 Test Requirements

**Question 31:** Are automated tests required for specs in this project?

**Answer:**
- [ ] Yes - Tests MANDATORY for all specs
- [ ] Yes - Tests required for critical specs only
- [ ] No - Tests optional
- [ ] Not applicable to this project

**Question 32:** If tests are required, what type?

**Answer:**
Check all that apply:
- [ ] Unit tests (individual functions/methods)
- [ ] Integration tests (component interactions)
- [ ] Contract tests (API/interface compliance)
- [ ] End-to-end tests (full workflow)
- [ ] Regression tests (verify no breakage)

**Question 33:** When should tests be written?

**Answer:**
- [ ] Before implementation (TDD - RECOMMENDED if tests used)
- [ ] After implementation
- [ ] Doesn't matter

### 6.2 Validation Requirements

**Question 34:** Should acceptance scenarios be mandatory?

**Answer:**
- [ ] Yes - Every spec must include Given/When/Then scenarios
- [ ] Yes - Only for complex specs (4+ tasks)
- [ ] No - Acceptance scenarios optional

**Question 35:** Should success criteria be quantitative?

**Answer:**
- [ ] Yes - All success criteria must be measurable
- [ ] Preferred but not mandatory
- [ ] No - Qualitative criteria acceptable

**Question 36:** Should edge cases be documented?

**Answer:**
- [ ] Yes - Mandatory for all specs
- [ ] Yes - For critical specs only
- [ ] No - Document as encountered

---

## Section 7: Logging & Observability

### 7.1 Logging Detail Level

**Question 37:** How detailed should progress logging be?

**Answer:**
- [ ] **Verbose** - Log every action, decision, and outcome
- [ ] **Standard (RECOMMENDED)** - Log steps, failures, mode switches
- [ ] **Minimal** - Log only critical events and final status

**Question 38:** Should logging include performance metrics?

**Answer:**
- [ ] Yes - Include timing, confidence scores, resource usage
- [ ] Partial - Include timing only
- [ ] No - Status and outcomes only

### 7.2 Log Retention

**Question 39:** How long should execution logs be retained?

**Answer:**
```
Progress logs retention: [___] days/months
Archived logs: [___] months/years
Permanent retention: [Yes/No]
```

**Question 40:** Should logs be centralised?

**Answer:**
- [ ] Yes - Aggregate all spec logs to central location: _______________
- [ ] No - Keep logs with individual specs

### 7.3 Error Reporting

**Question 41:** How should errors be reported?

**Answer:**
Check all that apply:
- [ ] Log to progress.json (MANDATORY)
- [ ] Console output
- [ ] Email notification
- [ ] Slack/Teams notification
- [ ] Issue tracker (GitHub, Jira, etc.)
- [ ] Other: _______________

---

## Section 8: Collaboration & Review

### 8.1 Spec Review Process

**Question 42:** Must specs be reviewed before first execution?

**Answer:**
- [ ] Yes - Formal review required
- [ ] Yes - Informal review (quick check)
- [ ] No - Execute without review (solo projects)

**Question 43:** What must be reviewed?

**Answer:**
Check all that apply:
- [ ] Goal clarity and singularity
- [ ] Task decomposition logic
- [ ] Critical flag assignments
- [ ] Backup method quality
- [ ] Expected output specificity
- [ ] Constitutional compliance
- [ ] Other: _______________

### 8.2 Change Management

**Question 44:** How should spec modifications be tracked?

**Answer:**
- [ ] Version control (Git) - RECOMMENDED
- [ ] Change log in spec file
- [ ] No formal tracking

**Question 45:** Must spec changes be reviewed?

**Answer:**
- [ ] Yes - Always
- [ ] Yes - If critical sections changed
- [ ] No

---

## Section 9: Domain-Specific Requirements

### 9.1 Project-Specific Constraints

**Question 46:** Are there project-specific constraints that all specs must respect?

**Answer:**
```
[List constraints. Examples:]
- Must use Python 3.11+
- Cannot access external network
- Must complete within business hours
- Must preserve existing file structure
- [Add your constraints]
```

### 9.2 Required Components

**Question 47:** Are there standard components all specs should use?

**Answer:**
```
[List components. Examples:]
- Logging library: [name]
- Config management: [method]
- File handling: [standards]
- Error handling: [patterns]
- [Add your components]
```

### 9.3 Prohibited Actions

**Question 48:** Are there actions specs must NEVER perform?

**Answer:**
```
[List prohibited actions. Examples:]
- Do not delete files outside project directory
- Do not modify system configuration
- Do not install packages without approval
- Do not expose credentials/secrets
- [Add your prohibitions]
```

### 9.4 Compliance Requirements

**Question 49:** Are there compliance/regulatory requirements?

**Answer:**
- [ ] Yes - List below:
  ```
  [GDPR, HIPAA, SOC2, etc. - explain implications for specs]
  ```
- [ ] No

**Question 50:** Are there security requirements?

**Answer:**
Check all that apply:
- [ ] No credentials in logs
- [ ] Encrypt sensitive data
- [ ] Audit trail required
- [ ] Access control checks
- [ ] Other: _______________

---

## Section 10: Optional Features

### 10.1 User Story Format

**Question 51:** Should specs use user story format?

**Answer:**
- [ ] Yes - Mandatory for all specs
- [ ] Yes - For user-facing features only
- [ ] No - Use traditional task/step format

**If Yes:**
```
User story template to use:
As a [role]
I want [action]
So that [benefit]

Acceptance Criteria: [Given/When/Then]
```

### 10.2 Clarification Phase

**Question 52:** Should specs include upfront clarification phase?

**Answer:**
- [ ] Yes - Always detect and resolve ambiguities before generation
- [ ] Yes - For complex specs only
- [ ] No - Generate specs from prompt directly

**Question 53:** What triggers clarification phase?

**Answer:**
Check all that apply:
- [ ] Underspecified elements detected
- [ ] Multiple interpretations possible
- [ ] Missing edge cases
- [ ] Undefined terms/jargon
- [ ] Manual request

### 10.3 Quickstart Validation

**Question 54:** Should specs generate post-execution validation checklists?

**Answer:**
- [ ] Yes - Always generate quickstart validation
- [ ] Yes - For critical specs only
- [ ] No

**If Yes:**
```
Validation checklist should include:
- [ ] Manual verification steps
- [ ] Automated test commands
- [ ] Regression test scenarios
- [ ] Other: _______________
```

### 10.4 Parallel Execution

**Question 55:** Should parallel execution be allowed?

**Answer:**
- [ ] Yes - Enable parallel execution for independent steps
- [ ] No - Sequential execution only (RECOMMENDED)

**If Yes:**
```
Maximum parallel steps: [2-5]
Output conflict detection: [Yes/No]
```

**Rationale for choice:**
```
[Parallel execution is complex - explain why you need it]
```

---

## Section 11: Project Constitution Summary

### 11.1 Generated Defaults

Based on your answers, the following defaults apply to all specs in this project:

**Execution Configuration:**
```
[Auto-generated from answers above]
Default mode: [from Q12]
Escalation threshold: [from Q13]
Critical flag balance: [from Q15]
Error propagation: [from Q17, Q18]
Failure threshold: [from Q19]
```

**Quality Standards:**
```
[Auto-generated from answers above]
Expected output specificity: [from Q9]
Documentation requirements: [from Q11]
Test requirements: [from Q31, Q32]
Validation requirements: [from Q34, Q35, Q36]
```

**Resource Constraints:**
```
[Auto-generated from answers above]
Time limits: [from Q25, Q26]
Resource limits: [from Q27]
External dependencies: [from Q29, Q30]
```

**Optional Features:**
```
[Auto-generated from answers above]
User stories: [from Q51]
Clarification phase: [from Q52]
Quickstart validation: [from Q54]
Parallel execution: [from Q55]
```

### 11.2 Project-Specific Additions

**Custom principles for this project:**
```
[Add any project-specific principles not covered by questions above]

Example:
- All specs must include code review checklist
- Critical specs require pair programming
- Documentation must follow project style guide
```

### 11.3 Exemptions from System Constitution

**IMPORTANT:** The system constitution (_commander/constitution.md) is immutable. However, this project constitution can request exemptions for specific circumstances.

**Question 56:** Are there any system constitution rules you need to modify for this project?

**Answer:**
- [ ] No exemptions needed
- [ ] Request exemption (explain below)

**If exemption requested:**
```
Article/Section: [e.g., Article II, Section 2.3]
Standard rule: [e.g., "Tasks per goal: 2-5"]
Requested modification: [e.g., "Allow 6-8 tasks for highly complex workflows"]
Rationale: [Detailed justification]
Risk assessment: [What could go wrong]
Mitigation: [How to manage risks]
```

**Exemption approval:**
- [ ] Approved by: _______________
- [ ] Date: _______________
- [ ] Review date: _______________

---

## Section 12: Commander Integration

### 12.1 How Commander Uses This Constitution

When the Commander (`Spec_Commander.md`) generates a new spec, it will:

1. **Read system constitution** (`_commander/constitution.md`) for immutable rules
2. **Read this project constitution** for project-specific guidance
3. **Apply both** when validating and generating specs
4. **Flag conflicts** if project requirements contradict system rules
5. **Use defaults** from Section 11 when generating TOML parameters

### 12.2 Validation Integration

During Step 5 (Pre-Flight Validation), Commander will:

**From System Constitution:**
- Verify hierarchical structure (Article II)
- Check dual-file synchronisation (Article III)
- Validate explicitness requirements (Article V)
- Detect anti-patterns (Article XII)

**From Project Constitution:**
- Apply project-specific quality standards (Section 2)
- Use project execution configuration (Section 3)
- Check project constraints (Section 9)
- Verify optional features configured correctly (Section 10)

### 12.3 Progress Logging Integration

The `progress.json` file will include a project compliance section:

```json
{
  "run_id": "...",
  "project_constitution": {
    "project_name": "[PROJECT NAME]",
    "constitution_version": "1.0",
    "defaults_applied": {
      "execution_mode": "[from Q12]",
      "error_propagation": "[from Q18]",
      "critical_threshold": "[from Q15]"
    },
    "compliance_checks": [
      {
        "requirement": "[from this constitution]",
        "status": "pass/fail/warning",
        "details": "..."
      }
    ]
  }
}
```

---

## Section 13: Review and Maintenance

### 13.1 Review Schedule

**Question 57:** How often should this project constitution be reviewed?

**Answer:**
- [ ] After every 5 spec executions
- [ ] Monthly
- [ ] Quarterly
- [ ] Annually
- [ ] As needed (no schedule)

**Next review date:** _______________

### 13.2 Amendment Process

**Changes to this project constitution require:**
1. Documentation of rationale
2. Impact assessment (which specs affected)
3. Team review (if applicable)
4. Version increment
5. Update to all active specs (if needed)

**Version History:**
```
v1.0 ([DATE]): Initial project constitution
```

### 13.3 Lessons Learned

**After each spec execution, consider:**
- Did the defaults work well?
- Should any thresholds be adjusted?
- Are new constraints needed?
- Should any requirements be relaxed?

**Continuous improvement log:**
```
[Date] - [Observation] - [Action taken]
```

---

## Section 14: Quick Reference Card

### For Spec Authors

**Before creating a spec:**
1. Read system constitution: `_commander/constitution.md`
2. Read this project constitution
3. Ensure you understand project defaults
4. Follow project-specific constraints (Section 9)

**Your spec must:**
- Have singular, clear goal (System Article I)
- Follow hierarchical structure (System Article II)
- Use project default mode ([from Q12])
- Respect project critical flag balance ([from Q15])
- Include project-required documentation ([from Q11])
- Respect project constraints ([Section 9])

### For Spec Executors (LLMs)

**During execution:**
1. Validate against system constitution first
2. Validate against project constitution second
3. Use project defaults for execution configuration
4. Log project compliance in progress.json
5. Escalate according to project thresholds

**Project-specific rules:**
- Default mode: [from Q12]
- Escalation threshold: [from Q13]
- Critical failure handling: [from Q16]
- Error propagation: [from Q18]
- Failure threshold: [from Q19]

---

## Appendix: Example Configurations

### Example A: High-Criticality Project (Security Audit)

```yaml
Default mode: Collaborative
Escalation: Strict (2 failures)
Critical percentage: 60-80%
Critical failure handling: halt_on_critical
Tests: Mandatory
Acceptance scenarios: Mandatory
```

### Example B: Low-Criticality Project (Documentation Generation)

```yaml
Default mode: Silent
Escalation: Relaxed (5 failures)
Critical percentage: 20-40%
Critical failure handling: continue_and_log
Tests: Optional
Acceptance scenarios: Optional
```

### Example C: Balanced Project (Data Analysis)

```yaml
Default mode: Dynamic
Escalation: Moderate (3 failures)
Critical percentage: 40-60%
Critical failure handling: collaborative_review
Tests: Critical specs only
Acceptance scenarios: Complex specs only
```

---

**End of Project Constitution Template**

**Next Steps:**
1. Answer all questions in this template
2. Save as `_commander/constitution_[project_name].md`
3. Review with team (if applicable)
4. Update Commander to reference this file
5. Generate first spec and validate configuration
6. Iterate based on experience

**Integration Note:**  
The Commander will automatically detect and use this project constitution when generating specs in this project directory.

