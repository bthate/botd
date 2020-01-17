# BOTD - python3 IRC channel daemon
#
# console code.

""" 
    console class.

    provides a class that can be used to fetch input from the console.
    typed strings can run as commands.

"""

import sys
import threading

from botd.err import ENOTXT
from botd.evt import Event
from botd.krn import kernels
from botd.hdl import Handler
from botd.thr import launch

#defines

def __dir__():
    return ("Console",)

# classes

class Event(Event):

    """
        console events.
    
        just inherits from the basic event.

    """

class Console(Handler):

    """
        Console class
    
        provided stdin input polling and stdout output.

    """

    def __init__(self):
        super().__init__()
        self._connected = threading.Event()
        self._threaded = False
        
    def announce(self, txt):
        """
            announce text.

            echo to console.

        """
        self.raw(txt)

    def poll(self):
        """
            poll method.
        
            use input to fetch text from console and create an event based on that.

        """
        self._connected.wait()
        e = Event()
        e.etype = "command"
        e.origin = "root@shell"
        e.orig = repr(self)
        e.txt = input("> ")
        if not e.txt:
            raise ENOTXT 
        return e

    def input(self):
        """
            console input loop.
        
            wait for entered command to be processed,

        """
        k = kernels.get_first()
        while not self._stopped:
            try:
                e = self.poll()
            except ENOTXT:
                continue
            except EOFError:
                break
            k.put(e)
            e.wait()

    def raw(self, txt):
        """
            raw output to stdout.
        
            flushes stdout on every write.

        """
        sys.stdout.write(str(txt) + "\n")
        sys.stdout.flush()

    def say(self, channel, txt, type="chat"):
        """
            say method.
        
            allow output to channel to be related to stdout.

        """
        self.raw(txt)
 
    def start(self):
        """
            start the console
        
            starts input loop and adds console to the kernels fleet.

        """
        k = kernels.get_first()
        k.fleet.add(self)
        launch(self.input)
        self._connected.set()
