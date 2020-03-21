# LIBOBJ - library to manipulate objects.
#
#

import importlib
import inspect
import lo
import lo.tbl
import lo.tms
import lo.typ
import lo.thr
import logging
import os
import pkg_resources
import queue
import sys
import threading
import time
import _thread

from lo import DoL, locked
from lo.thr import launch
from lo.trc import get_exception

def __dir__():
    return ("Event", "Handler", "Loader")

dispatch_lock = _thread.allocate_lock()
load_lock = _thread.allocate_lock()

class EINIT(Exception):

    pass

class ENOMODULE(Exception):

    pass

class Loader(lo.Object):

    table = lo.Object()

    def __init__(self):
        super().__init__()
        self.cmds = lo.Object()
        self.error = ""
                
    def direct(self, name):
        logging.warn("direct %s" % name)
        return importlib.import_module(name)

    def find_callbacks(self, mod):
        cbs = {}
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if o.__code__.co_argcount == 2:
                cbs[key] = o
        return cbs

    def find_cmds(self, mod):
        cmds = {}
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1:
                    cmds[key] = o
        return cmds

    def find_modules(self, mod):
        modules = {}
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1:
                    modules[key] = o.__module__
        return modules

    def find_names(self, mod):
        names = DoL()
        for key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, lo.Object):
                t = "%s.%s" % (o.__module__, o.__name__)
                names.append(o.__name__.lower(), str(t))
        return names
        
    def init(self, mods):
        for mod in mods:
            if "init" in dir(mod):
                n = lo.thr.get_name(mod)
                launch(mod.init, self, name=mod.__name__)

    @locked(load_lock)
    def load_mod(self, mn, force=False):
        if not force and mn in Loader.table:
            logging.debug("cache %s" % mn)
            return Loader.table[mn]
        mod = None
        if not force and mn in sys.modules:
            return sys.modules[mn]
        else:
            Loader.table[mn] = self.direct(mn)
        logging.warning("load %s" % mn)
        return Loader.table[mn]

    def walk(self, mns, init=False, force=False):
        if not mns:
            return
        mods = []
        for mn in mns.split(","):
            if not mn:
                continue
            try:
                m = self.load_mod(mn, force)
            except ModuleNotFoundError:
                logging.warning("%s not found" % mn)
                continue
            loc = None
            if "__spec__" in dir(m):
                loc = m.__spec__.submodule_search_locations
            if not loc:
                mods.append(m)
                continue
            for md in loc:
                m = None
                if not os.path.isdir(md):
                    fns = pkg_resources.resource_listdir(mn, "")
                else:
                    fns = os.listdir(md)
                for x in fns:
                    if x.endswith(".py"):
                        mmn = "%s.%s" % (mn, x[:-3])
                        try:
                            m = self.load_mod(mmn, force)
                        except ModuleNotFoundError:
                            continue
                    if m and m not in mods:
                        mods.append(m)
        for mod in mods:
            cmds = self.find_cmds(mod)
            self.cmds.update(cmds)
            modules = self.find_modules(mod)
            lo.tbl.modules.update(modules)
            names = self.find_names(mod)
            lo.tbl.names.update(names)
        if init:
            self.init(mods)
        return mods

class Handler(Loader):
 
    def __init__(self):
        super().__init__()
        self._queue = queue.Queue()
        self._stopped = False
        self.cbs = lo.Object()
        self.outcache = DoL()
        self.register("command", dispatch_autoload)

    def handle_cb(self, event):
        if event.etype in self.cbs:
            try:
                self.cbs[event.etype](self, event)
            except Exception as ex:
                self.error = get_exception()
                logging.debug(self.error)
                if lo.cfg.bork:
                    logging.error("bork")
                    _thread.interrupt_main()
        event.ready()

    def handler(self):
        while not self._stopped:
            e = self._queue.get()
            if e == None:
                break
            if e.threaded:
                launch(self.handle_cb, e , name="%s %s" % (e.etype, e.txt))
            else:
                self.handle_cb(e)

    def poll(self):
        raise ENOTIMPLEMENTED

    def put(self, event):
        self._queue.put_nowait(event)

    def register(self, cbname, handler):
        self.cbs[cbname] = handler        

    def start(self, handler=True):
        if handler:
            launch(self.handler)

    def stop(self):
        self._stopped = True
        self._queue.put(None)

    def wait(self):
        while not self._stopped:
            time.sleep(1.0)

class Event(lo.Object):

    def __init__(self):
        super().__init__()
        self._ready = threading.Event()
        self.args = []
        self.channel = ""
        self.etype = "event"
        self.options = ""
        self.orig = ""
        self.origin = ""
        self.result = []
        self.threaded = False
        self.txt = ""

    def display(self, o, txt="", keys=None, options="t", post="", strict=False):
        if not keys:
            keys = list(o.keys())
        txt = txt[:]
        txt += " %s" % self.format(o, keys, strict=strict) 
        if "t" in options:
           txt += " %s" % lo.tms.elapsed(time.time() - lo.fntime(o._path))
        if post:
           txt += " " + post
        txt = txt.strip()
        self.reply(txt)

    def format(self, o, keys=None, strict=False):
        if keys is None:
            keys = list(vars(o).keys())
        res = []
        txt = ""
        for key in keys:
            val = o.get(key)
            if not val:
                continue
            val = str(val)
            if key == "text":
                val = val.replace("\\n", "\n")
            res.append((key, val))
        for key, val in res:
            if strict:
                txt += "%s%s" % (val.strip(), " ")
            else:
                txt += "%s=%s%s" % (key, val.strip(), " ")
        return txt.strip()

    def missing(self, txt):
        self.reply(txt)
        self.ready()

    def parse(self, txt=""):
        txt = txt or self.txt
        if not txt:
            return
        spl = self.txt.split()
        if not spl:
            return
        self.cmd = spl[0].lower()
        self.args = spl[1:]
        self.rest = " ".join(self.args)

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self.result.append(txt)
 
    def show(self):
        for txt in self.result:
            print(txt)

    def wait(self):
        self._ready.wait()

class Command(Event):

    def __init__(self):
        super().__init__()
        self.etype = "command"
        
def dispatch(handler, event):
    if not event.txt:
        event.ready()
        return
    event.parse()
    logging.debug("dispatch %s" % event.txt)
    if "_func" not in event:
        chk = event.txt.split()[0]
        event._func = handler.cmds.get(chk, None)
    if event._func:
        event._func(event)
        event.show()
    event.ready()
    del event

def dispatch_autoload(handler, event):
    if not event.txt:
        event.ready()
        return
    event.parse()
    logging.debug("dispatch_autoload %s" % event.txt)
    if "_func" not in event or not event._func:
        chk = event.txt.split()[0].lower()
        event._func = handler.cmds.get(chk, None)
        if not event._func:
            modname = lo.tbl.modules.get(chk, None)
            if modname:
                 handler.walk(modname)
            event._func = handler.cmds.get(chk, None)
    if event._func:
        event._func(event)
        event.show()
    event.ready()
    del event
