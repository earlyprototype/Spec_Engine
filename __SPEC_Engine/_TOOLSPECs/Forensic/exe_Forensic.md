# exe_Forensic.md

**Version:** 1.0  
**Last Updated:** 2 January 2026  
**Purpose:** Execution controller for Forensic root cause investigation

---

## Execution Model

This executor follows the standard SPEC Engine execution model defined in `__SPEC_Engine/_templates/exe_template.md` with Forensic-specific customizations documented below.

**Standard Sections (use template):**
- Section 1: Initialization and Validation
- Section 2: Execution Flow
- Section 3: Mode Control
- Section 4: Error Handling
- Section 5: Completion
- Section 6: Post-Execution Analysis

**Forensic-Specific Customizations:**
- Section 0: Incident Context Gathering (before standard Section 1)
- Section 2.8: Evidence Preservation Checkpoint (during execution)
- Section 6.7: Postmortem Report Generation (after standard Section 6)

---

## Section 0: Incident Context Gathering (Forensic-Specific)

**Execute BEFORE Section 1 (Initialization):**

### Purpose
Forensic investigation requires clear incident context upfront. Unlike exploratory specs, forensics begins with a known failure that must be scoped.

### Process

1. **Check for incident specification:**
   - Look for user-provided incident description
   - Check if basic context exists (what/when/impact)

2. **If incident context is provided:**
   ```json
   {
     "incident_context": {
       "what_failed": "API gateway service",
       "when": "2026-01-02T14:30:00Z",
       "observed_symptoms": "HTTP 500 errors, connection timeouts",
       "current_status": "Mitigated but not fully resolved",
       "context_complete": true
     }
   }
   ```
   - Log incident context
   - Verify evidence sources are accessible (logs, metrics)
   - Proceed to Section 1 (standard initialization)

3. **If incident context is NOT provided:**
   - **ESCALATE to collaborative mode immediately**
   - **HALT standard execution flow**
   - **Present incident context prompt:**

   ```
   [FORENSIC SETUP - Incident Context Required]
   
   Forensic investigation requires basic incident information to focus the analysis.
   
   Please provide:
   
   1. What system/service/component failed?
      Example: "API gateway", "PostgreSQL database", "Auth service"
   
   2. When did the incident occur?
      Example: "2026-01-02 14:30 UTC" or "Today at 2pm EST"
   
   3. What symptoms were observed?
      Example: "HTTP 500 errors", "Data corruption", "Unauthorized access"
   
   4. Current status?
      Example: "Still failing", "Mitigated with restart", "Fully resolved"
   
   5. Where can evidence be found?
      Example: "CloudWatch logs", "/var/log/app.log", "Datadog metrics"
   
   Enter incident details:
   ```

4. **Capture user input:**
   - Parse system/service identification
   - Record incident timestamp (convert to ISO-8601)
   - Store symptoms for investigation focus
   - Note current status
   - Document evidence locations

5. **Log incident context:**
   ```json
   {
     "incident_context": {
       "what_failed": "<user_provided>",
       "when": "<ISO-8601>",
       "observed_symptoms": "<user_provided>",
       "current_status": "<user_provided>",
       "evidence_locations": ["<paths_provided>"],
       "context_gathered_at": "<ISO-8601>",
       "context_complete": true
     }
   }
   ```

6. **Verify evidence accessibility:**
   - Check if log files/directories exist and are readable
   - If logs missing: warn user but proceed (may be able to use alternative sources)
   - If no evidence accessible: escalate and request alternative evidence sources

### Why This Matters

**Problem:** Generic execution assumes work scope emerges during execution. Forensics must begin with incident scope to avoid analyzing unrelated systems.

**Solution:** Mandatory incident context prevents wasted investigation effort and ensures focused analysis on the actual failure.

---

## Section 2.8: Evidence Preservation Checkpoint (Forensic-Specific)

**Execute AT START of Task 1, Step 1 (before any evidence collection):**

