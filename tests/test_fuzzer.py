# BOTD - python3 IRC channel daemon
#
# fuzzer test

import logging
import random
import unittest
import botd.tbl

from botd.evt import Event
from botd.krn import kernels
from botd.typ import get_cls

k = kernels.get_first()
k.cfg.prompt = False
k.cfg.debug = True
k.users.oper("test@shell")

class Test_Fuzzer(unittest.TestCase):

    def test_fuzzer1(self):
        for key in botd.tbl.modules:
            for n in botd.tbl.names:
                print(key, n)
                t = botd.tbl.names[n]
                try:
                    e = get_cls(t)()
                    e.txt = key + " " + random.choice(list(k.names))
                    e.parse(e.txt)
                    e.etype = "command"
                    e.orig = repr(b)
                    e.origin = "test@shell"
                    print(e)
                    v = k.get_cmd(key)
                    if v:
                        v(e)
                except AttributeError:
                    pass
                except TypeError as ex:
                    break
        self.assertTrue(True)

    def test_fuzzer2(self):
        event = Event()
        event.etype = "command"
        event.origin = "root@shell"
        event.txt = ""
        thrs = []
        nrloops = 1
        for x in range(nrloops):
            names = list(k.table.values())
            random.shuffle(names)
            for name in names:
                mod = k.load_mod(name, cmds=False)
                keys = dir(mod)
                random.shuffle(keys)
                for key in keys:
                    obj = getattr(mod, key, None)
                    if not obj:
                        for func in dir(obj):
                            print(func, type(func))
                            if func and type(func) in [types.FunctionType, types.MethodType]:
                                arglist = []
                                for name in func.__code__.co_varnames:
                                    nrvar = func.__code__.co_argcount
                                    n = randomarg(name)
                                    if n:
                                        arglist.append(n)
                                try:
                                    func(*arglist[:nrvar])
                                except:
                                    logging.error(get_exception())

# functions

def randomarg(name):
    t = random.choice(types.__all__)
    return types.new_class(t)()
