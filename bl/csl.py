# BOTD - python3 IRC channel daemon.
#
# console code.

import bl
import sys
import threading

def __dir__():
    return ("Console", "init")

def init(kernel):
    csl = Console()
    csl.cmds = kernel.cmds
    csl.start()
    return csl

class Event(bl.evt.Event):

    def show(self):
        for txt in self.result:
            print(txt)

class Console(bl.hdl.Handler):

    def __init__(self):
        super().__init__()
        self._connected = threading.Event()
        self._threaded = False
                
    def announce(self, txt):
        self.raw(txt)

    def cmd(self, txt, origin=""):
        e = bl.evt.Event()
        e.txt = txt
        e.orig = repr(self)
        e.origin = origin or "root@shell"
        self.dispatch(e)
        e.wait()

    def poll(self):
        self._connected.wait()
        e = bl.evt.Event(origin="root@shell")
        e.orig = repr(self)
        e.txt = input("> ")
        return e

    def input(self):
        while not self._stopped:
            try:
                e = self.poll()
            except bl.err.EOFError:
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
        bl.launch(self.input)
        self._connected.set()

