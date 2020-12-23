"test object functions"

import types
import unittest

from bot.dbs import last
from bot.obj import O, Object

class Test_Object(unittest.TestCase):

    def testO(self):
        o = O()
        self.assertEqual(type(o), O)

    def testObject(self):
        o = Object()
        self.assertEqual(type(o), Object)
    def test_intern1(self):
        o = Object()
        self.assertTrue(o.__type__)

    def test_intern2(self):
        o = Object()
        self.assertFalse(o)
        
    def test_intern3(self):
        o = Object()
        self.assertTrue("<bot.obj.Object object at" in repr(o))

    def test_intern4(self):
        o = Object()
        self.assertTrue(o.__type__ in str(type(o)))

    def test_intern5(self):
        o = Object()
        self.assertTrue(o.__id__)

    def test_empty(self):
        o = Object()
        self.assertTrue(not o) 

    def test_final(self):
        o = Object()
        o.last = "bla"
        last(o)
        self.assertEqual(o.last, "bla")

    def test_stamp(self):
        o = Object()
        o.save()
        self.assertTrue(o.__type__)

    def test_attribute(self):
        o = Object()
        o.bla = "test"
        p = o.save()
        oo = Object()
        oo.load(p)
        self.assertEqual(oo.bla, "test")

    def test_changeattr(self):
        o = Object()
        o.bla = "test"
        p = o.save()
        oo = Object()
        oo.load(p)
        oo.bla = "mekker"
        pp = oo.save()
        ooo = Object()
        ooo.load(pp)
        self.assertEqual(ooo.bla, "mekker")

    def test_last(self):
        o = Object()
        o.bla = "test"
        o.save()
        oo = Object()
        last(oo)
        self.assertEqual(oo.bla, "test")

    def test_lastest(self):
        o = Object()
        o.bla = "test"
        o.save()
        oo = Object()
        last(oo)
        oo.bla = "mekker"
        oo.save()
        ooo = Object()
        last(ooo)
        self.assertEqual(ooo.bla, "mekker")
