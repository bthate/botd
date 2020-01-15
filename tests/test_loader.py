# BOTLIB - Framework to program bots (a botlib).
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
        l.walk("botd.ldr")
        p = l.save()
        ll = Loader()
        ll.load(p)
        self.assertTrue("botd.ldr" in ll.table)

    def test_getmods1(self):
        l = Loader()
        mods = l.walk("botd")
        self.assertTrue("botd.flt" in [x.__name__ for x in mods])

    def test_botd(self):
        l = Loader()
        l.walk("botd.cmds")
        self.assertTrue("v" in k.cmds)
