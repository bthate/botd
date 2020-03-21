# LIBOBJ - library to manipulate objects.
#
#

import logging
import queue
import threading
import types

def __dir__():
    return ("Launcher", "Thr", "get_name", "launch")

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
        self.setName(self._name)
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
        name = kwargs.get("name", get_name(func))
        logging.debug("launch %s" % name)
        t = Thr(func, *args, name=name)
        t.start()
        return t

def get_name(o):
    t = type(o)
    if t == types.ModuleType:
        return o.__name__
    try:
        n = "%s.%s" % (o.__self__.__class__.__name__, o.__name__)
    except AttributeError:
        try:
            n = "%s.%s" % (o.__class__.__name__, o.__name__)
        except AttributeError:
            try:
                n = o.__class__.__name__
            except AttributeError:
                n = o.__name__
    return n

l = Launcher()

def launch(func, *args, **kwargs):
    return l.launch(func, *args, **kwargs)
