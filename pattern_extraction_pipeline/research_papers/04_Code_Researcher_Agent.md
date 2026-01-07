# Code Researcher: Deep Research Agent for Large Systems Code and Commit History

**Authors:** Ramneet Singh, Sathvik Joel, Abhav Mehrotra, Nalin Wadhwa, Ramakrishna Bairi, Aditya Kanade, Nagarajan Natarajan

**Published:** Microsoft Research Technical Report MSR-TR-2025-34, June 2025  
**ArXiv:** https://arxiv.org/abs/2506.11060  
**Microsoft Research:** https://www.microsoft.com/en-us/research/publication/code-researcher-deep-research-agent-for-large-systems-code-and-commit-history/

---

## Overview

Code Researcher is the **first deep research agent designed specifically for large systems code and commit history**. It performs multi-step reasoning about code semantics, patterns, and commit history to synthesize patches for mitigating crashes in systems code.

---

## The Problem

### Challenge: Systems Code Complexity

Large codebases like the Linux kernel require extensive research before making changes:
- Navigate massive codebases (millions of lines)
- Understand complex code semantics
- Analyze commit history patterns
- Reason across multiple files and components

**Even for humans, this is daunting.** Existing LLM coding agents struggle with systems code due to size and complexity.

### Current Agent Limitations

LLM-based coding agents show promise on benchmarks but:
- Focus on small, isolated tasks
- Lack deep exploration capabilities
- Don't leverage commit history effectively
- Can't gather sufficient context from large codebases

---

## Code Researcher Architecture

### Core Innovation: Multi-Step Deep Research

Code Researcher performs **multi-step reasoning** before generating patches:

1. **Code Semantics Analysis**
   - Understand function purposes
   - Identify data flow patterns
   - Map component interactions

2. **Pattern Recognition**
   - Detect common error patterns
   - Identify fix patterns from history
   - Recognize architectural patterns

3. **Commit History Mining**
   - Learn from previous fixes
   - Understand code evolution
   - Identify change patterns

4. **Context Gathering**
   - Explore related files systematically
   - Build comprehensive understanding
   - Store findings in structured memory

5. **Patch Synthesis**
   - Use gathered context to generate fixes
   - Apply learned patterns
   - Validate against semantics

### Structured Memory System

Code Researcher maintains structured memory containing:
- Discovered code patterns
- Relevant commit history
- Semantic relationships
- File dependencies

This memory informs patch generation.

---

## Evaluation Results

### Benchmark: kBenchSyz

**Dataset:** Linux kernel crashes from syzkaller fuzzer

**Results:**

| System | Crash Resolution Rate |
|--------|----------------------|
| Code Researcher | **58%** |
| SWE-agent (baseline) | 37.5% |

**Improvement:** +54.7% relative improvement over strong baseline

### Deep Exploration Metrics

**Average Files Explored Per Trajectory:**
- Code Researcher: **10 files**
- SWE-agent: 1.33 files

**Insight:** Code Researcher explores 7.5x more files, gathering comprehensive context before generating patches.

### Generalizability

Tested on additional open-source multimedia software:
- Successfully resolved crashes
- Demonstrated domain transfer
- Validated multi-faceted reasoning approach

---

## Key Technical Contributions

### 1. Global Context Gathering

Unlike agents that work locally, Code Researcher:
- Systematically explores the entire codebase
- Identifies distant dependencies
- Understands global architectural patterns

### 2. Multi-Faceted Reasoning

Combines multiple reasoning strategies:
- **Semantic reasoning**: What does this code do?
- **Pattern reasoning**: What patterns apply here?
- **Historical reasoning**: How was this fixed before?

### 3. Structured Memory

Organizes discovered information:
- Not just raw text retrieval
- Structured representation of findings
- Enables complex reasoning over context

### 4. Commit History Integration

Learns from repository evolution:
- Previous fix patterns
- Change patterns over time
- Evolution of architectural patterns

---

## Relevance to Your Pattern Extraction Pipeline

### Direct Parallels

