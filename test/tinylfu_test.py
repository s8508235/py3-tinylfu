import os, sys, inspect

current_dir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import tinylfu


def test_tinylfu():
    t = tinylfu.TinyLFU(size=3)
    # test if same key in different cache entry
    t.set("a", 1)  # a
    assert t.get("a") == 1
    assert len(t.lru) == 1
    assert len(t.slru) == 0
    # a goes to slru
    t.set("b", 2)  # b / a
    assert t.get("a") == 1
    assert len(t.slru) == 1
    assert len(t.lru) == 1
    t.set("a", "1")  # a / b
    assert len(t.slru) == 1
    assert len(t.lru) == 1
    assert t.get("a") == "1"
    t.set("c", 3)  # c / a -> b
    assert len(t.slru) == 2
    assert len(t.lru) == 1
    # fill out cache
    t.set("d", 4)  # d / c -> a b
    assert t.get("c") == 3
    assert t.get("b") == 2
    assert t.get("a") == "1"
    assert len(t.slru) == 3
    assert len(t.lru) == 1
    t.set("e", 5)  # e / c -> a b
    assert len(t.slru) == 3
    assert len(t.lru) == 1
    assert t.doorkeeper.allow("d") == True
    t.set("e", "5")  # e / c -> a b
    assert len(t.slru) == 3
    assert len(t.lru) == 1
    assert t.get("e") == "5"
    assert t.get("c") == 3
    assert t.get("b") == 2
    assert t.get("a") == "1"
    # d evict since not doorkeeper
    assert t.slru.get("d") == None
    t.set("d", "4")  # d / c -> a b
    assert len(t.slru) == 3
    assert len(t.lru) == 1
    assert t.get("c") == 3
    assert t.get("b") == 2
    assert t.get("a") == "1"
    assert t.slru.victim() == "c"
    # evict since not passing admission
    assert t.slru.get("e") == None
    # d will not pass admission since counter check
    t.set("f", 6)  # f / c-> a b
    assert t.get("d") == None
    assert t.get("f") == 6
    assert t.get("f") == 6
    assert t.get("f") == 6
    assert t.get("f") == 6
    # f will not pass admission since doorkeeper
    t.set("g", 7)  # g / c -> a b
    # f will pass admission and count check
    t.set("f", "6")
    t.set("g", "7")  # g / f -> a b
    assert t.get("c") == None
    assert t.get("f") == "6"
    # print(t.lru.queue, t.slru.probation_queue, t.slru.protect_queue)


def test_tinylfu_cache():
    @tinylfu.TinyLFUCache(cache_size=3)
    def my_getter(key: str):
        if len(key) == 1:
            return ord(key)
        else:
            return None

    assert my_getter("abc") == None
    assert my_getter("a") == 97
    assert my_getter("b") == 98
    assert my_getter("a") == 97
