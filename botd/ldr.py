# BOTD - IRC channel daemon.
#
# module loader.

import cmd
import importlib
import logging
import os
import sys
import types

from botd.err import ENOMODULE
from botd.obj import Object
from botd.trc import get_exception
from botd.typ import get_name, get_type
from botd.utl import xdir

def __dir__():
    return ("Loader",)

class Loader(Object):

    table = Object()
    
    def direct(self, name):
        logging.warn("direct %s" % name)
        return importlib.import_module(name)

    def find_cmds(mod):
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1:
                    yield (key, o)

    def load_mod(self, mn, force=False):
        if mn in Loader.table:
            return Loader.table[mn]
        mod = None
        if mn in sys.modules:
            mod = sys.modules[mn]
        else:
            try:
                mod = self.direct(mn)
            except ModuleNotFoundError:
                pass
        if not mod:
            try:
                mod = self.direct("botd.%s" % mn)
            except ModuleNotFoundError:
                pass
        if not mod:
            return
        if force or mn not in Loader.table:
            Loader.table[mn] = mod
        return Loader.table[mn]