| Code Researcher | Your Pipeline |
|----------------|---------------|
| Multi-step code analysis | Multi-stage pattern extraction |
| Structured memory | Neo4j knowledge graph |
| Context gathering | Repository structure analysis |
| Pattern recognition | Pattern naming & categorization |
| Commit history mining | Could add: pattern evolution tracking |

### Architectural Similarities

1. **Deep Exploration**
   - Code Researcher explores 10 files per task
   - Your pipeline analyzes README, structure, dependencies

2. **Structured Knowledge**
   - Code Researcher uses structured memory
   - You use Neo4j graph with relationships

3. **Multi-Stage Reasoning**
   - Code Researcher: semantics → patterns → history → patch
   - You: quality → critic → judge → validation

4. **Context is Everything**
   - Code Researcher: "global context gathering" is critical
   - You: Cross-repository pattern understanding is key

---

## Lessons for Your Pattern Extraction

### 1. Exploration Depth Matters

**Code Researcher's Success Factor:** Exploring 10 files vs 1.33 files

**Application to Your Work:**
- Don't just analyze entry points
- Explore dependencies deeply
- Follow architectural breadcrumbs
- Map relationships between components

**Current Status:** You analyze multiple sources (README, structure, dependencies)  
**Enhancement:** Could trace imports/dependencies more deeply

### 2. Commit History is Goldmine

**Code Researcher's Insight:** Commit history reveals patterns

**Application to Your Work:**
- Track pattern evolution over time
- When did pattern first appear?
- How has it changed?
- What patterns replaced what?

**Future Feature:** Add commit history analysis to pattern extraction

### 3. Structured Memory Enables Reasoning

**Code Researcher's Approach:** Organize findings in structured memory

**Your Implementation:** Neo4j provides this structure
- Patterns as nodes
- Relationships as edges
- Properties as attributes
- Queries as reasoning

**Validation:** Your architecture already implements this principle

### 4. Multi-Step is Better Than One-Shot

**Code Researcher's Design:** Multiple reasoning steps before action

**Your Pipeline Stages:**
1. Repository discovery
2. Quality assessment
3. Pattern extraction (LLM)
4. Pattern validation (Critic)
5. Quality evaluation (Judge)
6. Graph storage

**Insight:** Your multi-stage approach aligns with Code Researcher's philosophy

---

## Potential Enhancements Inspired by Code Researcher

### 1. Add Commit History Analysis

**Feature:** Analyze git history of analyzed repositories

**Benefits:**
- Track pattern emergence
- Understand pattern evolution
- Identify pattern adoption speed
- Map architectural changes

**Implementation:**
```python
def analyze_commit_history(self, repo):
    # Get commits related to pattern files
    # Extract architectural changes
    # Track pattern evolution
    # Store in Neo4j with temporal edges
```

### 2. Deep Dependency Tracing

**Feature:** Follow imports/dependencies multiple levels deep

**Benefits:**
- Understand complete architectural context
- Identify hidden dependencies
- Map pattern relationships
- Discover dependency patterns

**Implementation:**
- Parse import statements
- Trace to source files
- Analyze dependencies recursively
- Build dependency graph

### 3. Pattern Evolution Tracking

**Feature:** Track how patterns change across versions

**Benefits:**
- Understand architectural trends
- Predict pattern futures
- Identify improving vs declining patterns

**Implementation:**
- Store pattern snapshots over time
- Compare pattern versions
- Identify evolutionary trajectories

### 4. Cross-Repository Pattern Flow

**Feature:** Track how patterns spread between repositories

**Benefits:**
- Understand pattern adoption
- Identify influential repositories
- Map knowledge transfer

**Implementation:**
- Compare patterns across repos
- Identify similar patterns
- Track temporal relationships
- Build diffusion graph

---

## Code Researcher's Success Factors Applied

### Success Factor 1: Deep Exploration

**Code Researcher:** 10 files explored  
**Your Pipeline:** Multiple data sources analyzed  
**Enhancement:** Could increase file exploration depth

### Success Factor 2: Multi-Faceted Reasoning

**Code Researcher:** Semantics + Patterns + History  
**Your Pipeline:** Quality + Validation + Evaluation  
**Status:** Already implemented

### Success Factor 3: Structured Knowledge

