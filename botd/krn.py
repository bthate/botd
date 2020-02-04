# BOTD - IRC channel daemon.
#
# kernel for boot proces.

__version__ = 7

import inspect
import logging
import os
import time

from botd.err import EINIT
from botd.flt import Fleet
from botd.gnr import format
from botd.hdl import Handler
from botd.obj import Cfg, Default, Object
from botd.shl import enable_history, set_completer, writepid
from botd.trc import get_exception
from botd.tms import days
from botd.usr import Users
from botd.utl import get_name

def __dir__():
    return ("Cfg", "Kernel", "Kernels", "kernels")

starttime = time.time()

class Cfg(Cfg):

    pass

class Kernel(Handler):

    def __init__(self, cfg=None, **kwargs):
        super().__init__()
        self._stopped = False
        self.cfg = Cfg()
        self.cfg.update(cfg or {})
        self.cfg.update(kwargs)
        self.cmds = Object()
        self.fleet = Fleet()
        self.run = Default()
        self.users = Users()
        kernels.add(self)

    def add(self, cmd, func):
        self.cmds[cmd] = func

    def cmd(self, txt):
        from botd.evt import Event
        self.fleet.add(self)
        e = Event()
        e.txt = txt
        dispatch(self, e)
        e.wait()

    def display(self, o, txt=""):
        txt = txt[:]
        txt += " " + "%s %s" % (format(o), days(o._path))
        txt = txt.strip()
        self.say("", txt)
        
    def find_cmds(self, mod):
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1:
                    if key not in self.cmds:
                        self.add(key, o)

    def get_cmd(self, cn):
        return self.cmds.get(cn, None)
 
    def load_mod(self, mn, force=False, cmds=True):
        mod = super().load_mod(mn, force)
        if cmds:
             self.find_cmds(mod)
        return mod
       
    def say(self, channel, txt, mtype="normal"):
        print(txt)

    def start(self):
        self.register("command", dispatch)
        set_completer(self.cmds)
        super().start()

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
            m = self.load_mod(mn, False, cmds)
            if not m:
                continue
            loc = None
            if "__spec__" in dir(m):
                loc = m.__spec__.submodule_search_locations
            if not loc:
                mods.append(m)
                continue
            for md in loc:
                for x in os.listdir(md):
                    if x.endswith(".py"):
                        mmn = "%s.%s" % (mn, x[:-3])
                        m = self.load_mod(mmn, False, cmds)
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
        if kernel not in Kernels.kernels:
            Kernels.kernels.append(kernel)
            Kernels.nr += 1

    def get_first(self):
        try:
            return Kernels.kernels[0]
        except IndexError:
            k = Kernel()
            self.add(k)
            return k

def dispatch(handler, event):
    if not event.txt:
        event.ready()
        return
    event.parse()
    if "_func" not in event:
        chk = event.txt.split()[0]
        event._func = handler.cmds.get(chk, None)
    if event._func:
        event._func(event)
        event.show()
    event.ready()

kernels = Kernels()
