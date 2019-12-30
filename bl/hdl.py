# BOTD - python3 IRC channel daemon.
#
# event handler.

import inspect
import logging
import pkgutil
import queue
import time
import threading
import bl.tbl

from bl import Object, Register
from bl.err import ENOTIMPLEMENTED
from bl.ldr import Loader
from bl.thr import launch
from bl.typ import get_name, get_type
from bl.utl import get_mods

def __dir__():
    return ("Handler",)

class Handler(Loader):
    
    def __init__(self):
        super().__init__()
        self._autoload = False
        self._queue = queue.Queue()
        self._started = False
        self._stopped = False
        self._threaded = True
        self._type = get_type(self)
        self.cmds = Register()

    def dispatch(self, event):
        event.parse(event.txt)
        event._func = self.get_cmd(event.chk)
        if event._func:
            event._func(event)
            event.show()
        event.ready()

    def handler(self):
        logging.warning("starting %s" % get_name(self))
        while not self._stopped:
            e = self._queue.get()
            if self._threaded:
                e._thrs.append(launch(self.dispatch, e))
            else:
                self.dispatch(e)

    def poll(self):
        raise ENOTIMPLEMENTED

    def put(self, event):
        self._queue.put_nowait(event)

    def start(self):
        self._started = True
        launch(self.handler)

    def stop(self):
        self._stopped = True
        self._queue.put(None)

    def sync(self, other):
        self.cmds.update(other.cmds)
