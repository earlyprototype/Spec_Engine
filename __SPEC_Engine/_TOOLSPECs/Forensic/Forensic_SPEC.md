# Forensic SPEC (Root Cause Investigation)

**Version:** 1.0  
**Last Updated:** 2 January 2026  
**Purpose:** Forensic analysis for crashes, data corruption, security incidents, or catastrophic failures

---

## Goal

Conduct systematic forensic investigation to determine root cause, blast radius, and remediation strategy for critical production incidents, producing an actionable investigation report.

---

## Knowledge Capture (Notepad)

**Purpose:** Capture insights, observations, and learnings during execution.

This notepad will be populated during execution with:
- Key insights and aha moments from evidence analysis
- Technical discoveries and investigative decisions
- Ideas for prevention and monitoring improvements
- Cross-system connections and patterns
- Observations from both AI executor and human investigator

**File:** `notepad_Forensic.md` (automatically created during execution)

**Update Frequency:** Configured in parameters.toml (per_task by default)

---

## Software Stack & Architecture

**Not Applicable** - This is a forensic investigation task, not a build goal.

---

## Definition of Complete

What must exist and be verified:
- [ ] **Primary deliverable:** Comprehensive forensic investigation report including:
  - Incident timeline reconstructed with timestamps
  - Root cause identified with supporting evidence
  - Blast radius quantified (affected systems, users, data)
  - Contributing factors documented
  - Remediation recommendations (immediate and long-term)
  - Prevention measures proposed (monitoring, safeguards)
- [ ] **Quality standards met:**
  - Root cause supported by evidence (logs, traces, code analysis)
  - Timeline is accurate and complete (no unexplained gaps)
  - Blast radius is quantified with specific numbers
  - Remediation is actionable and tested (where possible)
- [ ] **Verification method:**
  - Root cause reproduces in controlled environment (or is explained if not reproducible)
  - Remediation prevents recurrence (verified by testing)
  - Prevention measures are implementable
  - Human incident commander confirms report completeness

---

## Troubleshooting Ecosystem

This TOOLSPEC is part of a three-spec troubleshooting ecosystem:

| TOOLSPEC | When to Use | Output |
|----------|-------------|--------|
| **Troubleshoot** | Post-development issues blocking goal | Fixed deliverables |
| **WTF** | Mysterious/legacy code needs understanding | Documentation |
| **Forensic** | Critical failure needs root cause | Investigation report |

**Decision Tree:**
1. Is this a production incident with data loss/security breach? → Use **Forensic** (this spec)
2. Is the code mysterious/undocumented and you need to understand it? → Use **WTF**
3. Is something broken and needs fixing? → Use **Troubleshoot**

**When to use Forensic:**
- Production system crashed or became unavailable
- Data corruption or loss occurred
- Security breach or unauthorized access detected
- Cascading failures across multiple systems
- Critical performance degradation (>10x slowdown)
- Financial loss or regulatory incident

---

## MCP Toolset

### Installed Tools (Verified During SPEC Creation)

**REQUIRED Tools:**
- **filesystem**: Read logs, configuration files, source code
  - Rationale: Essential for evidence gathering
  - Install command: Built-in (no installation required)

**RECOMMENDED Tools:**
- **git**: Access commit history, blame information, recent changes
  - Rationale: Recent code changes often correlate with incidents
  - Alternative: Manual git commands
  - Install command: `npx @modelcontextprotocol/server-git`

- **github**: Check for known issues, recent deployments, CI/CD logs
  - Rationale: Context from issues and deployment history
  - Alternative: Manual GitHub web interface
  - Install command: `npx @modelcontextprotocol/server-github`

- **postgres** or **database**: Query database logs, transaction history
  - Rationale: Database incidents require direct access
  - Alternative: Database CLI tools
  - Install command: `npx @modelcontextprotocol/server-postgres`

**OPTIONAL Tools:**
- **docker**: Inspect container logs, resource usage
  - Use case: Containerized application incidents
  - Install command: `npx @modelcontextprotocol/server-docker`

- **slack** or **pagerduty**: Retrieve incident timeline from alerting systems
  - Use case: Correlate alerts with incident progression
  - Install command: MCP server for respective platform

### Tool Verification

The executor will verify tool availability during initialisation (Section 1.11) as a safety check.

