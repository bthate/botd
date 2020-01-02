# BOTD - python3 IRC channel daemon.
#
# loader tests.

import bl
import os
import unittest

class Test_Loader(unittest.TestCase):

    def test_loadmod(self):
        l = bl.ldr.Loader()
        l.walk("bl.ldr")
        p = l.save()
        ll = bl.ldr.Loader()
        ll.load(p)
        self.assertTrue("cmds" in ll)

    def test_getmods1(self):
        l = bl.ldr.Loader()
        mods = l.get_mods("bl")
        self.assertTrue("bl.flt" in [x.__name__ for x in mods])

    def test_getmods2(self):
        l = bl.ldr.Loader()
        mods = l.get_mods("botd")
        self.assertTrue("botd.cmd" in [x.__name__ for x in mods])
           