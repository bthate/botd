# BOTD - python3 IRC channel daemon.
#
# fuzzer tests.

import logging
import random
import unittest
import bl.tbl

from bl.krn import Kernel
from bl.typ import get_cls

from botd.usr import Users

k = Kernel()
k.cfg.prompt = False
k.walk("botd")
k.start()

users = Users()
users.oper("test@shell")

class Test_Fuzzer(unittest.TestCase):

    def test_fuzzer1(self):
        for t in bl.tbl.classes:
            for key in bl.tbl.names:
                try:
                    e = get_cls(t)()
                    e.verbose = k.cfg.verbose
                    e.txt = key + " " + random.choice(list(bl.tbl.names))
                    e.parse(e.txt)
                    e.orig = repr(k)
                    e.origin = "test@shell"
                    v = k.get_cmd(key)
                    if v:
                        v(e)
                except AttributeError:
                    pass
                except TypeError as ex:
                    break
        self.assertTrue(True)
