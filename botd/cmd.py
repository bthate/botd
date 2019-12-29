# BOTD - python3 IRC channel daemon.
#
# basic commands. 

__version__ = 1

import os
import sys
import time
import threading
import bl.pst
import bl.tbl

from bl.dbs import Db
from bl.krn import Kernel
from bl.gnr import edit, keys
from bl.hdl import Handler
from bl.obj import Object
from bl.tms import elapsed
from bl.typ import get_type

from botd.flt import Fleet
from botd.usr import Users

starttime = time.time()

db = Db()
bots = Fleet()
k = Kernel()
users = Users()

def cfg(event):
    event.reply(str(k.cfg))

def ed(event):
    if not event.args:
        ls(event)
        return
    l = db.last(event.args[0])
    if not l:
        event.reply("no %s found." % event.args[0])
        return
    if len(event.args) == 1:
        event.reply(l)
        return
    if len(event.args) == 2:
        event.reply(l.get(event.args[1]))
        return
    setter = {event.args[1]: event.args[2]}
    edit(l, setter)
    l.save()
    event.reply("ok")

def cmds(event):
    event.reply("|".join(sorted(bl.tbl.modules)))

def fleet(event):
    try:
        event.reply(str(bots.bots[event.index-1]))
        return
    except (TypeError, ValueError, IndexError):
        pass
    event.reply(str([get_type(x) for x in bots.bots]))

def ls(event):
    event.reply("|".join(os.listdir(os.path.join(bl.pst.workdir, "store"))))

def meet(event):
    if not event.args:
        event.reply("meet origin [permissions]")
        return
    try:
        origin, *perms = event.args[:]
    except ValueError:
        event.reply("meet origin [permissions]")
        return
    origin = Users.userhosts.get(origin, origin)
    u = users.meet(origin, perms)
    event.reply("added %s" % u.user)

def pid(event):
    event.reply(str(os.getpid()))

def ps(event):
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

def users(event):
    res = ""
    for o in db.all("botd.usr.User"):
        res += "%s," % o.user
    event.reply(res)

def v(event):
    event.reply("BOTD %s" % __version__)
