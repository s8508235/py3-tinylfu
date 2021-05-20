import os, sys, inspect

current_dir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import lru


def test_lru_size_16():
    c = lru.LRUCache(16)
    c.set("1", 2)
    assert c.get("1") == 2
    assert len(c) == 1
    assert c.get("2") == None
    c.set("2_", "zz")
    assert c.get("1") == 2
    assert len(c) == 2
    assert c.get("2") == None
    assert c.get("2_") == "zz"


def test_lru_size_2():
    c = lru.LRUCache(2)
    c.set("1", 2)
    assert c.get("1") == 2
    assert len(c) == 1
    # test if evicted
    evicted_key, evicted_value, is_evicted = c.set("2", 3)
    assert evicted_key == ''
    assert evicted_value == None
    assert not is_evicted
    assert len(c) == 2
    assert c.is_cache_full()
    assert c.get("2") == 3
    # test if arrange order
    c.get("1")
    evicted_key, evicted_value, is_evicted = c.set("3", 4)
    assert evicted_key == "2"
    assert evicted_value == 3
    assert is_evicted == True
    evicted_key, evicted_value, is_evicted = c.set("4", 5)
    assert evicted_key == "1"
    assert evicted_value == 2
    assert is_evicted == True


def test_lru_size_2_remove():
    c = lru.LRUCache(2)
    c.set("1", 2)
    c.set("2", 3)
    assert c.remove("2") == 3
    assert c.get("2") == None
    assert c.get("1") == 2
    assert len(c) == 1