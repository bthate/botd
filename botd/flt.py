# BOTD - python3 IRC channel daemon.
#
# list of bots. 

from botd.obj import Object

# defines

def __dir__():
    return ("Fleet",)

# classes

class Fleet(Object):

    bots = []

    def __iter__(self):
        return iter(self.bots)

    def add(self, bot):
        if bot not in self.bots:
            self.bots.append(bot)
        return self

    def announce(self, txt):
        for b in self.bots:
            b.announce(str(txt))

    def echo(self, bid, channel, txt, mtype="chat"):
        b = self.get_bot(bid)
        if b:
            b.say(channel, txt, mtype)

    def get_bot(self, bid):
        res = None
        for b in self.bots:
            if str(bid) in repr(b):
                res = b
                break
        return res

    def match(self, m):
        for b in self.bots:
            if m not in repr(b):
                continue
            return b

    def remove(self, bot):
        self.bots.remove(bot)
