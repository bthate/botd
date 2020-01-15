# BOTLIB - Framework to program bots (a botlib).
#
# edit command tests.

import json
import logging
import os
import unittest

from botd.krn import kernels
from botd.prs import Command

k = kernels.get_first()

class Test_Ed(unittest.TestCase):

    def test_ed1(self):
        e = Command()
        e.parse("ed log txt==bla txt=mekker")
        k.put(e)
        e.wait()
        self.assertEqual(e.result, [])
