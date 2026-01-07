# An In-Depth Study of the Promises and Perils of Mining GitHub

**Authors:** Eirini Kalliamvakou, Georgios Gousios, Kelly Blincoe, Leif Singer, Daniel M. German, Daniela Damian

**Published:** September 2016  
**Journal:** Empirical Software Engineering, Vol 21(5): pp. 2035-2071  
**DOI:** https://doi.org/10.1007/s10664-015-9393-5  
**PDF:** http://thesegalgroup.org/wp-content/uploads/2015/10/EMSE.pdf

---

## Executive Summary

This paper documents the results of an empirical study aimed at understanding the characteristics of GitHub repositories and users. It highlights critical **misalignments between real activity and mined data** that researchers must consider when using GitHub for empirical software engineering research.

---

## Key Findings

### 1. Repository Characteristics

**The Majority of Projects Are Personal and Inactive**

- Most GitHub repositories are personal projects
- High proportion of inactive repositories
- Only a small percentage are active, collaborative projects

**Implication for Your Work:**
- Quality filtering is essential (you already have this with quality_score)
- Star count and activity metrics help identify serious projects
- Need to distinguish between toy projects and production code

### 2. Pull Request Anomaly

**~40% of Merged Pull Requests Don't Appear as Merged**

- Pull requests can be integrated without using GitHub's merge button
- Developers often merge manually via git command line
- GitHub's API doesn't reflect actual merge status

**Critical Insight:**
- Relying solely on GitHub's "merged" flag gives false negatives
- Need to check commit history, not just PR status
- Your pattern extraction correctly focuses on actual code, not PR metadata

### 3. User Activity Tracking Issues

**Approximately 50% of Registered Users Have No Public Activity**

- Many accounts are inactive or observers
- Actual contributors are a small subset
- Activity tracking is not always straightforward

**Application to Your Pipeline:**
- Focus on repositories with commits, not just stars
- Quality metrics should include commit frequency
- Your `extracted_at` timestamp helps track actual activity

### 4. Repository Usage Patterns

**GitHub Used for Non-Software-Development Purposes**

- Documentation repositories
- Data storage
- Personal note-taking
- Course materials

**Your Advantage:**
- Focusing on GraphRAG/knowledge-graph topic ensures code repositories
- Star threshold filters out trivial repos
- LLM-based analysis can detect actual architectural patterns

---

## Identified Perils (Validity Threats)

### Peril 1: Project Maturity Misrepresentation

**Issue:** Many repositories appear active but are early-stage experiments

**Mitigation in Your Pipeline:**
- Quality scoring system (PatternCritic + QualityJudge)
- Star count as popularity proxy
- README and structure analysis

### Peril 2: Collaboration Misidentification

**Issue:** Not all multi-contributor projects are truly collaborative

**Examples:**
- Course projects with student contributions
- Forked repos with minimal changes
- Bot-generated commits

**Your Protection:**
- Analyzing actual code structure, not commit counts
- Pattern validation through multiple criteria
- Focus on architectural patterns, not contributor metrics

### Peril 3: Activity Metrics Unreliability

**Issue:** Commit counts, PR numbers don't reflect real development activity

**Problems:**
- Bulk commits skew metrics
- Merge commits inflate numbers
- Bot activity counted as human

**Your Approach:**
- Analyzing final code state, not development process
- Quality-based filtering
- Structural analysis over activity metrics

### Peril 4: Language and Framework Misclassification

**Issue:** GitHub's language detection can be inaccurate

**Your Solution:**
- LLM analyzes actual code content
- Dependency files provide ground truth
- Topic tags offer additional context

---

## Recommendations for Researchers (Applied to Your Work)

### 1. Be Explicit About Data Selection

**Paper's Advice:** Document exactly what you're mining and why

**Your Implementation:**
- Query strings clearly defined
- Star thresholds documented
- Quality scoring transparent
- Trajectory logging tracks everything

### 2. Validate Assumptions

**Paper's Advice:** Don't assume GitHub data is ground truth

**Your Implementation:**
- PatternCritic validates extracted patterns
- QualityJudge provides independent assessment
- Multiple data sources (README, structure, dependencies)

### 3. Filter Aggressively

**Paper's Advice:** Most repos shouldn't be in your dataset

**Your Implementation:**
- Star count minimum (e.g., >100, >500)
- Topic filtering (knowledge-graph, rag)
- Quality score thresholds
- Active skip logic for already-analyzed repos

### 4. Be Cautious with Automated Metrics

**Paper's Advice:** PR counts, commit counts can mislead

**Your Implementation:**
- Focus on architectural patterns, not metrics
- Qualitative analysis via LLM
- Multi-faceted quality assessment

---

## Validation Checklist (For Your Pipeline)

Based on the paper's identified issues, validate your approach:

- [x] **Project Selection Criteria:** Documented (stars, topics, query strings)
- [x] **Quality Assessment:** Multi-stage (quality_score, validation_score, judge_score)
- [x] **Activity Verification:** Actual code analysis, not just GitHub metrics
- [x] **Data Provenance:** Trajectory logging tracks all decisions
- [x] **Duplicate Detection:** Implemented to handle re-analysis correctly
- [x] **Ground Truth:** LLM analyzes actual code, not just metadata

---

