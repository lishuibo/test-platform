from exts import cache

__author__ = 'litl'


def set(key, value, timeout=60):
    return cache.set(key, value, timeout)


def get(key):
    return cache.get(key)


def delete(key):
    return cache.delete(key)