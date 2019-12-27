# BOTD - python3 IRC channel daemon.
#
# edit command tests.

import json
import logging
import os
import unittest

from bl.evt import Event
from bl.krn import Kernel

class Test_Ed(unittest.TestCase):

    k = Kernel()

    def setUp(self):
        self.k.start()
        
    def test_ed1(self):
        e = Event()
        e.parse("ed log txt==bla txt=mekker")
        self.k.put(e)
        e.wait()
        self.assertEqual(e.result, [])
