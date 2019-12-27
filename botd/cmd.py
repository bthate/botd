# BOTD - python3 IRC channel daemon.
#
# basic commands. 

__version__ = 1

import os
import sys
import time
import threading

from bl.dbs import Db
from bl.flt import Fleet
from bl.hdl import Handler
from bl.pst import workdir
from bl.obj import Object
from bl.tms import elapsed
from bl.typ import get_type
from bl.usr import Users

db = Db()
fleet = Fleet()
handler = Handler()
starttime = time.time()
users = Users()

def cfg(event):
    if len(event.args) >= 1:
        cn = "bl.%s.Cfg" % event.args[0]
    else:
        cn = "bl.krn.Cfg"
    l = db.last(cn)
    if not l:
        event.reply("no %s found." % cn)
        return
    if len(event.args) == 1:
        event.reply(l)
        return
    if len(event.args) == 2:
        event.reply(l.get(event.args[1]))
        return
    l.set(event.args[0], event.args[1])
    l.save()
    event.reply("ok")

def cmd(event):
    event.reply("|".join(sorted(handler.cmds)))

def flt(event):
    try:
        event.reply(str(fleet.bots[event.index-1]))
        return
    except (TypeError, ValueError, IndexError):
        pass
    event.reply([get_type(x) for x in fleet.bots])

def ls(event):
    event.reply("|".join(os.listdir(os.path.join(workdir, "store"))))

def meet(event):
    if not event.args:
        event.reply("meet origin [permissions]")
        return
    try:
        origin, *perms = event.args[:]
    except ValueError:
        event.reply("meet origin [permissions]")
        return
    origin = users.userhosts.get(origin, origin)
    u = users.meet(origin, perms)
    event.reply("added %s" % u.user)

def pid(event):
    event.reply(str(os.getpid()))

def thr(event):
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

def v(event):
    import __main__
    event.reply("BOTD %s" % __main__.__version__)
