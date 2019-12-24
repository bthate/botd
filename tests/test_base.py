# BOTLIB - Framework to program bots.
#
# 

import bl
import unittest

class Test_Base(unittest.TestCase):

    def test_construct(self):
        o = bl.Object()
        self.assertEqual(type(o), bl.Object)

    def test_cleanpath(self):
        o = bl.Object()
        self.assertEqual(str(o), "{}")

    def test_clean(self):
        o = bl.Object()
        self.assertTrue(not o)

    def test_cleanload(self):
        o = bl.pst.Persist()
        o.test = "bla"
        p = o.save()
        o.load(p)
        self.assertEqual(type(o), bl.pst.Persist)

    def test_settingattribute(self):
        o = bl.Object()
        o.bla = "mekker"
        self.assertEqual(o.bla, "mekker")

    def test_checkattribute(self):
        o = bl.Object()
        with self.failUnlessRaises(AttributeError):
            o.mekker

    def test_underscore(self):
        o = bl.Object()
        o._bla = "mekker"
        self.assertEqual(o._bla, "mekker")

    def test_update(self):
        o1 = bl.Object()
        o1._bla = "mekker"
        o2 = bl.Object()
        o2._bla = "blaet"
        bl.update(o1, o2)
        self.assertEqual(o1._bla, "blaet")

    def test_iter(self):
        o1 = bl.Object()
        o1.bla1 = 1
        o1.bla2 = 2
        o1.bla3 = 3
        res = sorted(list(o1))
        self.assertEqual(res, ["bla1","bla2","bla3"])
