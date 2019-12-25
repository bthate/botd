# BOTLIB - Framework to program bots.
#
# basic commands. 

import os
import time
import threading

from bl.krn import k, workdir, __version__
from bl.obj import Object
from bl.tms import elapsed
from bl.typ import get_type

def cfg(event):
    if not event.args:
        event.reply(k.cfg)
        return
    if len(event.args) >= 1:
        cn = "bl.%s.Cfg" % event.args[0]
        l = k.db.last(cn)
        if not l:
            event.reply("no %s config found." % event.args[0])
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
    event.reply("|".join(sorted(k.cmds)))

def flt(event):
    try:
        event.reply(str(k.fleet.bots[event.index-1]))
        return
    except (TypeError, ValueError, IndexError):
        pass
    event.reply([get_type(x) for x in k.fleet.bots])

def knl(event):
    event.reply(str(k))

def ls(event):
    event.reply("|".join(os.listdir(os.path.join(k.cfg.workdir, "store"))))

def meet(event):
    if not event.args:
        event.reply("meet origin [permissions]")
        return
    try:
        origin, *perms = event.args[:]
    except ValueError:
        event.reply("meet origin [permissions]")
        return
    origin = k.users.userhosts.get(origin, origin)
    u = k.users.meet(origin, perms)
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
            up = int(time.time() - bl.state.starttime)
        result.append((up, thr.getName(), o))
    nr = -1
    for up, thrname, o in sorted(result, key=lambda x: x[0]):
        nr += 1
        res = "%s %s" % (nr, psformat % (elapsed(up), thrname[:60]))
        if res.strip():
            event.reply(res)

def up(event):
    event.reply(elapsed(time.time() - bl.state.starttime))

def v(event):
        res = []
        res.append("BOTLIB %s" % __version__)
        for name, mod in k.table.items():
            if not mod:
                continue
            ver = getattr(mod, "__version__", None)
            if ver:
                txt = "%s %s" % (name, ver)
                res.append(txt.upper())
        if res:
            event.reply(" | ".join(res))
