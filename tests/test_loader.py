# BOTLIB - Framework to program bots (a botlib).
#
# loader tests.

import os
import unittest

from botd.ldr import Loader

class Test_Loader(unittest.TestCase):

    def test_loadmod(self):
        l = Loader()
        l.walk("botd.ldr")
        p = l.save()
        ll = Loader()
        ll.load(p)
        self.assertTrue("cmds" in ll)

    def test_getmods1(self):
        l = Loader()
        mods = l.walk("botd")
        self.assertTrue("botd.flt" in [x.__name__ for x in mods])

    def test_bl(self):
        l = Loader()
        l.walk("botd")
        self.assertTrue("botd.obj.Object" in l.names.values())

    def test_botd(self):
        l = Loader()
        l.walk("botd")
        self.assertTrue("botd.udp.UDP" in l.names.values())
