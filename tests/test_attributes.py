# BOTLIB - Framework to program bots (a botlib).
#
# tests attributes on Objects

from botd.obj import Object

import unittest
import time

class Test_Attribute(unittest.TestCase):

    def timed(self):
        with self.assertRaises((AttributeError, )):
            o = Object()
            o.timed2

    def timed2(self):
        o = Object()
        o.date = time.ctime(time.time())
        self.assert_(o.timed())
