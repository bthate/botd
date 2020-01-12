# BOTLIB - Framework to program bots (a botlib).
#
# tinder tests.

import logging
import os
import random
import sys
import time
import unittest

from botd.bot import Bot
from botd.obj import Object
from botd.hdl import Event
from botd.krn import Kernel, kernels
from botd.tbl import names
from botd.utl import consume
from botd.thr import launch
from botd.usr import Users

class Param(Object):

    pass

k = kernels.get_first()
k.users.oper("test@shell")

try:
    index = int(k.cfg.args[1])
except:
    index = 1

bot = Bot()
bot.start()

names = list(names)
param = Param()
param.cfg = [random.choice(["irc", "rss"]),]
param.find = names
param.log = ["yo!",]
param.rm = ["%s txt==yo" % random.choice(names)]
param.meet = ["test@shell",]
#param.mbox = ["~/evidence/25-1-2013",]

class Test_Tinder(unittest.TestCase):

    def test_tinder(self):
        thrs = []
        for x in range(index):
            thrs.append(launch(tests, k))
        for thr in thrs:
            thr.join()

    def test_tinder2(self):
        for x in range(index):
            tests(k)
        
def tests(b):
    events = []
    keys = list(b.cmds)
    random.shuffle(keys)
    for cmd in keys:
        if cmd in ["fetch", "exit", "reboot", "reconnect", "test"]:
            continue
        events.extend(do_cmd(k, cmd))
    consume(events)

def do_cmd(b, cmd):
    exs = param.get(cmd, [])
    if not exs:
        exs = ["bla",]
    e = list(exs)
    random.shuffle(e)
    events = []
    for ex in e:
        e = Event()
        e.orig = repr(bot)
        e.origin = "test@shell"
        e.txt = cmd + " " + ex
        e.verbose = k.cfg.verbose
        k.dispatch(e)
        events.append(e)
    return events
