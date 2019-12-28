# BOTD - python3 IRC channel daemon.
#
# bot base class.

import sys

from bl.evt import Event
from bl.hdl import Handler
from bl.pst import Cfg, Persist

from botd.flt import Fleet

def __dir__():
    return ('Bot', 'Cfg')

fleet = Fleet()

class Cfg(Cfg):

    def __init__(self):
        super().__init__()
        self.channel = ""
        self.nick = ""
        self.port = 0
        self.server = ""

class Event(Event):

    def show(self):
        for txt in self.result:
            fleet.echo(self.orig, self.channel, txt)

class Bot(Handler, Persist):

    def __init__(self):
        super().__init__()
        self.cfg = Cfg()
        self.channels = []
        self.verbose = True
        
    def announce(self, txt):
        for channel in self.channels:
            self.say(channel, txt)

    def dispatch(self, event):
        event.parse(event.txt)
        event._func = self.get_cmd(event.chk)
        if event._func:
            event._func(event)
            event.show()
        event.ready()

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
            self.raw(txt)

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
        fleet.add(self)
        if handler:
            super().start(handler)
        if output:
            self.launch(self.output)
        if input:
            self.launch(self.input)
