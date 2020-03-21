# BOTLIB - Framework to program bots.
#
#

import bot
import lo

class Fleet(lo.Object):

    bots = []

    def __iter__(self):
        return iter(Fleet.bots)

    def add(self, bot):
        Fleet.bots.append(bot)

    def announce(self, txt, skip=[]):
        for h in self.by_type(lo.hdl.Handler):
            if skip and type(h) in skip:
                continue
            if "announce" in dir(h):
                h.announce(txt)

    def dispatch(self, event):
        for o in Fleet.bots:
            if repr(o) == event.orig:
                o.dispatch(event)

    def by_orig(self, orig):
        for o in Fleet.bots:
            if repr(o) == orig:
                return o

    def by_type(self, otype, default=None):
        res = []
        for o in Fleet.bots:
            if isinstance(o, otype):
                res.append(o)
        return res
