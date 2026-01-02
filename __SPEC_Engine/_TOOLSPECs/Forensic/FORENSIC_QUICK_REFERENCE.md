# Forensic TOOLSPEC - Quick Reference Guide

**Root Cause Investigation** - Systematic forensic analysis for critical incidents

---

## When to Use Forensic

Use this TOOLSPEC when:
- Production system crashed or became unavailable
- Data corruption or loss occurred
- Security breach or unauthorized access detected
- Cascading failures across multiple systems
- Critical performance degradation (>10x slowdown)
- Financial loss or regulatory incident requiring investigation

**Don't use Forensic when:**
- Minor bugs need fixing → Use **Troubleshoot** instead
- Code is mysterious but no incident → Use **WTF** instead
- Issue is not critical/production → Use **Troubleshoot** or **Dev_Analysis**

---

## Quick Start

### 1. Gather Incident Context

Before starting, collect:
- **What failed?** (specific system/service)
- **When?** (timestamp in UTC if possible)
- **Observed symptoms?** (errors, symptoms, user complaints)
- **Current status?** (still failing, mitigated, resolved)
- **Evidence locations?** (log paths, metrics dashboards)

### 2. Preserve Evidence IMMEDIATELY

**CRITICAL:** Before any remediation:
```bash
# Create evidence archive
mkdir evidence_$(date +%Y%m%d_%H%M%S)

# Copy all logs
cp -rp /var/log/app/* evidence_*/logs/
cp /etc/app/config.yaml evidence_*/config/

# Generate checksums
find evidence_* -type f -exec sha256sum {} \; > evidence_checksums.txt
```

**Why:** Remediation destroys evidence (log rotation, restarts, config changes)

### 3. Launch Forensic Executor

```bash
cd __SPEC_Engine/_TOOLSPECs/Forensic
# AI will prompt for incident context
```

---

## What Forensic Produces

### Primary Deliverable: Postmortem Report

Structured markdown including:

#### 1. Executive Summary
```markdown
**Incident:** API gateway exhausted database connections
**Impact:** 1,247 users, 23 minutes, no data loss
**Root Cause:** Connection pool size (20) insufficient for traffic spike
**Status:** Resolved - pool increased to 100, monitoring added
```

#### 2. Timeline
```
14:27 - Normal operation (19 active connections)
14:28 - Traffic spike begins (user promotion email sent)
14:30 - Connection pool exhausted, 500 errors begin
14:32 - Incident detected via PagerDuty alert
14:35 - Emergency restart (temporary relief)
14:42 - Pool size increased to 100 (permanent fix)
14:50 - System stable, incident resolved
```

#### 3. Root Cause Analysis
```markdown
**Root Cause:** Database connection pool size (20) was insufficient for traffic spikes

**Evidence Chain:**
1. Logs show connection pool exhaustion at 14:30:15
2. Traffic metrics show 5x normal load from 14:28
3. Database connections maxed at 20 (config value)
4. Error rate correlated 1:1 with pool exhaustion

**Contributing Factors:**
- No connection timeout configured (connections held indefinitely)
- No rate limiting on API endpoints
- Alert threshold (50 errors/min) too high for early detection
```

#### 4. Impact Assessment
```markdown
**Systems:** API Gateway (critical), User Service (major), Notification Service (minor)
**Data:** No corruption or loss
**Users:** 1,247 affected, 87% error rate during peak, 23 min duration
**Business:** Minimal - non-revenue endpoint, no regulatory reportability
```

#### 5. Remediation & Prevention
```markdown
**Immediate:** Increased pool to 100, added connection timeout (60s)
**Long-term:** Implement circuit breaker, auto-scaling for connection pool
**Prevention:**
- Alert on 90% pool utilization (early warning)
- Rate limit endpoints at 1000 req/min per user
- Load testing with 10x normal traffic
```

---

## The 5-Task Investigation Process

### Task 1: Evidence Gathering (30 min)
**Critical:** Preserve before remediation!

**Collect:**
- System logs (app, database, web server, network)
- Error messages and stack traces
- Environment state (versions, config)
- Metrics (CPU, memory, connections)

### Task 2: Timeline Reconstruction (45 min)
**Goal:** Chronological sequence of events

**Output:**
- Incident start time (precise)
- Trigger event identified
- Failure cascade mapped
- Detection time noted

### Task 3: Root Cause Analysis (60 min)
**Goal:** Fundamental cause identification

**Process:**
- Generate hypotheses (5 Whys, Fishbone)
- Test against evidence
- Reproduce if possible
- Confirm with proof

### Task 4: Blast Radius Assessment (30 min)
**Goal:** Quantify full impact

**Measure:**
- Systems affected (with severity)
- Data impact (specific counts)
- User impact (numbers, not "many")
- Business impact (financial, regulatory)

### Task 5: Remediation & Prevention (60 min)
**Goal:** Fix and prevent recurrence

**Deliverables:**
- Immediate fix (already deployed?)
- Long-term fix (permanent solution)
- Prevention measures (alerts, safeguards)
- Action items (owners, deadlines)

