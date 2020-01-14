# BOTD - python3 IRC channel daemon.
#
#

import threading
import time

from botd.krn import kernels, starttime
from botd.obj import Object
from botd.tms import elapsed

# defines

k = kernels.get_first()

# commands

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

# runtime

k.add("ps", ps)
