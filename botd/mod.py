# BOTD - IRC channel daemon.
#
# module related

import inspect

from botd.krn import kernels

k = kernels.get_first()

def get_mods(mod):
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                yield (key,  o.__module__)

def get_modules():
    mods = {}
    for mod in k.table.values():
        for key, m in get_mods(mod):
            mods[key] = m
    return mods

def get_classes(mod):
    for key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, Object):
            yield (key, "%s.%s" % (mod.__name__, key))

def get_namez(mod):
    for key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, Object):
            yield (key.split(".")[-1].lower(), "%s.%s" % (mod.__name__, key))

def get_names():
    names = {}
    for mod in k.table.values():
       for key, m in get_namez(mod):
            names[key] = m
    return names
