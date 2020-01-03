# BOTD - python3 IRC channel daemon.
#
# database tests.

import unittest

from bl.dbs import Db
from bl.err import ENOFILE

class Test_Store(unittest.TestCase):

    def test_emptyargs(self):
        db = Db()
        res = list(db.find("", {}))
        self.assertEqual(res, [])
