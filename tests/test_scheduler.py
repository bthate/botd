# BOTD - python3 IRC channel daemon.
#
# scheduler tests

import unittest

from bl.evt import Event
from bl.krn import Kernel

k = Kernel()
k.start()

class Test_Scheduler(unittest.TestCase):

    def test_scheduler_put(self):
        e = Event()
        e.origin = "root@shell"
        e.txt = "v"
        k.put(e)
        e.wait()
        self.assertTrue(e.result and "BOTD" in e.result[0])
