# BOTLIB - Framework to program bots.
#
# event handler.

import inspect
import logging
import pkgutil
import queue
import time
import threading

from bl.err import ENOTIMPLEMENTED
from bl.obj import Object
from bl.pst import Register
from bl.ldr import Loader
from bl.thr import Launcher
from bl.typ import get_name, get_type

def __dir__():
    return ("Handler",)

class Handler(Loader, Launcher):

    classes = []
    cmds = Register()
    modules = {}
    names = {}
    
    def __init__(self):
        super().__init__()
        self._outputed = False
        self._outqueue = queue.Queue()
        self._queue = queue.Queue()
        self._ready = threading.Event()
        self._stopped = False
        self._threaded = True
        self._type = get_type(self)
        self.handlers = []
        self.sleep = False
        self.state = Object()
        self.state.last = time.time()
        self.state.nrsend = 0
        self.verbose = True

    def get_cmd(self, cmd):
        return self.cmds.get(cmd, None)

    def get_handler(self, cmd):
        return self.handler.get(cmd, None)

    def handle(self, e):
        for h in self.handlers:
            h(self, e)

    def handler(self):
        while not self._stopped:
            e = self._queue.get()
            e._thrs.append(self.launch(self.handle, e))
        self._ready.set()

    def load_mod(self, mn, force=True):
        logging.warning("load %s into %s" % (mn, get_name(self)))
        mod = super().load_mod(mn, force=force)
        self.scan(mod)
        return mod

    def poll(self):
        raise ENOTIMPLEMENTED

    def put(self, event):
        self._queue.put_nowait(event)

    def register(self, handler):
        if handler not in self.handlers:
            self.handlers.append(handler)

    def scan(self, mod):
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1 and key not in self.cmds:
                    self.cmds.register(key, o)
                    self.modules[key] = o.__module__
        for key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object):
                t = get_type(o)
                if t not in self.classes:
                    self.classes.append(t)
                    self.names[t.split(".")[-1].lower()] = str(t)
                
    def start(self, handler=True):
        if handler:
            self.launch(self.handler)

    def stop(self):
        self._stopped = True
        self._queue.put(None)

    def sync(self, other):
        self.handlers.extend(other.handlers)
        self.cmds.update(other.cmds)
        logging.warning("synced %s to %s" % (get_name(other), get_name(self)))

    def walk(self, pkgname):
        mod = self.load_mod(pkgname)
        mods = [mod,]
        try:
            mns = pkgutil.iter_modules(mod.__path__, mod.__name__+".")
        except:
            mns = pkgutil.iter_modules([mod.__file__,], mod.__name__+".")
        for n in mns:
            mods.append(self.load_mod(n[1], force=False))
        return mods
