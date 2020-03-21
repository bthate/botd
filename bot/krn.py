# BOTLIB - Framework to program bots.
#
#

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
from lo.hdl import Handler, Event, dispatch_autoload

from bot.flt import Fleet
from bot.usr import Users

def __dir__():
    return ("Cfg", "Kernel")

class Cfg(lo.Default):

    pass

class Kernel(lo.hdl.Handler, lo.thr.Launcher):

    def __init__(self, cfg={}):
        super().__init__()
        self._outputed = False
        self._prompted = threading.Event()
        self._prompted.set()
        self._started = False
        self.cfg = Cfg()
        self.db = Db()
        self.fleet = Fleet()
        self.users = Users()

    def add(self, cmd, func):
        self.cmds[cmd] = func

    def cmd(self, txt):
        e = Event()
        e.txt = txt
        e.orig = repr(self)
        e.parse()
        dispatch_autoload(self, e)
        e.wait()

    def start(self, shell=False):
        self.cfg.last()
        cfg = lo.strip(lo.cfg)
        self.cfg.update(cfg)
        self.walk(lo.cfg.modules, True)
        if self.error:
            print(self.error)
            return False
        lo.shl.set_completer(sorted(self.cmds))
        lo.shl.enable_history()
        lo.shl.writepid()
        super().start()
        if shell:
            c = Console()
            c.start()
            self.fleet.add(c)
        return True

    def wait(self):
        logging.warning("waiting on %s" % lo.typ.get_name(self))
        while not self._stopped:
            time.sleep(1.0)
        logging.warning("shutdown")

