# BOTLIB - Framework to program bots (a botlib).
#
# database tests.

import unittest

from botd.dbs import Db
from botd.err import ENOFILE

class Test_Store(unittest.TestCase):

    def test_emptyargs(self):
        db = Db()
        res = list(db.find("", {}))
        self.assertEqual(res, [])
