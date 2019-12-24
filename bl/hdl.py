# BOTLIB - Framework to program bots.
#
# event handler.

import bl
import bl.ldr
import bl.thr
import bl.typ
import inspect
import pkgutil
import queue
import time
import threading

def __dir__():
    return ("Handler",)

class Handler(bl.ldr.Loader, bl.thr.Launcher):
    
    def __init__(self):
        super().__init__()
        self._outputed = False
        self._outqueue = queue.Queue()
        self._queue = queue.Queue()
        self._ready = threading.Event()
        self._stopped = False
        self._threaded = True
        self._type = bl.typ.get_type(self)
        self.classes = []
        self.cmds = bl.Register()
        self.handlers = []
        self.modules = {}
        self.names = {}
        self.sleep = False
        self.state = bl.Object()
        self.state.last = time.time()
        self.state.nrsend = 0
        self.verbose = True

    def get_cmd(self, cmd):
        return bl.get(self.cmds, cmd, None)

    def get_handler(self, cmd):
        return bl.get(self.handler, cmd, None)

    def handle(self, e):
        for h in self.handlers:
            h(self, e)

    def handler(self):
        while not self._stopped:
            e = self._queue.get()
            if not e:
                break
            if self._threaded:
                e._thrs.append(self.launch(self.handle, e))
            else:
                self.handle(e)
        self._ready.set()

    def input(self):
        while not self._stopped:
            e = self.poll()
            self.put(e)

    def load_mod(self, mn, force=True):
        mod = super().load_mod(mn, force=force)
        self.scan(mod)
        return mod

    def output(self):
        self._outputed = True
        while not self._stopped:
            channel, txt, type = self._outqueue.get()
            if self.verbose:
                print(txt)

    def poll(self):
        raise bl.err.ENOTIMPLEMENTED

    def put(self, event):
        self._queue.put_nowait(event)

    def register(self, handler):
        if handler not in self.handlers:
            self.handlers.append(handler)

    def say(self, channel, txt, type="chat"):
        raise bl.err.ENOTIMPLEMENTED

    def scan(self, mod):
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1 and key not in self.cmds:
                    self.cmds.register(key, o)
                    self.modules[key] = o.__module__
        for key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, bl.Persist):
                t = bl.typ.get_type(o)
                if t not in self.classes:
                    self.classes.append(t)
                    self.names[t.split(".")[-1].lower()] = str(t)
                
    def start(self, handler=True, input=True, output=True):
        if handler:
            self.launch(self.handler)
        if input:
            self.launch(self.input)
        if output:
            self.launch(self.output)

    def stop(self):
        self._stopped = True
        self._queue.put(None)

    def sync(self, other):
        self.handlers = other.handlers
        bl.update(self.cmds, other.cmds)

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