---

## Definitions

- **goal**: Determine root cause, blast radius, and remediation for critical production incident
- **task[n]**: Discrete investigation objectives (evidence, timeline, root cause, blast radius, remediation)
- **step[m]**: Concrete forensic actions within each task
- **backup[p]**: Alternative investigation method when primary approach fails
- **critical_flag**: Boolean indicating whether step failure blocks investigation goal
- **mode**: Execution mode per step - `collaborative` (incident triage), then `dynamic` (systematic investigation)
- **progress.json**: Structured log tracking investigation execution and findings
- **incident**: The critical failure being investigated
- **evidence**: Logs, traces, metrics, code, configuration supporting analysis

---

## Components

Forensic investigation requires access to:
- **System logs:** Application logs, system logs, web server logs, database logs
- **Error traces:** Stack traces, core dumps, crash reports
- **Metrics and monitoring:** CPU, memory, disk, network usage during incident
- **Version control:** Recent code changes, deployments, configuration changes
- **Configuration:** Environment variables, feature flags, infrastructure configuration
- **Data snapshots:** Database state before/during/after incident (if available)
- **External dependencies:** Third-party API status, network conditions
- **Alerting history:** When alerts fired, escalation timeline
- **User reports:** Error messages users saw, actions they were performing

---

## Constraints

- MUST preserve evidence (read-only access to logs and data where possible)
- MUST establish timeline before hypothesizing root cause
- MUST quantify blast radius with specific numbers (affected users, data, systems)
- MUST support root cause with evidence (not speculation)
- MUST distinguish between root cause and contributing factors
- SHOULD reproduce issue in controlled environment if possible
- SHOULD correlate multiple evidence sources for verification
- MAY require human subject matter experts for domain-specific analysis

---

## Tasks

### Task [1]: Evidence Gathering

**Purpose:** Collect all available evidence related to the incident.

#### Step [1.1]: Collect system logs (application, system, network)
- **Primary method:** Gather logs from all relevant systems during incident window (±1 hour)
- **Expected output:** Log collection manifest listing all logs, their time ranges, and sizes
- **Critical:** true
- **Backup [1]:** If centralized logging unavailable, collect from individual servers/containers

#### Step [1.2]: Capture error messages and stack traces
- **Primary method:** Extract all error/exception messages from logs during incident
- **Expected output:** Categorized error list with frequencies and timestamps
- **Critical:** true
- **Backup [1]:** If structured logging missing, use regex patterns to extract errors

#### Step [1.3]: Document environmental state (versions, config, dependencies)
- **Primary method:** Record software versions, configuration values, dependency versions at incident time
- **Expected output:** Environment snapshot document (YAML or JSON format)
- **Critical:** true
- **Backup [1]:** If version info not logged, infer from deployment logs and git history

#### Step [1.4]: Preserve evidence (timestamped snapshots)
- **Primary method:** Create timestamped copies of all evidence before any remediation
- **Expected output:** Evidence archive with SHA256 checksums for integrity
- **Critical:** false
- **Backup [1]:** If disk space limited, compress logs and store critical evidence only

---

### Task [2]: Timeline Reconstruction

**Purpose:** Build accurate chronological sequence of events.

#### Step [2.1]: Establish incident start time
- **Primary method:** Identify first error or anomaly in logs, cross-reference with monitoring alerts
- **Expected output:** Incident start timestamp with supporting evidence
- **Critical:** true
- **Backup [1]:** If exact start unclear, establish range and note uncertainty

#### Step [2.2]: Identify trigger event or initial symptom
- **Primary method:** Analyze logs immediately before incident start for anomalies or changes
- **Expected output:** Trigger event description with timestamp and evidence
- **Critical:** true
- **Backup [1]:** If trigger not found in logs, interview operators/users for context

#### Step [2.3]: Map sequence of failures (cascade analysis)
- **Primary method:** Trace error propagation across systems chronologically
- **Expected output:** Timeline diagram showing cascade (System A failed → System B failed → ...)
- **Critical:** true
- **Backup [1]:** If cascade is complex, create simplified diagram focusing on critical path

#### Step [2.4]: Identify detection/discovery time
- **Primary method:** Find when incident was first detected (alert, user report, manual discovery)
- **Expected output:** Detection timestamp and method (alert name, user report, manual check)
- **Critical:** false
- **Backup [1]:** If detection time unclear, use first remediation action as proxy

