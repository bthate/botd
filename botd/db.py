# BOTD - python3 IRC channel daemon
#
# database commands.

import logging
import os

from bl.dbs import Db
from bl.krn import kernels

# defines

def __dir__():
    return ("find",)

# functions

def find(event):
    opts = os.listdir(os.path.join(k.cfg.workdir, "store"))
    try:
        match = event.txt.split(" ")[1]
    except (IndexError, AttributeError):
        event.reply("find %s" % "|".join([x.split(".")[-1].lower() for x in opts]))
        return
    opts = [x for x in opts if match in x.lower()]
    c = 0
    db = Db()
    for opt in opts:
        if len(event.txt.split()) > 2:
           for arg in event.txt.split()[2:]:
               selector = {arg: ""}
        else:
            selector = {"txt": ""}
        for o in db.find(opt, selector):
            event.display(o, str(c))
            c += 1
# runtime

k = kernels._get("0")
