# BOTLIB - Framework to program bots
#
# 

import bl
import unittest

class Test_Scheduler(unittest.TestCase):

    def test_scheduler_put(self):
        e = bl.evt.Event()
        e.origin = "root@shell"
        e.txt = "show version"
        bl.k.put(e)
        e.wait()
        self.assertTrue(e.result and "BOTLIB" in e.result[0])
