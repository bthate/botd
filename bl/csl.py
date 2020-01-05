# BOTD - python3 IRC channel daemon.
#
# console code.

import bl
import sys
import threading

from bl.err import ENOTXT
from bl.flt import Fleet
from bl.krn import kernels
from bl.obj import get
from bl.hdl import Event, Handler
from bl.thr import launch

#defines

def __dir__():
    return ("Console", "init")


def init(kernel):
    csl = Console()
    csl.cmds = kernel.cmds
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
        k.fleet.add(self)
        
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
        launch(self.input)
        self._connected.set()

# runtime

k = get(kernels, "0", None)
