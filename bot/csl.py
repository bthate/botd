# BOTLIB - the bot library !
#
#

import sys, threading

from .krn import k
from .obj import Cfg, Object
from .hdl import Event, Handler
from .shl import setcompleter
from .thr import launch

class Cfg(Cfg):

    pass

class Console(Object):

    def announce(self, txt):
        self.raw(txt)

    def input(self):
        while 1:
            event = self.poll()
            if not event:
                break
            if not event.txt:
                continue
            event.orig = repr(self)
            k.queue.put(event)
            event.wait()

    def poll(self):
        e = Event()
        e.parse(input("> "))
        return e

    def raw(self, txt):
        print(txt.rstrip())

    def say(self, channel, txt, type="chat"):
        self.raw(txt)

    def start(self):
        try:
            from .tbl import names
            setcompleter(names)
        except:
            pass
        launch(self.input)
