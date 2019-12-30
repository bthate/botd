# BOTD - python3 IRC channel daemon.
#
# kernel tables. 

__version__ = 1

import inspect
import logging
import sys
import time

from bl import Cfg
from bl.csl import Console
from bl.err import EINIT, ENOTXT
from bl.evt import Event
from bl.ldr import Loader
from bl.log import level
from bl.shl import enable_history, parse_cli, set_completer, writepid
from bl.utl import get_name, hd

class Cfg(Cfg):

    def __init__(self):
        super().__init__()
        self.dosave = False
        self.doexec = False
        self.exclude = ""
        self.kernel = False
        self.level =  ""
        self.logdir = ""
        self.modules = ""
        self.name = ""
        self.options = ""
        self.owner = ""
        self.prompting = False
        self.verbose = False
        self.workdir = ""

class Event(Event):

    def show(self):
        if "verbose" in self and not self.verbose:
            return
        for txt in self.result:
            print(txt)

class Kernel(Loader):

    cfg = Cfg()
    
    def __init__(self):
        super().__init__()
        self._autoload = False
        self._started = False
        self._stopped = False
        
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
        if not ms:
            return []
        modules = []
        for mn in ms.split(","):
            if not mn:
                continue
            try:
                m = self.walk("botd.%s" % mn)
            except ModuleNotFoundError as ex:
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
        bots = []
        for mod in self.get_mods(modstr):
            if "init" not in dir(mod):
                continue
            logging.warning("init %s" % mod.__name__)
            bot = mod.init(self)
            bots.append(bot)
        return bots

    def start(self, cfg=None):
        if cfg and "kernel" in cfg and cfg.kernel:
            self.cfg.last()
        if cfg:
            self.cfg.update(cfg)
        if not self.cfg.name:
            self.cfg.name = "botd"
        try:
            self.init(self.cfg.modules)
        except EINIT as ex:
            self._stopped = True
            print(ex)
            return
        if self.cfg.dosave:
            self.cfg.save()
        if self.cfg.shell:
            set_completer(self.cmds)
            enable_history()
            writepid()

    def wait(self):
        if not self.cfg.shell and not self.cfg.daemon:
            return
        while not self._stopped:
            time.sleep(1.0)
