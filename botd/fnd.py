# BOTD - IRC channel daemon
#
# find command

"""
    find command.
    
    query objects.

 """


import os
import time

from botd.dbs import Db
from botd.krn import kernels
from botd.obj import workdir
from botd.tbl import names
from botd.tms import elapsed

# defines

k = kernels.get_first()

# commands

def find(event):
    """
        find <type> <selector>
        
        find uses a type to search for and a selector (key,value) dict to match and select objects. 
    
    """
    if not event.args:
        fns = os.listdir(os.path.join(workdir, "store"))
        fns = sorted({x.split(".")[-1].lower() for x in fns})
        if fns:
            event.reply("|".join(fns))
        return
    if not len(event.args) > 1:
        event.reply("find <type> <match>")
        return
    match = event.args[0]
    match = names.get(match, match)
    nr = -1
    db = Db()
    for o in db.find_value(match, event.args[1]):
        nr += 1
        event.display(o, str(nr))
