# BOTD - python3 IRC channel daemon.
#
# scheduler tests

import unittest

from bl.hdl import Event
from bl.krn import Kernel

k = Kernel()
k.walk("botd.cmd")
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
        self.assertTrue(e.result and "BOTD" in e.result[0])
