# BOTD - python3 IRC channel daemon.
#
# loader tests.

import bl
import os
import unittest

from bl.ldr import Loader

class Test_Loader(unittest.TestCase):

    def test_loadmod(self):
        l = Loader()
        l.walk("bl.ldr")
        p = l._save()
        ll = Loader()
        ll._load(p)
        self.assertTrue("cmds" in ll)

    def test_getmods1(self):
        l = Loader()
        mods = l.get_mods("bl")
        self.assertTrue("bl.flt" in [x.__name__ for x in mods])

    def test_getmods2(self):
        l = Loader()
        mods = l.get_mods("botd")
        self.assertTrue("botd.cmd" in [x.__name__ for x in mods])

    def test_bl(self):
        l = Loader()
        l.walk("bl.all")
        l.walk("bl")
        self.assertTrue("bl.obj.Object" in l.names._values())

    def test_botd(self):
        l = Loader()
        l.walk("botd.all")
        l.walk("botd")
        self.assertTrue("botd.udp.UDP" in l.names._values())
