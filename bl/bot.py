# BOTD - python3 IRC channel daemon.
#
# bot base class.

import bl
import queue
import sys

from bl.krn import kernels
from bl.obj import Cfg
from bl.thr import launch

# defines

def __dir__():
    return ('Bot', 'Cfg')

# classes

class Cfg(Cfg):

    def __init__(self):
        super().__init__()
        self.channel = ""
        self.nick = ""
        self.port = 0
        self.server = ""

class Bot(bl.hdl.Handler):

    def __init__(self):
        super().__init__()
        self._outputed = False
        self._outqueue = queue.Queue()
        self.cfg = Cfg()
        self.channels = []
        k.fleet.add(self)

    def _say(self, channel, txt, mtype="normal"):
        self.raw(txt)
        
    def announce(self, txt):
        for channel in self.channels:
            self.say(channel, txt)

    def input(self):
        while not self._stopped:
            try:
                e = self.poll()
            except EOFError:
                break
            self.put(e)

    def output(self):
        self._outputed = True
        while not self._stopped:
            channel, txt, type = self._outqueue.get()
            if txt:
                self._say(channel, txt, type)

    def poll(self):
        pass

    def raw(self, txt):
        sys.stdout.write(str(txt) + "\n")
        sys.stdout.flush()

    def say(self, channel, txt, mtype):
        if self._outputed:
            self._outqueue.put((channel, txt, mtype))
        else:
            self.raw(txt)

    def start(self, input=False, output=False):
        super().start()
        if output:
            launch(self.output)
        if input:
            launch(self.input)

# runtime

k = kernels._get("0")