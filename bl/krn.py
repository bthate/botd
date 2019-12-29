# BOTD - python3 IRC channel daemon.
#
# kernel tables. 

import inspect
import logging
import sys
import time

from bl.csl import Console
from bl.err import EINIT, ENOTXT
from bl.evt import Event
from bl.ldr import Loader
from bl.log import level
from bl.pst import Cfg, Persist
from bl.shl import enable_history, parse_cli, set_completer, writepid
from bl.utl import hd

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
    
    def __init__(self, name="botd", version=1, opts={}, **kwargs):
        super().__init__()
        self._autoload = False
        self._started = False
        self._stopped = False
        self.cfg.name = name
        self.cfg.version = version
        self.opts = opts

    def cmd(self, txt, origin=""):
        if not txt:
            return
        e = Event()
        e.txt = txt
        e.orig = repr(self)
        e.origin = origin or "root@shell"
        self.dispatch(e)
        e.wait()

    def dispatch(self, event):
        try:
            event.parse(event.txt)
        except ENOTXT:
            event.ready()
            return
        event._func = self.get_cmd(event.chk)
        if event._func:
            event._func(event)
            event.show()
        event.ready()

    def get_mods(self, ms):
        modules = []
        for mn in ms.split(","):
            if not mn:
                continue
            try:
                m = self.walk("botd.%s" % mn)
            except ModuleNotFoundError:
                try:
                    m = self.walk(mn)
                except ModuleNotFoundError as ex:
                    if mn in str(ex):
                        continue
                    raise
            if m:
                modules.extend(m)
        return modules
        
    def init(self, modstr):
        mods = []
        for mod in self.get_mods(modstr):
            if "init" not in dir(mod):
                continue
            logging.warning("init %s" % mod.__name__)
            mod.init(self.cfg)
            mods.append(mod)
        return mods

    def start(self, shell=True):
        cfg = parse_cli(self.cfg.name, self.cfg.version, self.opts, wd=hd(".%s" % self.cfg.name))
        self.cfg.update(cfg)
        level(cfg.level)
        try:
            self.init(cfg.modules)
        except EINIT as ex:
            self._stopped = True
            print(ex)
            return
        if shell:
            c = Console(self)
            c.start()
            set_completer(k.cmds)
            enable_history()
            writepid()

    def wait(self):
        while not self._stopped:
            time.sleep(1.0)

