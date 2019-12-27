# BOTD - python3 IRC channel daemon.
#
# loader tests.

import bl
import os
import unittest

class Test_Loader(unittest.TestCase):

    def test_loadmod(self):
        l = bl.ldr.Loader()
        l.load_mod("bl.ldr")
        p = l.save()
        ll = bl.ldr.Loader()
        ll.load(p)
        self.assertTrue("bl.ldr" in ll.table)
