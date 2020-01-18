# BOTD - IRC channel daemon.
#
# types.

""" type system using FQN module.class pairs """

import importlib
import sys
import types

from botd.err import ENOCLASS

# defines

def __dir__():
    return ("get_cls", "get_name", "get_type", "get_clstype", "get_objtype", "get_vartype")
    
# functions

def get_cls(name):
    """
        get_cls function.
        
        return a class from given module.class string.

    """
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
    """
        get_name
        
        return the module.class name of an object.

    """
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
    """
        get_type function.
        
        return the class of an object.
        
    """
    t = type(o)
    if t == type:
        return get_vartype(o)
    return str(type(o)).split()[-1][1:-2]

def get_clstype(o):
    """
        get_clstype function.
        
        return the type if the object is a class.
        
    """
    try:
        return "%s.%s" % (o.__class__.__module__, o.__class__.__name__)
    except AttributeError:
        pass

def get_objtype(o):
    """
        get_objtype function.
        
        return the type if the object is a an object.
    """        
    try:
        return "%s.%s" % (o.__self__.__module__, o.__self__.__name__)
    except AttributeError:
        pass

def get_vartype(o):
    """
        get_vartype function/
        
        return the type if the object is a variable.
    """
    try:
        return "%s.%s" % (o.__module__, o.__name__)
    except AttributeError:
        pass

