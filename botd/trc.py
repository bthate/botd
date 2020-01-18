# BOTD - IRC channel daemon.
#
# tracebacks and exception catcher.

""" trace module. """

import os
import sys
import traceback
import _thread

# defines

def __dir__():
    return ("get_exception", "get_from")

# functions

def get_exception(txt="", sep=""):
    """
        get_exception function
        
        returns the current exception in a 1 line error message.
        
    """
    exctype, excvalue, tb = sys.exc_info()
    trace = traceback.extract_tb(tb)
    result = ""
    for elem in trace:
        fname = elem[0]
        linenr = elem[1]
        func = elem[2]
        plugfile = fname[:-3].split(os.sep)
        mod = []
        for elememt in plugfile[::-1]:
            mod.append(elememt)
            if elememt == "bl":
                break
        ownname = '.'.join(mod[::-1])
        result += "%s:%s %s %s " % (ownname, linenr, func, sep)
    res = "%s%s: %s %s" % (result, exctype, excvalue, str(txt))
    del trace
    return res

def get_from(nr=2):
    """
        get_from function
        
        return code line number and file.
        
    """
    frame = sys._getframe(nr)
    if not frame:
        return frame
    if not frame.f_back:
        return frame
    filename = frame.f_back.f_code.co_filename
    linenr = frame.f_back.f_lineno
    plugfile = filename.split(os.sep)
    del frame
    return ".".join(plugfile[-2:]) + ":" + str(linenr)
