# BOTD - python3 IRC channel daemon.
#
# event handler.

import bl
import inspect
import logging
import pkgutil
import queue
import time
import threading

from bl.flt import Fleet
from bl.ldr import Loader
from bl.obj import Object, Register
from bl.thr import launch

def __dir__():
    return ("Handler",)

class Event(Object):

    def __init__(self):
        super().__init__()
        self._ready = threading.Event()
        self._verbose = True
        self.args = []
        self.channel = ""
        self.orig = ""
        self.origin = ""
        self.result = []
        self.txt = ""

    def display(self, o):
        txt = ""
        if "k" in self.options:
            self.reply("|".join(o))
        elif "d" in self.options:
            self.reply(str(o))
        elif "f" in self.options:
            full = True
        elif not full and self.dkeys:
            txt += " " + bl.gnr.format(o, self.dkeys, full)
        else:
            txt += " " + bl.gnr.format(o, full=full)
        if "t" in self.options and o._path:
            txt += " %s" % bl.tms.days(o._path)
        txt = txt.strip()
        self.reply(txt)

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self.result.append(txt)

    def show(self):
        if not self._verbose:
            return
        from bl.krn import kernels
        k = kernels.get("0", None)
        for txt in self.result:
            k.fleet.echo(self.orig, self.channel, txt)
 
    def wait(self):
        self._ready.wait()

class Handler(Loader):
    
    def __init__(self):
        super().__init__()
        self._queue = queue.Queue()
        self._stopped = False
        self.cmds = Register()

    def dispatch(self, event):
        if not event.txt:
            return
        chk = event.txt.split()[0]
        event._func = self.get_cmd(chk)
        if event._func:
            event._func(event)
            event.show()
        event.ready()

    def handle(self, event):
        self.dispatch(event)

    def handler(self):
        while not self._stopped:
            e = self._queue.get()
            self.handle(e)

    def poll(self):
        raise ENOTIMPLEMENTED

    def put(self, event):
        self._queue.put_nowait(event)

    def start(self):
        launch(self.handler)

    def stop(self):
        self._stopped = True
        self._queue.put(None)
