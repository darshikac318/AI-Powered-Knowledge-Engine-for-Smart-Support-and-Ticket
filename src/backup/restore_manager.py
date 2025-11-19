import shutil

class RestoreManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def restore(self, backup_file):
        shutil.copy(backup_file, self.db_path)
        return f"Restored from {backup_file}"
