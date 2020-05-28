# LIBOBJ - library to manipulate objects.
#
#

"""event handler."""

import importlib
import inspect
import lo
import lo.exp
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

from lo import DoL, Object, locked
from lo.thr import get_name, launch
from lo.trc import get_exception

def __dir__():
    return ("Event", "Handler", "Loader")

dispatch_lock = _thread.allocate_lock()
load_lock = _thread.allocate_lock()

class Cfg(lo.Cfg):

    pass

class Loader(lo.Object):

    table = lo.Object()

    def __init__(self):
        super().__init__()
        self.cmds = lo.Object()
        self.mods = lo.Object()
        self.error = ""
                
    def direct(self, name):
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

    def find_modules(self):
        mod = self.direct("bot")
        mods = []
        for key, o in inspect.getmembers(mod, inspect.ismodule):
             if o not in mods:
                 mods.append(o)
        mod = self.direct("lo")
        for key, o in inspect.getmembers(mod, inspect.ismodule):
             if o not in mods:
                 mods.append(o)
        return mods

    def find_names(self, mod):
        names = {}
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1:
                    names[key] = o.__module__
        return names

    def find_shorts(self):
        shorts = DoL()
        for mod in self.find_modules():
            for key, o in inspect.getmembers(mod, inspect.isclass):
                if issubclass(o, lo.Object):
                    t = "%s.%s" % (o.__module__, o.__name__)
                    shorts.append(o.__name__.lower(), str(t))
        return shorts

    def find_types(self, mod):
        res = []
        for mod in self.find_modules():
            for key, o in inspect.getmembers(mod, inspect.isclass):
                if issubclass(o, lo.Object):
                    t = "%s.%s" % (o.__module__, o.__name__)
                    res.append(t)
        return res

    def init(self, mod):
        if "init" in dir(mod):
            n = lo.thr.get_name(mod)
            launch(mod.init, self, name=mod.__name__)

    @locked(load_lock)
    def load_mod(self, mn):
        if mn in Loader.table:
            logging.debug("cache %s" % mn)
            return Loader.table[mn]
        logging.debug("load %s" % mn)
        Loader.table[mn] = self.direct(mn)
        return Loader.table[mn]

    def walk(self, mns, init=False):
        mods = []
        for mn in mns.split(","):
            if not mn:
                continue
            loc = None
            try:
                m = self.load_mod(mn)
            except Exception as ex:
                if mn not in str(ex):
                    raise
                logging.warning(str(ex).lower())
                continue
            mods.append(m)
            try:
                loc = m.__spec__.submodule_search_locations
            except AttributeError:
                try:
                    loc = [m.__file__,]
                except AttributeError:
                    continue
            if not loc:
                continue
            for md in loc:
                logging.debug("location %s" % md)
                if not os.path.isdir(md):
                    try:
                        fns = pkg_resources.resource_listdir(md, "")
                    except ModuleNotFoundError:
                        fns = dir(m)
                else:
                    fns = os.listdir(md)
                for x in fns:
                    if x.startswith("__"):
                        continue
                    if x.endswith(".py"):
                        mmn = "%s.%s" % (mn, x[:-3])
                    elif not x.endswith("~"):
                        mmn = "%s.%s" % (mn, x)
                    else:
                        continue
                    module = None
                    try:
                        module = self.load_mod(mmn)
                    except Exception as ex:
                        if mn not in str(ex):
                            raise
                        logging.warning(str(ex).lower())
                        continue
                    if not module:
                        continue
                    mods.append(module)
        for mod in mods:
            self.scan(mod)
            if init:
                self.init(mod)
        return mods

    def scan(self, mod):
        cmds = self.find_cmds(mod)
        self.cmds.update(cmds)
        modules = self.find_names(mod)
        self.mods.update(modules)
        return cmds

class Handler(Loader):
 
    def __init__(self):
        super().__init__()
        self._queue = queue.Queue()
        self._closed = threading.Event()
        self._stopped = False
        self.cbs = lo.Object()
        self.outcache = DoL()
        self.register("command", dispatch)

    def handle_cb(self, event):
        if event.etype in self.cbs:
            try:
                self.cbs[event.etype](self, event)
            except Exception as ex:
                self.error = get_exception()
                logging.debug("error %s" % self.error)
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
        logging.warning("stop %s" % get_name(self))
        self._closed.set()

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
        
    def wait(self, nrsec):
        while not self._stopped:
            time.sleep(nrsec)

class Event(lo.Object):

    def __init__(self):
        super().__init__()
        self._error = ""
        self._ready = threading.Event()
        self._thrs = []
        self.args = []
        self.channel = ""
        self.etype = "event"
        self.index = None
        self.options = lo.cfg.options
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
        if txt:
            self.txt = txt
        for arg in self.options.split(","):
            try:
                self.index = int(arg)
            except ValueError:
                continue
        if not self.txt:
            return
        if self.index == None and "-o" in self.txt:
            try:
                self.index = int(self.txt.split("-o")[-1].split()[0])            
            except (ValueError, IndexError):
                pass            
        spl = self.txt.split()
        if not spl:
            return
        donext = False
        indexes = []
        i = 0
        for p in spl:
            if donext:
                index = int(p)
                donext = False
                indexes.append(i)
                continue
            if p == "-o":
                donext = True
            i += 1
        for i in indexes:
            del spl[i]
        self.txt = " ".join(spl)
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

    def wait(self, nrsec=None):
        self._ready.wait(nrsec)

class Command(Event):

    def __init__(self, txt, origin="root@shell", orig=None):
        super().__init__()
        self.etype = "command"
        self.orig = orig
        self.txt = txt
        self.parse()
        self.verbose = lo.cfg.verbose
        
def dispatch(handler, event):
    if not event.txt:
        event.ready()
        return
    event.parse()
    if "_func" not in event:
        chk = event.txt.split()[0]
        event._func = handler.cmds.get(chk, None)
    if event._func:
        logging.debug("dispatch %s (%s)" % (event.txt, event.origin))
        event._func(event)
        event.show()
    event.ready()
    del event
