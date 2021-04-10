from collections import deque
from typing import Tuple
# what will happen if cache None


class LRUCache:
    def __init__(self, cache_size):
        self.cache_size = cache_size
        self.queue = deque()
        self.hash_map = dict()

    def is_queue_full(self):
        return len(self.queue) == self.cache_size

    def __len__(self):
        return len(self.queue)

    def __contains__(self, key) -> bool:
        return key in self.queue

    def set(self, key: str, value) -> Tuple[str, object, bool]:
        if key not in self.hash_map:
            if self.is_queue_full():
                old_key = self.queue.pop()
                old_value = self.hash_map.pop(old_key)
                self.queue.appendleft(key)
                self.hash_map[key] = value
                return old_key, old_value, True if key != old_key else False
            else:
                self.queue.appendleft(key)
                self.hash_map[key] = value
                return "", None, False
        else:
            self.queue.remove(key)
            self.queue.appendleft(key)
            self.hash_map[key] = value
            return "", None, False

    def get(self, key: str):
        if key in self.hash_map:
            self.queue.remove(key)
            self.queue.appendleft(key)
            return self.hash_map[key]

    def remove(self, key: str) -> object:
        if key in self.hash_map:
            self.queue.remove(key)
            return self.hash_map.pop(key)
        return None
