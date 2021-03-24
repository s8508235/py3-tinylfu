from probables import BloomFilter


class Doorkeeper:
    def __init__(self, cap=100000, false_positive=0.01):
        self.bloom = BloomFilter(cap, false_positive)

    def __insert(self, key: str):
        already_present = self.bloom.check(key)
        self.bloom.add(key)
        return already_present

    def allow(self, key: str):
        return self.__insert(key)

    def reset(self):
        self.bloom.clear()
