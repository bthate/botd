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
users = Users()

k.cfg.prompt = False
k.walk("botd")
users.oper("test@shell")

class Test_Fuzzer(unittest.TestCase):

    def test_fuzzer1(self):
        for key in bl.tbl.modules:
            for n in bl.tbl.names:
                t = bl.tbl.names[n]
                try:
                    e = get_cls(t)()
                    e.txt = key + " " + random.choice(list(bl.tbl.names))
                    e.parse(e.txt)
                    e.orig = repr(b)
                    e.origin = "test@shell"
                    e.update(o)
                    v = k.get_cmd(key)
                    if v:
                        v(e)
                except AttributeError:
                    pass
                except TypeError as ex:
                    break
        self.assertTrue(True)
