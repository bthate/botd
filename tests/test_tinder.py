# BOTD - python3 IRC channel daemon.
#
# tinder tests.

import logging
import os
import random
import sys
import time
import unittest

from bl.obj import Object
from bl.hdl import Event
from bl.krn import Kernel
from bl.gnr import values
from bl.utl import consume
from bl.thr import launch
from bl.usr import Users

k = Kernel()
k.walk("botd.cmd")
k.start()
users = Users()

class Param(Object):

    pass

users.oper("test@shell")
e = Event()
e.verbose = k.cfg.verbose
#e.parse("-o %s" % k.cfg.options)
try:
    e.index = int(k.cfg.args[0])
except:
    e.index = 1

param = Param()
param.cfg = ["%s txt==yo channel=#mekker" % x for x in k.names]
param.cfg.extend(["%s txt==yo test=a,b,c,d" % x for x in k.names])
param.ed = ["%s txt==yo channel=#mekker" % x for x in k.names]
param.ed.extend(["%s txt==yo test=a,b,c,d" % x for x in k.names])
param.find = ["%s txt==yo -f" % x for x in k.names] + ["email txt==gif", ]
param.load = values(k.names)
param.log = ["yo!",]
param.rm = ["%s txt==yo" % x for x in k.names]
param.show = ["config", "cmds", "fleet", "kernel", "tasks", "version"]
#param.mbox = ["~/evidence/25-1-2013",]

class Test_Tinder(unittest.TestCase):

    def test_tinder(self):
        thrs = []
        for x in range(e.index or 1):
            thrs.append(launch(tests, k))
        for thr in thrs:
            thr.join()

    def test_tinder2(self):
        for x in range(e.index or 1):
            tests(k)
        
def tests(b):
    events = []
    keys = list(b.cmds)
    random.shuffle(keys)
    for cmd in keys:
        if cmd in ["fetch", "exit", "reboot", "reconnect", "test"]:
            continue
        events.extend(do_cmd(b, cmd))
    consume(events)

def do_cmd(b, cmd):
    exs = param.get(cmd, ["test1", "test2"])
    e = list(exs)
    random.shuffle(e)
    events = []
    for ex in e:
        e = Event()
        e.origin = "test@shell"
        e.txt = cmd + " " + ex
        e.verbose = k.cfg.verbose
        k.dispatch(e)
        events.append(e)
    return events
