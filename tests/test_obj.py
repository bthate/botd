""" object unittests. """

import os
import time
import unittest

from ob import Object

class Test_Object(unittest.TestCase):

    def test_checkattribute(self):
        o = Object()
        with self.failUnlessRaises(AttributeError):
            o.blabla

    def test_construct(self):
        o = Object()
        self.assertEqual(type(o), Object)

    def test_cleanpath(self):
        o = Object()
        self.assertEqual(str(o), '{}')

    def test_depth(self):
        o = Object()
        o.state = Object()
        o.state.starttime = time.time()
        self.assertTrue(isinstance(o.state.starttime, float)) 

    def test_settingattribute(self):
        o = Object()
        o.bla = "mekker"
        self.assertEqual(o.bla, "mekker")

    def test_typed(self):
        o = Object()
        self.assertEqual(o.__class__.__name__, "Object")
        
    def test_underscore(self):
        o = Object()
        o._bla = "mekker"
        self.assertEqual(o._bla, "mekker")
