# BOTD - python3 IRC channel daemon.
#
# kernel for boot proces.

__version__ = 1

import inspect
import logging
import sys
import time

import bl

from bl.flt import Fleet
from bl.hdl import Event
from bl.ldr import Loader
from bl.obj import Cfg, Object, Register
from bl.shl import enable_history, set_completer, writepid
from bl.trc import get_exception
from bl.usr import Users
from bl.utl import get_name

class Cfg(Cfg):

    pass

class Kernel(Loader):

    cfg = Cfg()
    fleet = Fleet()
    users = Users()
        
    def __init__(self, cfg=None, **kwargs):
        super().__init__()
        self._stopped = False
        self._skip = False
        self.cfg.update(cfg or {})
        self.cfg.update(kwargs)
        kernels.add(self)
        
    def cmd(self, txt, origin=""):
        if not txt:
            return
        from bl.csl import Console
        c = Console()
        e = Event()
        e.txt = txt
        e.origin = origin
        e.orig = repr(c)
        self.dispatch(e)
        e.wait()

    def dispatch(self, event):
        if not event.txt:
            return
        event.parse()
        chk = event.txt.split()[0]
        try:
            event._func = self.get_cmd(chk)
        except Exception as ex:
            logging.error(get_exception())
            return
        if event._func:
            event._func(event)
            event.show()
        event.ready()

    def init(self, modstr):
        mods = self.walk(modstr)
        for mod in mods:
            logging.warning("found %s" % mod.__name__)
            try:
                mod.init(self)
            except (AttributeError, ModuleNotFoundError) as ex:
                if mod.__name__ in str(ex):
                    continue
                raise

    def register(self, k, v):
        self.cmds.set(k, v)

    def start(self):
        c = Cfg(self.cfg)
        l = self.cfg.last()
        self.cfg.update(l, True)
        self.cfg.update(c, True)
        try:
            self.init(self.cfg.modules)
        except bl.err.EINIT as ex:
            print(ex)
            self._skip = True
            return
        if self.cfg.dosave:
            self.cfg.save()
        if self.cfg.shell:
            self.init("bl.csl,botd.cmd")
        else:
            self._skip = True

    def wait(self):
        if self._skip:
            return
        while not self._stopped:
            time.sleep(1.0)

class Kernels(Register):

    nr = 0

    def add(self, kernel):
        self.register(str(Kernels.nr), kernel)
        Kernels.nr += 1

kernels = Kernels()
