# BOTD - IRC channel daemon
#
# tinder tests.

import logging
import os
import random
import sys
import time
import unittest

from botd.bot import Bot
from botd.evt import Event
from botd.krn import Kernel, kernels
from botd.obj import Object
from botd.utl import consume
from botd.thr import launch
from botd.usr import Users
from botd.mod import get_names

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

# OPML <outline text="The Verge" title="The Verge" type="rss" xmlUrl="https://www.youtube.com/feeds/videos.xml?channel_id=UCddiUEpeqJcYeBxX1IVBKvQ" />

param = Param()
param.cfg = ["irc", "rss", "krn"]
param.log = ["yo!",]
param.meet = ["test@shell",]
param.find = ["%s yo" % x for x in get_names()]
param.rss = ["https://www.reddit.com/r/python/.rss", ""]
#param.mbox = ["~/evidence/25-1-2013",]

class Event(Event):

    def show(self):
        if self.verbose:
            super().show()

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
        e.etype = "command"
        e.orig = repr(bot)
        e.origin = "test@shell"
        e.txt = cmd + " " + ex
        e.verbose = k.cfg.verbose
        k.put(e)
        events.append(e)
    return events
