# BOTLIB - Framework to program bots.
#
# console code.

import sys

from bl.krn import dispatch
from bl.evt import Event
from bl.flt import Fleet
from bl.hdl import Handler
from bl.pst import Persist

def __dir__():
    return ("Console",)

fleet = Fleet()

class Event(Event):

    def show(self):
        for txt in self.result:
            print(txt)

class Console(Handler, Persist):

    def __init__(self):
        super().__init__()
        self.verbose = True
        
    def announce(self, txt):
        self.raw(txt)

    def poll(self):
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
        fleet.add(self)
        self.register(dispatch)
        super().start(False)
        self.launch(self.input)
