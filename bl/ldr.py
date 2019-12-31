# BOTD - python3 IRC channel daemon.
#
# module loader.

import bl
import inspect
import importlib
import logging
import pkgutil
import typing

def __dir__():
    return ("Loader",)

class Loader(bl.Object):

    def __init__(self):
        super().__init__()
        self.cmds = bl.Register()

    def direct(self, name):
        return importlib.import_module(name)
            
    def get_cmd(self, cn):
        if not cn:
            return None
        return self.cmds.get(cn, None)

    def get_cmds(self, mod):
        cmds = bl.Register()
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1:
                    cmds.register(key, o)
        return cmds

    def get_mods(self, ms):
        for mn in ms.split(","):
             if not mn:
                 continue
             mod = self.direct(mn)
             if mod:
                 yield mod

    def get_names(self, mod):
        names = bl.Register()
        for key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object):
                t = get_type(o)
                n = t.split(".")[-1].lower()
                names.register(n, t)
        return names

    def unload(self, modname):
        if modname in Loader.table:
            del Loader.table[modname]
