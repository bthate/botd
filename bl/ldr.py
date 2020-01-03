# BOTD - python3 IRC channel daemon.
#
# module loader.

import bl
import inspect
import importlib
import logging
import pkgutil
import types
import typing

from bl.obj import Object, Register
from bl.trc import get_exception
from bl.typ import get_type

# defines

def __dir__():
    return ("Loader",)

# classes

class Loader(Object):

    names = Register()
    
    def __init__(self):
        super().__init__()
        self.cmds = Register()

    def direct(self, name):
        try:
            return importlib.import_module(name)
        except Exception as ex:
            logging.debug(get_exception())
            raise

    def get_mn(self, pn):
        names = []
        for mod in self.get_mods(pn):
            names.append(mod.__name__)
        return names

    def get_cmd(self, cn):
        return self.cmds._get(cn, None)

    def get_cmds(self, mod):
        cmds = Register()
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1:
                    if key not in cmds:
                        cmds._register(key, o)
        return cmds

    def get_mods(self, ms):
        mods = []
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
             mods.append(mod)
             for key, o in inspect.getmembers(mod, inspect.ismodule):
                 print(key, o)
                 if mn in str(o):
                     mods.append(o)
        return mods

    def get_names(self, mod):
        names = Register()
        for key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object):
                t = get_type(o)
                n = t.split(".")[-1].lower()
                if n not in names:
                    names._register(n, t)
        return names

    def walk(self, modstr):
        mods = self.get_mods(modstr)
        for mod in mods:
            names = self.get_names(mod)
            self.names._update(names)
            cmds = self.get_cmds(mod)
            self.cmds._update(cmds)
        return mods
