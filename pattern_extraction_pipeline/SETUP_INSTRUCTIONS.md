# Setup New Neo4j Container and Migrate Data

## Quick Start

Follow these steps in order:

### Step 1: Create and Start New Container

```powershell
cd pattern_extraction_pipeline
.\setup_new_container.ps1
```

This will:
- Create a new Docker container named `spec-engine-neo4j`
- Run on ports **7475** (HTTP) and **7688** (Bolt) to avoid conflicts
- Use credentials: `neo4j/specengine123`
- Automatically update your `.env` file (with backup)

### Step 2: Migrate Your Data

```powershell
python migrate_to_new_container.py
```

This will:
- Export **1,483 pattern extraction nodes** from old container
- Export **1,797 relationships** from old container
- Import everything to new container
- Verify data integrity
- Ask for confirmation before cleaning old container
- Delete pattern extraction data from old container
- Leave **7,037 other project nodes** in old container

### Step 3: Verify

Access your new Neo4j instance:
- Browser: http://localhost:7475
- Username: `neo4j`
- Password: `specengine123`

Run a test query:
```cypher
MATCH (p:Pattern) RETURN count(p)
```

## What Gets Created

### New Container Details
- **Name**: `spec-engine-neo4j`
- **Ports**: 
  - HTTP: 7475 (instead of 7474)
  - Bolt: 7688 (instead of 7687)
- **Credentials**: neo4j/specengine123
- **Memory**: 2GB heap, 1GB pagecache
- **Plugins**: APOC included

### Updated .env File
```env
NEO4J_URI=bolt://localhost:7688
NEO4J_PASSWORD=specengine123
NEO4J_DATABASE=neo4j
```

## Container Management

### View logs
```powershell
docker logs spec-engine-neo4j
docker logs -f spec-engine-neo4j  # Follow logs
```

### Stop container
```powershell
docker stop spec-engine-neo4j
```

### Start container
```powershell
docker start spec-engine-neo4j
```

### Remove container completely
```powershell
docker-compose down -v  # -v removes volumes (data)
```

## Two Containers Running

After migration, you'll have:

| Container | Purpose | HTTP Port | Bolt Port | Data |
|-----------|---------|-----------|-----------|------|
| `plasticflower-neo4j` | Other project | 7474 | 7687 | Other project data |
| `spec-engine-neo4j` | Pattern extraction | 7475 | 7688 | Pattern extraction data |

Both can run simultaneously without conflicts.

## Troubleshooting

### Port conflicts
If ports 7475 or 7688 are in use, edit `docker-compose.yml` and change the LEFT side of the port mappings:
```yaml
ports:
  - "7476:7474"  # Change 7475 to 7476
  - "7689:7687"  # Change 7688 to 7689
```

Then update your `.env` accordingly.

### Container won't start
Check logs:
```powershell
docker logs spec-engine-neo4j
```

Common issues:
- Docker Desktop not running
- Ports already in use
- Insufficient memory

### Migration fails
If migration fails:
1. Your old data remains intact
2. You can re-run the migration script
3. The script will offer to clear the new container and start fresh

### Can't connect to Neo4j
Wait 30-60 seconds after starting the container for Neo4j to initialize.

Check container is healthy:
```powershell
docker ps
```

Look for "healthy" status.

## Rollback

If you need to rollback (before cleaning old container):

1. Stop using new container:
```powershell
docker stop spec-engine-neo4j
```

2. Restore old .env:
```powershell
Copy-Item .env.backup.TIMESTAMP .env
```

3. Restart your application

Your old data is still in `plasticflower-neo4j` until you confirm cleanup.

## Complete Removal

To completely remove the new setup:

```powershell
docker-compose down -v
```

This removes:
- The container
- All data volumes
- All networks

## Next Steps

After successful migration:
1. Test pattern extraction: `python test_extraction.py`
2. Test queries: `python test_query.py`
3. Access Neo4j Browser: http://localhost:7475
4. The other project can continue using the old container independently
