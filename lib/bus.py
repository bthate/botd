"announce to listeners"

from obj import Object

class Bus(Object):

    "bus class"

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

    def dispatch(self, event):
        "dispatch on all listeners"
        for b in Bus.objs:
            if repr(b) == event.orig:
                b.dispatch(event)

    def by_orig(self, orig):
        "fetch listener by orig"
        for o in Bus.objs:
            if repr(o) == orig:
                return o

    def say(self, orig, channel, txt):
        "say something to specific listener"
        for o in Bus.objs:
            if repr(o) == orig:
                o.say(channel, str(txt))

bus = Bus()
