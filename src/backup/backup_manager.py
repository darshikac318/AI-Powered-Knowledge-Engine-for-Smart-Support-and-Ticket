import os
import shutil
from datetime import datetime

class BackupManager:
    def __init__(self, db_path, backup_folder="backups"):
        self.db_path = db_path
        self.backup_folder = backup_folder
        os.makedirs(self.backup_folder, exist_ok=True)

    def create_backup(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.backup_folder, f"backup_{timestamp}.db")
        shutil.copy(self.db_path, backup_file)
        return backup_file

    def list_backups(self):
        return os.listdir(self.backup_folder)
