# LIBOBJ - library to manipulate objects.
#
#

import importlib
import os
import sys
import types

def get_cls(name):
    try:
        modname, clsname = name.rsplit(".", 1)
    except:
        raise ENOCLASS(name)
    if modname in sys.modules:
        mod = sys.modules[modname]
    else:
        mod = importlib.import_module(modname)
    return getattr(mod, clsname)

def get_name(o):
    t = type(o)
    if t == types.ModuleType:
        return o.__name__
    try:
        n = "%s.%s" % (o.__self__.__class__.__name__, o.__name__)
    except AttributeError:
        try:
            n = "%s.%s" % (o.__class__.__name__, o.__name__)
        except AttributeError:
            try:
                n = o.__class__.__name__
            except AttributeError:
                n = o.__name__
    return n

def get_type(o):
    t = type(o)
    if t == type:
        return get_vartype(o)
    return str(type(o)).split()[-1][1:-2]

def get_clstype(o):
    try:
        return "%s.%s" % (o.__class__.__module__, o.__class__.__name__)
    except AttributeError:
        pass

def get_objtype(o):
    try:
        return "%s.%s" % (o.__self__.__module__, o.__self__.__name__)
    except AttributeError:
        pass

def get_vartype(o):
    try:
        return "%s.%s" % (o.__module__, o.__name__)
    except AttributeError:
        pass
