# BOTD - python3 IRC channel daemon.
#
# show status information.

import os
import threading
import time

from botd.krn import kernels, starttime
from botd.obj import Object
from botd.tms import elapsed
from botd.typ import get_type

# defines

def __dir__():
    return ("flt", "pid", "ps", "up")

# functions

def flt(event):
    k = kernels.get_first()
    try:
        index = int(event.args[0])
        event.reply(str(k.fleet.bots[index]))
        return
    except (TypeError, ValueError, IndexError):
        pass
    event.reply([get_type(x) for x in k.fleet.bots])

def pid(event):
    event.reply(str(os.getpid()))

def ps(event):
    k = kernels.get_first()
    psformat = "%-8s %-50s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        d = vars(thr)
        o = Object()
        o.update(d)
        if o.get("sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - starttime)
        result.append((up, thr.getName(), o))
    nr = -1
    for up, thrname, o in sorted(result, key=lambda x: x[0]):
        nr += 1
        res = "%s %s" % (nr, psformat % (elapsed(up), thrname[:60]))
        if res.strip():
            event.reply(res)

def up(event):
    event.reply(elapsed(time.time() - starttime))

