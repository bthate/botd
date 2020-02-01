# BOTD - IRC channel daemon
#
# find command

import os
import time

from botd.dbs import Db
from botd.krn import kernels
from botd.obj import workdir
from botd.tms import elapsed

k = kernels.get_first()

def find(event):
    if not event.args:
        fns = os.listdir(os.path.join(workdir, "store"))
        fns = sorted({x.split(".")[-1].lower() for x in fns})
        if fns:
            event.reply("|".join(fns))
        return
    if not len(event.args) > 1:
        event.reply("find <type> <match>")
        return
    match = event.args[0]
    nr = -1
    db = Db()
    for o in db.find_value(match, event.args[1]):
        nr += 1
        event.display(o, str(nr))
