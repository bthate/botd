# BOTD - python3 IRC channel daemon.
#
# event handler.

import bl
import inspect
import logging
import pkgutil
import queue
import time
import threading

def __dir__():
    return ("Handler",)

class Handler(bl.ldr.Loader):
    
    def __init__(self):
        super().__init__()
        self._queue = queue.Queue()
        self._stopped = False
        self.cmds = bl.Register()

    def dispatch(self, event):
        event.parse(event.txt)
        event._func = self.get_cmd(event.chk)
        if event._func:
            event._func(event)
            event.show(self)
        event.ready()

    def handler(self):
        while not self._stopped:
            e = self._queue.get()
            self.dispatch(e)

    def poll(self):
        raise ENOTIMPLEMENTED

    def put(self, event):
        self._queue.put_nowait(event)

    def start(self):
        launch(self.handler)

    def stop(self):
        self._stopped = True
        self._queue.put(None)
