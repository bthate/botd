# BOTD - python3 IRC channel daemon.
#
# configuration tests

import unittest

from bl import Default

class O(Default):

    def bla(self):
        return "yo!"

class Test_Default(unittest.TestCase):

    def test_defaultiter(self):
        d = Default()
        d.bla = "mekker"
        self.assertTrue("bla" in d)

    def test_default1(self):
        o = O()
        o.bla = "bla"
        with self.assertRaises(TypeError) as x:
            res = o.bla()

    def test_defaultattribute(self):
        cfg = Default()
        cfg.last = "bla"
        self.assertEqual(cfg.last, "bla")

    def test_defaultattribute2(self):
        cfg = Default()
        cfg.last = "bla"
        with self.assertRaises(TypeError) as x:
            l = cfg.last()
