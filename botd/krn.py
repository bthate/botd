# BOTD - python3 IRC channel daemon.
#
# kernel for boot proces.

__version__ = 3

import inspect
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

    def find_cmds(self, mod):
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1:
                    if key not in self.cmds:
                        self.add(key, o)

    def get_cmd(self, cn):
        return self.cmds.get(cn, None)
 
    def say(self, channel, txt, mtype="normal"):
        print(txt)

    def wait(self):
        while not self._stopped:
            time.sleep(1.0)
        logging.warn("exit")

    def walk(self, mns, init=False, cmds=True):
        if not mns:
            return
        mods = []
        for mn in mns.split(","):
            if not mn:
                continue
            m = self.load_mod(mn)
            if not m:
                continue
            loc = None
            if "__spec__" in dir(m):
                loc = m.__spec__.submodule_search_locations
            if not loc:
                if cmds:
                    self.find_cmds(m)
                mods.append(m)
                continue
            for md in loc:
                for x in os.listdir(md):
                    if x.endswith(".py"):
                        mmn = "%s.%s" % (mn, x[:-3])
                        m = self.load_mod(mmn)
                        if cmds:
                            self.find_cmds(m)
                        if m:
                            mods.append(m)
        if init:
            for mod in mods:
                if "init" in dir(mod):
                    mod.init(self)
        return mods


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
