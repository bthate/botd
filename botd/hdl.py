# BOTD - python3 IRC channel daemon.
#
# event handler.

import inspect
import logging
import pkgutil
import queue
import time
import threading

from botd.flt import Fleet
from botd.ldr import Loader
from botd.obj import Object
from botd.thr import launch
from botd.tms import days

# defines

def __dir__():
    return ("Event", "Handler")

# classes

class Event(Object):

    def __init__(self):
        super().__init__()
        self._ready = threading.Event()
        self.verbose = True
        self.args = []
        self.channel = ""
        self.options = ""
        self.orig = ""
        self.origin = ""
        self.result = []
        self.txt = ""

    def display(self, o, txt=""):
        txt = txt[:]
        txt += " " + "%s %s" % (self.format(o), days(o._path))
        txt = txt.strip()
        self.reply(txt)

    def format(self, o, keys=None):
        if keys is None:
            keys = vars(o).keys()
        res = []
        txt = ""
        for key in keys:
            if key == "stamp":
                continue
            val = o.get(key, None)
            if not val:
                continue
            val = str(val)
            if key == "text":
                val = val.replace("\\n", "\n")
            res.append(val)
        for val in res:
            txt += "%s%s" % (val.strip(), " ")
        return txt.strip()

    def parse(self, txt=""):
        txt = txt or self.txt
        if not txt:
            return
        spl = self.txt.split()
        if not spl:
            return
        self.cmd = spl[0]
        self.args = spl[1:]
        self.rest = " ".join(self.args)

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self.result.append(txt)

    def show(self):
        if not self.verbose:
            return
        from botd.krn import kernels
        k = kernels.get_first()
        for txt in self.result:
            k.fleet.echo(self.orig, self.channel, txt)

    def wait(self):
        self._ready.wait()

class Handler(Loader):
    
    def __init__(self):
        super().__init__()
        self._queue = queue.Queue()
        self._stopped = False

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
