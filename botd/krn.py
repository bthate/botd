# BOTD - python3 IRC channel daemon.
#
# kernel for boot proces.

__version__ = 1

import logging
import time

from botd.err import EINIT
from botd.flt import Fleet
from botd.hdl import Event
from botd.ldr import Loader
from botd.obj import Cfg, Object
from botd.shl import enable_history, set_completer, writepid
from botd.thr import launch
from botd.trc import get_exception
from botd.usr import Users
from botd.utl import get_name

# defines

def __dir__():
    return ("Cfg", "Kernel", "Kernels", "kernels")

starttime = time.time()

# classes

class Cfg(Cfg):

    pass

class Kernel(Loader):

    cfg = Cfg()
    fleet = Fleet()
    users = Users()
        
    def __init__(self, cfg=None, **kwargs):
        super().__init__()
        self._stopped = False
        self._skip = False
        self.cfg.modules = ""
        self.cfg.update(cfg or {})
        self.cfg.update(kwargs)
        
    def dispatch(self, event):
        if not event.txt:
            return
        event.parse()
        chk = event.txt.split()[0]
        try:
            event._func = self.get_cmd(chk)
        except Exception as ex:
            logging.error(get_exception())
            return
        if event._func:
            event._func(event)
            event.show()
        event.ready()

    def init(self, mns):
        mods = []
        for mod in self.walk(mns):
            if "init" in dir(mod):
                logging.warning("init %s" % mod.__name__)
                try:
                    mod.init(self)
                except EINIT as ex:
                    print(ex)
                    self._skip = True
                    return
                mods.append(mod)
        return mods

    def register(self, k, v):
        self.cmds.set(k, v)

    def start(self):
        kernels.add(self)
        if self.cfg.shell:
            from botd.csl import Console
            c = Console()
            c.start()
        if not self.cfg.modules:
            self.cfg.modules = "botd"
        self.init(self.cfg.modules)

    def wait(self):
        while not self._stopped:
            time.sleep(1.0)

class Kernels(Object):

    kernels = []
    nr = 0

    def add(self, kernel):
        logging.warning("add %s" % get_name(kernel))
        if kernel not in Kernels.kernels:
            Kernels.kernels.append(kernel)
            Kernels.nr += 1

    def get(self, nr, default=None):
        return Kernels.kernels[nr]

# runtime

kernels = Kernels()
