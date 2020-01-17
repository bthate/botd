# BOTD - python3 IRC channel daemon.
#
# event handler.

"""
    the event handler.
    
    handles events putted to the handler's queue.
    
"""


import logging
import queue

from botd.ldr import Loader
from botd.obj import Object
from botd.thr import launch
from botd.trc import get_exception
from botd.utl import get_name

# defines

def __dir__():
    return ("Handler",)

# classes

class Handler(Loader):
 
    """
        handler class
        
        class used to provide to event handling to various bots.
        
    """
   
    def __init__(self):
        super().__init__()
        self._queue = queue.Queue()
        self._stopped = False
        self.cbs = Object()

    def handle_cb(self, event):
        """
            handle_cb method.
            
            calls callbacks based on the 'etype' attribute of an object.
            
        """
        if event.etype in self.cbs:
            self.cbs[event.etype](self, event)

    def handler(self):
        """
            handler method.
            
            loop to process events.
            
        """
        while not self._stopped:
            e = self._queue.get()
            try:
                self.handle_cb(e)
            except Exception as ex:
                logging.error(get_exception())
                e.ready()

    def poll(self):
        """
            poll method.
            
            return an event to be processed (should block).
            
        """
        raise ENOTIMPLEMENTED

    def put(self, event):
        """
            put method
            
            put an event on the processing queue.
            
        """
        self._queue.put_nowait(event)

    def register(self, cbname, handler):
        """
            register method.
            
            add callback to the event handler (for a specific 'etype').

        """
        logging.debug("register %s" % cbname)
        self.cbs[cbname] = handler        

    def start(self):
        """
            start method.
            
            start the handler loop in it's own thread.
            
        """
        from botd.thr import launch
        launch(self.handler)

    def stop(self):
        """
            stop method.
            
            stop the event handling loop.
            
        """
        self._stopped = True
        self._queue.put(None)
