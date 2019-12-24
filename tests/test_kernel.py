import logging
import ob
import os
import unittest

from ob import k
from ob.krn import Cfg

class Test_Kernel(unittest.TestCase):

    def test_kernel(self):
        self.assertEqual(type(k.cfg), Cfg)
