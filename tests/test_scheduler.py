# BOTLIB - Framework to program bots (a botlib).
#
# scheduler tests

import unittest

from bl.hdl import Event
from bl.krn import Kernel

k = Kernel()
k.walk("bl")
k.start()

class Test_Scheduler(unittest.TestCase):

    def test_scheduler_put(self):
        e = Event()
        e.orig = repr(k)
        e.origin = "root@shell"
        e.txt = "v"
        e.verbose = k.cfg.verbose
        k.dispatch(e)
        e.wait()
        self.assertTrue(e.result and "BOTLIB" in e.result[0])