**Code Researcher:** Structured memory system  
**Your Pipeline:** Neo4j knowledge graph  
**Status:** Already implemented

### Success Factor 4: Global Context

**Code Researcher:** Codebase-wide understanding  
**Your Pipeline:** Ecosystem-wide pattern understanding  
**Enhancement:** Could add more cross-repository analysis

---

## Research Methodology Lessons

### 1. Strong Baseline Comparison

Code Researcher compares against SWE-agent, a strong baseline:
- Shows meaningful improvement (+54.7%)
- Validates approach against state-of-art

**Application:** When evaluating your patterns:
- Compare against baseline extraction (no LLM)
- Measure quality improvements
- Validate multi-stage vs single-stage

### 2. Multiple Evaluation Dimensions

Code Researcher measures:
- Resolution rate (success metric)
- File exploration (depth metric)
- Generalizability (transfer test)

**Application:** Evaluate your pipeline on:
- Pattern quality scores
- Coverage metrics (files analyzed)
- Generalizability (different domains)

### 3. Ablation Studies

Code Researcher likely tested:
- With vs without commit history
- With vs without structured memory
- Deep vs shallow exploration

**Application:** Test your pipeline:
- With vs without Critic
- With vs without Judge
- Single LLM call vs multi-stage

---

## Key Takeaways

### 1. Systems-Level Thinking Required

Code Researcher succeeds because it thinks at **system level**, not file level.

**Your Parallel:** Pattern extraction needs **ecosystem-level thinking**, not just repository level.

### 2. Context > Cleverness

58% resolution from gathering comprehensive context, not sophisticated algorithms.

**Your Parallel:** Your multi-source extraction (README + structure + dependencies) provides context that single-source can't.

### 3. Memory Enables Intelligence

Structured memory allows Code Researcher to reason over findings.

**Your Parallel:** Neo4j graph enables complex pattern queries and relationship reasoning.

### 4. History Informs Future

Commit history analysis provides patterns for fixing current issues.

**Your Parallel:** Pattern history could inform future architectural decisions.

---

## Future Research Directions

Inspired by Code Researcher:

1. **Temporal Pattern Analysis**
   - How do patterns evolve?
   - What patterns are emerging?

2. **Cross-Repository Learning**
   - Which patterns spread fastest?
   - What makes patterns adoptable?

3. **Pattern Recommendation**
   - Given a codebase, suggest patterns
   - Based on similar repositories

4. **Architectural Debt Detection**
   - Identify anti-patterns
   - Suggest refactoring paths

---

## Implementation Priority

High-impact enhancements from Code Researcher's approach:

**High Priority:**
1. ✅ Multi-stage reasoning (already implemented)
2. ✅ Structured knowledge storage (Neo4j)
3. 🔲 Commit history analysis (major enhancement)

**Medium Priority:**
4. 🔲 Deep dependency tracing
5. 🔲 Pattern evolution tracking

**Low Priority (Future):**
6. 🔲 Cross-repository flow analysis
7. 🔲 Pattern recommendation system

---

## Conclusion

Code Researcher validates your architectural choices:
- ✅ Multi-stage processing
- ✅ Structured knowledge representation
- ✅ Comprehensive context gathering

Its success (58% vs 37.5%) comes from the same principles your pipeline embodies: **deep exploration, structured memory, and multi-faceted reasoning**.

The key enhancement opportunity: **Add commit history analysis** to understand pattern evolution.

---

## Resources

- **ArXiv:** https://arxiv.org/abs/2506.11060
- **Microsoft Research:** https://www.microsoft.com/en-us/research/publication/code-researcher-deep-research-agent-for-large-systems-code-and-commit-history/
- **Technical Report:** MSR-TR-2025-34

---

## Citation

```bibtex
@techreport{singh2025coderesearcher,
  title={Code Researcher: Deep Research Agent for Large Systems Code and Commit History},
  author={Singh, Ramneet and Joel, Sathvik and Mehrotra, Abhav and Wadhwa, Nalin and Bairi, Ramakrishna and Kanade, Aditya and Natarajan, Nagarajan},
  year={2025},
  institution={Microsoft Research},
  number={MSR-TR-2025-34}
}
```
