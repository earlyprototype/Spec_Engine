"""
Charity Shop POS - Database Backup Utility
Automated backup functionality with timestamped copies
"""

import os
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path


class DatabaseBackup:
    """Handles database backup operations"""
    
    def __init__(self, db_path='charity_pos.db', backup_dir='backups'):
        """
        Initialize backup manager
        
        Args:
            db_path: Path to source database file
            backup_dir: Directory to store backups
        """
        self.db_path = Path(db_path)
        self.backup_dir = Path(backup_dir)
        
        # Create backup directory if it doesn't exist
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_backup(self, backup_name=None):
        """
        Create a timestamped backup of the database
        
        Args:
            backup_name: Optional custom backup name (default: auto-generated timestamp)
        
        Returns:
            Path to created backup file
        """
        if not self.db_path.exists():
            raise FileNotFoundError(f"Source database not found: {self.db_path}")
        
        # Generate backup filename with timestamp
        if backup_name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"charity_pos_backup_{timestamp}.db"
        
        backup_path = self.backup_dir / backup_name
        
        # Method 1: Use SQLite backup API (recommended for active databases)
        try:
            self._sqlite_backup(backup_path)
            print(f"✓ Backup created successfully: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"✗ SQLite backup failed: {e}")
            print("  Trying file copy method...")
            
            # Method 2: Fallback to file copy
            try:
                shutil.copy2(self.db_path, backup_path)
                print(f"✓ Backup created successfully (file copy): {backup_path}")
                return backup_path
            except Exception as copy_error:
                raise Exception(f"Both backup methods failed: {e}, {copy_error}")
    
    def _sqlite_backup(self, backup_path):
        """
        Create backup using SQLite backup API
        This method is safer for active databases
        """
        source_conn = sqlite3.connect(str(self.db_path))
        backup_conn = sqlite3.connect(str(backup_path))
        
        try:
            with backup_conn:
                source_conn.backup(backup_conn)
        finally:
            source_conn.close()
            backup_conn.close()
    
    def list_backups(self):
        """
        List all available backups
        
        Returns:
            List of tuples: (backup_path, size_mb, created_time)
        """
        backups = []
        
        for backup_file in self.backup_dir.glob('*.db'):
            stats = backup_file.stat()
            size_mb = stats.st_size / (1024 * 1024)
            created_time = datetime.fromtimestamp(stats.st_mtime)
            
            backups.append((
                backup_file.name,
                f"{size_mb:.2f} MB",
                created_time.strftime('%Y-%m-%d %H:%M:%S')
            ))
        
        # Sort by created time (newest first)
        backups.sort(key=lambda x: x[2], reverse=True)
        
        return backups
    
    def restore_backup(self, backup_name, confirm=True):
        """
        Restore database from a backup
        
        Args:
            backup_name: Name of backup file to restore
            confirm: Require confirmation before overwriting (default: True)
        
        Returns:
            True if restored successfully
        """
        backup_path = self.backup_dir / backup_name
        
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_path}")
        
        if confirm:
            if self.db_path.exists():
                print(f"\nWARNING: This will overwrite the current database: {self.db_path}")
                response = input("Continue? (yes/no): ")
                if response.lower() != 'yes':
                    print("Restore cancelled.")
                    return False
        
        # Create a safety backup of current database before restoring
        if self.db_path.exists():
            safety_backup = f"before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            safety_path = self.backup_dir / safety_backup
            shutil.copy2(self.db_path, safety_path)
            print(f"✓ Created safety backup: {safety_path}")
        
        # Restore backup
        shutil.copy2(backup_path, self.db_path)
        print(f"✓ Database restored from: {backup_name}")
        return True
    
    def delete_old_backups(self, keep_count=10):
        """
        Delete old backups, keeping only the most recent ones
        
        Args:
            keep_count: Number of most recent backups to keep (default: 10)
        
        Returns:
            Number of backups deleted
        """
        backups = list(self.backup_dir.glob('*.db'))
        
        if len(backups) <= keep_count:
            print(f"Only {len(backups)} backups found. Nothing to delete.")
            return 0
        
        # Sort by modification time (oldest first)
        backups.sort(key=lambda p: p.stat().st_mtime)
        
        # Delete oldest backups
        delete_count = len(backups) - keep_count
        deleted = 0
        
        for backup_path in backups[:delete_count]:
            try:
                backup_path.unlink()
                print(f"✓ Deleted old backup: {backup_path.name}")
                deleted += 1
            except Exception as e:
                print(f"✗ Failed to delete {backup_path.name}: {e}")
        
        return deleted
    
    def get_backup_info(self):
        """Get information about backup directory and backups"""
        total_size = sum(f.stat().st_size for f in self.backup_dir.glob('*.db'))
        backup_count = len(list(self.backup_dir.glob('*.db')))
        
        return {
            'backup_dir': str(self.backup_dir.absolute()),
            'backup_count': backup_count,
            'total_size_mb': total_size / (1024 * 1024),
        }


