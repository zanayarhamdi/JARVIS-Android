from typing import Dict, Any, Optional, List
from core.logger import create_logger
from memory.persistence import get_database
from datetime import datetime

logger = create_logger("BACKUP_MANAGER")

class BackupManager:
    """Manage system backups for safety"""
    
    def __init__(self):
        self.db = get_database()
    
    def create_backup(self, backup_name: str, files_to_backup: Optional[List[str]] = None) -> Dict[str, Any]:
        """Create system backup"""
        try:
            import shutil
            from pathlib import Path
            
            backup_dir = Path('data/backups') / datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            files = files_to_backup or ['core/', 'brain/', 'planner/', 'agent/', 'tools/', 'skills/']
            total_size = 0
            
            for file_path in files:
                src = Path(file_path)
                if src.exists():
                    if src.is_file():
                        dest = backup_dir / src.name
                        shutil.copy2(src, dest)
                        total_size += dest.stat().st_size
                    elif src.is_dir():
                        dest = backup_dir / src.name
                        shutil.copytree(src, dest, dirs_exist_ok=True)
                        for item in dest.rglob('*'):
                            if item.is_file():
                                total_size += item.stat().st_size
            
            # Log backup
            self.db.insert('backup_log', {
                'backup_name': backup_name,
                'file_path': str(backup_dir),
                'size_bytes': total_size
            })
            
            logger.info(f"Backup created: {backup_name} ({total_size} bytes)")
            return {
                'success': True,
                'backup_path': str(backup_dir),
                'backup_size': total_size,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return {'success': False, 'error': str(e)}
    
    def restore_backup(self, backup_path: str) -> Dict[str, Any]:
        """Restore from backup"""
        try:
            import shutil
            from pathlib import Path
            
            backup_src = Path(backup_path)
            if not backup_src.exists():
                return {'success': False, 'error': 'Backup not found'}
            
            # Restore files
            for item in backup_src.iterdir():
                dest = Path(item.name)
                if item.is_file():
                    shutil.copy2(item, dest)
                elif item.is_dir():
                    shutil.copytree(item, dest, dirs_exist_ok=True)
            
            logger.info(f"Backup restored from: {backup_path}")
            return {
                'success': True,
                'message': f'Restored from {backup_path}',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            return {'success': False, 'error': str(e)}
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List all backups"""
        try:
            return self.db.select('backup_log', limit=100)
        except Exception as e:
            logger.error(f"Error listing backups: {e}")
            return []
