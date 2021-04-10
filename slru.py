from functools import lru_cache, wraps
from collections import deque


# should put queue and hash_map in same class in the future
# left means new
class SLRUCache:
    def __init__(self, probation_cap, protect_cap):
        self.probation_cap = probation_cap
        self.protect_cap = protect_cap
        self.probation_queue = deque()
        self.protect_queue = deque()
        self.probation_hash_map = dict()
        self.protect_hash_map = dict()

    def __len__(self) -> int:
        return len(self.protect_queue) + len(self.probation_queue)

    def pop(self) -> str:
        if len(self) < (self.protect_cap + self.probation_cap):
            return None
        victim_key = self.probation_queue.pop()
        self.probation_hash_map.pop(victim_key)
        return victim_key

    def get(self, key: str) -> object:
        if key in self.protect_hash_map:
            self.protect_queue.remove(key)
            self.protect_queue.appendleft(key)
            return self.protect_hash_map[key]

        if key in self.probation_hash_map:
            if len(self.protect_queue) < self.protect_cap:
                # remove from probation
                self.probation_queue.remove(key)
                value = self.probation_hash_map.pop(key)
                # add to protect
                self.protect_queue.appendleft(key)
                self.protect_hash_map[key] = value
                return value
            # remove from protect and append to probation
            back = self.protect_queue.pop()
            back_value = self.protect_hash_map.pop(back)
            self.probation_queue.appendleft(back)
            self.probation_hash_map[back] = back_value
            # remove from probation and append to protect
            self.probation_queue.remove(key)
            value = self.probation_hash_map.pop(key)
            self.protect_queue.appendleft(key)
            self.protect_hash_map[key] = value
            return value

    def set(self, key: str, value):
        if len(self.probation_queue) < self.probation_cap:
            self.probation_queue.appendleft(key)
            self.probation_hash_map[key] = value
            return
        if key not in self.probation_hash_map:
            self.pop()
        else:
            self.probation_queue.remove(key)
        self.probation_queue.appendleft(key)
        self.probation_hash_map[key] = value

    def remove(self, key: str) -> object:
        if key in self.probation_hash_map:
            self.probation_queue.remove(key)
            return self.probation_hash_map.pop(key)
        if key in self.protect_hash_map:
            self.protect_queue.remove(key)
            return self.protect_hash_map.pop(key)
