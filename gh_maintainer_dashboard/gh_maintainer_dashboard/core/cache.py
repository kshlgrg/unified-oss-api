import json
import time
from typing import Optional, Any
from functools import wraps


class InMemoryCache:
    def __init__(self, ttl: int = 3600):
        self._cache = {}
        self._ttl = ttl
    
    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            data, timestamp = self._cache[key]
            if time.time() - timestamp < self._ttl:
                return data
            else:
                del self._cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        self._cache[key] = (value, time.time())
    
    def delete(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]
    
    def clear(self) -> None:
        self._cache.clear()


class CacheManager:
    def __init__(self, ttl: int = 3600, use_redis: bool = False):
        self.ttl = ttl
        self.use_redis = use_redis
        
        if use_redis:
            try:
                import redis
                self.cache = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
                self.cache.ping()
            except Exception:
                self.cache = InMemoryCache(ttl)
                self.use_redis = False
        else:
            self.cache = InMemoryCache(ttl)
    
    def get(self, key: str) -> Optional[Any]:
        if self.use_redis:
            data = self.cache.get(key)
            return json.loads(data) if data else None
        return self.cache.get(key)
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        ttl = ttl or self.ttl
        if self.use_redis:
            self.cache.setex(key, ttl, json.dumps(value))
        else:
            self.cache.set(key, value)
    
    def delete(self, key: str) -> None:
        if self.use_redis:
            self.cache.delete(key)
        else:
            self.cache.delete(key)


def cached(ttl: int = 3600):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            cache_key = f"{func.__name__}:{':'.join(map(str, args))}"
            
            if hasattr(self, 'cache'):
                cached_result = self.cache.get(cache_key)
                if cached_result is not None:
                    return cached_result
            
            result = func(self, *args, **kwargs)
            
            if hasattr(self, 'cache'):
                self.cache.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator
