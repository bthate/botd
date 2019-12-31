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
from bl.usr import Users

class Kernel(Loader):

    cfg = Cfg()
    fleet = Fleet()
    users = Users()
        
    def __init__(self):
        super().__init__()
        self._stopped = False
        self._skip = False
        kernels.add(self)
        
    def cmd(self, txt, origin=""):
        e = Event()
        e.txt = txt
        e.origin = origin
        e.orig = repr(self)
        self.dispatch(e)
        e.wait()

    def dispatch(self, event):
        if not event.txt:
            return
        chk = event.txt.split()[0]
        event._func = self.get_cmd(chk)
        if event._func:
            event._func(event)
            event.show()
        event.ready()

    def init(self, modstr):
        for mod in self.get_mods(modstr):
            cmds = self.get_cmds(mod)
            for cmd in cmds:
                func = cmds.get(cmd)
                self.cmds.register(cmd, func)
            if "init" in dir(mod):
                logging.warning("init %s" % mod.__name__)
                mod.init(self)

    def register(self, k, v):
        self.cmds.set(k, v)

    def start(self, shell=True):
        try:
            self.init(self.cfg.modules)
        except bl.err.EINIT as ex:
            print(ex)
            self._skip = True
            return
        if shell:
            self.init("bl.csl,botd.cmd")

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