### Purpose
Critical evidence can be lost during remediation. Evidence must be preserved before ANY modification attempts.

### Preservation Process

1. **Identify evidence sources from incident context:**
   - Log files specified by user
   - System logs (application, database, web server)
   - Configuration files
   - Metrics/monitoring data

2. **Create evidence archive:**
   ```bash
   # Create timestamped evidence directory
   mkdir -p evidence_archive_$(date +%Y%m%d_%H%M%S)
   
   # Copy logs with permissions preserved
   cp -p /path/to/logs/* evidence_archive_*/
   
   # Generate checksums for integrity
   sha256sum evidence_archive_*/* > evidence_checksums.txt
   ```

3. **Log preservation actions:**
   ```json
   {
     "evidence_preservation": {
       "archive_path": "evidence_archive_20260102_143000/",
       "files_preserved": [
         {"path": "/var/log/app.log", "size_bytes": 1234567, "sha256": "abc123..."},
         {"path": "/etc/app/config.yaml", "size_bytes": 4567, "sha256": "def456..."}
       ],
       "preservation_timestamp": "2026-01-02T14:30:00Z",
       "integrity_verified": true
     }
   }
   ```

4. **Warn if preservation fails:**
   - If disk space insufficient: escalate to collaborative mode
   - If permissions deny access: request elevated access or alternative evidence
   - If evidence already modified: note this limitation in investigation

### Constitutional Requirement

Per Article XV (Troubleshooting Ecosystem Parity), forensic investigation must preserve evidence integrity. This checkpoint ensures compliance.

---

## Section 6.7: Postmortem Report Generation (Forensic-Specific)

**Execute AFTER Section 6 (Post-Execution Analysis):**

### Purpose
Compile all investigation findings into structured postmortem report following industry standards.

### Report Structure

The executor MUST generate a markdown file `postmortem_<incident_date>.md` with this structure:

```markdown
# Incident Postmortem - [Brief Incident Description]

**Date:** [Incident Date]  
**Duration:** [Start to Resolution Time]  
**Severity:** [Critical/High/Medium]  
**Status:** [Resolved/Mitigated/Ongoing]

---

## 1. Executive Summary

### Incident
[One-sentence description of what failed]

### Impact
- **Users Affected:** [Specific number or percentage]
- **Duration:** [Minutes/hours of impact]
- **Data Impact:** [Records affected, if any]
- **Systems Affected:** [List of systems]

### Root Cause
[One-sentence root cause statement]

### Current Status
[Resolved/Mitigated/Ongoing with brief status]

---

## 2. Timeline

| Time (UTC) | Event | Notes |
|------------|-------|-------|
| [timestamp] | [Pre-incident normal state] | |
| [timestamp] | [Trigger event] | [Evidence reference] |
| [timestamp] | [First symptom observed] | [Evidence reference] |
| [timestamp] | [Incident detected] | [How detected] |
| [timestamp] | [Remediation action 1] | [Who/what] |
| [timestamp] | [Resolution] | |

---

## 3. Root Cause Analysis

### Root Cause
[Detailed explanation with evidence]

### Evidence Chain
1. [Evidence A] proves [Connection 1]
2. [Connection 1] leads to [Connection 2]
3. [Connection 2] caused [Symptom X]

### Contributing Factors
- [Factor 1]: [How it amplified impact]
- [Factor 2]: [How it delayed detection/resolution]

### Why It Happened
[Contextual explanation]

---

## 4. Impact Assessment

### Systems Affected
| System | Severity | Details |
|--------|----------|---------|
| [System 1] | Critical | [Impact details] |
| [System 2] | Major | [Impact details] |

### Data Impact
- **Corrupted:** [X records in Y table]
- **Lost:** [A records, recoverable from backup]
- **Exposed:** [None/B records, details]

### User Impact
- **Affected Users:** [N users]
- **Error Rate:** [X%]
- **Duration:** [Y minutes]

### Business Impact
- **Revenue:** [Impact if applicable]
- **Regulatory:** [Reportable incident? Yes/No]
- **Reputational:** [Customer complaints, media attention]

---

## 5. Remediation & Prevention

### Immediate Fix
[What was done to stop the incident]

**Status:** [Deployed/Tested/Pending]

### Long-Term Fix
[Permanent solution addressing root cause]

**Implementation Plan:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Timeline:** [When fix will be deployed]

### Prevention Measures
- [ ] [New alert for early detection]
- [ ] [Circuit breaker to prevent cascade]
- [ ] [Rate limit to prevent overload]
- [ ] [Monitoring improvement]

### Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| [Action 1] | [Name] | [Date] | [Pending/In Progress/Done] |
| [Action 2] | [Name] | [Date] | [Pending/In Progress/Done] |

---

## Appendix

### Evidence References
1. [Log excerpt A] - [Location]
2. [Metrics screenshot] - [Dashboard URL]
3. [Configuration diff] - [Git commit]

### Reproduction Steps
[Steps to reproduce in test environment, if applicable]

### References
- [Incident ticket]
- [Related past incidents]
- [External documentation]

---

**Postmortem Author:** [Generated by Forensic TOOLSPEC v1.0]  
**Review Status:** [Pending Review/Reviewed/Approved]
```

