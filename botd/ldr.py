# BOTD - python3 IRC channel daemon.
#
# module loader.

import importlib
import logging
import os
import types
import botd.tbl

from botd.err import ENOMODULE
from botd.obj import Object
from botd.trc import get_exception
from botd.typ import get_name, get_type
from botd.utl import xdir

# defines

def __dir__():
    return ("Loader",)

# classes

class Loader(Object):

    table = Object()
    
    def __init__(self):
        super().__init__()
        self.cmds = Object()

    def direct(self, name):
        return importlib.import_module(name)

    def get_mn(self, pn):
        return self.table.keys()

    def get_cmd(self, cn):
        modname = botd.tbl.modules.get(cn, None)
        if modname and modname not in Loader.table:
            self.get_mod(modname)
        return self.cmds.get(cn, None)

    def get_mod(self, mn, force=True):
        if mn in Loader.table:
            return Loader.table[mn]
        mod = None
        try:
            mod = self.direct("botd.%s" % mn)
        except ModuleNotFoundError as ex:
            pass
        if not mod:
            mod =  self.direct(mn)
        if not mod:
            raise ENOMODULE(mn)
        if force or mn not in Loader.table:
            Loader.table[mn] = mod
            self.introspect(Loader.table[mn])
        return Loader.table[mn]
            
    def introspect(self, mod):
        for key in xdir(mod, "_"):
            o = getattr(mod, key)
            if type(o) == types.FunctionType and "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1:
                    if key in self.cmds:
                        continue
                    self.cmds[key] = o
                    botd.tbl.modules[key] = mod.__name__
                continue
            try:
                sc = issubclass(o, Object)
                if not sc:
                    continue
            except TypeError:
                continue
            n = key.split(".")[-1].lower()
            if n in botd.tbl.names:
                continue
            mn = "%s.%s" % (mod.__name__, o.__name__)
            botd.tbl.names[n] = mn 
            botd.tbl.classes.append(mn)

    def walk(self, mns, init=False):
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
                mods.append(m)
                continue
            for md in loc:
                for x in os.listdir(md):
                    if x.endswith(".py"):
                        mmn = "%s.%s" % (mn, x[:-3])
                        m = self.get_mod(mmn)
                        if m:
                            mods.append(m)
        if init:
            for mod in mods:
                if "init" in dir(mod):
                    mod.init(self)
        return mods
