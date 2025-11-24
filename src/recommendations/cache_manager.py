import hashlib
import json
import time
from typing import Any, Dict, Optional, List
from functools import lru_cache
import pickle
import os

class CacheManager:
    
    def __init__(self, cache_dir: str = "data/cache", ttl: int = 3600):
        self.cache_dir = cache_dir
        self.ttl = ttl
        self.memory_cache: Dict[str, tuple] = {}  
        os.makedirs(cache_dir, exist_ok=True)
    
    def _generate_key(self, query: str, **kwargs) -> str:
        data = f"{query}_{json.dumps(kwargs, sort_keys=True)}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def get(self, query: str, **kwargs) -> Optional[Any]:
        key = self._generate_key(query, **kwargs)
       
        if key in self.memory_cache:
            value, timestamp = self.memory_cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.memory_cache[key]

        cache_file = os.path.join(self.cache_dir, f"{key}.pkl")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    value, timestamp = pickle.load(f)
                
                if time.time() - timestamp < self.ttl:
                    self.memory_cache[key] = (value, timestamp)
                    return value
                else:
                    os.remove(cache_file)
            except Exception as e:
                print(f"Error loading cache: {e}")
        
        return None
    
    def set(self, query: str, value: Any, **kwargs) -> None:
        key = self._generate_key(query, **kwargs)
        timestamp = time.time()
        self.memory_cache[key] = (value, timestamp)
        cache_file = os.path.join(self.cache_dir, f"{key}.pkl")
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump((value, timestamp), f)
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def clear(self) -> None:
        self.memory_cache.clear()
        if os.path.exists(self.cache_dir):
            for filename in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting cache file {file_path}: {e}")
    
    def clear_expired(self) -> int:
        cleared = 0
        current_time = time.time()
        
        expired_keys = [
            key for key, (_, timestamp) in self.memory_cache.items()
            if current_time - timestamp >= self.ttl
        ]
        for key in expired_keys:
            del self.memory_cache[key]
            cleared += 1
        
        if os.path.exists(self.cache_dir):
            for filename in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        with open(file_path, 'rb') as f:
                            _, timestamp = pickle.load(f)
                        
                        if current_time - timestamp >= self.ttl:
                            os.remove(file_path)
                            cleared += 1
                except Exception as e:
                    print(f"Error checking cache file {file_path}: {e}")
        
        return cleared
    
    def get_stats(self) -> Dict[str, int]:
        memory_count = len(self.memory_cache)
        disk_count = 0
        
        if os.path.exists(self.cache_dir):
            disk_count = len([
                f for f in os.listdir(self.cache_dir)
                if os.path.isfile(os.path.join(self.cache_dir, f))
            ])
        
        return {
            "memory_entries": memory_count,
            "disk_entries": disk_count,
            "ttl_seconds": self.ttl
        }

_global_cache: Optional[CacheManager] = None

def get_cache_manager() -> CacheManager:
    global _global_cache
    if _global_cache is None:
        _global_cache = CacheManager()
    return _global_cache


@lru_cache(maxsize=100)
def cache_embedding(query: str) -> str:
    return query