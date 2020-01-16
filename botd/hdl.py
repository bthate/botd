# BOTD - python3 IRC channel daemon.
#
# event handler.

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
    
    def __init__(self):
        super().__init__()
        self._queue = queue.Queue()
        self._stopped = False
        self.cbs = Object()

    def handle_cb(self, event):
        if event.etype in self.cbs:
            self.cbs[event.etype](self, event)

    def handler(self):
        while not self._stopped:
            e = self._queue.get()
            try:
                self.handle_cb(e)
            except Exception as ex:
                logging.error(get_exception())
                e.ready()

    def poll(self):
        raise ENOTIMPLEMENTED

    def put(self, event):
        self._queue.put_nowait(event)

    def register(self, cbname, handler):
        logging.debug("register %s" % cbname)
        self.cbs[cbname] = handler        

    def start(self):
        from botd.thr import launch
        launch(self.handler)

    def stop(self):
        self._stopped = True
        self._queue.put(None)
