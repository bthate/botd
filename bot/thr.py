# BOTLIB - the bot library !
#
#

import queue, threading, time, types

from .obj import Object

def __dir__():
    return ("Launcher", "Thr", "get_name", "launch")

class Thr(threading.Thread):

    def __init__(self, func, *args, name="noname", daemon=True):
        super().__init__(None, self.run, name, (), {}, daemon=daemon)
        self._name = name
        self._result = None
        self._queue = queue.Queue()
        self._queue.put((func, args))
        self.sleep = None
        self.state = Object()
        
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

    def launch(self, func, *args, **kwargs):
        name = kwargs.get("name", get_name(func))
        t = Thr(func, *args, name=name, daemon=True)
        t.start()
        return t

    def wait(self, *args, **kwargs):
        thr = self.launch(*args, **kwargs)
        return thr.join()

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
