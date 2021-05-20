from lru import LRUCache

PREV, NEXT, KEY, RESULT = 0, 1, 2, 3  # names for the link fields


class SLRUCache:
    def __init__(self, probation_cap, protect_cap):
        self.probation_cap = probation_cap
        self.protect_cap = protect_cap
        self.probation = LRUCache(probation_cap)
        self.protect = LRUCache(protect_cap)

    def __len__(self) -> int:
        return len(self.protect) + len(self.probation)

    def __contains__(self, key) -> bool:
        return key in self.protect or key in self.probation

    def victim(self) -> str:
        if len(self) < (self.protect_cap + self.probation_cap):
            return None
        victim = self.probation.root[NEXT]
        return victim[KEY]

    def get(self, key: str) -> object:
        if key in self.protect:
            return self.protect.get(key)

        if key in self.probation:
            if len(self.protect) < self.protect_cap:
                # remove from probation
                result = self.probation.remove(key)
                # add to protect
                self.protect.set(key, result)
                return result
            # remove from probation and append to protect
            result = self.probation.remove(key)
            # remove from protect and append to probation
            protect_last = self.protect.root[NEXT]
            protect_last_key = protect_last[KEY]
            protect_last_result = self.protect.remove(protect_last_key)
            self.protect.set(key, result)
            self.probation.set(protect_last_key, protect_last_result)
            return result

    def set(self, key: str, result: object):
        if len(self.probation) < self.probation_cap:
            self.probation.set(key, result)
            return
        if key not in self.probation:
            self.remove(self.victim())

        self.probation.set(key, result)

    def remove(self, key: str) -> object:
        if key in self.probation:
            return self.probation.remove(key)
        if key in self.protect:
            return self.protect.remove(key)
        return None