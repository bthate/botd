# BOTD - python3 IRC channel daemon.
#
# module loader.

import importlib
import logging
import os
import types

from botd.obj import Object
from botd.trc import get_exception
from botd.typ import get_name, get_type
from botd.utl import xdir

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
        return self.table.keys()

    def get_cmd(self, cn):
        return self.cmds.get(cn, None)

    def get_mod(self, mn):
        return self.direct(mn)

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

    def introspect(self, mod):
        for key in xdir(mod, "_"):
            o = getattr(mod, key)
            if type(o) == types.FunctionType and "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1:
                    if key in self.cmds:
                        continue
                    self.cmds[key] = o
                continue
            try:
                sc = issubclass(o, Object)
                if not sc:
                    continue
            except TypeError:
                continue
            n = key.split(".")[-1].lower()
            if n in self.names:
                continue
            self.names[n] = "%s.%s" % (mod.__name__, o.__name__)

    def walk(self, mns):
        mods = []
        for mn in mns.split(","):
            if not mn:
                continue
            m = self.get_mod(mn)
            if not m:
                continue
            loc = None
            if "__spec__" in dir(m):
                loc = m.__spec__.submodule_search_locations
            if not loc:
                self.introspect(m)
                mods.append(m)
                continue
            for md in loc:
                for x in os.listdir(md):
                    if x.endswith(".py"):
                        mmn = "%s.%s" % (mn, x[:-3])
                        m = self.get_mod(mmn)
                        if m:
                            self.introspect(m)
                            mods.append(m)
        return mods