### Generation Process

1. **Extract data from progress_Forensic.json:**
   - Timeline entries from Task 2
   - Root cause from Task 3
   - Blast radius from Task 4
   - Remediation from Task 5

2. **Populate template sections:**
   - Use actual data, not placeholders
   - Include specific numbers (users affected, error rates)
   - Link evidence to claims

3. **Validate completeness:**
   - All 5 main sections present
   - No "TBD" or "[Insert X]" placeholders
   - Evidence references are specific (not "see logs")

4. **Save postmortem file:**
   - Filename: `postmortem_YYYYMMDD_HHMM.md`
   - Location: Same directory as progress.json
   - Log file path to progress.json

### Postmortem Quality Check

Before completing Section 6.7:
- [ ] Executive summary fits on one screen
- [ ] Timeline has at least 5 entries
- [ ] Root cause is single sentence
- [ ] Evidence supports root cause
- [ ] Impact is quantified (not "many users")
- [ ] Remediation is actionable (not "improve monitoring")
- [ ] Action items have owners and deadlines

If quality check fails: escalate to collaborative mode for human review/completion.

---

## Integration with Standard Execution

**Forensic execution flow:**

```
0. Incident Context Gathering (Forensic-specific)
   ↓
1. Initialization and Validation (standard, Section 1)
   ↓
2. Execution Flow (standard, Section 2)
   ├─ Evidence Preservation Checkpoint (2.8, before Task 1.1)
   ├─ Task 1 → Evidence Gathering
   ├─ Task 2 → Timeline Reconstruction
   ├─ Task 3 → Root Cause Analysis
   ├─ Task 4 → Blast Radius Assessment
   └─ Task 5 → Remediation & Prevention
   ↓
3. Mode Control (standard, Section 3)
   ↓
4. Error Handling (standard, Section 4)
   ↓
5. Completion (standard, Section 5)
   ↓
6. Post-Execution Analysis (standard, Section 6)
   ↓
6.7 Postmortem Report Generation (Forensic-specific)
```

**All standard sections from exe_template.md apply unless explicitly overridden above.**

---

## Reference Documents

- **Standard Execution Logic:** `__SPEC_Engine/_templates/exe_template.md`
- **SPEC Definition:** `Forensic_SPEC.md`
- **Parameters:** `parameters_Forensic.toml`
- **Constitution:** `__SPEC_Engine/_Constitution/constitution.md`

---

**End of exe_Forensic.md**

*This execution controller implements Forensic-specific investigation logic while inheriting standard SPEC Engine execution patterns. For complete execution details, consult exe_template.md.*
