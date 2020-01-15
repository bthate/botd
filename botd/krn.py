# BOTD - python3 IRC channel daemon.
#
# kernel for boot proces.

__version__ = 3

import logging
import os
import time
import botd.tbl

from botd.err import EINIT
from botd.flt import Fleet
from botd.hdl import Handler
from botd.obj import Cfg, Object
from botd.shl import enable_history, set_completer, writepid
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

class Kernel(Handler):

        
    def __init__(self, cfg=None, **kwargs):
        super().__init__()
        self._stopped = False
        self._skip = False
        self.cfg = Cfg()
        self.cfg.modules = ""
        self.cfg.update(cfg or {})
        self.cfg.update(kwargs)
        self.cmds = Object()
        self.fleet = Fleet()
        self.run = Object()
        self.users = Users()
        kernels.add(self)
        self.register("command", dispatch)

    def add(self, cmd, func):
        self.cmds[cmd] = func

    def get_cmd(self, cn):
        mn = botd.tbl.modules.get(cn, None)
        if mn and mn not in self.table:
            self.load_mod(mn)
        return self.cmds.get(cn, None)
        
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

# functions

def dispatch(handler, event):
    if not event.txt:
        return
    event.parse()
    chk = event.txt.split()[0]
    event._func = handler.get_cmd(chk)
    if event._func:
        event._func(event)
        event.show()
    event.ready()

# runtime

kernels = Kernels()
