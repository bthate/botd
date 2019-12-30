# BOTD - python3 IRC channel daemon.
#
# module loader.

import inspect
import importlib
import logging
import pkgutil
import typing
import bl.tbl

from bl import Object, Register
from bl.typ import get_type
from bl.utl import get_name

def __dir__():
    return ("Loader",)

class Loader(Object):

    table = {}

    def __init__(self):
        super().__init__()
        self.cmds = Register()

    def direct(self, name):
        return importlib.import_module(name)

    def get_cmd(self, cn):
        if self._autoload:
            mn = bl.tbl.modules.get(cn, None)
            if not mn:
                return
            if mn not in Loader.table:
                self.load_mod(mn)
        return self.cmds.get(cn, None)

    def load_mod(self, name, mod=None, force=False):
        if force or name not in Loader.table:
            logging.warning("load %s into %s" % (name, get_name(self)))
            Loader.table[name] = mod or self.direct(name)
        return Loader.table[name]

    def scan(self, mod):
        added = []
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1 and key not in self.cmds:
                    added.append(key)
                    self.cmds.register(key, o)
                    bl.tbl.modules[key] = o.__module__
        for key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object):
                t = get_type(o)
                if t not in bl.tbl.classes:
                    bl.tbl.classes.append(t)
                    bl.tbl.names[t.split(".")[-1].lower()] = str(t)
        if added:
            logging.warning("found %s" % ",".join(added))

    def sync(self, other):
        self.cmds.update(other.cmds)

    def unload(self, modname):
        if modname in Loader.table:
            del Loader.table[modname]

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
            mods.append(self.load_mod(n[1]))
        for mod in mods:
            self.scan(mod)
        return mods
