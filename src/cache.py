import time
from collections import OrderedDict

# Global in-memory store of cache data.
_caches = {}
_expire_info = {}


class LocalMemoryCache:
    """
    Cache class that keeps data in memory and remove when expires.
    """

    def __init__(self):
        self._cache = _caches.setdefault('cache_data', OrderedDict())
        self._expire_info = _expire_info.setdefault('cache_data', {})
        self._default_timeout = 300

    def add(self, key, value):
        self._cache[key] = value
        self._expire_info[key] = time.time() + self._default_timeout

    def get(self, key):
        if self._has_expired(key):
            self._delete(key)
            return None

        return self._cache.get(key, None)

    def has_key(self, key):
        if key not in self._cache:
            return False

        if self._has_expired(key):
            self._delete(key)
            return False

        return True

    def _has_expired(self, key):
        expiry = self._expire_info.get(key)
        return expiry is not None and expiry <= time.time()

    def _delete(self, key):
        try:
            del self._cache[key]
            del self._expire_info[key]
        except KeyError:
            pass

    def delete(self, key):
        self._delete(key)
