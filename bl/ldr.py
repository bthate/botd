# BOTD - python3 IRC channel daemon.
#
# module loader.

import bl
import inspect
import importlib
import logging
import pkgutil
import typing

from bl.obj import Object, Register
from bl.typ import get_type

def __dir__():
    return ("Loader",)

class Loader(Object):

    names = Register()

    def __init__(self):
        super().__init__()
        self.cmds = Register()

    def direct(self, name):
        return importlib.import_module(name)
            
    def get_cmd(self, cn):
        return self.cmds.get(cn, None)

    def get_cmds(self, mod):
        cmds = Register()
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1:
                    cmds.register(key, o)
        return cmds

    def get_mods(self, ms):
        mods = []
        for mn in ms.split(","):
             if not mn:
                 continue
             mod = self.direct(mn)
             if mod:
                 mods.append(mod)
        return mods

    def get_names(self, mod):
        names = Register()
        for key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object):
                t = get_type(o)
                n = t.split(".")[-1].lower()
                names.register(n, t)
        return names

    def walk(self, modstr):
        mods = self.get_mods(modstr)
        for mod in mods:
            names = self.get_names(mod)
            self.names.update(names)
            cmds = self.get_cmds(mod)
            self.cmds.update(cmds)
        return mods
