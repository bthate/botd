# BOTLIB - Framework to program bots (a botlib).
#
# scheduler tests

import unittest

from botd.evt import Event
from botd.krn import kernels

k = kernels.get_first()

class Test_Scheduler(unittest.TestCase):

    def test_scheduler_put(self):
        e = Event()
        e.etype = "command"
        e.orig = repr(k)
        e.origin = "root@shell"
        e.txt = "v"
        e.verbose = k.cfg.verbose
        k.put(e)
        e.wait()
        self.assertTrue(e.result and "BOTD" in e.result[0])
