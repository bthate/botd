# BOTD - python3 IRC channel daemon.
#
# test Object and Persist

import json
import unittest

from bl.obj import Object, ObjectDecoder, ObjectEncoder, load, save, stamp, update

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
        p = save(o)
        load(o, p)
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
        update(o1, o2)
        self.assertEqual(o1._bla, "blaet")

    def test_iter(self):
        o1 = Object()
        o1.bla1 = 1
        o1.bla2 = 2
        o1.bla3 = 3
        res = sorted(list(o1))
        self.assertEqual(res, ["bla1","bla2","bla3"])

    def test_json1(self):
        o = Object()
        d = json.dumps(o, cls=ObjectEncoder)
        self.assertEqual(d, "{}")
        
    def test_json2(self):
        o = Object()
        o.test = "bla"
        d = json.dumps(o, cls=ObjectEncoder)
        oo = json.loads(d, cls=ObjectDecoder)
        self.assertEqual(oo.test, "bla")

    def test_jsonempty(self):
        o = json.loads("", cls=ObjectDecoder)
        self.assertEqual(type(o), Object)
        
    def test_jsonempty2(self):
        o = json.loads("{}", cls=ObjectDecoder)
        self.assertEqual(type(o), Object)
        
    def test_jsonattribute(self):
        o = Object()
        o.test = "bla"
        dstr = json.dumps(o, cls=ObjectEncoder)
        o = json.loads(dstr, cls=ObjectDecoder)
        self.assertEqual(o.test, "bla")

    def test_stamp(self):
        o = Object()
        o.test = Object()
        o.test.test = Object()
        stamp(o)
        self.assertTrue(o.test.test.stamp, "ob.obj.Object")

    def test_overload1(self):
        class O(object):
            def bla(self):
                print("yo!")
        o = O()
        o.bla = "mekker"
        self.assertTrue(o.bla, "mekker")                

    def test_overload2(self):
        class O(object):
            def bla(self):
                return "yo!"
        o = O()
        a = o.bla()
        self.assertTrue(a, "yo!")                

    def test_overload3(self):
        class O(object):
            def bla(self):
                return "yo!"
        o = O()
        setattr(o, "bla", "mekker")
        with self.assertRaises(TypeError):
            o.bla()
            
    def test_overload4(self):
        class O(Object):
            def bla(self):
                return "yo!"
        o = O()
        a = o.bla()
        self.assertTrue(a, "yo!")                