---

### Task [3]: Root Cause Analysis

**Purpose:** Determine the fundamental cause of the incident.

#### Step [3.1]: Generate hypotheses (5 Whys, Fishbone)
- **Primary method:** Use 5 Whys technique starting from symptoms, create fishbone diagram for categories
- **Expected output:** List of 3-7 hypotheses ranked by likelihood with supporting observations
- **Critical:** true
- **Backup [1]:** If 5 Whys is insufficient, use fault tree analysis

#### Step [3.2]: Test hypotheses against evidence
- **Primary method:** For each hypothesis, check if all evidence supports it or contradicts it
- **Expected output:** Hypothesis evaluation matrix (hypothesis vs evidence compatibility)
- **Critical:** true
- **Backup [1]:** If evidence is ambiguous, design targeted experiments to test hypotheses

#### Step [3.3]: Reproduce issue in controlled environment (if possible)
- **Primary method:** Set up test environment matching production state, trigger incident conditions
- **Expected output:** Reproduction steps or documentation of why reproduction failed
- **Critical:** false
- **Backup [1]:** If full reproduction impossible, reproduce simplified version or related behaviour

#### Step [3.4]: Confirm root cause with proof
- **Primary method:** Provide definitive evidence linking root cause to observed symptoms
- **Expected output:** Root cause statement with evidence chain (Cause X → Symptom Y → Symptom Z)
- **Critical:** true
- **Backup [1]:** If definitive proof unavailable, provide "most likely root cause" with confidence level

---

### Task [4]: Blast Radius Assessment

**Purpose:** Quantify the full scope and impact of the incident.

#### Step [4.1]: Identify affected systems and services
- **Primary method:** Trace error propagation to enumerate all impacted systems/services
- **Expected output:** List of affected systems with impact severity (critical/major/minor)
- **Critical:** true
- **Backup [1]:** If system dependencies unclear, use architecture diagram to infer

#### Step [4.2]: Quantify data impact (corrupted, lost, exposed)
- **Primary method:** Query databases/storage for data anomalies during incident window
- **Expected output:** Data impact report with specific counts (X records corrupted, Y records lost)
- **Critical:** true
- **Backup [1]:** If exact quantification impossible, provide estimates with confidence intervals

#### Step [4.3]: Determine user impact (count, severity, duration)
- **Primary method:** Analyze user session logs, error rates, support tickets during incident
- **Expected output:** User impact metrics (N users affected, M% error rate, D minutes duration)
- **Critical:** true
- **Backup [1]:** If user metrics unavailable, extrapolate from system load and typical traffic

---

### Task [5]: Remediation & Prevention

**Purpose:** Define fixes and safeguards to prevent recurrence.

#### Step [5.1]: Immediate fix (stop the bleeding)
- **Primary method:** Identify fastest way to restore service (rollback, restart, disable feature)
- **Expected output:** Immediate remediation action plan with rollback procedure
- **Critical:** true
- **Backup [1]:** If clean fix unavailable, define temporary workaround

#### Step [5.2]: Long-term remediation (address root cause)
- **Primary method:** Design code/configuration/infrastructure change that eliminates root cause
- **Expected output:** Detailed remediation plan with implementation steps and testing strategy
- **Critical:** true
- **Backup [1]:** If complex remediation needed, break into phased approach

#### Step [5.3]: Prevention measures (monitoring, safeguards)
- **Primary method:** Identify monitoring gaps and add alerts/circuit breakers to prevent recurrence
- **Expected output:** Prevention checklist (new alerts, rate limits, validation checks)
- **Critical:** false
- **Backup [1]:** If monitoring infrastructure limited, prioritize most critical safeguards

#### Step [5.4]: Documentation and postmortem report
- **Primary method:** Compile all findings into structured postmortem (timeline, root cause, remediation)
- **Expected output:** Postmortem document following 5-part structure (below)
- **Critical:** true
- **Backup [1]:** If time-constrained, create abbreviated postmortem with link to full investigation

---

## Postmortem Report Structure

The final deliverable MUST follow this structure:

### 1. Executive Summary
- **Incident:** One-sentence description
- **Impact:** Users affected, duration, data loss/corruption
- **Root Cause:** One-sentence root cause
- **Status:** Resolved, mitigated, or ongoing

