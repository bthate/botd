# BOTLIB - Framework to program bots.
#
# console code.

import bl
import sys
import threading

from botd.err import ENOTXT
from botd.flt import Fleet
from botd.krn import kernels
from botd.hdl import Event, Handler
from botd.thr import launch

#defines

def __dir__():
    return ("Console", "init")

def init(kernel):
    csl = Console()
    csl.start()
    return csl

# classes

class Event(Event):

    pass

class Console(Handler):

    def __init__(self):
        super().__init__()
        self._connected = threading.Event()
        self._threaded = False
        
    def announce(self, txt):
        self.raw(txt)

    def cmd(self, txt):
        e = Event()
        e.txt = txt
        e.orig = repr(self)
        e.origin = "root@shell"
        self.dispatch(e)
        e.wait()

    def poll(self):
        self._connected.wait()
        e = Event()
        e.origin = "root@shell"
        e.orig = repr(self)
        e.txt = input("> ")
        if not e.txt:
            raise ENOTXT 
        return e

    def input(self):
        while not self._stopped:
            try:
                e = self.poll()
            except ENOTXT:
                continue
            except EOFError:
                break
            k.dispatch(e)
            e.wait()

    def raw(self, txt):
        sys.stdout.write(str(txt) + "\n")
        sys.stdout.flush()

    def say(self, channel, txt, type="chat"):
        self.raw(txt)
 
    def start(self):
        k.fleet.add(self)
        launch(self.input)
        self._connected.set()

# runtime

k = kernels.get(0)
