# BOTD - python3 IRC channel daemon.
#
# kernel for boot proces.

__version__ = 1

import logging
import os
import time

from botd.err import EINIT
from botd.flt import Fleet
from botd.hdl import Event
from botd.ldr import Loader
from botd.obj import Cfg, Object
from botd.shl import enable_history, set_completer, writepid
from botd.thr import launch
from botd.trc import get_exception
from botd.usr import Users
from botd.utl import get_name

# defines

def __dir__():
    return ("Cfg", "Kernel", "Kernels", "kernels")

starttime = time.time()

# classes

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
        self.cfg.modules = ""
        self.cfg.update(cfg or {})
        self.cfg.update(kwargs)
        self.run = Object()
        kernels.add(self)
        
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

    def register(self, k, v):
        self.cmds.set(k, v)

    def say(self, channel, txt, mtype="normal"):
        print(txt)

    def wait(self):
        while not self._stopped:
            time.sleep(1.0)

class Kernels(Object):

    kernels = []
    nr = 0

    def add(self, kernel):
        logging.warning("add %s" % get_name(kernel))
        if kernel not in Kernels.kernels:
            Kernels.kernels.append(kernel)
            Kernels.nr += 1

    def get_first(self):
        try:
            return Kernels.kernels[0]
        except IndexError:
            pass
# runtime

kernels = Kernels()