### 2. Timeline
Chronological sequence with timestamps:
- Pre-incident state
- Trigger event
- Failure cascade
- Detection
- Remediation actions
- Resolution

### 3. Root Cause Analysis
- **Root Cause:** Definitive statement with evidence
- **Contributing Factors:** Secondary issues that amplified impact
- **Why It Happened:** Context and background

### 4. Impact Assessment
- **Systems Affected:** List with severity
- **Data Impact:** Quantified (records corrupted/lost/exposed)
- **User Impact:** Quantified (users affected, error rate, duration)
- **Business Impact:** Financial, reputational, regulatory

### 5. Remediation & Prevention
- **Immediate Fix:** What was done to stop incident
- **Long-term Fix:** Permanent solution addressing root cause
- **Prevention Measures:** New monitors, safeguards, processes
- **Action Items:** Specific tasks with owners and deadlines

---

## Bridging (Markdown ↔ TOML)

**All task and step IDs in this markdown MUST match corresponding entries in `parameters_Forensic.toml`.**

**Cross-References:**
- Task [1] → `tasks[id=1]` in TOML
- Task [5] → `tasks[id=5]` in TOML
- All step IDs must match between files

**Validation:** `exe_Forensic.md` Section 1.8 verifies this synchronisation before execution.

---

## Instructions for LLM Executor

### Execution Philosophy

Forensic is a **critical incident investigation** TOOLSPEC. Your approach must be:

1. **Evidence-based:** Every claim supported by logs, traces, or data
2. **Systematic:** Follow investigative process, don't jump to conclusions
3. **Objective:** Root cause may be uncomfortable (human error, design flaw) but must be honest
4. **Actionable:** Recommendations must be specific and implementable
5. **Time-sensitive:** Production incidents require urgency balanced with thoroughness

### Incident Context Gathering

**Before starting Task 1, you MUST establish:**
- What failed? (system, service, component)
- When did it fail? (approximate time)
- Who detected it? (alert, user, engineer)
- What was impact? (users affected, data lost, downtime duration)

**If context unclear, escalate to collaborative mode:**
```
[FORENSIC SETUP - Incident Context Required]

I need basic incident information to begin investigation:

1. What system/service failed?
   Example: "API gateway", "database cluster", "authentication service"

2. When did incident occur?
   Example: "2026-01-02 14:30 UTC" or "today around 2pm"

3. What was observed?
   Example: "500 errors", "data corruption", "unauthorized access"

4. Current status?
   Example: "Still failing", "mitigated but not fixed", "resolved"

Please provide incident context:
```

### Investigation Priorities

**Critical path (must complete):**
1. Preserve evidence → Reconstruct timeline → Identify root cause
2. If time-constrained, focus on these three

**Important (complete if possible):**
3. Quantify blast radius
4. Design remediation

**Nice-to-have (if time permits):**
5. Reproduce in test environment
6. Design prevention measures

### Evidence Preservation

**CRITICAL:** Before ANY remediation:
1. Copy all logs to safe location
2. Record configuration snapshots
3. Document system state
4. Calculate checksums for integrity

**Why:** Remediation often destroys evidence (log rotation, config changes, system restarts)

### Root Cause vs Contributing Factors

**Root Cause:** The fundamental issue that, if eliminated, prevents recurrence
**Contributing Factor:** Issues that amplified impact but aren't fundamental

**Example:**
- Root Cause: Memory leak in authentication service
- Contributing Factors: No memory limit configured, No automated restarts, Alert threshold too high

### Communication During Investigation

If in collaborative mode:
- Provide status updates after each task
- Escalate if evidence is missing or insufficient
- Ask for subject matter experts when encountering unfamiliar systems

**Status update format:**
```
[FORENSIC UPDATE - Task X Complete]
Progress: Completed evidence gathering
Key Finding: Database connection pool exhaustion at 14:32 UTC
Next: Reconstructing timeline of connection consumption
Blocker: None
```

---

**End of Forensic SPEC**

*This TOOLSPEC implements Lia Workflow Specs' "investigate.toml" concept within SPEC Engine's constitutional framework. For related troubleshooting workflows, see Troubleshoot_SPEC.md and WTF_SPEC.md.*
