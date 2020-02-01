# BOTD - IRC channel daemon.
#
# module related

"""
    module related functions.
    
    provices module introspection.
    
"""

import inspect

from botd.krn import kernels

# defines

k = kernels.get_first()

# functions

def get_mods(mod):
    """
        return commands as a key,modname pairs.
        
        uses yield.

    """ 
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                yield (key,  o.__module__)

def get_modules():
    """
        get_modules function.

        return all module names scanning all registered modules.
               
    """
    mods = {}
    for mod in k.table.values():
        for key, m in get_mods(mod):
            mods[key] = m
    return mods

def get_classes(mod):
    """
        return list of classname,FQN pairs.
        
        scans the module for classes that are Object instances.

    """
    for key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, Object):
            yield (key, "%s.%s" % (mod.__name__, key))

def get_namez(mod):
    """
        return last part of the FQN of classes found in the module.

        usefull as aliases.
  
    """
    for key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, Object):
            yield (key.split(".")[-1].lower(), "%s.%s" % (mod.__name__, key))

def get_names():
    """
        get_names.
        
        return all names scanning all available modules.
        
    """
    names = {}
    for mod in k.table.values():
       for key, m in get_namez(mod):
            names[key] = m
    return names
