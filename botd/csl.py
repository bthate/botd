# BOTD - IRC channel daemon
#
# console code.

import sys
import threading

from botd.err import ENOTXT
from botd.evt import Event
from botd.krn import kernels
from botd.hdl import Handler
from botd.thr import launch

def __dir__():
    return ("Console",)

class Event(Event):

    def reply(self, txt):
        print(txt)
        
class Console(Handler):

    def __init__(self):
        super().__init__()
        self._connected = threading.Event()
        self._threaded = False
        
    def announce(self, txt):
        self.raw(txt)

    def poll(self):
        self._connected.wait()
        e = Event()
        e.etype = "command"
        e.origin = "root@shell"
        e.orig = repr(self)
        e.txt = input("> ")
        if not e.txt:
            raise ENOTXT 
        return e

    def input(self):
        k = kernels.get_first()
        while not self._stopped:
            try:
                e = self.poll()
            except ENOTXT:
                continue
            except EOFError:
                break
            k.put(e)
            e.wait()

    def raw(self, txt):
        sys.stdout.write(str(txt) + "\n")
        sys.stdout.flush()

    def say(self, channel, txt, type="chat"):
        self.raw(txt)
 
    def start(self):
        k = kernels.get_first()
        k.fleet.add(self)
        launch(self.input)
        self._connected.set()
