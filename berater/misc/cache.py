# -*- coding: utf-8 -*-
# created by inhzus

from .models import redis_client


class MemoryCache(object):
    def __init__(self, name: str, ttl: int):
        self.name = name
        self.ttl = ttl

    @staticmethod
    def concat_keys(*args):
        return '_'.join([str(arg) for arg in args])

    def get(self, key) -> dict:
        named_key = self.concat_keys(key, self.name)
        # default to be {}
        data: dict = redis_client.hgetall(named_key)
        return data

    def set(self, key, **kwargs):
        named_key = self.concat_keys(key, self.name)
        redis_client.hmset(named_key, kwargs)
        redis_client.expire(named_key, self.ttl)

    def refresh(self, key):
        named_key = self.concat_keys(key, self.name)
        redis_client.expire(named_key, self.ttl)
