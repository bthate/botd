# BOTLIB - hdl.py
#
# this file is placed in the public domain

"handler (hdl)"

import inspect, os, queue, threading, time
import importlib
import importlib.util

from bot.bus import bus
from bot.dbs import list_files
from bot.obj import Default, Object, Ol, get, spl, update
from bot.prs import parse
from bot.thr import launch

__version__ = 114

debug = False
md = ""

class Event(Default):

    "event class"

    __slots__ = ("prs", "src")

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.done = threading.Event()
        self.result = []
        self.thrs = []
        self.type = "event"

    def direct(self, txt):
        "send txt to console - overload this"
        bus.say(self.orig, self.channel, txt)

    def parse(self):
        "parse an event"
        self.prs = Default()
        parse(self.prs, self.otxt or self.txt)
        args = self.prs.txt.split()
        if args:
            self.cmd = args.pop(0)
        if args:
            self.args = list(args)
            self.rest = " ".join(self.args)
            self.otype = args.pop(0)
        if args:
            self.xargs = args

    def ready(self):
        "event is handled"
        self.done.set()

    def reply(self, txt):
        "add txt to result"
        self.result.append(txt)

    def show(self):
        "display result"
        for txt in self.result:
            self.direct(txt)
        self.ready()

    def wait(self):
        "wait for event to be handled"
        self.done.wait()
        for thr in self.thrs:
            thr.join()

class Command(Event):

    def __init__(self, txt):
        super().__init__()
        self.type = "cmd"
        self.txt = txt
        self.parse()

    def direct(self, txt):
        print(txt)
 
class Handler(Object):

    "basic event handler"

    threaded = False

    def __init__(self):
        super().__init__()
        self.cbs = Object()
        self.cmds = Object()
        self.names = Ol()
        self.queue = queue.Queue()
        self.stopped = False
        self.register("cmd", cmd)
        bus.add(self)
        
    def clone(self, hdl):
        "copy callbacks"
        update(self.cmds, hdl.cmds)
        update(self.cbs, hdl.cbs)
        update(self.names, hdl.names)

    def cmd(self, txt):
        global cmd
        c = Command(txt)
        c.orig = repr(self)
        c.origin = "root@shell"
        self.dispatch(c)

    def dispatch(self, event):
        "run callbacks for event"
        event.orig = repr(self)
        event.parse()
        if event.type and event.type in self.cbs:
            self.cbs[event.type](event)

    def files(self):
        "show files in workdir"
        import bot.obj
        assert bot.obj.wd
        return list_files(bot.obj.wd)

    def init(self, mns, name="bot"):
        "call init() of modules"
        thrs = []
        for mn in spl(mns):
            try:
                spec = importlib.util.find_spec("%s.%s" % (name, mn))
            except ModuleNotFoundError:
                continue
            if spec:
                mod = self.intro(direct("%s.%s" % (name, mn)))
                func = getattr(mod, "init", None)
                if func:
                    thrs.append(func(self))
        return thrs

    def intro(self, mod):
        "introspect a module"
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if o.__code__.co_argcount == 1:
                if "obj" in o.__code__.co_varnames:
                    self.register(key, o)
                elif "event" in o.__code__.co_varnames:
                    self.cmds[key] = o
        for _key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object):
                t = "%s.%s" % (o.__module__, o.__name__)
                self.names.append(o.__name__.lower(), t)
        return mod

    def handler(self):
        "handler loop"
        while not self.stopped:
            event = self.queue.get()
            if not event:
                break
            event.thrs.append(launch(self.dispatch, event))

    def put(self, e):
        "put event on queue"
        self.queue.put_nowait(e)

    def register(self, name, callback):
        "register a callback"
        self.cbs[name] = callback

    def fromdir(self, path, name="bot"):
        "scan a modules directory"
        if not path:
            return
        for mn in [x[:-3] for x in os.listdir(path)
                   if x and x.endswith(".py")
                   and not x.startswith("__")
                   and not x == "setup.py"]:
            self.intro(direct("%s.%s" % (name, mn)))

    def start(self):
        "start handler"
        launch(self.handler)

    def stop(self):
        "stop handler"
        self.stopped = True
        self.queue.put(None)

    def walk(self, pkgnames, name="bot"):
        "walk over packages and load their modules"
        for pn in spl(pkgnames):
            mod = direct(pn)
            self.fromdir(mod.__path__[0], name)

    def wait(self):
        "wait for handler stopped status"
        if not self.stopped:
            while 1:
                time.sleep(30.0)

def cmd(obj):
    "callbackx to dispatch to command"  
    bot = bus.by_orig(obj.orig)
    if bot and obj.cmd in bot.cmds:
        f = get(bot.cmds, obj.cmd, None)
        if f:
            f(obj)
            obj.show()
    obj.ready()

def direct(name, pname=''):
    "load a module"
    return importlib.import_module(name, pname)

def mods(mn, name="bot"):
    "return all modules in a package"
    mod = []
    pkg = direct(mn)
    path = pkg.__file__ or pkg.__path__[0]
    for m in ["%s.%s" % (name, x.split(os.sep)[-1][:-3]) for x in os.listdir(path)
              if x.endswith(".py")
              and not x == "setup.py"]:
        mod.append(direct(m))
    return mod
