# BOTLIB - Framework to program bots.
#
# 

import bl
import logging
import os
import random
import sys
import time
import unittest

class Param(bl.Object):

    pass

bl.k.users.oper("test@shell")
e = bl.evt.Event()
e.parse("-o %s" % bl.k.cfg.options)

param = Param()
param.ed = ["%s txt==yo channel=#mekker" % x for x in bl.k.names]
param.ed.extend(["%s txt==yo test=a,b,c,d" % x for x in bl.k.names])
param.find = ["%s txt==yo -f" % x for x in bl.k.names] + ["email txt==gif", ]
param.load = bl.k.table.keys()
param.log = ["yo!",]
param.rm = ["%s txt==yo" % x for x in bl.k.names]
param.show = ["config", "cmds", "fleet", "kernel", "tasks", "version"]
#param.mbox = ["~/evidence/25-1-2013",]

class Test_Tinder(unittest.TestCase):

    def test_tinder(self):
        thrs = []
        for x in range(e.index or 1):
            thrs.append(bl.k.launch(tests, bl.k))
        for thr in thrs:
            thr.join()

    def test_tinder2(self):
        for x in range(e.index or 1):
            tests(bl.k)
        
def tests(b):
    events = []
    keys = list(b.cmds)
    random.shuffle(keys)
    for cmd in keys:
        if cmd in ["fetch", "exit", "reboot", "reconnect", "test"]:
            continue
        events.extend(do_cmd(b, cmd))
    bl.utl.consume(events)

def do_cmd(b, cmd):
    exs = bl.get(param, cmd, ["test1", "test2"])
    e = list(exs)
    random.shuffle(e)
    events = []
    for ex in e:
        e = bl.evt.Event()
        e.origin = "test@shell"
        e.txt = cmd + " " + ex
        b.put(e)
        events.append(e)
    return events
