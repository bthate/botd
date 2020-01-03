# BOTD - python3 IRC channel daemon.
#
# test load/save

import json
import os
import unittest

from bl.obj import Object, workdir

class ENOTCOMPAT(Exception):
    pass

class Test_Core(unittest.TestCase):

    def test_load2(self):
        o = Object()
        o.bla = "mekker"
        p = o._save()
        oo = Object()._load(p)
        self.assertEqual(oo.bla, "mekker")

    def test_save(self):
        o = Object()
        p = o._save()
        self.assertTrue(os.path.exists(os.path.join(workdir, "store", p)))

    def test_subitem(self):
        o = Object()
        o.test2 = Object()
        p = o._save()
        oo = Object()
        oo._load(p)
        self.assertTrue(type(oo.test2), Object)

    def test_subitem2(self):
        o = Object()
        o.test = Object()
        o.test.bla = "test"
        p = o._save()
        oo = Object()._load(p)
        self.assertTrue(type(oo.test.bla), "test")
