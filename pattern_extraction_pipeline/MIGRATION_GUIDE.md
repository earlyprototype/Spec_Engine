# Database Migration Guide: patterns → specengine

## Overview

This guide helps you migrate from the shared `patterns` database to the dedicated `specengine` database in Neo4j.

## Why Migrate?

The `patterns` database is shared with another project, which can cause conflicts and data confusion. The `specengine` database is dedicated to this project only.

## Prerequisites

- Python installed with `neo4j` package
- Access to the Neo4j instance (bolt://localhost:7688)
- `.env` file configured with Neo4j credentials

## Migration Process

### Option 1: Automated Migration (Recommended)

Run the PowerShell script which handles everything automatically:

```powershell
cd pattern_extraction_pipeline
.\migrate_database.ps1
```

The script will:
1. Check your environment
2. Create the `specengine` database
3. Export data from `patterns`
4. Import data to `specengine`
5. Verify the migration
6. Clean the `patterns` database
7. Offer to update your `.env` file automatically

### Option 2: Manual Migration

If you prefer to run the Python script directly:

```powershell
cd pattern_extraction_pipeline
python migrate_database.py
```

Then manually update your `.env` file:

```bash
# Change this line:
NEO4J_DATABASE=patterns

# To this:
NEO4J_DATABASE=specengine
```

## What the Migration Does

1. **Creates Target Database**: Creates a new `specengine` database in Neo4j
2. **Exports Data**: Reads all nodes and relationships from `patterns`
3. **Imports Data**: Writes all data to `specengine`
4. **Verifies**: Compares counts to ensure nothing was lost
5. **Cleans Source**: Removes all data from `patterns` (with confirmation)
6. **Updates Config**: Updates `.env` file to point to `specengine`

## Safety Features

- **Backup Created**: Your original `.env` is backed up with a timestamp
- **Confirmation Required**: The script asks before deleting data from `patterns`
- **Verification**: Counts are compared to ensure data integrity
- **Rollback Option**: If something goes wrong, you can restore from `patterns` (if you don't clean it)

## After Migration

1. **Restart Services**: If you have any services running (query interface, extractors, etc.), restart them
2. **Verify**: Run a test query to ensure everything works:
   ```powershell
   python test_query.py
   ```
3. **Test Extraction**: Try a small extraction to verify the system works:
   ```powershell
   python test_extraction.py
   ```

## Troubleshooting

### Migration Failed

If the migration fails midway:
1. Check the error message
2. The `specengine` database may be partially populated
3. You can re-run the script - it will offer to drop and recreate `specengine`
4. Your original `patterns` data remains intact until you confirm the cleanup

### Connection Errors

If you get connection errors:
1. Verify Neo4j is running: check Docker Desktop or run `docker ps`
2. Check your `.env` file has the correct credentials
3. Test connection: `python test_query.py`

### Database Already Exists

If `specengine` already exists, the script will:
1. Detect it
2. Ask if you want to drop and recreate it
3. If you say no, it will skip creation but continue with migration

## Rollback

If you need to rollback (only possible before cleaning `patterns`):

1. Update `.env` back to:
   ```
   NEO4J_DATABASE=patterns
   ```
2. Restart your services
3. Delete the `specengine` database (optional):
   ```cypher
   // In Neo4j Browser, connected to 'system' database:
   DROP DATABASE specengine IF EXISTS
   ```

## Configuration Files Updated

After migration, these files will reflect the new database name:

- `.env` - Main configuration file (if you chose to auto-update)
- `.env.backup.TIMESTAMP` - Backup of your original configuration

## Database Structure Preserved

The migration preserves:
- All node labels
- All node properties
- All relationships
- All relationship properties
- Graph structure

## Next Steps

Once migration is complete:
1. Continue using the pattern extraction pipeline normally
2. All new data will go to `specengine`
3. The other project can continue using `patterns` without interference

## Questions?

If you encounter issues:
1. Check the error messages in the script output
2. Verify Neo4j is running and accessible
3. Check logs in Neo4j Browser (http://localhost:7474)
4. Ensure you have the correct credentials in `.env`
