# BOTLIB - Framework to program bots.
#
# kernel tables. 

workdir = ""

import logging
import time

from bl.dbs import Db, last
from bl.err import EINIT, ENOTXT
from bl.evt import Event
from bl.hdl import Handler
from bl.log import level
from bl.obj import Object
from bl.pst import Cfg, Persist
from bl.shl import enable_history, set_completer, writepid
from bl.utl import get_mods, get_name

class Kernel(Handler, Persist):

    db = Db()
    cfg = Cfg()
    state = Object()

    def __init__(self, cfg={}, **kwargs):
        super().__init__()
        self._outputed = False
        self._started = False
        self.prompt = True
        self.verbose = True
        self.cfg.update(cfg)
        self.cfg.update(kwargs)

    def cmd(self, txt, origin=""):
        if not txt:
            return
        self.cfg.prompting = False
        c = Console()
        c.sync(self)
        c.start()
        e = Event()
        e.txt = txt
        e.options = self.cfg.options
        e.orig = repr(c)
        e.origin = origin or "root@shell"
        self.register(dispatch)
        self.prompt = False
        self.add(c)
        self.handle(e)
        e.wait()

    def init(self, modstr):
        mods = []
        for mod in get_mods(self, modstr):
            if "init" not in dir(mod):
                continue
            logging.warning("init %s" % mod.__name__)
            mod.init(self.cfg)
            mods.append(mod)
        return mods

    def input(self):
        while not self._stopped:
            try:
                e = self.poll()
            except EOFError:
                break
            self.put(e)

    def start(self, handler=True, input=False, output=False):
        if self._started:
            return
        level(self.cfg.level, self.cfg.logdir)
        self._started = True
        self.state.started = False
        self.state.starttime = time.time()
        if self.cfg.owner:
            self.users.oper(cfg.owner)
        if self.cfg.kernel:
            last(cfg)
        self.register(dispatch)
        super().start(handler)
        if input:
            self.launch(self.input)
            
    def wait(self):
        while not self._stopped:
            time.sleep(1.0)

def dispatch(handler, event):
    try:
        event.parse(event.txt)
    except ENOTXT:
        event.ready()
        return
    event._func = handler.get_cmd(event.chk)
    if event._func:
        event._calledfrom = str(event._func)
        event._func(event)
        event.show()
    event.ready()
