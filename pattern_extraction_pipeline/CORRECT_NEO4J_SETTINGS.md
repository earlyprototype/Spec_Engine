# Correct Neo4j Settings for Pattern Extraction Pipeline

## Important: Use spec-engine-neo4j Container

The pattern extraction pipeline should connect to **spec-engine-neo4j**, NOT plasticflower-neo4j.

### Container Ports

From `docker ps`:
```
spec-engine-neo4j:
- HTTP:  localhost:7475 (mapped from internal 7474)
- Bolt:  localhost:7688 (mapped from internal 7687)

plasticflower-neo4j: (DO NOT USE)
- HTTP:  localhost:7474
- Bolt:  localhost:7687
```

### Correct .env Configuration

Update your `.env` file with these settings:

```env
# Neo4j Connection - spec-engine-neo4j container
NEO4J_URI=bolt://localhost:7688
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
NEO4J_DATABASE=specengine
```

### Previous Issue

The `env.template` had the wrong port (7687), which points to the plasticflower-neo4j database. This caused connection timeouts and confusion about which database was being used.

### Verification

Test connection with:
```powershell
python test_connection.py
```

Or manually in Neo4j Browser:
```
http://localhost:7475
```

### Why This Matters

- **spec-engine-neo4j**: Contains the pattern extraction graph data
- **plasticflower-neo4j**: Different database, different data
- Using wrong port = connecting to wrong database = wrong data

### Update Checklist

- [ ] Update `.env` with `NEO4J_URI=bolt://localhost:7688`
- [ ] Test connection with `python test_connection.py`
- [ ] Verify correct database with `MATCH (p:Pattern) RETURN count(p)`
- [ ] Run `setup_data_quality.py` to create constraints
- [ ] Proceed with duplicate detection testing
