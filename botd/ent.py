# BOTLIB - Framework to program bots.
#
# data entry.

from bl.obj import Object

# defines

def __dir__():
    return ("Log", "Todo", "log", "todo")

# classes

class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

# functions

def log(event):
    obj = Log()
    obj.txt = event.rest
    obj.save()
    event.reply("ok")

def todo(event):
    obj = Todo()
    obj.txt = event.rest
    obj.save()
    event.reply("ok")
