# BOTLIB - Framework to program bots (a botlib).
#
# fuzzer tests.

import logging
import random
import unittest
import botd.tbl

from botd.krn import Kernel
from botd.typ import get_cls
from botd.usr import Users

k = Kernel()
k.cfg.prompt = False
k.walk("botd")

users = Users()
users.oper("test@shell")

class Test_Fuzzer(unittest.TestCase):

    def test_fuzzer1(self):
        for t in botd.tbl.names.values():
            for key in botd.tbl.names:
                try:
                    e = get_cls(t)()
                    e.verbose = k.cfg.verbose
                    e.txt = key + " " + random.choice(botd.tbl.names.values())
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
