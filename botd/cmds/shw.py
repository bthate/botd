# BOTD - python3 IRC channel daemon.
#
# show status information.

import os
import threading
import time

from botd.krn import kernels, starttime, __version__
from botd.obj import Object
from botd.tms import elapsed
from botd.typ import get_type

# defines

def __dir__():
    return ("flt", "pid", "up", "v")

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

def up(event):
    event.reply(elapsed(time.time() - starttime))

def v(event):
    event.reply("BOTD %s" % __version__)

# runtime

k = kernels.get_first()
k.add("flt", flt)
k.add("pid", pid)
k.add("up", up)
k.add("v", v)
