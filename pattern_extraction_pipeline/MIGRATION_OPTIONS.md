# Database Separation Options for Shared Neo4j Instance

## Problem

You're sharing the default `neo4j` database with another project:
- **Pattern Extraction Data**: 1,483 nodes (Pattern, Requirement, Constraint, Technology, ReferenceNode)
- **Other Project Data**: 7,037 nodes (Flower, Session, TranscriptChunk, etc.)

Neo4j Community Edition only supports ONE database, so you cannot create separate `specengine` and `patterns` databases.

## Solutions

### Option 1: Upgrade to Neo4j Enterprise Edition (Best Separation)

**Pros:**
- True database isolation
- Better performance
- Professional solution
- Each project completely independent

**Cons:**
- Requires licence (free for development/testing)
- Need to recreate container

**Steps:**
1. Stop existing container
2. Use `neo4j:5.22-enterprise` image
3. Accept licence agreement
4. Run migration script successfully

See `UPGRADE_TO_ENTERPRISE.md` for detailed instructions.

---

### Option 2: Use Different Neo4j Container (Recommended)

**Pros:**
- Simple and quick
- Both instances can run simultaneously
- Complete isolation
- No licence needed

**Cons:**
- Uses more resources (2 Neo4j instances)
- Need to manage another container

**Steps:**
1. Create new Docker container for spec-engine on different ports
2. Update `.env` to point to new container
3. Run fresh extraction in new container
4. Leave other project untouched

See `CREATE_SEPARATE_CONTAINER.md` for detailed instructions.

---

### Option 3: Namespace Segregation within Same Database

**Pros:**
- Works with Community Edition
- No infrastructure changes
- Uses existing setup

**Cons:**
- Data still mixed in same database
- Requires careful query filtering
- Risk of cross-project queries
- More complex to maintain

**Implementation:**
- Add a `project` property to all nodes: `{project: "specengine"}`
- Filter all queries by project
- Use Cypher query prefixes: `MATCH (n {project: "specengine"})`

See `NAMESPACE_SEGREGATION.md` for implementation.

---

### Option 4: Do Nothing (Not Recommended)

**Keep current setup:**
- Both projects share the `neo4j` database
- Distinguish by node labels only
- Your queries already filter by label (Pattern, Requirement, etc.)

**Risks:**
- Data confusion
- Accidental cross-project operations
- Hard to debug issues
- Difficult to backup/restore separately

---

## Recommendation

**For your situation, I recommend Option 2: Create a separate Neo4j container**

This is the best balance of:
- ✅ Complete isolation (like Option 1)
- ✅ No licence needed (unlike Option 1)
- ✅ Simple setup (unlike Option 3)
- ✅ Professional approach
- ✅ Can run both projects simultaneously

**Next steps:**
1. I'll create a Docker Compose file for a new `spec-engine-neo4j` container
2. It will run on ports 7475/7688 (avoiding conflict with 7474/7687)
3. Update your `.env` to use the new container
4. Optionally migrate existing data

Would you like me to proceed with Option 2?
