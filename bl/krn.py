# BOTLIB - Framework to program bots.
#
# kernel tables. 

workdir = ""

import logging
import time

from bl.dbs import Db
from bl.err import EINIT, ENOTXT
from bl.evt import Event
from bl.flt import Fleet
from bl.hdl import Handler
from bl.log import level
from bl.obj import Object
from bl.pst import Cfg, Persist
from bl.shl import enable_history, set_completer, writepid
from bl.dbs import Db
from bl.usr import Users
from bl.utl import get_mods, get_name

class Kernel(Handler, Persist):

    db = Db()
    cfg = Cfg()
    fleet = Fleet()
    state = Object()
    users = Users()

    def __init__(self, cfg={}, **kwargs):
        super().__init__()
        self._outputed = False
        self._started = False
        self.prompt = True
        self.verbose = True
        self.cfg.update(cfg)
        self.cfg.update(kwargs)

    def add(self, bot):
        self.fleet.add(bot)

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
        if not modstr:
            return
        ok = True
        for mod in get_mods(self, modstr):
            if "init" not in dir(mod):
                continue
            n = get_name(mod)
            if self.cfg.exclude and n in self.cfg.exclude.split(","):
                continue
            try:
                mod.init()
            except EINIT as ex:
                if not self.cfg.doexec and not self.cfg.shell and not self.cfg.kernel:
                    print(str(ex))
                    ok = False
                    break
        return ok

    def show(self, event):
        for txt in event.result:
            self.fleet.echo(event.channel, txt)

    def start(self):
        if self._started:
            return
        level(self.cfg.level, self.cfg.logdir)
        self._started = True
        self.state.started = False
        self.state.starttime = time.time()
        if self.cfg.owner:
            self.users.oper(cfg.owner)
        if self.cfg.kernel:
            bl.dbs.last(cfg)
        super().start()

    def wait(self):
        while not self._stopped:
            time.sleep(1.0)

k = Kernel()

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

def launch(func, *args):
    return k.launch(func, *args)