def automated_backup(db_path='charity_pos.db', backup_dir='backups', keep_count=10):
    """
    Perform automated backup with old backup cleanup
    Suitable for scheduled tasks (e.g., daily cron job)
    
    Args:
        db_path: Path to database file
        backup_dir: Directory for backups
        keep_count: Number of backups to retain
    
    Returns:
        Path to created backup
    """
    backup_manager = DatabaseBackup(db_path, backup_dir)
    
    # Create new backup
    backup_path = backup_manager.create_backup()
    
    # Clean up old backups
    deleted = backup_manager.delete_old_backups(keep_count)
    if deleted > 0:
        print(f"✓ Cleaned up {deleted} old backup(s)")
    
    return backup_path


def main():
    """Interactive backup utility"""
    import sys
    
    print("=" * 60)
    print("Charity Shop POS - Database Backup Utility")
    print("=" * 60)
    
    backup_manager = DatabaseBackup()
    
    # Check if database exists
    if not backup_manager.db_path.exists():
        print(f"\n✗ Error: Database not found: {backup_manager.db_path}")
        print("Please create the database first using init_database.py")
        return
    
    while True:
        print("\nOptions:")
        print("  1. Create backup")
        print("  2. List backups")
        print("  3. Restore backup")
        print("  4. Delete old backups")
        print("  5. Backup info")
        print("  6. Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            # Create backup
            try:
                backup_path = backup_manager.create_backup()
                print(f"\nBackup size: {backup_path.stat().st_size / 1024:.2f} KB")
            except Exception as e:
                print(f"\n✗ Error creating backup: {e}")
        
        elif choice == '2':
            # List backups
            backups = backup_manager.list_backups()
            if not backups:
                print("\nNo backups found.")
            else:
                print(f"\nFound {len(backups)} backup(s):")
                print(f"\n{'Filename':<40} {'Size':<15} {'Created':<20}")
                print("-" * 75)
                for name, size, created in backups:
                    print(f"{name:<40} {size:<15} {created:<20}")
        
        elif choice == '3':
            # Restore backup
            backups = backup_manager.list_backups()
            if not backups:
                print("\nNo backups available to restore.")
            else:
                print("\nAvailable backups:")
                for i, (name, size, created) in enumerate(backups, 1):
                    print(f"  {i}. {name} ({size}) - {created}")
                
                try:
                    selection = int(input("\nSelect backup number to restore: "))
                    if 1 <= selection <= len(backups):
                        backup_name = backups[selection - 1][0]
                        backup_manager.restore_backup(backup_name, confirm=True)
                    else:
                        print("Invalid selection.")
                except ValueError:
                    print("Invalid input.")
                except Exception as e:
                    print(f"✗ Error restoring backup: {e}")
        
        elif choice == '4':
            # Delete old backups
            try:
                keep = int(input("How many recent backups to keep? [10]: ") or "10")
                deleted = backup_manager.delete_old_backups(keep)
                print(f"\n✓ Deleted {deleted} old backup(s)")
            except ValueError:
                print("Invalid number.")
            except Exception as e:
                print(f"✗ Error deleting backups: {e}")
        
        elif choice == '5':
            # Backup info
            info = backup_manager.get_backup_info()
            print(f"\nBackup Directory: {info['backup_dir']}")
            print(f"Total Backups: {info['backup_count']}")
            print(f"Total Size: {info['total_size_mb']:.2f} MB")
        
        elif choice == '6':
            print("\nExiting...")
            break
        
        else:
            print("\nInvalid option. Please select 1-6.")


if __name__ == '__main__':
    main()



