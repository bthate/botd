# BOTLIB - Framework to program bots.
#
#

import lo

class Log(lo.Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(lo.Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

def log(event):
    if not event.rest:
       db = lo.Db()
       nr = 0
       for o in db.find("bot.ent.Log", {"txt": ""}):
            event.display(o, str(nr), strict=True)
            nr += 1
       return
    o = Log()
    o.txt = event.rest
    o.save()
    event.reply("ok")

def todo(event):
    if not event.rest:
       db = lo.Db()
       nr = 0
       for o in db.find("bot.ent.Todo", {"txt": ""}):
            event.display(o, str(nr), strict=True)
            nr += 1
       return
    o = Todo()
    o.txt = event.rest
    o.save()
    event.reply("ok")
