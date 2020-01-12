# BOTLIB - Framework to program bots (a botlib).
#
# test commands as functions.

import os
import logging
import termios
import string
import random
import time
import types
import unittest
import botd.tbl

from botd.krn import Kernel
from botd.hdl import Event
from botd.thr import launch

k = Kernel()

class Test_Func(unittest.TestCase):

    def test_func(self):
        event = Event()
        event.origin = "root@shell"
        event.txt = ""
        thrs = []
        nrloops = 1
        for x in range(nrloops):
            thr = launch(functest, x)
            thr.join()

def randomarg(name):
    t = random.choice(types.__all__)
    return types.new_class(t)()
    
def functest(nr):
    names = list(botd.tbl.modules.values())
    for x in range(nr):
        random.shuffle(names)
        for name in names:
            mod = k.walk(name)
            keys = dir(mod)
            random.shuffle(keys)
            for key in keys:
                obj = getattr(mod, key)
                if not obj:
                    for func in dir(obj):
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
