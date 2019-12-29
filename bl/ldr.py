# BOTD - python3 IRC channel daemon.
#
# module loader.

import inspect
import importlib
import logging
import pkgutil
import typing
import bl.tbl

from bl.obj import Object
from bl.pst import Persist, Register
from bl.typ import get_type
from bl.utl import get_name

def __dir__():
    return ("Loader",)

class Loader(Persist):

    def __init__(self):
        self.cmds = Register()
        self.table = {}

    def direct(self, name: str):
        return importlib.import_module(name)

    def get_cmd(self, cn):
        if self._autoload:
            mn = bl.tbl.modules.get(cn, None)
            if not mn:
                return
            if mn not in self.table:
                self.load_mod(mn)
        return self.cmds.get(cn, None)

    def load_mod(self, name, mod=None, force=False):
        logging.warning("load %s into %s" % (name, get_name(self)))
        if force or name not in self.table:
            self.table[name] = mod or self.direct(name)
        self.scan(self.table[name])
        return self.table[name]

    def scan(self, mod):
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1 and key not in self.cmds:
                    self.cmds.register(key, o)
                    bl.tbl.modules[key] = o.__module__
        for key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object):
                t = get_type(o)
                if t not in bl.tbl.classes:
                    bl.tbl.classes.append(t)
                    bl.tbl.names[t.split(".")[-1].lower()] = str(t)

    def sync(self, other):
        self.cmds.update(other.cmds)

    def unload(self, modname):
        if modname in self.table:
            del self.table[modname]

    def walk(self, pkgname):
        if not pkgname:
             return
        mod = self.load_mod(pkgname)
        mods = [mod,]
        try:
            mns = pkgutil.iter_modules(mod.__path__, mod.__name__+".")
        except:
            mns = pkgutil.iter_modules([mod.__file__,], mod.__name__+".")
        for n in mns:
            mods.append(self.load_mod(n[1], force=True))
        return mods
