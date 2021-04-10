import os, sys, inspect

current_dir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import tinylfu


def test_tinylfu():
    t = tinylfu.TinyLFU()
    # test if same key in different cache entry