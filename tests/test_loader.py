# BOTLIB - Framework to program bots (a botlib).
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
        mods = l.walk("bl")
        self.assertTrue("bl.flt" in [x.__name__ for x in mods])

    def test_bl(self):
        l = Loader()
        l.walk("bl")
        self.assertTrue("bl.obj.Object" in l.names.values())

    def test_botd(self):
        l = Loader()
        l.walk("bl")
        self.assertTrue("bl.udp.UDP" in l.names.values())