**Total Time:** ~4 hours for thorough investigation

---

## Investigation Best Practices

### 1. Preserve Evidence First
❌ "Let me restart and see what happens"  
✅ "Copy all logs, then restart"

### 2. Follow the Evidence
❌ "I think it's the database"  
✅ "Logs show connection timeouts at 14:30, let's check database connections"

### 3. Quantify Everything
❌ "Many users were affected"  
✅ "1,247 users saw errors (87% of active users)"

### 4. Distinguish Root Cause from Symptoms
❌ Root Cause: "API returned 500 errors"  
✅ Root Cause: "Connection pool exhausted due to undersized configuration"

### 5. Make Remediation Actionable
❌ "Improve monitoring"  
✅ "Add alert: connection_pool_utilization > 90% for 1 minute → PagerDuty"

---

## Root Cause vs Contributing Factors

**Root Cause:** If eliminated, incident would NOT have occurred

**Contributing Factor:** Amplified impact or delayed detection/resolution

**Example:**
- **Root Cause:** Memory leak in authentication service
- **Contributing Factors:**
  - No memory limit configured (allowed leak to consume all RAM)
  - No automated restarts (service stayed down)
  - Alert threshold too high (detected late)

**Test:** "If we only fix the root cause, will this incident recur?"
- If YES → you haven't found the root cause yet
- If NO → correct root cause identified

---

## Common Forensic Scenarios

### Scenario A: Crash (Service Down)
**Evidence:** Core dumps, logs before crash, system resources
**Focus:** What was different? (code changes, config, load, dependencies)
**Timeline:** Build backwards from crash to trigger

### Scenario B: Data Corruption
**Evidence:** Database logs, transaction history, data samples
**Focus:** When did corruption start? What writes occurred?
**Timeline:** Compare good data vs corrupted data timestamps

### Scenario C: Security Breach
**Evidence:** Access logs, authentication logs, network logs
**Focus:** Entry point, lateral movement, data exfiltration
**Timeline:** First unauthorized access to last activity

### Scenario D: Performance Degradation
**Evidence:** Metrics (CPU, memory, I/O), slow query logs, traces
**Focus:** What changed? Resource exhaustion? N+1 queries?
**Timeline:** When performance started degrading

---

## Validation Checkpoints

After each task:

**Task 1:** Do I have all relevant evidence preserved?  
**Task 2:** Can I explain the sequence of events confidently?  
**Task 3:** Is root cause supported by evidence (not speculation)?  
**Task 4:** Are all impact numbers specific and verified?  
**Task 5:** Are remediation steps actionable with owners/deadlines?

If **NO** to any: return to that task with deeper analysis.

---

## Postmortem Report Quality

A good postmortem:
- ✅ Tells a clear story (anyone can understand what happened)
- ✅ Has specific numbers (not "many", "several", "significant")
- ✅ Links every claim to evidence
- ✅ Distinguishes facts from speculation
- ✅ Provides actionable next steps
- ✅ Is blameless (focuses on systems, not people)

A bad postmortem:
- ❌ Uses vague language ("system had issues")
- ❌ Speculates without evidence ("probably a memory leak")
- ❌ Blames individuals ("Bob deployed bad code")
- ❌ Has no action items or timeline
- ❌ Leaves gaps unexplained ("then somehow it recovered")

---

## FAQ

**Q: How long does Forensic take?**
A: 2-6 hours depending on incident complexity:
- Simple (single system failure): 2-3 hours
- Moderate (cascade across systems): 3-5 hours
- Complex (security breach, data corruption): 5-6+ hours

**Q: What if I can't determine root cause?**
A: Document "most likely root cause" with confidence level and why it's uncertain. Better to admit uncertainty than fabricate false certainty.

**Q: Can I do forensics after remediation is done?**
A: Yes, but evidence may be lost (rotated logs, restarted systems). Always prefer preserving evidence first.

**Q: What if evidence was already destroyed?**
A: Work with what you have. Document evidence gaps explicitly. Interview engineers who responded.

**Q: Should I include sensitive information in postmortem?**
A: Redact credentials, customer data, financial specifics. Focus on technical details.

---

## Related TOOLSPECs

- **Troubleshoot:** Non-critical issues needing fixes
- **WTF:** Understanding mysterious but working code
- **Dev_Analysis:** Planning system changes
- **Security:** Proactive security assessment

---

## Support Files

- **Full Specification:** `Forensic_SPEC.md`
- **Configuration:** `parameters_Forensic.toml`
- **Execution Controller:** `exe_Forensic.md`
- **Progress Log:** `progress_Forensic.json` (generated)
- **Knowledge Capture:** `notepad_Forensic.md` (generated)
- **Postmortem Report:** `postmortem_YYYYMMDD_HHMM.md` (generated)

---

**Last Updated:** 2 January 2026  
**TOOLSPEC Version:** 1.0  
**Part of:** Constitutional Slow-Code Engine v2.0
