# BOTD - python3 IRC channel daemon.
#
# basic commands. 

__version__ = 1

import os
import sys
import time
import threading

import bl
import bl.tms

from bl.obj import Object
from bl.dbs import Db
from bl.flt import Fleet
from bl.krn import kernels
from bl.tms import elapsed
from bl.typ import get_cls, get_type
from bl.usr import Users

starttime = time.time()
k = kernels.get("0")

def cfg(event):
    if "IRC" in event.orig:
        event.reply("this command might flood, use a DCC connection.")
        return
    if not event.args:
        event.reply(str(k.cfg))
        return
    cn = "botd.%s.Cfg" % event.args[0]
    event.reply("using %s" % cn)
    db = Db()
    l = db.last(cn)
    if not l:     
        try:
            cls = get_cls(cn)
        except (AttributeError, ModuleNotFoundError):
            event.reply("no %s found" % cn)
            return
        l = cls()
        l.save()
        event.reply("created a %s file" % cn)
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
    event.reply(",".join(k.cmds))

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
    u = k.users.meet(origin, perms)
    event.reply("added %s" % u.user)

def ps(event):
    if "IRC" in event.orig:
        event.reply("this command might flood, use a DCC connection.")
        return
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
        res = "%s %s" % (nr, psformat % (bl.tms.elapsed(up), thrname[:60]))
        if res.strip():
            event.reply(res)

def up(event):
    event.reply(elapsed(time.time() - starttime))

def u(event):
    if "IRC" in event.orig:
        event.reply("this command might flood, use a DCC connection.")
        return
    res = ""
    db = Db()
    for o in db.all("bl.usr.User"):
        res += "%s," % o.user
    event.reply(res)

def v(event):
    event.reply("BOTD %s" % __version__)
