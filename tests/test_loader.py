# BOTD - python3 IRC channel daemon.
#
# loader tests.

import bl
import os
import unittest

class Test_Loader(unittest.TestCase):

    def test_loadmod(self):
        l = bl.ldr.Loader()
        l.walk("bl.ldr")
        p = l.save()
        ll = bl.ldr.Loader()
        ll.load(p)
        self.assertTrue("cmds" in ll)
