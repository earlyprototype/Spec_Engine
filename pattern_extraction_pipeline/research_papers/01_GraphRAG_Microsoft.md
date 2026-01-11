# GraphRAG - Microsoft Research

**Source:** https://microsoft.github.io/graphrag/  
**GitHub:** https://github.com/microsoft/graphrag  
**Paper:** https://arxiv.org/pdf/2404.16130  
**Date Accessed:** January 2026

---

## Overview

GraphRAG is a structured, hierarchical approach to Retrieval Augmented Generation (RAG), as opposed to naive semantic-search approaches using plain text snippets. The GraphRAG process involves extracting a knowledge graph out of raw text, building a community hierarchy, generating summaries for these communities, and then leveraging these structures when performing RAG-based tasks.

## Key Innovation

GraphRAG uses knowledge graphs to provide substantial improvements in question-and-answer performance when reasoning about complex information, particularly for private datasets that LLMs have never seen before.

---

## The Problem with Baseline RAG

Traditional RAG (using vector similarity search) struggles in two key scenarios:

1. **Connecting the Dots**: Baseline RAG fails when answering questions requires traversing disparate pieces of information through their shared attributes to provide new synthesized insights.

2. **Holistic Understanding**: Baseline RAG performs poorly when asked to understand summarized semantic concepts over large data collections or even singular large documents.

---

## The GraphRAG Process

### Indexing Phase

1. **Text Chunking**
   - Slice input corpus into `TextUnits`
   - These serve as analyzable units and provide fine-grained references

2. **Entity & Relationship Extraction**
   - Extract all entities, relationships, and key claims from TextUnits
   - Build comprehensive knowledge graph

3. **Hierarchical Clustering**
   - Use the Leiden algorithm for community detection
   - Create multi-level hierarchy of entity communities
   - Each entity (person, place, organization) assigned to communities

4. **Community Summarization**
   - Generate summaries bottom-up through the hierarchy
   - Aids holistic understanding of the dataset

### Query Phase

Four primary query modes:

1. **Global Search**
   - Reasoning about holistic questions about the corpus
   - Leverages community summaries
   - Best for high-level, overview questions

2. **Local Search**
   - Reasoning about specific entities
   - Fans out to neighbors and associated concepts
   - Best for detailed, entity-specific questions

3. **DRIFT Search**
   - Local search enhanced with community context
   - Combines entity-level and community-level information

4. **Basic Search**
   - Standard top-k vector search
   - For queries best answered by baseline RAG

### Prompt Tuning

GraphRAG includes prompt tuning capabilities to optimize performance for specific datasets:
- Auto-tuning functionality
- Manual tuning options
- Domain-specific customization

---

## Architecture Components

### Index Architecture
- **Inputs**: Text documents, structured data
- **Dataflow**: Multi-stage processing pipeline
- **Outputs**: Knowledge graph, community structure, embeddings
- **Custom Graphs**: Support for bring-your-own-graph (BYOG)

### Configuration
- YAML-based configuration system
- Language model selection (supports multiple LLM providers)
- Flexible initialization via CLI

---

## Relevance to Pattern Extraction Pipeline

### Direct Parallels

1. **Knowledge Graph Construction**
   - GraphRAG extracts entities/relationships from text
   - Your pipeline extracts patterns/dependencies from code

2. **Community Detection**
   - GraphRAG uses Leiden algorithm for hierarchical clustering
   - Could apply to pattern clustering by domain/similarity

3. **Quality Scoring**
   - GraphRAG validates extracted information
   - Similar to your PatternCritic/QualityJudge system

4. **Hierarchical Organization**
   - GraphRAG builds community hierarchies
   - Applicable to organizing patterns by abstraction level

### Potential Applications

1. **Pattern Querying**
   - Implement Global Search for "What architectural patterns exist in GraphRAG domain?"
   - Use Local Search for "Show me all patterns from repository X"

2. **Pattern Relationships**
   - Build knowledge graph of how patterns relate to each other
   - Track pattern evolution and dependencies

3. **Domain Clustering**
   - Apply Leiden algorithm to cluster similar patterns
   - Generate domain summaries from pattern clusters

4. **Multi-level Abstraction**
   - Low-level: Individual code patterns
   - Mid-level: Repository architectural patterns
   - High-level: Domain-wide pattern trends

---

## Technical Stack

- **Graph Processing**: Leiden algorithm for community detection
- **LLM Integration**: Supports multiple providers (OpenAI, Azure, local models)
- **Storage**: Parquet files for scalability
- **Embeddings**: Vector representations for semantic search
- **Query Engine**: Multiple search strategies

---

## Key Takeaways for Your Work

1. **Structured Knowledge Beats Flat Data**: GraphRAG proves that organizing information into a graph with hierarchical communities significantly outperforms flat vector search.

2. **Multi-Query Strategy**: Different question types need different search strategies (global vs local vs DRIFT).

3. **Community Summaries**: Pre-computed summaries at different abstraction levels enable efficient querying of large datasets.

4. **Prompt Engineering Matters**: GraphRAG emphasizes prompt tuning for domain-specific optimization.

5. **Validation is Critical**: The system validates extracted entities and relationships before graph construction.

---

## Implementation Considerations

If adapting GraphRAG concepts to your pattern extraction:

1. **Entities = Patterns**: Map code patterns to graph nodes
2. **Relationships = Dependencies**: Track how patterns depend on each other
3. **Communities = Domains**: Cluster patterns by architectural domain
4. **Summaries = Domain Overviews**: Generate high-level architectural insights
5. **Claims = Quality Metrics**: Extract and validate pattern quality indicators

---

## Resources

- Documentation: https://microsoft.github.io/graphrag/
- GitHub Repository: https://github.com/microsoft/graphrag
- Research Blog: https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/
- ArXiv Paper: https://arxiv.org/pdf/2404.16130

---

## Version Notes

GraphRAG is under active development with breaking changes between major versions. The team recommends:
- Running `graphrag init --root [path] --force` between minor version bumps
- Using provided migration notebooks between major version bumps
- Backing up configurations and prompts before updates
