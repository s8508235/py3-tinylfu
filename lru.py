from typing import Tuple
# port from functools

PREV, NEXT, KEY, RESULT = 0, 1, 2, 3  # names for the link fields


class LRUCache:
    def __init__(self, cache_size=128):
        self.cache_size = cache_size
        self.cache = {}
        self.cache_get = self.cache.get
        self.root = []  # root of the circular doubly linked list
        self.root[:] = [self.root, self.root, None,
                        None]  # initialize by pointing to self

    def is_cache_full(self):
        return len(self.cache) == self.cache_size

    def __len__(self):
        return len(self.cache)

    def __contains__(self, key) -> bool:
        return key in self.cache

    def set(self, key: str, result: object) -> Tuple[str, object, bool]:
        if key not in self.root:
            if self.is_cache_full():
                # Use the old root to store the new key and result.
                oldroot = self.root
                oldroot[KEY] = key
                oldroot[RESULT] = result
                # Empty the oldest link and make it the new root.
                # Keep a reference to the old key and old result to
                # prevent their ref counts from going to zero during the
                # update. That will prevent potentially arbitrary object
                # clean-up code (i.e. __del__) from running while we're
                # still adjusting the links.
                self.root = oldroot[NEXT]
                oldkey = self.root[KEY]
                oldresult = self.root[RESULT]
                self.root[KEY] = self.root[RESULT] = None
                # Now update the cache dictionary.
                del self.cache[oldkey]
                # Save the potentially reentrant cache[key] assignment
                # for last, after the root and links have been put in
                # a consistent state.
                self.cache[key] = oldroot
                return oldkey, oldresult, True if key != oldkey else False
            else:
                last = self.root[PREV]
                link = [last, self.root, key, result]
                last[NEXT] = self.root[PREV] = self.cache[key] = link
                return "", None, False
        else:
            link = self.cache_get(key)
            link_prev, link_next, _key, result = link
            # remove from original position
            link_prev[NEXT] = link_next
            link_next[PREV] = link_prev
            # add to head
            last = self.root[PREV]
            link[KEY] = result
            last[NEXT] = self.root[PREV] = link
            link[PREV] = last
            link[NEXT] = self.root
            return "", None, False

    def get(self, key: str) -> object:
        link = self.cache_get(key)
        if link is not None:
            link_prev, link_next, _key, result = link
            link_prev[NEXT] = link_next
            link_next[PREV] = link_prev
            last = self.root[PREV]
            last[NEXT] = self.root[PREV] = link
            link[PREV] = last
            link[NEXT] = self.root
            return result

    def remove(self, key: str) -> object:
        link = self.cache_get(key)
        if link is not None:
            link_prev, link_next, _key, result = link
            link_prev[NEXT] = link_next
            link_next[PREV] = link_prev
            del self.cache[key]
            return result
