# BOTLIB - Framework to program bots (a botlib).
#
# test load/save

import json
import os
import unittest

from botd.obj import Object, workdir

class ENOTCOMPAT(Exception):
    pass

class Test_Core(unittest.TestCase):

    def test_load2(self):
        o = Object()
        o.bla = "mekker"
        p = o.save()
        oo = Object().load(p)
        self.assertEqual(oo.bla, "mekker")

    def test_save(self):
        o = Object()
        p = o.save()
        self.assertTrue(os.path.exists(os.path.join(workdir, "store", p)))

    def test_subitem(self):
        o = Object()
        o.test2 = Object()
        p = o.save()
        oo = Object()
        oo.load(p)
        self.assertTrue(type(oo.test2), Object)

    def test_subitem2(self):
        o = Object()
        o.test = Object()
        o.test.bla = "test"
        p = o.save()
        oo = Object().load(p)
        self.assertTrue(type(oo.test.bla), "test")
