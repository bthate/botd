# BOTD - python3 IRC channel daemon.
#
# test Object and Persist

import unittest

from bl.obj import Object

class Test_Base(unittest.TestCase):

    def test_construct(self):
        o = Object()
        self.assertEqual(type(o), Object)

    def test_cleanpath(self):
        o = Object()
        self.assertEqual(str(o), "{}")

    def test_clean(self):
        o = Object()
        self.assertTrue(not o)

    def test_cleanload(self):
        o = Object()
        o.test = "bla"
        p = o.save()
        o.load(p)
        self.assertEqual(type(o), Object)

    def test_settingattribute(self):
        o = Object()
        o.bla = "mekker"
        self.assertEqual(o.bla, "mekker")

    def test_checkattribute(self):
        o = Object()
        with self.failUnlessRaises(AttributeError):
            o.mekker

    def test_underscore(self):
        o = Object()
        o._bla = "mekker"
        self.assertEqual(o._bla, "mekker")

    def test_update(self):
        o1 = Object()
        o1._bla = "mekker"
        o2 = Object()
        o2._bla = "blaet"
        o1.update(o2)
        self.assertEqual(o1._bla, "blaet")

    def test_iter(self):
        o1 = Object()
        o1.bla1 = 1
        o1.bla2 = 2
        o1.bla3 = 3
        res = sorted(list(o1))
        self.assertEqual(res, ["bla1","bla2","bla3"])
