from cm4 import CM4
from doorkeeper import Doorkeeper
from lru import LRUCache
from slru import SLRUCache
import math
import functools
import time


def TinyLFUCache(cache_size=128, sample_size=100000, false_positive=0.0001):
    def decorator(func):
        t = TinyLFU(size=cache_size,
                    sample=sample_size,
                    false_positive=false_positive)

        def search(*args, **kargs):

            key = str(functools._make_key(args, kargs, True))
            if key in t:
                search.__hits += 1
                start = time.time()
                value = t.get(key)
                end = time.time()
                timeit = int(end * 1000000 - start * 1000000)
                return t.get(key)
            else:
                search.__misses += 1
                result = func(*args, **kargs)
                start = time.time()
                t.set(key, result)
                end = time.time()
                timeit = int(end * 1000000 - start * 1000000)
                return result

        search.__hits = search.__misses = 0
        search.cache_info = lambda: functools._CacheInfo(
            search.__hits, search.__misses, cache_size, len(t))
        return search

    return decorator


class TinyLFU:
    def __init__(self, size=1000000, sample=100000, false_positive=0.01):
        self.__age = 0
        self.__sample = sample
        self.counter = CM4(size)
        self.doorkeeper = Doorkeeper(sample, false_positive)
        if size <= 1:
            size = 2
        # percentage from https://arxiv.org/abs/1512.00727
        lru_percent = 1
        lru_size = (lru_percent * size) / 100
        if lru_size < 1:
            lru_size = 1
        self.lru = LRUCache(cache_size=lru_size)

        slru_size = math.ceil(((100.0 - lru_percent) / 100.0) * size)
        slru20_size = math.ceil(slru_size * 0.2)
        if slru20_size < 1:
            slru20_size = 1
        self.slru = SLRUCache(probation_cap=slru20_size,
                              protect_cap=slru_size - slru20_size)

    def __len__(self) -> int:
        return len(self.lru) + len(self.slru)

    def __contains__(self, key) -> bool:
        return key in self.lru or key in self.slru

    def get(self, key: str):
        # for tinylfu aging, reset only admission
        self.__age += 1
        if self.__age == self.__sample:
            self.counter.reset()
            self.doorkeeper.reset()
            self.__age = 0

        self.counter.add(key)

        value = self.lru.get(key)
        if value != None:
            # timeout
            return value

        value = self.slru.get(key)
        if value != None:
            # timeout
            return value

    def set(self, key: str, value):
        if key in self.slru:
            self.slru.remove(key)

        old_key, old_value, evicted = self.lru.set(key, value)
        if not evicted:
            return
        victim_key = self.slru.victim()
        if victim_key == None:
            self.slru.set(old_key, old_value)
            return

        if not self.doorkeeper.allow(old_key):
            # on evict
            return
        victim_count = self.counter.estimate(victim_key)
        item_count = self.counter.estimate(old_key)
        if victim_count < item_count:
            self.slru.set(old_key, old_value)
        else:
            # on evict
            return

    def remove(self, key: str) -> object:
        value = self.lru.remove(key)
        if value != None:
            return value

        value = self.slru.remove(key)
        if value != None:
            return value
