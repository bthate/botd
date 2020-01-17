# BOTD - python3 IRC channel daemon.
#
# bot base class.

""" 
    provides the bot's base class.

    the Bot class runs with it's own input loop, calling Bot.poll() to return an event.
    A outloop thread can also be started to have output to the bot queued.
    
    todo: 1) write an output cache that can buffer this output.

"""

import queue
import sys

from botd.hdl import Handler
from botd.krn import kernels
from botd.obj import Cfg
from botd.thr import launch

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

class Bot(Handler):

    """
        Bot base class. 
    
        basic bot outputs to stdout.

    """

    def __init__(self):
        super().__init__()
        self._outputed = False
        self._outqueue = queue.Queue()
        self.cfg = Cfg()
        self.channels = []

    def _say(self, channel, txt, mtype="normal"):
        """
            raw output
        
            called when output is buffered.

        """
        self.raw(txt)
        
    def announce(self, txt):
        """
            annouce to all channels
        
            uses the say method on registered bots

        """
        for channel in self.channels:
            self.say(channel, txt)

    def input(self):
        """
            input loop
        
            calls the poll method of the inherited class that returns an event to process.

        """
        while not self._stopped:
            try:
                e = self.poll()
            except EOFError:
                break
            self.put(e)

    def output(self):
        """
            output loop
        
            queues output to create buffered output.

        """
        self._outputed = True
        while not self._stopped:
            channel, txt, type = self._outqueue.get()
            if txt:
                self._say(channel, txt, type)

    def poll(self):
        """
            polls for events
        
            child classes should implement this (blocking) to return the event to be processed.

        """
        pass

    def raw(self, txt):
        """
            raw output
        
            outputs directly to the screen

        """
        sys.stdout.write(str(txt) + "\n")
        sys.stdout.flush()

    def say(self, channel, txt, mtype):
        """
            say something. 
        
            output text to the channel.

        """ 
        if self._outputed:
            self._outqueue.put((channel, txt, mtype))
        else:
            self.raw(txt)

    def start(self, input=False, output=False):
        """
            start the bot
        
            add the bot to the kernels fleet and launches input,output threads.

        """
        k = kernels.get_first()
        k.fleet.add(self)
        super().start()
        if output:
            launch(self.output)
        if input:
            launch(self.input)
