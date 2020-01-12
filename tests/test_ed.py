# BOTLIB - Framework to program bots (a botlib).
#
# edit command tests.

import json
import logging
import os
import unittest

from botd.krn import Kernel
from botd.prs import Command
class Test_Ed(unittest.TestCase):

    k = Kernel()

        
    def test_ed1(self):
        e = Command()
        e.parse("ed log txt==bla txt=mekker")
        self.k.dispatch(e)
        e.wait()
        self.assertEqual(e.result, [])
