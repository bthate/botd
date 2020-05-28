# BOTLIB - Framework to program bots.
#
#

""" fleet (list of bots). """

import lo

class Fleet(lo.Object):

    """ A Fleet contains a list of bots. """

    #:
    bots = []

    def __iter__(self):
        return iter(Fleet.bots)

    def add(self, bot):
        """ add a bot to the fleet. """
        Fleet.bots.append(bot)

    def announce(self, txt, skip=[]):
        """ loop over all registered bots and call announce. """
        for h in self.by_type(lo.hdl.Handler):
            if skip and type(h) in skip:
                continue
            if "announce" in dir(h):
                h.announce(txt)

    def dispatch(self, event):
        """ call dispatch on all bots. """
        for b in Fleet.bots:
            if repr(b) == event.orig:
                b.dispatch(event)

    def by_orig(self, orig):
        """ return bot by originator. """
        for o in Fleet.bots:
            if repr(o) == orig:
                return o

    def by_type(self, otype, default=None):
        """ return all bots of a type. """
        res = []
        for o in Fleet.bots:
            if isinstance(o, otype):
                res.append(o)
        return res
