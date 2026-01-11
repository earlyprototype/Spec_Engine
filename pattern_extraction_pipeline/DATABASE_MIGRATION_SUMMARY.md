# Database Migration Summary

## Current Situation
- **Current Database**: `patterns` (shared with another project)
- **Target Database**: `specengine` (dedicated to this project)
- **Connection**: bolt://localhost:7688

## Files Created

### 1. `migrate_database.py`
Python script that performs the actual migration:
- Creates the new `specengine` database
- Exports all nodes and relationships from `patterns`
- Imports everything to `specengine`
- Verifies data integrity
- Cleans the `patterns` database (with confirmation)

### 2. `migrate_database.ps1`
PowerShell wrapper script that:
- Checks prerequisites
- Runs the Python migration script
- Offers to automatically update your `.env` file
- Creates a backup of your `.env` before updating

### 3. `MIGRATION_GUIDE.md`
Comprehensive documentation covering:
- Why to migrate
- Step-by-step instructions
- Troubleshooting
- Rollback procedures

## Files Updated

### 1. `env.template`
Updated to use `specengine` as the default database name

### 2. `QUICK_SETUP.ps1`
Updated to configure `specengine` instead of `patterns` for new setups

## How to Run the Migration

### Quick Start (Recommended)
```powershell
cd pattern_extraction_pipeline
.\migrate_database.ps1
```

### What Will Happen
1. Script checks your environment
2. Shows you statistics about the current `patterns` database
3. Creates the new `specengine` database
4. Copies all your data
5. Verifies the copy was successful
6. Asks if you want to clean the `patterns` database
7. Asks if you want to update your `.env` file

### Safety Features
- Your `.env` will be backed up before any changes
- You'll be asked to confirm before deleting data
- Data integrity is verified before cleanup
- The `patterns` database keeps your data until you explicitly confirm deletion

## After Migration

1. Your `.env` will have:
   ```
   NEO4J_DATABASE=specengine
   ```

2. Restart any running services

3. Test the system:
   ```powershell
   python test_query.py
   python test_extraction.py
   ```

## Important Notes

- The migration preserves ALL data (nodes, relationships, properties)
- The `patterns` database will be cleaned only after you confirm
- If something goes wrong, you can re-run the migration
- New installations will automatically use `specengine`

## Need Help?

See `MIGRATION_GUIDE.md` for detailed troubleshooting and rollback procedures.
