""" edit command tests. """

import json
import logging
import os
import unittest

from ob import k
from ob.evt import Event

class Test_Ed(unittest.TestCase):

    def setUp(self):
        k.start()
        
    def test_ed1(self):
        e = Event()
        e.parse("ed log txt==bla txt=mekker")
        k.put(e)
        e.wait()
        self.assertEqual(e.result, [])
