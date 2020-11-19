"run all commands"

import os, sys ; sys.path.insert(0, os.getcwd())

import os
import random
import sys
import time
import unittest

from bot.hdl import Event, Handler
from bot.obj import Object, get
from bot.prs import parse_cli
from bot.thr import launch

cfg = parse_cli()
verbose = "v" in cfg.opts
index = cfg.index

param = Object()
param.add = ["test@shell", "bart"]
param.dne = ["test4", ""]
param.edt = ["bot.rss.Cfg", "bot.rss.Cfg server=localhost", "bot.rss.Cfg channel=#dunkbots"]
param.rm = ["reddit", ]
param.dpl = ["reddit title,summary,link",]
param.log = ["test1", ""]
param.flt = ["0", "1", ""]
param.fnd = ["cfg server==localhost", "kernel wd", "rss rss==reddit rss", "email From==pvp From Subject -t"]
param.rss = ["https://www.reddit.com/r/python/.rss"]
param.tdo = ["test4", ""]
param.mbx = ["~/Desktop/25-1-2013", ""]

events = []
ignore = ["mbx", "rss"]
nrtimes = 1

k = Handler()
k.walk("bot")
k.start()

class Event(Event):

    def direct(self, txt):
        if verbose:
            print(txt)

class Test_Tinder(unittest.TestCase):

    def test_thrs(self):
        thrs = []
        for x in range(index or 1):
            launch(tests, k)
        consume(events)

    def test_neuman(self):
        for x in range(index or 1):
            tests(k)

    def test_sorted(self):
        for x in range(index or 1):
            sortedtests(k)
        
def consume(elems):
    fixed = []
    res = []
    for e in elems:
        r = e.wait()
        res.append(r)
        fixed.append(e)
    for f in fixed:
        try:
            elems.remove(f)
        except ValueError:
            continue
    k.stop()
    return res
    
def sortedtests(b):
    keys = sorted(k.cbs)
    for cmd in keys:
        if cmd in ignore:
            continue
        events.extend(do_cmd(cmd))

def tests(b):
    keys = list(k.cbs)
    random.shuffle(keys)
    for cmd in keys:
        if cmd in ignore:
            continue
        events.extend(do_cmd(cmd))

def do_cmd(cmd):
    exs = get(param, cmd, [""])
    e = list(exs)
    random.shuffle(e)
    events = []
    nr = 0
    for ex in e:
        nr += 1
        txt = cmd + " " + ex 
        e = Event()
        e.txt = txt
        k.put(e)
        events.append(e)
    return events

for e in do_cmd("mbx"):
    e.wait()

for e in do_cmd("rss https://www.reddit.com/r/python/.rss"):
    e.wait()
