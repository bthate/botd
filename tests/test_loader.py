# BOTD - python3 IRC channel daemon.
#
# loader tests.

import bl
import os
import unittest

from bl.obj import load, save, values
from bl.ldr import Loader

class Test_Loader(unittest.TestCase):

    def test_loadmod(self):
        l = Loader()
        l.walk("bl.ldr")
        p = save(l)
        ll = Loader()
        load(ll, p)
        self.assertTrue("cmds" in ll)

    def test_getmods1(self):
        l = Loader()
        mods = l.walk("bl")
        self.assertTrue("bl.flt" in [x.__name__ for x in mods])

    def test_getmods2(self):
        l = Loader()
        mods = l.walk("botd")
        self.assertTrue("botd.cmd" in [x.__name__ for x in mods])

    def test_bl(self):
        l = Loader()
        l.walk("bl")
        self.assertTrue("bl.obj.Object" in values(l.names))

    def test_botd(self):
        l = Loader()
        l.walk("botd")
        self.assertTrue("botd.udp.UDP" in values(l.names))
