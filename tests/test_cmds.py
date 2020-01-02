# BOTD - python3 IRC channel daemon.
#
# test commands.

import random
import time
import types
import unittest

from bl.obj import Object, values
from bl.hdl import Event
from bl.krn import Kernel
from bl.thr import launch

k = Kernel()

def test():
    print("yooo!")

def randomarg():
    t = random.choice(types.__all__)
    return types.new_class(t)()

examples = Object()
examples.find = "find todo"
examples.last = "last cfg"
examples.tommorrow = "tomorrow take some time off."
examples.deleted = "deleted rss"
examples.log = "log wakker"
examples.rss = "http://nos.nl"
examples.todo = "todo code some code"
examples.user = "user root@shell"
examples.timer = "timer 23.35 blablabla"
examples.show = "show fleet"
examples.shop = "shop bacon"
examples.rm = "rm rss[0]"
examples.restore = "restore rss[0]"
examples.reload = "reload cmnds"
examples.perm = "perm root@shell oper"
examples.meet = "meet root@shell oper"
examples.mbox = "mbox ~/25-1-2013"
examples.loglevel = "loglevel info"
examples.first = "first cfg"
examples.dump = "dump todo"
examples.delperm = "delperm root@shell oper"
examples.cfg = "cfg irc"
examples.announce = "announce bla"
examples.alias = "alias l cmnds"

varnames = Object()
varnames.object = Object()
varnames.daystring = "2017-08-29 16:34:23.837288"
varnames.seconds = 60
varnames.daystr = "Sat Jan 14 00:02:29 2017"
varnames.txt = "i told you so !!"
varnames.path = "data/runtime/kernel"
varnames.optionlist = "-b -a -l info"
varnames.level = "info"
varnames.error = "info"
varnames.fd = 1
varnames.event = Event()
#varnames.old = termios.tcgetattr(1)
varnames.text = "blablabla mekker"
varnames.signature = "1e7f50d2015ac2ddc1f2ae8cf8ed6dfd896cab71"
varnames.u = "bart!~bart@localhost"
varnames.jid = "monitor@localhost/blamekker"
varnames.url = "http://localhost"
varnames.obj = Object()
varnames.func = test
varnames.timestamp = time.time()
varnames.origin = "root@shell"
varnames.perm = "OPER"
varnames.o = Object()
varnames.depth = 2
varnames.keys = ["test", "txt"]
varnames.uniqs = ["bla"]
varnames.ignore = {"test": "mekker"}
varnames.notwant = {"test": "mekker"}
varnames.want = {"test": "mekker"}

class Test_Cmnds(unittest.TestCase):

    def test_run(self):
        event = Event()
        event._verbose = k.cfg.verbose
        event.origin = "root@shell"
        event.txt = ""
        thrs = []
        nrloops = 10
        for x in range(nrloops):
            thr = launch(testcmnds, event)
            thr.join()

    def test_func(self):
        event = Event()
        event.origin = "root@shell"
        event._verbose = k.cfg.verbose
        event.txt = ""
        thrs = []
        nrloops = 10
        for x in range(nrloops):
            thr = launch(functest, event)
            thr.join()

    def test_cmnd(self):
        event = Event()
        event.origin = "root@shell"
        event.txt = ""
        event._verbose = k.cfg.verbose
        thrs = []
        nrloops = 10
        for x in range(nrloops):
            thr = launch(cmndrun, event)
            thr.join()
    
def cmndrun(event):
    mods = k.get_mods("botd")
    for mod in mods:
        if mod.__name__ in ["botd.rss",]:
            continue
        for n in dir(mod):
           if n in exclude:
               continue
           func = getattr(mod, n, None)
           if func and type(func) in [types.FunctionType, types.MethodType]:
               if "event" in func.__code__.co_varnames:
                   e = Event()
                   e._func = func
                   e._verbose = k.cfg.verbose
                   e.origin = "root@shell"
                   e.server = "localhost"
                   e.btype = "cli"
                   k.dispatch(e)

def functest(event):
    for name in k.get_mn("botd"):
        if name in ["botd.rss"]:
            continue
        mod = k.walk(name)
        keys = dir(mod)
        random.shuffle(keys)
        for n in keys:
           if n in exclude:
               continue
           obj = getattr(mod, n, None)
           for func in dir(obj):
               if  func and type(func) in [types.FunctionType, types.MethodType]:
                   arglist = []
                   for name in func.__code__.co_varnames:
                       nrvar = func.__code__.co_argcount
                       n = varnames.get(name, None)
                       if n:
                           arglist.append(n)
                   try:
                       func(*arglist[:nrvar])
                   except:
                       logging.error(get_exception())
               
def testcmnds(event):
    keys = list(k.cmds)
    random.shuffle(keys)
    for cmnd in keys:
        if cmnd in exclude:
            continue
        if cmnd == "find":
            name = "email"
        else:
            name = randomarg()
        e = Event()
        e.update(event)
        e._verbose = k.cfg.verbose
        e.orig = event.orig
        e.server = "localhost"
        cmnd = examples.get(cmnd, cmnd)
        e.txt = "%s %s" % (cmnd, name)
        e.origin = "root@shell"
        k.dispatch(e)

exclude = ["exit", "loglevel", "reboot", "real_reboot", "fetcher", "synchronize", "init", "shutdown", "wrongxml","mbox", "testcmnds", "runkernel", "functest", "cmndrun"]
outtxt = u"Đíť ìš éèñ ëņċøďıńğŧęŝţ· .. にほんごがはなせません .. ₀0⁰₁1¹₂2²₃3³₄4⁴₅5⁵₆6⁶₇7⁷₈8⁸₉9⁹ .. ▁▂▃▄▅▆▇▉▇▆▅▄▃▂▁ .. .. uǝʌoqǝʇsɹǝpuo pɐdı ǝɾ ʇpnoɥ ǝɾ"
