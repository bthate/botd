# BOTD - python3 IRC channel daemon.
#
# console code.

import sys
import threading

from bl.err import ENOTXT
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

    def dispatch(self, event):
        try:
            event.parse(event.txt)
        except ENOTXT:
            event.ready()
            return
        event._func = self.get_cmd(event.chk)
        if event._func:
            event._func(event)
            event.show()
        event.ready()

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
            self.dispatch(e)
            e.wait()

    def raw(self, txt):
        if not self.verbose or not txt:
            return
        sys.stdout.write(str(txt) + "\n")
        sys.stdout.flush()

    def say(self, channel, txt, type="chat"):
        self.raw(txt)
 
    def start(self):
        super().start()
        self.launch(self.input)
        self._connected.set()
