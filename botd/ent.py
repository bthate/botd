# BOTD - python3 IRC channel daemon.
#
# basic commands. 

import os
import time
import threading

from bl import Object
from bl.dbs import Db

db = Db()

class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

def log(event):
    if not event.rest:
        nr = 0
        if not event.dkeys:
            event.dkeys.append("txt")
        for o in db.find("botd.ent.Log", event.selector or {"txt": ""}):
            event.display(o, "%s" % str(nr))
            nr += 1
        return
    obj = Log()
    obj.txt = event.rest
    obj.save()
    event.reply("ok")

def todo(event):
    if not event.rest:
        nr = 0
        if "txt" not in event.dkeys:
            event.dkeys.append("txt")
        for o in db.find("botd.ent.Todo", event.selector or {"txt": ""}):
            event.display(o, "%s" % str(nr))
            nr += 1
        return
    obj = Todo()
    obj.txt = event.rest
    obj.save()
    event.reply("ok")
