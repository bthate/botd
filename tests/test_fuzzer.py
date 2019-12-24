import bl
import logging
import random
import unittest

bl.k.cfg.prompt = False
bl.k.walk("bl")
bl.k.users.oper("test@shell")

class Test_Fuzzer(unittest.TestCase):

    def test_fuzzer1(self):
        for key in bl.k.modules:
            for n in bl.k.names:
                t = bl.k.names[n]
                try:
                    e = bl.typ.get_cls(t)()
                    e.txt = key + " " + random.choice(list(bl.k.names))
                    e.parse(e.txt)
                    e.orig = repr(b)
                    e.origin = "test@shell"
                    e.update(o)
                    v = bl.k.get_cmd(key)
                    if v:
                        v(e)
                except AttributeError:
                    pass
                except TypeError as ex:
                    break
        self.assertTrue(True)
