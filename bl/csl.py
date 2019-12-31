# BOTD - python3 IRC channel daemon.
#
# console code.

import bl
import sys
import threading

from bl.hdl import Event, Handler
from bl.thr import launch

def __dir__():
    return ("Console", "init")

def init(kernel):
    csl = Console()
    csl.cmds = kernel.cmds
    csl.start()
    return csl

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
        e = bl.evt.Event()
        e.txt = txt
        e.orig = repr(self)
        e.origin = "root@shell"
        if e.txt:
            e.chk = e.txt.split()[0]
        self.dispatch(e)
        e.wait()

    def poll(self):
        self._connected.wait()
        e = bl.hdl.Event()
        e.origin = "root@shell"
        e.orig = repr(self)
        e.txt = input("> ")
        if e.txt:
            e.chk = e.txt.split()[0]
        return e

    def input(self):
        while not self._stopped:
            try:
                e = self.poll()
            except EOFError:
                break
            try:
                self.dispatch(e)
                e.wait()
            except bl.err.ENOTXT:
                continue

    def raw(self, txt):
        sys.stdout.write(str(txt) + "\n")
        sys.stdout.flush()

    def say(self, channel, txt, type="chat"):
        self.raw(txt)
 
    def start(self):
        launch(self.input)
        self._connected.set()
