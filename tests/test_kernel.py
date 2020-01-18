# BOTD - IRC channel daemon
#
# kernel tests.

import logging
import os
import unittest

from botd.krn import kernels, Cfg

k = kernels.get_first()

class Test_Kernel(unittest.TestCase):

    def test_kernel(self):
        self.assertEqual(type(k.cfg), Cfg)

    def test_cmds(self):
        k.load_mod("botd.cmd")
        self.assertTrue("cmds" in k.cmds)

    def test_walk(self):
        mods = k.walk("botd")
        self.assertTrue("botd.flt" in [x.__name__ for x in mods])
