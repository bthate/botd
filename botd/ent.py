# BOTD - python3 IRC channel daemon.
#
# data entry.

"""
    data entry commands


    log and todo commands
    
"""

from botd.dbs import Db
from botd.obj import Object

# defines

def __dir__():
    return ("Log", "Todo", "log", "todo")

# classes

class Log(Object):

    """ item to log. """

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(Object):

    """ todo item. """

    def __init__(self):
        super().__init__()
        self.txt = ""

# commands

def log(event):
    """
        log command.
        
        shows a list of log entries when no argument is given or log <txt>.

    """
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
    """
        todo command.

        shows a list of todo's when no argument is given or todo <txt>.

    """
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
