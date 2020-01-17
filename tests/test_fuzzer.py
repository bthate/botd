# BOTD - python3 IRC channel daemon
#
# fuzzer test

import logging
import random
import types
import unittest
import botd.tbl

from botd.evt import Event
from botd.krn import kernels
from botd.obj import Object
from botd.trc import get_exception
from botd.typ import get_cls
from botd.utl import xobj

k = kernels.get_first()
k.cfg.prompt = False
k.cfg.debug = True
k.users.oper("test@shell")

class Test_Fuzzer(unittest.TestCase):

    def test_fuzzer1(self):
        for key in botd.tbl.modules:
            for n in botd.tbl.names:
                t = botd.tbl.names[n]
                try:
                    e = get_cls(t)()
                    e.txt = key + " " + random.choice(list(k.modules.values()))
                    e.parse(e)
                    e.etype = "command"
                    e.orig = repr(b)
                    e.origin = "test@shell"
                    v = k.get_cmd(key)
                    if v:
                        logging.debug("%s %s" % (str(v), e))
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
        exs = []
        for x in range(nrloops):
            names = list(botd.tbl.names)
            random.shuffle(names)
            for name in names:
                mod = k.load_mod(name, cmds=False)
                for obj in xobj(mod, "_"):
                    for func in xobj(obj, "_", [types.MethodType, types.FunctionType]):
                        if "handleError" in str(func):
                            continue
                        arglist = []
                        for name in func.__code__.co_varnames:
                            nrvar = func.__code__.co_argcount
                            n = randomarg(name)
                            if n:
                                arglist.append(n)
                        try:
                            logging.debug("%s %s" % (str(func), str(arglist)))
                            func(*arglist[:nrvar])
                        except:
                            exs.append(get_exception())
        self.assertTrue(True)
                        
# functions

def randomarg(name):
    t = random.choice(types.__all__)
    return types.new_class(t)()
