# BOTD - python3 IRC channel daemon.
#
# console code.

import sys
import threading

from bl.krn import dispatch
from bl.evt import Event
from bl.hdl import Handler
from bl.pst import Persist

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
        self.verbose = True
        
    def announce(self, txt):
        self.raw(txt)

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
            dispatch(self, e)
            e.wait()

    def raw(self, txt):
        if not self.verbose or not txt:
            return
        sys.stdout.write(str(txt) + "\n")
        sys.stdout.flush()

    def say(self, channel, txt, type="chat"):
        self.raw(txt)
 
    def start(self):
        self.register(dispatch)
        super().start(False)
        self.launch(self.input)
        self._connected.set()