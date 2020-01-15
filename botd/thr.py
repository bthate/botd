# BOTD - python3 IRC channel daemon.
#
# threading.

import logging
import queue
import threading
import types

from botd.trc import get_exception
from botd.utl import get_name

# defines

def __dir__():
    return ("Launcher", "Thr", "launch")

# classes

class Thr(threading.Thread):

    def __init__(self, func, *args, name="noname", daemon=True):
        super().__init__(None, self.run, name, (), {}, daemon=daemon)
        self._name = name
        self._result = None
        self._queue = queue.Queue()
        self._queue.put((func, args))

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def run(self):
        func, args = self._queue.get()
        self._result = func(*args)

    def join(self, timeout=None):
        super().join(timeout)
        return self._result


class Launcher:

    def __init__(self):
        super().__init__()
        self._queue = queue.Queue()
        self._stopped = False

    def launch(self, func, *args, **kwargs):
        logging.debug("launch %s" % get_name(func))
        name = ""
        try:
            name = kwargs.get("name", args[0].name or args[0].txt)
        except (AttributeError, IndexError):
            name = get_name(func)
        t = Thr(func, *args, name=name)
        t.start()
        return t

    def start(self):
        while not self._stopped:
            t = self._queue.get()
            t.start()

# functions

def launch(func, *args):
    l = Launcher()
    return l.launch(func, *args)
