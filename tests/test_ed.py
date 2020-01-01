# BOTD - python3 IRC channel daemon.
#
# edit command tests.

import json
import logging
import os
import unittest

from bl.krn import Kernel
from bl.prs import Command
class Test_Ed(unittest.TestCase):

    k = Kernel()

    def setUp(self):
        self.k.start()
        
    def test_ed1(self):
        e = Command()
        e.parse("ed log txt==bla txt=mekker")
        self.k.dispatch(e)
        e.wait()
        self.assertEqual(e.result, [])
