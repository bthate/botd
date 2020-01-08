# BOTLIB - Framework to program bots (a botlib).
#
# kernel tests.

import logging
import os
import unittest

from botd.krn import Kernel, Cfg

class Test_Kernel(unittest.TestCase):

    k = Kernel()

    def test_kernel(self):
        self.assertEqual(type(self.k.cfg), Cfg)
