# BOTLIB - Framework to program bots.
#
#

""" kernel code. """

import bot
import inspect
import lo
import logging
import sys
import threading
import time
import _thread

from lo import Db, Cfg
from lo.csl import Console
from lo.hdl import Handler, Event, dispatch

from bot.flt import Fleet
from bot.usr import Users

def __dir__():
    return ("Cfg", "Kernel")

class Cfg(lo.Cfg):

    pass

class Kernel(lo.hdl.Handler, lo.thr.Launcher):

    def __init__(self):
        super().__init__()
        self._outputed = False
        self._prompted = threading.Event()
        self._prompted.set()
        self._started = False
        self.cfg = Cfg()
        self.db = Db()
        self.fleet = Fleet()
        self.users = Users()
        bot.kernels.append(self)

    def add(self, cmd, func):
        self.cmds[cmd] = func

    def cmd(self, txt):
        self.fleet.add(self)
        e = Event()
        e.txt = txt
        e.orig = repr(self)
        e.parse()
        dispatch(self, e)
        e.wait()
        return e
        
    def start(self, shell=False):
        if self.error:
            print(self.error)
            return False
        lo.shl.writepid()
        super().start()
        if shell:
            c = Console()
            c.cmds.update(self.cmds)
            c.start()
            self.fleet.add(c)
        return True

    def wait(self):
        logging.warning("waiting on %s" % lo.typ.get_name(self))
        while not self._stopped:
            time.sleep(1.0)
        logging.warning("shutdown")
