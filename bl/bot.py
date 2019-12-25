# BOTLIB - Framework to program bots.
#
# bot base class 

import sys

from bl.
from bl.pst import Cfg

def __dir__():
    return ('Bot', 'Cfg')

class Cfg(Cfg):

    def __init__(self):
        super().__init__()
        self.channel = ""
        self.nick = ""
        self.port = 0
        self.server = ""

class Bot(Handler):

    def __init__(self):
        super().__init__()
        self.cfg = Cfg()
        self.channels = []
        self.verbose = False
        
    def announce(self, txt):
        for channel in self.channels:
            self.say(channel, txt)

    def output(self):
        self._outputed = True
        while not self._stopped:
            channel, txt, type = self._outqueue.get()
            if self.verbose:
                print(txt)

    def poll(self):
        pass

    def raw(self, txt):
        if not self.verbose or not txt:
            return
        sys.stdout.write(str(txt) + "\n")
        sys.stdout.flush()

    def say(self, channel, txt, mtype=None) -> None:
        if self._outputed:
            self._outqueue.put((channel, txt, mtype))
        else:
            self.raw(txt)

    def start(self, handler=True, input=False, output=False):
        self.register(dispatch)
        super().start(handler)
        if output:
            self.launch(self.output)
        bl.fleet.add(self)
