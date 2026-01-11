// Vector Index Setup for Pattern Knowledge Graph
// Creates vector indexes for semantic search on Pattern nodes
//
// Requirements:
//   - Neo4j 5.x or later (vector index support)
//   - Pattern nodes with 'embedding' property (768-dimensional float array)
//
// Usage:
//   cypher-shell -u neo4j -p password < vector_index_setup.cypher
//   Or run in Neo4j Browser

// ============================================================================
// Check Neo4j Version (informational)
// ============================================================================

CALL dbms.components() YIELD name, versions, edition
WHERE name = 'Neo4j Kernel'
RETURN name, versions[0] AS version, edition;

// ============================================================================
// Create Vector Index on Pattern Embeddings
// ============================================================================

// Check if index already exists
SHOW INDEXES
YIELD name, type, labelsOrTypes, properties, state
WHERE name = 'pattern_embeddings'
RETURN name, type, state;

// Create vector index (idempotent - will fail gracefully if exists)
CREATE VECTOR INDEX pattern_embeddings IF NOT EXISTS
FOR (p:Pattern)
ON p.embedding
OPTIONS {
    indexConfig: {
        `vector.dimensions`: 768,
        `vector.similarity_function`: 'cosine'
    }
};

// ============================================================================
// Wait for Index to Come Online
// ============================================================================

// Wait for all indexes to be online (blocks until ready)
CALL db.awaitIndexes(300);

// Verify index status
SHOW INDEXES
YIELD name, type, labelsOrTypes, properties, state, populationPercent
WHERE name = 'pattern_embeddings'
RETURN name, type, state, populationPercent;

// ============================================================================
// Verify Pattern Node Schema
// ============================================================================

// Check how many patterns have embeddings
MATCH (p:Pattern)
RETURN count(p) AS total_patterns,
       count(p.embedding) AS with_embeddings,
       count(p) - count(p.embedding) AS missing_embeddings;

// Sample pattern with embedding
MATCH (p:Pattern)
WHERE p.embedding IS NOT NULL
RETURN p.name,
       size(p.embedding) AS embedding_dimensions,
       p.embedding_model,
       p.embedding_version,
       p.embedding_date
LIMIT 1;

// ============================================================================
// Test Vector Search (if patterns have embeddings)
// ============================================================================

// Note: This requires at least one pattern with embedding to work
// Run after generate_pattern_embeddings.py has been executed

// Test query - find patterns similar to a sample embedding
// (Replace $test_embedding with actual 768-dimensional vector)
//
// Example:
// :param test_embedding => [0.1, 0.2, ..., 0.05]  // 768 floats
//
// CALL db.index.vector.queryNodes('pattern_embeddings', 5, $test_embedding)
// YIELD node, score
// RETURN node.name AS pattern,
//        score AS similarity,
//        node.confidence AS confidence,
//        node.stars AS stars
// ORDER BY score DESC;

// ============================================================================
// Future: Additional Vector Indexes
// ============================================================================

// Requirement embeddings (for semantic requirement matching)
// Uncomment when requirement embeddings are implemented:
//
// CREATE VECTOR INDEX requirement_embeddings IF NOT EXISTS
// FOR (r:Requirement)
// ON r.embedding
// OPTIONS {
//     indexConfig: {
//         `vector.dimensions`: 768,
//         `vector.similarity_function`: 'cosine'
//     }
// };

// Technology embeddings (for semantic technology discovery)
// Uncomment when technology embeddings are implemented:
//
// CREATE VECTOR INDEX technology_embeddings IF NOT EXISTS
// FOR (t:Technology)
// ON t.embedding
// OPTIONS {
//     indexConfig: {
//         `vector.dimensions`: 768,
//         `vector.similarity_function`: 'cosine'
//     }
// };

// ============================================================================
// Index Management Commands (for reference)
// ============================================================================

// Drop index (use with caution)
// DROP INDEX pattern_embeddings IF EXISTS;

// Show all vector indexes
// SHOW INDEXES
// YIELD name, type, labelsOrTypes, properties
// WHERE type = 'VECTOR';

// Check index population progress
// SHOW INDEXES
// YIELD name, populationPercent, state
// WHERE name = 'pattern_embeddings';

// ============================================================================
// Performance Tuning (Future)
// ============================================================================

// When pattern count exceeds 1000, consider enabling quantization:
//
// DROP INDEX pattern_embeddings IF EXISTS;
//
// CREATE VECTOR INDEX pattern_embeddings
// FOR (p:Pattern)
// ON p.embedding
// OPTIONS {
//     indexConfig: {
//         `vector.dimensions`: 768,
//         `vector.similarity_function`: 'cosine',
//         `vector.quantization.enabled`: true,
//         `vector.quantization.type`: 'bit'  // or 'int8'
//     }
// };

// ============================================================================
// Verification Complete
// ============================================================================

// If all above queries execute successfully:
// ✓ Vector index created
// ✓ Index is online
// ✓ Ready for semantic search
//
// Next steps:
// 1. Run generate_pattern_embeddings.py to populate embeddings
// 2. Run test_vector_search.py to validate search functionality
// 3. Integrate with PatternQueryInterface for hybrid queries
