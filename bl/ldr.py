# BOTD - python3 IRC channel daemon.
#
# module loader.

import importlib
import typing

from bl.pst import Persist

def __dir__():
    return ("Loader",)

class Loader(Persist):

    def __init__(self):
        super().__init__()
        self.table = {}

    def direct(self, name: str):
        return importlib.import_module(name)

    def load_mod(self, name, mod=None, force=False):
        if force or name not in self.table:
            self.table[name] = mod or self.direct(name)
        return self.table[name]

    def unload(self, modname):
        if modname in self.table:
            del self.table[modname]
