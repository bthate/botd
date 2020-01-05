# BOTD - python3 IRC channel daemon.
#
# module loader.

import importlib
import os
import types

from bl.obj import Object, get, keys, update, xdir
from bl.trc import get_exception
from bl.typ import get_name, get_type

# defines

def __dir__():
    return ("Loader",)

# classes

class Loader(Object):
    
    def __init__(self):
        super().__init__()
        self.cmds = Object()
        self.names = Object()
        self.table = Object()

    def direct(self, name):
        return importlib.import_module(name)

    def get_mn(self, pn):
        return keys(self.table)

    def get_cmd(self, cn):
        return get(self.cmds, cn, None)

    def get_mods(self, ms):
        for mn in ms.split(","):
             if not mn:
                 continue
             try:
                 mod = self.direct(mn)
             except ModuleNotFoundError as ex:
                 if self.cfg and self.cfg.name:
                     try:
                         mod = self.direct("%s.%s" % (self.cfg.name, mn)) 
                     except ModuleNotFoundError:
                         raise ex
             yield mod

    def introspect(self, mod):
        for key in xdir(mod, "_"):
            o = getattr(mod, key)
            if type(o) == types.FunctionType and "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1:
                    if key in self.cmds:
                        continue
                    self.cmds[key] = o
            if type(o) == type and issubclass(o, Object):
                n = key.split(".")[-1].lower()
                if n in self.names:
                    continue
                self.names[n] = "%s.%s" % (mod.__name__, o.__name__)

    def walk(self, mn):
        mods = []
        for mod in self.get_mods(mn):
            loc = mod.__spec__.submodule_search_locations
            if not loc:
                mods.append(mod)
                self.introspect(mod)
                continue
            for md in loc:
                for x in os.listdir(md):
                    if x.endswith(".py"):
                        mmn = "%s.%s" % (mn, x[:-3])
                        m = self.direct(mmn)
                        mods.append(m)
                        self.introspect(m)
        return mods