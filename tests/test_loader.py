# BOTD - IRC channel daemon
#
# loader tests.

import os
import unittest

from botd.krn import kernels
from botd.ldr import Loader

k = kernels.get_first()

class Test_Loader(unittest.TestCase):

    def test_loadmod(self):
        l = Loader()
        l.load_mod("botd.ldr")
        p = l.save()
        ll = Loader()
        ll.load(p)
        self.assertTrue("botd.ldr" in ll.table)

    def test_loadmod(self):
        l = Loader()
        l.load_mod("botd.cmd")
        self.assertTrue("botd.cmd" in l.table)
