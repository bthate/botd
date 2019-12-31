# BOTD - python3 IRC channel daemon.
#
# basic commands. 

import os
import time
import threading

from bl.obj import Object
from bl.dbs import Db

class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

def log(event):
    if not event.args:
        nr = 0
        db = Db()
        for o in db.find("botd.ent.Log", {"txt": ""}):
            event.display(o, "%s" % str(nr))
            nr += 1
        return
    obj = Log()
    obj.txt = " ".join(event.args)
    obj.save()
    event.reply("ok")

def todo(event):
    if not event.rest:
        nr = 0
        db = Db()
        for o in db.find("botd.ent.Todo", {"txt": ""}):
            event.display(o, "%s" % str(nr))
            nr += 1
        return
    obj = Todo()
    obj.txt = event.rest
    obj.save()
    event.reply("ok")
