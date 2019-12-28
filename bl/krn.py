# BOTD - python3 IRC channel daemon.
#
# kernel tables. 

workdir = ""

import inspect
import logging
import time
import bl.tbl

from bl.dbs import Db, last
from bl.err import EINIT, ENOTXT
from bl.evt import Event
from bl.hdl import Handler
from bl.ldr import Loader
from bl.log import level
from bl.obj import Object
from bl.pst import Cfg, Persist, Register
from bl.shl import enable_history, set_completer, writepid
from bl.typ import get_type
from bl.utl import get_mods, get_name

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
           "prompting": False,
           "shell": False,
           "verbose": False,
           "workdir": ""
          }

class Event(Event):

    def show(self):
        for txt in self.result:
            print(txt)

class Kernel(Loader, Persist):

    cfg = Cfg(default)
    cmds = Register()
    
    def __init__(self, cfg={}, **kwargs):
        super().__init__()
        self._started = False
        self._stopped = False
        self.cfg.update(cfg)
        self.cfg.update(kwargs)

    def cmd(self, txt, origin=""):
        if not txt:
            return
        self.cfg.prompting = False
        e = Event()
        e.txt = txt
        e.options = self.cfg.options
        e.orig = repr(self)
        e.origin = origin or "root@shell"
        self.dispatch(e)
        e.wait()

    def init(self, modstr):
        mods = []
        for mod in get_mods(self, modstr):
            if "init" not in dir(mod):
                continue
            logging.warning("init %s" % mod.__name__)
            mod.init(self.cfg)
            mods.append(mod)
        return mods

    def load_mod(self, mn, force=True):
        logging.warning("load %s into %s" % (mn, get_name(self)))
        mod = super().load_mod(mn, force=force)
        self.scan(mod)
        return mod

    def scan(self, mod):
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1 and key not in self.cmds:
                    self.cmds.register(key, o)
                    bl.tbl.modules[key] = o.__module__
        for key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object):
                t = get_type(o)
                if t not in bl.tbl.classes:
                    bl.tbl.classes.append(t)
                    bl.tbl.names[t.split(".")[-1].lower()] = str(t)

    def start(self):
        if self._started:
            return
        self._started = True
        if self.cfg.owner:
            self.users.oper(cfg.owner)
        if self.cfg.kernel:
            self.cfg.last()
            
    def wait(self):
        while not self._stopped:
            time.sleep(1.0)
