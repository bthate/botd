# BOTD - python3 IRC channel daemon.
#
# event handler.

import inspect
import logging
import pkgutil
import queue
import time
import threading
import bl.tbl

from bl.err import ENOTIMPLEMENTED
from bl.obj import Object
from bl.pst import Register
from bl.ldr import Loader
from bl.thr import Launcher
from bl.typ import get_name, get_type


def __dir__():
    return ("Handler",)

class Handler(Loader, Launcher):

    
    def __init__(self):
        super().__init__()
        self._outputed = False
        self._outqueue = queue.Queue()
        self._queue = queue.Queue()
        self._ready = threading.Event()
        self._stopped = False
        self._threaded = True
        self._type = get_type(self)
        self.cmds = Register()
        self.handlers = []
        self.sleep = False
        self.state = Object()
        self.state.last = time.time()
        self.state.nrsend = 0
        self.verbose = True
        self.classes = bl.tbl.classes
        self.modules = bl.tbl.modules
        self.names = bl.tbl.names

    def dispatch(self, event):
        event.parse(event.txt)
        event._func = self.get_cmd(event.chk)
        if event._func:
            event._func(event)
            event.show()
        event.ready()

    def get_cmd(self, cn):
        mn = bl.tbl.modules.get(cn, None)
        if not mn:
            return
        if mn not in self.table:
            self.load_mod(mn)
        return self.cmds.get(cn, None)

    def get_handler(self, cmd):
        return self.handler.get(cmd, None)

    def handler(self):
        while not self._stopped:
            e = self._queue.get()
            self.dispatch(e)
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

    def scan(self, mod):
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1 and key not in self.cmds:
                    self.cmds.register(key, o)
                    bl.tbl.modules[key] = o.__module__
        for key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object):
                t = get_type(o)
                if t not in bl.tbl.classes:
                    bl.tbl.classes.append(t)
                    bl.tbl.names[t.split(".")[-1].lower()] = str(t)
                
    def start(self, handler=True):
        if handler:
            self.launch(self.handler)

    def stop(self):
        self._stopped = True
        self._queue.put(None)

    def walk(self, pkgname):
        if not pkgname:
             return
        mod = self.load_mod(pkgname)
        mods = [mod,]
        try:
            mns = pkgutil.iter_modules(mod.__path__, mod.__name__+".")
        except:
            mns = pkgutil.iter_modules([mod.__file__,], mod.__name__+".")
        for n in mns:
            mods.append(self.load_mod(n[1], force=True))
        return mods
