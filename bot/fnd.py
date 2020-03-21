# BOTLIB - Framework to program bots.
#
#

import lo
import os
import time

def __dir__():
    return ("find",)

def find(event):
    if not event.args:
        wd = os.path.join(lo.workdir, "store", "")
        lo.cdir(wd)
        fns = os.listdir(wd)
        fns = sorted({x.split(os.sep)[0].split(".")[-1].lower() for x in fns})
        if fns:
            event.reply("|".join(fns))
        return
    db = lo.Db()
    otypes = []
    target = db.all
    try:
       otype = event.args[0]
       otypes = lo.tbl.names.get(otype, [otype,])
    except:
       otype = None
    try:
       match = event.args[1]
       target = db.find_value
    except:
       match = None
    try:
        args = event.args[2:]
    except ValueError:
        args = None
    nr = -1
    for ot in otypes:
        for o in target(ot, match):
            nr += 1
            event.display(o, str(nr), args or o.keys())
