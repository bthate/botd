# BOTLIB - Framework to program bots.
#
# 

import bl
import os
import unittest

class ENOTCOMPAT(Exception):
    pass

class Test_Core(unittest.TestCase):

    def test_load2(self):
        o = bl.pst.Persist()
        o.bla = "mekker"
        p = o.save()
        oo = bl.pst.Persist().load(p)
        self.assertEqual(oo.bla, "mekker")

    def test_save(self):
        o = bl.pst.Persist()
        p = o.save()
        self.assertTrue(os.path.exists(os.path.join(bl.workdir, "store", p)))

    def test_subitem(self):
        o = bl.pst.Persist()
        o.test = bl.pst.Persist()
        p = o.save()
        oo = bl.pst.Persist().load(p)
        self.assertTrue(type(oo.test), bl.pst.Persist)
