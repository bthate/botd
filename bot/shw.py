# BOTLIB - Framework to program bots.
#
#

import bot
import lo
import lo.tms
import os
import threading
import time

from bot import k
from bot.dft import defaults

def __dir__():
    return ("cfg", "cmds", "fleet", "ps", "up", "v")

def cfg(event):
    assert(lo.workdir)
    if not event.args:
        files = [x.split(".")[-2].lower() for x in os.listdir(os.path.join(lo.workdir, "store")) if x.endswith("Cfg")]
        if files:
            event.reply("|".join(["main",] + list(set(files))))
        else:
            event.reply("no configuration files yet.")
        return
    target = event.args[0]
    if target == "main":
        event.reply(lo.cfg)
        return
    cn = "bot.%s.Cfg" % target
    db = lo.Db()
    l = db.last(cn)
    if not l:     
        dft = defaults.get(target, None)
        if dft:
            c = lo.typ.get_cls(cn)
            l = c()
            l.update(dft)
            event.reply("created %s" % cn)
        else:
            event.reply("no %s found." % cn)
            return
    if len(event.args) == 1:
        event.reply(l)
        return
    if len(event.args) == 2:
        event.reply(l.get(event.args[1]))
        return
    setter = {event.args[1]: event.args[2]}
    l.edit(setter)
    p = l.save()
    event.reply("ok %s" % p)

def cmds(event):
    event.reply("|".join(sorted(lo.tbl.modules)))
    
def fleet(event):
    try:
        index = int(event.args[0])
        event.reply(str(k.fleet.bots[index]))
        return
    except (TypeError, ValueError, IndexError):
        pass
    event.reply([lo.typ.get_type(x) for x in k.fleet])

def ps(event):
    psformat = "%-8s %-50s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        d = vars(thr)
        o = lo.Object()
        o.update(d)
        if o.get("sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - bot.starttime)
        result.append((up, thr.getName(), o))
    nr = -1
    for up, thrname, o in sorted(result, key=lambda x: x[0]):
        nr += 1
        res = "%s %s" % (nr, psformat % (lo.tms.elapsed(up), thrname[:60]))
        if res.strip():
            event.reply(res)

def up(event):
    event.reply(lo.tms.elapsed(time.time() - bot.starttime))

def v(event):
    event.reply("%s %s" % (lo.cfg.name.upper(), lo.cfg.version))
