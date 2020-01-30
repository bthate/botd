# BOTD - IRC channel daemon.
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
    return ("Log", "Todo")

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

