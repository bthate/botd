# BOTD - IRC channel daemon.
#
# data entry.

from botd.dbs import Db
from botd.ent import Log, Todo
from botd.obj import Object

def __dir__():
    return ("log", "todo")

def log(event):
    if not event.rest:
       db = Db()
       nr = 0
       for o in db.find("botd.ent.Log", {"txt": ""}):
            event.display(o, str(nr))
            nr += 1
       return
    obj = Log()
    obj.txt = event.rest
    obj.save()
    event.reply("ok")

def todo(event):
    if not event.rest:
       db = Db()
       nr = 0
       for o in db.find("botd.ent.Todo", {"txt": ""}):
            event.display(o, str(nr))
            nr += 1
       return
    obj = Todo()
    obj.txt = event.rest
    obj.save()
    event.reply("ok")
