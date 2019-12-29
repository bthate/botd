# BOTD - python3 IRC channel daemon.
#
# console code.

import sys
import threading

from bl.err import ENOTXT
from bl.evt import Event
from bl.hdl import Handler
from bl.pst import Persist
from bl.thr import launch

def __dir__():
    return ("Console",)

class Event(Event):

    def show(self):
        for txt in self.result:
            print(txt)

class Console(Handler, Persist):

    def __init__(self):
        super().__init__()
        self._connected = threading.Event()
        self._threaded = False
                
    def announce(self, txt):
        self.raw(txt)

    def cmd(self, txt, origin=""):
        if not txt:
            return
        e = Event()
        e.txt = txt
        e.orig = repr(self)
        e.origin = origin or "root@shell"
        self.dispatch(e)
        e.wait()

    def poll(self):
        self._connected.wait()
        e = Event()
        e.orig = repr(self)
        e.origin = "root@shell"
        e.txt = input("> ")
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
            except ENOTXT:
                continue

    def raw(self, txt):
        sys.stdout.write(str(txt) + "\n")
        sys.stdout.flush()

    def say(self, channel, txt, type="chat"):
        self.raw(txt)
 
    def start(self):
        launch(self.input)
        self._connected.set()
