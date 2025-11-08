"""
Backup database script for production
"""
import os
import shutil
from datetime import datetime
from pathlib import Path

def backup_database():
    """Backup SQLite database with timestamp"""
    
    # Paths
    base_dir = Path(__file__).parent
    db_path = base_dir / 'roommaster.db'
    backup_dir = base_dir / 'backups'
    
    # Create backup directory if not exists
    backup_dir.mkdir(exist_ok=True)
    
    if not db_path.exists():
        print("❌ Database file not found!")
        return False
    
    # Backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f'roommaster_backup_{timestamp}.db'
    backup_path = backup_dir / backup_name
    
    try:
        # Copy database
        shutil.copy2(db_path, backup_path)
        
        # Get file sizes
        db_size = db_path.stat().st_size / 1024  # KB
        backup_size = backup_path.stat().st_size / 1024  # KB
        
        print("=" * 60)
        print("✅ Database backup successful!")
        print("=" * 60)
        print(f"Original: {db_path} ({db_size:.2f} KB)")
        print(f"Backup:   {backup_path} ({backup_size:.2f} KB)")
        print(f"Time:     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Clean old backups (keep last 10)
        clean_old_backups(backup_dir, keep=10)
        
        return True
        
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False


def clean_old_backups(backup_dir, keep=10):
    """Keep only the last N backups"""
    
    # Get all backup files
    backups = sorted(
        backup_dir.glob('roommaster_backup_*.db'),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    
    # Remove old backups
    removed = 0
    for old_backup in backups[keep:]:
        try:
            old_backup.unlink()
            removed += 1
        except Exception as e:
            print(f"⚠️  Could not remove {old_backup.name}: {e}")
    
    if removed > 0:
        print(f"\n🗑️  Removed {removed} old backup(s)")
        print(f"📦 Kept {len(backups[:keep])} recent backup(s)")


def list_backups():
    """List all available backups"""
    
    base_dir = Path(__file__).parent
    backup_dir = base_dir / 'backups'
    
    if not backup_dir.exists():
        print("No backups found.")
        return
    
    backups = sorted(
        backup_dir.glob('roommaster_backup_*.db'),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    
    if not backups:
        print("No backups found.")
        return
    
    print("\n" + "=" * 60)
    print("📦 Available Backups")
    print("=" * 60)
    
    for i, backup in enumerate(backups, 1):
        size = backup.stat().st_size / 1024  # KB
        mtime = datetime.fromtimestamp(backup.stat().st_mtime)
        print(f"{i}. {backup.name}")
        print(f"   Size: {size:.2f} KB | Date: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        print()


def restore_backup(backup_name):
    """Restore database from backup"""
    
    base_dir = Path(__file__).parent
    db_path = base_dir / 'roommaster.db'
    backup_path = base_dir / 'backups' / backup_name
    
    if not backup_path.exists():
        print(f"❌ Backup file not found: {backup_name}")
        return False
    
    try:
        # Backup current database before restore
        if db_path.exists():
            current_backup = base_dir / 'backups' / f'before_restore_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
            shutil.copy2(db_path, current_backup)
            print(f"💾 Current database backed up to: {current_backup.name}")
        
        # Restore
        shutil.copy2(backup_path, db_path)
        
        print("=" * 60)
        print("✅ Database restored successfully!")
        print("=" * 60)
        print(f"Restored from: {backup_name}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Restore failed: {e}")
        return False


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'list':
            list_backups()
        elif command == 'restore' and len(sys.argv) > 2:
            restore_backup(sys.argv[2])
        else:
            print("Usage:")
            print("  python backup_db.py          - Create backup")
            print("  python backup_db.py list     - List backups")
            print("  python backup_db.py restore <filename> - Restore backup")
    else:
        # Default: create backup
        backup_database()
