// Manual cleanup queries for Neo4j Browser
// Run these one at a time in Neo4j Browser

// =================================
// Step 1: Merge duplicate 'sqlite'/'SQLite'
// =================================

MATCH (dup:Technology {name: 'SQLite'})
MATCH (primary:Technology {name: 'sqlite'})
MATCH (p:Pattern)-[r:USES]->(dup)
MERGE (p)-[new:USES]->(primary)
ON CREATE SET new.role = r.role
WITH dup
DETACH DELETE dup;

// =================================
// Step 2: Merge duplicate 'rust'/'Rust'
// =================================

MATCH (dup:Technology {name: 'Rust'})
MATCH (primary:Technology {name: 'rust'})
MATCH (p:Pattern)-[r:USES]->(dup)
MERGE (p)-[new:USES]->(primary)
ON CREATE SET new.role = r.role
WITH dup
DETACH DELETE dup;

// =================================
// Step 3: Merge duplicate 'react'/'React'
// =================================

MATCH (dup:Technology {name: 'React'})
MATCH (primary:Technology {name: 'react'})
MATCH (p:Pattern)-[r:USES]->(dup)
MERGE (p)-[new:USES]->(primary)
ON CREATE SET new.role = r.role
WITH dup
DETACH DELETE dup;

// =================================
// Step 4: Merge duplicate 'Go'/'go'
// =================================

MATCH (dup:Technology {name: 'Go'})
MATCH (primary:Technology {name: 'go'})
MATCH (p:Pattern)-[r:USES]->(dup)
MERGE (p)-[new:USES]->(primary)
ON CREATE SET new.role = r.role
WITH dup
DETACH DELETE dup;

// =================================
// Step 5: Merge duplicate constraints
// =================================

MATCH (dup:Constraint), (primary:Constraint)
WHERE dup.rule = primary.rule AND id(dup) > id(primary)
MATCH (p:Pattern)-[r:REQUIRES]->(dup)
MERGE (p)-[:REQUIRES]->(primary)
WITH dup
DETACH DELETE dup;

// =================================
// Step 6: Normalize all remaining technology names
// =================================

MATCH (t:Technology)
WHERE t.name <> toLower(t.name)
SET t.name = toLower(t.name);

// =================================
// Step 7: Remove duplicate USES relationships
// =================================

MATCH (p:Pattern)-[r:USES]->(t:Technology)
WITH p, t, collect(r) AS rels
WHERE size(rels) > 1
FOREACH (rel IN tail(rels) | DELETE rel);

// =================================
// Step 8: Create unique constraints (if not exists)
// =================================

CREATE CONSTRAINT tech_unique IF NOT EXISTS FOR (t:Technology) REQUIRE t.name IS UNIQUE;
CREATE CONSTRAINT constraint_unique IF NOT EXISTS FOR (c:Constraint) REQUIRE c.rule IS UNIQUE;

// =================================
// Step 9: Verify cleanup
// =================================

// Should return 0 rows
MATCH (t:Technology)
WITH toLower(t.name) AS normalized_name, collect(t.name) AS names
WHERE size(names) > 1
RETURN normalized_name, names, size(names) AS count;

// Should return 0 rows
MATCH (p:Pattern)-[r:USES]->(t:Technology)
WITH p, t, count(r) AS rel_count
WHERE rel_count > 1
RETURN p.name, t.name, rel_count;
