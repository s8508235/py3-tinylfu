import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import cm4

def test_cm4_width_100():
    c = cm4.CM4(100)
    # test if cm4 count correctly with easy operation
    c.add("w")
    c.add("w")
    c.add("w")
    assert c.estimate("w") == 3
    # test if cm4 count correctly resetting
    c.reset()
    assert c.estimate("w") == 2
    c.add("w")
    assert c.estimate("w") == 3
    c.add("ww")
    assert c.estimate("w") == 3
    assert c.estimate("ww") == 1
    c.reset()
    assert c.estimate("w") == 2
    assert c.estimate("ww") == 0
