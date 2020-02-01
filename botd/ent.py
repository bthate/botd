# BOTD - IRC channel daemon.
#
# data entry.

from botd.dbs import Db
from botd.obj import Object

def __dir__():
    return ("Log", "Todo")

class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

