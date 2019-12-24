# BOTLIB - Framework to program bots.
#
# 

__version__ = 72

workdir = ""

import logging
import time

import bl.obj

from bl.obj import Object, get, keys, set, update

import bl.pst

from bl.utl import locked
from bl.pst import Persist

def __dir__():
    return ("Cfg", "Event", "Kernel", "Persist", "Object", "cfg", "db", "fleet", "get", "k", "last", "locked", "set", "update", "workdir")

default = {
           "dosave": False,
           "doexec": False,
           "exclude": "",
           "kernel": False,
           "level": "",
           "logdir": "",
           "modules": "",
           "options": "",
           "owner": "",
           "prompting": True,
           "shell": False,
           "verbose": False,
           "workdir": ""
          }

class Cfg(Persist):

    def __init__(self, cfg=None):
        super().__init__()
        if cfg:
            bl.update(self, cfg)


class Default(Persist):

    def __init__(self, cfg=None):
        super().__init__()
        if cfg:
            bl.update(self, cfg)

    def __getattr__(self, k):
        if not k in self:
            bl.set(self, k, "")
        return bl.get(self, k)

import bl.hdl

class Kernel(bl.hdl.Handler, Persist):

    def __init__(self):
        super().__init__()
        self._outputed = False
        self._started = False
        self.prompt = True
        self.verbose = True

    def add(self, bot):
        fleet.add(bot)

    def cmd(self, txt, origin=""):
        if not txt:
            return
        cfg.prompting = False
        c = bl.csl.Console()
        c.start(False, False, False)
        e = Event()
        e.txt = txt
        e.options = cfg.options
        e.orig = repr(c)
        e.origin = origin or "root@shell"
        self.register(dispatch)
        self.prompt = False
        self.add(c)
        self.handle(e)
        e.wait()

    def init(self, modstr):
        if not modstr:
            return
        ok = True
        for mod in bl.utl.get_mods(self, modstr):
            if "init" not in dir(mod):
                continue
            n = bl.utl.get_name(mod)
            if cfg.exclude and n in cfg.exclude.split(","):
                continue
            try:
                mod.init()
            except bl.err.EINIT as ex:
                if not cfg.doexec and not cfg.shell and not cfg.kernel:
                    print(str(ex))
                    ok = False
                    break
        return ok

    def start(self):
        if self._started:
            return
        self._started = True
        state.started = False
        state.starttime = time.time()
        if cfg.owner:
            self.users.oper(cfg.owner)
        if cfg.kernel:
            bl.last(cfg)
        super().start(True, False, False)
        self.register(bl.dispatch)
        self.init(cfg.modules)

    def wait(self):
        if cfg.doexec:
            return
        if not cfg.kernel and cfg.dosave:
            cfg.save()
        if cfg.kernel or cfg.shell or (cfg.prompting and cfg.args):
            bl.shl.writepid()
            bl.shl.set_completer(self.cmds)
            bl.shl.enable_history()
            c = bl.csl.Console()
            c.start()
            while not self._stopped:
                time.sleep(1.0)

class Register(bl.pst.Persist):

    def get(self, k):
        return bl.get(self, k)

    def register(self, k, v):
        bl.set(self, k, v)

import bl.dbs
import bl.flt
import bl.usr

k = Kernel()
cfg = Cfg(default)
db = bl.dbs.Db()
fleet = bl.flt.Fleet()
state = bl.Object()
users = bl.usr.Users()

def dispatch(handler, event):
    try:
        event.parse()
    except bl.err.ENOTXT:
        event.ready()
        return
    event._func = handler.get_cmd(event.chk)
    if event._func:
        event._calledfrom = str(event._func)
        event._func(event)
        event.show()
    event.ready()

def launch(func, *args):
    return k.launch(func, *args)

def last(o, skip=True):
    val = db.last(str(str(bl.typ.get_type(o))))
    if val:
        bl.update(o, val)
        o.__path__ = val.__path__
        return o.__path__

from bl.bot import Bot
import bl.evt
from bl.evt import Event
import bl.all
