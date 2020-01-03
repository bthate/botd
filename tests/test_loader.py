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
        p = l.save()
        ll = Loader()
        ll.load(p)
        self.assertTrue("cmds" in ll)

    def test_getmods1(self):
        l = Loader()
        mods = l.get_mods("bl")
        self.assertTrue("bl.flt" in [x.__name__ for x in mods])

    def test_getmods2(self):
        l = Loader()
        mods = l.get_mods("botd")
        self.assertTrue("botd.cmd" in [x.__name__ for x in mods])

    def test_names(self):
        l = Loader()
        l.walk("bl")
        l.walk("botd")
        print(l.names)
        self.assertTrue("botd.cmd" in l.names)           