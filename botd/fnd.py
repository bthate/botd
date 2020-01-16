# BOTD - python3 IRC channel daemon
#
# find command

import os
import time

from botd.dbs import Db
from botd.krn import kernels
from botd.obj import workdir
from botd.tms import elapsed

# defines

k = kernels.get_first()

# commands

def find(event):
    db = Db()
    if "k" in event.options:
        o = db.last(event.match)
        if o:
            event.reply("|".join(sorted({x for x in o.keys() if not x.startswith("_")})))
            return
    if not event.args:
        fns = os.listdir(os.path.join(workdir, "store"))
        fns = sorted({x.split(".")[-1].lower() for x in fns})
        if fns:
            event.reply("|".join(fns))
        return
    if len(event.args) == 1 and not event.selector:
        o = db.last(event.match)
        if o:
            res = sorted({x.split(".")[-1].lower() for x in o})
            if len(res) > 1:
                event.reply("|".join(res))
            else:
                for a in res:
                    if a not in event.selector:
                        event.selector[a] = None
                    if a not in event.dkeys:
                        event.dkeys.append(a)
    nr = -1
    for o in db.find(event.match, event.selector, event.index, event.delta):
        nr += 1
        event.display(o, str(nr))

def rm(event):
    if not event.args:
        event.reply("rm <selector>")
        return
    nr = -1
    db = Db()
    for o in db.find(event.match, event.selector, event.index, event.delta):
        if not o:
            continue
        nr += 1
        o._deleted = True
        o.save()
    event.reply("ok %s" % (nr+1))

def undel(event):
    if not event.args:
        event.reply("undel <selector>")
        return
    st = time.time()
    nr = -1
    db = Db()
    for o in db.deleted(event.match, event.selector):
        nr += 1
        o._deleted = False
        o.save()
    event.reply("ok %s %s" % (nr+1, elapsed(time.time()-st)))
