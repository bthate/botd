# BOTLIB - the bot library !
#
#

import importlib, inspect, os

from .obj import Object

def direct(name):
    return importlib.import_module(name)

def find_names(mod):
    names = {}
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                names[key] = o.__module__
    return names

def find_allnames(name):
    mns = Object()
    pkg = direct(name)
    for mod in find_modules(pkg):
        mns.update(find_names(mod))
    return mns

def find_callbacks(mod):
    cbs = {}
    for key, o in inspect.getmembers(mod, inspect.isfunction):
       if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 2:
                cbs[key] = o
    return cbs

def find_cls(mod):
    res = {}
    for key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, Object):
            res[o.__name__] = o.__module__
    return res

def find_cmds(mod):
    cmds = {}
    for key, o in inspect.getmembers(mod, inspect.isfunction):
       if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                cmds[key] = o
    return cmds

def find_modules(pkgs, filter=None):
    mods = []
    for pkg in pkgs.split(","):
        if filter and filter not in mn:
            continue
        try:
            p = direct(pkg)
        except ModuleNotFoundError:
            continue
        for key, m in inspect.getmembers(p, inspect.ismodule):
            if m not in mods:
                mods.append(m)
    return mods

def find_shorts(mn):
    shorts = {}
    for mod in find_modules(mn):
        for key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object) and key == o.__name__.lower():
                t = "%s.%s" % (o.__module__, o.__name__)
                shorts[o.__name__.lower()] = t.lower()
    return shorts

def find_types(mod):
    res = {}
    for key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, Object):
            t = "%s.%s" % (o.__module__, o.__name__)
            res[t] = o.__module__
    return res

def resources(name):
    resources = {}
    for x in pkg_resources.resource_listdir(name, ""):
        if x.startswith("_") or not x.endswith(".py"):
            continue
        mmn = "%s.%s" % (mn, x[:-3])
        resources[mmn] = direct(mmn)
    return mmn

def walk(name):
    mods = {}
    mod = direct(name)
    for pkg in mod.__path__:
        for x in os.listdir(pkg):
            if x.startswith("_") or not x.endswith(".py"):
                continue
            mmn = "%s.%s" % (mod.__name__, x[:-3])
            mods[mmn] = direct(mmn)
    return mods
