from probables import CountMinSketch


class CM4:
    def __init__(self, width=128):
        if width < 1:
            raise RuntimeError("bad width for cm4")
        self.cm4 = CountMinSketch(width, 4)
        self.keys = set()

    def add(self, key: str):
        self.cm4.add(key)
        self.keys.add(key)

    def estimate(self, key: str):
        return self.cm4.check(key)

    def reset(self):
        for key in self.keys.copy():
            down = self.cm4.check(key) >> 1 & 9223372036854775807
            # if down > 1, it will be half of the count
            if down == 0:
                down = 1
                self.keys.discard(key)
            self.cm4.remove(key, down)
