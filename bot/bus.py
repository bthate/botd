# BOTLIB - bus.py
#
# this file is placed in the public domain

"announce to listeners"

from bot.obj import Object

class Bus(Object):

    "bus class - registered recipient event handler"

    objs = []

    def __call__(self, *args, **kwargs):
        return self.objs

    def __iter__(self):
        return iter(Bus.objs)

    def add(self, obj):
        "add listener to bus"
        Bus.objs.append(obj)

    def announce(self, txt, skip=None):
        "announce to all listeners"
        for h in self.objs:
            if skip is not None and isinstance(h, skip):
                continue
            if "announce" in dir(h):
                h.announce(txt)

    def by_orig(self, orig):
        "fetch listener by orig"
        for o in Bus.objs:
            if repr(o) == orig:
                return o

    def dispatch(self, event):
        for o in Bus.objs:
            o.dispatch(event)

    def say(self, orig, channel, txt):
        "say something to specific listener"
        for o in Bus.objs:
            if repr(o) == orig:
                o.say(channel, str(txt))

bus = Bus()
