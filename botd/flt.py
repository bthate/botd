# BOTD - IRC channel daemon.
#
# list of bots. 

"""
    fleet module
    
    fleet is a list of bots that can be used to broadcast text or send text to a specific bot registered on the fleet.

"""

from botd.obj import Object

# defines

def __dir__():
    return ("Fleet",)

# classes

class Fleet(Object):

    """
        fleet class

        contains a bots list to hold references to all registed bots.
        
    """

    bots = []

    def __iter__(self):
        return iter(self.bots)

    def add(self, bot):
        """
            add method.
            
            adds a bot to the fleet.

        """
        if bot not in self.bots:
            self.bots.append(bot)
        return self

    def announce(self, txt):
        """
            announce method.
            
            broadcast text to all registered bots.
            
        """
        for b in self.bots:
            b.announce(str(txt))

    def echo(self, bid, channel, txt, mtype="chat"):
        """
            echo method.
            
            send text to a specific bot, use repr(bot) as the bot id.

        """
        b = self.get_bot(bid)
        if b:
            b.say(channel, txt, mtype)

    def get_bot(self, bid):
        """
            get_bot method.
            
            return the bot with same bot identity.
            
        """ 
        res = None
        for b in self.bots:
            if str(bid) in repr(b):
                res = b
                break
        return res

    def remove(self, bot):
        """
            remove method.
            
            remove bot from fleet.
            
        """
        self.bots.remove(bot)
