# BOTLIB - Framework to program bots (a botlib).
#
# scheduler tests

import unittest

from botd.hdl import Event
from botd.krn import kernels

k = kernels.get(0)

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
