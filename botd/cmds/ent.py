# BOTD - python3 IRC channel daemon.
#
# data entry.

from botd.dbs import Db
from botd.krn import kernels
from botd.obj import Object

# defines

def __dir__():
    return ("Log", "Todo", "log", "todo")

k = kernels.get_first()

# classes

class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

# commands

def log(event):
    if not event.rest:
       db = Db()
       nr = 0
       for o in db.find("botd.cmds.ent.Log", {"txt": ""}):
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
       for o in db.find("botd.cmds.ent.Todo", {"txt": ""}):
            event.display(o, str(nr))
            nr += 1
       return
    obj = Todo()
    obj.txt = event.rest
    obj.save()
    event.reply("ok")

# runtime

k.add("log", log)
k.add("todo", todo)
