# BOTD - python3 IRC channel daemon.
#
# kernel tables. 

workdir = ""

import inspect
import logging
import time
import bl.tbl

from bl.csl import Console
from bl.dbs import Db, last
from bl.err import EINIT, ENOTXT
from bl.evt import Event
from bl.hdl import Handler
from bl.ldr import Loader
from bl.log import level
from bl.obj import Object
from bl.pst import Cfg, Persist, Register
from bl.shl import enable_history, parse_cli, set_completer, writepid
from bl.typ import get_type
from bl.utl import get_mods, get_name, hd

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
            m = self.walk(mn)
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

    def start(self, name="", version=1, opts={}, shell=True):
        cfg = parse_cli(self.cfg.name, self.cfg.version, self.opts, wd=hd(".%s" % self.cfg.name))
        self.cfg.update(cfg)
        level(cfg.level)
        if shell or cfg.shell:
             c = Console(self)
             c.start()
             
    def wait(self):
        while not self._stopped:
            time.sleep(1.0)

