# BOTD - python3 IRC channel daemon.
#
# kernel for boot proces.

__version__ = 1

import bl
import inspect
import logging
import sys
import time

from bl.shl import enable_history, set_completer, writepid

class Cfg(bl.Cfg):

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

class Event(bl.evt.Event):

    def show(self):
        if "verbose" in self and not self.verbose:
            return
        for txt in self.result:
            print(txt)

class Kernel(bl.ldr.Loader):

    cfg = bl.Cfg()
    
    def __init__(self):
        super().__init__()
        self._stopped = False
        bl.kernels.add(self)
        
    def cmd(self, txt, origin=""):
        e = bl.evt.Event(txt=txt, origin=origin)
        e.orig = repr(self)
        self.dispatch(e)
        e.wait()

    def dispatch(self, event):
        try:
            event.parse(event.txt)
        except bl.err.ENOTXT:
            event.ready()
            return
        event._func = super().get_cmd(event.chk)
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
                mod.init(self)

    def register(self, k, v):
        self.cmds.set(k, v)

    def start(self, cfg=None):
        #l = self.cfg.last()
        #tmp = bl.Cfg(self.cfg)
        #self.cfg.update(l)
        #self.cfg.update(tmp)
        #self.cfg.save()
        self.init("bl.csl")
        self.init("botd.cmd")
        self.init(self.cfg.modules)

    def wait(self):
        while not self._stopped:
            time.sleep(1.0)
