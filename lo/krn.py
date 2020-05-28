# BOTLIB - Framework to program bots.
#
#

""" kernel code. """

import inspect
import lo
import logging
import sys
import threading
import time
import _thread

from lo import Db, Cfg
from lo.csl import Console
from lo.flt import Fleet
from lo.hdl import Handler, Event, dispatch
from lo.shl import writepid
from lo.thr import launch
from lo.typ import get_name
from lo.usr import Users

def __dir__():
    return ("Cfg", "Kernel")

class Cfg(lo.Cfg):

    pass

class Kernel(lo.hdl.Handler):

    def __init__(self):
        super().__init__()
        self._outputed = False
        self._prompted = threading.Event()
        self._prompted.set()
        self._ready = threading.Event()
        self._started = False
        self.cfg = Cfg(lo.cfg)
        self.db = Db()
        self.fleet = Fleet()
        self.force = False
        self.users = Users()
        lo.kernels.append(self)

    def add(self, cmd, func):
        self.cmds[cmd] = func

    def cmd(self, txt):
        self.fleet.add(self)
        e = Event()
        e.txt = txt
        e.orig = repr(self)
        e.origin = "root@shell"
        e.parse()
        launch(dispatch, self, e)
        e.wait()
        return e
        
    def start(self, shell=False, init=True):
        if self.error:
            print(self.error)
            return False
        writepid()
        if lo.cfg.root:
            self.cfg.last()
            self.cfg.txt = ""
            self.cfg.merge(lo.cfg)
            self.cfg.save()
        else:
            self.cfg.merge(lo.cfg)
        if self.cfg.owner:
            if not self.users.allowed(self.cfg.owner, "USER", log=False):
                self.users.meet(self.cfg.owner)
        if not self.cfg.modules:
            self.cfg.modules = "lo.shw"
        self.walk(self.cfg.modules, init)
        if shell:
            c = Console()
            c.cmds.update(self.cmds)
            c.start()
            self.fleet.add(c)
        super().start()
        return True

    def ready(self):
        self._ready.set()

    def stop(self):
        self._stopped = True
        self._queue.put(None)

    def wait(self):
        logging.warning("waiting on %s" % get_name(self))
        self._ready.wait()
        logging.warning("shutdown")
