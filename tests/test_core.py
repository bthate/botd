# BOTLIB - Framework to program bots.
#
# 

import os
import unittest

from bl.pst import Persist, workdir

class ENOTCOMPAT(Exception):
    pass

class Test_Core(unittest.TestCase):

    def test_load2(self):
        o = Persist()
        o.bla = "mekker"
        p = o.save()
        oo = Persist().load(p)
        self.assertEqual(oo.bla, "mekker")

    def test_save(self):
        o = Persist()
        p = o.save()
        self.assertTrue(os.path.exists(os.path.join(workdir, "store", p)))

    def test_subitem(self):
        o = Persist()
        o.test = Persist()
        p = o.save()
        oo = Persist().load(p)
        self.assertTrue(type(oo.test), Persist)
