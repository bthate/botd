# LIBOBJ - object library.
#
# trace

import os
import sys
import traceback

def get_exception(txt="", sep=""):
    exctype, excvalue, tb = sys.exc_info()
    trace = traceback.extract_tb(tb)
    result = ""
    for elem in trace:
        fname = elem[0]
        linenr = elem[1]
        func = elem[2]
        plugfile = fname[:-3].split(os.sep)
        mod = []
        for element in plugfile[::-1]:
            mod.append(element)
            if element == "lo" or element == "bot":
                break
        ownname = '.'.join(mod[::-1])
        result += "%s:%s %s %s " % (ownname, linenr, func, sep)
    res = "%s%s: %s %s" % (result, exctype, excvalue, str(txt))
    del trace
    return res
