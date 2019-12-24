# BOTLIB - Framework to program bots.
#
# basic commands. 

import bl
import os
import time
import threading

class Log(bl.Persist):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(bl.Persist):

    def __init__(self):
        super().__init__()
        self.txt = ""

def cfg(event):
    if not event.args:
        event.reply(bl.cfg)
        return
    if len(event.args) >= 1:
        cn = "bl.%s.Cfg" % event.args[0]
        l = bl.db.last(cn)
        if not l:
            event.reply("no %s config found." % event.args[0])
            return
        if len(event.args) == 1:
            event.reply(l)
            return
        if len(event.args) == 2:
            event.reply(bl.get(l, event.args[1]))
            return
        bl.set(l, event.args[0], event.args[1])
        bl.cfg.save()
        event.reply("ok")

def cmd(event):
    event.reply("|".join(sorted(bl.k.cmds)))

def flt(event):
    try:
        event.reply(str(bl.fleet.bots[event.index-1].json()))
        return
    except (TypeError, ValueError, IndexError):
        pass
    event.reply([bl.typ.get_type(x) for x in bl.fleet.bots])

def k(event):
    event.reply(str(bl.k))

def log(event):
    if not event.rest:
        nr = 0
        if not event.dkeys:
            event.dkeys.append("txt")
        for o in bl.db.find("bl.cmd.Log", event.selector or {"txt": ""}):
            event.display(o, "%s" % str(nr))
            nr += 1
        return
    obj = Log()
    obj.txt = event.rest
    obj.save()
    event.reply("ok")

def ls(event):
    event.reply("|".join(os.listdir(os.path.join(bl.cfg.workdir, "store"))))

def meet(event):
    if not event.args:
        event.reply("meet origin [permissions]")
        return
    try:
        origin, *perms = event.args[:]
    except ValueError:
        event.reply("meet origin [permissions]")
        return
    origin = bl.get(bl.users.userhosts, origin, origin)
    u = bl.users.meet(origin, perms)
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
        o = bl.Object()
        bl.update(o, d)
        if getattr(o, "sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - bl.state.starttime)
        result.append((up, thr.getName(), o))
    nr = -1
    for up, thrname, o in sorted(result, key=lambda x: x[0]):
        nr += 1
        res = "%s %s" % (nr, psformat % (bl.tms.elapsed(up), thrname[:60]))
        if res.strip():
            event.reply(res)

def todo(event):
    if not event.rest:
        nr = 0
        if "txt" not in event.dkeys:
            event.dkeys.append("txt")
        for o in bl.db.find("bl.cmd.Todo", event.selector or {"txt": ""}):
            event.display(o, "%s" % str(nr))
            nr += 1
        return
    obj = Todo()
    obj.txt = event.rest
    obj.save()
    event.reply("ok")

def up(event):
    event.reply(bl.tms.elapsed(time.time() - bl.state.starttime))

def v(event):
        res = []
        res.append("BOTLIB %s" % bl.__version__)
        for name, mod in bl.k.table.items():
            if not mod:
                continue
            ver = getattr(mod, "__version__", None)
            if ver:
                txt = "%s %s" % (name, ver)
                res.append(txt.upper())
        if res:
            event.reply(" | ".join(res))
