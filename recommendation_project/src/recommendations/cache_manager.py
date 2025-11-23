"""Simple thread-safe LRU cache for query results."""
from collections import OrderedDict
from threading import RLock
from typing import Any, Callable

class LRUCache:
    def __init__(self, max_size: int = 1024):
        self.max_size = max_size
        self.store = OrderedDict()
        self.lock = RLock()

    def get(self, key: str) -> Any:
        with self.lock:
            if key not in self.store:
                return None
            value = self.store.pop(key)
            self.store[key] = value
            return value

    def set(self, key: str, value: Any) -> None:
        with self.lock:
            if key in self.store:
                self.store.pop(key)
            elif len(self.store) >= self.max_size:
                self.store.popitem(last=False)
            self.store[key] = value

    def clear(self):
        with self.lock:
            self.store.clear()

# convenience global cache instance
_cache = LRUCache(max_size=1000)

def cache_query(query: str, compute_fn: Callable[[], Any]):
    """Cache by raw query string. Returns cached result if present."""
    key = query
    cached = _cache.get(key)
    if cached is not None:
        return cached
    result = compute_fn()
    _cache.set(key, result)
    return result
