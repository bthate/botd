"handler (hdl)"

import importlib, inspect, os, queue, sys, threading, time
import importlib.util

from dbs import list_files
from obj import Default, Object, Ol, get_type, spl, update
from prs import parse
from thr import launch, get_exception

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

    def direct(self, txt):
        "send txt to console"
        print(txt)

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

class Handler(Object):

    "basic event handler"

    threaded = False

    def __init__(self):
        super().__init__()
        self.cbs = Object()
        self.names = Ol()
        self.queue = queue.Queue()
        self.stopped = False

    def clone(self, hdl):
        "copy callbacks"
        update(self.cbs, hdl.cbs)
        update(self.names, hdl.names)

    def cmd(self, txt):
        "do a command"
        e = Event()
        e.txt = txt
        return self.dispatch(e)

    def dispatch(self, event):
        "run callbacks for event"
        if not event.src:
            event.src = self
        event.parse()
        if event.cmd and event.cmd in self.cbs:
            self.cbs[event.cmd](event)
            event.show()
        event.ready()

    def files(self):
        "show files in workdir"
        import obj
        assert obj.wd
        return list_files(obj.wd)

    def init(self, mns):
        "call init() of modules"
        thrs = []
        for mn in spl(mns):
            try:
                spec = importlib.util.find_spec(mn)
            except ModuleNotFoundError:
                print("%s not found" % mn)
                continue
            if spec:
                mod = self.intro(direct(mn))
                func = getattr(mod, "init", None)
                if func:
                    thrs.append(func(self))
        return thrs

    def intro(self, mod):
        "introspect a module"
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1:
                    self.register(key, o) 
        for _key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object):
                t = "%s.%s" % (o.__module__, o.__name__)
                self.names.append(o.__name__.lower(), t)
        return mod
        
    def mods(self, pkgname):
        path = os.path.dirname(direct(pkgname).__file__)
        res = []
        for mn in [x[:-3] for x in os.listdir(path)
                          if x and x.endswith(".py")
                          and not x.startswith("__")
                          and not x == "setup.py"]:
              res.append(direct(mn))
        return res

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

    def fromdir(self, path):
        "scan a modules directory"
        if not path:
            return
        sys.path.insert(0, path)
        for mn in [x[:-3] for x in os.listdir(path)
                          if x and x.endswith(".py")
                          and not x.startswith("__")
                          and not x == "setup.py"]:
            self.intro(direct(mn))

    def scan(self, modname):
        "scan a modules directory"
        path = os.path.dirname(direct(modname).__file__)
        self.fromdir(path)

    def start(self):
        "start handler"
        launch(self.handler)

    def stop(self):
        "stop handler"
        self.stopped = True
        self.queue.put(None)

    def walk(self, pkgnames):
        "walk over packages and load their modules"
        for name in spl(pkgnames):
            mod = direct(name)
            self.fromdir(mod.__path__[0])
            
    def wait(self):
        "wait for handler stopped status"
        if not self.stopped:
            while 1:
                time.sleep(30.0)

def direct(name, pname=''):
    "load a module"
    return importlib.import_module(name, pname)

def mods(mn):
    "return all modules in a package"
    mod = []
    pkg = direct(mn)
    path = os.path.dirname(pkg.__file__ or pkg.__path__[0])
    for m in [x.split(os.sep)[-1][:-3] for x in os.listdir(path) 
                                  if x.endswith(".py")
                                  and not x == "setup.py"]:
        mod.append(direct(m))
    return mod
