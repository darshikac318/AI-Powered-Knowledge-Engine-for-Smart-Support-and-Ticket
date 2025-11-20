import os
import psutil
from datetime import datetime
from typing import Dict

class SystemHealth:
    def __init__(self):
        pass
    
    def get_database_size(self, db_path="data/support_system.db") -> float:
        if os.path.exists(db_path):
            size_bytes = os.path.getsize(db_path)
            size_mb = size_bytes / (1024 * 1024)
            return round(size_mb, 2)
        return 0.0
    
    def get_chromadb_size(self, chroma_path="data/processed") -> float:
        if os.path.exists(chroma_path):
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(chroma_path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
            size_mb = total_size / (1024 * 1024)
            return round(size_mb, 2)
        return 0.0
    
    def get_memory_usage(self) -> Dict:
        memory = psutil.virtual_memory()
        return {
            'total_gb': round(memory.total / (1024**3), 2),
            'available_gb': round(memory.available / (1024**3), 2),
            'percent_used': memory.percent
        }
    
    def get_disk_usage(self, path=".") -> Dict:
        disk = psutil.disk_usage(path)
        return {
            'total_gb': round(disk.total / (1024**3), 2),
            'used_gb': round(disk.used / (1024**3), 2),
            'free_gb': round(disk.free / (1024**3), 2),
            'percent_used': disk.percent
        }
    
    def get_system_health_report(self) -> Dict:
        return {
            'timestamp': datetime.now().isoformat(),
            'database_size_mb': self.get_database_size(),
            'chromadb_size_mb': self.get_chromadb_size(),
            'memory': self.get_memory_usage(),
            'disk': self.get_disk_usage(),
            'status': 'healthy'
        }