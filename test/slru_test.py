from slru import RESULT, SLRUCache
import os, sys, inspect

current_dir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


def test_slru_size_16_4():
    c = SLRUCache(16, 4)
    c.set("1", 2)
    assert c.probation.cache.keys() == {"1"}
    assert c.get("1") == 2
    assert len(c) == 1
    assert c.get("2") == None
    c.set("2_", "zz")
    assert c.get("1") == 2
    assert len(c) == 2
    assert c.get("2") == None
    assert c.get("2_") == "zz"
    assert c.protect.cache.keys() == {"2_", "1"}
    assert len(c.probation.cache.keys()) == 0
    assert c.victim() == None


def test_slru_size_2_1():
    c = SLRUCache(2, 1)
    c.set("1", 2)
    assert len(c.protect) == 0
    assert len(c.probation) == 1
    assert c.victim() == None
    # test if go to protect queue
    assert c.get("1") == 2
    assert len(c) == 1
    assert len(c.protect) == 1
    assert len(c.probation) == 0
    # test if go to probation queue
    c.set("2", 3)
    assert len(c.protect) == 1
    assert len(c.probation) == 1
    assert c.get("1") == 2
    assert len(c) == 2
    # test if 1 go to probation queue 2 go to protect queue
    assert c.get("2") == 3
    assert len(c.protect) == 1
    assert c.probation.cache.keys() == {"1"}
    assert c.protect.cache.keys() == {"2"}
    assert len(c.probation) == 1
    c.set("3", 4)
    assert len(c) == 3
    assert len(c.protect) == 1
    assert len(c.probation) == 2
    assert c.probation.cache.keys() == {"1", "3"}
    assert c.protect.cache.keys() == {"2"}
    # test if key 3 go to protect queue others go to probation queue
    value = c.get("3")
    assert len(c) == 3
    assert len(c.protect) == 1
    assert len(c.probation) == 2
    assert value == 4
    assert c.protect.cache["3"][RESULT] == 4
    assert c.probation.cache.keys() == {"1", "2"}
    # test if order is right
    assert c.victim() == "1"


def test_slru_victim_size_3_2():
    c = SLRUCache(3, 2)
    c.set("1", 2)
    c.set("2", 3)
    c.set("3", 4)
    c.get("2")
    c.get("3")
    c.set(4, 4)
    c.set(5, 5)
    assert c.victim() == "1"
    assert c.get("1") == 2
    assert c.victim() == 4