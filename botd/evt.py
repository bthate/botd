# BOTD - python3 IRC channel daemon.
#
# event base.

""" base event for the event handler. """


import threading

from botd.krn import kernels
from botd.obj import Object
from botd.tms import days

# defines

def __dir__():
    return ("Event", "Handler")

# classes

class Event(Object):

    """
        event class

        event base class used to define other specific events.

    """    

    def __init__(self):
        super().__init__()
        self._ready = threading.Event()
        self.verbose = True
        self.args = []
        self.channel = ""
        self.etype = "event"
        self.options = ""
        self.orig = ""
        self.origin = ""
        self.result = []
        self.txt = ""

    def display(self, o, txt=""):
        """
            display method.
        
            display object to the event origin.

         """
        txt = txt[:]
        txt += " " + "%s %s" % (self.format(o), days(o._path))
        txt = txt.strip()
        self.reply(txt)

    def format(self, o, keys=None):
        """
            format this event.

            format the event in a one string response.
        """
        if keys is None:
            keys = vars(o).keys()
        res = []
        txt = ""
        for key in keys:
            val = o.get(key, None)
            if not val:
                continue
            val = str(val)
            if key == "text":
                val = val.replace("\\n", "\n")
            res.append(val)
        for val in res:
            txt += "%s%s" % (val.strip(), " ")
        return txt.strip()

    def parse(self, txt=""):
        """
            parse method
            
            parse text into this event.

        """
        txt = txt or self.txt
        if not txt:
            return
        spl = self.txt.split()
        if not spl:
            return
        self.cmd = spl[0]
        self.args = spl[1:]
        self.rest = " ".join(self.args)

    def ready(self):
        """
            ready method.

            signal this event as ready.
            
        """
        self._ready.set()

    def reply(self, txt):
        """
            reply method.
            
            reply text to origin.
            
        """
        self.result.append(txt)

    def show(self):
        """
            show method.
            
            show result to the origin.
            
        """
        if not self.verbose:
            return
        k = kernels.get_first()
        for txt in self.result:
            k.fleet.echo(self.orig, self.channel, txt)

    def wait(self):
        """
            wait method.
            
            wait for event to complete.
            
        """
        self._ready.wait()

