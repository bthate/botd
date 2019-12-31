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

class Kernel(bl.ldr.Loader):

    cfg = bl.Cfg()
    
    def __init__(self):
        super().__init__()
        self._stopped = False
        self._skip = False
        bl.kernels.add(self)
        
    def cmd(self, txt, origin=""):
        e = bl.evt.Event(txt=txt, origin=origin)
        e.orig = repr(self)
        self.dispatch(e)
        e.wait()

    def dispatch(self, event):
        event._func = self.get_cmd(event.chk)
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
