# BOTD - python3 IRC channel daemon.
#
# kernel tests.

import logging
import os
import unittest

from bl.krn import Cfg

class Test_Kernel(unittest.TestCase):

    k = Kernel()

    def test_kernel(self):
        self.assertEqual(type(self.k.cfg), Cfg)
