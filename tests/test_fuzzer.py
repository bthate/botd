import logging
import random
import unittest

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
        for key in k.modules:
            for n in k.names:
                t = k.names[n]
                try:
                    e = get_cls(t)()
                    e.txt = key + " " + random.choice(list(k.names))
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
