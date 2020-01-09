# BOTD - python3 IRC channel daemon
#
# find command.

import os
import botd.obj

from botd.dbs import Db

# functions

def find(event):
    assert botd.obj.workdir
    opts = os.listdir(os.path.join(botd.obj.workdir, "store"))
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
