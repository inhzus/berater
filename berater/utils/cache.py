# -*- coding: utf-8 -*-
# created by inhzus

import collections
import time
import weakref


class MemoryCache(object):
    class Entity(object):
        def __init__(self, ttl: int, data: dict):
            self.expire = (time.time() + ttl) if ttl else 0
            self.data = data

        def is_expired(self):
            return self.expire and time.time() > self.expire

    def __init__(self, ttl: int, max_len: int = 0):
        self.ttl = ttl
        self.weak = weakref.WeakValueDictionary()
        self.strong = collections.deque(maxlen=max_len) if max_len else collections.deque()

    def get(self, key, default=None) -> dict:
        entity: MemoryCache.Entity = self.weak.get(key, None)
        if entity is not None:
            if not entity.is_expired():
                return entity.data
        return default

    def set(self, key, **kwargs):
        self.weak[key] = ref = MemoryCache.Entity(self.ttl, kwargs)
        self.strong.append(ref)
        while self.strong[0].is_expired():
            self.strong.popleft()

    def put(self, key, **kwargs):
        data = self.get(key)
        if data is not None:
            for k, v in kwargs.items():
                data[k] = v
            return True
        return False
