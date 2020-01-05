# BOTD - python3 IRC channel daemon.
#
# test load/save

import json
import os
import unittest

from bl.obj import Object, load, save, workdir

class ENOTCOMPAT(Exception):
    pass

class Test_Core(unittest.TestCase):

    def test_load2(self):
        o = Object()
        o.bla = "mekker"
        p = save(o)
        oo = load(Object(), p)
        self.assertEqual(oo.bla, "mekker")

    def test_save(self):
        o = Object()
        p = save(o)
        self.assertTrue(os.path.exists(os.path.join(workdir, "store", p)))

    def test_subitem(self):
        o = Object()
        o.test2 = Object()
        p = save(o)
        oo = Object()
        load(oo, p)
        self.assertTrue(type(oo.test2), Object)

    def test_subitem2(self):
        o = Object()
        o.test = Object()
        o.test.bla = "test"
        p = save(o)
        oo = load(Object(), p)
        self.assertTrue(type(oo.test.bla), "test")
