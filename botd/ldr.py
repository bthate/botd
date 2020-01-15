# BOTD - python3 IRC channel daemon.
#
# module loader.

import importlib
import logging
import os
import types

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
    
    def direct(self, name):
        logging.warn("direct %s" % name)
        return importlib.import_module(name)

    def get_mod(self, mn, force=True):
        if mn in Loader.table:
            return Loader.table[mn]
        mod = None
        try:
            mod = self.direct(mn)
        except ModuleNotFoundError:
            pass
        if not mod:
            raise ENOMODULE(mn)
        if force or mn not in Loader.table:
            Loader.table[mn] = mod
        return Loader.table[mn]
            
    def walk(self, mns, init=False):
        if not mns:
            return
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
