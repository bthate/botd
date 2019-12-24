""" database tests """

import unittest

from ob import k

class Test_Store(unittest.TestCase):

    def test_emptyargs(self):
        res = k.db.find("", {})
        self.assertEqual(list(res), [])

    def test_emptyargs2(self):
        res = k.db.find("", {})
        self.assertEqual(list(res), [])