## Specific Threats Avoided

### Threat 1: Sampling Bias

**Risk:** Only analyzing popular repos misses ecosystem diversity

**Your Mitigation:**
- Multiple query strategies
- Range of star thresholds (>100 to >5000)
- Topic-based discovery, not just popularity

### Threat 2: Temporal Validity

**Risk:** GitHub data changes rapidly; old analyses become stale

**Your Mitigation:**
- Timestamp tracking (`extracted_at`)
- Force re-analyze option for updates
- Monthly/weekly refresh planned

### Threat 3: False Negatives

**Risk:** Missing relevant repos due to poor tagging

**Your Mitigation:**
- Multiple search strategies (topics, README, description)
- Query refinement when results insufficient
- Broad initial queries, then filter

### Threat 4: False Positives

**Risk:** Including toy projects or irrelevant repos

**Your Mitigation:**
- Star threshold
- Quality scoring
- LLM validates actual patterns present
- Human-like pattern critic

---

## Key Statistics from Paper

| Metric | Finding | Implication |
|--------|---------|-------------|
| Inactive Projects | Majority | Need activity filtering |
| Merged PRs Not Marked | ~40% | Don't rely on PR status |
| Users Without Activity | ~50% | Focus on repos, not users |
| Personal Projects | High % | Need collaboration indicators |

---

## Actionable Insights for Your Work

### 1. Strengthen Quality Filtering

The paper validates your multi-stage quality assessment:
- Initial quality check (0-1 score)
- Pattern validation (critic)
- Final evaluation (judge)

**Recommendation:** Keep all three stages; each catches different issues.

### 2. Track Metadata Comprehensively

The paper shows metadata matters:
- Stars (popularity proxy)
- Last update (activity indicator)
- Contributors (collaboration indicator)
- Fork status (originality indicator)

**Current Status:** You track stars, quality, extracted_at. Consider adding:
- Last commit date
- Contributor count
- Fork parent (if applicable)

### 3. Document Limitations

The paper emphasizes transparency about:
- What data is excluded and why
- Known biases in selection
- Potential validity threats

**Action Item:** Create a `DATA_QUALITY.md` documenting:
- Query strategies and rationale
- Filtering criteria
- Known limitations
- Validation approach

### 4. Version Your Dataset

GitHub data changes; your analysis should be reproducible:
- [x] Timestamp all extractions (`extracted_at`)
- [x] Track analysis version (trajectory logs)
- [ ] Consider adding git commit hash from analyzed repos
- [ ] Archive query results for reproducibility

---

## Comparison: Paper's Warnings vs. Your Defenses

| Warning | Your Defense | Status |
|---------|-------------|---------|
| Personal/inactive projects | Star threshold + quality score | Strong |
| PR status unreliable | Analyze actual code, not PRs | Excellent |
| User activity misleading | Focus on repo patterns | Excellent |
| Metadata inaccurate | LLM validates actual content | Strong |
| Temporal staleness | Timestamp + re-analyze option | Strong |
| Selection bias | Multiple query strategies | Good |

---

## Research Validity Framework

The paper provides a framework for evaluating mining studies. Apply to your pipeline:

### Internal Validity
- **Threat:** Did you measure what you intended?
- **Your Approach:** LLM extracts actual patterns, not proxies
- **Rating:** Strong

### External Validity  
- **Threat:** Do results generalize beyond your sample?
- **Your Approach:** Multiple queries, broad topic coverage
- **Rating:** Good (can improve with more diverse queries)

### Construct Validity
- **Threat:** Do your metrics represent the concepts?
- **Your Approach:** Quality score validated by critic and judge
- **Rating:** Strong

### Conclusion Validity
- **Threat:** Are your conclusions statistically justified?
- **Your Approach:** Qualitative analysis, not statistical claims
- **Rating:** Appropriate for exploratory research

---

## Recommended Reading Strategy

For implementing recommendations from this paper:

1. **Read Section 3:** "Characteristics of GitHub" - Understand the data landscape
2. **Read Section 4:** "Promises and Perils" - Learn specific pitfalls
3. **Read Section 6:** "Recommendations" - Apply to your pipeline
4. **Skim Section 7:** "Validity Analysis" - See examples from MSR 2014

---

## Key Takeaway

This paper validates your cautious, multi-stage approach to analyzing GitHub data. The perils identified (inactive projects, metadata unreliability, hidden biases) are exactly what your quality scoring, LLM validation, and trajectory logging are designed to mitigate.

**Your pipeline's architecture shows you've internalized these lessons—intentionally or not.**

---

## Citation

```bibtex
@article{kalliamvakou2016github,
  title={An in-depth study of the promises and perils of mining GitHub},
  author={Kalliamvakou, Eirini and Gousios, Georgios and Blincoe, Kelly and Singer, Leif and German, Daniel M and Damian, Daniela},
  journal={Empirical Software Engineering},
  volume={21},
  number={5},
  pages={2035--2071},
  year={2016},
  publisher={Springer}
}
```

---

## Resources

- **Paper PDF:** http://thesegalgroup.org/wp-content/uploads/2015/10/EMSE.pdf
- **DOI:** https://doi.org/10.1007/s10664-015-9393-5
- **Publisher:** Springer - Empirical Software Engineering Journal
